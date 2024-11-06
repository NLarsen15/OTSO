import time
from datetime import datetime
import multiprocessing as mp
import os
from Parameters import *
from Parameters.flight_params import *
from . import fortran_calls, readme_generators, cores, misc

def OTSO_Flight():

    FlightInputArray = flight_inputs.FlightInputs()

    RigidityArray = FlightInputArray[0]
    DateArrayList = FlightInputArray[1]
    Model = FlightInputArray[2]
    IntModel = FlightInputArray[3]
    ParticleArray = FlightInputArray[4]
    IOPTList = FlightInputArray[5]
    WindArrayList = FlightInputArray[6]
    Magnetopause = FlightInputArray[7]
    FileDescriptorsList = FlightInputArray[8]
    CoordinateSystem = FlightInputArray[9]
    MaxStepPercent = FlightInputArray[10]/100
    EndParams = FlightInputArray[11]
    Station_Array = FlightInputArray[12]
    Rcomp = FlightInputArray[13]
    Rscan = FlightInputArray[14]

    mp.set_start_method('spawn')

    UsedCores = cores.Cores(Station_Array, CoreNum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()

    truestart = time.time()

    print("OTSO Flight Computation Started")
    start = time.time()
    ChildProcesses = []
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Queue()
    for Data, Core, Date, File, I, Wind in zip(Positionlists,CoreList,DateArrayList, FileDescriptorsList, IOPTList, WindArrayList):
        if not os.path.exists(File[2]):
         os.makedirs(File[2])
        Child = mp.Process(target=fortran_calls.fortrancallFlight,  args=(Data, Core, RigidityArray, Date, Model, IntModel, ParticleArray, I, Wind, Magnetopause, File, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan))
        ChildProcesses.append(Child)
    for a in ChildProcesses:
        a.start()
    for b in ChildProcesses:
        b.join()
    while not ProcessQueue.empty():
        print(ProcessQueue.get())

    print("OTSO Flight Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Compuation Took: " + str(Printtime) + " Seconds")
    month, day = misc.day_of_year_to_date(Date[1], Date[0])
    EventDate = datetime(int(Date[0]),int(month),int(day),int(Date[2]),int(Date[3]),int(Date[4]))
    LiveData = 0
    readme_generators.READMECutoff(Station_Array, RigidityArray, EventDate, Model, IntModel, AtomicNum, AntiCheck, I, Wind, Magnetopause, File, CoordinateSystem, Printtime, MaxStepPercent*100, EndParams, Rcomp, Rscan, LiveData)
    misc.FlightFile(File[2])
    misc.FlightCopy(FileDescriptorsList[0][2])
    finalstop = time.time()
    Printtime = round((finalstop-truestart),3)
    print("Whole Program Took: " + str(Printtime) + " Seconds")   