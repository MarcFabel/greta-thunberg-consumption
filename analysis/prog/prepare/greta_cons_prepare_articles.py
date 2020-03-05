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
import numpy as np

#style.available
style.use('seaborn-darkgrid')
import pandas as pd


# HOME directories
#z_media_input =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'



# work directories (LOCAL)
z_media_input =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'
z_media_figures =   'W:/EoCC/analysis/output/graphs/descriptive/'
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

school = pd.read_csv(z_media_input + 'genios_articles_school_management.csv', sep=',',
                    names=['date', 'art_school'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)

articles = pd.read_csv(z_media_input + 'genios_articles_all.csv', sep=',',
                       names=['date', 'art_all'], header=0,
                       index_col='date', parse_dates=True , dayfirst=True)

greta_sz = pd.read_csv(z_media_input + 'outlets/genios_articles_SZ_greta_thunberg.csv', sep=',',
                    names=['date', 'art_greta_sz'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)

greta_faz = pd.read_csv(z_media_input + 'outlets/genios_articles_FAZ_greta_thunberg.csv', sep=',',
                    names=['date', 'art_greta_faz'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)

articles_sz = pd.read_csv(z_media_input + 'outlets/genios_articles_SZ_all.csv', sep=',',
                       names=['date', 'art_all_sz'], header=0,
                       index_col='date', parse_dates=True , dayfirst=True)

articles_faz = pd.read_csv(z_media_input + 'outlets/genios_articles_FAZ_all.csv', sep=',',
                       names=['date', 'art_all_faz'], header=0,
                       index_col='date', parse_dates=True , dayfirst=True)


########## merge dfs  #########################################################
articles = articles.join(greta, how='inner')
articles = articles.join(fff, how='inner')
articles = articles.join(school, how='inner')
articles = articles.join(greta_sz, how='outer')
articles = articles.join(greta_faz, how='outer')
articles = articles.join(articles_sz, how='outer')
articles = articles.join(articles_faz, how='outer')


########## generate variables  ################################################

# number of articles per thousand
articles['art_greta_ratio'] = articles['art_greta'] * 1000 / articles['art_all']
articles['art_fff_ratio'] = articles['art_fff'] * 1000 / articles['art_all']
articles['art_school_ratio'] = articles['art_school'] * 1000 / articles['art_all']


# day of the week
articles['dow'] 	= articles.index.map(lambda x: x.strftime('%a'))



# moving averages
articles['art_greta_ma3'] = articles.art_greta.rolling(window=3).mean()
articles['art_greta_ratio_ma3'] = articles.art_greta_ratio.rolling(window=3).mean()
articles['art_greta_ratio_ma7'] = articles.art_greta_ratio.rolling(window=7).mean()

articles['art_fff_ma3'] = articles.art_fff.rolling(window=3).mean()
articles['art_fff_ratio_ma3'] = articles.art_fff_ratio.rolling(window=3).mean()
articles['art_fff_ratio_ma7'] = articles.art_fff_ratio.rolling(window=7).mean()

articles['art_school_ma3'] = articles.art_school.rolling(window=3).mean()
articles['art_school_ratio_ma3'] = articles.art_school_ratio.rolling(window=3).mean()
articles['art_school_ratio_ma7'] = articles.art_school_ratio.rolling(window=7).mean()


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
plt.savefig(z_media_figures + z_prefix + 'genios_greta_2018_2019.pdf')



########## plot greta articles per 1,000 articles for entire time horizon #####
fig, ax = plt.subplots()
ax.plot(articles.index.values, articles['art_greta_ratio'])
ax.plot(articles.index.values, articles['art_greta_ratio_ma7'])
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
plt.savefig(z_media_figures + z_prefix + 'genios_greta_per_1000_2018_2019.pdf')



########## plot greta articles per 1,000 articles - 2019 ######################
c_shading = 'darkgreen'
c_opacity = 0.4


# without events
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio, alpha=0.6, color='darkgrey', label='unsmoothed')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio_ma3, label='smoothed')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
ax.legend()
ax.set(xlabel='Date', ylabel='Number of articles covering Greta Thunberg,\n per 1,000 articles') #xlabel='months',
plt.savefig(z_media_figures + z_prefix + 'genios_greta_per_1000_2019.pdf')




# with events
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio, alpha=0.006, color='darkgrey', label='unsmoothed')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio_ma3, label='smoothed')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
ax.set(xlabel='Date', ylabel='Number of articles covering Greta Thunberg,\n per 1,000 articles')

ax.axvspan(datetime(2018,12,3), datetime(2018,12,14), color=c_shading, alpha=c_opacity)   # Katowice - climate conference
ax.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax.axvline(datetime(2019,3,29), color=c_shading, alpha=c_opacity)                         # Berlin - climate strike with Greta (friday)
ax.axvline(datetime(2019,4,16), color=c_shading, alpha=c_opacity)                         # Strasbourg - EU speech
ax.axvline(datetime(2019,5,24), color=c_shading, alpha=c_opacity)                         # 2nd Global Climate Strike (for EU elections)
ax.axvspan(datetime(2019,8,14), datetime(2019,8,28), color=c_shading, alpha=c_opacity)    # Atlantic - travel to UN
ax.axvspan(datetime(2019,9,23), datetime(2019,9,29), color=c_shading, alpha=c_opacity)    # NY - UN climate action summit
ax.axvspan(datetime(2019,12,2), datetime(2019,12,13), color=c_shading, alpha=c_opacity)   # Madrid - UN climate change conference
plt.savefig(z_media_figures + z_prefix + 'genios_greta_per_1000_events_2019.pdf')






