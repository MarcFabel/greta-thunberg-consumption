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
import matplotlib.dates as mdates



#style.available
#style.use('seaborn-darkgrid')
style.use('seaborn-white')


# HOME directory
z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'
z_media_figures =   '/Users/marcfabel/Desktop/twitter_fff_figures/'
z_prefix =          'greta_cons_'
z_figures_diss =    '/Users/marcfabel/econ/greta_consumption/analysis/output/graphs/descriptive/'
z_media_output =    '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/temp/twitter_print_media/'


# work directories (LOCAL)
#z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'
#z_media_figures =   'W:/EoCC/analysis/output/graphs/descriptive/'
#z_prefix =          'greta_cons_'



# color
c_shading = 'darkgreen'
c_opacity = 0.4

###############################################################################
#           Read in & prepare Data
###############################################################################



#############################################
# generate dictionary of activist
list_twitter_accounts = sorted(['GretaThunberg', 'Luisamneubauer', 'jakobblasel', 'carla_reemtsma',
         'FranziWessel', 'FridayForFuture', 'Ende__Gelaende', 'parents4future',
         'ExtinctionR_DE', 'sciforfuture'], key=str.lower)
dfs = {p: pd.read_csv(z_media_input + 'twitter_' +  p + '.csv', sep='\t',
                      index_col='date', parse_dates=True, encoding = "utf-8")
      for p in list_twitter_accounts}


# more workable keys:
dfs['greta']  = dfs.pop('GretaThunberg')
dfs['luisa']  = dfs.pop('Luisamneubauer')
dfs['jakob']  = dfs.pop('jakobblasel')
dfs['carla']  = dfs.pop('carla_reemtsma')
dfs['franzi'] = dfs.pop('FranziWessel')
dfs['f4f']    = dfs.pop('FridayForFuture')
dfs['ende']   = dfs.pop('Ende__Gelaende')
dfs['p4f']    = dfs.pop('parents4future')
dfs['extreb'] = dfs.pop('ExtinctionR_DE')
dfs['s4f']    = dfs.pop('sciforfuture')


z_list_activists = list(dfs.keys())

# use dictionary to have short (work in code) and long (save output) keys
z_dict_keys_sl = {
        	'carla' 	: 'carla_reemtsma',
		'ende'  	: 'Ende__Gelaende',
		'extreb'	: 'ExtinctionR_DE',
		'franzi'	: 'FranziWessel',
		'f4f'   	: 'FridayForFuture',
		'greta' 	: 'GretaThunberg',
		'jakob' 	: 'jakobblasel',
		'luisa' 	: 'Luisamneubauer',
		'p4f'   	: 'parents4future',
		's4f'   	: 'sciforfuture'
          }
# swap key, value pairs
z_dict_keys_ls = dict([(value, key) for key, value in z_dict_keys_sl.items()])



for activist in z_list_activists:
    dfs[activist]['favorites'] = dfs[activist]['favorites'] / 1000
    dfs[activist]['retweets'] = dfs[activist]['retweets'] / 1000
    dfs[activist + '_w'] = dfs[activist].resample('W').sum()




# export 2019 greta weekly to gen graph in stata
dfs['greta_w'].loc['2019'].to_csv(z_media_output+ z_prefix + 
   'greta_2019_weekly_favorites_retweets.csv',
   sep=';', encoding='UTF-8', index=True)




###############################################################################
#           Graphs
###############################################################################


##########  Graph : favorites and retweets per activist #######################
for activist in z_list_activists:
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
	plt.savefig(z_media_figures + z_prefix + 'twitter_favorites_retweets_' +
				z_dict_keys_sl[activist]  +'.pdf')



    
    



