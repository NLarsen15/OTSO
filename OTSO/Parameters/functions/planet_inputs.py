import numpy as np
from datetime import datetime,timedelta
import os
from . import date, solar_wind, stations
from . import misc, Request, Server

def PlanetInputs(startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           gyropercent,magnetopause,corenum,azimuth,zenith, asymptotic,asymlevels,unit,
           latstep,longstep,maxlat,minlat,maxlong,minlong,g,h):
    
    EventDate = datetime(year,month,day,hour,minute,second)
    DateCreate = date.Date(EventDate)
    DateArray = DateCreate.GetDate()

    if unit not in ["GeV", "GV"]:
         print("Please enter a valid asymlevel unit: ""GeV"" or ""GV"" ")
         exit()

    if anti == "YES":
         AntiCheck = 1
    elif anti == "NO":
         AntiCheck = 0
    else:
         print("Please enter a valid anti value: ""YES"" or ""NO"" ")
         exit()

    if asymptotic not in ["YES","NO"]:
         print("Please enter a valid asymptotic value: ""YES"" or ""NO"" ")
         exit()

    if magnetopause == "Sphere":
         Magnetopause = 0
    elif magnetopause == "aFormisano":
         Magnetopause = 1
    elif magnetopause == "Sibeck":
         Magnetopause = 2
    elif magnetopause == "Kobel":
         Magnetopause = 3
    else:
         print("Please enter a valid magnetopause model: ""Sphere"", ""aFormisano"", ""Sibeck"", ""Kobel"" ")
         exit()


    if intmodel == "4RK":
         IntModel = 0
    elif intmodel == "Boris":
         IntModel = 1
    elif intmodel == "Vay":
         IntModel = 2
    elif intmodel == "HC":
         IntModel = 3
    else:
         print("Please enter a valid intmodel model: ""4RK"", ""Boris"", ""Vay"", ""HC"" ")
         exit()

    if cutoff_comp == "Vertical":
         CutoffComputation = 0
         Zenith = 0
         Azimuth = 0
    elif cutoff_comp == "Apparent":
         CutoffComputation = 1
         Zenith = 0
         Azimuth = 0
    elif cutoff_comp == "Custom":
         CutoffComputation = 0
         Zenith = zenith
         Azimuth = azimuth
    else:
         print("Please enter a valid cutoff_comp: ""Vertical"", ""Apparent"", or ""Custom"" ")
         exit()

    if serverdata == "ON":
         ServerData = 1
    elif serverdata == "OFF":
         ServerData = 0
    else:
         print("Please enter a valid serverdata value: ""ON"" or ""OFF"" ")
         exit()

    if livedata == "ON":
         LiveData = 1
    elif livedata == "OFF":
         LiveData = 0
    else:
         print("Please enter a valid livedata value: ""ON"" or ""OFF"" ")
         exit()
    
    if internalmag == "IGRF":
         Internal = 1
         if not g or not h: 
            g = [0] * 105
            h = [0] * 105
    elif internalmag == "Dipole":
         Internal = 2
         if not g or not h: 
            g = [0] * 105
            h = [0] * 105
    elif internalmag == "Custom Gauss":
         Internal = 4
         if not g or not h:
              print("Please enter values for the g and h Gaussian coefficients to use the Custom Gauss option")
              exit()
         elif len(g) != 105:
              print(f"There should be 105 g coefficents in the inputted list, you have entered {len(g)}")
              exit()
         elif len(h) != 105:
              print(f"There should be 105 h coefficents in the inputted list, you have enetered {len(h)}")
    else:
         print("Please enter a valid internalmag model: ""IGRF"",""Dipole"", or ""Custom Gauss""")
         exit()
      
    if externalmag == "NONE":
         External = 0
    elif externalmag == "TSY87short":
         External = 1
    elif externalmag == "TSY87long":
         External = 2
    elif externalmag == "TSY89":
         External = 3
    elif externalmag == "TSY96":
         External = 4
    elif externalmag == "TSY01":
         External = 5
    elif externalmag == "TSY01S":
         External = 6
    elif externalmag == "TSY04":
         External = 7
    else:
         print("Please enter a valid externalmag model: ""NONE"", ""TSY87short"",""TSy87long"",""TSY89"",""TSY96"",""TSY01"",""TSY01S"",""TSY04""")
         exit()

    
    if rigidityscan == "ON":
         Rscan = 1
    elif rigidityscan == "OFF":
         Rscan = 0
    else:
         print("Please enter a valid rigidityscan value: ""ON"" or ""OFF"" ")
         exit()


    misc.DataCheck(ServerData,LiveData,EventDate)

    IOPTinput = misc.IOPTprocess(kp)
    KpS = 0

    if ServerData == 1:
         if int(EventDate.year) > 1981:
              Server.DownloadServerFile(int(EventDate.year))
         elif int(EventDate.year) < 1981 and int(EventDate.year) > 1963:
              Server.DownloadServerFileLowRes(int(EventDate.year))
         else:
              print("Server data only valid for 1963 to present, please enter a valid date.")
         ByS, BzS, VS, DensityS, PdynS, KpS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S = Server.GetServerData(EventDate,External)
         IOPTinput = misc.IOPTprocess(KpS)
         WindCreate = solar_wind.Solar_Wind(VS, vy, vz, ByS, BzS, DensityS, PdynS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S)
         WindArray = WindCreate.GetWind()
         
    if LiveData == 1:
         misc.DateCheck(EventDate)
         DstLive, VxLive, DensityLive, ByLive, BzLive, IOPTLive, G1Live, G2Live, G3Live, KpLive = Request.Get_Data(EventDate)
         PdynLive = misc.Pdyn_comp(DensityLive,VxLive)
         IOPTinput = IOPTLive
         WindCreate = solar_wind.Solar_Wind(VxLive, vy, vz, ByLive, BzLive, DensityLive, PdynLive, DstLive, G1Live, G2Live, G3Live, W1, W2, W3, W4, W5, W6)
         WindArray = WindCreate.GetWind()

    if ServerData == 0 and LiveData == 0:
          if vx > 0:
               vx = -1*vx
          WindCreate = solar_wind.Solar_Wind(vx, vy, vz, by, bz, density, pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6)
          WindArray = WindCreate.GetWind()

    RigidityArray = [startrigidity,endrigidity,rigiditystep]

    MagFieldModel = np.array([Internal,External])

    EndParams = [minaltitude,maxdistance,maxtime]

    if latstep > 0:
         latstep = -1*latstep

    LatitudeList = np.arange(maxlat,minlat + latstep,latstep)
    LongitudeList = np.arange(minlong,maxlong + longstep,longstep)

    ParticleArray = [Anum,AntiCheck]

    misc.ParamCheck(startaltitude,year,Internal,EndParams)

    PlanetInputArray = [LongitudeList,LatitudeList,RigidityArray,DateArray,MagFieldModel,IntModel,ParticleArray,IOPTinput,WindArray,Magnetopause,gyropercent,EndParams, CutoffComputation, Rscan, Zenith, Azimuth, corenum, asymptotic, asymlevels, startaltitude, LiveData, AntiCheck, g, h]

    return PlanetInputArray