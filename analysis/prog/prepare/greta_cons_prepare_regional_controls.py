#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 11:30:45 2021

@author: marcfabel


Description:
    The program prepares regional controls on ags5

Inputs: [source]
    111_area_2019.xlsx                      [source]
	131_workers_degree_2019.xlsx            [source]
	132_ue_rates_2019.xlsx                  [source]
	133_workers_sector_2018.xlsx            [source]
    
    population_ags5_prepared.csv            [intermed]
    

Outputs:
    - reta_cons_regional_controls.csv             [intermediate]
    
Update:

"""

# packages
import pandas as pd


# paths (HOME)
z_regional_source =         '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/regional_database/'
z_population_intermed =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/population/'
z_regional_output =         '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/regional_database/'




###############################################################################
#           11_TERRITORY [IN SQUARE KILOMETERS]
###############################################################################

territory = pd.read_excel(z_regional_source + '111_area_2019.xlsx',
                          dtype=str, skiprows=6, skipfooter=29)
territory.columns=['ags', 'ags_name', 'area']


# corect Hamburg & Berlin
territory.loc[territory['ags']=='02', 'ags'] = '02000'
territory.loc[territory['ags']=='11', 'ags'] = '11000'


# keep only ags5
territory = territory.loc[territory['ags'].str.len() == 5]
territory = territory.loc[territory['area'] != '-'] 


# encode
territory['area'] = pd.to_numeric(territory['area'], errors='coerce')




###############################################################################
#           Population (already prepared in anohter prog)
###############################################################################

population = pd.read_csv(z_population_intermed + 'population_ags5_prepared.csv',
                         sep=';', encoding='UTF-16', dtype=str)
population = population[['ags', 'ags_name', 'pop_t', 'pop_t_growth']]
population['pop_t'] = pd.to_numeric(population['pop_t'], errors='coerce')




###############################################################################
#           131 workers with degree
###############################################################################



# 2019 ########################################################################
degree = pd.read_excel(z_regional_source + '131_workers_degree_2019.xlsx',
                          dtype=str, skiprows=15, skipfooter=19)
degree.columns=['ags', 'ags_name', 'degree', 'total', 'male', 'female', 'f_t', 'f_m', 'f_f']
degree = degree[['ags', 'ags_name', 'degree', 'total']]

# drop irrelevant rows
degree = degree.loc[degree['total'] != '-'] 
degree['total'] = pd.to_numeric(degree['total'], errors='coerce')

# corect Hamburg & Berlin
degree.loc[degree['ags']=='02', 'ags'] = '02000'
degree.loc[degree['ags']=='11', 'ags'] = '11000'

# fill in ags & select only ags5
degree.fillna(method='ffill', inplace=True)
degree = degree.loc[degree['ags'].str.len() == 5]

# pivot table to generate share
degree = degree.pivot(values='total', index=['ags'],
                    columns='degree')

degree['share_uni_degree'] = (degree['mit akademischem Abschluss'] / degree['Insgesamt']) *100
degree.reset_index(inplace=True)
degree_2019 = degree.copy()




# 2014 ########################################################################
degree = pd.read_excel(z_regional_source + '131_workers_degree_2014.xlsx',
                          dtype=str, skiprows=15, skipfooter=19)
degree.columns=['ags', 'ags_name', 'degree', 'total', 'male', 'female', 'f_t', 'f_m', 'f_f']
degree = degree[['ags', 'ags_name', 'degree', 'total']]

# drop irrelevant rows
degree = degree.loc[degree['total'] != '-'] 
degree['total'] = pd.to_numeric(degree['total'], errors='coerce')

# corect Hamburg & Berlin
degree.loc[degree['ags']=='02', 'ags'] = '02000'
degree.loc[degree['ags']=='11', 'ags'] = '11000'

# fill in ags & select only ags5
degree.fillna(method='ffill', inplace=True)
degree = degree.loc[degree['ags'].str.len() == 5]

# pivot table to generate share
degree = degree.pivot(values='total', index=['ags'],
                    columns='degree')
degree.reset_index(inplace=True)

# correct for district reform
degree.loc[degree['ags']=='03156', 'ags'] = '03159'
degree.loc[degree['ags']=='03152', 'ags'] = '03159'
degree = degree.groupby(['ags']).sum() 
degree.reset_index(inplace=True)

# generate share
degree['share_uni_degree'] = (degree['mit akademischem Abschluss'] / degree['Insgesamt']) *100

degree = degree[['ags', 'share_uni_degree']]
degree.rename(columns={'share_uni_degree':'share_uni_degree_2014'}, inplace=True)




## Combine the cross sections #################################################
degree = degree.merge(degree_2019, on=['ags'])
degree['share_uni_degree_growth'] = degree['share_uni_degree'] - degree['share_uni_degree_2014']
degree = degree[['ags', 'share_uni_degree', 'share_uni_degree_growth']]




###############################################################################
#           132 Unemplyoment
###############################################################################


# 2019  #######################################################################
ue = pd.read_excel(z_regional_source + '132_ue_rates_2019.xlsx',
                          dtype=str, skiprows=7, skipfooter=43,
                          usecols= "A, B, J")
ue.columns =['ags', 'ags_name', 'ue_rate']

# corect Hamburg & Berlin
ue.loc[ue['ags']=='02', 'ags'] = '02000'
ue.loc[ue['ags']=='11', 'ags'] = '11000'

# drop irrelevant rows
ue = ue.loc[ue['ue_rate'] != '-'] 
ue = ue.loc[ue['ags'].str.len() == 5]
ue['ue_rate'] = pd.to_numeric(ue['ue_rate'], errors='coerce')
ue_2019 = ue.copy()




# 2014  #######################################################################
ue = pd.read_excel(z_regional_source + '132_ue_rates_2014.xlsx',
                          dtype=str, skiprows=7, skipfooter=43,
                          usecols= "A, B, J")
ue.columns =['ags', 'ags_name', 'ue_rate']

# corect Hamburg & Berlin
ue.loc[ue['ags']=='02', 'ags'] = '02000'
ue.loc[ue['ags']=='11', 'ags'] = '11000'

# drop irrelevant rows
ue = ue.loc[ue['ue_rate'] != '-'] 
ue = ue.loc[ue['ags'].str.len() == 5]
ue['ue_rate'] = pd.to_numeric(ue['ue_rate'], errors='coerce')

# correct for district reforms
ue.loc[ue['ags']=='03156', 'ags'] = '03159'
ue.loc[ue['ags']=='03152', 'ags'] = '03159'
ue = ue.groupby(['ags']).mean() 
ue.reset_index(inplace=True)
ue.rename(columns={'ue_rate':'ue_rate_2014'}, inplace=True)




## Combine the cross sections #################################################
ue = ue.merge(ue_2019, on='ags')
ue['ue_rate_growth'] = ue['ue_rate'] - ue['ue_rate_2014']
ue = ue[['ags', 'ue_rate', 'ue_rate_growth']]





###############################################################################
#           133 Sectors
###############################################################################


# 2019  #######################################################################
sectors = pd.read_excel(z_regional_source + '133_workers_sector_2018.xlsx',
                          dtype=str, skiprows=7, skipfooter=12)
sectors.columns = ['ags', 'ags_name', 'total', 'agriculture', 'industry',
                   'processing', 'building', 'trade', 'service', 'public']
sectors.drop(columns='processing', inplace=True)

# corect Hamburg & Berlin
sectors.loc[sectors['ags']=='02', 'ags'] = '02000'
sectors.loc[sectors['ags']=='11', 'ags'] = '11000'

# drop irrelevant rows
sectors = sectors.loc[sectors['total'] != '-'] 
sectors = sectors.loc[sectors['ags'].str.len() == 5]

# encode
z_sector_num_cols = ['total', 'agriculture', 'industry', 
              'building', 'trade', 'service', 'public']
for col in z_sector_num_cols:
    sectors[col] = pd.to_numeric(sectors[col], errors='coerce')

# generate shares 
z_sector_sectors = ['agriculture', 'industry',
              'building', 'trade', 'service', 'public']
for col in z_sector_sectors:
    sectors['share_'+col] = (sectors[col]/sectors['total'])*100
sectors.drop(columns=['total','ags_name']+z_sector_sectors, inplace=True)
sectors_2019 = sectors.copy()


# 2014  #######################################################################
sectors = pd.read_excel(z_regional_source + '133_workers_sector_2014.xlsx',
                          dtype=str, skiprows=7, skipfooter=12)
sectors.columns = ['ags', 'ags_name', 'total', 'agriculture', 'industry',
                   'processing', 'building', 'trade', 'service', 'public']
sectors.drop(columns='processing', inplace=True)

# corect Hamburg & Berlin
sectors.loc[sectors['ags']=='02', 'ags'] = '02000'
sectors.loc[sectors['ags']=='11', 'ags'] = '11000'

# drop irrelevant rows
sectors = sectors.loc[sectors['total'] != '-'] 
sectors = sectors.loc[sectors['ags'].str.len() == 5]

# encode
z_sector_num_cols = ['total', 'agriculture', 'industry', 
              'building', 'trade', 'service', 'public']
for col in z_sector_num_cols:
    sectors[col] = pd.to_numeric(sectors[col], errors='coerce')

# generate shares 
z_sector_sectors = ['agriculture', 'industry',
              'building', 'trade', 'service', 'public']
for col in z_sector_sectors:
    sectors['share_'+col] = (sectors[col]/sectors['total'])*100
sectors.drop(columns=['total','ags_name']+z_sector_sectors, inplace=True)

# rename columns
sectors.rename(columns={'share_agriculture'	:'share_agriculture_2014',
                        'share_industry'    	:'share_industry_2014',
                        'share_building'	    :'share_building_2014',
                        'share_trade'		:'share_trade_2014',
                        'share_service'		:'share_service_2014',
                        'share_public'		:'share_public_2014'}, inplace=True)


    
    
    
 # combine the cross-sections  ################################################
sectors = sectors.merge(sectors_2019, on='ags')

for var in ['share_agriculture', 'share_industry', 'share_building', 'share_trade', 'share_service', 'share_public']:
    sectors[var+'_growth'] = sectors[var] - sectors[var+'_2014']
    sectors.drop(var+'_2014', axis=1, inplace=True)
   
    
    



###############################################################################
#           Combine data and generate variables
###############################################################################

# combine data
regional = territory[['ags', 'area']].copy()
regional = regional.merge(population, on='ags')
regional = regional.merge(degree, on='ags')
regional = regional.merge(ue, on='ags')
regional = regional.merge(sectors, on='ags')


# generate density
regional['pop_density'] = regional['pop_t'] / regional['area']
regional.drop(columns=['pop_t', 'area'], inplace=True)

regional['pop_density_cat'] = pd.cut(regional['pop_density'], 
  bins=[0,regional['pop_density'].quantile(0.33) ,
        regional['pop_density'].quantile(0.66), float('Inf')],
  labels=['rural', 'medium', 'city'])


# export 
regional.to_csv(z_regional_output + 'greta_cons_regional_controls.csv', 
                sep=';', encoding='UTF-8', index=False, float_format='%.3f')



