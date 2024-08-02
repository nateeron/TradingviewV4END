

import datetime
import requests
import pandas as pd

def cal_NumberBar_day(value):
  
    D1__Minute = 1440
    if value == '1m':
        return D1__Minute 
    elif value == '15m':
        return D1__Minute / 15
    elif value == '30m':
        return D1__Minute / 30
    elif value == '90m':
        return D1__Minute / 90
    elif value == '1h':
        return D1__Minute / 60
    elif value == '2h':
        return D1__Minute / 120
    elif value == '4h':
        return D1__Minute / 240
    elif value == '1d':
        return 1
    else:
        return 'This is the default case'
    
    
    
def CaldateTime(number):
    start_datetime = datetime.datetime.now()
    start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    new_datetime = start_datetime - datetime.timedelta(days=number)
    print("now:",start_datetime)
    print("to :",new_datetime)
    return new_datetime


def add_hours(timestamp_str, hours):
    # Convert timestamp string to datetime object
    start_datetime = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    # Set minutes, seconds, and microseconds to 0
    start_datetime = start_datetime.replace(minute=0, second=0, microsecond=0)
    print("Start datetime:", start_datetime)
    # Add specified hours
    new_datetime = start_datetime - datetime.timedelta(hours=hours)
    return new_datetime

def Down_hours(timestamp_str, hours):
    # Convert timestamp string to datetime object
    start_datetime = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    # Set minutes, seconds, and microseconds to 0
    #start_datetime = start_datetime.replace(minute=0, second=0, microsecond=0)
    # Add specified hours
    new_datetime = start_datetime - datetime.timedelta(hours=hours)
    return new_datetime


def Up_hours(timestamp_str, hours):
    # Convert timestamp string to datetime object
    start_datetime = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    # Set minutes, seconds, and microseconds to 0
    start_datetime = start_datetime.replace(minute=0, second=0, microsecond=0)
    print("Start datetime:", start_datetime)
    # Add specified hours
    new_datetime = start_datetime + datetime.timedelta(hours=hours)
    return new_datetime

numberDay1  =  int(1000/cal_NumberBar_day("1m")) 
numberDay15 = int(1000/cal_NumberBar_day("15m"))
numberDay30 = int(1000/cal_NumberBar_day("30m"))
numberDay1h = int(1000/cal_NumberBar_day("1h") )
numberDay90 = int(1000/cal_NumberBar_day("90m"))
numberDay2h = int(1000/cal_NumberBar_day("2h") )
numberDay4h = int(1000/cal_NumberBar_day("4h") )
numberDay1d = int(1000/cal_NumberBar_day("1d") )
print("-----------------------------------------------")

print("1m",cal_NumberBar_day("1m") ,"bar"   ,numberDay1  , "Day" , "to date" ,CaldateTime(numberDay1 ) )
print("15m",cal_NumberBar_day("15m"),"bar"  ,numberDay15 , "Day" , "to date" ,CaldateTime(numberDay15) )
print("30m",cal_NumberBar_day("30m"),"bar"  ,numberDay30 , "Day" , "to date" ,CaldateTime(numberDay30) )
print("1h",cal_NumberBar_day("1h"),"bar"    ,numberDay1h , "Day" , "to date" ,CaldateTime(numberDay1h) )
print("90m",cal_NumberBar_day("90m"),"bar"  ,numberDay90 , "Day" , "to date" ,CaldateTime(numberDay90) )
print("2h",cal_NumberBar_day("2h"),"bar"    ,numberDay2h , "Day" , "to date" ,CaldateTime(numberDay2h) )
print("4h",cal_NumberBar_day("4h"),"bar"    ,numberDay4h , "Day" , "to date" ,CaldateTime(numberDay4h) )
print("1d",cal_NumberBar_day("1d"),"bar"    ,numberDay1d , "Day" , "to date" ,CaldateTime(numberDay1d) )
print("-----------------------------------------------")

def conver_time(datetime_str):
    # Parse datetime string into a datetime object
    dt_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
  
    # Convert datetime to time in seconds since the UNIX epoch
    time_sec = dt_obj.timestamp()

    # Convert time in seconds to milliseconds
    time_ms = int(time_sec * 1000)
    
    return time_ms