###############################################################################
# Luisa Neubauer Favorites with events
txt = '''
    The green lines/areas indicate important events: 
    1) Climate Strike Hamburg (01.03.2019), 2) 1st Global Climate Strike - more than 1.4 million people
    involved (15.03.2019), 3) Greta Thunberg's speech in Strasbourg in front of EU Parliament (16.04.2019)
    4) 2nd Global Climate Strike - just before EU elections (24.05.2019),  5) Greta Thunberg starts journey
    across Atlantic (14.08.2019), 6) 3rd Global Climate Strike + UN Climate Action Summit in NY (29.09.2019)
    7) 4th Global Climate Strike + UN Climate Change Conference in Madrid (Nov/Dec 2019), 
    8) World Economic Forum in Davos (January 2020), 9) Online Strike during Corona Pandemic (April 2020)
    10) Corona Stimulus Package #KlimazielstattLobbyDeal (June 2020)
    '''

fig, ax = plt.subplots()
ax.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax.axvline(datetime(2019,5,24), color=c_shading, alpha=c_opacity)                         # 2nd global climate strike (EU election)
ax.axvline(datetime(2019,8,14), color=c_shading, alpha=c_opacity)                         # start travel Atlantic - travel to UN
ax.axvspan(datetime(2019,9,20), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # 3rd global climate strike + NY - UN climate action summit
ax.axvspan(datetime(2019,11,29), datetime(2019,12,13), color=c_shading, alpha=c_opacity)  # 4th global climate strike + Madrid - UN climate change conference
ax.axvspan(datetime(2020,1,20), datetime(2020,1,24), color=c_shading, alpha=c_opacity)    # Davos WEF
ax.axvline(datetime(2020,4,24), color=c_shading, alpha=c_opacity)                         # online strike during corona pandemic
ax.axvline(datetime(2020,6,2), color=c_shading, alpha=c_opacity)                          # Corona-Konjunkturpaket
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
fig.text(.1, -0.25, txt, ha='left', wrap=True, fontsize=7)

ax.plot(dfs['luisa_w'].loc['2019':].index.values,
        dfs['luisa_w'].loc['2019':]['favorites'],
        color='darkblue',
        label='luisa')
ax.set_title('Twitter feed of Luisamneubauer', fontweight='bold')
ax.set(xlabel='Date', ylabel='Favorites [in thousand]')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig(z_media_figures + z_prefix + 'twitter_luisa_favorites_events.pdf', bbox_inches = "tight")









##########  Graphs : compare the activists ####################################

#w/o greta thunberg - has to be programmed as spaghetti graph
# dictionary color
tab_color_palette = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
                     'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                     'tab:olive', 'tab:cyan']
tab_color_palette = tab_color_palette[:len(z_list_activists)] # shorten the color pallete to the number of activists w/o greta
z_dict_activists_color = dict(zip(z_list_activists, tab_color_palette))


# likes: all in one graph
fig, ax = plt.subplots()
for activist in z_list_activists:
     ax.plot(dfs[activist + '_w'].index.values, dfs[activist+'_w']['favorites'],
             label=z_dict_keys_sl[activist],
             color=z_dict_activists_color[activist])
ax.legend(loc='upper left')
ax.set_ylabel('Favorites [in thousand]')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
plt.savefig(z_media_figures + z_prefix + 'twitter_favorites_spaghetti_all.pdf')



     
# Spaghetti graph
fig, axs = plt.subplots(3, 3,  figsize=(12,9))
fig.subplots_adjust(hspace = .5)
#fig = plt.gcf()
#fig.suptitle('Favorites [in thousand]', fontsize=16)
axs = axs.ravel()

num = 0
for activist in z_list_activists[1:]:
    temp = z_list_activists.copy()[1:] # list w/o greta
    temp.remove(activist)

    axs[num].plot(dfs[activist+ '_w'].loc['2019'].index.values, dfs[activist+ '_w'].loc['2019']['favorites'],
            linewidth=2, alpha=0.99, label=z_dict_keys_sl[activist],
            color=z_dict_activists_color[activist])
    for other_activists in temp:
         axs[num].plot(dfs[other_activists+'_w'].loc['2019'].index.values,
                 dfs[other_activists+ '_w'].loc['2019']['favorites'],
                 color='grey', linewidth=0.3, alpha=0.7)
#    axs[num].legend(loc='upper center')
    axs[num].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    #axs[num].xaxis.set_minor_locator(mdates.YearLocator())
    axs[num].xaxis.set_major_formatter(mdates.DateFormatter('%b%y'))
    #axs[num].xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
    axs[num].spines['right'].set_visible(False)
    axs[num].spines['top'].set_visible(False)
    axs[num].set_title(z_dict_keys_sl[activist], fontsize=11,
       color=z_dict_activists_color[activist])
    num+=1

plt.savefig(z_figures_diss + z_prefix + 'twitter_favorites_spaghetti_wo_greta_2019.pdf',
            bbox_inches = 'tight')


  

##########  Graph : favorites and retweets Greta only #########################

temp = dfs['greta_w'].loc['2019'].copy()


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

# ask matplotlib for the plotted objects and their labels
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_favorites_retweets_weekly.pdf')



# with events
txt = '''
    The green lines/areas indicate important events: 
    1) Climate Conference Katowice (Dec 2018), 2) WEF in Davos (Jan 2019) 3) 1st Global Climate Strike (Mar 2019),
    4) Speech British Parliament (Apr 2019), 5) Speech French Parliament (July 2019), 6) Journey across Atlantic
    (Aug 2019), 7) UN Climate Action Summit in NY (Sep 2019), 8) UN Climate Change Conference in Madrid, 
    Time's Person of the Year, UK elections (Nov/Dec 2019), 9) WEF in Davos (Jan 2020), 
    10) Meeting w/ Malala Yousafzai (Feb 2020)
    '''

fig, ax1 = plt.subplots()
ax1.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # 1 Katowice - climate conference
ax1.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # 2 Davos - world economic forum
ax1.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # 3 worldwide - 1.4 million young people go on strike (friday)
ax1.axvline(datetime(2019,4,23), color=c_shading, alpha=c_opacity)                         # 4 Speech in front of British Parliament
ax1.axvline(datetime(2019,7,24), color=c_shading, alpha=c_opacity)                         # 5 Speech in front of Fench Parliament
ax1.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # 6 Atlantic - travel to UN
ax1.axvspan(datetime(2019,9,20), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # 7 NY - UN climate action summit
ax1.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # 8 Madrid - UN climate change conference & Time Person of the Year & Tweet about UK election
ax1.axvspan(datetime(2020,1,20), datetime(2020,1,24), color=c_shading, alpha=c_opacity)    # 9 Davos WEF
ax1.axvline(datetime(2020,2,25), color=c_shading, alpha=c_opacity)                         # 10 Greta meets Malala Yousafzai (Nobel laureate 2014)

ax2 = ax1.twinx()
color_re = 'tab:orange'
ax2.plot(temp.index.values, temp['retweets'], color=color_re, label='retweets', alpha=0.9)
ax2.set_ylabel('retweets [in thousand]', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
color_fav = 'darkblue'
ax1.plot(temp.index.values, temp['favorites'], color=color_fav, label='favorites') 
ax1.set_xlabel('Date')
ax1.set_ylabel('Favorites [in thousand]', color=color_fav)
ax1.tick_params(axis='y', labelcolor=color_fav)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
#ax1.spines['right'].set_visible(False)
#ax2.spines['right'].set_visible(False)
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax1.xaxis.set_minor_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
fig.text(.1, -0.25, txt, ha='left', wrap=True, fontsize=7)
ax1.set_title('Twitter feed of GretaThunberg', fontweight='bold')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_favorites_retweets_weekly_events.pdf',
             bbox_inches = "tight")



################################################################
# Number of Tweets by Greta Thunberg
################################################################
temp = dfs['greta'].copy()
temp['counts'] = 1
temp = temp.resample('W').sum()



# mit drei Achsen##################################
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



# we would also need the number of followers: Hiwi-fun with
# https://web.archive.org/web/20190501000000*/https://twitter.com/GretaThunberg
# https://stackoverflow.com/questions/4084909/how-to-get-a-count-of-followers-from-twitter-api-and-trendline
# https://ws-dl.blogspot.com/2018/03/2018-03-14-twitter-follower-count.html



###############################################################################
#           NLP
###############################################################################
greta = dfs['greta'].loc['2019'].copy()


## classify language of tweet
#from langdetect import detect
#import numpy as np
#
## define missing values as str.nan
#greta['text'] = greta['text'].replace('', np.nan)
#greta['text'] = greta['text'].replace(' ', np.nan)
#
#
#
#
## there are two tweets that just contain links, which cannot be classified as language
#criterium_no_link = (greta['text'] != 'https://www.fridaysforfuture.org') & \
#    (greta['text'] != 'https://unfccc-cop25.streamworld.de/webcast/high-level-event-on-climate-emergency')
#
#greta['lang'] = greta.loc[greta.text.notnull() & criterium_no_link].text.apply(detect)
#
#
## correct language missclassifications
#temp1 = greta.loc[greta.lang != 'en']
#
#lang_misclass = ['af', 'ca', 'cs', 'cy', 'et', 'fi', 'id', 'it', 'no', 'pl',
#                 'pt', 'ro', 'sl', 'so', 'sw', 'tl', 'tr']
#for lang in lang_misclass:
#    greta['lang'] = greta['lang'].replace(lang, 'en')
#
#temp1 = greta.loc[greta.lang != 'en']
#
#
#
#
#
## change order of columns
#z_cols_to_order = ['favorites', 'retweets', 'lang', 'text']
#z_new_columns = z_cols_to_order + (greta.columns.drop(z_cols_to_order).tolist())
#greta = greta[z_new_columns]




################################################################
# Word Cloud
###############################################################

from wordcloud import WordCloud, STOPWORDS
import re
from string import digits, punctuation
import nltk

import random


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

# eliminate urls, hastags, and mentions
no_links = re.sub(r'http\S+', '', raw_string)
no_hashtags = re.sub(r'#\S+', '', no_links)
no_mentions = re.sub(r'@\S+', '', no_hashtags)

# remove punctuation and special characters
remove = digits + punctuation + '“”—'
remove
no_punctuation = no_mentions.translate(str.maketrans({p: "" for p in remove}))


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
plt.savefig(z_figures_diss + z_prefix + 'twitter_greta_word_cloud.pdf')







################################################################
# Top Words in Greta Thunberg's Tweets
################################################################

import seaborn as sns


# generate df with number of occurences per word
dfwords = pd.DataFrame(words, columns=['words'])
dfwords['counts'] = 1
words_nr = dfwords.groupby(['words']).sum()
words_nr.sort_values(['counts'], inplace=True, ascending=False)
words_nr = words_nr[:20]

# bar
fig, ax = plt.subplots()
ax = sns.barplot(words_nr.index, words_nr.counts, palette='Blues_d') #
ax.set(xlabel='', ylabel='Number of uses')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for item in ax.get_xticklabels():
     item.set_rotation(90)
plt.tight_layout()      # makes room for the x-label (as it is quite wide)
plt.savefig(z_figures_diss + z_prefix + 'twitter_greta_frequency_common_words.pdf')



##########  Graphs : top hashtags #############################################

# make hashtags into list
raw_hashtags = greta.hashtags.values.tolist()

# eliminate empty fields
raw_hashtags =  [x for x in raw_hashtags if type(x)== str]

# seperate lists entries further to have one hashtag per entry
raw_hashtags = ' '.join(raw_hashtags)
hashtags = raw_hashtags.split(" ")

# make entries lower-case
hashtags = [h.lower() for h in hashtags]


# unify fridays for future
hashtags = [sub.replace('#fridayforfuture', '#fridaysforfuture') for sub in hashtags]
hashtags = [sub.replace('#fridaysforfurture', '#fridaysforfuture') for sub in hashtags]
hashtags = [sub.replace('#schoolsstrike4climate', '#schoolstrike4climate') for sub in hashtags]


# generate df with number of occurences per hashtag
dfhashtags = pd.DataFrame(hashtags, columns=['hashtags'])
dfhashtags['counts'] = 1
hashtags_nr = dfhashtags.groupby(['hashtags']).sum()
hashtags_nr.sort_values(['counts'], inplace=True, ascending=False)
# keep if hashtag is appearing at least 5 times
hashtags_nr = hashtags_nr[:10]

# bar
fig, ax = plt.subplots()
ax = sns.barplot(hashtags_nr.index, hashtags_nr.counts, palette='Blues_d') #
ax.set(xlabel='', ylabel='Number of uses')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for item in ax.get_xticklabels():
     item.set_rotation(90)
plt.tight_layout()      # makes room for the x-label (as it is quite wide)
plt.savefig(z_figures_diss + z_prefix + 'twitter_greta_frequency_common_hashtags.pdf')




##########  Graphs : top mentions #############################################

# make mentions into list
raw_mentions = greta.mentions.values.tolist()

# eliminate empty fields
raw_mentions =  [x for x in raw_mentions if type(x)== str]

# seperate lists entries further to have one hashtag per entry
raw_mentions = ' '.join(raw_mentions)
mentions = raw_mentions.split(" ")

# generate df with number of occurences per hashtag
dfmentions = pd.DataFrame(mentions, columns=['mentions'])
dfmentions['counts'] = 1
mentions_nr = dfmentions.groupby(['mentions']).sum()
mentions_nr.sort_values(['counts'], inplace=True, ascending=False)
# show 10 most cited mentions
mentions_nr = mentions_nr[:10]



# bar
txt = '''
    The figure lists the ten most frequent mentions in Greta Thunberg’s tweets. 
    The people/organizations behind the Twitter accounts are: 
    @_NikkiHenderson, @Sailing_LaVaga, @elayna_c (Sailors), @GeorgeMonbiot (British writer and politcal activist), 
    @KevinClimate (Professor of energy and climate change),  @AnunaDe (Belgian climate activist),
    @Luisamneubauer (German climate activist), @jrockstrom (Director of Potsdam Institute for Climate Impact Research),
    @ExtinctionR (Global environmental movement),  @NaomiAKlein (Journalist, author, activist, and professor).
    '''

fig, ax = plt.subplots()
ax = sns.barplot(mentions_nr.index, mentions_nr.counts, palette='Blues_d') #
ax.set(xlabel='', ylabel='Number of uses')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for item in ax.get_xticklabels():
     item.set_rotation(90)
plt.tight_layout()      # makes room for the x-label (as it is quite wide)
#fig.text(.1, -0.25, txt, ha='left', wrap=True, fontsize=7)

plt.savefig(z_figures_diss + z_prefix + 'twitter_greta_frequency_common_mentions.pdf',
            bbox_inches = 'tight')









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
subjectivity_df = sentiment_df[sentiment_df.subjectivity != 0]


# Histogram of polarity and subjectivity
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16,6))
sns.despine()

