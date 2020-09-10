# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:33:46 2020

@author: Marc Fabel

Description:
    The program prepares the Brandenburg 2019 election data on the AGS level

Inputs:
    -  Brandenburg_LT_Gemeindeebene.xlsx                     [input]

Outputs:
    - election_brandenburg2019_ags_prepared.csv              [intermediate]

"""

# packages
import pandas as pd
import numpy as np



# paths (WORK LOCAL)

z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_brandenburg_2019/'
z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/landtag_brandenburg_2019/'



###############################################################################
#           Prepare Election Data
###############################################################################


# keys to connect municipalities w/ AGS code   ################################
municipality_ags_keys = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
                     sheet_name='LT-Wahlkreiseinteilung2019', skiprows=4, header=None)

municipality_ags_keys.columns = ['wahlkrs_nr', 'wahlkrs_name', 'kurzbezeichnung',
                                 'kreis', 'amt', 'gemeinde', 'ags']
municipality_ags_keys.drop('amt', axis=1, inplace=True)
municipality_ags_keys.dropna(subset=['gemeinde'], inplace=True)




## gemeinde names are not unqiue so I have to match on kreis & gemeinde
## forward fill of kreis information after clearing false entries
#z_false_identifiers = (municipality_ags_keys['wahlkrs_name'].isnull()) & (municipality_ags_keys['kreis'].notnull())
#municipality_ags_keys.loc[z_false_identifiers, 'kreis'] = np.nan
#
#municipality_ags_keys = municipality_ags_keys.fillna(method='ffill')
#
#
#
#temp = municipality_ags_keys['kreis'].unique()
#
#
#
#
## too complictaed match and correct three instances manually




# adjust municipality names to match the other

municipality_ags_keys.gemeinde = municipality_ags_keys.gemeinde.replace({
          'Ketzin/Havel'           : 'Ketzin',
          'Petershagen/Eggersdorf' : 'Petershagen/ Eggersdorf',
          'Glienicke/Nordbahn'     : 'Glienicke/ Nordbahn',
          'Lübbenau/Spreewald'     : 'Lübbenau/ Spreewald',
          'Vetschau/Spreewald'     : 'Vetschau/ Spreewald',
          'Fürstenwalde/Spree'     : 'Fürstenwalde/ Spree',
          'Wusterhausen/Dosse'     : 'Wusterhausen/ Dosse',
          'Rabenstein/Fläming'     : 'Rabenstein/ Fläming',
          'Teltow, Stadt'          : 'Teltow',
          'Nordwestuckermark'      : 'Nordwest-uckermark'
})



###############################################################################




# generate empty dataframe, which I can append sheet-information into:
results = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
                     sheet_name='3.2', skiprows=3, nrows=0)
# keep relevant columns & adjust names
results.columns = results.columns.str.lower()
results.columns = results.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     results.columns = results.columns.str.replace(umlaut, replacement)
results.rename(columns={'gruene/\nb_90':'gruene',
                     'bvb_/_freie_waehler':'freie_waehler',
                     'gueltige\nstimmen':'gueltig',
                     'wahlbe-\nrechtigte':'wahlberechtigte'}, inplace=True)





# Loop through kreise (sheets of exel file)
z_list_regions = list(range(1,28+1))[1::2]                                     # only zweitstimme of municipalities in kreise
for kreis in range(len(z_list_regions)):
	sheet_name_kreis = '3.' + str(z_list_regions[kreis])
	elec = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
	                     sheet_name=sheet_name_kreis, skiprows=3)


	# keep relevant columns & adjust names
	elec.columns = elec.columns.str.lower()
	elec.columns = elec.columns.str.replace(' ','_')
	for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
	     elec.columns = elec.columns.str.replace(umlaut, replacement)
	elec.rename(columns={'gruene/\nb_90':'gruene',
	                     'bvb_/_freie_waehler':'freie_waehler',
	                     'gueltige\nstimmen':'gueltig',
	                     'wahlbe-\nrechtigte':'wahlberechtigte'}, inplace=True)



	# drop irrelevant rows
	elec = elec.loc[elec.wahlberechtigte!='x']
	elec.dropna(subset=['region'], inplace=True)


	# define results as fractions
	z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'freie_waehler',
	                  'fdp', 'sonstige']
	for club in z_list_parties:
	     elec[club] = (elec[club]/elec['gueltig'])*100


	# delete kreis total
	elec = elec.iloc[:-1]

	# names of regions with no line break
	elec['region'] = elec['region'].str.replace('\n','')

	# add to results
	results = results.append(elec)



# match with ags information & manually correct for the three doublings which might be matched wrongly

temp = municipality_ags_keys[['gemeinde', 'ags']]

temp2 = results.merge(temp, left_on=['region'], right_on=['gemeinde'], how='outer', indicator=True)


# there is still a dimension mismatch by 417-413 =4, check doublings

# temp2._merge.value_counts()
#Out[121]:
#both          417
#right_only     50
#left_only       0
#Name: _merge, dtype: int64



# write-out
#elec.to_csv(z_election_output + 'election_sachsen2019_ags_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.1f')