# get Time on Bar Last
def get_binance_ohlc(symbol, interval, limit):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
  
    response = requests.get(base_url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Set Time Zone
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')  # Convert to Bangkok time
    df.set_index('timestamp', inplace=True)
   
    # Convert numeric columns to float
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    # Select 'open', 'high', 'low', 'close' only
    return df[['open', 'high', 'low', 'close']]

def get_90m_ohlc(df):
    return df.iloc[::1]  # Select every 3rd row (since 90 minutes is 1.5 hours)

def get_data_between_datetimes(symbol, interval, start_time, end_time):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,  # Start time in milliseconds
        "endTime": end_time,      # End time in milliseconds
        "limit": 1000             # Adjust as needed, max is 1000
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Set Time Zone
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Bangkok')  # Convert to Bangkok time
    df.set_index('timestamp', inplace=True)

    # Convert numeric columns to float
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df[['open', 'high', 'low', 'close']]



def TF(t):
    if t == '1h':
        return 1
    if t == '4h':
        return 4

# print(ohlc_data)
def main():
    # Config
    symbol = 'XRPUSDT'  # XRP/USDT trading pair
    interval = '4h'     # 30 minit
    limit = 1   # Maximum number of data points to retrieve

    #get Last Bar as time
    ohlc_data = get_binance_ohlc(symbol, interval, limit)
    ohlc_data.index = pd.to_datetime(ohlc_data.index)
    ohlc_data['time_only'] = ohlc_data.index.strftime('%Y-%m-%d %H:%M:%S')


    # Display only the 'time_only' column
    t = ohlc_data.index[-1].strftime('%Y-%m-%d %H:%M:%S')
    # print(ohlc_data['time_only'])
    
    ohlc_90m_data = get_90m_ohlc(ohlc_data) # Get Time Fream 90
    
    print("--------------------------")
    print(t)
    print("--------------------------")
    
    # ************************ Select Time ******************************
    h4 = TF(interval)
    date = add_hours(t,h4*1000)
    # print(date,h4,"h",h4/24,"D",(h4/24)/7,"W",(h4/24)/30,"M")
    
    start_time = conver_time(str(date)) # 1617224400000 # 1617249600000 #conver_time('2021-04-02 04:00:00')     # Example start time in milliseconds (e.g., March 31, 2021, 00:00:00)
    end_time =   conver_time(t) # 1617310800000 # 1617336000000 #conver_time('2021-04-01 04:00:00')       # Example end time in milliseconds (e.g., March 31, 2021, 23:59:59)
    ohlc_data = get_data_between_datetimes(symbol, interval, start_time, end_time)
    BeginTime = ohlc_data.index[-1].strftime('%Y-%m-%d %H:%M:%S')
    print("--------------------------")
    print(len(ohlc_data))
    print(ohlc_data.index[-1].strftime('%Y-%m-%d %H:%M:%S'))
    print(BeginTime)
    print("--------------------------")
    lenbar = 0
    i = 1
    while True:
        
        print("--------->>> i : ",i)
        if lenbar == 1000 :
            BeginTime_ =  BeginTime 
        else:
            BeginTime_ = Down_hours(str(BeginTime),h4)
        print("************[while True:]*******************")
        # print(BeginTime_,"start_time", conver_time(str(Down_hours(str(BeginTime_),h4*1000))))
        # print(Down_hours(str(BeginTime_),h4*1000),"end_time" ,  conver_time(str(BeginTime_)))
        
        s = str(Down_hours(str(BeginTime_),h4*1000))
        e = str(BeginTime_)
        start_time = conver_time(s)
        end_time =   conver_time(e)
        print("start:",s," | ","end:",e)
        ohlc_data_ = get_data_between_datetimes(symbol, interval, start_time, end_time)
        if len(ohlc_data_) > 0 :
            BeginTime = ohlc_data_.index[0].strftime('%Y-%m-%d %H:%M:%S')
            print("[start]",ohlc_data_.index[0],"| [End]",ohlc_data_.index[len(ohlc_data_)-1],ohlc_data_.index[-1].strftime('%Y-%m-%d %H:%M:%S') )
        print("dataEnd",ohlc_data_)
        print(BeginTime)
        print(len(ohlc_data_))
        
        if i == 999999 or len(ohlc_data_) == 0 or len(ohlc_data_) == 1:
            
            break
        i += 1
        print("--------------------------")

main()