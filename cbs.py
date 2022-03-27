# 라이브러리 import
import requests
import xml.etree.ElementTree as ET
from konlpy.tag import Okt

url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D&pageNo=1&numOfRows=10&type=xml'
response = requests.get(url)
contents = response.text
xml = ET.fromstring(contents)

for message in xml.findall("row"):
    print("here")
    create_date = message.find("create_date")  # 생성일시
    location_id = message.find("location_id")  # 수신지역 코드
    location_name = message.find("location_name")  # 수신지역 이름
    md101_sn = message.find("md101_sn")  # 일련번호
    msg = message.find("msg")  # 내용
    send_platform = message.find("send_platform")  # 발신처

tagger=Okt()
#part_of_speech = tagger.pos('[영동군청]코로나19 확진 159명(확진자접촉 56, 증상발현 101, 무증상 2) ▲검사 실시.')
#print(part_of_speech)  # 튜플 형태로 출력
noun_list = tagger.nouns(msg.text)
print(noun_list)  # 리스트 형식으로 출력









