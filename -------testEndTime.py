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
    return end_time_strptime.timestamp()
# Example usage
# if __name__ == "__main__":
#     interval_1s = '1s'
#     interval_1m = '1m'
#     interval_10m = '10m'

#     factor = 1000
#     # 1 m = 60 s  
#     # 16.66
#     # 1 h = 60 m 
#     # 1 h = 60*60 
#     # 1h = 3600s
#     end_time_1s = calculate_end_time(interval_1s, factor)
#     end_time_1m = calculate_end_time(interval_1m, factor)
#     end_time_10m = calculate_end_time(interval_10m, factor)

#     print(f"End time for {interval_1s} with factor {datetime.now()}: {end_time_1s}")
#     print(f"End time for {interval_1m} with factor {datetime.now()}: {end_time_1m}")
#     print(f"End time for {interval_10m} with factor {datetime.now()}: {end_time_10m}")



# Convert the datetime string to a datetime object
datetime_obj = datetime.now()

# Convert the datetime object to a Unix timestamp
unix_timestamp = int(datetime_obj.timestamp())

print(f"timestamp Now  '{datetime_obj}': {unix_timestamp}")


# Convert the timestamp to seconds
timestamp_s = unix_timestamp

# Convert the Unix timestamp to a datetime object
datetime_obj = datetime.fromtimestamp(timestamp_s)

# Print the datetime object
print(f"Datetime for timestamp '{timestamp_s}': {datetime_obj}")

def convert_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d/%m/%y %H:%M:%S')

print(f"'Time Convert ': {convert_timestamp(1722445320)}")
print(f"'Time Convert ': {convert_timestamp(1722445200)}")

