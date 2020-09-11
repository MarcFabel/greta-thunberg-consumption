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

Comment:
     Two municipalitiy names were adjusted in the source data, such that there
     are no doublings. The affected regions are: Golzow and Mittelmark

"""

# packages
import pandas as pd



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



# results from the regions    #################################################


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




# match with ags information    ###############################################

# match with ags information
results.rename(columns={'region':'gemeinde'}, inplace=True)
df_final = results.merge(municipality_ags_keys[['gemeinde', 'ags']], on=['gemeinde'], how='left', indicator=False)


df_final.drop('gemeinde', axis=1, inplace=True)



# write-out
df_final.to_csv(z_election_output + 'election_brandenburg2019_ags_prepared.csv', sep=';', encoding='UTF-8', index=False, float_format='%.1f')