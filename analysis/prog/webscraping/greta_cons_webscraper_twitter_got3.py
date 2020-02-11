# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 10:05:52 2020

@author: Marc Fabel

Description:
     Webscapring of tweets from Twitter via GetOldTweets3

Inputs:
     none

Outputs:
     twitter_greta_thunberg_temp.csv [source] with \t as delim
"""

# packages
from datetime import timedelta,datetime
import GetOldTweets3 as got
import time


# HOME directories
z_media_output =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'


# work directories (LOCAL)
#z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'

# function to loop through days
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
#z_username = 'Ende__Gelaende'
#z_username = 'ExtinctionR_DE'

# finished scraping
#z_username = 'Luisamneubauer'
#z_username = 'jakobblasel'  
#z_username = 'GretaThunberg' 
#z_username = 'carla_reemtsma'  
#z_username = 'FranziWessel'
#z_username = 'FridayForFuture' # FFF Germany




# get number of followers

  

###############################################################################
#       1) use GOT to collect tweets
###############################################################################

# have a large constant in order to capture all tweets per day
z_maxtweets = 1000


# time period over which you want to scrape the old tweets
z_start_date = datetime(2018, 12, 1) # 2018, 10, 1
z_end_date = datetime(2020,1,31) # 2020,1,1


# open file handle with headers
fh_write = open(z_media_output + 'twitter_' + z_username + '.csv', 'w',
                encoding='utf8') 
fh_write.write('date\tfavorites\tretweets\tmentions\ttext\thashtags' + '\n')

for day in daterange(z_start_date, z_end_date):
     tomorrow = day + timedelta(1) # enables extraction of tweets between today and tomorrow
     print('currently extracting:', day.strftime('%Y-%m-%d'))
     tweetCriteria = got.manager.TweetCriteria().setUsername(z_username)\
                .setSince(day.strftime('%Y-%m-%d'))\
                .setUntil(tomorrow.strftime('%Y-%m-%d'))\
                .setMaxTweets(z_maxtweets)

     # etract all tweets today
     j = 0
     len_tweets_month = len(got.manager.TweetManager.getTweets(tweetCriteria))
     while j < z_maxtweets and j < len_tweets_month:
          tweet = got.manager.TweetManager.getTweets(tweetCriteria)[j]
          fh_write.write(tweet.date.strftime('%Y-%m-%d %H:%M:%S') + '\t' +
                    str(tweet.favorites) + '\t' +
                    str(tweet.retweets) + '\t' +
                    tweet.mentions + '\t' +
                    tweet.text + '\t' +
                    tweet.hashtags + '\n')
          j += 1

     # additional time between daily requests
     time.sleep(7)

fh_write.close()
print('program finished')