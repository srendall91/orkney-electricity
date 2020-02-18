#!/usr/bin/env python3

import urllib.request, json
import sqlite3
from bs4 import BeautifulSoup
import re
import logging

def getIconValue(s):
    result = re.search('glyphicon-(.*)-sign', str(s))
    return result.group(1)

def getZoneNumber(s):
    result = re.search('Zone (.*) ', str(s))
    if (result):
        return result.group(1)
    else:
        return 'Core'

# global variables
dbname='/home/pi/ssen/database/anmlog.db'
STATUS_URL ='https://www.ssen.co.uk/ANMGeneration/'
logging.basicConfig(filename='/home/pi/ssen/database/ANMstatus.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

def get_data():
    with urllib.request.urlopen(STATUS_URL) as url:
        page = url.read()
        soup = BeautifulSoup(page, 'html.parser')

        AMNTable = soup.find('div', {'class': 'Widget-Base Widget-ANMStatus'})

        AMNrows = AMNTable.find_all('tr')
        

        AMN={}

        for i in range(2,11):
            
            AMNdata = AMNrows[i].find_all('td')
            key = getZoneNumber(AMNdata[0])
            data = (getIconValue(AMNdata[1]),
                   getIconValue(AMNdata[2]),
                   getIconValue(AMNdata[3])
                   )
            AMN[key]=data

        return(AMN)


# store the data in the database
def log_data(readings):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO records VALUES (datetime('now'), ?)",
                 (readings,))

    # commit the changes
    conn.commit()
    conn.close()

def get_last_written_record():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT log FROM records ORDER BY timestamp DESC LIMIT 1")
    rec= curs.fetchone()

    # commit the changes
    conn.commit()
    conn.close()
    return rec


cur_readings = json.dumps(get_data(), sort_keys=True)
last_readings = get_last_written_record()[0]
#print(cur_readings)
#print(last_readings)
if (cur_readings!=last_readings):
    log_data(cur_readings)
    logging.info("ANM state changed - data stored")
    #print( 'Data stored')
else:
    logging.info("no change")
    #print ('Not recorded')