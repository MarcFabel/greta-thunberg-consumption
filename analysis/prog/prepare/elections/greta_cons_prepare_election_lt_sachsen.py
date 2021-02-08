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
    - election_sachsen_ags8_prepared.csv                     [intermediate]
    
Updates:
    08.02.2021 add fd_voter_turnout

"""

# packages
import pandas as pd



# paths (HOME)
z_election_input =       '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/landtag_sachsen_2019/'
z_election_output =      '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'


# paths (WORK LOCAL & SERVER)
#z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_sachsen_2019/'
#z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



###############################################################################
#           2014
###############################################################################


elec = pd.read_excel(z_election_input + 'Sachsen_LT_Gemeindeebene_2014.xlsx',
                     sheet_name='LW14_Ergebnisse_GE_TG')


# keep relevant columns
elec.columns = elec.columns.str.lower()
elec.columns = elec.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     elec.columns = elec.columns.str.replace(umlaut, replacement)

elec = elec[[
     'ags', 'ortname',
       'wahlberechtigte',  'gueltige_2',

       
       'cdu_2', 'die_linke_2', 'spd_2', 'fdp_2', 'gruene_2', 'npd_2',
       'tierschutzpartei_2', 'piraten_2', 'bueso_2', 'dsu_2', 'afd_2',
       'pro_deutschland_2', 'freie_waehler_2', 'die_partei_2']]

# adjust column names
elec.columns = elec.columns.str.replace('_2','')


elec['ags5'] = elec['ags'].astype(str).str[:5]



# aggregate to municipality level
elec_ags5 = elec.groupby(['ags5']).sum()
elec_ags5.drop('ags', axis=1, inplace=True)
elec_ags8 = elec.groupby(['ags']).sum()


# generate others column
z_list_others = elec_ags5.columns.drop(['wahlberechtigte', 'gueltige',
                                        'cdu', 'die_linke', 'spd', 'afd',
                                        'gruene', 'fdp']).to_list()
elec_ags5['others'] = elec_ags5[z_list_others].sum(axis=1)
elec_ags5.drop(z_list_others, axis=1, inplace=True)
elec_ags8['others'] = elec_ags8[z_list_others].sum(axis=1)
elec_ags8.drop(z_list_others, axis=1, inplace=True)


# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'fdp', 'others']
for club in z_list_parties:
    elec_ags5[club] = (elec_ags5[club]/elec_ags5['gueltige'])*100
    elec_ags8[club] = (elec_ags8[club]/elec_ags8['gueltige'])*100



# harmonize variables
elec_ags5['voter_turnout'] = (elec_ags5['gueltige']/elec_ags5['wahlberechtigte']*100)         

elec_ags5.rename(columns={'cdu':'union',
                    'die_linke':'the_left',
                    'gruene':'the_greens'}, inplace=True)
elec_ags5.drop(['wahlberechtigte', 'gueltige'], axis=1, inplace=True)

elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']]         
         


elec_ags8['voter_turnout'] = (elec_ags8['gueltige']/elec_ags8['wahlberechtigte']*100)         

elec_ags8.rename(columns={'cdu':'union',
                    'die_linke':'the_left',
                    'gruene':'the_greens'}, inplace=True)
elec_ags8.drop(['wahlberechtigte', 'gueltige'], axis=1, inplace=True)

elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']] 


elec_ags8_2014 = elec_ags8[['the_greens', 'voter_turnout']].copy()
elec_ags8_2014.reset_index(inplace=True)
elec_ags8_2014.rename({'the_greens':'the_greens_2014',
                       'voter_turnout':'voter_turnout_2014'}, axis=1, inplace=True)



###############################################################################
#           2019
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
elec_ags5 = elec.groupby(['ags5']).sum()
elec_ags5.drop('ags', axis=1, inplace=True)
elec_ags8 = elec.groupby(['ags']).sum()


# generate others column
z_list_others = elec_ags5.columns.drop(['wahlberechtigte', 'gueltige',
                                        'cdu', 'die_linke', 'spd', 'afd',
                                        'gruene', 'fdp']).to_list()
elec_ags5['others'] = elec_ags5[z_list_others].sum(axis=1)
elec_ags5.drop(z_list_others, axis=1, inplace=True)
elec_ags8['others'] = elec_ags8[z_list_others].sum(axis=1)
elec_ags8.drop(z_list_others, axis=1, inplace=True)


# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'fdp', 'others']
for club in z_list_parties:
    elec_ags5[club] = (elec_ags5[club]/elec_ags5['gueltige'])*100
    elec_ags8[club] = (elec_ags8[club]/elec_ags8['gueltige'])*100



# harmonize variables
elec_ags5['voter_turnout'] = (elec_ags5['gueltige']/elec_ags5['wahlberechtigte']*100)         

elec_ags5.rename(columns={'cdu':'union',
                    'die_linke':'the_left',
                    'gruene':'the_greens'}, inplace=True)
elec_ags5.drop(['wahlberechtigte', 'gueltige'], axis=1, inplace=True)

elec_ags5 = elec_ags5[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']]         
         


elec_ags8['voter_turnout'] = (elec_ags8['gueltige']/elec_ags8['wahlberechtigte']*100)         

elec_ags8.rename(columns={'cdu':'union',
                    'die_linke':'the_left',
                    'gruene':'the_greens'}, inplace=True)
elec_ags8.drop(['wahlberechtigte', 'gueltige'], axis=1, inplace=True)

elec_ags8 = elec_ags8[['voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others']] 
  








# combine with 2014
elec_ags8.reset_index(inplace=True)
elec_ags8 = elec_ags8.merge(elec_ags8_2014, on='ags', indicator=False, how='inner')
elec_ags8['fd_the_greens'] = elec_ags8['the_greens'] - elec_ags8['the_greens_2014']
elec_ags8['fd_voter_turnout'] = elec_ags8['voter_turnout'] - elec_ags8['voter_turnout_2014']
elec_ags8.drop(['the_greens_2014', 'voter_turnout_2014'], axis=1, inplace=True)


      


# write-out
#elec_ags5.to_csv(z_election_output + 'election_sachsen2019_ag5s_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
elec_ags8.to_csv(z_election_output + 'election_sachsen_ags8_prepared.csv', sep=';', encoding='UTF-8', index=False, float_format='%.3f')