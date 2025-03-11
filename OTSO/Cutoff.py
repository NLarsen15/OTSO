from .Parameters.functions import otso_cutoff

def cutoff(Stations, customlocations=None, startaltitude=20,cutoff_comp="Vertical",minaltitude=20,maxdistance=100,maxtime=0,
           serverdata="OFF",livedata="OFF",vx=-500,vy=0,vz=0,by=5,bz=5,density=1,pdyn=0,Dst=0,
           G1=0,G2=0,G3=0,W1=0,W2=0,W3=0,W4=0,W5=0,W6=0,kp=0,Anum=1,anti="YES",year=2024,
           month=1,day=1,hour=12,minute=0,second=0,internalmag="IGRF",externalmag="TSY89",
           intmodel="Boris",startrigidity=20,endrigidity=0,rigiditystep=0.01,rigidityscan="ON",
           coordsystem="GEO",gyropercent=15,magnetopause="Kobel",corenum=1, azimuth=0, zenith=0, g=None,h=None):
    
    arguments = locals()
    for arg in arguments:
       if arguments[arg] is None:
          arguments[arg] = []

    cutoff = otso_cutoff.OTSO_cutoff(Stations,arguments["customlocations"],startaltitude,cutoff_comp,minaltitude,maxdistance,maxtime,
           serverdata,livedata,vx,vy,vz,by,bz,density,pdyn,Dst,
           G1,G2,G3,W1,W2,W3,W4,W5,W6,kp,Anum,anti,year,
           month,day,hour,minute,second,internalmag,externalmag,
           intmodel,startrigidity,endrigidity,rigiditystep,rigidityscan,
           coordsystem,gyropercent,magnetopause,corenum,azimuth,zenith,arguments["g"],arguments["h"])
    
    return cutoff