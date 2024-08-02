import requests
from datetime import datetime, timedelta
from pprint import pprint


def calculate_end_time(interval, factor):
    # Define the number of seconds per interval unit
    interval_units = {
        's': 1,           # Seconds
        'm': 60,          # Minutes
        'h': 3600,        # Hours
        'd': 86400,       # Days
        'w': 604800       # Weeks
    }
    
    # Parse the interval to get the number and the unit
    interval_value = int(interval[:-1])
    interval_unit = interval[-1]

    if interval_unit not in interval_units:
        raise ValueError(f"Unsupported interval unit: {interval_unit}")

    # Calculate the total time in seconds
    total_time_seconds = interval_value * interval_units[interval_unit] * factor

    # Calculate the end time by adding the total time in seconds to the current time
    end_time = datetime.now() + timedelta(seconds=total_time_seconds)
    
    # Convert end_time to string in desired format
    end_time_str = end_time.strftime('%d-%m-%y %H:%M:%S')
    
    # Parse the end_time string back to datetime object using strptime
    end_time_strptime = datetime.strptime(end_time_str, '%d-%m-%y %H:%M:%S')
    print(end_time.timestamp(),end_time_strptime.timestamp())
    #return end_time_strptime.timestamp()
    return end_time


def fetch_binance_klines(symbol='XRPUSDT', interval='1s', limit=1000, start_time=None, end_Time=None):
    base_url = "https://api.binance.com/api/v3/klines"
  

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit,
        'startTime':int(start_time.timestamp()),
    }
    pprint(params)
    # if start_time:
    #     params['startTime'] = int(start_time.timestamp() * 1000)  # Convert to milliseconds
    
    try:
        response = requests.get(base_url, params=params)
        print(response)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        processed_data = [{
            'time': convert_timestamp(item[0] / 1000),  # Convert milliseconds to formatted time string
            'open': float(item[1]),
            'high': float(item[2]),
            'low': float(item[3]),
            'close': float(item[4]),
            'volume': float(item[5]),
            'close_time': convert_timestamp(item[6] / 1000),  # Convert milliseconds to formatted time string
            'quote_asset_volume': float(item[7]),
            'number_of_trades': int(item[8]),
            'taker_buy_base_asset_volume': float(item[9]),
            'taker_buy_quote_asset_volume': float(item[10]),
            'ignore': float(item[11])
        } for item in data]
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def convert_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d-%m-%y %H:%M:%S')

def fetch_historical_data(symbol, interval, total_candles, limit_per_request=1000):
    all_data = []
    start_time = datetime.now()  # Start from current time
    remaining_candles = total_candles

    while remaining_candles > 0:
        limit = min(limit_per_request, remaining_candles)
        data = fetch_binance_klines(symbol, interval, limit, start_time)
        print("Time : ",start_time)
        print("Time : ",start_time.timestamp())
        if data:
            all_data.extend(data)
            #start_time = datetime.strptime(data[-1]['time'], '%d-%m-%y %H:%M:%S') - timedelta(milliseconds=1)
            start_time = calculate_end_time(interval,1000)
            print("Time : ",start_time)
            remaining_candles -= len(data)
        else:
            break  # Stop if there is an error or no more data

    return all_data

# Example usage
if __name__ == "__main__":
    symbol = 'XRPUSDT'
    interval = '1m'
    total_candles = 5000
    historical_data = fetch_historical_data(symbol, interval, total_candles)
    pprint(f"Total number of candlesticks retrieved: {len(historical_data)}")
    pprint("*********************************************************************")
    # pprint(historical_data)
    pprint("*********************************************************************")
    
    for kline in historical_data[:5]:  # Print the first 5 candlesticks
        pprint(kline)
