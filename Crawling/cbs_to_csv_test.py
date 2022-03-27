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

url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D&pageNo=1&numOfRows=10&type=xml'
response = requests.get(url)
contents = response.text
print(contents)
xml = ET.fromstring(contents)

#csv파일 열기
csv_file = open("../data2.csv", 'w', encoding='utf-8-sig')

csv_file_writer = csv.writer(csv_file)
csv_file_writer.writerow(["create_date", "location_id", "location_name", "md101_sn", "msg", "send_platform"])
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
