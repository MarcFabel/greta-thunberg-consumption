# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:34:26 2020

@author: Marc Fabel

Description:
    The program prepares the EU 2019 election data on the municipality level

Inputs:
    -  ew14_wbz_ergebnisse.xlsx                     [input]  
    -  ew19_wbz_ergebnisse.xlsx                     [input]   

Outputs:
    - election_eu2019_ags5_prepared.csv             [intermediate]
    - election_eu2019_ags8_prepared.csv             [intermediate]
    - election_eu2014_ags5_prepared.csv             [intermediate]
    - election_eu20194_ags8_prepared.csv            [intermediate]    
    
Updates:
    14.01.2021 preparation on ags5 & 8, before only 8 level - harmonize variable names
    24.01.2021 adjust ags8 preparation to ags5, which was more advanced
    24.01.2021 add year 2014
    08.02.2021 add fd_voter_turnout

"""

# packages
import pandas as pd



# paths (HOME)
z_election_input19 =  '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/ew19_wbz/'
z_election_input14 =  '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/ew14_wbz/'
z_election_output = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'


# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/ew19_wbz/'




###############################################################################
#           2014
###############################################################################


elec = pd.read_csv(z_election_input14 + 'EW14_Wbz_Ergebnisse.csv', skiprows=4, sep='\t',encoding='UTF-16 LE')


# change column names: non-capital & no spaces
elec.columns = elec.columns.str.lower()
elec.columns = elec.columns.str.replace(' ','_')


# select relevant columns
elec = elec[[
       'land', 'regierungsbezirk', 'kreis', 'verbandsgemeinde', 'gemeinde',
       'kennziffer_briefwahlzugehörigkeit', 'wahlbezirk', 'bezirksart',
       'wahlberechtigte_(a)', 'ungültig', 'gültig', 'cdu', 'spd', 'grüne',
       'die_linke', 'afd', 'csu', 'fdp']]


# make string vars with correct length (bula, bezirk, kreis) 
z_region_identifiers = ['land', 'regierungsbezirk', 'kreis', 'verbandsgemeinde', 'gemeinde',
       'kennziffer_briefwahlzugehörigkeit', 'wahlbezirk', 'bezirksart']
elec[z_region_identifiers] = elec[z_region_identifiers].astype(str)


# Berlin districts should be labeled as one ags
elec.loc[elec['land'] == '11', 'regierungsbezirk'] = '0'
elec.loc[elec['land'] == '11', 'kreis'] = '00'

# generate ags
elec['ags8'] = elec['land'].str.zfill(2) + elec['regierungsbezirk'] + elec['kreis'].str.zfill(2) + elec['gemeinde'].str.zfill(3)
elec['ags5'] = elec['land'].str.zfill(2) + elec['regierungsbezirk'] + elec['kreis'].str.zfill(2)
elec.drop(['land', 'regierungsbezirk', 'kreis', 'gemeinde'], axis=1, inplace=True)




# aggregate to municipality level & district level
elec_ags5 = elec.groupby(['ags5']).sum()
elec_ags8 = elec.groupby(['ags8']).sum()



# generate share of vote for each party: 
z_list_parties = elec_ags5.columns.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig']).tolist()
for party in z_list_parties:
    elec_ags5[party] = (elec_ags5[party] / elec_ags5['gültig'])*100
    elec_ags8[party] = (elec_ags8[party] / elec_ags8['gültig'])*100


# generate turnout
elec_ags5['voter_turnout'] = (elec_ags5['gültig'] / elec_ags5['wahlberechtigte_(a)']) *100 
elec_ags5.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig'], axis=1, inplace=True)
elec_ags8['voter_turnout'] = (elec_ags8['gültig'] / elec_ags8['wahlberechtigte_(a)']) *100 
elec_ags8.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig'], axis=1, inplace=True)


#harmonize variable names
elec_ags5['union'] = elec_ags5['cdu'] + elec_ags5['csu']
elec_ags5.drop(['cdu', 'csu'], axis=1, inplace=True)
elec_ags5.rename(columns={'grüne':'the_greens', 'die_linke':'the_left'},inplace=True)
elec_ags8['union'] = elec_ags8['cdu'] + elec_ags8['csu']
elec_ags8.drop(['cdu', 'csu'], axis=1, inplace=True)
elec_ags8.rename(columns={'grüne':'the_greens', 'die_linke':'the_left'},inplace=True)




# generate others (parties column)
z_list_other_parties = elec_ags5.columns.drop(['voter_turnout']).tolist()
elec_ags5['others'] = 100 - elec_ags5[z_list_other_parties].sum(axis=1)
elec_ags8['others'] = 100 - elec_ags8[z_list_other_parties].sum(axis=1)





    
#reorder columns
elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                       'the_left', 'afd', 'fdp', 'others' ]]
elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                       'the_left', 'afd', 'fdp', 'others' ]]
    

# Read out
elec_ags5.to_csv(z_election_output + 'election_eu2014_ags5_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
elec_ags8.to_csv(z_election_output + 'election_eu2014_ags8_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')


elec_ags8_2014 = elec_ags8.copy()
elec_ags8_2014 = elec_ags8_2014[['the_greens', 'voter_turnout']]
elec_ags8_2014.reset_index(inplace=True)
elec_ags8_2014.rename(columns={'the_greens':'the_greens_2014',
                               'voter_turnout':'voter_turnout_2014'}, inplace=True)





###############################################################################
#           2019
###############################################################################


elec = pd.read_excel(z_election_input19 + 'ew19_wbz_ergebnisse.xlsx', skiprows=4)


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


# make string vars with correct length (bula, bezirk, kreis) 
z_region_identifiers = ['land', 'regierungsbezirk', 'kreis', 'verbandsgemeinde', 'gemeinde',
       'kennziffer_briefwahlzugehörigkeit', 'wahlbezirk', 'bezirksart']
elec[z_region_identifiers] = elec[z_region_identifiers].astype(str)


# Berlin districts should be labeled as one ags
elec.loc[elec['land'] == '11', 'regierungsbezirk'] = '0'
elec.loc[elec['land'] == '11', 'kreis'] = '00'

# generate ags
elec['ags8'] = elec['land'].str.zfill(2) + elec['regierungsbezirk'] + elec['kreis'].str.zfill(2) + elec['gemeinde'].str.zfill(3)
elec['ags5'] = elec['land'].str.zfill(2) + elec['regierungsbezirk'] + elec['kreis'].str.zfill(2)
elec.drop(['land', 'regierungsbezirk', 'kreis', 'gemeinde'], axis=1, inplace=True)




# aggregate to municipality level & district level
elec_ags5 = elec.groupby(['ags5']).sum()
elec_ags8 = elec.groupby(['ags8']).sum()



# generate share of vote for each party: 
z_list_parties = elec_ags5.columns.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig']).tolist()
for party in z_list_parties:
    elec_ags5[party] = (elec_ags5[party] / elec_ags5['gültig'])*100
    elec_ags8[party] = (elec_ags8[party] / elec_ags8['gültig'])*100


# generate turnout
elec_ags5['voter_turnout'] = (elec_ags5['gültig'] / elec_ags5['wahlberechtigte_(a)']) *100 
elec_ags5.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig'], axis=1, inplace=True)
elec_ags8['voter_turnout'] = (elec_ags8['gültig'] / elec_ags8['wahlberechtigte_(a)']) *100 
elec_ags8.drop(['wahlberechtigte_(a)', 'ungültig', 'gültig'], axis=1, inplace=True)


# generate others (parties column)
z_list_other_parties = elec_ags5.columns.drop(['cdu', 'spd', 'grüne', 'die_linke', 'afd', 'csu', 'fdp', 'voter_turnout']).tolist()
elec_ags5['others'] = elec_ags5[z_list_other_parties].sum(axis=1)
elec_ags5.drop(z_list_other_parties, axis=1, inplace=True)
elec_ags8['others'] = elec_ags8[z_list_other_parties].sum(axis=1)
elec_ags8.drop(z_list_other_parties, axis=1, inplace=True)


#harmonize variable names
elec_ags5['union'] = elec_ags5['cdu'] + elec_ags5['csu']
elec_ags5.drop(['cdu', 'csu'], axis=1, inplace=True)
elec_ags5.rename(columns={'grüne':'the_greens', 'die_linke':'the_left'},inplace=True)
elec_ags8['union'] = elec_ags8['cdu'] + elec_ags8['csu']
elec_ags8.drop(['cdu', 'csu'], axis=1, inplace=True)
elec_ags8.rename(columns={'grüne':'the_greens', 'die_linke':'the_left'},inplace=True)

    
#reorder columns
elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                       'the_left', 'afd', 'fdp', 'others' ]]
elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                       'the_left', 'afd', 'fdp', 'others' ]]
    



# combine with 2014 data ######################################################
elec_ags8.reset_index(inplace=True)
elec_ags8 = elec_ags8.merge(elec_ags8_2014, on='ags8', how='inner')

elec_ags8['fd_the_greens'] = elec_ags8['the_greens'] - elec_ags8['the_greens_2014']
elec_ags8['fd_voter_turnout'] = elec_ags8['voter_turnout'] - elec_ags8['voter_turnout_2014']
elec_ags8.drop(['the_greens_2014', 'voter_turnout_2014'], axis=1, inplace=True)


# export active regions
active_regions = elec_ags8[['ags8']]



# Read out
elec_ags5.to_csv(z_election_output + 'election_eu2019_ags5_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
elec_ags8.to_csv(z_election_output + 'election_eu2019_ags8_prepared.csv', sep=';', encoding='UTF-8', index=False, float_format='%.3f')
