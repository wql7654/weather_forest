#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ======== CONVERT LONLAT
# ======== Version 1.0.0
# ======== Author : Song Junghyun of SELab
# ======== Latest Update : 2017-07-11 10:50


# =================================================
# IMPORT MODULES
# =================================================


# SYSTEM MODULES
import sys

# THIRD PARTY MODULES
import numpy as np
import requests

# USERS MODULES


# =================================================
# FUNCTION - LAMBERT CONFORMAL PROJECTION
# =================================================


#  [ Lambert Conformal Conic Projection ]
#
#      o lon, lat                 : (longitude,latitude) at earth  [degree]
#      o x, y                     : (x,y) cordinate in map  [grid]
#      o inputSourceType = lonlat : (lon,lat) --> (x,y)
#                          xy     : (x,y) --> (lon,lat)

def lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter):
    
    PI = np.arcsin(1.0) * 2.0
    degreeToRadian = PI / 180.0
    radianToDegree = 180.0 / PI
    radiusOfEarth = mapParameter.radiusOfEarth / mapParameter.gridSpacing
    standardLatitude1 = mapParameter.standardLatitude1 * degreeToRadian
    standardLatitude2 = mapParameter.standardLatitude2 * degreeToRadian
    longitudeOfReferencePoint = mapParameter.longitudeOfReferencePoint * degreeToRadian
    latitudeOfReferencePoint = mapParameter.latitudeOfReferencePoint * degreeToRadian
    sn = np.tan(PI * 0.25 + standardLatitude2 * 0.5) / np.tan(PI * 0.25 + standardLatitude1 * 0.5)
    sn = np.log(np.cos(standardLatitude1) / np.cos(standardLatitude2)) / np.log(sn)
    sf = np.tan(PI * 0.25 + standardLatitude1 * 0.5)
    sf = pow(sf, sn) * np.cos(standardLatitude1) / sn
    ro = np.tan(PI * 0.25 + latitudeOfReferencePoint * 0.5)
    ro = radiusOfEarth * sf / pow(ro, sn)

    # INPUT LONGITUDE AND LATITUDE
    if (inputSourceType == "lonlat"):
        inputSource1 = float(inputSource1)
        inputSource2 = float(inputSource2)
        
        # OUTPUT XY
        if (outputType == "xy"):
            ra = np.tan(PI * 0.25 + inputSource2 * degreeToRadian * 0.5)
            ra = radiusOfEarth * sf / pow(ra, sn)
            theta = inputSource1 * degreeToRadian - longitudeOfReferencePoint
            if (theta > PI):
                theta = theta - (2.0 * PI)
            if (theta < -PI):
                theta = theta + (2.0 * PI)
            theta = theta * sn
            x = (ra * np.sin(theta)) + mapParameter.xCoordinateOfReferencePoint
            x = round(x)
            y = (ro - ra * np.cos(theta)) + mapParameter.yCoordinateOfReferencePoint
            y = round(y)
        
            return (x, y)

        # OUTPUT ADDRESS
        if (outputType == "address"):
            googleMapApiURL = u'https://maps.googleapis.com/maps/api/geocode/json?'
            parameters = {'latlng': str("%3.6f,%3.6f" % (inputSource2, inputSource1)), 'language' : 'ko'}
            try:
                getPage = requests.get(googleMapApiURL, params=parameters)
            except:
                sys.stderr.write("http requests time out : {0} {1}.\n".format(googleMapApiURL,parameters))
                exit(1)
            getPageJson = getPage.json()

            addressArray = []
            for resulti in getPageJson["results"]:
                address = resulti["address_components"][0]
                for typei in address["types"]:
                    if typei == "sublocality_level_2":
                        addressArray.append(resulti["formatted_address"])

            return (addressArray)

    # INPUT XY AND OUTPUT LONGITUDE AND LATITUDE
    if (inputSourceType == "xy"):
        inputSource1 = float(inputSource1)
        inputSource2 = float(inputSource2)

        xn = inputSource1 - mapParameter.xCoordinateOfReferencePoint
        yn = ro - inputSource2 + mapParameter.yCoordinateOfReferencePoint
        ra = np.sqrt(xn * xn + yn * yn)
        if (sn < 0.0):
            ra = -ra
        alat = pow((radiusOfEarth * sf / ra), (1.0 / sn))
        alat = 2.0 * np.arctan(alat) - PI * 0.5
        if (abs(xn) <= 0.0):
            theta = 0.0
        else:
            if (abs(yn) <= 0.0):
                theta = PI * 0.5
                if (xn < 0.0):
                    theta = -theta
            else:
                theta = np.arctan2(xn, yn)
        alon = theta / sn + longitudeOfReferencePoint
        longitude = alon * radianToDegree
        latitude = alat * radianToDegree

        return (longitude, latitude)

    # INPUT XY AND OUTPUT LONGITUDE AND LATITUDE
    if (inputSourceType == "address"):
        googleMapApiURL = u'https://maps.googleapis.com/maps/api/geocode/json?'
        parameters = {'address': inputSource1, 'language' : 'ko'}
        try:
            getPage = requests.get(googleMapApiURL, params=parameters)
        except:
            sys.stderr.write("http requests time out : {0} {1}.\n".format(googleMapApiURL,parameters))
            exit(1)
        getPageJson = getPage.json()

        for resulti in getPageJson["results"]:
            geometry = resulti["geometry"]
            location = geometry["location"]
            longitude = location["lng"]
            latitude = location["lat"]
            
        return (longitude, latitude)

    
