import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.cone_params import *
from . import fortran_calls, readme_generators,cores,misc

def OTSO_cone():

    ConeInputArray = cone_inputs.ConeInputs()

    RigidityArray = ConeInputArray[0]
    DateArray = ConeInputArray[1]
    Model = ConeInputArray[2]
    IntModel = ConeInputArray[3]
    ParticleArray = ConeInputArray[4]
    IOPT = ConeInputArray[5]
    WindArray = ConeInputArray[6]
    Magnetopause = ConeInputArray[7]
    FileDescriptors = ConeInputArray[8]
    CoordinateSystem = ConeInputArray[9]
    MaxStepPercent = ConeInputArray[10]/100
    EndParams = ConeInputArray[11]
    Station_Array = ConeInputArray[12]
    InputtedStations = ConeInputArray[13]

    if not os.path.exists(FileDescriptors[2]):
        os.makedirs(FileDescriptors[2])

    ChildProcesses = []

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

    start = time.time()
    InputtedStations.find_non_matching_stations()
    print("OTSO Cone Computation Started")

# Set the process creation method to 'forkserver'
    mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for Data,Core in zip(Positionlists,CoreList):
        Child = mp.Process(target=fortran_calls.fortrancallCone,  args=(Data, Core, RigidityArray, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams))
        ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

    for b in ChildProcesses:
        b.join()

# Wait for child processes to complete

    while not ProcessQueue.empty():
        print(ProcessQueue.get())

    print("OTSO Cone Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")
    
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    readme_generators.READMECone(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams, LiveData)

    if LiveData == 1:
        misc.remove_folder('./Parameters/data_files')