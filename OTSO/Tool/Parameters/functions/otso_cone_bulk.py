import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.bulk_cone_params import *
from . import fortran_calls, readme_generators, cores, misc

def OTSO_cone_bulk():

    BulkConeInputArraySpace, BulkConeInputArrayGauss = bulk_cone_inputs.BulkConeInputs()

    RigidityArray = BulkConeInputArraySpace[0]
    DateArrayList = BulkConeInputArraySpace[1]
    Model = BulkConeInputArraySpace[2]
    IntModel = BulkConeInputArraySpace[3]
    ParticleArray = BulkConeInputArraySpace[4]
    IOPTList = BulkConeInputArraySpace[5]
    WindArrayList = BulkConeInputArraySpace[6]
    Magnetopause = BulkConeInputArraySpace[7]
    FileDescriptorsList = BulkConeInputArraySpace[8]
    CoordinateSystem = BulkConeInputArraySpace[9]
    MaxStepPercent = BulkConeInputArraySpace[10]/100
    EndParams = BulkConeInputArraySpace[11]
    Station_Array = BulkConeInputArraySpace[12]
    InputtedStations = BulkConeInputArraySpace[13]

    DateArrayGauss = BulkConeInputArrayGauss[1]
    IOPTGauss = BulkConeInputArrayGauss[5]
    WindGauss = BulkConeInputArrayGauss[6]
    FileDescriptorsListGauss = BulkConeInputArrayGauss[8]
    GaussCoeffs = BulkConeInputArrayGauss[14]

    mp.set_start_method('spawn')

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

    truestart = time.time()
    InputtedStations.find_non_matching_stations()

    if Bulkcomp == 0:
        for Date, File, I, Wind in zip(DateArrayList, FileDescriptorsList, IOPTList, WindArrayList):
            start = time.time()
            ChildProcesses = []
            if not os.path.exists(File[2]):
                os.makedirs(File[2])
            print("OTSO Cone Computation Started")
            ProcessQueue = mp.Queue()
            for Data,Core in zip(Positionlists,CoreList):
                Child = mp.Process(target=fortran_calls.fortrancallCone,  args=(Data, Core, RigidityArray, Date, Model, IntModel, ParticleArray, I, Wind, Magnetopause, File, CoordinateSystem, MaxStepPercent, EndParams))
                ChildProcesses.append(Child)
            for a in ChildProcesses:
                a.start()
            for b in ChildProcesses:
                b.join()
            while not ProcessQueue.empty():
                print(ProcessQueue.get())
        
            print("OTSO Cone Computation Complete")
            stop = time.time()
            Printtime = round((stop-start),3)
            print("Computation Took: " + str(Printtime) + " Seconds")

            month, day = misc.day_of_year_to_date(Date[1], Date[0])
            EventDate = datetime(int(Date[0]),int(month),int(day),int(Date[2]),int(Date[3]),int(Date[4]))
            readme_generators.READMECone(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, I, Wind, Magnetopause, File, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams)
    elif Bulkcomp == 1:
        for File, Gauss in zip(FileDescriptorsListGauss, GaussCoeffs):
            start = time.time()
            ChildProcesses = []
            if not os.path.exists(File[2]):
                os.makedirs(File[2])
            print("OTSO Cone Computation Started")
            ProcessQueue = mp.Queue()
            for Data,Core in zip(Positionlists,CoreList):
                Child = mp.Process(target=fortran_calls.fortrancallConeGauss,  args=(Data, Core, RigidityArray, DateArrayGauss, Model, IntModel, ParticleArray, IOPTGauss, WindGauss, Magnetopause, File, CoordinateSystem, MaxStepPercent, EndParams, Gauss))
                ChildProcesses.append(Child)
            for a in ChildProcesses:
                a.start()
            for b in ChildProcesses:
                b.join()
            while not ProcessQueue.empty():
                print(ProcessQueue.get())

            print("OTSO Cone Computation Complete")
            stop = time.time()
            Printtime = round((stop-start),3)
            print("Computation Took: " + str(Printtime) + " Seconds")

            month, day = misc.day_of_year_to_date(DateArrayGauss[1], DateArrayGauss[0])
            EventDate = datetime(int(DateArrayGauss[0]),int(month),int(day),int(DateArrayGauss[2]),int(DateArrayGauss[3]),int(DateArrayGauss[4]))
            readme_generators.READMECone(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPTGauss, WindGauss, Magnetopause, File, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams)

    finalstop = time.time()
    Printtime = round((finalstop-truestart),3)
    print("Whole Program Took: " + str(Printtime) + " Seconds")   