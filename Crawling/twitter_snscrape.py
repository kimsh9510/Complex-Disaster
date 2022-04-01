#snscrape로 원하는 keyword 원하는 날짜의 트윗 크롤링
from neo4j import __version__ as neo4j_version
from neo4j import GraphDatabase
import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
import csv
import matplotlib.pyplot as plt
from datetime import datetime

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

# Set maximum tweets to pull
maxTweets = 9
# Set what keywords you want your twitter scraper to pull
keyword = '코로나'
#since = '2021-10-06'
#until = '2021-10-07'
#Open/create a file to append data to
#english crawling

#csvFile = open('tweets_result_1.csv', 'w', newline='', encoding='utf-8-sig')
#Use csv writer
#csvWriter = csv.writer(csvFile)
#csvWriter.writerow(['date','id','user','tweet','hashtags','place'])

conn = Neo4jConnection(uri="bolt://localhost:7687", user="kimsh9510", pwd="sork")

# Write tweets into the csv file
for i,tweet in enumerate(
        #sntwitter.TwitterSearchScraper(keyword + ' lang:ko since:'+ since + 'until:' + until +' -filter:links -filter:replies').get_items()):
        sntwitter.TwitterSearchScraper(keyword + 'since:2022-03-27 until:2022-03-28').get_items()):
        if i > maxTweets :
            break
        date = tweet.date.strftime("%Y/%m/%d %H:%M:%S")
        id = str(tweet.id)
        user = str(tweet.user.username)
        tweets = str(tweet.content)
        hashtag = str(tweet.hashtags)
        place = str(tweet.place)
        print(type(hashtag))
        print(hashtag)

        conn.query("create (a1:Twitter {date: '" + date + "', id: '" + id + "', user: '" + user + "', tweet: '" + tweets + "', hashtags: 'hashtags', place: 'place'})")

        #특정 label 노드 모두 삭제
        #conn.query("match(n: Twitter) detach delete n")

        #csvWriter.writerow([tweet.date, tweet.id, tweet.user.username, tweet.content, tweet.hashtags, tweet.place])
#csvFile.close()
