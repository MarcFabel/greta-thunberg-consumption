#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 11:56:07 2021

@author: marcfabel

Description:
    The program prepares the election data on the county level for placebo tests
    It contains elections for: 
        - Bundestag
        - eu + federal states (main analysis) with changes from previous years

Inputs:
    - elections_bundestag_YYYY_ags5.xlsx               [source]  
    - elections_eu_YYYY_ags5                           [source]
    - elections_brandenburg_YYYY_ags5.xlsx             [source]
    - elections_sachsen_YYYY_ags5.xlsx                 [source]
    - elections_thüringen_YYYY_ags5.xlsx               [source]

Outputs:
    - placebo_elections_ags5_prepared.csv             [intermediate]
    
Comments:
    - only on AGS5 level


"""

# packages
import pandas as pd



# paths (HOME)
z_election_input =  '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/'
z_election_output =   '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'


# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/ew19_wbz/'




###############################################################################
#           Bundestagswahl
###############################################################################


#  2013 #######################################################################
elec_13 = pd.read_excel(z_election_input + 'bundestagswahlen/elections_bundestag_2013_ags5.xlsx', skiprows=4)

elec_13.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_13', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_13', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
elec_13 = elec_13[['ags5', 'ags_name',  'nr_eligibles', 'turnout_13', 'valid_votes', 'greens_13']]

# replace Hamburg and Berlin 
elec_13['ags5'].replace({'02':'02000', '11':'11000'}, inplace=True)

# keep only ags5 levels
elec_13=elec_13[elec_13.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_13', 'valid_votes', 'greens_13']
elec_13[z_num_cols] = elec_13[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
elec_13 = elec_13.dropna()

# generate share of vote
elec_13['greens_13'] = (elec_13['greens_13']/ elec_13['valid_votes'])*100

elec_13 = elec_13[['ags5', 'ags_name', 'turnout_13', 'greens_13']]






#  2017 #######################################################################
elec_17 = pd.read_excel(z_election_input + 'bundestagswahlen/elections_bundestag_2017_ags5.xlsx', skiprows=4)

elec_17.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_17', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_17', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
elec_17 = elec_17[['ags5', 'ags_name',  'nr_eligibles', 'turnout_17', 'valid_votes', 'greens_17']]

# replace Hamburg and Berlin 
elec_17['ags5'].replace({'02':'02000', '11':'11000'}, inplace=True)

# keep only ags5 levels
elec_17=elec_17[elec_17.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_17', 'valid_votes', 'greens_17']
elec_17[z_num_cols] = elec_17[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
elec_17 = elec_17.dropna()

# generate share of vote
elec_17['greens_17'] = (elec_17['greens_17']/ elec_17['valid_votes'])*100

elec_17 = elec_17[['ags5', 'turnout_17', 'greens_17']]



# combine dfs and generate first differences
elec_final = elec_13.merge(elec_17, on='ags5', how='inner')
elec_final['fd_greens'] = elec_final['greens_17'] - elec_final['greens_13']
elec_final['fd_turnout'] = elec_final['turnout_17'] - elec_final['turnout_13']
elec_final = elec_final[['ags5', 'fd_greens', 'fd_turnout']]
elec_final['election'] = 'bundestag (2017-2013)'





###############################################################################
#           EU election
###############################################################################


#  2009 #######################################################################
eu_09 = pd.read_excel(z_election_input + 'elections_2009/elections_eu_2009_ags5.xlsx', skiprows=4)

eu_09.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_09', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_09', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
eu_09 = eu_09[['ags5', 'ags_name',  'nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']]

# replace Hamburg and Berlin 
eu_09['ags5'].replace({'02':'02000', '11':'11000'}, inplace=True)

# keep only ags5 levels
eu_09=eu_09[eu_09.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']
eu_09[z_num_cols] = eu_09[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
eu_09 = eu_09.dropna()

# generate share of vote
eu_09['greens_09'] = (eu_09['greens_09']/ eu_09['valid_votes'])*100

eu_09 = eu_09[['ags5', 'ags_name', 'turnout_09', 'greens_09']]




#  2014 #######################################################################
eu_14 = pd.read_excel(z_election_input + 'elections_2014/elections_eu_2014_ags5.xlsx', skiprows=4)

eu_14.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_14', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_14', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
eu_14 = eu_14[['ags5', 'ags_name',  'nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']]

# replace Hamburg and Berlin 
eu_14['ags5'].replace({'02':'02000', '11':'11000'}, inplace=True)

# keep only ags5 levels
eu_14=eu_14[eu_14.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']
eu_14[z_num_cols] = eu_14[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
eu_14 = eu_14.dropna()

# generate share of vote
eu_14['greens_14'] = (eu_14['greens_14']/ eu_14['valid_votes'])*100

eu_14 = eu_14[['ags5', 'turnout_14', 'greens_14']]



# combine dfs, generate first differences, add to final df
eu = eu_09.merge(eu_14, on='ags5', how='inner')
eu['fd_greens'] = eu['greens_14'] - eu['greens_09']
eu['fd_turnout'] = eu['turnout_14'] - eu['turnout_09']
eu = eu[['ags5', 'fd_greens', 'fd_turnout']]
eu['election'] = 'eu (2014-2009)'





###############################################################################
#           Brandenburg
###############################################################################


#  2009 #######################################################################
bb_09 = pd.read_excel(z_election_input + 'elections_2009/elections_brandenburg_2009_ags5.xlsx', skiprows=4)

bb_09.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_09', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_09', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
bb_09 = bb_09[['ags5', 'ags_name',  'nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']]

# keep only ags5 levels
bb_09=bb_09[bb_09.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']
bb_09[z_num_cols] = bb_09[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
bb_09 = bb_09.dropna()

# generate share of vote
bb_09['greens_09'] = (bb_09['greens_09']/ bb_09['valid_votes'])*100

bb_09 = bb_09[['ags5', 'ags_name', 'turnout_09', 'greens_09']]



#  2014 #######################################################################
bb_14 = pd.read_excel(z_election_input + 'elections_2014/elections_brandenburg_2014_ags5.xlsx', skiprows=4)

bb_14.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_14', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_14', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
bb_14 = bb_14[['ags5', 'ags_name',  'nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']]

# keep only ags5 levels
bb_14=bb_14[bb_14.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']
bb_14[z_num_cols] = bb_14[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
bb_14 = bb_14.dropna()

# generate share of vote
bb_14['greens_14'] = (bb_14['greens_14']/ bb_14['valid_votes'])*100

bb_14 = bb_14[['ags5', 'turnout_14', 'greens_14']]




# combine dfs, generate first differences, add to final df
bb = bb_09.merge(bb_14, on='ags5', how='inner')
bb['fd_greens'] = bb['greens_14'] - bb['greens_09']
bb['fd_turnout'] = bb['turnout_14'] - bb['turnout_09']
bb = bb[['ags5', 'fd_greens', 'fd_turnout']]
bb['election'] = 'brandenburg (2014-2009)'





###############################################################################
#          Saxony
###############################################################################


#  2009 #######################################################################
sa_09 = pd.read_excel(z_election_input + 'elections_2009/elections_sachsen_2009_ags5.xlsx', skiprows=4)

sa_09.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_09', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_09', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
sa_09 = sa_09[['ags5', 'ags_name',  'nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']]

# keep only ags5 levels
sa_09=sa_09[sa_09.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']
sa_09[z_num_cols] = sa_09[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
sa_09 = sa_09.dropna()

# generate share of vote
sa_09['greens_09'] = (sa_09['greens_09']/ sa_09['valid_votes'])*100

sa_09 = sa_09[['ags5', 'ags_name', 'turnout_09', 'greens_09']]



#  2014 #######################################################################
sa_14 = pd.read_excel(z_election_input + 'elections_2014/elections_sachsen_2014_ags5.xlsx', skiprows=4)

sa_14.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_14', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_14', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
sa_14 = sa_14[['ags5', 'ags_name',  'nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']]

# keep only ags5 levels
sa_14=sa_14[sa_14.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']
sa_14[z_num_cols] = sa_14[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
sa_14 = sa_14.dropna()

# generate share of vote
sa_14['greens_14'] = (sa_14['greens_14']/ sa_14['valid_votes'])*100

sa_14 = sa_14[['ags5', 'turnout_14', 'greens_14']]




# combine dfs, generate first differences, add to final df
sa = sa_09.merge(sa_14, on='ags5', how='inner')
sa['fd_greens'] = sa['greens_14'] - sa['greens_09']
sa['fd_turnout'] = sa['turnout_14'] - sa['turnout_09']
sa = sa[['ags5', 'fd_greens', 'fd_turnout']]
sa['election'] = 'saxony (2014-2009)'




###############################################################################
#          Thuringia
###############################################################################


#  2009 #######################################################################
th_09 = pd.read_excel(z_election_input + 'elections_2009/elections_thüringen_2009_ags5.xlsx', skiprows=4)

th_09.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_09', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_09', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
th_09 = th_09[['ags5', 'ags_name',  'nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']]

# keep only ags5 levels
th_09=th_09[th_09.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_09', 'valid_votes', 'greens_09']
th_09[z_num_cols] = th_09[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
th_09 = th_09.dropna()

# generate share of vote
th_09['greens_09'] = (th_09['greens_09']/ th_09['valid_votes'])*100

th_09 = th_09[['ags5', 'ags_name', 'turnout_09', 'greens_09']]



#  2014 #######################################################################
th_14 = pd.read_excel(z_election_input + 'elections_2014/elections_thüringen_2014_ags5.xlsx', skiprows=4)

th_14.columns = ['ags5', 'ags_name', 'nr_eligibles', 'turnout_14', 'valid_votes',
                    'cdu_csu', 'spd', 'greens_14', 'fdp', 'linke', 'afd', 'others']

# select relevant columns
th_14 = th_14[['ags5', 'ags_name',  'nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']]

# keep only ags5 levels
th_14=th_14[th_14.ags5.apply(lambda x: len(str(x))==5)]

# encode variables
z_num_cols = ['nr_eligibles', 'turnout_14', 'valid_votes', 'greens_14']
th_14[z_num_cols] = th_14[z_num_cols].apply(pd.to_numeric, errors='coerce')

# drop missing columns
th_14 = th_14.dropna()

# generate share of vote
th_14['greens_14'] = (th_14['greens_14']/ th_14['valid_votes'])*100

th_14 = th_14[['ags5', 'turnout_14', 'greens_14']]




# combine dfs, generate first differences, add to final df
th = th_09.merge(th_14, on='ags5', how='inner')
th['fd_greens'] = th['greens_14'] - th['greens_09']
th['fd_turnout'] = th['turnout_14'] - th['turnout_09']
th = th[['ags5', 'fd_greens', 'fd_turnout']]
th['election'] = 'thuringia (2014-2009)'




###############################################################################
#          Append all Data Frames
###############################################################################

elec_final = elec_final.append(eu, ignore_index=True)
elec_final = elec_final.append(bb, ignore_index=True)
elec_final = elec_final.append(sa, ignore_index=True)
elec_final = elec_final.append(th, ignore_index=True)


# Read out
elec_final.to_csv(z_election_output + 'placebo_elections_ags5_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.3f')