sns.distplot(polarity_df.polarity, hist=True, kde=True, norm_hist=False, 
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax1)
sns.distplot(subjectivity_df.subjectivity, hist=True, kde=True, norm_hist=False,
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax2)
ax1.set_xlabel('')
ax2.set_xlabel('')
ax1.set_title('Polarity')
ax2.set_title('Subjectivity')
plt.savefig(z_media_figures + z_prefix + 'twitter_greta_subjectivity_polarity_hist.pdf')




##########  Polarity and Subjectivity for all activists #######################
temp = {}
for activist in z_list_activists:

     # make tweets into list
     raw_tweets = dfs[activist].text.values.tolist()

     # eliminate empty fields
     raw_tweets =  [x for x in raw_tweets if type(x)== str]

     tweets_no_urls = [remove_url(tweet) for tweet in raw_tweets]
     sentiment_objects = [TextBlob(tweet) for tweet in tweets_no_urls]
     sentiment_objects[1].polarity, sentiment_objects[1]

     sentiment_values = [[tweet.sentiment.polarity,
                     tweet.sentiment.subjectivity] for tweet in sentiment_objects]
     sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity",
                                                       'subjectivity'])

     temp[activist] = [sentiment_df[sentiment_df['polarity'] != 0].polarity.mean(),
          sentiment_df[sentiment_df['polarity'] != 0].polarity.std(),
          sentiment_df[sentiment_df['subjectivity'] != 0].subjectivity.mean(),
          sentiment_df[sentiment_df['subjectivity'] != 0].subjectivity.mean()]

