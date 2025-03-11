import time
from datetime import datetime
import multiprocessing as mp
import os
from .. import *
from . import fortran_calls, readme_generators,cores, misc, planet_inputs
import pandas as pd
import sys
import queue
import random
import numpy as np


def OTSO_planet(startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           gyropercent,magnetopause,corenum, azimuth,zenith, asymptotic,asymlevels,unit,
           latstep,longstep,maxlat,minlat,maxlong,minlong,g,h):

    Anum = 1
    PlanetInputArray = planet_inputs.PlanetInputs(startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           gyropercent,magnetopause,corenum, azimuth,zenith, asymptotic,asymlevels,unit,
           latstep,longstep,maxlat,minlat,maxlong,minlong,g,h)

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
    MaxStepPercent = PlanetInputArray[10]/100
    EndParams = PlanetInputArray[11]
    Rcomp = PlanetInputArray[12]
    Rscan = PlanetInputArray[13]
    Zenith = PlanetInputArray[14]
    Azimuth = PlanetInputArray[15]
    CoreNum = PlanetInputArray[16]
    asymptotic = PlanetInputArray[17]
    asymlevels = PlanetInputArray[18]
    Alt = PlanetInputArray[19]
    LiveData = PlanetInputArray[20]
    AntiCheck = PlanetInputArray[21]
    g = PlanetInputArray[22]
    h = PlanetInputArray[23]

    ChildProcesses = []

    totalprocesses = len(LongitudeList)*len(LatitudeList)

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
        DataPlanet.append([name,point[0],point[1],Alt,Zenith,Azimuth,Core])
        i = i + 1

    shuffled_list = DataPlanet.copy()
    random.shuffle(shuffled_list)
    DataLists = np.array_split(shuffled_list, CoreNum)
    CoreList = np.arange(1, CoreNum + 1)
    start = time.time()

    print("OTSO Planet Computation Started")
    sys.stdout.write(f"\r{0:.2f}% complete")
# Set the process creation method to 'forkserver'
    try:
        if not mp.get_start_method(allow_none=True):
            mp.set_start_method('spawn')
    except RuntimeError:

        pass

# Create a shared message queue for the processes to produce/consume data
    ProcessQueue = mp.Manager().Queue()
    for Data,Core in zip(DataLists, CoreList):
            Child = mp.Process(target=fortran_calls.fortrancallPlanet,  args=(Data, RigidityArray, DateArray, Model, IntModel, 
                                                                              ParticleArray, IOPT, WindArray, 
                                                                              Magnetopause, MaxStepPercent, EndParams, 
                                                                              Rcomp, Rscan, asymptotic, asymlevels, unit,
                                                                              ProcessQueue,g,h))
            ChildProcesses.append(Child)

    for a in ChildProcesses:
        a.start()

    results = []
    processed = 0
    while processed < totalprocesses:
        try:
            # Collect all results available in the queue at this moment
            result_collector = []
            while True:
                try:
                    result_df = ProcessQueue.get_nowait()  # Non-blocking, does not wait
                    result_collector.append(result_df)
                    processed += 1
                except queue.Empty:
                    break
    
            # Append all collected results to the main results list
            results.extend(result_collector)
    
            # Calculate and print the progress
            percent_complete = (processed / totalprocesses) * 100
            sys.stdout.write(f"\r{percent_complete:.2f}% complete")
            sys.stdout.flush()
    
        except queue.Empty:
            # Queue is empty, but processes are still running, so we continue checking
            pass
        
        # Wait for 5 seconds before the next iteration
        time.sleep(2)

    for b in ChildProcesses:
        b.join()

    combined_planet = pd.concat(results, ignore_index=True)
    combined_planet['Longitude'] = pd.to_numeric(combined_planet['Longitude'])
    combined_planet['Latitude'] = pd.to_numeric(combined_planet['Latitude'])
    planet = combined_planet.sort_values(by=["Latitude", "Longitude"], ascending=[False, True]).reset_index(drop=True)

    print("\nOTSO Planet Computation Complete")
    stop = time.time()
    Printtime = round((stop-start),3)
    print("Whole Program Took: " + str(Printtime) + " seconds")
    
    EventDate = datetime(year,month,day,hour,minute,second)
    readme = readme_generators.READMEPlanet(Data, RigidityArray, EventDate, Model, IntModel, 
                                            AntiCheck, IOPT, WindArray, Magnetopause, Printtime,
                                            maxlat,maxlong,minlat,minlong, latstep, longstep,
                                            MaxStepPercent*100, EndParams, cutoff_comp, Rscan, 
                                            LiveData, asymptotic, asymlevels, unit, serverdata, kp)

    if LiveData == 1:
        misc.remove_files()

    return [planet, readme]