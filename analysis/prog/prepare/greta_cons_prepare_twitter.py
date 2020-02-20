#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:58:06 2020

@author: marcfabel


notes:
     be aware that the input-file needed to have encoding adjusted: " and '

"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
from datetime import datetime



#style.available
style.use('seaborn-darkgrid')


# HOME directory
#z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'


# work directories (LOCAL)
z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'
z_media_figures =   'W:/EoCC/analysis/output/graphs/descriptive/'
z_prefix =          'greta_cons_'


###############################################################################
#           Read in & prepare Data
###############################################################################

########## Read in activists ##################################################
greta = pd.read_csv(z_media_input + 'twitter_GretaThunberg.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "utf-8")

luisa = pd.read_csv(z_media_input + 'twitter_Luisamneubauer.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "utf-8")

jakob = pd.read_csv(z_media_input + 'twitter_jakobblasel.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "utf-8")





# define common activists
activists = luisa['favorites'].copy()


list_activists = [greta, luisa, jakob]

# make graph for each of the activists:
for activist in list_activists:
    # define variables in per thousand+
    # define variables for greta
    activist['favorites'] = activist['favorites'] / 1000
    activist['retweets']  = activist['retweets']  / 1000
    temp = jakob.resample('W').sum()


#############################################
# Versuch alles über ein großes dictionary zu machen


# generate dictionary of activist
paths = ['GretaThunberg', 'Luisamneubauer', 'jakobblasel', 'carla_reemtsma',
         'FranziWessel']
dfs = {p: pd.read_csv(z_media_input + 'twitter_' +  p + '.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "utf-8") for p in paths}


# more workable keys:
dfs['greta'] = dfs.pop('GretaThunberg')
dfs['luisa'] = dfs.pop('Luisamneubauer')
dfs['jakob'] = dfs.pop('jakobblasel')
dfs['carla'] = dfs.pop('carla_reemtsma')
dfs['franzi']= dfs.pop('FranziWessel')

list_activists = ['greta', 'luisa', 'jakob', 'carla', 'franzi']

for activist in list_activists:
    dfs[activist]['favorites'] = dfs[activist]['favorites'] / 1000
    dfs[activist]['retweets'] = dfs[activist]['retweets'] / 1000
    dfs[activist + '_w'] = dfs[activist].resample('W').sum()


# kann ich df übergreifend plotten - yes
fig, ax = plt.subplots()
ax.plot(dfs['luisa_w'].index.values, dfs['jakob_w']['favorites'],
        color='blue', label='jakob blasel')
ax.plot(dfs['carla_w'].index.values, dfs['carla_w']['favorites'],
        color='green', label='carla reemtsma')
ax.plot(dfs['franzi_w'].index.values, dfs['franzi_w']['favorites'],
        color='red', label='franzi wessel')
ax.legend(loc='upper left')


# loop over activists to have graph
for activist in list_activists:
	fig, ax1 = plt.subplots()
	color_fav = 'tab:blue'
	ax1.plot(dfs[activist + '_w'].index.values, dfs[activist + '_w']['favorites'], color=color_fav, label='favorites') # T10 categorical palette
	ax1.set_xlabel('Date')
	ax1.set_ylabel('Favorites [in thousand]', color=color_fav)
	ax1.tick_params(axis='y', labelcolor=color_fav)

	ax2 = ax1.twinx()
	color_re = 'tab:orange'
	ax2.plot(dfs[activist + '_w'].index.values, dfs[activist + '_w']['retweets'], color=color_re, label='retweets')
	ax2.set_ylabel('Retweets [in thousand]', color=color_re)
	ax2.tick_params(axis='y', labelcolor=color_re)
	ax2.grid(None)

	ax3 = ax1.twinx()
	ax3.plot(dfs['greta_w'].index.values, dfs['greta_w']['favorites'], alpha=0.0006)
	ax3.grid(None)
	ax3.set_yticklabels([])

	# ask matplotlib for the plotted objects and their labels
	lines, labels = ax1.get_legend_handles_labels()
	lines2, labels2 = ax2.get_legend_handles_labels()
	ax2.legend(lines + lines2, labels + labels2, loc='upper left')



###############################################################################
#           Graphs
###############################################################################

# without events
fig, ax1 = plt.subplots()

color_fav = 'tab:blue'
ax1.plot(temp.index.values, temp['favorites'], color=color_fav, label='favorites') # T10 categorical palette
ax1.set_xlabel('Date')
ax1.set_ylabel('Favorites [in thousand]', color=color_fav)
ax1.tick_params(axis='y', labelcolor=color_fav)

ax2 = ax1.twinx()
color_re = 'tab:orange'
ax2.plot(temp.index.values, temp['retweets'], color=color_re, label='retweets')
ax2.set_ylabel('Retweets [in thousand]', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
ax2.grid(None)

# ask matplotlib for the plotted objects and their labels
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_favorites_retweets_weekly.pdf')



# with events
c_shading = 'darkgreen'
c_opacity = 0.4

fig, ax1 = plt.subplots()

color_fav = 'tab:blue'
ax1.plot(temp.index.values, temp['favorites'], color=color_fav, label='favorites') # T10 categorical palette
ax1.set_xlabel('Date')
ax1.set_ylabel('Favorites [in thousand]', color=color_fav)
ax1.tick_params(axis='y', labelcolor=color_fav)

ax2 = ax1.twinx()
color_re = 'tab:orange'
ax2.plot(temp.index.values, temp['retweets'], color=color_re, label='retweets')
ax2.set_ylabel('Retweets [in thousand]', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
ax2.grid(None)

ax1.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # Katowice - climate conference
ax1.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax1.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax1.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax1.axvline(datetime(2019,3,29), color=c_shading, alpha=c_opacity)                         # Berlin - climate strike with Greta (friday)
ax1.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax1.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # Atlantic - travel to UN
ax1.axvspan(datetime(2019,9,23), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # NY - UN climate action summit
ax1.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # Madrid - UN climate change conference

plt.savefig(z_media_figures + z_prefix + 'twitter_greta_favorites_retweets_weekly_events.pdf')





# we would also need the number of followers: Hiwi-fun with
# https://web.archive.org/web/20190501000000*/https://twitter.com/GretaThunberg
# https://stackoverflow.com/questions/4084909/how-to-get-a-count-of-followers-from-twitter-api-and-trendline
# https://ws-dl.blogspot.com/2018/03/2018-03-14-twitter-follower-count.html



###############################################################################
#           NLP
###############################################################################

# classify language of tweet
from langdetect import detect
import numpy as np

# define missing values as str.nan
greta['text'] = greta['text'].replace('', np.nan)
greta['text'] = greta['text'].replace(' ', np.nan)




# there are two tweets that just contain links, which cannot be classified as language
criterium_no_link = (greta['text'] != 'https://www.fridaysforfuture.org') & \
    (greta['text'] != 'https://unfccc-cop25.streamworld.de/webcast/high-level-event-on-climate-emergency')

greta['lang'] = greta.loc[greta.text.notnull() & criterium_no_link].text.apply(detect)


# correct language missclassifications
temp1 = greta.loc[greta.lang != 'en']

lang_misclass = ['af', 'ca', 'cs', 'cy', 'et', 'fi', 'id', 'it', 'no', 'pl',
                 'pt', 'ro', 'sl', 'so', 'sw', 'tl', 'tr']
for lang in lang_misclass:
    greta['lang'] = greta['lang'].replace(lang, 'en')

temp1 = greta.loc[greta.lang != 'en']





# change order of columns
z_cols_to_order = ['favorites', 'retweets', 'lang', 'text']
z_new_columns = z_cols_to_order + (greta.columns.drop(z_cols_to_order).tolist())
greta = greta[z_new_columns]




################################################################
# Word Cloud
###############################################################

from wordcloud import WordCloud, STOPWORDS
import re
from string import digits, punctuation
import nltk

import random
import numpy as np


# color function for different shades of gray in the word cloud
def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(230, 0%%, %d%%)" % random.randint(20, 51)


# make tweets into list
raw_tweets = greta.text.values.tolist()

# eliminate empty fields
raw_tweets =  [x for x in raw_tweets if type(x)== str]

# Create a string form of our list of text
raw_string = ' '.join(raw_tweets)

# eliminate urls
no_links = re.sub(r'http\S+', '', raw_string)

# remove punctuation and special characters
remove = digits + punctuation + '“”—'
remove

no_punctuation = no_links.translate(str.maketrans({p: "" for p in remove}))


# tokenization
words = no_punctuation.split(" ")
words = [w for w in words if len(w) > 2]  # ignore a, an, be, ...
words = [w.lower() for w in words]
words = [w for w in words if w not in STOPWORDS]

# remove more stopwords
_stopwords = nltk.corpus.stopwords.words('english')
words = [w for w in words if w not in _stopwords]

_further_stopwords = ['must', 'att', 'som', 'inte', 'och', 'dont', 'det', 'för',
                      'har', 'doesnt', 'ive', 'alla']
words = [w for w in words if w not in _further_stopwords]


# unify fridays for future
words = [sub.replace('fridayforfuture', 'fridaysforfuture') for sub in words]
words = [sub.replace('fridaysforfurture', 'fridaysforfuture') for sub in words]


# word cloud w/o stemming

wc = WordCloud(
    width = 1500,
    height = 1000,
    background_color = 'white',
    max_words=90,
    collocations=False,
    random_state=1) # collocations=False -> use only monograms
clean_string = ' '.join(words)
wc.generate(clean_string)

fig = plt.figure(
    figsize = (20, 16),
    facecolor = 'k',
    edgecolor = 'k')


plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_word_cloud.pdf')




################################################################
# Top Words in Greta Thunberg's Tweets
################################################################

import seaborn as sns


# generate df with number of occurences per word
dfwords = pd.DataFrame(words, columns=['words'])
dfwords['counts'] = 1
words_nr = dfwords.groupby(['words']).sum()
words_nr.sort_values(['counts'], inplace=True, ascending=False)
words_nr = words_nr[:39]

# bar
fig, ax = plt.subplots()
ax = sns.barplot(words_nr.index, words_nr.counts, palette='Blues_d') #
ax.set(xlabel='', ylabel='Number of uses')
for item in ax.get_xticklabels():
     item.set_rotation(90)
plt.tight_layout()      # makes room for the x-label (as it is quite wide)
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_frequency_common_words.pdf')



################################################################
# Number of Tweets by Greta Thunberg
################################################################
temp = greta.copy()
temp['counts'] = 1
temp = temp.resample('W').sum()

## without events
#fig, ax1 = plt.subplots()
#color_fav = 'darkgrey'
#ax1.plot(temp.index.values, temp['favorites'], color=color_fav, label='favorites',zorder=100)
#ax1.set_xlabel('Date')
#ax1.set_ylabel('Favorites [in thousand]', color=color_fav)
#ax1.tick_params(axis='y', labelcolor=color_fav)
#ax2 = ax1.twinx()
#color_re = 'tab:blue'
#ax2.plot(temp.index.values, temp['counts'], color=color_re, label='count', zorder=0)
#ax2.set_ylabel('Number of tweets', color=color_re)
#ax2.tick_params(axis='y', labelcolor=color_re)
#ax2.grid(None)
## ask matplotlib for the plotted objects and their labels
#lines, labels = ax1.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()
#lines3, labels3 = ax3.get_legend_handles_labels()
#ax2.legend(lines + lines2, labels + labels2, loc='upper left')




# andersrum mit drei Achsen##################################
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax3 =fig.add_axes(ax1.get_position(), sharex=ax1, sharey=ax1)
ax3.set_facecolor('none') #prevents axes background from hiding artists below
ax3.set_axis_off() # pervents superimposed ticks from being drawn
color_fav = 'tab:blue'
color_re = 'darkgrey'
ax2.plot(temp.index.values, temp['favorites'], color=color_re, label='favorites')
ax3.plot(temp.index.values, temp['counts'], color=color_fav, label='count')
ax2.set_ylabel('Favorites [in thousand]', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of tweets', color=color_fav)
ax1.tick_params(axis='y', labelcolor=color_fav)
ax2.grid(None)
ax3.grid(None)
lines, labels = ax3.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_favorites_counts_weekly.pdf')





################################################################
# Sentiment of Greta Thunberg's Tweets
################################################################

# histogram of positive or negative tweets
from textblob import TextBlob



# eliminate urls
def remove_url(txt):
     return " ".join(re.sub(r'http\S+', '', txt).split())

tweets_no_urls = [remove_url(tweet) for tweet in raw_tweets]
sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]
sentiment_objects[1].polarity, sentiment_objects[1]

sentiment_values = [[tweet.sentiment.polarity,
                     tweet.sentiment.subjectivity,
                     str(tweet)] for tweet in sentiment_objects]
sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity",
                                                       'subjectivity', "tweet"])




# Polarity histogram conditional on having a polarity
polarity_df = sentiment_df[sentiment_df.polarity != 0]


sns.distplot(polarity_df.polarity, hist=True, kde=True, norm_hist=False, color = 'darkblue',
             hist_kws={'edgecolor':'black'})
plt.ylabel('Density')
plt.xlabel('')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_polarity_hist.pdf')

# add vertical line





subjectivity_df = sentiment_df[sentiment_df.subjectivity != 0]


sns.distplot(subjectivity_df.subjectivity, hist=True, kde=True, norm_hist=False, color = 'darkblue',
             hist_kws={'edgecolor':'black'})
plt.ylabel('Density')
plt.xlabel('')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_subjectivity_hist.pdf')









# readability scores

