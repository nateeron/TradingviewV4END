import requests
import pandas as pd
import sqlite3
from pprint import pprint
# Define the base URL and parameters
from datetime import datetime,timedelta

import threading
import time
import websocket
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from flask_cors import CORS
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; specify domains as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)



base_url = "https://api.binance.com/api/v3/klines"
symbol = 'XRPUSDT'
interval = '1m'  # Interval for candlesticks
limit = 5  # Number of data points to fetch
lengtbar = 15

    
CONN = sqlite3.connect('crypto_prices.db')

      
def StartNewTime(interval, factor):
    # Define the number of seconds per interval unit
    intervalUnits = {
        's': 1,         # Seconds
        'm': 60,        # Minutes
        'h': 3600,      # Hours
        'd': 86400,     # Days
        'w': 604800     # Weeks
    }
    
    # Parse the interval to get the number and the unit
    intervalValue = int(interval[:-1])
    intervalUnit = interval[-1]
    
    # Calculate the total number of milliseconds
    totalMilliseconds = intervalValue * intervalUnits[intervalUnit] * factor * 1000
    
    return totalMilliseconds



def load_data(symbol, interval, limit, lastEndTime):
    
    params = {
         
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
    if lastEndTime != 0:
        params['startTime'] = lastEndTime
        
    response = requests.get(base_url, params=params)
    data = []
    if response.status_code == 200:
        data = response.json()
      
    
    return data

def SortData(data):
    sortedData = sorted(data, key=lambda x: x[0])
    return sortedData

def get_data(lengtbar_ ,limit_):
    
    num_batches = int(lengtbar_ / limit_)
    data_ALL = []
    lastEndTime = 0
    
    for _ in range(num_batches):
        x = load_data(symbol, interval, limit_, lastEndTime)
        
       
        data_ALL.extend(x)  # Use extend to add elements of x to data_ALL
        
        
        if len(x) > 0 :
            st = StartNewTime(interval, limit_)
            lastEndTime = x[0][0] - st
        
    resp = SortData(data_ALL)
    insert(resp)
    return resp






def CreateTable():
    cursor = CONN.cursor()
    
    cursor.execute('''
             CREATE TABLE IF NOT EXISTS tb_price (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestem DATETIME,
                 close REAL
             )
         ''')
    CONN.commit()
    CONN.close()
    
    
def insert(data):
         # Connect to the SQLite database (or create it if it doesn't exist)
        CONN = sqlite3.connect('crypto_prices.db')
        print(data)
        cursor = CONN.cursor()
        # Insert data into the table
        for row in data:
            cursor.execute('''
                INSERT INTO tb_price (timestem, close)
                VALUES (?,  ?)
            ''', (row[0],  row[4]))

        # Commit the changes and close the connection
        CONN.commit()
        CONN.close()
  
def CaldateTimessss(number):
    start_datetime = datetime.now()
    start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    new_datetime = start_datetime - timedelta(days=number)
    # print("now:",start_datetime)
    # print("to :",new_datetime)
    return new_datetime
def CaldateTime(timestamp):
    # Convert the timestamp to a datetime object
    original_datetime = datetime.fromtimestamp(timestamp / 1000.0)
    
    # Print the current datetime and the adjusted datetime
    #print("Original datetime:", original_datetime)
    
    return original_datetime

def select():
    cs = sqlite3.connect('crypto_prices.db')
    cursor = cs.cursor()
    qury = ''' select * From  tb_price order by timestem '''
    cursor.execute(qury)
    data = cursor.fetchall()
    # print(data)
    print("------------------------------------")
    
    oj_ALL = []
    for item in data:
        oj = {}
        # print(CaldateTime(item[1]),item[2])
        oj["time"] = item[1]
        oj["value"] = item[2]
        oj_ALL.append(oj)
    cs.close()
    print("///////-----------------------------------/////////-")
    # print(oj_ALL)
    
    return oj_ALL

def delete():
    CONN = sqlite3.connect('crypto_prices.db')
    cursor = CONN.cursor()
      
    cursor.execute('''DELETE FROM tb_price ''')

    # Commit the changes and close the connection
    CONN.commit()
    CONN.close()
        
class req(BaseModel):
    ok: str
    limit:int
    lengtbar:int
    
   
@app.get("/xrp")
def getxrp():
    
    return select()

@app.get("/delete")
def getxrp():
    delete()
    return 'success'

@app.post("/insert")
def posxrp(req: req):
   
    # print(req.ok)
    lengtbar_ = req.lengtbar
    limit_ = req.limit
    get_data(lengtbar_ ,limit_)
    return "OK"

# CreateTable()
#insert()
# select()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,  port=8400)