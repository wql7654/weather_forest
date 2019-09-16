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

access_key="wVZT97T%2BsuuSV5VY%2BDE0/ZKr9/U1bq3lnu0Zs/xWT8l46ajIXKev9yIn97c1BtJt"


bc = open("./새파일5.txt", 'a',encoding="utf-8")


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

def get_Weather_URL(strat_day,strat_time,end_day,end_time,location):       ## (1) 기상 정보 request 보내기 전, url 만드는 함수
    end_point = "http://data.kma.go.kr/apiData/getData?type=json&dataCd=ASOS&dateCd=HR"


    parameters = "&startDt=" + strat_day  #시작일 ex: 20100101
    parameters += "&startHh=" + strat_time #시작시간 10
    parameters += "&stnIds=" + location #위치 108
    parameters += "&endDt=" + end_day
    parameters += "&endHh=" + end_time
    parameters += "&schListCnt=10&pageIndex=1"
    parameters += "&apiKey=" + access_key


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
    bc.write(output_data + '\n')
for cx in range(0,6):
    df = pd.read_csv('./hwasung.csv', encoding='cp949')
    df.columns = df.columns.str.replace(' ', '')
    fc = open("./time6.csv", 'r', encoding="utf-8")

    line = fc.readlines()
    d = ''
    timedata = []
    alldata = []
    a = ''
    location = ''
    cnt = 0
    count_day = 0

    for i in line:
        timedata = []
        for b in i:
            if b == ',' or b == '\n':
                timedata.append(d)
                d = ''
            else:
                d = d + b

        re = []
        count_day = cx

        ds = datetime.timedelta(days=count_day)

        s2 = datetime.datetime(int(timedata[0]), int(timedata[1]), int(timedata[2]), 0)
        s3 = datetime.datetime(int(timedata[4]), int(timedata[5]), int(timedata[6]), 0)
        time_st = str(s2-ds )
        time_ed = str(s3-ds )

        if len(timedata[3][:-3]) == 1:
            timedata[3] = '0' + timedata[3][:-3]
        else:
            timedata[3] = timedata[3][:-3]
        if len(timedata[7][:-3]) == 1:
            timedata[7] = '0' + timedata[7][:-3]
        else:
            timedata[7] = timedata[7][:-3]
        time_st = time_st.replace('-', '')
        time_ed = time_ed.replace('-', '')
        strat_day = time_st[0:8]
        strat_time = timedata[3]
        end_day = time_ed[0:8]
        end_time = timedata[7]

        location = str(119) #안동 136 홍천 121 춘천 101 화성(수원)119
        data = get_Weather_URL(strat_day, strat_time, end_day, end_time, location)
        read_Weather_json(data)
        time.sleep(1)
        cnt += 1
        print(cnt)
    bc.write('close' + '\n')
    fc.close()


