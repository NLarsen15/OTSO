from .Parameters.functions import otso_flight

def flight(latitudes, longitudes, dates,altitudes,cutoff_comp="Vertical",minaltitude=20,maxdistance=100,maxtime=0,
           serverdata="OFF",livedata="OFF",vx=None,vy=None,vz=None,by=None,bz=None,density=None,pdyn=None,Dst=None,
           G1=None,G2=None,G3=None,W1=None,W2=None,W3=None,W4=None,W5=None,W6=None,kp=None,Anum=1,anti="YES",internalmag="IGRF",externalmag="TSY89",
           intmodel="Boris",startrigidity=20,endrigidity=0,rigiditystep=0.01,rigidityscan="ON",
           coordsystem="GEO",gyropercent=15,magnetopause="Kobel",corenum=1,azimuth=0,zenith=0,g=None,h=None,
           asymptotic="NO",asymlevels=[0.1,0.3,0.5,1,2,3,4,5,6,7,8,9,10,15,20,30,50,70,100,300,500,700,1000],
           unit="GeV"):
       
    arguments = locals()
    for arg in arguments:
         if arguments[arg] is None:
             arguments[arg] = []
    
    flight = otso_flight.OTSO_flight(latitudes, longitudes, dates, altitudes, cutoff_comp, minaltitude, maxdistance, maxtime,
             serverdata, livedata, arguments["vx"], arguments["vy"], arguments["vz"], arguments["by"], arguments["bz"], 
             arguments["density"], arguments["pdyn"], arguments["Dst"], arguments["G1"], arguments["G2"], arguments["G3"], 
             arguments["W1"], arguments["W2"], arguments["W3"], arguments["W4"], arguments["W5"], arguments["W6"], 
             arguments["kp"], Anum, anti, internalmag, externalmag, intmodel, startrigidity, endrigidity, rigiditystep, 
             rigidityscan, coordsystem, gyropercent, magnetopause, corenum, azimuth, zenith, arguments["g"], arguments["h"], 
             asymptotic, asymlevels, unit)

    
    return flight