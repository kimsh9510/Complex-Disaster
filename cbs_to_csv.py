# 라이브러리 import
import requests
import pprint
import json
import pandas as pd
import write as write
from pandas.io.json import json_normalize
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import csv
import datetime
import math

#pageNos = [1, 2]
#pages = 1

url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D&pageNo=1&numOfRows=1000&type=xml'
response = requests.get(url)
contents = response.text
xml = ET.fromstring(contents)

#원하는 태그 값 받아오기
for node in xml:
    try:
        count = node.find("totalCount").text
        print(count)
    except Exception as e:
        continue

pages = math.ceil(int(count)/1000)
print(pages)
#csv파일 열기
csv_file = open("data.csv", 'w', encoding='utf-8-sig')
csv_file_writer = csv.writer(csv_file)
csv_file_writer.writerow(["create_date", "location_id", "location_name", "md101_sn", "msg", "send_platform"])

for pageNo in range(1, pages+1):
    # url 입력 - ServiceKey=인증키, pageNo=페이지 시작, numOfRows=출력 행 갯수, type=json or xml
    url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D&pageNo='+str(pageNo)+'&numOfRows=1000&type=xml'
    # startCreateDt=20220101, endCreateDt=20210103
    #url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D'
    # url 불러오기
    response = requests.get(url)

    #데이터 값 출력해보기
    contents = response.text
    #contents2 = contents+contents
    #print(contents2)

    #json 변경
    #json_ob = json.loads(contents)
    #print(json_ob)
    #print(type(json_ob)) #json타입 확인-dict

    xml = ET.fromstring(contents)
    for message in xml.findall("row"):
        create_date = message.find("create_date") #생성일시
        location_id = message.find("location_id") #수신지역 코드
        location_name = message.find("location_name") #수신지역 이름
        md101_sn = message.find("md101_sn") #일련번호
        msg = message.find("msg") #내용
        send_platform = message.find("send_platform") #발신처
        csv_line = [create_date.text, location_id.text, location_name.text, md101_sn.text, msg.text, send_platform.text]
        csv_file_writer.writerow(csv_line)

        #location_id 부산인 데이터만 저장
        # if (location_id.text == '119'):
        #     csv_file_writer.writerow(csv_line)
        # if (create_date.text >= '2022-01-07 11:00:09 AM'):
        #     csv_file_writer.writerow(csv_line)

