#snscrape로 원하는 keyword 원하는 날짜의 트윗 크롤링
import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwitter
import csv
import matplotlib.pyplot as plt

# Set maximum tweets to pull
maxTweets = 800
# Set what keywords you want your twitter scraper to pull
keyword = '산불'
#since = '2021-10-06'
#until = '2021-10-07'
#Open/create a file to append data to
#english crawling
#csvFile = open('tweets_result.csv', 'a', newline='', encoding='utf-8')
csvFile = open('tweets_result_1.csv', 'w', newline='', encoding='utf-8-sig')
#Use csv writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['date','id','user','tweet','hashtags','place'])

# Write tweets into the csv file
for i,tweet in enumerate(
        #sntwitter.TwitterSearchScraper(keyword + ' lang:ko since:'+ since + 'until:' + until +' -filter:links -filter:replies').get_items()):
        sntwitter.TwitterSearchScraper(keyword + 'since:2022-03-08 until:2022-03-09').get_items()):
        if i > maxTweets :
            break
        csvWriter.writerow([tweet.date, tweet.id, tweet.user.username, tweet.content, tweet.hashtags, tweet.place])
csvFile.close()