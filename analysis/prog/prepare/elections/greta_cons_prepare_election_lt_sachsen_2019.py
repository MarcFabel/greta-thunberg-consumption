# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:48:00 2020

@author: Marc Fabel

Description:
    The program prepares the Sachsen 2019 election data on the AGS level

Inputs:
    -  Sachsen_LT_Gemeindeebene.xlsx                     [input]

Outputs:
    - election_thueringen2019_ags_prepared.csv              [intermediate]

"""

# packages
import pandas as pd



# paths (WORK LOCAL)

z_election_input =       'W:/EoCC/analysis/data/source/elections/landtag_sachsen_2019/'
z_election_output =      'W:/EoCC/analysis/data/intermediate/elections/'



# paths (SERVER)
#z_election_input =      'W:/EoCC/analysis/data/source/elections/landtag_sachsen_2019/'



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
       'wahlberechtigte', 'ungueltige_2', 'gueltige_2',

       'wahlbeteiligung',
       'cdu_2_in_%', 'die_linke_2_in_%', 'spd_2_in_%', 'afd_2_in_%',
       'gruene_2_in_%', 'npd_2_in_%', 'fdp_2_in_%', 'freie_waehler_2_in_%',
       'tierschutzpartei_2_in_%', 'piraten_2_in_%', 'die_partei_2_in_%',
       'bueso_2_in_%', 'adpm_2_in_%', 'blaue_#teampetry_2_in_%', 'kpd_2_in_%',
       'oedp_2_in_%', 'die_humanisten_2_in_%', 'pdv_2_in_%',
       'gesundheitsforschung_2_in_%']]

# adjust column names
elec.columns = elec.columns.str.replace('_2_in_%','')
elec.columns = elec.columns.str.replace('_2','')




# aggregate to municipality level
elec = elec.groupby(['ags']).sum()


# write-out
elec.to_csv(z_election_output + 'election_sachsen2019_ags_prepared.csv', sep=';', encoding='UTF-8', index=True, float_format='%.1f')