# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 10:57:31 2020

@author: Marc Fabel

Description:
     Webscapring of tweets from Twitter

Inputs:
     none

Outputs:
     xyz
"""

# packages
import tweepy
import time
import json
import pandas as pd
import GetOldTweets3 as got


# Store OAuth authentication credentials in relevant variables
access_token = "165818745-x3wLpDdKgN3A24DXJmbmSZUzbFeEVCUf75aH9QIX"
access_token_secret = "Ur5PX2LmPF9egjG0nVYVRavK0LyD3DoTGNtajuzupAyuE"
consumer_key = "9UYHCptzCkclqz0wXqbGYfgXu"
consumer_secret = "KS0NyzN7exRRK06OmIXrPrPGLbNKuBOfIyNW2EF8TVsJy98rx1"

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# work directories (LOCAL)
z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/media/'


###############################################################################
#       1) use tweepy to collect tweets
###############################################################################

tweets = []
username = 'GretaThunberg'
count = 1200
try:
     # Pulling individual tweets from query
     for tweet in api.user_timeline(id=username, count=count):
          # Adding to list that contains all tweets
          tweets.append((tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.source, tweet.truncated, tweet.text))
          # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
          # tweepy can get max 3240 tweets: https://gist.github.com/yanofsky/5436496

except BaseException as e:
      print('failed on_status,',str(e))
      time.sleep(3)

# transform in more readable version
df = pd.DataFrame(tweets)


#######################################
# extract one tweet
temp = api.user_timeline(id=username, count=1)

for status in temp:
    dictionary = status._json

#by looking at the dictionary, you can see the root level atributes of the tweets
#######################################



###############################################################################
#       2) use GetOldTweets3
###############################################################################
z_maxtweets = 3
j = 0

# looks only at own tweets
fh_write = open(z_media_output + 'twitter_greta_thunberg', 'w')
tweetCriteria = got.manager.TweetCriteria().setUsername("GretaThunberg")\
                                           .setMaxTweets(z_maxtweets)
# problem with writing down the results
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[2]
print(tweet.date, tweet.favorites, tweet.retweets, tweet.mentions, tweet.text)
fh_write.write(tweet.date + ';' + tweet.favorites + ';' + tweet.retweets + ';' + tweet.mentions + ';' + tweet.text + '\n')

while j < z_maxtweets:
     tweet = got.manager.TweetManager.getTweets(tweetCriteria)[j]
     print(tweet.date, tweet.favorites, tweet.retweets, tweet.mentions, tweet.text)
     fh_write.write(tweet.date + ';' + tweet.favorites + ';' + tweet.retweets + ';' + tweet.mentions + ';' + tweet.text + '\n')
     j += 1
