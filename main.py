from neo4j import __version__ as neo4j_version
from neo4j import GraphDatabase
import requests
import xml.etree.ElementTree as ET
from konlpy.tag import Okt

print(neo4j_version)

#neo4j class 생성
class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

if __name__ == "__main__":
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="kimsh9510", pwd="sork")
    url = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=vBWCvCxW515%2BgkLcMNXIXHBLHaNh9Xa8F8V9TrjFpKFeB0lP7D9%2BwXEIuAttbGQPrND%2BREAx2GIJf5eXoHF%2FdA%3D%3D&pageNo=1&numOfRows=10&type=xml'
    response = requests.get(url)
    contents = response.text
    #print(contents)
    xml = ET.fromstring(contents)
    tagger = Okt()

    for message in xml.findall("row"):
        create_date = message.find("create_date").text  # 생성일시
        location_id = message.find("location_id").text  # 수신지역 코드
        location_name = message.find("location_name").text  # 수신지역 이름
        md101_sn = message.find("md101_sn").text # 일련번호
        msg = message.find("msg").text  # 내용
        send_platform = message.find("send_platform").text  # 발신처

        #쿼리 입력
        conn.query("create (a1:CBS {date: '"+create_date+"', location_id: '"+location_id+"', location_name: '"+location_name+"', md101_sn: '"+md101_sn+"', msg: '"+msg+"', send_platform: '"+send_platform+"'})")
        #conn.query("create (a1: CBS {date : '"+create_date+"'})")
        #conn.query("match (a) optional match (a)-[r]-() delete a, r")

        #각 msg에 대한 keyword 추출 후 KEYWORD 쿼리 생성
        noun_list = tagger.nouns(msg)
        for keyword in noun_list:
            conn.query("create (a2:KEYWORD {msg: '" + msg + "', keyword: '" + keyword + "'})")
            print("finish")

        #각 cbs메시지와 키워드 간의 match
        conn.query("match(a1:CBS{msg:'" + msg + "'}),(a2:KEYWORD{msg:'" + msg + "'})create(a1)-[r:keyword]->(a2)")




