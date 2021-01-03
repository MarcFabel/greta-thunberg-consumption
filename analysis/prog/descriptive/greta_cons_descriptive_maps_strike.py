#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 14:47:19 2020

@author: marcfabel


Description:
    The program reads in shapefiles (Kreis and Bula) and csv-files for 
    strikes (different sources: ordnungsamt, fff, facebook & insta)
    

Inputs:
    VG250_KRS.shp                                                                   [source]
    VG250_bula_borders.shp                                                          [intermed]
    
    greta_cons_fff_strikes_internet_geocoordinates_all_strikes.csv                  [intermed]
    greta_cons_fff_strikes_biggest_cities_social_media_geocoordinates.csv           [intermed]
    greta_cons_FFF_strikes_ordnungsaemter_geocoordinates_all_strikes_wahlkreise.csv [intermed]
    

Outputs:
    various figures                                                                 [z_output_figures]


"""

import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt



# directories (HOME)
z_data              = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/'
z_path_admin        = z_data + 'source/shapes/vg250_2019-01-01.geo84.shape.ebenen/vg250_ebenen/'
z_shape_intermed    = z_data + 'intermediate/shapes/'
z_strike_intermed   = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/fff_strikes/'
z_output_figures    = '/Users/marcfabel/econ/greta_consumption/analysis/output/graphs/descriptive/'
z_prefix            = 'greta_cons_'

# magic numbers
z_epsg_wgs84    = 4326
z_epsg_mercator = 3785


# color_palette
z_c_lightgray = '#c0cabe'
z_c_darkred   = '#94122c'



###############################################################################
# Read in relevant shapes and csv
###############################################################################


# Admin shapes  ###############################################################

# kreise
kreise = gp.read_file(z_path_admin + 'VG250_KRS.shp')

# bula_borders
bula_borders = gp.read_file(z_shape_intermed + 'VG250_bula_borders.shp')


# Teralytics shapes  ##########################################################
z_teralytics_fn = 'source/shapes/teralytics/deldd-1-taeglich-aktualisierte-langdistanz-reisen-ifo-institut-shapes.shp'
teralytics = gp.read_file(z_data + z_teralytics_fn)



# Strike - files ##############################################################

# internet strikes
df = pd.read_csv(z_strike_intermed + 'greta_cons_fff_strikes_internet_geocoordinates_all_strikes.csv')
df.rename(columns={'jointg_lat':'latitude', 'jointg_lon':'longitude'}, inplace=True)
strikes_internet = gp.GeoDataFrame(df,geometry=gp.points_from_xy(df.longitude, df.latitude)).set_crs(epsg=z_epsg_wgs84)
strikes_internet.plot(figsize=(8, 8))

# big cities
df = pd.read_csv(z_strike_intermed + 'greta_cons_fff_strikes_biggest_cities_social_media_geocoordinates.csv', delimiter=';')
strikes_cities = gp.GeoDataFrame(df,geometry=gp.points_from_xy(df.longitude, df.latitude)).set_crs(epsg=z_epsg_wgs84)

# ordnungsamt
df = pd.read_csv(z_strike_intermed + 'greta_cons_FFF_strikes_ordnungsaemter_geocoordinates_all_strikes_wahlkreise.csv', delimiter=';')
df.rename(columns={'jointg_lat':'latitude', 'jointg_lon':'longitude'}, inplace=True)
strikes_ordnungsamt = gp.GeoDataFrame(df,geometry=gp.points_from_xy(df.longitude, df.latitude)).set_crs(epsg=z_epsg_wgs84)



# Append strikes and take 2019 only ###########################################
strikes = strikes_internet[['day', 'month', 'year', 'geometry']].copy()
strikes = strikes.append(strikes_cities[['day', 'month', 'year', 'geometry']])
strikes = strikes.append(strikes_ordnungsamt[['day', 'month', 'year', 'geometry']])

strikes = strikes.loc[strikes['year'] == 2019]





# Residualized_strikes
resid_places_ols = pd.read_csv(z_data+'temp/greta_cons_resid_ols_selected_places.csv',
                           delimiter=';', dtype={'startid':object,'endid':object},
                           parse_dates=['date'], infer_datetime_format=True)

resid_places_poisson = pd.read_csv(z_data+'temp/greta_cons_resid_poisson_selected_places.csv',
                           delimiter=';', dtype={'startid':object,'endid':object},
                           parse_dates=['date'], infer_datetime_format=True)




resid_times_ols = pd.read_csv(z_data+'temp/greta_cons_resid_ols_selected_times.csv',
                           delimiter=';', dtype={'startid':object,'endid':object},
                           parse_dates=['date'], infer_datetime_format=True)

resid_times_poisson = pd.read_csv(z_data+'temp/greta_cons_resid_poisson_selected_times.csv',
                           delimiter=';', dtype={'startid':object,'endid':object},
                           parse_dates=['date'], infer_datetime_format=True)


# combine ols & poisson
resid_places = resid_places_ols.merge(resid_places_poisson, 
                                      on=['date', 'startid', 'endid', 'count'])

resid_times = resid_times_ols.merge(resid_times_poisson,
                                    on=['date', 'endid', 'count'])


# change order of columns



###############################################################################
# Plots - strikes
###############################################################################




# all strikes in 2019 #########################################################
f, ax = plt.subplots(figsize=(11, 15))
kreise.plot(ax=ax, color=z_c_lightgray, edgecolor='white', linewidth=0.15)
bula_borders.plot(ax=ax, color='white', linewidth=0.6)
strikes.plot(ax=ax, marker='o', color=z_c_darkred, markersize=2)
plt.axis('off')
plt.savefig(z_output_figures + z_prefix + 'fff_strikes_2019.png',
            bbox_inches = 'tight', dpi=250)





# matrix: plot month month ####################################################
dict_month_name = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May',
                   6:'June', 7:'July', 8:'August', 9:'September', 10:'October',
                   11:'November', 12:'December'}



# landscape
fig, axs = plt.subplots(3, 4, figsize=(14, 10.5))
fig.subplots_adjust(hspace = .25)
axs = axs.ravel()

for num in range(12):
    month = num + 1
    kreise.plot(ax=axs[num], color=z_c_lightgray)
    bula_borders.plot(ax=axs[num], color='white', linewidth=0.3)
    strikes.loc[strikes['month'] == month].plot(ax=axs[num], marker='o', color=z_c_darkred, markersize=0.7)
    axs[num].axis('off')
    axs[num].set_title(dict_month_name[month], fontweight='bold')

plt.savefig(z_output_figures + z_prefix + 'fff_strikes_months.png',
            bbox_inches = 'tight', dpi=300)




# portrait version of matrix
fig, axs = plt.subplots(4, 3, figsize=(10.5, 15))
fig.subplots_adjust(hspace = .25)
axs = axs.ravel()

for num in range(12):
    month = num + 1
    kreise.plot(ax=axs[num], color=z_c_lightgray)
    strikes.loc[strikes['month'] == month].plot(ax=axs[num], marker='o', color=z_c_darkred, markersize=1.5)
    axs[num].axis('off')
    axs[num].set_title(dict_month_name[month], fontweight='bold')







###############################################################################
# Plots - strike participation
###############################################################################




aachen = teralytics.merge(resid_places.loc[resid_places['endid']=='006266500'], 
                          right_on=['startid'], left_on=['FID'], how='outer')
berlin = teralytics.merge(resid_places.loc[resid_places['endid']=='006242203'], 
                          right_on=['startid'], left_on=['FID'], how='outer')
hamburg = teralytics.merge(resid_places.loc[resid_places['endid']=='006278202'], 
                          right_on=['startid'], left_on=['FID'], how='outer')
lubbenau = teralytics.merge(resid_places.loc[resid_places['endid']=='006257100'], 
                          right_on=['startid'], left_on=['FID'], how='outer')
garzweiler = teralytics.merge(resid_places.loc[resid_places['endid']=='006253500'], 
                          right_on=['startid'], left_on=['FID'], how='outer')



# other scheme that are working
# headtailbreaks
# naturalbreaks
# 'userdefined' classification_kwds={'bins':[200, 500, 10000]},




# plot Aachen strike 2019  
aachen.plot(figsize=(8, 8), missing_kwds={'color': 'lightgrey'}, cmap = 'Greens', 
            edgecolor=z_c_lightgray, linewidth=0.3,
            column='res_ols_interaction_small', scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
plt.axis('off')



    
berlin.plot(figsize=(8, 8), missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
            edgecolor=z_c_lightgray, linewidth=0.3,
            column='res_p_interaction_small', scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
plt.axis('off')


    
hamburg.plot(figsize=(8, 8), missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column='res_p_interaction_large', scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
plt.axis('off')







# loop through resid_specification
z_dict_resids = {'res_ols':'OLS, no interaction',
                 'res_ols_interaction_small':'OLS, interaction w/ week+month',
                 'res_ols_interaction_large':'OLS, fully interacted',
                 'res_p':'Poisson, no interaction',
                 'res_p_interaction_small':'Poisson, interaction w/ week+month',
                 'res_p_interaction_large':'Poisson, fully interacted'}



# Aachen
f, axs = plt.subplots(2, 3, figsize=(21, 15)) 
axs = axs.ravel()
num = 0
for spec in list(z_dict_resids.keys()):
     
    aachen.plot(ax=axs[num], missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column=spec, scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
    axs[num].axis('off')
    axs[num].set_title(z_dict_resids[spec], fontweight='bold') 
    num = num + 1
plt.savefig(z_output_figures + 'maps_resid_trips/' + z_prefix +
                'resid_trips_aachen.png',
            bbox_inches = 'tight', dpi=200)

    
# Berlin
f, axs = plt.subplots(2, 3, figsize=(21, 15)) 
axs = axs.ravel()
num = 0
for spec in list(z_dict_resids.keys()):
     
    berlin.plot(ax=axs[num], missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column=spec, scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
    axs[num].axis('off')
    axs[num].set_title(z_dict_resids[spec], fontweight='bold') 
    num = num + 1
plt.savefig(z_output_figures + 'maps_resid_trips/' + z_prefix +
                'resid_trips_berlin.png',
            bbox_inches = 'tight', dpi=200)
    
    
# Hamburg
f, axs = plt.subplots(2, 3, figsize=(21, 15)) 
axs = axs.ravel()
num = 0
for spec in list(z_dict_resids.keys()):
     
    hamburg.plot(ax=axs[num], missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column=spec, scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
    axs[num].axis('off')
    axs[num].set_title(z_dict_resids[spec], fontweight='bold') 
    num = num + 1
plt.savefig(z_output_figures + 'maps_resid_trips/' + z_prefix +
                'resid_trips_hamburg.png',
            bbox_inches = 'tight', dpi=200)





f, axs = plt.subplots(2, 3, figsize=(21, 15)) 
axs = axs.ravel()
num = 0
for spec in list(z_dict_resids.keys()):
     
    lubbenau.plot(ax=axs[num], missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column=spec, scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
    axs[num].axis('off')
    axs[num].set_title(z_dict_resids[spec], fontweight='bold') 
    num = num + 1
plt.savefig(z_output_figures + 'maps_resid_trips/' + z_prefix +
                'resid_trips_lubbenau.png',
            bbox_inches = 'tight', dpi=200)





f, axs = plt.subplots(2, 3, figsize=(21, 15)) 
axs = axs.ravel()
num = 0
for spec in list(z_dict_resids.keys()):
     
    garzweiler.plot(ax=axs[num], missing_kwds={'color': 'lightgrey'}, cmap = 'Greens',
             edgecolor=z_c_lightgray, linewidth=0.3,
            column=spec, scheme='fisher_jenks', legend=True,
            legend_kwds={'fontsize':'x-small', 'loc':'lower right'})
    axs[num].axis('off')
    axs[num].set_title(z_dict_resids[spec], fontweight='bold') 
    num = num + 1
plt.savefig(z_output_figures + 'maps_resid_trips/' + z_prefix +
                'resid_trips_garzweiler.png',
            bbox_inches = 'tight', dpi=200)
















