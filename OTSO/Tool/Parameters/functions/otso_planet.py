import time
import numpy as np
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.planet_params import *
from . import fortran_calls, readme_generators, misc


def OTSO_planet():

    LongitudeList = PlanetInputArray[0]
    LatitudeList = PlanetInputArray[1]
    RigidityArray = PlanetInputArray[2]
    DateArray = PlanetInputArray[3]
    Model = PlanetInputArray[4]
    IntModel = PlanetInputArray[5]
    ParticleArray = PlanetInputArray[6]
    IOPT = PlanetInputArray[7]
    WindArray = PlanetInputArray[8]
    Magnetopause = PlanetInputArray[9]
    FileDescriptors = PlanetInputArray[10]
    MaxStepPercent = ConeInputArray[10]/100
    EndParams = PlanetInputArray[12]
    Rcomp = PlanetInputArray[13]
    Rscan = PlanetInputArray[14]

    if not os.path.exists(FileDescriptors[1]):
        os.makedirs(FileDescriptors[1])

    ChildProcesses = []

    NewCoreNum = misc.CheckCoreNumPlanet(CoreNum)

    LongLists = np.array_split(LongitudeList, NewCoreNum)
    FileNames = []

    for list in LongLists:
     FileNames.append(str(list[0]) + "-" + str(list[-1]))
 
     Data = []
     i = 1
     for long,name in zip(LongLists, FileNames):
        Core = "Core " + str(i)
        Data.append([name,LatitudeList,long,Alt,0,0,Core])
        i = i + 1

    start = time.time()

    print("OTSO Planet Computation Started")
# Set the process creation method to 'forkserver'
    mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for RegionData in Data:
        Child = mp.Process(target=fortran_calls.fortrancallPlanet,  args=(RegionData, RigidityArray, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent, EndParams, Rcomp, Rscan))
        ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

    for b in ChildProcesses:
        b.join()

# Wait for child processes to complete

    while not ProcessQueue.empty():
        print(ProcessQueue.get())

    print("OTSO Planet Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")

    misc.PlanetFile(FileDescriptors[1])
    
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    readme_generators.READMEPlanet(Data, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, Printtime, LatStep, LongStep, MaxStepPercent*100, EndParams, Rcomp, Rscan)