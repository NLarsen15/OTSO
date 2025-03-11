import numpy as np
from datetime import datetime
import os
import pandas as pd
from Parameters.bulk_cone_params import *
from . import date, cores, solar_wind, stations
from . import misc

def BulkConeInputs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_pathspace = os.path.join(parent_dir, 'Bulk_Space_Weather_Params.csv')
    file_pathgauss = os.path.join(parent_dir, 'Bulk_Gaussian_Coefficients.csv')
    dfspace = pd.read_csv(file_pathspace)
    dfgauss = pd.read_csv(file_pathgauss)
 
    FileGaussStringList = dfgauss.columns[3:].tolist()
 
    dfspace['Time'] = pd.to_datetime(dfspace['Time'], format='%d/%m/%Y %H:%M:%S')
    dfspace['Converted'] = dfspace['Time'].dt.strftime('%d-%m-%Y %H-%M-%S')
 
    TimeString = dfspace['Converted'].tolist()
 
    dfspace['Year'] = dfspace['Time'].dt.year
    dfspace['Month'] = dfspace['Time'].dt.month
    dfspace['Day'] = dfspace['Time'].dt.day
    dfspace['Hour'] = dfspace['Time'].dt.hour
    dfspace['Minute'] = dfspace['Time'].dt.minute
    dfspace['Second'] = dfspace['Time'].dt.second
 
    Dateresults = dfspace.apply(lambda row: Dateprocess(row['Year'], row['Month'], row['Day'], row['Hour'], row['Minute'], row['Second']), axis=1)
    DateArrayList = Dateresults.tolist()
 
    WindResults = dfspace.apply(lambda row: Windprocess(row['Vx'], row['Vy'], row['Vz'], row['By'], row['Bz'], row['Density'], row['Pdyn'], row['Dst'], row['G1'], row['G2'], 
                                                    row['G3'], row['W1'], row['W2'], row['W3'], row['W4'], row['W5'], row['W6']), axis=1)
    WindArrayList = WindResults.tolist()
 
    IOPTResults = dfspace.apply(lambda row: IOPTprocess(row['Kp']), axis=1)
    IOPTList = IOPTResults.tolist()
    
    ##########################################################
    # Placeholder values for when using own gaussian coefficients
    EventDateGauss = datetime(2000,1,1,12,0,0)
    DateCreateGauss = date.Date(EventDateGauss)
    DateArrayGauss = DateCreateGauss.GetDate()
    WindCreateGauss = solar_wind.Solar_Wind(-500, 0, 0, 5, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    WindArrayGauss = WindCreateGauss.GetWind()
    IOPTGauss = 1
    FileArrayGauss = FileprocessGauss(FileGaussStringList, FileName)
    GaussCoeffs = GaussAssign(dfgauss)
    #########################################################

    RigidityArray = [StartRigidity,EndRigidity,RigidityStep]

    MagFieldModel = np.array([Internal,External])

    EndParams = [MinAlt,MaxDist,MaxTime]

    CreateStations = stations.Stations(List, Alt, Zenith, Azimuth)
    InputtedStations = CreateStations
    if 'Custom_Locations' in locals() or 'Custom_Locations' in globals():
          CreateStations.AddLocation(Custom_Locations)
    Used_Stations_Temp = CreateStations.GetStations()
    temp = list(Used_Stations_Temp)
    Station_Array = temp

    if Bulkcomp == 0:
      for Y in dfspace['Year']:
        misc.ParamCheck(Alt,Y,Internal,EndParams)
    elif Bulkcomp == 1:
        misc.ParamCheck(Alt,DateArrayGauss[0],Internal,EndParams)

    FileArrayList = Fileprocess(TimeString, FileName)

    ParticleArray = [AtomicNum,AntiCheck]

    BulkConeInputArraySpace = [RigidityArray,DateArrayList,MagFieldModel,IntModel,ParticleArray,IOPTList,WindArrayList,Magnetopause,FileArrayList,CoordinateSystem,MaxStepPercent,EndParams, Station_Array, InputtedStations]
    BulkConeInputArrayGauss = [RigidityArray,DateArrayGauss,MagFieldModel,IntModel,ParticleArray,IOPTGauss,WindArrayGauss,Magnetopause,FileArrayGauss,CoordinateSystem,MaxStepPercent, EndParams, Station_Array, InputtedStations, GaussCoeffs]

    return BulkConeInputArraySpace, BulkConeInputArrayGauss

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
        FolderNameFinal = FolderName + " " + string
        final_directory = os.path.join(result_directory,FolderNameFinal)
        FileArray = [FileName, FolderNameFinal, final_directory]
        FileArrayList.append(FileArray)

    return FileArrayList 

def FileprocessGauss(FileGaussStringList, FileName):

    FileGaussArrayList = []

    for string in FileGaussStringList:
        current_directory = os.getcwd()
        result_directory = os.path.join(current_directory,"Results")
        FolderNameFinal = FolderName + " " + string
        final_directory = os.path.join(result_directory,FolderNameFinal)
        FileArray = [FileName, FolderNameFinal, final_directory]
        FileGaussArrayList.append(FileArray)

    return FileGaussArrayList

def GaussAssign(Gaussdf):

    GaussCoefficients = []

    for col in Gaussdf.columns[3:]:
        glist = []
        hlist = []
        # Filter rows where 'g/h' column is 'g', and get values from the current column
        g_values = Gaussdf.loc[Gaussdf['g/h'] == 'g', col].tolist()
        glist.append(g_values)
        
        # Filter rows where 'g/h' column is 'h', and get values from the current column
        h_values = Gaussdf.loc[Gaussdf['g/h'] == 'h', col].tolist()
        hlist.append(h_values)

        GaussCoefficients.append([glist,hlist])

    return GaussCoefficients