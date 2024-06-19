import numpy as np
from datetime import datetime
import os
from Parameters.planet_params import *
from . import date, cores, solar_wind
from . import misc

def PlanetInputs():
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    DateCreate = date.Date(EventDate)
    DateArray = DateCreate.GetDate()

    WindCreate = solar_wind.Solar_Wind(Vx, Vy, Vz, By, Bz, Density, Pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6)
    WindArray = WindCreate.GetWind()

    RigidityArray = [StartRigidity,EndRigidity,RigidityStep]

    MagFieldModel = np.array([Internal,External])

    EndParams = [MinAlt,MaxDist,MaxTime]

    Zenith = 0
    Azimuth = 0

    LatitudeList = np.arange(MaxLat,MinLat + LatStep,LatStep)
    LongitudeList = np.arange(MinLong,MaxLong + LongStep,LongStep)

    current_directory = os.getcwd()
    result_directory = os.path.join(current_directory,"Results")
    final_directory = os.path.join(result_directory,FolderName)
    FileArray = [FolderName, final_directory]

    ParticleArray = [AtomicNum,AntiCheck]

    misc.ParamCheck(Alt,Year,Internal,EndParams)

    PlanetInputArray = [LongitudeList,LatitudeList,RigidityArray,DateArray,MagFieldModel,IntModel,ParticleArray,IOPT,WindArray,Magnetopause,FileArray,MaxStepPercent,EndParams, CutoffComputation, RigidityScan]

    return PlanetInputArray