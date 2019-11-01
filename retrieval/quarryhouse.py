#!/usr/bin/env python3

import urllib.request, json
import datetime
import sqlite3
from bs4 import BeautifulSoup
import re


# global variables
#dbname='/home/pi/ssen/database/quarryhouse.db'
dbname='database/quarryhouse.db'
URL ="https://www.sunnyportal.com/Templates/PublicChartValues.aspx\
?ID=aa6b2b6e-f836-4ff5-b90c-91754955b988\
&splang=en-GB\
&plantTimezoneBias=0\
&name=\
&endTime="  #16/01/2019%2023:59:59"
startdate =datetime.datetime(2019, 1, 14, 23, 59, 59)
enddate =datetime.datetime.now()

def textToFloat(string):
    if (string):
        return float(string)
    else:
        return 0.0
    
def datestamp(enddate, datestring):
    prevdate = enddate - datetime.timedelta(days=1)
    nextdate = enddate + datetime.timedelta(days=1)
    returndate = enddate
    
    if (int(datestring)== prevdate.date().day): returndate=prevdate
    if (int(datestring)== nextdate.date().day): returndate=nextdate
    return returndate
    

def get_data(recDate):
    callurl = URL+recDate.strftime('%Y/%m/%d%%20%H:%M:%S')
    with urllib.request.urlopen(callurl) as url:
        page = url.read()
        soup = BeautifulSoup(page, 'html.parser')
        
        DataTable = soup.find('table',)
        
        rows = DataTable.find_all('tr')

        data=[]

        for row in rows[1:]:
            entry = row.find_all('td')
            #print(entry[0].text,entry[1].text, entry[2].text)
            timestamp = str(datestamp(recDate, entry[0].text[7:9]).date())+' '+entry[0].text[:5]
            data.append([timestamp, textToFloat(entry[1].text),textToFloat(entry[2].text)])

        return data

# store the data in the database
def log_data(readings):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for obs in readings[1:]:
                    
        curs.execute("INSERT INTO readings values(?,?,?)",(
            obs[0],
            obs[1],
            obs[2]
            ))

        # commit the changes
        conn.commit()

    conn.close()

getdate = startdate
while (getdate <= enddate):
    records = get_data(getdate)
    log_data(records)
    getdate = getdate + datetime.timedelta(days=2)
    print(getdate)

print("job done")
    
    