########## Fridays For Future #################################################


########## plot fff articles per 1,000 articles - 2019 ######################


# without events
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio, alpha=0.6, color='darkgrey', label='unsmoothed')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio_ma3, label='smoothed')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
ax.legend()
ax.set(xlabel='Date', ylabel='Number of articles covering FFF,\n per 1,000 articles') #xlabel='months',
plt.savefig(z_media_figures + z_prefix + 'genios_fff_per_1000_2019.pdf')




#events
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio, alpha=0.006, color='darkgrey', label='unsmoothed')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio_ma3, label='smoothed')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
ax.set(xlabel='Date', ylabel='Number of articles covering FFF,\n per 1,000 articles')
ax.axvspan(datetime(2019,1,23), datetime(2019,1,25), color=c_shading, alpha=c_opacity)    # Davos - world economic forum
ax.axvline(datetime(2019,3,1), color=c_shading, alpha=c_opacity)                          # Hamburg - climate strike with Greta (friday)
ax.axvline(datetime(2019,3,15), color=c_shading, alpha=c_opacity)                         # worldwide - 1.4 million young people go on strike (friday)
ax.axvline(datetime(2019,3,29), color=c_shading, alpha=c_opacity)                         # Berlin - climate strike with Greta (friday)
ax.axvline(datetime(2019,5,24), color=c_shading, alpha=c_opacity)                         # 2nd Global Climate Strike (for EU elections)
ax.axvline(datetime(2019,6,21), color=c_shading, alpha=c_opacity)                         # Aachen: International Climate Strike
ax.axvspan(datetime(2019,9,20), datetime(2019,9,27), color=c_shading, alpha=c_opacity)    # Global Week of Climate Action
ax.axvline(datetime(2019,11,29), color=c_shading, alpha=c_opacity)                        # Fourth Global Climate Strike
plt.savefig(z_media_figures + z_prefix + 'genios_fff_per_1000_events_2019.pdf')



#plot both in one graph
fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_greta_ratio_ma3)
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio_ma3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))











########## plot School articles per 1,000 articles - 2019 ######################

fig, ax = plt.subplots()
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_school_ratio, alpha=0.6, color='darkgrey', label='unsmoothed')
ax.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_school_ratio_ma3, label='smoothed')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))
ax.legend()
ax.set(xlabel='Date', ylabel='Number of articles covering School Management,\n per 1,000 articles') #xlabel='months',
plt.savefig(z_media_figures + z_prefix + 'genios_school_per_1000_2019.pdf')






# plot school management and FFF

fig, ax1 = plt.subplots()
color_fav = 'tab:blue'
ax1.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_school_ratio_ma3,
         label='school management', color=color_fav)
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of articles covering School Management,\n per 1,000 articles', color=color_fav) #xlabel='months',
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax1.xaxis.set_minor_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('\n%Y'))

ax2 = ax1.twinx()
color_re = 'tab:orange'
ax2.plot(articles.loc['2018-11':].index.values, articles.loc['2018-11':].art_fff_ratio_ma3,
         label='fff strikes', color=color_re, alpha=0.45, linewidth=2.1)
ax2.set_ylabel('Number of articles covering FFF strikes,\n per 1,000 articles', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
ax2.grid(None)

# ask matplotlib for the plotted objects and their labels
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.savefig(z_media_figures + z_prefix + 'genios_school_fff_strikes_per_1000_2019.pdf')




###############################################################################
#           evolution of greta in SZ & FAZ
###############################################################################
temp = articles[['art_greta_faz', 'art_greta_sz', 'art_greta']].loc['2018-11':].resample('W').sum()

# w/o general trend in germany
fig, ax = plt.subplots()
ax.plot(temp.index.values, temp['art_greta_sz'], color='tab:blue', label='SZ')
ax.plot(temp.index.values, temp['art_greta_faz'], color='tab:orange', label='FAZ')
ax.legend(loc='upper left')
ax.set_yticks(np.arange(0, 17, 4))
ax.set_xlabel('Date')
ax.set_ylabel('Number of articles')
plt.savefig(z_media_figures + z_prefix + 'genios_greta_SZ_FAZ.pdf')


# mit generellen trend
fig, ax1 = plt.subplots()

ax1.plot(temp.index.values, temp['art_greta_sz'], color='tab:blue', label='SZ')
ax1.plot(temp.index.values, temp['art_greta_faz'], color='tab:orange', label='FAZ')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of articles,\n SZ and FAZ')
ax1.set_yticks(np.arange(0, 17, 4))

ax2 = ax1.twinx()
color_re = 'tab:green'
ax2.plot(temp.index.values, temp['art_greta'], color=color_re, label='all newspapers', alpha=0.4, linewidth=4)
ax2.set_ylabel('Number of articles,\n all German newspapers', color=color_re)
ax2.tick_params(axis='y', labelcolor=color_re)
ax2.grid(None)
ax2.set_yticks(np.arange(0, 2001, 500))


lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

fig.tight_layout() # otherwise right label is clipped
plt.savefig(z_media_figures + z_prefix + 'genios_greta_SZ_FAZ_all_newspapers.pdf')
