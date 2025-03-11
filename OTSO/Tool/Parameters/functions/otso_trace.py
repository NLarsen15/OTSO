import time
import numpy as np
from datetime import datetime
import multiprocessing as mp
import os
import random
import zipfile
from Parameters import *
from Parameters.trace_params import *
from . import fortran_calls, readme_generators, cores, misc

def OTSO_trace():

    TraceInputArray = trace_inputs.TraceInputs()

    Rigidity = TraceInputArray[0]
    DateArray = TraceInputArray[1]
    Model = TraceInputArray[2]
    IntModel = TraceInputArray[3]
    ParticleArray = TraceInputArray[4]
    IOPT = TraceInputArray[5]
    WindArray = TraceInputArray[6]
    Magnetopause = TraceInputArray[7]
    FileDescriptors = TraceInputArray[8]
    CoordinateSystem = TraceInputArray[9]
    MaxStepPercent = TraceInputArray[10]/100
    EndParams = TraceInputArray[11]
    Station_Array = TraceInputArray[12]
    InputtedStations = TraceInputArray[13]
    LongitudeList = TraceInputArray[14]
    LatitudeList = TraceInputArray[15]
    PlanetCheck = TraceInputArray[16]

    if not os.path.exists(FileDescriptors[2]):
        os.makedirs(FileDescriptors[2])

    ChildProcesses = []

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

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

    start = time.time()
    InputtedStations.find_non_matching_stations()

    print("OTSO Trace Computation Started")
    mp.set_start_method('spawn')
        # Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    if (PlanetCheck != 1):
        for Data,Core in zip(Positionlists,CoreList):
            Child = mp.Process(target=fortran_calls.fortrancallTrace,  args=(Data, Core, Rigidity, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams))
            ChildProcesses.append(Child)
    else:
        for Data,Core in zip(DataLists,CoreList):
            Child = mp.Process(target=fortran_calls.fortrancallTracePlanet,  args=(Data, Core, Rigidity, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams))
            ChildProcesses.append(Child)
        
    for a in ChildProcesses:
        a.start()
        
    for b in ChildProcesses:
        b.join()
        
        # Wait for child processes to complete
        
    while not ProcessQueue.empty():
        print(ProcessQueue.get())


    print("OTSO Trace Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")

    
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    readme_generators.READMETrace(Alt, EventDate, Model, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, LiveData)

    if LiveData == 1:
        misc.remove_folder('./Parameters/data_files')