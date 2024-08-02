
import datetime

def convert_time(datetime_str):
    # Parse datetime string into a datetime object
    dt_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
  
    # Convert datetime to time in seconds since the UNIX epoch
    time_sec = dt_obj.timestamp()

    # Convert time in seconds to milliseconds
    time_ms = int(time_sec * 1000)
    
    return time_ms


print(convert_time(1722445020))