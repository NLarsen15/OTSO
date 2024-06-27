import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.bulk_cutoff_params import *
from . import fortran_calls, readme_generators, cores, misc

def OTSO_cutoff_bulk():
    RigidityArray = BulkCutoffInputArraySpace[0]
    DateArrayList = BulkCutoffInputArraySpace[1]
    Model = BulkCutoffInputArraySpace[2]
    IntModel = BulkCutoffInputArraySpace[3]
    ParticleArray = BulkCutoffInputArraySpace[4]
    IOPTList = BulkCutoffInputArraySpace[5]
    WindArrayList = BulkCutoffInputArraySpace[6]
    Magnetopause = BulkCutoffInputArraySpace[7]
    FileDescriptorsList = BulkCutoffInputArraySpace[8]
    CoordinateSystem = BulkCutoffInputArraySpace[9]
    MaxStepPercent = BulkCutoffInputArraySpace[10]/100
    EndParams = BulkCutoffInputArraySpace[11]
    Station_Array = BulkCutoffInputArraySpace[12]
    InputtedStations = BulkCutoffInputArraySpace[13]
    Rcomp = BulkCutoffInputArraySpace[14]
    Rscan = BulkCutoffInputArraySpace[15]

    DateArrayGauss = BulkCutoffInputArrayGauss[1]
    IOPTGauss = BulkCutoffInputArrayGauss[5]
    WindGauss = BulkCutoffInputArrayGauss[6]
    FileDescriptorsListGauss = BulkCutoffInputArrayGauss[8]
    GaussCoeffs = BulkCutoffInputArrayGauss[16]

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
        # Create a shared message queue for the processes to produce/consume data
            print("OTSO Cutoff Computation Started")
            ProcessQueue = mp.Queue()
            for Data, Core in zip(Positionlists,CoreList):
                Child = mp.Process(target=fortran_calls.fortrancallCutoff,  args=(Data, Core, RigidityArray, Date, Model, IntModel, ParticleArray, I, Wind, Magnetopause, File, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan))
                ChildProcesses.append(Child)
            for a in ChildProcesses:
                a.start()
            for b in ChildProcesses:
                b.join()
            while not ProcessQueue.empty():
                print(ProcessQueue.get())


            print("OTSO Cutoff Computation Complete")
            stop = time.time()
            Printtime = round((stop-start),3)
            print("Compuation Took: " + str(Printtime) + " Seconds")
            month, day = misc.day_of_year_to_date(Date[1], Date[0])
            EventDate = datetime(int(Date[0]),int(month),int(day),int(Date[2]),int(Date[3]),int(Date[4]))
            readme_generators.READMECutoff(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, I, Wind, Magnetopause, File, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams, Rcomp, Rscan)
    elif Bulkcomp == 1:
        for File, Gauss in zip(FileDescriptorsListGauss, GaussCoeffs):
            start = time.time()
            ChildProcesses = []
            if not os.path.exists(File[2]):
                os.makedirs(File[2])
            print("OTSO Cutoff Computation Started")
            ProcessQueue = mp.Queue()
            for Data, Core in zip(Positionlists,CoreList):
                Child = mp.Process(target=fortran_calls.fortrancallCutoffGauss,  args=(Data, Core, RigidityArray, DateArrayGauss, Model, IntModel, ParticleArray, IOPTGauss, WindGauss, Magnetopause, File, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan, Gauss))
                ChildProcesses.append(Child)
            for a in ChildProcesses:
                a.start()
            for b in ChildProcesses:
                b.join()

            while not ProcessQueue.empty():
                print(ProcessQueue.get())


            print("OTSO Cutoff Computation Complete")
            stop = time.time()
            Printtime = round((stop-start),3)
            print("Compuation Took: " + str(Printtime) + " Seconds")

            month, day = misc.day_of_year_to_date(DateArrayGauss[1], DateArrayGauss[0])
            EventDate = datetime(int(DateArrayGauss[0]),int(month),int(day),int(DateArrayGauss[2]),int(DateArrayGauss[3]),int(DateArrayGauss[4]))
            readme_generators.READMECutoff(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPTGauss, WindGauss, Magnetopause, File, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams, Rcomp, Rscan)
    
    finalstop = time.time()
    Printtime = round((finalstop-truestart),3)
    print("Whole Program Took: " + str(Printtime) + " Seconds")   