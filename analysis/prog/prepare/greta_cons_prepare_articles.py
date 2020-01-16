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
import matplotlib.pyplot as plt
import matplotlib.style as style
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

greta = pd.read_csv(z_media_input + 'genios_articles_greta_thunberg.csv', sep=',',
                    names=['date', 'art_greta'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)

fff = pd.read_csv(z_media_input + 'genios_articles_FFF.csv', sep=',',
                    names=['date', 'art_fff'], header=0, index_col='date',
                    parse_dates=True, dayfirst=True)


articles = pd.read_csv(z_media_input + 'genios_articles_all.csv', sep=',',
                       names=['date', 'art_all'], header=0,
                       index_col='date', parse_dates=True , dayfirst=True)

# merge dfs
articles = articles.merge(greta, on='date', how='inner')
articles = articles.merge(fff, on='date', how='inner')
articles['art_greta_ratio'] = articles['art_greta'] * 1000 / articles['art_all']
articles['art_fff_ratio'] = articles['art_fff'] * 1000 / articles['art_all']


#articles['dow'] 	= articles.index.apply(lambda x: x.strftime('%a'))



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

# plot greta articles for entire time horizon
articles.art_greta.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'greta_2018_2019.pdf')
plt.show()

#plot greta articles per 1,000 articles for entire time horizon
articles.art_greta_ratio.plot()
articles.art_greta_ratio_ma7.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'greta_per_1000_2018_2019.pdf')
plt.show()


# plot for the year 2019
articles.loc['2019'].art_greta.plot()
articles.loc['2019'].art_greta_ma3.plot()
fig = plt.gcf()
fig.savefig(z_media_figures + z_prefix + 'greta_2019.pdf')
plt.show()


# plot greta articles per 1,000 articles
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