df_polarity_subjectivty = pd.DataFrame.from_dict(temp, orient='index',
                                                 columns=['pol_m', 'pol_sd', 'sub_m', 'sub_sd'])


# change index values
df_polarity_subjectivty.index = df_polarity_subjectivty.index.map(z_dict_keys_sl)


# export the dataframe to a scatter plot
fig, ax = plt.subplots()
ax = sns.scatterplot(x=df_polarity_subjectivty["pol_m"],
                     y=df_polarity_subjectivty["sub_m"],
                     hue= df_polarity_subjectivty.index)
ax.set_xlabel('mean polarity')
ax.set_ylabel('mean subjectivity')

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True,  ncol=5)
#plt.savefig(z_media_figures + z_prefix + 'twitter_activists_scatter_polarity_subjectivity.pdf',
#             bbox_inches='tight')









###############################################################################
# Readability scores: Greta Thunberg

import textstat
import numpy as np

# drop empty text fields
temp = greta.copy()
temp['text'].replace('', np.nan, inplace=True)
temp['text'].replace(' ', np.nan, inplace=True)
temp.dropna(subset=['text'], inplace=True)


temp['syl_count'] = temp.text.apply(lambda x: textstat.syllable_count(x))
temp['word_count'] = temp.text.apply(lambda x: textstat.lexicon_count(x, removepunct=True))
temp['sent_count'] = temp.text.apply(lambda x: textstat.sentence_count(x))
temp['score_fre'] = temp.text.apply(lambda x: textstat.flesch_reading_ease(x))
temp['score_are'] = temp.text.apply(lambda x: textstat.automated_readability_index(x))
temp['char_count'] = temp.text.apply(lambda x: len(x))


