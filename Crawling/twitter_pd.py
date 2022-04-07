#pd에 데이터 넣어서 데이터베이스에 넣기
#hashtag 값이 여전히 안들어감

import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
import csv
from datetime import datetime
from konlpy.tag import Okt
from database import conn

# Set maximum tweets to pull
maxTweets = 9

# Creating list to append tweet data
tweets_list1 = []
hashtag =[]
# Set what keywords you want your twitter scraper to pull
keyword = '코로나'
tagger = Okt()

def hash(a):
    #a = ['화천군청', '라라군청']
    hash = ''
    separtor = ','
    for idx, val in enumerate(a):
        hash += val + ('' if idx == len(a) - 1 else separtor)
    print(hash)
    print(type(hash))

for i,tweet in enumerate(
    #sntwitter.TwitterSearchScraper(keyword + ' lang:ko since:'+ since + 'until:' + until +' -filter:links -filter:replies').get_items()):
    sntwitter.TwitterSearchScraper(keyword + 'since:2022-03-27 until:2022-03-28').get_items()):
    if i > maxTweets :
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.hashtags, tweet.place])  # declare the attributes to be returned

tweets_df = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'hashtags', 'place'])

for i in range(3):
    hashtag[i] = hash(str(tweets_df['hashtags'][i]))
    print(hashtag[i])

for i in range(maxTweets):
    conn.query("create (a3:TWITTER {date : '" + str(tweets_df['Datetime'][i]) + "', id:'" + str(tweets_df['Tweet Id'][i]) + "', user:'" + str(tweets_df['Username'][i]) + "', tweet:'" + str(tweets_df['Text'][i]) + "', hashtag:'"+str(tweets_df['hashtags'][i])+"', place:'place'})")

print(tweets_df['Datetime'][0])