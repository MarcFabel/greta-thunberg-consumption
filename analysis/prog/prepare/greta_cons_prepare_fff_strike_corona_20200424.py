#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:09:31 2020

@author: marcfabel

Descritpion:
     This Program prepares the source data from the Online Corona Strikes to
     have the number of events per zip code


Inputs:
     - fff_strikes_2020_04_24_19-00_online_corona.json      [source]    source data

Outputs:
     - fff_strikes_corona_2020_04_24_prepared.csv          [intermed]   number of events per zip code
     
"""


import pandas as pd
import json



# HOME directory
z_fff_input     = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/fff_strikes/'
z_fff_output    = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/fff_strikes/'
z_fff_filename  = 'fff_strikes_2020_04_24_19-00_online_corona.json'



##########  Read-in Data ######################################################
with open(z_fff_input + z_fff_filename) as json_file:
    json_data = json.load(json_file)
     
entries = pd.DataFrame(json_data['entries'])
places = pd.DataFrame.from_dict(json_data['places'], orient='index')




##########  edit DataFrames  ##################################################
# keep only relevant columns
entries.drop(['img_status', 'img_dir', 'links', 'featured'], inplace=True,
             axis=1)

# replace name with anonymus when empty
entries['name'] = entries['name'].replace(r'^\s*$', 'anonymus', regex=True)


# prepare places for merging
places.reset_index(inplace=True, drop=False)
places.rename(columns={'index':'place'}, inplace=True)




##########  aggregate entry & merge with places ###############################
entries['count'] = 1
strikes = entries.groupby('place').sum()
strikes = strikes.merge(places, on='place')
strikes = strikes[['plz', 'stadt', 'count', 'lat', 'lon']]
strikes.sort_values(by='stadt', inplace=True)



##########  Read-out data #####################################################
strikes.to_csv(z_fff_output + 'fff_strikes_corona_2020_04_24_prepared.csv',
               sep=';', encoding='UTF-8', index=False)




