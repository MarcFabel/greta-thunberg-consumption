# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:48:00 2020

@author: Marc Fabel

Description:
    The program prepares the Sachsen 2019 election data on the AGS level

Inputs:
    -  Sachsen_LT_Gemeindeebene.xlsx                     [input]

Outputs:
    - election_thueringen2019_ags5_prepared.csv              [intermediate]

"""

# packages
import pandas as pd



# paths (WORK LOCAL & SERVER)

z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_sachsen_2019/'
z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'





###############################################################################
#           Prepare Election Data
###############################################################################
z_list_result_parties = list(range(18,93+1))[1::4]                             # only landesstimme in percent
z_list_select_columns = sorted([3,4,6,9,14,15] + z_list_result_parties)        # regional identifiers + parties

elec = pd.read_excel(z_election_input + 'Sachsen_LT_Gemeindeebene.xlsx',
                     sheet_name='LW19_endgErgebnisse_GE&TG')


# keep relevant columns
elec.columns = elec.columns.str.lower()
elec.columns = elec.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     elec.columns = elec.columns.str.replace(umlaut, replacement)

elec = elec[[
     'ags', 'ortname',
       'wahlberechtigte',  'gueltige_2',

       
       'cdu_2', 'die_linke_2', 'spd_2', 'afd_2',
       'gruene_2', 'npd_2', 'fdp_2', 'freie_waehler_2',
       'tierschutzpartei_2', 'piraten_2', 'die_partei_2',
       'bueso_2', 'adpm_2', 'blaue_#teampetry_2', 'kpd_2',
       'oedp_2', 'die_humanisten_2', 'pdv_2',
       'gesundheitsforschung_2']]

# adjust column names
elec.columns = elec.columns.str.replace('_2','')


elec['ags5'] = elec['ags'].astype(str).str[:5]



# aggregate to municipality level
elec = elec.groupby(['ags5']).sum()


# generate others column
z_list_others = elec.columns.drop(['ags', 'wahlberechtigte', 'gueltige', 'cdu', 'die_linke', 'spd', 'afd',
       'gruene', 'fdp']).to_list()
elec['others'] = elec[z_list_others].sum(axis=1)
elec.drop(z_list_others, axis=1, inplace=True)


# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'fdp', 'others']
for club in z_list_parties:
	     elec[club] = (elec[club]/elec['gueltige'])*100



# harmonize variables
elec['voter_turnout'] = (elec['gueltige']/elec['wahlberechtigte']*100)         

elec.rename(columns={'cdu':'union',
                    'die_linke':'the_left',
                    'gruene':'the_greens'}, inplace=True)
elec.drop(['ags', 'wahlberechtigte', 'gueltige'], axis=1, inplace=True)



elec = elec[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']]         
         
        


# write-out
elec.to_csv(z_election_output + 'election_sachsen2019_ag5s_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')