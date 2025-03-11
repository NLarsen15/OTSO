import numpy as np
from datetime import datetime, timedelta
import os
from Parameters.planet_params import *
from . import date, cores, solar_wind
from . import misc, Request, Server

def PlanetInputs():
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    DateCreate = date.Date(EventDate)
    DateArray = DateCreate.GetDate()

    misc.DataCheck(ServerData,LiveData,EventDate)

    IOPTinput = IOPT

    if ServerData == 1:
         Server.DownloadServerFile(int(EventDate.year))
         ByS, BzS, VS, DensityS, PdynS, KpS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S = Server.GetServerData(EventDate,External)
         IOPTinput = misc.IOPTprocess(KpS)
         WindCreate = solar_wind.Solar_Wind(VS, Vy, Vz, ByS, BzS, DensityS, PdynS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S)
         WindArray = WindCreate.GetWind()
         
    if LiveData == 1:
         misc.DateCheck(EventDate)
         DstLive, VxLive, DensityLive, ByLive, BzLive, IOPTLive, G1Live, G2Live, G3Live = Request.Get_Data(EventDate)
         PdynLive = misc.Pdyn_comp(Density,Vx)
         IOPTinput = IOPTLive
         WindCreate = solar_wind.Solar_Wind(VxLive, Vy, Vz, ByLive, BzLive, DensityLive, PdynLive, DstLive, G1Live, G2Live, G3Live, W1, W2, W3, W4, W5, W6)
         WindArray = WindCreate.GetWind()

    if ServerData == 0 and LiveData == 0:
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

    PlanetInputArray = [LongitudeList,LatitudeList,RigidityArray,DateArray,MagFieldModel,IntModel,ParticleArray,IOPTinput,WindArray,Magnetopause,FileArray,MaxStepPercent,EndParams, CutoffComputation, RigidityScan]

    return PlanetInputArray