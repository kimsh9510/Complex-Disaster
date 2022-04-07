#트위터 데이터 받아와서 바로 데이터베이스에 입력
#hashtag 값이 안들어가서 제외하고함
#match 해서 relation까지 표현

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
    #hashtag = tweet.hashtags.text
    #place = str(tweet.place)

    conn.query("create (a3:TWITTER {date : '" + date + "', id:'" + id + "', user:'" + user + "', tweet:'" + tweets + "', hashtag:'hashtag', place:'place'})")

    noun_list = tagger.nouns(tweets)
    for keyword in noun_list:
        #키워드 노드 생성
        conn.query("create (a4:KEYWORD {tweet: '" + tweets + "', keyword: '" + keyword + "'})")

    conn.query("match(a3:TWITTER{tweet:'" + tweets + "'}),(a4:KEYWORD{tweet:'" + tweets + "'})create(a3)-[r:keyword2]->(a4)")



