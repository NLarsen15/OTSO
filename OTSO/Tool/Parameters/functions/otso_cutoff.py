import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.cutoff_params import *
from . import fortran_calls, readme_generators,cores

def OTSO_cutoff():
    RigidityArray = CutoffInputArray[0]
    DateArray = CutoffInputArray[1]
    Model = CutoffInputArray[2]
    IntModel = CutoffInputArray[3]
    ParticleArray = CutoffInputArray[4]
    IOPT = CutoffInputArray[5]
    WindArray = CutoffInputArray[6]
    Magnetopause = CutoffInputArray[7]
    FileDescriptors = CutoffInputArray[8]
    CoordinateSystem = CutoffInputArray[9]
    MaxStepPercent = CutoffInputArray[10]
    EndParams = CutoffInputArray[11]
    Station_Array = CutoffInputArray[12]
    InputtedStations = CutoffInputArray[13]
    Rcomp = CutoffInputArray[14]
    Rscan = CutoffInputArray[15]


    if not os.path.exists(FileDescriptors[2]):
        os.makedirs(FileDescriptors[2])

    ChildProcesses = []

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

    start = time.time()
    InputtedStations.find_non_matching_stations()
    print("OTSO Cutoff Computation Started")

# Set the process creation method to 'forkserver'
    mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for Data,Core in zip(Positionlists,CoreList):
        Child = mp.Process(target=fortran_calls.fortrancallCutoff,  args=(Data, Core, RigidityArray, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan))
        ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

    for b in ChildProcesses:
        b.join()

# Wait for child processes to complete

    while not ProcessQueue.empty():
        print(ProcessQueue.get())

    print("OTSO Cutoff Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")
    
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    readme_generators.READMECutoff(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent, EndParams, Rcomp, Rscan)