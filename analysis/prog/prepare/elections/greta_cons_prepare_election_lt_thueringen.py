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
    - election_thueringen_ags8_prepared.csv                 [intermediate]     contains also the fd of greens, only for time-invariant municipalities

Updates:
    08.02.2021 add fd_voter_tunout
"""

# packages
import pandas as pd



# paths (work HOME)
z_election_input =       '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/landtag_thueringen_2019/'
z_election_output =      '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'

# paths (WORK LOCAL)
#z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_thueringen_2019/'
#z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/landtag_thueringen_2019/'


###############################################################################
#           2014
###############################################################################
#z_list_result_parties = list(range(18,93+1))[1::4]                             # only landesstimme in percent
z_list_result_parties = list(range(18,93+1))[0::4]                             # only landesstimme in absolute numbers
z_list_select_columns = sorted([3,4,6,9,14,15] + z_list_result_parties)        # regional identifiers + parties

elec = pd.read_excel(z_election_input + 'Thueringen_LT_Gemeindeebene_2014.xlsx', skiprows=8,
                     usecols=z_list_select_columns, header=None)


# generate column names
party_names = pd.read_excel(z_election_input + 'Thueringen_LT_Gemeindeebene_2014.xlsx', skiprows=5,
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
elec['ags5'] = '160' + elec.kreis.astype(str)
elec.drop(['kreis','gemeinde'], axis=1, inplace=True)


# encode other colums and set NaNs to zero
for party in ['wahlberechtigte', 'ungueltig'] + party_names:
     elec[party] = pd.to_numeric(elec[party], errors='coerce')
elec = elec.fillna(0)
elec = elec.loc[elec.wahlberechtigte != 0]



# aggregate to municipality level
elec_ags8 = elec.groupby('ags').sum()
elec_ags5 = elec.groupby(['ags5']).sum()



# 
# generate others column
z_list_others = elec_ags5.columns.drop(['wahlberechtigte', 'gueltig', 'cdu', 'die_linke', 'spd', 'afd',
       'gruene', 'fdp']).to_list()
elec_ags5['others'] = elec_ags5[z_list_others].sum(axis=1)
elec_ags5.drop(z_list_others, axis=1, inplace=True)
elec_ags8['others'] = elec_ags8[z_list_others].sum(axis=1)
elec_ags8.drop(z_list_others, axis=1, inplace=True)


# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'fdp', 'others']
for club in z_list_parties:
    elec_ags5[club] = (elec_ags5[club]/elec_ags5['gueltig'])*100
    elec_ags8[club] = (elec_ags8[club]/elec_ags8['gueltig'])*100



# harmonize variables
elec_ags5['voter_turnout'] = (elec_ags5['gueltig']/elec_ags5['wahlberechtigte']*100)         

elec_ags5.rename(columns={'cdu':'union', 'die_linke':'the_left','gruene':'the_greens'}, inplace=True)
elec_ags5.drop(['wahlberechtigte', 'gueltig'], axis=1, inplace=True)

elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']]       



elec_ags8['voter_turnout'] = (elec_ags8['gueltig']/elec_ags8['wahlberechtigte']*100)         

elec_ags8.rename(columns={'cdu':'union', 'die_linke':'the_left','gruene':'the_greens'}, inplace=True)
elec_ags8.drop(['wahlberechtigte', 'gueltig'], axis=1, inplace=True)

elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']] 




elec_ags8_2014 = elec_ags8[['the_greens', 'voter_turnout']].copy()
elec_ags8_2014.reset_index(inplace=True)
elec_ags8_2014.rename({'the_greens':'the_greens_2014',
                       'voter_turnout':'voter_turnout_2014'}, axis=1, inplace=True)




###############################################################################
#           2019
###############################################################################
#z_list_result_parties = list(range(18,93+1))[1::4]                             # only landesstimme in percent
z_list_result_parties = list(range(18,93+1))[0::4]                             # only landesstimme in absolute numbers
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
elec['ags5'] = '160' + elec.kreis.astype(str)
elec.drop(['kreis','gemeinde'], axis=1, inplace=True)


# encode other colums and set NaNs to zero
for party in ['wahlberechtigte', 'ungueltig'] + party_names:
     elec[party] = pd.to_numeric(elec[party], errors='coerce')
elec = elec.fillna(0)
elec = elec.loc[elec.wahlberechtigte != 0]



# aggregate to municipality level
elec_ags8 = elec.groupby('ags').sum()
elec_ags5 = elec.groupby(['ags5']).sum()



# 
# generate others column
z_list_others = elec_ags5.columns.drop(['wahlberechtigte', 'gueltig', 'cdu', 'die_linke', 'spd', 'afd',
       'gruene', 'fdp']).to_list()
elec_ags5['others'] = elec_ags5[z_list_others].sum(axis=1)
elec_ags5.drop(z_list_others, axis=1, inplace=True)
elec_ags8['others'] = elec_ags8[z_list_others].sum(axis=1)
elec_ags8.drop(z_list_others, axis=1, inplace=True)


# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'fdp', 'others']
for club in z_list_parties:
    elec_ags5[club] = (elec_ags5[club]/elec_ags5['gueltig'])*100
    elec_ags8[club] = (elec_ags8[club]/elec_ags8['gueltig'])*100



# harmonize variables
elec_ags5['voter_turnout'] = (elec_ags5['gueltig']/elec_ags5['wahlberechtigte']*100)         

elec_ags5.rename(columns={'cdu':'union', 'die_linke':'the_left','gruene':'the_greens'}, inplace=True)
elec_ags5.drop(['wahlberechtigte', 'gueltig'], axis=1, inplace=True)

elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']]       



elec_ags8['voter_turnout'] = (elec_ags8['gueltig']/elec_ags8['wahlberechtigte']*100)         

elec_ags8.rename(columns={'cdu':'union', 'die_linke':'the_left','gruene':'the_greens'}, inplace=True)
elec_ags8.drop(['wahlberechtigte', 'gueltig'], axis=1, inplace=True)

elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']] 



# combine with 2014
elec_ags8.reset_index(inplace=True)
elec_ags8 = elec_ags8.merge(elec_ags8_2014, on='ags', indicator=False, how='inner')
elec_ags8['fd_the_greens'] = elec_ags8['the_greens'] - elec_ags8['the_greens_2014']
elec_ags8['fd_voter_turnout'] = elec_ags8['voter_turnout'] - elec_ags8['voter_turnout_2014']

elec_ags8.drop(['the_greens_2014', 'voter_turnout_2014'], axis=1, inplace=True)



# write-out
#elec_ags5.to_csv(z_election_output + 'election_thueringen2019_ags5_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
elec_ags8.to_csv(z_election_output + 'election_thueringen_ags8_prepared.csv', sep=';', encoding='UTF-8', index=False, float_format='%.3f')
