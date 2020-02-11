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
z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'


# work directories (LOCAL)
#z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/twitter/'
#z_media_figures =   'G:/Projekte/Projekte_ab2016/greta_cons/analysis/output/graphs/descriptive/'
#z_prefix =          'greta_cons_'


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


