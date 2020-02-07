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
#z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'


# work directories (LOCAL)
z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'
z_media_figures =   'G:/Projekte/Projekte_ab2016/greta_cons/analysis/output/graphs/descriptive/'
z_prefix =          'greta_cons_'


###############################################################################
#           Read in & prepare Data
###############################################################################

greta = pd.read_csv(z_media_input + 'twitter_greta_thunberg_FINAL.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "ISO-8859-1")

greta['favorites'] = greta['favorites'] / 1000
greta['retweets']  = greta['retweets']  / 1000


temp = greta.resample('W').sum()


#           favorites       retweets
#count    1137.000000    1137.000000
#mean    22510.556728    3872.345646
#std     55636.754014    8923.097434
#min         0.000000       0.000000
#25%       776.000000     143.000000
#50%      6024.000000    1261.000000
#75%     19014.000000    3988.000000
#max    797112.000000  130185.000000






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









# check: prorgam read-in linewise and check dimension
import csv



with open(z_media_input + 'twitter_greta_thunberg_FINAL.csv', 'r') as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print('{}:  {} entries'.format(i,len(line)))






