import time
import numpy as np
from datetime import datetime
import multiprocessing as mp
import os
import random
from Parameters import *
from Parameters.planet_params import *
from . import fortran_calls, readme_generators, misc, cores


def OTSO_planet():

    PlanetInputArray = planet_inputs.PlanetInputs()

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
    MaxStepPercent = PlanetInputArray[11]/100
    EndParams = PlanetInputArray[12]
    Rcomp = PlanetInputArray[13]
    Rscan = PlanetInputArray[14]

    if not os.path.exists(FileDescriptors[1]):
        os.makedirs(FileDescriptors[1])

    ChildProcesses = []

    combined_coordinates = [(lat, lon) for lat in LatitudeList for lon in LongitudeList]

    NewCoreNum = misc.CheckCoreNumPlanet(CoreNum)
    FileNamesPlanet = []

    combined_coordinates = [(lat, lon) for lat in LatitudeList for lon in LongitudeList]
    for list in combined_coordinates:
        FileNamesPlanet.append(str(list[0]) + "_" + str(list[1]))
    DataPlanet = []
    i = 1
    for point,name in zip(combined_coordinates, FileNamesPlanet):
        Core = "Core " + str(i)
        DataPlanet.append([name,point[0],point[1],Alt,0,0,Core])
        i = i + 1

    shuffled_list = DataPlanet.copy()
    random.shuffle(shuffled_list)
    DataLists = np.array_split(shuffled_list, CoreNum)
    CoreList = np.arange(1, CoreNum + 1)
    start = time.time()

    print("OTSO Planet Computation Started")
# Set the process creation method to 'forkserver'
    mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for Data,Core in zip(DataLists, CoreList):
            Child = mp.Process(target=fortran_calls.fortrancallPlanet,  args=(Data, RigidityArray, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent, EndParams, Rcomp, Rscan))
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
    readme_generators.READMEPlanet(Data, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, Printtime, LatStep, LongStep, MaxStepPercent*100, EndParams, Rcomp, Rscan, LiveData)

    if LiveData == 1:
        misc.remove_folder('./Parameters/data_files')