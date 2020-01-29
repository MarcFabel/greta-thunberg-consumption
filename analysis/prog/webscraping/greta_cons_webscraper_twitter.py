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
count = 12
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
    
    
#######################################

# have the one tweet as json    
    status = temp[0]    
#convert to string
json_str = json.dumps(status._json)

#deserialise string into python object
parsed = json.loads(json_str)

print(json.dumps(parsed, indent=4, sort_keys=True))


    

#by looking at the dictionary, you can see the root level atributes of the tweets
#######################################

# have the one tweet as json
with open("greta.json") as json_file:
    json_data = json.load(json_file)

# Print each key-value pair in json_data
for k,val in json_data.items():
    print(k + ': ', val)    
    



###############################################################################
#       2) Tweepy V2
###############################################################################
# CHANGE THIS TO THE USER YOU WANT
user = 'GretaThunberg

with open('sample_api_keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)
user = user.lower()
output_file = '{}.json'.format(user)
output_file_short = '{}_short.json'.format(user)
compression = zipfile.ZIP_DEFLATED

with open('all_ids.json') as f:
    ids = json.load(f)

print('total ids: {}'.format(len(ids)))

all_data = []
start = 0
end = 100
limit = len(ids)
i = math.ceil(limit / 100)

for go in range(i):
    print('currently getting {} - {}'.format(start, end))
    sleep(6)  # needed to prevent hitting API rate limit
    id_batch = ids[start:end]
    start += 100
    end += 100
    tweets = api.statuses_lookup(id_batch)
    for tweet in tweets:
        all_data.append(dict(tweet._json))

print('metadata collection complete')
print('creating master json file')
with open(output_file, 'w') as outfile:
    json.dump(all_data, outfile)

print('creating ziped master json file')
zf = zipfile.ZipFile('{}.zip'.format(user), mode='w')
zf.write(output_file, compress_type=compression)
zf.close()

results = []

def is_retweet(entry):
    return 'retweeted_status' in entry.keys()

def get_source(entry):
    if '<' in entry["source"]:
        return entry["source"].split('>')[1].split('<')[0]
    else:
        return entry["source"]

with open(output_file) as json_data:
    data = json.load(json_data)
    for entry in data:
        t = {
            "created_at": entry["created_at"],
            "text": entry["text"],
            "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
            "retweet_count": entry["retweet_count"],
            "favorite_count": entry["favorite_count"],
            "source": get_source(entry),
            "id_str": entry["id_str"],
            "is_retweet": is_retweet(entry)
        }
        results.append(t)

print('creating minimized json master file')
with open(output_file_short, 'w') as outfile:
    json.dump(results, outfile)

with open(output_file_short) as master_file:
    data = json.load(master_file)
    fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]
    print('creating CSV version of minimized json master file')
    f = csv.writer(open('{}.csv'.format(user), 'w'))
    f.writerow(fields)
    for x in data:
        f.writerow([x["favorite_count"], x["source"], x["text"], x["in_reply_to_screen_name"], x["is_retweet"], x["created_at"], x["retweet_count"], x["id_str"]])








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
