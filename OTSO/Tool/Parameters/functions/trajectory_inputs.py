import numpy as np
from datetime import datetime
import os
from . import date, cores, solar_wind, stations
from . import misc, Request
from Parameters.trajectory_params import *

def TrajectoryInputs():
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    DateCreate = date.Date(EventDate)
    DateArray = DateCreate.GetDate()

    if LiveData == 1:
         misc.DateCheck(EventDate)
         DstLive, VxLive, DensityLive, ByLive, BzLive, IOPTLive, G1Live, G2Live, G3Live = Request.Get_Data(EventDate)
         PdynLive = misc.Pdyn_comp(Density,Vx)
         WindCreate = solar_wind.Solar_Wind(VxLive, Vy, Vz, ByLive, BzLive, DensityLive, PdynLive, DstLive, G1Live, G2Live, G3Live, W1, W2, W3, W4, W5, W6)
         WindArray = WindCreate.GetWind()
    else:
         WindCreate = solar_wind.Solar_Wind(Vx, Vy, Vz, By, Bz, Density, Pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6)
         WindArray = WindCreate.GetWind()

    MagFieldModel = np.array([Internal,External])

    EndParams = [MinAlt,MaxDist,MaxTime]

    CreateStations = stations.Stations(List, Alt, Zenith, Azimuth)
    InputtedStations = CreateStations
    if 'Custom_Locations' in locals() or 'Custom_Locations' in globals():
         CreateStations.AddLocation(Custom_Locations)
    Used_Stations_Temp = CreateStations.GetStations()
    temp = list(Used_Stations_Temp)
    Station_Array = temp


    current_directory = os.getcwd()
    result_directory = os.path.join(current_directory,"Results")
    final_directory = os.path.join(result_directory,FolderName)
    FileArray = [FileName, FolderName, final_directory]

    ParticleArray = [AtomicNum,AntiCheck]

    misc.ParamCheck(Alt,Year,Internal,EndParams)

    TrajectoryInputArray = [Rigidity,DateArray,MagFieldModel,IntModel,ParticleArray,IOPT,WindArray,Magnetopause,FileArray,CoordinateSystem,MaxStepPercent,EndParams, Station_Array, InputtedStations]

    return TrajectoryInputArray