import time
import numpy as np
from datetime import datetime
import multiprocessing as mp
import os
import random
from Parameters import *
from Parameters.bulk_planet_params import *
from . import fortran_calls, readme_generators, misc, cores


def OTSO_planet_bulk():

    BulkPlanetInputArraySpace, BulkPlanetInputArrayGauss = bulk_planet_inputs.BulkPlanetInputs()

    LongitudeList = BulkPlanetInputArraySpace[0]
    LatitudeList = BulkPlanetInputArraySpace[1]
    RigidityArray = BulkPlanetInputArraySpace[2]
    DateArrayList = BulkPlanetInputArraySpace[3]
    Model = BulkPlanetInputArraySpace[4]
    IntModel = BulkPlanetInputArraySpace[5]
    ParticleArray = BulkPlanetInputArraySpace[6]
    IOPTList = BulkPlanetInputArraySpace[7]
    WindArrayList = BulkPlanetInputArraySpace[8]
    Magnetopause = BulkPlanetInputArraySpace[9]
    FileDescriptorsList = BulkPlanetInputArraySpace[10]
    MaxStepPercent = BulkPlanetInputArraySpace[11]/100
    EndParams = BulkPlanetInputArraySpace[12]
    Rcomp = BulkPlanetInputArraySpace[13]
    Rscan = BulkPlanetInputArraySpace[14]

    DateArrayGauss = BulkPlanetInputArrayGauss[3]
    IOPTGauss = BulkPlanetInputArrayGauss[7]
    WindGauss = BulkPlanetInputArrayGauss[8]
    FileDescriptorsListGauss = BulkPlanetInputArrayGauss[10]
    GaussCoeffs = BulkPlanetInputArrayGauss[15]

    mp.set_start_method('spawn')

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
    truestart = time.time()

    if Bulkcomp == 0:
        for Date, File, I, Wind in zip(DateArrayList, FileDescriptorsList, IOPTList, WindArrayList):
            start = time.time()
            ChildProcesses = []
            if not os.path.exists(File[1]):
                os.makedirs(File[1])
    
            print("OTSO Planet Computation Started")
        # Create a shared message queue for the processes to produce/consume data
            ProcessQueue = mp.Queue()
            for Data,Core in zip(DataLists, CoreList):
                    Child = mp.Process(target=fortran_calls.fortrancallPlanet,  args=(Data, RigidityArray, Date, Model, IntModel, ParticleArray, I, Wind, Magnetopause, File, MaxStepPercent, EndParams, Rcomp, Rscan))
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
            print("Compuation Took: " + str(Printtime) + " Seconds")
            misc.PlanetFile(File[1])
    
            month, day = misc.day_of_year_to_date(Date[1], Date[0])
            
            EventDate = datetime(int(Date[0]),int(month),int(day),int(Date[2]),int(Date[3]),int(Date[4]))
            LiveData = 0
            readme_generators.READMEPlanet(Data, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, I, Wind, Magnetopause, File, Printtime, LatStep, LongStep, MaxStepPercent*100, EndParams, Rcomp, Rscan, LiveData)
    elif Bulkcomp == 1:
            for File, Gauss in zip(FileDescriptorsListGauss, GaussCoeffs):
                start = time.time()
                ChildProcesses = []
                if not os.path.exists(File[1]):
                    os.makedirs(File[1])
        
                print("OTSO Planet Computation Started")
            # Create a shared message queue for the processes to produce/consume data
                ProcessQueue = mp.Queue()
                for Data,Core in zip(DataLists, CoreList):
                        Child = mp.Process(target=fortran_calls.fortrancallPlanetGauss,  args=(Data, RigidityArray, DateArrayGauss, Model, IntModel, ParticleArray, IOPTGauss, WindGauss, Magnetopause, File, MaxStepPercent, EndParams, Rcomp, Rscan, Gauss))
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
                print("Computation Took: " + str(Printtime) + " Seconds")
                misc.PlanetFile(File[1])
        
                month, day = misc.day_of_year_to_date(DateArrayGauss[1], DateArrayGauss[0])
                LiveData = 0
                EventDate = datetime(int(DateArrayGauss[0]),int(month),int(day),int(DateArrayGauss[2]),int(DateArrayGauss[3]),int(DateArrayGauss[4]))
                readme_generators.READMEPlanet(Data, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPTGauss, WindGauss, Magnetopause, File, Printtime, LatStep, LongStep, MaxStepPercent*100, EndParams, Rcomp, Rscan, LiveData)

    finalstop = time.time()
    Printtime = round((finalstop-truestart),3)
    print("Whole Program Took: " + str(Printtime) + " Seconds")            