# =================================================
# CLASS - LAMBERT CONFORMAL PARAMETER
# =================================================


class lambertConformalParameter:
    def __init__(self):

        # RADIUS OF EARTH [km]
        radiusOfEarth = 6371
        # GRID SPACING [km]
        gridSpacing = 5
        # STANDARD LATITUDE 1 [degree]
        standardLatitude1 = 30.0
        # STANDARD LATITUDE 2 [degree]
        standardLatitude2 = 60.0
        # LONGITUDE OF REFERENCE POINT [degree]
        longitudeOfReferencePoint = 126.0
        # LATITUDE OF REFERENCE POINT [degree]
        latitudeOfReferencePoint = 38.0
        # X COORDINATE OF REFERENCE POINT [POINT]
        xCoordinateOfReferencePoint = 43
        # Y COORDINATE OF REFERENCE POINT [POINT]
        yCoordinateOfReferencePoint = 136
        # START FLAG (1 = START)

        ## SELF DEFINE
        self.radiusOfEarth = radiusOfEarth
        self.gridSpacing = gridSpacing
        self.standardLatitude1 = standardLatitude1
        self.standardLatitude2 = standardLatitude2
        self.longitudeOfReferencePoint = longitudeOfReferencePoint
        self.latitudeOfReferencePoint = latitudeOfReferencePoint
        self.xCoordinateOfReferencePoint = xCoordinateOfReferencePoint
        self.yCoordinateOfReferencePoint = yCoordinateOfReferencePoint


# =================================================
# RUN PROGRAM
# =================================================


# WARNING
getArgs = len(sys.argv) - 1
if (getArgs == 0):

    # 1. INPUT LONGITUDE AND LATITUDE, OUTPUT XY
    print ("\n1. CONVERT LONLAT TO XY")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT LON] [INPUT LAT] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py lonlat 126.9156168 37.476128 xy")

    # 2. INPUT LONGITUDE AND LATITUDE, OUTPUT address
    print ("\n2. CONVERT LONLAT TO ADDRESS")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT LON] [INPUT LAT] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py lonlat 126.9156168 37.476128 address")

    # 3. INPUT XY, OUTPUT LONGITUDE AND LATITUDE
    print ("\n3. CONVERT XY TO LONLAT")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT X] [INPUT Y] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py xy 59 125 lonlat")

    # 4. INPUT XY, OUTPUT ADDRESS
    print ("\n4. CONVERT XY TO ADDRESS")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT X] [INPUT Y] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py xy 59 125 address")

    # 5. INPUT ADDRESS, OUTPUT LONGITUDE AND LATITUDE
    print ("\n5. CONVERT ADDRESS TO LONLAT")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT LEVEL 1] [INPUT LEVEL 2] [INPUT LEVEL 3] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py address 서울특별시 관악구 미성동 lonlat")

    # 6. INPUT ADDRESS, OUTPUT XY
    print ("\n6. CONVERT ADDRESS TO XY")
    print ("PLEASE INPUT ARGUMENTS : ./convertLocationData.py [INPUT SOURCE TYPE] [INPUT LEVEL 1] [INPUT LEVEL 2] [INPUT LEVEL 3] [OUTPUT TYPE]")
    print ("EXAMPLE ARGUMENTS      : ./convertLocationData.py address 서울특별시 관악구 미성동 xy")
    print ("")
    sys.exit()

    
