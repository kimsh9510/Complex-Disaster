#snscrape를 이용해서 특정 사용자 'from:A' 의 트위터 크롤링
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:jack').get_items()):  # declare a username
    if i > 10:  # number of tweets you want to scrape
        break
    tweets_list1.append(
        [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.hashtags, tweet.place])  # declare the attributes to be returned

# Creating a dataframe from the tweets list above
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'hashtags', 'place'])
print(tweets_df1[['hashtags','place']])