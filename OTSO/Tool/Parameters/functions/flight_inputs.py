import numpy as np
from datetime import datetime
import os
import pandas as pd
from Parameters.flight_params import *
from . import date, cores, solar_wind, stations
from . import misc

def FlightInputs():

    FileName = ""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_pathflight = os.path.join(parent_dir, 'Flight_Params.csv')
    dfflight = pd.read_csv(file_pathflight)

    dfflight['Time'] = pd.to_datetime(dfflight['Time'], format='%d/%m/%Y %H:%M:%S')
    dfflight['Converted'] = dfflight['Time'].dt.strftime('%d-%m-%Y %H-%M-%S')

    TimeString = dfflight['Converted'].tolist()

    dfflight['Year'] = dfflight['Time'].dt.year
    dfflight['Month'] = dfflight['Time'].dt.month
    dfflight['Day'] = dfflight['Time'].dt.day
    dfflight['Hour'] = dfflight['Time'].dt.hour
    dfflight['Minute'] = dfflight['Time'].dt.minute
    dfflight['Second'] = dfflight['Time'].dt.second

    Dateresults = dfflight.apply(lambda row: Dateprocess(row['Year'], row['Month'], row['Day'], row['Hour'], row['Minute'], row['Second']), axis=1)
    DateArrayList = Dateresults.tolist()

    WindResults = dfflight.apply(lambda row: Windprocess(row['Vx'], row['Vy'], row['Vz'], row['By'], row['Bz'], row['Density'], row['Pdyn'], row['Dst'], row['G1'], row['G2'], 
                                                    row['G3'], row['W1'], row['W2'], row['W3'], row['W4'], row['W5'], row['W6']), axis=1)
    WindArrayList = WindResults.tolist()

    IOPTResults = dfflight.apply(lambda row: IOPTprocess(row['Kp']), axis=1)
    IOPTList = IOPTResults.tolist()

    RigidityArray = [StartRigidity,EndRigidity,RigidityStep]

    MagFieldModel = np.array([Internal,External])

    EndParams = [MinAlt,MaxDist,MaxTime]

    Zenith = 0
    Azimuth = 0

    stat = stations.Stations([[]], 0, 0, 0)
    LocationArray = dfflight.apply(lambda row: Pathprocess(row['altitude'],row['latitude'],row['longitude'],row['Converted'],stat), axis=1)
    Used_Stations_Temp = stat.GetStations()
    temp = list(Used_Stations_Temp)
    LocationArray = temp   
    FileArrayList = Fileprocess(TimeString, FileName)

    ParticleArray = [AtomicNum,AntiCheck]

    FlightInputArray = [RigidityArray,DateArrayList,MagFieldModel,IntModel,ParticleArray,IOPTList,WindArrayList,Magnetopause,FileArrayList,CoordinateSystem,MaxStepPercent,EndParams, LocationArray, CutoffComputation,  RigidityScan]
    return FlightInputArray

def Dateprocess(Year, Month, Day, Hour, Minute, Second):
    EventDate = datetime(Year,Month,Day,Hour,Minute,Second)
    DateCreate = date.Date(EventDate)
    DateArray = DateCreate.GetDate()

    return DateArray

def Windprocess(Vx, Vy, Vz, By, Bz, Density, Pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6):

    WindCreate = solar_wind.Solar_Wind(Vx, Vy, Vz, By, Bz, Density, Pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6)
    WindArray = WindCreate.GetWind()

    return WindArray

def IOPTprocess(Kp):
    if Kp >= 6:
        IOPT = 7
    else:
        IOPT = Kp + 1

    return IOPT

def Fileprocess(FileStringList, FileName):

    FileArrayList = []

    for string in FileStringList:
        current_directory = os.getcwd()
        result_directory = os.path.join(current_directory,"Results")
        FolderNameFinal = FolderName
        final_directory = os.path.join(result_directory,FolderNameFinal)
        FileArray = [FileName, FolderNameFinal, final_directory]
        FileArrayList.append(FileArray)

    return FileArrayList 

def FileprocessGauss(FileGaussStringList, FileName):

    FileGaussArrayList = []

    for string in FileGaussStringList:
        current_directory = os.getcwd()
        result_directory = os.path.join(current_directory,"Results")
        FolderNameFinal = FolderName
        final_directory = os.path.join(result_directory,FolderNameFinal)
        FileArray = [FileName, FolderNameFinal, final_directory]
        FileGaussArrayList.append(FileArray)

    return FileGaussArrayList

def Pathprocess(alt,lat,long,time, stat):

    stat.AddLocationFlight([[time,lat,long]], alt) 

    return stat