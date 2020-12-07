# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 11:09:42 2020

@author: Marc Fabel

Description:
    The program prepares the Thueringen 2019 election data on the municipality level

Inputs:
    -  Thueringen_LT_Gemeindeebene.xlsx                     [input]

Outputs:
    - election_thueringen2019_ags_prepared.csv              [intermediate]

"""

# packages
import pandas as pd



# paths (WORK LOCAL)

z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_thueringen_2019/'
z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/landtag_thueringen_2019/'



###############################################################################
#           Prepare Election Data
###############################################################################
z_list_result_parties = list(range(18,93+1))[1::4]                             # only landesstimme in percent
z_list_select_columns = sorted([3,4,6,9,14,15] + z_list_result_parties)        # regional identifiers + parties

elec = pd.read_excel(z_election_input + 'Thueringen_LT_Gemeindeebene.xlsx', skiprows=7,
                     usecols=z_list_select_columns, header=None)


# generate column names
party_names = pd.read_excel(z_election_input + 'Thueringen_LT_Gemeindeebene.xlsx', skiprows=5,
                     usecols=list(range(18,93+1))[0::4]     , nrows=1, header=None)
party_names = party_names.apply(lambda x: x.str.lower())
party_names = party_names.apply(lambda x: x.str.replace(' ','_'))
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     party_names = party_names.apply(lambda x: x.str.replace(umlaut, replacement))

party_names = party_names.values.tolist()[0]
elec.columns = ['kreis','gemeinde','name','wahlberechtigte', 'ungueltig', 'gueltig'] + party_names


# generate ags
elec = elec.loc[(elec.kreis !=0)] # use onlz rows with kreis-information
elec['ags'] = '160' + elec.kreis.astype(str) + elec.gemeinde.astype(str).str.zfill(3)
elec.drop(['kreis','gemeinde'], axis=1, inplace=True)


# encode other colums and set NaNs to zero
for party in ['wahlberechtigte', 'ungueltig'] + party_names:
     elec[party] = pd.to_numeric(elec[party], errors='coerce')
elec = elec.fillna(0)
elec = elec.loc[elec.wahlberechtigte != 0]



# aggregate to municipality level
elec = elec.groupby(['ags']).sum()


# write-out
elec.to_csv(z_election_output + 'election_thueringen2019_ags_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.1f')