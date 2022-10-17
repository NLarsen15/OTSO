import numpy as np
import time
import math
from scipy import constants
import MiddleMan as OTSOLib
from datetime import datetime, timedelta
import csv
from dateutil import parser 
import multiprocessing as mp
from multiprocessing import Process
import random
from Classes import Stations
from Classes import SolarWind
from Classes import Date
from Classes import Cores
from Classes import fortrancallTrajectory
from Classes import READMETrajectory
import os
import shutil

if __name__ == '__main__':
################################################################################################################
# Picking the stations to be tested.
# Additional stations can be added via the .AddLocation("Name",Latitude,Longitude) function
 Alt_km = 20.0
 Zenith = 0.0
 Azimuth = 0.0

 List = ["Oulu"]
 Alt = 20.0
 Zenith = 0
 Azimuth = 0
 CreateStations = Stations(List, Alt, Zenith, Azimuth)
#CreateStations.AddLocation("New", 30, 30)

 UsedStationstemp = CreateStations.GetStations()

 temp = list(UsedStationstemp)
 UsedStations = random.shuffle(temp)
 UsedStations = temp

 Positions = np.array_split(UsedStations, 7)

################################################################################################################
# Solar Wind Conditions
 Vx = -1003 #[km/s]
 Vy = 0.0 #[km/s]
 Vz = 0.0 #[km/s]
 By = 16.369 #[nT]
 Bz = -19.679 #[nT]
 Density = 1.9 #[cm^-2]
 Dst = -253 #[nT]

# G1 and G2 are only needed for TSY01 use (use external TSY01_Constants tool to calculate them)
# or enter the average solar wind speed, By, and Bz over the 1 hour period prior to event
# G3 Used only in TSY01(Storm)
 G1 = 208.309
 G2 = 98.69018
 G3 = 18.7511


 WindCreate = SolarWind(Vx, Vy, Vz, By, Bz, Density, Dst, G1, G2, G3)
 WindArray = WindCreate.GetWind()
################################################################################################################
# IOPT is Picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
 IOPT = 5
###############################################################################################################
# Choose the atomic number of particle you want to test e.g 0 = electron, 1 = proton, 2 = helium
# Choose if you want to reverse the charge 0 = particle, 1 = anti-particle
 AtomicNum = 1
 AntiCheck = 1
################################################################################################################
# Enter date to be investigated as a datetime under EventDate
 EventDate = datetime(2006, 12, 13, 3, 00, 00)
 DateCreate = Date(EventDate)
 DateArray = DateCreate.GetDate()
###############################################################################################################
# Pick the magnetosphere models that you want to use. 
# Internal: 1 = IGRF, 2 = Dipole (First Number in model array)
# External: 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm) (Second Number in model Array)
 model = np.array([1,3])
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step
 Rigidity = 0.65
###############################################################################################################
# Pick the coordinate system desired for the output
# GDZ, GEO, GSM , GSE, SM, GEI, MAG, SPH (GEO in spherical), RLL 
 CoordinateSystem  = "GEO"
###############################################################################################################
# Pick the maximum percentage of the particles gyrofrequency that can be used as the max time step in the
# computation
 MaxStepPercent = 0.15
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
 Magnetopause = 3
###############################################################################################################
# Choose name of folder that output files will be sent to. Folder created in current directory
 FolderName = "Pause Test"
 FileName = "_Trajectory"
 current_directory = os.getcwd()
 final_directory = os.path.join(current_directory, FolderName)
 if not os.path.exists(final_directory):
   os.makedirs(final_directory)

 FileDescriptors = [FileName, FolderName, final_directory]
###############################################################################################################
# Select number of cores for multicore processing
 CoreNum = 3
 UsedCores = Cores(UsedStations, CoreNum)
 CoreList = UsedCores.getCoreList()
 Positionlists = UsedCores.getPositions()
 ChildProcesses = []
###############################################################################################################
 start = time.time()

 print("Parent Process started")
# Set the process creation method to 'forkserver'
 mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
 ProcessQueue    = mp.Queue()
 for Data,Core in zip(Positionlists,CoreList):
    Child = mp.Process(target=fortrancallTrajectory,  args=(Data, Core, Rigidity, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent))
    ChildProcesses.append(Child)

 for a in ChildProcesses:
    a.start()

 for b in ChildProcesses:
    b.join()

# Wait for child processes to complete

 while not ProcessQueue.empty():

    print(ProcessQueue.get())

 print("Parent Process Exiting")
 stop = time.time()
 Printtime = round((stop-start),3)
 print("Whole Program Took: " + str(Printtime) + " seconds")

 READMETrajectory(UsedStationstemp, Rigidity, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent)