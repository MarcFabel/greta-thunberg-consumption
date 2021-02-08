# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:33:46 2020

@author: Marc Fabel

Description:
    The program prepares the Brandenburg 2019 election data on the AGS level

Inputs:
    -  Brandenburg_LT_Gemeindeebene.xlsx                     [input]
    -  Brandenburg_LT_Gemeindeebene_2014.xlsx                [input]

Outputs:
    - election_brandenburg_ags8_prepared.csv              [intermediate]

Comment:
     Two municipalitiy names were adjusted in the source data, such that there
     are no doublings. The affected regions are: Golzow and Mittelmark

Updates: 
    add fd_voter_turnout
"""

# packages
import pandas as pd



# paths (HOME)
z_election_input =      '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/elections/landtag_brandenburg_2019/'
z_election_output =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/elections/'


# paths (WORK LOCAL)
#z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_brandenburg_2019/'
#z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/landtag_brandenburg_2019/'
#z_election_output =     'W:/EoCC/analysis/data/intermediate/elections/'



###############################################################################
#           2014
###############################################################################

# amtsfrei 
elec = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene_2014.xlsx',
	                     sheet_name='Zweitstimmen_Gemeinden amtsfrei', skiprows=8,
                         usecols=[0, 1, 8, 20], converters={0:str})
elec.columns = ['ags', 'ags_name', 'voter_turnout_2014', 'the_greens_2014']
elec.dropna(inplace=True)
#adjust ags
elec['ags'] = '120' + elec['ags']




elec2 = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene_2014.xlsx',
	                     sheet_name='Zweitstimmen_Gemeinden amtsang.', skiprows=8,
                         usecols=[0, 1, 8, 20], converters={0:str})
elec2.columns = ['gem_nr', 'ags_name', 'voter_turnout_2014', 'the_greens_2014']
elec2.dropna(inplace=True)
elec2['ags'] = '120' + elec2['gem_nr'].str[0:2] + elec2['gem_nr'].str[-3:]
elec2.drop('gem_nr', axis=1, inplace=True)
elec = elec.append(elec2)
elec.sort_values(by='ags', inplace=True)
elec.reset_index(drop=True, inplace=True)
elec_2014 = elec.copy()
elec_2014.ags = elec_2014.ags.astype(str)

# correct ags changes
elec_2014.replace({'12069304':'69304304',
                   '12069454':'69454454',
                   '12069604':'69604604',
                   '12069616':'69616616'}, inplace=True)
    
    









###############################################################################
#           2019
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
          'Nordwestuckermark'      : 'Nordwest-uckermark',
          'Brandenburg an der Havel, OT Görden':'Brandenburg an der Havel',
          'Cottbus, OT Branitz'    : 'Cottbus',
          'Potsdam, OT Potsdam Nord': 'Potsdam',
          'Frankfurt (Oder), OT Beresinchen' : 'Frankfurt (Oder)'})

# drop duplicates (stadtteile)
municipality_ags_keys = municipality_ags_keys.drop_duplicates(subset='ags')




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





	# delete kreis total
	elec = elec.iloc[:-1]

	# names of regions with no line break
	elec['region'] = elec['region'].str.replace('\n','')

	# add to results
	results = results.append(elec)




# read-in results from cities    ##############################################
    
# brandenburg
temp = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
	                     sheet_name='2.2', skiprows=3)
temp.columns = temp.columns.str.lower()
temp.columns = temp.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     temp.columns = temp.columns.str.replace(umlaut, replacement)
temp.rename(columns={'gruene/b_90':'gruene',
	                     'bvb_/_freie_waehler':'freie_waehler',
	                     'gueltige\nstimmen':'gueltig',
	                     'wahlbe-\nrechtigte':'wahlberechtigte',
                         'stadtteil/ortsteil':'region'}, inplace=True)  
temp['region'] = temp['region'].str.replace('\n','')

results = results.append(temp.iloc[16])

    
# cottbus
temp = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
	                     sheet_name='2.4', skiprows=3)
temp.columns = temp.columns.str.lower()
temp.columns = temp.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     temp.columns = temp.columns.str.replace(umlaut, replacement)
temp.rename(columns={'gruene/b_90':'gruene',
	                     'bvb_/_freie_waehler':'freie_waehler',
	                     'gueltige\nstimmen':'gueltig',
	                     'wahlbe-\nrechtigte':'wahlberechtigte',
                         'stadtteil/ortsteil':'region'}, inplace=True)  
temp['region'] = temp['region'].str.replace('\n','')
results = results.append(temp.iloc[27])


# frankfurt (oder)
temp = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
	                     sheet_name='2.6', skiprows=3)
temp.columns = temp.columns.str.lower()
temp.columns = temp.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     temp.columns = temp.columns.str.replace(umlaut, replacement)
temp.rename(columns={'gruene/b_90':'gruene',
	                     'bvb_/_freie_waehler':'freie_waehler',
	                     'gueltige\nstimmen':'gueltig',
	                     'wahlbe-\nrechtigte':'wahlberechtigte',
                         'stadtteil/ortsteil':'region'}, inplace=True)  
temp['region'] = temp['region'].str.replace('\n','')
results = results.append(temp.iloc[22])


    
# potsdam 
temp = pd.read_excel(z_election_input + 'Brandenburg_LT_Gemeindeebene.xlsx',
	                     sheet_name='2.8', skiprows=3)
temp.columns = temp.columns.str.lower()
temp.columns = temp.columns.str.replace(' ','_')
for umlaut, replacement in {'ä':'ae', 'ü':'ue', 'ö':'oe', 'ß':'ss'}.items():    # remove umlaute
     temp.columns = temp.columns.str.replace(umlaut, replacement)
temp.rename(columns={'gruene/b_90':'gruene',
	                     'bvb_/_freie_waehler':'freie_waehler',
	                     'gueltige\nstimmen':'gueltig',
	                     'wahlbe-\nrechtigte':'wahlberechtigte',
                         'stadtteil/ortsteil':'region'}, inplace=True)  
temp['region'] = temp['region'].str.replace('\n','')
results = results.append(temp.iloc[16])    
    



# match with ags information    ###############################################

# match with ags information
results.rename(columns={'region':'gemeinde'}, inplace=True)
df_final = results.merge(municipality_ags_keys[['gemeinde', 'ags']], on=['gemeinde'], how='left', indicator=False)
#df_final.drop('gemeinde', axis=1, inplace=True)
df_final['wahlberechtigte'] = pd.to_numeric(df_final['wahlberechtigte'])




# correct ags for Potsdam Mittelmark
#df_final['ags2'] = df_final['ags'].astype(str).str[:2]
#df_final['ags'].loc[df_final['ags2'] == '69'] = '12069XXX'





# define results as fractions
z_list_parties = ['spd', 'cdu', 'die_linke', 'afd', 'gruene', 'freie_waehler',
	                  'fdp', 'sonstige']
for club in z_list_parties:
	     df_final[club] = (df_final[club]/df_final['gueltig'])*100



# harmonize variabel names
df_final['voter_turnout'] = (df_final['gueltig']/df_final['wahlberechtigte']*100)         

df_final.rename(columns={'cdu':'union',
                              'die_linke':'the_left',
                              'gruene':'the_greens',
                              'freie_waehler':'free_voters',
                              'sonstige':'others'}, inplace=True)
df_final['others'] = df_final['free_voters'] + df_final['others']    
    
    
df_final.drop(['wahlberechtigte', 'gueltig', 'free_voters'], axis=1, inplace=True)




# combine with 2014 ###########################################################
df_final.ags = df_final.ags.astype(str)
df_final = df_final.merge(elec_2014, on='ags', how='left', indicator=False)


# cities 2014 manually https://www.wahlergebnisse.brandenburg.de/wahlen/LT2014/tabelleAmt.html
df_final.loc[df_final['ags']=='12051000', 'the_greens_2014'] = 5.8  # brandenburg
df_final.loc[df_final['ags']=='12052000', 'the_greens_2014'] = 4.5  # cottbus
df_final.loc[df_final['ags']=='12053000', 'the_greens_2014'] = 5.3  # frankfurt (oder)
df_final.loc[df_final['ags']=='12054000', 'the_greens_2014'] = 13.6 # potsdam

df_final.loc[df_final['ags']=='12051000', 'voter_turnout_2014'] = 38.2  # brandenburg
df_final.loc[df_final['ags']=='12052000', 'voter_turnout_2014'] = 49.5  # cottbus
df_final.loc[df_final['ags']=='12053000', 'voter_turnout_2014'] = 46.2  # frankfurt (oder)
df_final.loc[df_final['ags']=='12054000', 'voter_turnout_2014'] = 55.7  # potsdam

df_final['fd_the_greens'] = df_final['the_greens'] - df_final['the_greens_2014']
df_final['fd_voter_turnout'] = df_final['voter_turnout'] - df_final['voter_turnout_2014']


df_final = df_final[['ags', 'voter_turnout', 'union', 'spd', 'the_greens',
                               'the_left', 'afd', 'fdp', 'others', 'fd_the_greens', 'fd_voter_turnout']]
    

# write-out
df_final.to_csv(z_election_output + 'election_brandenburg_ags8_prepared.csv', sep=';', encoding='UTF-8', index=False, float_format='%.1f')