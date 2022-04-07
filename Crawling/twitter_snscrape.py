#snscrape로 원하는 keyword 원하는 날짜의 트윗 크롤링
#트위터 데이터 csv로 받아온 다음 쿼리입력 - match가 안되어서 포기함

import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
import csv
from datetime import datetime
from konlpy.tag import Okt
from database import conn

# Set maximum tweets to pull
maxTweets = 9
# Set what keywords you want your twitter scraper to pull
keyword = '코로나'
tagger = Okt()

csvFile = open('tweets_result_1.csv', 'w', newline='', encoding='utf-8-sig')
#Use csv writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['date','id','user','twitter_context','hashtags','place'])

# Write tweets into the csv file
for i,tweet in enumerate(
        sntwitter.TwitterSearchScraper(keyword + 'since:2022-03-27 until:2022-03-28').get_items()):
        if i > maxTweets :
            break
        tweets = str(tweet.content)
        csvWriter.writerow([tweet.date, tweet.id, tweet.user.username, tweets, tweet.hashtags, tweet.place])

        noun_list = tagger.nouns(tweets)
        #for keyword in noun_list:
                #키워드 노드 생성
                #conn.query("create (a4:KEYWORD {tweet: '" + tweets + "', keyword: '" + keyword + "'})")

csvFile.close()

# 트위터 노드 생성
#conn.query("Load csv with headers from 'file:///tweets_result_1.csv' as A create(a3: TWITTER {date: A.date, id: A.id, user: A.user, tweets: A.twitter_context, hashtags: A.hashtags, place: A.place}) return A")


# 각 트위터 노드와 키워드 노드 간의 match
#conn.query("match(a3:TWITTER{twitter:'" + tweets + "'}),(a4:KEYWORD{tweet:'" + tweets + "'})create(a3)-[r:keyword2]->(a4)")
conn.query("Load csv with headers from 'file:///tweets_result_1.csv' as A match(a3: TWITTER {tweets: A.twitter_context}),(a4:KEYWORD{tweet: A.twitter_context})create(a3)-[r:keyword2]->(a4)")