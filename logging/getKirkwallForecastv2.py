#!/usr/bin/env python

## script to retrieve weather forecasts for the next 5 days for Kirkwall Airport
## which are stored in an sqlite3 database file
## the forecasts are revised and updated every hour.

## Stuart Rendall
## MSc Web technologies project
## May 2019

## detailed instructions 
## https://www.metoffice.gov.uk/datapoint/product/uk-3hourly-site-specific-forecast/detailed-documentation

import sqlite3

import os
import datetime
import glob
import urllib.request,json
import logging

from urllib.request import Request, urlopen



# global variables
dbname='/home/pi/ssen/database/forecastlog.db'
logging.basicConfig(filename='/home/pi/ssen/database/forecast.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

# get data from met office website
# def get_data():
    # with urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352157?res=3hourly&?key=d4ea5cd6-6cfd-4f4c-8098-62497d80eb52") as url:

        # data = json.loads(url.read().decode())
        # forecast_data =  data['SiteRep']['DV']
        
        # return forecast_data

# get data from met office website
def get_data():
    req = Request("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/352157?res=3hourly&?key=d4ea5cd6-6cfd-4f4c-8098-62497d80eb52",headers={'User-Agent': 'Mozilla/5.0'})
	
    webpage = urlopen(req).read()
    my_json = webpage.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    forecast_data =  data['SiteRep']['DV']

    return forecast_data

# store the data in the database
def log_data(forecast):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO rep VALUES (datetime('now'), ?)",
                 (forecast,))

    # commit the changes
    conn.commit()

    conn.close()

    # print(' store routine called')

def get_last_written_record():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT forecast FROM rep ORDER BY timestamp DESC LIMIT 1")
    rec= curs.fetchone()

    # commit the changes
    conn.commit()

    conn.close()
    return rec


cur_forecast = json.dumps(get_data(), sort_keys=True)
last_forecast = get_last_written_record()[0]
#print(cur_forecast)
log_data(cur_forecast)
logging.info('New Forecast recorded')
#print(last_forecast)
if (cur_forecast!=last_forecast):
    log_data(cur_forecast)
    logging.info('New forecast recorded')
else:
    logging.info('still same forecast')

