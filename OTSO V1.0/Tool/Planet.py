import numpy as np
import pandas as pd
import time
import math
import glob
from scipy import constants
#import MiddleMan as LarsenLib
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
from Classes import fortrancallPlanet
from Classes import READMEPlanet
from Classes import PlanetFile
import os
import shutil



if __name__ == '__main__':
################################################################################################################
# Select the step size that will be taken in longitude and latitude across the entire globe
 LatStep = -5
 LongStep = 5

 LatitudeList = np.arange(90.0,-90.0 + LatStep,LatStep)
 LongitudeList = np.arange(0,360 + LongStep,LongStep)
################################################################################################################
# Starting conditions for the simulations
 Alt = 20.0
 Zenith = 0
 Azimuth = 0
################################################################################################################
# Select the number of cores that the computation will be preformed over
 CoreNum = 3

 LongLists = np.array_split(LongitudeList, CoreNum)
 FileNames = []

 for list in LongLists:
     FileNames.append(str(list[0]) + "-" + str(list[-1]))

 Data = []
 i = 1
 for long,name in zip(LongLists, FileNames):
     Core = "Core " + str(i)
     Data.append([name,LatitudeList,long,Alt,Zenith,Azimuth,Core])
     i = i + 1

 ChildProcesses = []
################################################################################################################
# Solar Wind Conditions
 Vx = -400.0616 #[km/s]
 Vy = 0.0 #[km/s]
 Vz = 0.0 #[km/s]
 By = 3.5541 #[nT]
 Bz = -0.3016 #[nT]
 Density = 3.6005 #[cm^-2]
 Dst = -33 #[nT]

# G1 and G2 are only needed for TSY01 use (use external TSY01_Constants tool to calculate them)
# or enter the average solar wind speed, By, and Bz over the 1 hour period prior to event
 G1 = -0.43939
 G2 = 2.48525
 G3 = 0

 WindCreate = SolarWind(Vx, Vy, Vz, By, Bz, Density, Dst, G1, G2, G3)
 WindArray = WindCreate.GetWind()
################################################################################################################
# IOPT is Picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
 IOPT = 5
################################################################################################################
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
# Internal: 1=IGRF, 2=Dipole (First Number in model array)
# External: 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01 (Second Number in model Array)
 model = np.array([1,3])
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step
 StartRigidity = 20
 EndRigidity = 0
 RigidityStep = 1
 RigidityArray = [StartRigidity, EndRigidity, RigidityStep]
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
 FolderName = "Planet1"
 current_directory = os.getcwd()
 final_directory = os.path.join(current_directory, FolderName)
 if not os.path.exists(final_directory):
  os.makedirs(final_directory)

 FileDescriptors = [FolderName, final_directory]
###############################################################################################################


 start = time.time()

 print("Parent Process started")
# Set the process creation method to 'forkserver'
 mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
 ProcessQueue    = mp.Queue()
 for RegionData in Data:
     Child = mp.Process(target=fortrancallPlanet,  args=(RegionData, RigidityArray, DateArray, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent))
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

 PlanetFile(final_directory)

 READMEPlanet(Data, RigidityArray, EventDate, model, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, Printtime, LatStep, LongStep, MaxStepPercent)