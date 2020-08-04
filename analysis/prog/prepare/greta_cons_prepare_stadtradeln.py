#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:33:05 2020


Description:
    This file scrapes (for year 2018) & appends the data from the stadtradeln
    website


Inputs:
    Cross-sections 2012-2017, 2019

Outputs:
    stadtradeln_prepared.csv.csv
"""


# packages
import requests
from bs4 import BeautifulSoup
import pandas as pd


# HOME directories
z_radl_source =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/stadtradeln/'
z_radl_output =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/stadtradeln/'

# work directories (LOCAL)
#z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/stadtradeln/'

###############################################################################
#       1) Scrape info from website
###############################################################################


link = 'https://www.stadtradeln.de/kommunen2018'
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')
regions = soup.find('tbody').find_all('tr')


result_final = [] # will be a list of lists
region_iterator = 0
while region_iterator < len(regions): # loop through regions
    list_entries = regions[region_iterator].find_all('td') # generate entry list per region
    j = 0 # j is entry iterator (iterates through columns)
    result_region = []
    while j < len(list_entries): # loop through columns (entries)
        if list_entries[j].get_text() != '': # condition on non-empty cells
            result_region.append(list_entries[j].get_text())
            #print(list_entries[j].get_text()+';')
        j = j+1
    region_iterator = region_iterator + 1
    #print(result_region)
    result_final.append(result_region)


###############################################################################
#       2) transform into DataFrame
###############################################################################


df_18 = pd.DataFrame(result_final)
df_18.columns = ['region_orig', 'bula', 'time', 'km', 'co2']
df_18['year'] = 2018


# drop non-German regions:
non_german_regions = df_18[df_18.bula == '-'].index
df_18.drop(non_german_regions, inplace=True)
assert(df_18.shape == (region_iterator-len(non_german_regions),6))

# bring region column in right format
df_18['region'] = df_18['region_orig'].str.slice(0,-19)
df_18.drop('region_orig', axis=1, inplace=True)


# encode variables (distance & co2)
df_18['km'] = pd.to_numeric(df_18.km.str.replace('.', '').str.replace(' km', ''))
df_18['co2'] = pd.to_numeric(df_18.co2.str.replace('.',''))


# start and end time of the event
df_18['start'] = pd.to_datetime(df_18.time.str.slice(0,6) + df_18.year.astype(str), format='%d.%m.%Y')
df_18['end'] = pd.to_datetime(df_18.time.str.slice(-10,), format='%d.%m.%Y')
df_18.drop('time', axis=1, inplace=True)                    





###############################################################################
#       3) Prepare other years
###############################################################################

# note that single file handling necessary as there are minor differences in 
# how the individual cross-sections are set up

# 2012
df_12 = pd.read_excel(z_radl_source + 'stadtradeln_2012.xlsx')
df_12.columns = ['region', 'time', 'km', 'co2']
df_12['year'] = 2012
df_12['km'] = pd.to_numeric(df_12.km.str.replace('.', '').str.replace(' km', ''))
df_12['co2'] = pd.to_numeric(df_12.co2.str.replace('.','').str.replace(' kg', ''))
df_12['start'] = pd.to_datetime(df_12.time.str.slice(0,10), format='%d.%m.%Y')
df_12['end'] = pd.to_datetime(df_12.time.str.slice(-10,), format='%d.%m.%Y')
df_12.drop('time', axis=1, inplace=True)


# 2013
df_13 = pd.read_excel(z_radl_source + 'stadtradeln_2013.xlsx')
df_13.columns = ['region', 'bula', 'time', 'km', 'co2']
df_13['year'] = 2013
df_13['km'] = pd.to_numeric(df_13.km.str.replace('.', '').str.replace(' km', ''))
df_13['co2'] = pd.to_numeric(df_13.co2.str.replace('.','').str.replace(' kg', ''))
df_13['start'] = pd.to_datetime(df_13.time.str.slice(0,10), format='%d.%m.%Y')
df_13['end'] = pd.to_datetime(df_13.time.str.slice(-10,), format='%d.%m.%Y')
df_13.drop('time', axis=1, inplace=True)


# 2014
df_14 = pd.read_excel(z_radl_source + 'stadtradeln_2014.xlsx')
df_14.columns = ['region', 'bula', 'time', 'km', 'co2']
df_14['year'] = 2014
df_14['km'] = pd.to_numeric(df_14.km.str.replace('.', '').str.replace(' km', ''))
df_14['co2'] = pd.to_numeric(df_14.co2.str.replace('.','').str.replace(' kg', ''))
df_14['start'] = pd.to_datetime(df_14.time.str.slice(0,10), format='%d.%m.%Y')
df_14['end'] = pd.to_datetime(df_14.time.str.slice(-10,), format='%d.%m.%Y')
df_14.drop('time', axis=1, inplace=True)


# 2015
df_15 = pd.read_excel(z_radl_source + 'stadtradeln_2015.xlsx')
df_15.columns = ['region', 'country', 'bula', 'time', 'km', 'co2', 'radar']
df_15.drop('country', axis=1, inplace=True)
df_15['year'] = 2015
df_15['km'] = pd.to_numeric(df_15.km.str.replace('.', '').str.replace(' km', ''))
df_15['co2'] = pd.to_numeric(df_15.co2.str.replace('.','').str.replace(' kg', ''))
df_15['start'] = pd.to_datetime(df_15.time.str.slice(0,6) + df_15.year.astype(str), format='%d.%m.%Y')
df_15['end'] = pd.to_datetime(df_15.time.str.slice(-10,), format='%d.%m.%Y')
df_15.drop('time', axis=1, inplace=True)


# 2016
df_16 = pd.read_excel(z_radl_source + 'stadtradeln_2016.xlsx')
df_16.columns = ['region', 'country', 'bula', 'time', 'km', 'co2', 'radar']
df_16.drop('country', axis=1, inplace=True)
df_16['year'] = 2016
df_16['km'] = pd.to_numeric(df_16.km.str.replace('.', '').str.replace(' km', ''))
df_16['co2'] = pd.to_numeric(df_16.co2.str.replace('.','').str.replace(' kg', ''))
df_16['start'] = pd.to_datetime(df_16.time.str.slice(0,6) + df_16.year.astype(str), format='%d.%m.%Y')
df_16['end'] = pd.to_datetime(df_16.time.str.slice(-10,), format='%d.%m.%Y')
df_16.drop('time', axis=1, inplace=True)


# 2017
df_17 = pd.read_excel(z_radl_source + 'stadtradeln_2017.xlsx')
df_17.columns = ['region', 'country', 'bula', 'time', 'km', 'co2', 'radar']
df_17 = df_17.loc[df_17.country == 'Germany'].copy()                           #drop non German regions
df_17.drop('country', axis=1, inplace=True)
df_17['year'] = 2017
df_17['start'] = pd.to_datetime(df_17.time.str.slice(0,6) + df_17.year.astype(str), format='%d.%m.%Y')
df_17['end'] = pd.to_datetime(df_17.time.str.slice(-10,), format='%d.%m.%Y')
df_17.drop('time', axis=1, inplace=True)


# 2019
df_19 = pd.read_excel(z_radl_source + 'stadtradeln_2019.xlsx')
df_19.columns = ['region', 'country', 'bula', 'time', 'km', 'co2', 'radar']
df_19 = df_19.loc[df_19.country == 'Deutschland'].copy() 
df_19.drop('country', axis=1, inplace=True)
df_19['year'] = 2019
df_19['km'] = pd.to_numeric(df_19.km.str.replace('.', '').str.replace(' km', ''))
df_19['start'] = pd.to_datetime(df_19.time.str.slice(0,6) + df_19.year.astype(str), format='%d.%m.%Y')
df_19['end'] = pd.to_datetime(df_19.time.str.slice(-10,), format='%d.%m.%Y')
df_19.drop('time', axis=1, inplace=True)



###############################################################################
#       4) Append all DataFrames and make them ready to be exported
###############################################################################


df_regions = df_12.copy()
df_regions = df_regions.append(df_13)
df_regions = df_regions.append(df_14)
df_regions = df_regions.append(df_15)
df_regions = df_regions.append(df_16)
df_regions = df_regions.append(df_17)
df_regions = df_regions.append(df_18)
df_regions = df_regions.append(df_19)


# reorder columns
df_regions = df_regions[['region', 'year', 'bula', 'start', 'end', 'km', 'co2', 'radar']]


# export
df_regions.to_csv(z_radl_output + 'stadtradeln_prepared.csv', sep=';', encoding='UTF-8', index=False)




###############################################################################
#       5) analysis
###############################################################################


import matplotlib.pyplot as plt
z_media_figures = '/Users/marcfabel/Desktop/'


df_regions['count'] = 1
temp = df_regions.groupby('year').sum()
temp['km_region'] = temp['km'] / temp['count']  /1000


# number of municipalities
fig, ax = plt.subplots()
ax.plot(temp.index.values, temp['count'])
ax.set(xlabel='year', ylabel='Number of participating municipalities')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig(z_media_figures + 'number_municipalities.jpg',bbox_inches = "tight")


# average number of kilometers
fig, ax = plt.subplots()
ax.plot(temp.index.values, temp['km_region'])
ax.set(xlabel='year', ylabel='Average Number of km,\n per region [in thousand]')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig(z_media_figures + 'number_km.jpg',bbox_inches = "tight")


# 

