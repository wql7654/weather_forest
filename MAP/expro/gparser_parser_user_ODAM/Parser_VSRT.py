#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 파이썬 버전 : 2.7.10
# 외부 라이브러리 : 사용안함 
# 외부 프로그램 : python
# 프로그램 버전 : v0.5
# 한글을 사랑합시다...

# 종료코드 목록
# 0 : 정상종료
# 1 : 프로그램 옵션이 부족하거나 잘못 입력됨
# 2 : 입력 파일 문제
# 3 : 외부 프로그램 문제

import os
import sys
import unittest
import subprocess
import ConfigParser
from datetime import datetime, timedelta
from optparse import OptionParser
#import DateChker

# 변수 설정 -> 변수 체크용

PROG_DIR = os.path.dirname(os.path.realpath(__file__))
VSRT_Val_Format = ['PTY', 'SKY', 'RN1', 'LGT']
VSRT_Val_Null = {'PTY':'-1', 'SKY':'-1', 'RN1':'-1', 'LGT':'-1'}

VSRT_Predict_Hour_Format = ['0', '1', '2', '3']
VSRT_Predict_Hour_Size = {'00':3, '01':2, '02':4, '03':3, '04':2, '05':4, '06':3, '07':2, '08':4, '09':3, '10':2,
                          '11':4, '12':3, '13':2, '14':4, '15':3, '16':2, '17':4, '18':3, '19':2, '20':4, '21':3,
                          '22':2, '23':4}
VSRT_Size = 37697

def OptionSetter():
    # 옵션을 처리하는 부분
    # 해당 부분을 통해 옵션 데이터를 받고 값을 반환한다.
    # 모든 변수 다 받으며, 하루치 다 변환, KST로도 전환
    usage = """
    %prog [StartTime] [EndTime] [LowX] [LowY] [HighX] [HighY] [Value] [OutputPath]
    ex) %prog 2015071712 2015071806 50 50 100 100 PTY ./output/
    X Range : 0 ~ 148
    Y Range : 0 ~ 252
    Value List : {0}""".format(', '.join(VSRT_Val_Format))
    
    Options = OptionParser(usage = usage)
    
    return Options
    # 옵션 처리 함수 완료
        
def ksttoutc(kst):
    kst = datetime.strptime(kst,'%Y%m%d%H')
    utc = kst + timedelta(hours=-9)
    year = utc.strftime('%Y')
    month = utc.strftime('%m')
    day = utc.strftime('%d')
    hour = utc.strftime('%H')

    return year, month, day, hour

def InitSetter(Year, Month, Day, IsOld, IsNew):
    # ini 파일을 읽어서 변수로 저장하는 부분
    # 해당 부분을 통해 기본적인 세팅값을 받는다.
    PathParserConfig = ConfigParser.ConfigParser()
    PathParserConfig.read(os.path.join(PROG_DIR, 'PathList.ini'))
    
    return PathParserConfig.get('PATH', 'VSRT').replace("%YEAR",Year).replace("%MONTH", Month).replace("%DAY", Day)

    #ini 처리 함수 완료 
    
def DateTimeSplit(DateTime):
    # 옵션으로 받는 날짜/시간을 분리하는 함수
    try: 
        StrYear = DateTime[0:4]
    except:
        print('DateTime Error!! : YEAR')
        sys.exit(1)
        
    try:
        StrMonth = DateTime[4:6]
    except:
        print('DateTime Error!! : MONTH')
        sys.exit(1)
        
    try:
        StrDay = DateTime[6:8]
    except:
        print('DateTime Error!! : DAY')
        sys.exit(1)
    try:
        StrHour = DateTime[8:10]
    except:
        print('DateTime Error!! : Hour')
        sys.exit(1)
    
    return StrYear, StrMonth, StrDay,StrHour
    # 날짜 시간 분리 함수 완료
    
def GetHourList(StartTime, EndTime):
    # 시간 리스트 생성
    TimeList = list()
    RunTime = StartTime
    while RunTime <= EndTime:
        TimeList.append(RunTime.strftime("%Y%m%d%H"))
        RunTime += timedelta(hours = 1)
    return TimeList

def GetXYGridList(LowX, LowY, HighX, HighY):
    # 지점 리스트 생성
    GridList = list()
    ListX = range(LowX, HighX + 1)
    ListY = range(LowY, HighY + 1)

    for iY in ListY:
        for iX in ListX:
            GridList.append(iX + (iY * 149))

    return GridList

