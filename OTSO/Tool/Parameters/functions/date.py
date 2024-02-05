import time
from datetime import datetime, timedelta, date
import numpy as np

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