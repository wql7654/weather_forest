import time
import urllib
import urllib.request
from xml.etree.ElementTree import parse, Element, dump, SubElement, ElementTree
import os



def scheduler_saved():

    while True:

        if time.strftime("%M%S") == "0330": #api가 매시간 3분30초에 데이터를 갱신
            get_xml()
            time.sleep(10)
            all_write()
            time.sleep(10)
            print("%s시 수집이 완료되었습니다."%time.strftime("%H"))
        else:
            continue

def get_xml():
    key="YHt09t28DYtoaKEfFxq%2Fjh0lxcidcTTWWywGQYJi1hxqmrOdWQ5hKmxlPYl8pX2Gro6rw96Drd47O%2BKK5vbl0w%3D%3D"
    parameters = "?serviceKey=" + key
    parameters += "&numOfRows=" + '2000'
    parameters += "&pageNo=" + '1'

    url = "http://car.daegu.go.kr/openapi-data/service/rest/data/linkspeed"+parameters
    data = urllib.request.urlopen(url).read()
    f = open("sample.xml", "wb")
    f.write(data)  # 파일로 저장됨
    f.close()

def all_write():
    tree = parse("sample.xml")  # 생성한 xml 파일 파싱하기
    note = tree.getroot()

    # times = time.strftime('%x', time.localtime(time.time()))
    # times = times.replace('/', '-')
    # f=open("%s.csv"%times, 'a',encoding='cp949')
    test = os.listdir("./")
    f = open("대구시 실시간 교통정보 조회.csv", 'a', encoding='cp949')
    if test.count('대구시 실시간 교통정보 조회.csv') == 0:
        index = "DSRC 링크정보,표준노드링크 정보,구간명,시작지점명,도착지점명,거리,가로명,링크속도,링크통행시간,소통정보코드,정보생성일시\n"
        f.write(index)
    for parent2 in note.getiterator("item"):
        txt = []
        txt.append(parent2.findtext("atmsTm"))
        txt.append(parent2.findtext("dist"))
        txt.append(parent2.findtext("dsrcLinkSn"))
        txt.append(parent2.findtext("endFacNm"))
        txt.append(parent2.findtext("linkSpeed"))
        txt.append(parent2.findtext("linkTime"))
        txt.append(parent2.findtext("roadNm"))
        txt.append(parent2.findtext("sectionInfoCd"))
        txt.append(parent2.findtext("sectionNm"))
        txt.append(parent2.findtext("startFacNm"))
        txt.append(parent2.findtext("stdLinkId"))
        txt2 = ','.join(txt) + "\n"
        f.write(txt2)
    f.close()

print("데이터 수집을 시작합니다")
scheduler_saved()

