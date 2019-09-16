import urllib
import urllib.request
import datetime
import json
import time
import os
import re
import pandas as pd
# http://data.kma.go.kr/apiData/getData?type=xml&dataCd=ASOS&dateCd=HR&startDt=20100101&startHh=09&endDt=20100102&endHh=04&stnIds=108&schListCnt=10&pageIndex=1&
# apiKey=wVZT97T%2BsuuSV5VY%2BDE0/ZKr9/U1bq3lnu0Zs/xWT8l46ajIXKev9yIn97c1BtJt&

access_key="YHt09t28DYtoaKEfFxq%2Fjh0lxcidcTTWWywGQYJi1hxqmrOdWQ5hKmxlPYl8pX2Gro6rw96Drd47O%2BKK5vbl0w%3D%3D"


# bc = open("./새파일5.txt", 'a',encoding="utf-8")


def get_Request_URL(url):                 ## (1) 기상 정보
    req = urllib.request.Request(url)     ## request 날리는 함수

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def get_Weather_URL(strat_num):       ## (1) 기상 정보 request 보내기 전, url 만드는 함수
    end_point = "http://car.daegu.go.kr/openapi-data/service/rest/data/linkspeed"

    parameters = "?serviceKey=" + access_key
    parameters += "&numOfRows=" + '3000'  #페이지 갯수
    parameters += "&pageNo=" + strat_num #시작시간 10



    url = end_point + parameters
    print(url)
    retData = get_Request_URL(url)
    if (retData == None):
        return None
    else:
        return json.loads(retData)

def read_Weather_json(data):
    json_data = data
    line_cnt = 0

    while True:
        output_data = ''
        try:
            if json_data[3]['info']:
                print("기온: %s \n습도: %s \n풍향: %s \n풍속: %s" % (
                    json_data[3]['info'][0]["TA"],
                    json_data[3]['info'][0]["HM"], json_data[3]['info'][0]["WD"],json_data[3]['info'][0]["WS"]))
                output_data = str(json_data[3]['info'][0]["TA"]) + ","  + str(
                    json_data[3]['info'][0]["HM"]) + "," + str(json_data[3]['info'][0]["WD"]) + "," + str(
                    json_data[3]['info'][0]["WS"])

            break

        except Exception:
            break
    # bc.write(output_data + '\n')


print(get_Weather_URL('3'))
# for cx in range(1,6):
#     fc = open("./traffic.csv", 'a', encoding="utf-8")
#     read_Weather_json(data)
#
#     time.sleep(1)
#     cnt += 1
#     print(cnt)
#     bc.write('close' + '\n')
#     fc.close()


