# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:11:04 2020

@author: Fabel
"""


# packages
import pandas as pd
import time
start_time = time.time()


# paths
z_soccer_webscraping_source   = 'W:/EoCC/analysis/data/source/soccer/'
z_soccer_source               = 'C:/Users/fabel/Dropbox/soc_ext_Dx/analysis/data/source/soccer/'
z_maps_input_intermediate     = 'C:/Users/fabel/Dropbox/soc_ext_Dx/analysis/data/intermediate/maps/'
z_soccer_output               = 'W:/EoCC/analysis/data/intermediate/soccer/'







###############################################################################

matches = pd.read_csv(z_soccer_webscraping_source + 'bundesliga_2019_20.csv',
                 sep=';', encoding='ISO-8859-1')



# correct team names
matches.home_team = matches.home_team.replace({
        'Bayern' 			: 'Bayern München',
        'Bayern II' 		: 'Bayern München II',
        'VfB II' 			: 'Stuttgart II',
        'Union' 			: 'Union Berlin',
        'Wehen' 			: 'Wehen Wiesbaden',
        'HSV'           : 'Hamburger SV',
        'Stuttg. Kick.' : 'Stuttgarter Kickers',
        'TSV 1860'      : '1860 München'})

matches.away_team = matches.away_team.replace({
        'Bayern' 			: 'Bayern München',
        'Bayern II' 		: 'Bayern München II',
        'VfB II' 			: 'Stuttgart II',
        'Union' 			: 'Union Berlin',
        'Wehen' 			: 'Wehen Wiesbaden',
        'HSV'           : 'Hamburger SV',
        'Stuttg. Kick.' : 'Stuttgarter Kickers',
        'TSV 1860'      : '1860 München'})


########## drop some variables ##########

matches.reset_index(inplace=True, drop=True)
# VARIABLES THAT COULD BE REACTIVATED: chances (2x), corners (2x), sold_out




# vereinheitlichung von teamnamen
teams = matches.drop_duplicates(subset='home_team')
teams = teams['home_team'].copy()
teams.sort_values(inplace=True)
teams.reset_index(inplace=True, drop=True)
# 68 teams in the data set



########## Stadiums ##########
# correct some stadiums
matches.stadium = matches.stadium.replace({
    'Impuls-Arena, Augsburg'                            : 'WWK-Arena, Augsburg',
    'SGL-Arena, Augsburg'                               : 'WWK-Arena, Augsburg',
    'Scholz-Arena, Aalen'                               : 'Ostalb Arena, Aalen',
    'Sparkassen-Erzgebirgsstadion, Aue'                 : 'Erzgebirgsstadion, Aue',
    'SchÃ¼co-Arena, Bielefeld'                          : 'Schüco-Arena, Bielefeld',
    'Rewirpower-Stadion, Bochum'                        : 'Vonovia-Ruhrstadion, Bochum',
    'Stadion an der GellertstraÃe, Chemnitz'           : 'Stadion an der Gellertstraße, Chemnitz',
    'StÃ¤dtisches Stadion am BÃ¶llenfalltor, Darmstadt' : 'Merck-Stadion am Böllenfalltor, Darmstadt',
    'GlÃ¼cksgas-Stadion, Dresden'                       : 'Rudolf-Harbig-Stadion, Dresden',
    'Glücksgas-Stadion, Dresden'                        : 'Rudolf-Harbig-Stadion, Dresden',
    'DDV-Stadion, Dresden'                              : 'Rudolf-Harbig-Stadion, Dresden',
    'Stadion Dresden, Dresden'                          : 'Rudolf-Harbig-Stadion, Dresden',
    'Stadion an der Schwarzwaldstraße, Freiburg'        : 'Schwarzwald-Stadion, Freiburg',
    'Mage-Solar-Stadion, Freiburg'                      : 'Schwarzwald-Stadion, Freiburg',
    'Badenova-Stadion, Freiburg'                        : 'Schwarzwald-Stadion, Freiburg',
    'Stadion am Laubenweg, Fürth'                       : 'Sportpark Ronhof | Thomas Sommer, Fürth',
    'Trolli-Arena, Fürth'                               : 'Sportpark Ronhof | Thomas Sommer, Fürth',
    'Imtech-Arena, Hamburg'                             : 'Volksparkstadion, Hamburg',
    'Millerntor-Stadion, Hamburg-St. Pauli'             : 'Millerntor-Stadion, Hamburg-St.Pauli',
    'AWD-Arena, Hannover'                               : 'HDI Arena, Hannover',
    'SÃ¼dstadion, KÃ¶ln'                                : 'Südstadion, Köln',
    'Coface-Arena, Mainz'                               : 'Opel-Arena, Mainz',
    'Stadion an der GrÃ¼nwalder StraÃe, MÃ¼nchen'       : 'Stadion an der Grünwalder Straße, München',
    'PreuÃenstadion, MÃ¼nster'                          : 'Preußenstadion, Münster',
    'Easy-Credit-Stadion, Nürnberg'                     : 'Grundig-Stadion, Nürnberg',
    'Bieberer Berg, Offenbach'                          : 'Sparda-Bank-Hessen-Stadion, Offenbach',
    'Osnatel-Arena, OsnabrÃ¼ck'                         : 'Bremer Brücke, Osnabrück',
    'Osnatel-Arena, Osnabrück'                          : 'Bremer Brücke, Osnabrück',
    'Energieteam-Arena, Paderborn'                      : 'Benteler-Arena, Paderborn',
    'StÃ¤dtisches Jahnstadion, Regensburg'              : 'Städtisches Jahnstadion, Regensburg',
    'DKB-Arena, Rostock'                                : 'Ostseestadion, Rostock',
    'Ludwigsparkstadion, SaarbrÃ¼cken'                  : 'Ludwigsparkstadion, Saarbrücken',
    'Hardtwaldstadion, Sandhausen'                      : 'BWT-Stadion am Hardtwald, Sandhausen',
    'Rhein-Neckar-Arena, Sinsheim'                      : 'Wirsol Rhein-Neckar-Arena, Sinsheim',
    'Generali-Sportpark, Unterhaching'                  : 'Stadion am Sportpark, Unterhaching',
    'Alpenbauer Sportpark, Unterhaching'                : 'Stadion am Sportpark, Unterhaching',
    'Allianz-Arena, Mnchen'                             : 'Allianz-Arena, München',
    'Wohninvest Weserstadion, Bremen'                   : 'Weser-Stadion, Bremen',
    'Borussia-Park, Mnchengladbach'                     : 'Borussia-Park, Mönchengladbach',
    'Stadion An der Alten Frsterei, Berlin'             : 'Stadion An der Alten Försterei, Berlin',
    'Rhein-Energie-Stadion, Kln'                        : 'Rhein-Energie-Stadion, Köln',
    'PreZero-Arena, Sinsheim'                           : 'Wirsol Rhein-Neckar-Arena, Sinsheim',
    'Merkur Spiel-Arena, Dsseldorf'                     : 'Esprit-Arena, Düsseldorf'})


# drop duplicates
stadiums =  matches.drop_duplicates(subset=['stadium']) # , 'home_team'
stadiums = stadiums['stadium'].copy() #, 'home_team'
#stadiums = stadiums.str.split(pat=',', expand=True)
#stadiums.sort_values(1, inplace=True)
#stadiums = stadiums.rename(columns={0:'stadium', 1:'city'})
stadiums = stadiums.to_frame()
len_stadiums = len(stadiums)





# add Geographic components (intern Domink set up the data base)
stadiums_geo = pd.read_excel(z_soccer_source  + 'stadiums_coordinates_1011_1617.xlsx')
stadiums = stadiums.merge(stadiums_geo, on=['stadium'], how='outer', indicator=True)
stadiums.sort_values(['Ort'], inplace=True)
drop_rows = stadiums[stadiums['_merge'] != 'both'].index
stadiums.drop(drop_rows, inplace=True)
stadiums.drop('_merge', inplace=True, axis=1)




stadiums_regions = pd.read_csv(z_maps_input_intermediate + 'map_stadiums_AGS.csv', sep=';')
stadiums_regions = pd.read_csv(z_maps_input_intermediate + 'map_stadiums_AGS.csv', sep=';')
stadiums_regions = stadiums_regions[['stadium', 'AGS']]



matches = matches.merge(stadiums_regions, on='stadium', how='inner' )


matches.sort_values(['gameday','date', 'time'], inplace=True)
matches.reset_index(inplace=True, drop=True)

matches.to_csv(z_soccer_output + 'soccer_prepared.csv',
               sep=';', encoding='UTF-8', index=False)

