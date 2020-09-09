# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:34:26 2020

@author: Marc Fabel

Description:
    The program prepares the EU 2019 election data on the municipality level

Inputs:
    -  ew19_wbz_ergebnisse.xlsx                     [input]   

Outputs:
    - election_eu2019_municipality_prepared.csv     [intermediate]

"""

# packages
import pandas as pd



# paths (HOME)
z_election_input =  '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/ew19_wbz/'
z_election_output = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'


# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/ew19_wbz/'



###############################################################################
#           Prepare Election Data
###############################################################################


elec = pd.read_excel(z_election_input + 'ew19_wbz_ergebnisse.xlsx', skiprows=4)


# change column names: non-capital & no spaces
elec.columns = elec.columns.str.lower()
elec.columns = elec.columns.str.replace(' ','_')


# select relevant columns
elec = elec[[
       'land', 'regierungsbezirk', 'kreis', 'verbandsgemeinde', 'gemeinde',
       'kennziffer_briefwahlzugehörigkeit', 'wahlbezirk', 'bezirksart',
       'wahlberechtigte_(a)', 'ungültig', 'gültig', 'cdu', 'spd', 'grüne',
       'die_linke', 'afd', 'csu', 'fdp', 'freie_wähler', 'piraten',
       'tierschutzpartei', 'npd', 'familie', 'ödp', 'die_partei',
       'volksabstimmung', 'bp', 'dkp', 'mlpd', 'sgp', 'tierschutz_hier!',
       'tierschutzallianz', 'bündnis_c', 'big', 'bge', 'die_direkte!',
       'diem25', 'iii._weg', 'die_grauen', 'die_rechte', 'die_violetten',
       'liebe', 'die_frauen', 'graue_panther', 'lkr', 'menschliche_welt', 'nl',
       'ökolinx', 'die_humanisten', 'partei_für_die_tiere',
       'gesundheitsforschung', 'volt', 'ungekürzte_wahlbezirksbezeichnung']]


# make string vars with correct length (bula, bezirk, kreis) & generate ags
z_region_identifiers = ['land', 'regierungsbezirk', 'kreis', 'verbandsgemeinde', 'gemeinde',
       'kennziffer_briefwahlzugehörigkeit', 'wahlbezirk', 'bezirksart']
elec[z_region_identifiers] = elec[z_region_identifiers].astype(str)
elec['ags'] = elec['land'].str.zfill(2) + elec['regierungsbezirk'] + elec['kreis'].str.zfill(2) + elec['gemeinde'].str.zfill(3)
elec.drop(['land', 'regierungsbezirk', 'kreis', 'gemeinde'], axis=1, inplace=True)



# aggregate to municipality level
elec = elec.groupby(['ags']).sum()


# generate share of vote for each party: 
z_list_parties = elec.columns.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig']).tolist()
for party in z_list_parties:
    elec[party] = (elec[party] / elec['gültig'])*100


# Read out
elec.to_csv(z_election_output + 'election_eu2019_municipality_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
