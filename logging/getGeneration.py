#!/usr/bin/env python

import sqlite3

import os
import time
import glob
import urllib.request, json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# global variables
dbname='/home/pi/ssen/database/eleclog.db'

# get data from ssen website
def get_data():
    with urllib.request.urlopen("https://www.ssen.co.uk/Sse_Components/Views/Controls/FormControls/Handlers/ActiveNetworkManagementHandler.ashx?action=graph&contentId=14973&_=1537467858726") as url:
        data = json.loads(url.read().decode())

        electricity_data = data['data']['datasets']

        readings = {}
        for item in electricity_data:
            label = item['label']
            val = float(max(item['data']))
            readings[label] = val

        readings['Winter Peak Demand']= readings['Winter Peak Demand']+readings['Live Demand']
        readings['Total Renewable Capacity'] = readings['Total Renewable Capacity'] + readings['Orkney ANM'] + readings['Non-ANM Renewable Generation']

        return readings

# store the data in the database
def log_data(readings):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO readings values(datetime('now'), (?), (?), (?), (?), (?))",
                 (readings['Live Demand'],
                  readings['Winter Peak Demand'],
                  readings['Orkney ANM'],
                  readings['Non-ANM Renewable Generation'],
                  readings['Total Renewable Capacity']))

    # commit the changes
    conn.commit()
    conn.close()
    #print('store routine called')

data=get_data()
#print(data)
log_data(data)
