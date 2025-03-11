import numpy as np
from datetime import datetime,timedelta
import os
from . import date, solar_wind, stations
from . import misc, Request, Server

def FlightInputs(latitudes,longitudes,dates,altitudes,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           coordsystem,gyropercent,magnetopause,corenum,azimuth,zenith,g,h,asymptotic,asymlevels,unit):
    
    DateArrayList = []
    for x in dates:
         DateCreate = date.Date(x)
         DateArray = DateCreate.GetDate()
         DateArrayList.append(DateArray)

    if unit not in ["GeV", "GV"]:
         print("Please enter a valid asymlevel unit: ""GeV"" or ""GV"" ")
         exit()

    if asymptotic not in ["YES","NO"]:
     print("Please enter a valid asymptotic value: ""YES"" or ""NO"" ")
     exit()

    if anti == "YES":
         AntiCheck = 1
    elif anti == "NO":
         AntiCheck = 0
    else:
         print("Please enter a valid anti value: ""YES"" or ""NO"" ")
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
    
    variablelist = [vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp]
    variablelist2 = [latitudes,longitudes,dates,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp]
    
    if serverdata == "OFF" and livedata == "OFF":
         if any(not lst for lst in variablelist):
              print("If not using livedata or server data you must provide full lists for the input variables\n"
              "vx,vy,vz,by,bz,density,pdyn,Dst,G1,G2,G3,W1,W2,W3,W4,W5,W6,kp")
              exit()
         if any(len(lst) != len(variablelist2[0]) for lst in variablelist2):
              print("If not using livedata or server data all provided variable lists must be the same length")
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

    if coordsystem not in ["GDZ","GEO","GSM","GSE","SM","GEI","MAG","SPH","RLL"]:
         print("Please select a valid coordsystem: ""GDZ"", ""GEO"", ""GSM"", ""GSE"", ""SM"", ""GEI"", ""MAG"", ""SPH"", ""RLL""")
         exit()

    
    if rigidityscan == "ON":
         Rscan = 1
    elif rigidityscan == "OFF":
         Rscan = 0
    else:
         print("Please enter a valid rigidityscan value: ""ON"" or ""OFF"" ")
         exit()

    #IOPTinput = misc.IOPTprocess(kp[0])
    #KpS = 0

    KpList = []


    WindArrayList = []
    IOPTList = []
    i = 0
    for x in dates:
         
       if ServerData == 1:
          if int(x.year) > 1981:
               Server.DownloadServerFile(int(x.year))
          elif int(x.year) < 1981 and int(x.year) > 1963:
               Server.DownloadServerFileLowRes(int(x.year))
          else:
               print("Server data only valid for 1963 to present, please enter a valid date.")
          ByS, BzS, VS, DensityS, PdynS, KpS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S = Server.GetServerData(x,External)
          KpList.append(KpS)
          IOPTinput = misc.IOPTprocess(KpS)
          IOPTList.append(IOPTinput)
          vytemp = 0
          vztemp = 0
          WindCreate = solar_wind.Solar_Wind(VS, vytemp, vztemp, ByS, BzS, DensityS, PdynS, DstS, G1S, G2S, G3S, W1S, W2S, W3S, W4S, W5S, W6S)
          WindArray = WindCreate.GetWind()
          WindArrayList.append(WindArray)
          
          if LiveData == 1:
               misc.DateCheck(x)
               DstLive, VxLive, DensityLive, ByLive, BzLive, IOPTLive, G1Live, G2Live, G3Live, KpLive = Request.Get_Data(x)
               PdynLive = misc.Pdyn_comp(DensityLive,VxLive)
               KpList.append(KpLive)
               IOPTinput = IOPTLive
               IOPTList.append(IOPTinput)
               vytemp = 0
               vztemp = 0
               WindCreate = solar_wind.Solar_Wind(VxLive, vytemp, vztemp, ByLive, BzLive, DensityLive, PdynLive, DstLive, G1Live, G2Live, G3Live, W1, W2, W3, W4, W5, W6)
               WindArray = WindCreate.GetWind()
               WindArrayList.append(WindArray)

       if ServerData == 0 and LiveData == 0:
          if vx[i] > 0:
               vx[i] = -1*vx[i]
          WindCreate = solar_wind.Solar_Wind(vx[i], vy[i], vz[i], by[i], bz[i], density[i], pdyn[i], Dst[i], G1[i], G2[i], G3[i], W1[i], W2[i], W3[i], W4[i], W5[i], W6[i])
          WindArray = WindCreate.GetWind()
          KpList.append(kp[i])
          IOPTinput = misc.IOPTprocess(kp[i])
          IOPTList.append(IOPTinput)
          WindArrayList.append(WindArray)
          i += 1

    RigidityArray = [startrigidity,endrigidity,rigiditystep]

    MagFieldModel = np.array([Internal,External])

    EndParams = [minaltitude,maxdistance,maxtime]
    
    stationslist = []
    for lat,long,alt in zip(latitudes,longitudes,altitudes):
         station = ["temp",lat,long,alt,Zenith,Azimuth]
         stationslist.append(station)
         misc.ParamCheck(alt,2000,Internal,EndParams)
         

    
    ParticleArray = [Anum,AntiCheck]

    FlightInputArray = [RigidityArray,DateArrayList,MagFieldModel,IntModel,ParticleArray,IOPTList,WindArrayList,Magnetopause,
    coordsystem,gyropercent,EndParams, stationslist, CutoffComputation, Rscan, KpList, corenum, LiveData, serverdata,g,h]

    return FlightInputArray