#!/usr/bin/env python

## script to retrieve hourly weather observations for the last 24 hours for Kirkwall Airport
## which are stored in an sqlite3 database file

## Stuart Rendall
## MSc Web technologies project
## May 2019

## detailed instructions 
## https://www.metoffice.gov.uk/datapoint/product/uk-hourly-site-specific-observations/detailed-documentation

## data retrieved:
## T: Temperature (degrees Celsius)
## D: Wind direction (16 point compass)
## S: Wind speed (mph)
## G: Wind gust (mph)
## Dp: Dew Point (degrees Celsius)
## H: Screen Relative Humidity (%)
## W: Weather Type
## V: Visibility (m)
## P: Pressure (hPa)
## Pt: Pressure Tendency (Pa/s)


import sqlite3

import os
import datetime
import glob
import urllib.request,json
from urllib.request import Request, urlopen

# global variables
dbname='/home/pi/ssen/database/weatherlog.db'

# get data from met office website
def get_data():
#    with urllib.request.urlopen("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3017?res=hourly&?key=d4ea5cd6-6cfd-4f4c-8098-62497d80eb52") as url:
#
#        data = json.loads(url.read().decode())
#        observation_data = data['SiteRep']['DV']['Location']['Period']
    req = Request("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3017?res=hourly&?key=d4ea5cd6-6cfd-4f4c-8098-62497d80eb52",headers={'User-Agent': 'Mozilla/5.0'})
	
    webpage = urlopen(req).read()
    my_json = webpage.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    observation_data = data['SiteRep']['DV']['Location']['Period']
    readings = []

    for day in observation_data:
        obs_date = day['value']
        date = datetime.datetime.strptime( obs_date,'%Y-%m-%dZ')
        for rep in day['Rep']:
            dtime = date + datetime.timedelta(minutes=int(rep['$']))
            timestamp = dtime.isoformat(sep=' ')

            readings.append({
                'timestamp':timestamp,
                'D':rep['D'],
                'H':float(rep['H']),
                'P':int(rep['P']),
                'S':int(rep['S']),
                'T':float(rep['T']),
                'W':rep['W'],
                'V':int(rep['V']),
                'Pt':rep['Pt'],
                'Dp':float(rep['Dp'])
                })

    return readings

# store the data in the database
def log_data(readings):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for obs in readings[1:]:
                    
        curs.execute("INSERT INTO rep values(?,?,?,?,?,?,?,?,?,?)",(
            obs['timestamp'],
            obs['T'],
            obs['H'],
            obs['Dp'],
            obs['D'],
            obs['S'],
            obs['P'],
            obs['Pt'],
            obs['V'],
            obs['W']
            ))

        # commit the changes
        conn.commit()

    conn.close()

    # print(' store routine called')

data=get_data()
#print(data)
log_data(data)
