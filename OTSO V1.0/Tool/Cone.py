import numpy as np
import time
import math
from scipy import constants
import MiddleMan as LarsenLib
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
from Classes import fortrancallCone
from Classes import READMECone
from Classes import ParamCheck
import os
import shutil


if __name__ == '__main__':
################################################################################################################
# Picking the stations to be tested.
# Additional stations can be added via the .AddLocation("Name",Latitude,Longitude) function
 List = ["Oulu"]
 Alt = 20
 Zenith = 0
 Azimuth = 0
 CreateStations = Stations(List, Alt, Zenith, Azimuth)

 UsedStationstemp = CreateStations.GetStations()

 temp = list(UsedStationstemp)
 UsedStations = random.shuffle(temp)
 UsedStations = temp

################################################################################################################
# Ending parameters
# Input the values for the minimum altitude and maximum distance travelled by a particle. If either condition is
# met then the computation is terminated and the trajectory is assumed forbidden. 
 MinAlt = 20 #[km]
 MaxDist = 100 #[Re]

 EndParams = [MinAlt, MaxDist]
################################################################################################################
# Solar Wind Conditions
 Vx = -500.0 #[km/s]
 Vy = 0.0 #[km/s]
 Vz = 0.0 #[km/s]
 By = 5 #[nT]
 Bz = -5 #[nT]
 Density = 1.0 #[cm^-2]
 Dst = 0 #[nT]

# G1 and G2 are only needed for TSY01 use (use external TSY01_Constants tool to calculate them)
# or enter the average solar wind speed, By, and Bz over the 1 hour period prior to event
 G1 = 0
 G2 = 0
 G3 = 0


 WindCreate = SolarWind(Vx, Vy, Vz, By, Bz, Density, Dst, G1, G2, G3)
 WindArray = WindCreate.GetWind()
################################################################################################################
# IOPT is picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
 IOPT = 5
###############################################################################################################
# Choose the atomic number of the particle you want to test e.g 0 = electron, 1 = proton, 2 = helium
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
# External: 0 = No External Field 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 
# 6 = TSY01(Storm) (Second Number in model Array)
 model = np.array([1,3])
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step
 StartRigidity = 20
 EndRigidity = 0
 RigidityStep = 0.001
 RigidityArray = [StartRigidity, EndRigidity, RigidityStep]
###############################################################################################################
# Pick the coordinate system desired for the output
# GDZ, GEO, GSM, GSE, SM, GEI, MAG, SPH (GEO in spherical), RLL 
 CoordinateSystem  = "GEO"
###############################################################################################################
# Pick the maximum percentage of the particle's gyrofrequency that can be used as the max time step in the
# computation
 MaxStepPercent = 0.015
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
 Magnetopause = 3
###############################################################################################################
# Choose the name of the folder that output files will be sent to. Folder created in the current directory
 FolderName = "Example Folder"
 FileName = "_Example_File"
 current_directory = os.getcwd()
 final_directory = os.path.join(current_directory, FolderName)
 if not os.path.exists(final_directory):
   os.makedirs(final_directory)

 FileDescriptors = [FileName, FolderName, final_directory]
###############################################################################################################
# Select the number of cores for multicore processing
 CoreNum = 1
 UsedCores = Cores(UsedStations, CoreNum)
 CoreList = UsedCores.getCoreList()
 Positionlists = UsedCores.getPositions()
 ChildProcesses = []
###############################################################################################################

 ParamCheck(Alt, EndParams)

 start = time.time()

 print("Parent Process started")
# Set the process creation method to 'forkserver'
 mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
 ProcessQueue    = mp.Queue()
 for Data,Core in zip(Positionlists,CoreList):
    Child = mp.Process(target=fortrancallCone,  args=(Data, Core, RigidityArray, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams))
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

 READMECone(UsedStationstemp, RigidityArray, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent, EndParams)
