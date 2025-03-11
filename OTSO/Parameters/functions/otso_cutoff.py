import time
from datetime import datetime
import multiprocessing as mp
import os
from .. import *
from . import fortran_calls, readme_generators,cores, misc, cutoff_inputs
import pandas as pd
import sys
import queue

def OTSO_cutoff(Stations,customlocations,startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           coordsystem,gyropercent,magnetopause,corenum,azimuth,zenith,g,h):

    CutoffInputArray = cutoff_inputs.CutoffInputs(Stations,customlocations,startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           coordsystem,gyropercent,magnetopause,corenum,azimuth,zenith,g,h)

    RigidityArray = CutoffInputArray[0]
    DateArray = CutoffInputArray[1]
    Model = CutoffInputArray[2]
    IntModel = CutoffInputArray[3]
    ParticleArray = CutoffInputArray[4]
    IOPT = CutoffInputArray[5]
    WindArray = CutoffInputArray[6]
    Magnetopause = CutoffInputArray[7]
    CoordinateSystem = CutoffInputArray[8]
    MaxStepPercent = CutoffInputArray[9]/100
    EndParams = CutoffInputArray[10]
    Station_Array = CutoffInputArray[11]
    InputtedStations = CutoffInputArray[12]
    Rcomp = CutoffInputArray[13]
    Rscan = CutoffInputArray[14]
    Kp = CutoffInputArray[15]
    corenum = CutoffInputArray[16]
    LiveData = CutoffInputArray[17]
    g = CutoffInputArray[18]
    h = CutoffInputArray[19]

    AntiCheck = ParticleArray[1]

    ChildProcesses = []

    UsedCores = cores.Cores(Station_Array, corenum)
    CoreList = UsedCores.getCoreList()
    Positionlists = UsedCores.getPositions()
    InputtedStations.find_non_matching_stations()

    print("OTSO Cutoff Computation Started")
    start = time.time()
    sys.stdout.write(f"\r{0:.2f}% complete")

# Set the process creation method to 'forkserver'
    try:
        # Check if the start method is already set
        if not mp.get_start_method(allow_none=True):
            mp.set_start_method('spawn')
    except RuntimeError:
        # If the start method is already set, a RuntimeError will be raised
        # You can log or handle this as needed
        pass
# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Manager().Queue()
    for Data,Core in zip(Positionlists,CoreList):
        Child = mp.Process(target=fortran_calls.fortrancallCutoff,  args=(Data, Core, RigidityArray, DateArray, Model, IntModel, ParticleArray, IOPT,
         WindArray, Magnetopause, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan, Kp, ProcessQueue, g, h))
        ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

# Wait for child processes to complete

    total_stations = len(Station_Array)
    processed = 0
    results = []

    while processed < total_stations:
      try:
        # Check if the ProcessQueue has any new results
        result_df = ProcessQueue.get(timeout=0.001)  # Use timeout to avoid blocking forever
        results.append(result_df)
        processed += 1

        # Calculate and print the progress
        percent_complete = (processed / total_stations) * 100
        sys.stdout.write(f"\r{percent_complete:.2f}% complete")
        sys.stdout.flush()

      except queue.Empty:
        # Queue is empty, but processes are still running, so we continue checking
        pass
      
      time.sleep(1)

    # Ensure that all processes have completed
    for b in ChildProcesses:
        b.join()


    # Concatenate the results on the index
    merged_df = pd.concat(results, axis=1)
    merged_df = merged_df.sort_index(axis=1)

    print("\nOTSO Cone Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")
    
    EventDate = datetime(year,month,day,hour,minute,second)
    README = readme_generators.READMECutoff(Station_Array, RigidityArray, EventDate, Model, IntModel, Anum, AntiCheck, IOPT, WindArray, Magnetopause, 
                                            CoordinateSystem, Printtime, MaxStepPercent*100, EndParams, cutoff_comp, Rscan, LiveData, serverdata, kp)
    
    if livedata == 1:
        misc.remove_files()

    return [merged_df, README]