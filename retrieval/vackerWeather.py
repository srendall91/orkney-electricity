#!/usr/bin/env python

## script to take json file retrieved from vackerweather website and populate sqlite3 database

## Stuart Rendall
## MSc Web technologies project
## May 2019

import sqlite3

import os
import datetime
import glob
import urllib.request,json

# global variables
filename = 'database/epoch_observations.json'
dbname='database/vackerlog.db'

# display data types of each field within in the first row of data 
with open(filename, 'r') as f:
        data = json.load(f)
        observation_data = data['data']

        print(observation_data[0])
        firstobs= observation_data[0]
        print(datetime.datetime.fromtimestamp(firstobs[0]/1000))
        c=0
        for i in firstobs:
             print(c,i,':', type(i))
             c+=1
        f.close()

        
# get data from json file retrieved from the vacker weather website
def get_data():
    with open(filename, 'r') as f:
        data = json.load(f)
        observation_data = data['data']
        readings = []
        #
        for rep in observation_data:
            if (len(rep)==11):
                rep[10]=0.0
                rep.append(None)
                print('found an entry with no cloud cover value')
 
            readings.append({
                    'timestamp':rep[0]/1000,
                    'H':rep[6],
                    'P':rep[3],
                    'S':rep[4],
                    'T':rep[1],
                    'W':rep[7],
                    'V':rep[9],
                    'cc':rep[10],
                    'ch':rep[11]
                    })
        f.close()
        return readings

# store the data in the database
def log_data(readings):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for obs in readings[1:]:
                    
        curs.execute("INSERT INTO rep values(?,?,?,?,?,?,?,?,?)",(
            obs['timestamp'],
            obs['T'],
            obs['H'],
            obs['W'],
            obs['S'],
            obs['P'],
            obs['V'],
            obs['cc'],
            obs['ch']
            ))

        # commit the changes
        conn.commit()

    conn.close()

    # print(' store routine called')

data=get_data()
#print(data)
log_data(data)
