import numpy as np
import time
import math
from scipy import constants
import MiddleMan as OTSOLib
from datetime import datetime, timedelta, date
import csv
from dateutil import parser 
import multiprocessing as mp
from multiprocessing import Process
import random
import os
import csv
import glob
import shutil
import pandas as pd
import psutil

class Cores:
   def __init__(self, Positions, CoreNum):
        self.CoreNum = CoreNum
        self.Positions = Positions
        self.CoreNames = []

        self.CheckCoreNum()
        self.CreateCoreList()
        self.SplitPositions()



   def CheckCoreNum(self):
           if(psutil.cpu_count(logical=False) < self.CoreNum):

              print("You have entered an invalid number of cores")
              print("You have " + str(psutil.cpu_count(logical=False)) + " and have tried to use " + str(self.CoreNum) + " cores")
              print("To ensure operational integrity of your computer OTSO will run using 2 less than the max cores available")

              self.CoreNum = mp.cpu_count() - 2

   def CreateCoreList(self):
         i = 1
         while i <= self.CoreNum:
          string = "Core " + str(i)
          self.CoreNames.append(string)
          i += 1

   def SplitPositions(self):
         self.PositionSplit = np.array_split(self.Positions, self.CoreNum)

   def getCoreList(self):
         return self.CoreNames

   def getPositions(self):
         return self.PositionSplit

class Stations:
 def __init__(self, Stations, Altitude, Zenith, Azimuth):
    self.StationList = np.array([])
    self.Stations = Stations
    self.Altitude = Altitude
    self.Zenith = Zenith
    self.Azimuth = Azimuth

    data = pd.read_csv("StationList.csv")
    data['Altitude'] = self.Altitude
    data['Zenith'] = self.Zenith
    data['Azimuth'] = self.Azimuth
    
    self.CreateList(data)


 def AddLocation(self, Name, Latitude, Longitude):
    NewStation = np.array([Name, Latitude, Longitude, self.Altitude, self.Zenith, self.Azimuth])
    self.StationList = np.vstack((self.StationList, NewStation))

 def CreateList(self, data):
    NewList = data[data["Name"].isin(self.Stations)]
    self.StationList = NewList.to_numpy()

 def GetStations(self):
    return self.StationList

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
    
class SolarWind:
 def __init__(self, Vx, Vy, Vz, By, Bz, Density, Dst, G1, G2, G3):
    self.Vx = Vx
    self.Vy = Vy
    self.Vz = Vz
    self.By = By
    self.Bz = Bz
    self.Density = Density
    self.Dst = Dst
    self.G1 = G1
    self.G2 = G2
    self.G3 = G3

    self.WindArray = np.array([self.Vx, self.Vy, self.Vz, self.By, self.Bz, self.Density, self.Dst, self.G1, self.G2, self.G3])

 def GetWind(self):
    return self.WindArray
    

def fortrancallCone(Data, Core, RigidityArray, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent):
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      NMname = Station

      StartRigidity = RigidityArray[0]
      EndRigidity = RigidityArray[1]
      RigidityStep = RigidityArray[2]

      FileName = NMname + FileGLE + ".csv"
      OTSOLib.cone(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent)
      print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return

def fortrancallTrajectory(Data, Core, Rigidity, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent):
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      NMname = Station

      FileName = NMname + FileGLE + ".csv"
      OTSOLib.trajectory(Position, Rigidity, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent)
      print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return

def fortrancallPlanet(Data, Rigidity, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent):

   final_directory = FileDescriptors[1]
   FileName = Data[0] + ".csv"

   f = open(FileName, 'w')
   writer = csv.writer(f)
   header = ['Latitude', 'Longitude', 'Ru', 'Rc', 'Rl']
   writer.writerow(header)
   f.close()


   for lon in(Data[2]):
      for lat in(Data[1]):

       Position = [Data[3],lat,lon,Data[4],Data[5]]
       Core = Data[6]
       OTSOLib.planet(Position, Rigidity, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, MaxStepPercent)
       now = datetime.now()
       CurrentTime = now.strftime("%H:%M:%S")
       print(CurrentTime)


   current_directory = os.getcwd()
   final_directory = os.path.join(current_directory, FileDescriptors[0])
   if not os.path.exists(final_directory):
      os.makedirs(final_directory)

   final_directory = os.path.join(final_directory, FileName)
   shutil.move(os.path.join(current_directory, FileName), final_directory)

def PlanetFile(final_directory):

 files = os.path.join(final_directory, "*.csv")
 files = glob.glob(files)
 df = pd.concat(map(pd.read_csv, files), ignore_index=True)
 os.makedirs(final_directory, exist_ok=True)  
 df.to_csv(final_directory + '/Planet.csv', index=False)

 for i in files:
   os.remove(i)    

def READMECone(UsedStationstemp, RigidityArray, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent):
      FileName = "OTSO_CONE_RUN_INFO.txt"
      file = open(FileName, "w")

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Output Coordinate System:"+ "\n")
      file.write(str(CoordinateSystem)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(UsedStationstemp[0][3]) + "km \n")
      file.write("Zenith = " + str(UsedStationstemp[0][4]) + "\n")
      file.write("Azimuth = " + str(UsedStationstemp[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("Start = " + str(RigidityArray[0]) + " [GV]"+ "\n")
      file.write("End = " + str(RigidityArray[1]) + " [GV]"+ "\n")
      file.write("Step = " + str(RigidityArray[2]) + " [GV]"+ "\n")
      file.write("\n")
      file.write("Stations:"+ "\n")

      for i in UsedStationstemp:
         file.write(str(i[0])+"," + " Latitude: " + str(i[1])+"," + " Longitude: " + str(i[2])+ "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return

def READMETrajectory(UsedStationstemp, Rigidity, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent):
      FileName = "OTSO_TRAJECTORY_RUN_INFO.txt"
      file = open(FileName, "w")

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Output Coordinate System:"+ "\n")
      file.write(str(CoordinateSystem)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(UsedStationstemp[0][3]) + "km \n")
      file.write("Zenith = " + str(UsedStationstemp[0][4]) + "\n")
      file.write("Azimuth = " + str(UsedStationstemp[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("R = " + str(Rigidity) + " [GV]"+ "\n")
      file.write("\n")
      file.write("Stations:"+ "\n")

      for i in UsedStationstemp:
         file.write(str(i[0])+"," + " Latitude: " + str(i[1])+"," + " Longitude: " + str(i[2])+ "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return

def READMEPlanet(Data, Rigidity, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, Printtime, LatStep, LongStep, MaxStepPercent):
      FileName = "OTSO_PLANET_RUN_INFO.txt"
      file = open(FileName, "w")

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(Data[0][3]) + "km \n")
      file.write("Zenith = " + str(Data[0][4]) + "\n")
      file.write("Azimuth = " + str(Data[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("R = " + str(Rigidity) + " [GV]"+ "\n")
      file.write("Latitude and Longitude Steps"+ "\n")
      file.write("Latitude = " + str(LatStep) + " degree steps" + "\n")
      file.write("Longitude = " + str(LongStep) + " degree steps" + "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return