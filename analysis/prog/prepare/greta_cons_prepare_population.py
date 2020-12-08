# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:46:43 2020


@author: marcfabel



Descritpion:
    prepares population data on ags5 and ags8 level



Inputs:
    population_agegroups_2019_ags8.xlsx     [source]
    


Outputs:
     population_ags5_prepared.csv'         [intermediate]
     population_ags8_prepared.csv'         [intermediate]

"""

# packages
import pandas as pd


# work directories (SERVER)
z_regional_source =             'W:/EoCC/analysis/data/source/population/'
z_regional_intermediate =       'W:/EoCC/analysis/data/intermediate/population/'
z_prefix =                      'greta_cons'










###############################################################################
#           12_POPULATION
###############################################################################





########## 124_CURRENT_POPULATION ##########
pop_raw = pd.read_excel(z_regional_source + 'population_agegroups_2019_ags8.xlsx',
                    skiprows=6, skipfooter=33 ) 

pop_raw.columns = ['ags', 'ags_name', 'pop_0_2_t', 'pop_3_5_t', 'pop_6_9_t', 'pop_10_14_t', 'pop_15_17_t', 'pop_18_19_t', 'pop_20_24_t',
		'pop_25_29_t', 'pop_30_34_t', 'pop_35_39_t', 'pop_40_44_t' , 'pop_45_49_t', 'pop_50_54_t', 'pop_55_59_t',
		'pop_60_64_t', 'pop_65_74_t', 'pop_74+_t', 'pop_t',

		'pop_0_2_m', 'pop_3_5_m', 'pop_6_9_m', 'pop_10_14_m', 'pop_15_17_m', 'pop_18_19_m', 'pop_20_24_m',
		'pop_25_29_m', 'pop_30_34_m', 'pop_35_39_m', 'pop_40_44_m' , 'pop_45_49_m', 'pop_50_54_m', 'pop_55_59_m',
		'pop_60_64_m', 'pop_65_74_m', 'pop_74+_m', 'pop_m',

		'pop_0_2_f', 'pop_3_5_f', 'pop_6_9_f', 'pop_10_14_f', 'pop_15_17_f', 'pop_18_19_f', 'pop_20_24_f',
		'pop_25_29_f', 'pop_30_34_f', 'pop_35_39_f', 'pop_40_44_f' , 'pop_45_49_f', 'pop_50_54_f', 'pop_55_59_f',
		'pop_60_64_f', 'pop_65_74_f', 'pop_74+_f', 'pop_f']

# keep only relevant columns
pop_raw = pop_raw[['ags', 'ags_name', 'pop_t', 'pop_0_2_t', 'pop_3_5_t', 'pop_6_9_t', 
                   'pop_10_14_t', 'pop_15_17_t', 'pop_18_19_t', 'pop_20_24_t',
                   'pop_25_29_t', 'pop_30_34_t', 'pop_35_39_t', 'pop_40_44_t',
                   'pop_45_49_t', 'pop_50_54_t', 'pop_55_59_t',	'pop_60_64_t', 
                   'pop_65_74_t', 'pop_74+_t']]


# prepare ags8 population
pop_ags8 = pop_raw.loc[pop_raw['ags'].str.len() == 8]
pop_ags8 = pop_ags8.loc[pop_ags8['pop_t'] != '-'] # keep only values with entries (the data set contains deprecated ags keys)
# replace '-' with zeros
z_pop_cols = pop_raw.columns.drop(['ags', 'ags_name', 'pop_t']).tolist()
pop_ags8[z_pop_cols] = pop_ags8[z_pop_cols].replace('-', '0')
pop_ags8['ags_name'] = pop_ags8['ags_name'].str.lstrip() # remove preceding space


# prepare ags5 population
pop_ags5 = pop_raw.loc[pop_raw['ags'].str.len() == 5]
pop_ags5 = pop_ags5.loc[pop_ags5['pop_t'] != '-'] 
pop_ags5['ags_name'] = pop_ags5['ags_name'].str.lstrip() # remove preceding space


# read out
pop_ags5.to_csv(z_regional_intermediate + 'population_ags5_prepared.csv', sep=';', encoding='UTF-16', index=False)
pop_ags8.to_csv(z_regional_intermediate + 'population_ags8_prepared.csv', sep=';', encoding='UTF-16', index=False)