sns.distplot(temp.word_count, hist=True, kde=False, norm_hist=True, color = 'darkblue', hist_kws={'edgecolor':'black'})






fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(nrows=2, ncols=2, figsize=(8,6))
fig.subplots_adjust(hspace = .5)
sns.despine()
fig = plt.gcf()
#fig.suptitle('Sentiment and length of tweets [GretaThunberg]', fontsize=16)

ax1.axvline(polarity_df.polarity.mean(), color='darkred', alpha=c_opacity, linestyle='dashed')
ax1.axvline(polarity_df.polarity.median(), color='darkblue', alpha=c_opacity, linestyle='dashed')
sns.distplot(polarity_df.polarity, hist=True, kde=False, norm_hist=True, 
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax1)


ax2.axvline(subjectivity_df.subjectivity.mean(), color='darkred', alpha=c_opacity, linestyle='dashed')
ax2.axvline(subjectivity_df.subjectivity.median(), color='darkblue', alpha=c_opacity, linestyle='dashed')
sns.distplot(subjectivity_df.subjectivity, hist=True, kde=False, norm_hist=True,
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax2)

ax3.axvline(temp.loc[temp.char_count < 281].char_count.mean(), color='darkred', alpha=c_opacity, linestyle='dashed', label='mean')
ax3.axvline(temp.loc[temp.char_count < 281].char_count.median(), color='darkblue', alpha=c_opacity, linestyle='dashed', label='median')
sns.distplot(temp.loc[temp.char_count < 281].char_count, hist=True, kde=False, norm_hist=True,
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax3)

ax4.axvline(temp.word_count.mean(), color='darkred', alpha=c_opacity, linestyle='dashed', label='mean')
ax4.axvline(temp.word_count.median(), color='darkblue', alpha=c_opacity, linestyle='dashed', label='median')
ax4.legend(loc='upper right')
sns.distplot(temp.word_count, hist=True, kde=False, norm_hist=True,
             color = 'darkblue', hist_kws={'edgecolor':'black'}, ax=ax4)

ax1.set_xlabel('')
ax2.set_xlabel('')
ax3.set_xlabel('')
ax4.set_xlabel('')
ax1.set_title('Polarity')
ax2.set_title('Subjectivity')
ax3.set_title('Character count')
ax4.set_title('Word count')


plt.savefig(z_figures_diss + z_prefix + 'twitter_activists_scatter_polarity_subjectivity_word_count.pdf',
             bbox_inches='tight')







