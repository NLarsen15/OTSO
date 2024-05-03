import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.trajectory_params import *
from . import fortran_calls, readme_generators, cores

def OTSO_trajectory():

    Rigidity = TrajectoryInputArray[0]
    DateArray = TrajectoryInputArray[1]
    Model = TrajectoryInputArray[2]
    IntModel = TrajectoryInputArray[3]
    ParticleArray = TrajectoryInputArray[4]
    IOPT = TrajectoryInputArray[5]
    WindArray = TrajectoryInputArray[6]
    Magnetopause = TrajectoryInputArray[7]
    FileDescriptors = TrajectoryInputArray[8]
    CoordinateSystem = TrajectoryInputArray[9]
    MaxStepPercent = TrajectoryInputArray[10]/100
    EndParams = TrajectoryInputArray[11]
    Station_Array = TrajectoryInputArray[12]
    InputtedStations = TrajectoryInputArray[13]

    if not os.path.exists(FileDescriptors[2]):
        os.makedirs(FileDescriptors[2])

    ChildProcesses = []

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

    start = time.time()
    InputtedStations.find_non_matching_stations()
    print("OTSO Trajectory Computation Started")

# Set the process creation method to 'forkserver'
    mp.set_start_method('spawn')
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for Data,Core in zip(Positionlists,CoreList):
        Child = mp.Process(target=fortran_calls.fortrancallTrajectory,  args=(Data, Core, Rigidity, DateArray, Model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams))
        ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

    for b in ChildProcesses:
        b.join()

# Wait for child processes to complete

    while not ProcessQueue.empty():
        print(ProcessQueue.get())

    print("OTSO Trajectory Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")

    
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    readme_generators.READMETrajectory(Station_Array, Rigidity, EventDate, Model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams)