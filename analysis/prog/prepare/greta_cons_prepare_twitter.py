#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:58:06 2020

@author: marcfabel
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates
from datetime import timedelta, date,datetime


#style.available
style.use('seaborn-darkgrid')



z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/media/'
greta = pd.read_csv(z_media_input + 'twitter_greta_thunberg_FINAL.csv', sep='\t',
                    index_col='date', parse_dates=True, encoding = "ISO-8859-1")


greta_num = greta[['favorites', 'retweets']]

temp = greta_num.resample('D').sum()



c_shading = 'darkgreen'
c_opacity = 0.4

fig, ax = plt.subplots()
ax.plot(temp.index.values, temp['favorites'])
ax.plot(temp.index.values, temp['retweets'])

ax.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # Katowice - climate conference
ax.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax.axvline(datetime(2019,3,29), color=c_shading, alpha=c_opacity)                         # Berlin - climate strike with Greta (friday)
ax.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # Atlantic - travel to UN
ax.axvspan(datetime(2019,9,23), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # NY - UN climate action summit
ax.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # Madrid - UN climate change conference




# To do: nochmal scrapen: es gibt ein Loch zwischen 03. März und 05. Juli??


# Descriptives
#           favorites      retweets
#count     466.000000    466.000000
#mean     3750.731760    981.351931
#std     10008.629786   2545.397665
#min         0.000000      0.000000
#25%        70.500000      5.000000
#50%       746.000000    150.000000
#75%      3695.500000    860.500000
#max    164076.000000  35187.000000


# we would also need the number of followers: Hiwi-fun with 
# https://web.archive.org/web/20190501000000*/https://twitter.com/GretaThunberg