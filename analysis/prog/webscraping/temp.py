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

# magic numbers
z_start_date = datetime(2018, 8, 1)    # 2018, 8, 1
z_end_date   = datetime(2019, 12, 31)  # 2019, 12, 31

# HOME directories
#z_media_output =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'

# work directories (LOCAL)
z_media_output =     'C:/Users/fabel/Dropbox/greta_cons_Dx/analysis/data/source/media/'

###############################################################################
#       1) Define programs
###############################################################################


########## 1.1 loop through dates ##########
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


########## 1.2 scraper ##########
def scraper_outlet(term, output_name,outlet):
    fh_write = open(z_media_output + output_name, 'w')
    fh_write.write('The following terms were used: ' + ',' + term + '\n')

    # loop through days
    for day in daterange(z_start_date, z_end_date):
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
            print(day.strftime('%d.%m.%Y'), result[18:-1])
            fh_write.write(day.strftime('%d.%m.%Y') + ',' + result[18:-1] + '\n')
        if len(result)== 24:
            print(day.strftime('%d.%m.%Y'), result[18:19]+result[20:-1])
            fh_write.write(day.strftime('%d.%m.%Y') + ',' + result[18:19]+result[20:-1] + '\n')
        if len(result)== 25:
            print(day.strftime('%d.%m.%Y'), result[18:20]+result[21:-1])
            fh_write.write(day.strftime('%d.%m.%Y') + ',' + result[18:20]+result[21:-1] + '\n')
        if len(result)>25  and result[-9:-8]=="0":
            print(day.strftime('%d.%m.%Y'), '0')
            fh_write.write(day.strftime('%d.%m.%Y') + ',' + '0' + '\n')

    # close file handle
    fh_write.close()
    print('finished scraping for terms: ' + term)










###############################################################################
#       3) scrape for terms in specific outlets
###############################################################################


outlets = ['FAZ', 'SZ']

term_greta_thunberg = "\"greta thunberg\""

for outlet in outlets:
     print(outlet)
     scraper_outlet(term_greta_thunberg,
             'outlets/genios_articles_'+outlet+'_greta_thunberg.csv',
             outlet)








