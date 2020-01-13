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
import pandas as pd
import matplotlib.pyplot as plt

# HOME directories
z_media_input =     '/Users/marcfabel/Dropbox/greta_consumption_Dx/analysis/data/intermediate/media/'


###############################################################################
#           Read in Data
###############################################################################

greta = pd.read_csv(z_media_input + 'genios_articles_greta.csv', sep=',',
                    names=['date', 'art_greta'], header=0, index_col='date',  
                    parse_dates=True)

articles = pd.read_csv(z_media_input + 'genios_articles_all.csv', sep=',', 
                       names=['date', 'art_all'], header=0,
                       index_col='date', parse_dates=True)

# merge dfs
articles = articles.merge(greta, on='date', how='inner')
articles['art_greta_ratio'] = articles['art_greta'] * 1000 / articles['art_all']


#articles['dow'] 	= articles.index.apply(lambda x: x.strftime('%a'))



# moving averages
articles['art_greta_ma3'] = articles.art_greta.rolling(window=3).mean()
articles['art_greta_ratio_ma3'] = articles.art_greta_ratio.rolling(window=3).mean()


# plot greta articles
articles.art_greta.plot()
articles.art_greta_ma3.plot()
plt.show()

# plot greta articles per 1,000 articles
articles.art_greta_ratio.plot()
articles.art_greta_ratio_ma3.plot()
plt.show()
