import time
from datetime import datetime, timedelta, date
import numpy as np
import calendar

class Date:
 def __init__(self, Date):
    self.year = Date.year
    self.hour = Date.hour
    self.minute = Date.minute
    self.secs = Date.second
    self.seconds = timedelta(hours = Date.hour, minutes = Date.minute, seconds = Date.second).total_seconds()
    self.day = Date.timetuple().tm_yday

    self.DateArray = np.array([self.year, self.day, self.hour, self.minute, self.secs, self.seconds])

 def GetDate(self):
    return self.DateArray
 
def convert_to_datetime(date_list):
    year, day_of_year, hour, minute, second, seconds = date_list

    year = int(year)
    day_of_year = int(day_of_year)
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    
    # Automatically determine if it's a leap year
    is_leap_year = calendar.isleap(year)
    
    # Convert day_of_year to month and day
    month, day = day_of_year_to_date(day_of_year, is_leap_year)
    
    # Create the date from the year, month, and day
    date = datetime(year, month, day)
    
    # Create a timedelta for the time portion
    time_delta = timedelta(hours=hour, minutes=minute, seconds=second)
    
    # Add the time to the date
    full_datetime = date + time_delta
    return full_datetime

# Function to convert day_of_year to month and day
def day_of_year_to_date(day_of_year, is_leap_year=False):
    months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if is_leap_year:
        months_days[1] = 29
    
    month = 0
    while day_of_year > months_days[month]:
        day_of_year -= months_days[month]
        month += 1
    
    return month + 1, day_of_year