def ArgCheck(option):
    # 옵션 받은 현황 체크 
    options, args = option.parse_args()
    
    if (len(args) < 8):
        option.print_help()
        sys.exit(1)

    try:
        StartTime = datetime.strptime(args[0],'%Y%m%d%H')
    except:
        sys.stderr.write('Agument Check Error(StartTime) : {0[0]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        EndTime = datetime.strptime(args[1],'%Y%m%d%H')
    except:
        sys.stderr.write('Agument Check Error(EndTime) : {0[1]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        LowX = int(args[2])

        if (0 > LowX or LowX > 148):
            sys.stderr.write('Agument Range Error(LowX) : {0[2]}\n'.format(args))
            option.print_help()
            sys.exit(1)
            
    except:
        sys.stderr.write('Agument Check Error(LowX) : {0[2]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        LowY = int(args[3])

        if (0 > LowY or LowY > 252):
            sys.stderr.write('Agument Range Error(LowY) : {0[3]}\n'.format(args))
            option.print_help()
            sys.exit(1)
            
    except:
        sys.stderr.write('Agument Check Error(LowY) : {0[3]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        HighX = int(args[4])

        if (0 > HighX or HighX > 148):
            sys.stderr.write('Agument Range Error(HighX) : {0[4]}\n'.format(args))
            option.print_help()
            sys.exit(1)

    except:
        sys.stderr.write('Agument Check Error(HighX) : {0[4]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        HighY = int(args[5])

        if (0 > HighY or HighY > 252):
            sys.stderr.write('Agument Range Error(HighY) : {0[5]}\n'.format(args))
            option.print_help()
            sys.exit(1)
            
    except:
        sys.stderr.write('Agument Check Error(HighY) : {0[5]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        Value = args[6]

        if (Value not in VSRT_Val_Format):
            sys.stderr.write('Agument Value Error(Value) : {0[6]}\n'.format(args))
            option.print_help()
            sys.exit(1)
            
    except:
        sys.stderr.write('Agument Check Error(Value) : {0[6]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    try:
        OutputPath = args[7]

        if (os.path.exists(OutputPath) == False):
            sys.stderr.write('Agument Value Error(OutputPath) : {0[7]}\n'.format(args))
            option.print_help()
            sys.exit(1)
            
    except:
        sys.stderr.write('Agument Check Error(OutputPath) : {0[7]}\n'.format(args))
        option.print_help()
        sys.exit(1)

    if (LowX > HighX):
        sys.stdout.write('Warning : LowX higher then HighX\n')
        LowX, HighX = HighX, LowX

    if (LowY > HighY):
        sys.stdout.write('Warning : LowY higher then HighY\n')
        LowY, HighY = HighY, LowY

    return StartTime, EndTime, LowX, LowY, HighX, HighY, Value, OutputPath
    # 옵션 현황 체크 완료 
    
def MakeGribParseOption(Year, Month, Day, Hour, Var, Path, output, PHour, IsOld, IsNew):
    # 주어진 조건에 맞춰 옵션 문자열을 생성한다.
    if IsOld:
        StrInput = Path + "/DFS_VSRT_GRD_GRB1_{0}.{1}{2}{3}{4}30".format(Var, Year, Month, Day, Hour)
        StrFormat = "VSRT_OLD"
        StrOutput = output
    elif IsNew:
        StrInput = Path + "/DFS_VSRT_GRD_GRB3_{0}.{1}{2}{3}{4}30".format(Var, Year, Month, Day, Hour)
        StrFormat = "VSRT"
        StrOutput = output
    else:
        StrInput = Path + "/DFS_VSRT_GRD_GRIB_{0}.{1}{2}{3}{4}30".format(Var, Year, Month, Day, Hour)
        StrFormat = "VSRT"
        StrOutput = output
    
    StrOption = " -i {0} -f {1} -o {2} -p {3}".format(StrInput, StrFormat, StrOutput, PHour)
    
    return StrOption
    # 옵션 문자열 생성 완료 
    
def RunGribParser(StrOption):
    # GribParser를 실행시킨다.
    ParseStr = "python {0}/GribParser.py {1}".format(PROG_DIR, StrOption)
    result = subprocess.check_call(ParseStr, shell=True)
    
    return result
    # 간단하게 파일을 푼다. 리턴값을 확인하여 0이 아니면 문제가 발생한 것
    
def IsOldVSRT(DateTime):
    # 날짜를 확인하여 이전 종류의 파일인지 확인. 
    IsOld = False
    
    ProcDate = datetime.strptime(DateTime, "%Y%m%d").date()
    ChkDate = datetime.strptime("20130501", "%Y%m%d").date()
    
    if ProcDate < ChkDate:
        IsOld = True
    else:
        IsOld = False
        
    return IsOld
    # 파일 검사 끝, 이를 통해 파일명, 경로가 바뀜 
    
def IsNewVSRT(DateTime):
    # 날짜를 확인하여 이전 종류의 파일인지 확인. 
    IsNew = False
    
    ProcDate = datetime.strptime(DateTime, "%Y%m%d").date()
    ChkDate = datetime.strptime("20140531", "%Y%m%d").date()
    
    if ProcDate > ChkDate:
        IsNew = True
    else:
        IsNew = False
        
    return IsNew
    # 파일 검사 끝, 이를 통해 파일명, 경로가 바뀜 
    
if __name__ == '__main__':
    # 실 구현된 함수 부분 
        
    # 옵션 분리 및 스트링 생성 
    option = OptionSetter()
    StartTime, EndTime, LowX, LowY, HighX, HighY, Value, OutputPath = ArgCheck(option)

    TimeList = GetHourList(StartTime, EndTime)
    GridList = GetXYGridList(LowX, LowY, HighX, HighY)

    for DateTimeH in TimeList:
        # 시간에 따라 다른 파일이 생성
        Output_Base = "VSRT_" + Value + "_" + DateTimeH + ".csv"
        Output = os.path.join(OutputPath, Output_Base)
        Output_tmp = Output + '.tmp'
        if os.path.exists(Output):
            os.remove(Output)
        try:
            StrHour = DateTimeH[8:10]
        except:
            print('DateTime Error!! : Hour')
            sys.exit(1)
        UYear, UMonth, UDay, UHour = ksttoutc(DateTimeH)
        UDateTime = UYear + UMonth + UDay
        IsOld = IsOldVSRT(UDateTime)
        IsNew = IsNewVSRT(UDateTime)

        if IsOld:
            VSRT_Predict_Hour_FormatH = VSRT_Predict_Hour_Format[0:VSRT_Predict_Hour_Size[StrHour]-1]
        else:
            VSRT_Predict_Hour_FormatH = VSRT_Predict_Hour_Format[0:VSRT_Predict_Hour_Size[StrHour]]

        HEAD = '\n'+DateTimeH + ',' + ','.join( x + 'hr' for x in VSRT_Predict_Hour_FormatH) + '\n'

        with open(Output_tmp, 'w') as OutFP:

            OutFP.write(HEAD)
            VarLine = [Value] * len(GridList)

            for PHour in VSRT_Predict_Hour_FormatH:
                # 예보 시간에 따른 Grib 반복작업 
                DateTimeP = DateTimeH + "_{0}hr".format(PHour)
#                OutputH_tmp_Var = Output_tmp.replace('VSRT_', 'VSRT_{0}_'.format(Value))
                OutputH_tmp_Var_P = Output_tmp.replace(DateTimeH, DateTimeP)

                Path = InitSetter(UYear, UMonth, UDay, IsOld, IsNew)
                
                GribOption = MakeGribParseOption(UYear, UMonth, UDay, UHour, Value, Path, OutputH_tmp_Var_P, PHour, IsOld, IsNew)
            
                # 파일의 크기를 확인하여 파일이 잘못되어있으면 NULL 대체 데이터 입력
                Result = RunGribParser(GribOption)
                fsize = os.path.getsize(OutputH_tmp_Var_P)
                if fsize == 0:
                    os.remove(OutputH_tmp_Var_P)
                    for VarEch in VarLine:
                        VarEch += ',' + VSRT_Val_Null[Var]

                # 파일이 있는 경우 데이터를 읽어와서 기존 라인에 추가
                else:
                    with open(OutputH_tmp_Var_P) as InFP:
                        data = InFP.read().splitlines()
                        data.pop(0)

                    for idx in range(len(GridList)):
                        VarLine[idx] += ',' + data[GridList[idx]]

                    os.remove(OutputH_tmp_Var_P)

            # 완료된 변수의 데이터는 우선 입력
            for VarEch in VarLine:
                OutFP.write(VarEch + '\n')

        # 모든 작업이 완료되면 cat을 이용해서 기본 헤더파일과 하나로 합침
        cat_head = "cat {0}/head_vsrt.txt >> {1}".format(PROG_DIR, Output)
        cat_bady = "cat {0} >> {1}".format(Output_tmp, Output)
        result = subprocess.check_call(cat_head, shell=True)
        result = subprocess.check_call(cat_bady, shell=True)
        print "Parsing Success, Check Output File"
        print "FileName    : {0}".format(Output)
        if os.path.exists(Output):
            print "Check Success".format(Output)
        else:
            print "Check Fail".format(Output)

        os.remove(Output_tmp)