if (sys.argv[1] != "address"):

    # INPUT SOURCE TYPE
    inputSourceType = sys.argv[1] # lonlat / xy / address
    # inputSourceType = "lonlat"

    # INPUT SOURCE
    inputSource1 = sys.argv[2] # 126.9156168 / 72
    inputSource2 = sys.argv[3] # 37.476128 / 139
    # inputSource1 = "126.9156168"
    # inputSource2 = "37.476128"

    # OUTPUT TYPE
    outputType = sys.argv[4] # xy / lonlat
    # outputType = "address"

else:
    # INPUT SOURCE TYPE
    inputSourceType = sys.argv[1] # address
    # inputSourceType = "address"

    # INPUT SOURCE
    inputSource1 = sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4] # 대한민국 서울특별시 관악구 미성동
    inputSource2 = ""
    # inputSource1 = "대한민국 서울특별시 관악구 미성동"
    # inputSource2 = ""

    # OUTPUT TYPE
    outputType = sys.argv[5] # xy / lonlat
    # outputType = "lonlat"
    
    
# MAP PARAMETERS
mapParameter = lambertConformalParameter()

# INPUT LONGITUDE AND LATITUDE
if (inputSourceType == "lonlat"):

    # 1. INPUT LONGITUDE AND LATITUDE, OUTPUT XY
    if (outputType == "xy"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        print ("\nCONVERT LONLAT TO XY")
        print (("INPUT LONLAT : %s, %s") % (inputSource1, inputSource2))
        print (("OUTPUT XY    : %d, %d\n") % (convertedValue[0], convertedValue[1]))

    # 2. INPUT LONGITUDE AND LATITUDE, OUTPUT address
    if (outputType == "address"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        print ("\nCONVERT LONLAT TO ADDRESS")
        print (("INPUT LONLAT   : %s, %s") % (inputSource1, inputSource2))
        convertedValue = list(set(convertedValue))
        for addressi in range(len(convertedValue)):
            splitAddress = convertedValue[addressi].split(" ")
            outputAddress = splitAddress[1] + " " + splitAddress[2] + " " + splitAddress[3]
            print ("OUTPUT ADDRESS : %s" % outputAddress)
        print ("")

# INPUT XY
if (inputSourceType == "xy"):

    # 3. INPUT XY, OUTPUT LONGITUDE AND LATITUDE
    if (outputType == "lonlat"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        print ("\nCONVERT XY TO LONLAT")
        print (("INPUT XY      : %s, %s") % (inputSource1, inputSource2))
        print (("OUTPUT LONLAT : %s, %s\n") % (str(convertedValue[0]), str(convertedValue[1])))

    # 4. INPUT XY, OUTPUT ADDRESS
    if (outputType == "address"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        outputType = "lonlat"
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        inputSourceType = "lonlat"
        outputType = "address"
        convertedValue = lambertConformalProjection(inputSourceType, convertedValue[0], convertedValue[1], outputType,
                                                    mapParameter)
        print ("\nCONVERT XY TO ADDRESS")
        print (("INPUT XY       : %s, %s") % (inputSource1, inputSource2))
        convertedValue = list(set(convertedValue))
        for addressi in range(len(convertedValue)):
            splitAddress = convertedValue[addressi].split(" ")
            outputAddress = splitAddress[1] + " " + splitAddress[2] + " " + splitAddress[3]
            print ("OUTPUT ADDRESS : %s" % outputAddress)
        print ("")

# INPUT ADDRESS
if (inputSourceType == "address"):

    # 5. INPUT ADDRESS, OUTPUT LONGITUDE AND LATITUDE
    if (outputType == "lonlat"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        print ("\nCONVERT ADDRESS TO LONLAT")
        print (("INPUT ADDRESS : %s") % (inputSource1))
        print (("OUTPUT LONLAT : %s, %s\n") % (str(convertedValue[0]), str(convertedValue[1])))
    
    # 6. INPUT ADDRESS, OUTPUT XY
    if (outputType == "xy"):
        # FUNCTION LAMBERT CONFORMAL PROJECTION
        outputType = "lonlat"
        convertedValue = lambertConformalProjection(inputSourceType, inputSource1, inputSource2, outputType, mapParameter)
        inputSourceType = "lonlat"
        outputType = "xy"
        convertedValue = lambertConformalProjection(inputSourceType, convertedValue[0], convertedValue[1], outputType,
                                                    mapParameter)
        print ("\nCONVERT ADDRESS TO XY")
        print (("INPUT ADDRESS : %s") % (inputSource1))
        print (("OUTPUT XY     : %d, %d\n") % (convertedValue[0], convertedValue[1]))
