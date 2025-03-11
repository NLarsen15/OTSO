import numpy as np
import pandas as pd
import os

class Stations:
 def __init__(self, Stations, Altitude, Zenith, Azimuth):
    self.StationList = np.array([])
    self.Stations = Stations
    self.Altitude = Altitude
    self.Zenith = Zenith
    self.Azimuth = Azimuth
   
    script_dir = os.path.dirname(os.path.realpath(__file__))
    subfolder_name = ''
    csv_file_name = 'StationList.csv'

    csv_file_path = os.path.join(script_dir, subfolder_name, csv_file_name)
    data = pd.read_csv(csv_file_path)
    data['Altitude'] = self.Altitude
    data['Zenith'] = self.Zenith
    data['Azimuth'] = self.Azimuth
    
    self.df_stations = data

    self.CreateList(data)


 def AddLocation(self, CustomList):
    
    for x in CustomList:
       NewStation = np.array([x[0], x[1], x[2], self.Altitude, self.Zenith, self.Azimuth])
       self.StationList = np.vstack((self.StationList, NewStation))

 def AddLocationFlight(self, CustomList, alt):
    
    for x in CustomList:
       NewStation = np.array([x[0], x[1], x[2], alt, self.Zenith, self.Azimuth])
       self.StationList = np.vstack((self.StationList, NewStation))

 def CreateList(self, data):
    NewList = data[data["Name"].isin(self.Stations)]
    self.StationList = NewList.to_numpy()

 def GetStations(self):
    return self.StationList
 
 def find_non_matching_stations(self):
    csv_stations = self.df_stations['Name'].tolist()
    non_matching_stations = [name for name in self.Stations if name not in csv_stations]
    
    if len(non_matching_stations) > 0:
      print("ERROR: The following stations were not found in the StationList.csv file:")
      for x in non_matching_stations:
         print(x)
      print("Computations for these stations could not be conducted\n\
      To Fix:\n\
            Double check spelling\n\
            Add the station to the StationList.csv within the Parameters/functions folder\n\
            Manually add the station using customlocations folder\n", sep='\n') 
      