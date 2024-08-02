import requests
from datetime import datetime
from pprint import pprint
def fetch_binance_klines(symbol='XRPUSDT', interval='1s', limit=5000):
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    try:
        response = requests.get(base_url, params=params)
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
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def convert_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d-%m-%y %H:%M:%S')

# Example usage
if __name__ == "__main__":
    klines = fetch_binance_klines()
    if klines:
        pprint(f"Total number of candlesticks: {len(klines)}")
        for kline in klines[:5]:  # Print the first 5 candlesticks
            pprint(kline)
