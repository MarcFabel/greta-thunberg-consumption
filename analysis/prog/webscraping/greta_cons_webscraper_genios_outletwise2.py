#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 09:54:12 2020

@author: marcfabel

Description:
    This file scrapes the number of articles per specified topic in Germany.


Inputs:
    none

Outputs:
    genios_acrticles_greta.csv
    genios_articles_all.csv
"""


# packages
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import pandas as pd

# magic numbers
z_start_date = datetime(2018, 8, 1)    # 2018, 8, 1
z_end_date   = datetime(2020, 2, 28)  # 2020, 2, 28

# HOME directories
#z_media_input_list_outlets = '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/genios_sources_list/'
#z_media_output =             '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'


# work directories (LOCAL)
#z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/outlets/'


# work directories (SERVER)
z_media_output =               'W:/EoCC/analysis/data/source/media/'
z_media_input_list_outlets =   'W:/EoCC/analysis/data/source/media/'

###############################################################################
#       1) Define programs
###############################################################################


########## 1.1 loop through dates ##########
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


########## 1.2 scraper ##########
def scraper_outlet(terms, header, output_name,outlet):
    fh_write = open(z_media_output + output_name, 'w', encoding='utf8')

    # write header: outlet_var
    fh_write.write('date'+ ',' + ', '.join([outlet + '_' + s for s in header]) + '\n')    

    # loop through days
    for day in daterange(z_start_date, z_end_date):
        
        list_result = []
        
        # loop through terms
        for term in terms:        
            link = 'https://www.genios.de/dosearch?explicitSearch=true&q='+term+'&\
searchRestriction=&dbShortcut='+outlet+'&searchMask=5478&TI%2CUT\
%2CDZ%2CBT%2COT%2CSL=&KO=&MM%2COW%2CUF%2CMF%2CAO%2CTP%2CVM%2CNN%2CNJ%2\
CKV%2CZ2=&CO%2CC2%2CTA%2CKA%2CVA%2CZ1=&CT%2CZ4%2CKW=&BR%2CGW%2CN1%2CN2\
%2CNC%2CND%2CSC%2CWZ%2CZ5%2CAI%2CBC%2CKN%2CTN%2CVN%2CK0%2CB4%2CNW%2CVH\
=&Z3%2CCN%2CCE%2CKC%2CTC%2CVC=&timeFilterType=on&DT_from=\
'+ day.strftime('%d.%m.%Y') + '&DT_to=' + day.strftime('%d.%m.%Y') + '&x=61&y=18'

            # extract html
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            result_text_header = soup.find(class_="moduleResultTextHeader")
            result = result_text_header.get_text()
            
            #omit the thousands digit
            if len(result)<= 22:
                list_result.append(result[18:-1])
            if len(result)== 24:
                list_result.append(result[18:19]+result[20:-1])
            if len(result)== 25:
                list_result.append(result[18:20]+result[21:-1])
            if len(result)>25  and result[-9:-8]=="0":
                list_result.append('0')
                
        print(outlet, day.strftime('%d.%m.%Y'), ', '.join(list_result))        
        fh_write.write(day.strftime('%d.%m.%Y')+ ',' + ', '.join(list_result) + '\n')
                
                

    # close file handle
    fh_write.close()
    print('finished scraping for terms in : ' + outlet)










###############################################################################
#       3) scrape for terms in specific outlets
###############################################################################

# open list of outlets
outlets = pd.read_csv(z_media_input_list_outlets +
                     'list_outlets_url_abbreviations.csv',
                     sep=';')['abbrevation'].to_list()

#outlets = ['FTB', 'SZ']

# terms
term_all_paper = ''
term_greta_thunberg = "\"greta thunberg\""
term_FFF = "\"Fridays-For-Future\"+%7C%7C+Klimastreik+%7C%7C+\"FridaysForFuture\""

# define list of terms and list of headers
list_terms = [term_all_paper, term_greta_thunberg, term_FFF]
list_header = ['all', 'greta', 'fff']



for outlet in outlets:
     scraper_outlet(list_terms, list_header,
             'outlets/genios_articles_'+outlet+'.csv',
             outlet)
     

