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
#z_media_output =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'


# work directories (LOCAL)
z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'


# work directories (SERVER)
#z_media_output = 'F:/temp/'

# function to loop through days
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


# define user name
z_username = 'parents4future'              #z_start_date = datetime(2019, 2, 1)




# finished scraping
#z_username = 'GretaThunberg'
#z_username = 'Luisamneubauer'
#z_username = 'louismotaal'                 #z_start_date = datetime(2018, 10, 1)
#z_username = 'jakobblasel'
#z_username = 'carla_reemtsma'
#z_username = 'FranziWessel'                #z_start_date = datetime(2019, 5, 1)
#z_username = 'FridayForFuture'             #z_start_date = datetime(2018, 12, 1) FFF Germany
#z_username = 'sciforfuture'                #z_start_date = datetime(2019, 3, 1)
#z_username = 'Ende__Gelaende'
#z_username = 'ExtinctionR_DE'              #z_start_date = datetime(2018, 11, 1)

# get number of followers

###############################################################################
#       1) use GOT to collect old tweets
###############################################################################

# have a large constant in order to capture all tweets per day
z_maxtweets = 1000


# time period over which you want to scrape the old tweets
z_start_date = datetime(2020, 1, 30) # 2018, 10, 1
z_end_date = datetime(2020,6,23) # 2020,1,31


# open file handle with headers
fh_write = open(z_media_output + 'twitter_' + z_username + '_v2.csv', 'w',
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
    temp = got.manager.TweetManager.getTweets(tweetCriteria)
    len_tweets_month = len(temp)
    #print(len_tweets_month)

    while j < z_maxtweets and j < len_tweets_month:
        tweet = temp[j]
        fh_write.write(tweet.date.strftime('%Y-%m-%d %H:%M:%S') + '\t' +
            str(tweet.favorites) + '\t' +
            str(tweet.retweets) + '\t' +
            tweet.mentions + '\t' +
            tweet.text + '\t' +
            tweet.hashtags + '\n')
        j += 1

    # additional time between daily requests
    time.sleep(11)

fh_write.close()
print('program finished')
















