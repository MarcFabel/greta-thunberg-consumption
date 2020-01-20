#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:10:40 2020

@author: marcfabel

Description

Inputs:
    genios_articles_greta.csv
    genios_articles_all.csv

Outputs:

"""

# packages
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.dates as mdates

#style.available
style.use('seaborn-darkgrid')
import pandas as pd
import seaborn as sns


# HOME directories
#z_media_input =     '/Users/marcfabel/Dropbox/greta_consumption_Dx/analysis/data/intermediate/media/'

# work directories (LOCAL)
z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/media/'
z_media_figures =   'G:/Projekte/Projekte_ab2016/greta_cons/analysis/output/graphs/descriptive/'
z_prefix =          'greta_cons_'

###############################################################################
#           Read in Data
###############################################################################


########## generate dfs  ######################################################
greta = pd.read_csv(z_media_input + 'genios_articles_greta_thunberg.csv', sep=',',
                    names=['date', 'art_greta'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)

fff = pd.read_csv(z_media_input + 'genios_articles_FFF.csv', sep=',',
                    names=['date', 'art_fff'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)


articles = pd.read_csv(z_media_input + 'genios_articles_all.csv', sep=',',
                       names=['date', 'art_all'], header=0,
                       index_col='date', parse_dates=True , dayfirst=True)


########## merge dfs  #########################################################
articles = articles.join(greta, how='inner')
articles = articles.join(fff, how='inner')


########## generate variables  ################################################

# number of articles per thousand
articles['art_greta_ratio'] = articles['art_greta'] * 1000 / articles['art_all']
articles['art_fff_ratio'] = articles['art_fff'] * 1000 / articles['art_all']


# day of the week
articles['dow'] 	= articles.index.map(lambda x: x.strftime('%a'))



# moving averages
articles['art_greta_ma3'] = articles.art_greta.rolling(window=3).mean()
articles['art_greta_ratio_ma3'] = articles.art_greta_ratio.rolling(window=3).mean()
articles['art_greta_ratio_ma7'] = articles.art_greta_ratio.rolling(window=7).mean()

articles['art_fff_ma3'] = articles.art_fff.rolling(window=3).mean()
articles['art_fff_ratio_ma3'] = articles.art_fff_ratio.rolling(window=3).mean()
articles['art_fff_ratio_ma7'] = articles.art_fff_ratio.rolling(window=7).mean()



###############################################################################
#           Plot Time Series
###############################################################################


########## Greta Thunberg #####################################################


########## plot greta articles for entire time horizon ########################
fig, ax = plt.subplots()
ax.plot(articles.index.values, articles['art_greta'])
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
plt.savefig(z_media_figures + z_prefix + 'greta_2018_2019.pdf')



########## plot greta articles per 1,000 articles for entire time horizon #####
fig, ax = plt.subplots()
ax.plot(articles.index.values, articles['art_greta_ratio'])
ax.plot(articles.index.values, articles['art_greta_ratio_ma7'])
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
plt.savefig(z_media_figures + z_prefix + 'greta_per_1000_2018_2019.pdf')



########## plot for the year 2019 #############################################
c_shading = 'darkgreen'
c_opacity = 0.3

fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta, alpha=0.3, color='darkgrey')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ma3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
#events
ax.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # Katowice - climate conference
ax.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike
ax.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # Atlantic - travel to UN
ax.axvspan(datetime(2019,9,23), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # NY - UN climate action summit
ax.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # Madrid - UN climate change conference
#plt.savefig(z_media_figures + z_prefix + 'greta_events_2019.pdf')


articles.loc['2019'].art_greta.plot()
articles.loc['2019'].art_greta_ma3.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'greta_2019.pdf')
plt.show()


########## plot greta articles per 1,000 articles - 2019 ######################
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio, alpha=0.3, color='darkgrey')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio_ma3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
#events
ax.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # Katowice - climate conference
ax.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax.axvline(datetime(2019,3,29), color=c_shading, alpha=c_opacity)                         # Berlin - climate strike with Greta (friday)
ax.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # Atlantic - travel to UN
ax.axvspan(datetime(2019,9,23), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # NY - UN climate action summit
ax.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # Madrid - UN climate change conference
#plt.savefig(z_media_figures + z_prefix + 'greta_per_1000_events_2019.pdf')


articles.loc['2019'].art_greta_ratio.plot()
articles.loc['2019'].art_greta_ratio_ma3.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'greta_per_1000_2019.pdf')
plt.show()



########## Fridays For Future #################################################

# plot fff articles for entire time horizon
articles.art_fff.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'fff_2018_2019.pdf')
plt.show()

#plot fff articles per 1,000 articles for entire time horizon
articles.art_fff_ratio.plot()
articles.art_fff_ratio_ma7.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'fff_per_1000_2018_2019.pdf')
plt.show()


# plot for the year 2019
articles.loc['2019'].art_fff.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'fff_2019.pdf')
plt.show()


# plot fff articles per 1,000 articles
articles.loc['2019'].art_fff_ratio.plot()
articles.loc['2019'].art_fff_ratio_ma3.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'fff_per_1000_2019.pdf')
plt.show()
