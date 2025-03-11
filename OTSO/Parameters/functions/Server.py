from . import MiddleMan as OTSOLib
from . import OmniPull
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys
import platform

def round_to_nearest_five_minutes(date):
    if date.minute % 5 == 0 and date.second == 0 and date.microsecond == 0:
        return date.replace(second=0, microsecond=0)
    return (date + timedelta(minutes=5 - date.minute % 5)).replace(second=0, microsecond=0)

def GetServerData(Date, External):
    OMNIYEAR = int(Date.year)
    RoundedDate = round_to_nearest_five_minutes(Date)
    Date, By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6 = ExtractServerData(RoundedDate, External)

    return By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6


def ExtractServerData(RoundedDate,External):
    year = RoundedDate.year
    source_file = f'{year}_TSY_Inputs.csv'
    TSY_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ServerData")
    TSY_file = os.path.join(TSY_folder, os.path.basename(source_file))

    if not os.path.exists(TSY_file):
        print(f"File for year {year} not found in the directory.")
        return

    try:
        df = pd.read_csv(TSY_file)
    except Exception as e:
        print(f"Error reading {source_file}: {e}")
        return

    if 'Date' not in df.columns:
        print(f"'Date' column not found in {source_file}")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    matching_row = df[df['Date'] == RoundedDate]

    #print(RoundedDate)

    if matching_row.empty:
        print(f"No matching row found for datetime: {RoundedDate}")
        return None
    else:
        row_data = matching_row.iloc[0]  

        Date = row_data['Date'] if 'Date' in row_data else None
        By = row_data['By'] if 'By' in row_data else None
        Bz = row_data['Bz'] if 'Bz' in row_data else None
        V = row_data['V'] if 'V' in row_data else None
        Density = row_data['Density'] if 'Density' in row_data else None
        Pdyn = row_data['Pdyn'] if 'Pdyn' in row_data else None
        Kp = row_data['Kp'] if 'Kp' in row_data else None
        Dst = row_data['Dst'] if 'Dst' in row_data else None
        G1 = row_data['G1'] if 'G1' in row_data else None
        G2 = row_data['G2'] if 'G2' in row_data else None
        G3 = row_data['G3'] if 'G3' in row_data else None
        W1 = row_data['W1'] if 'W1' in row_data else None
        W2 = row_data['W2'] if 'W2' in row_data else None
        W3 = row_data['W3'] if 'W3' in row_data else None
        W4 = row_data['W4'] if 'W4' in row_data else None
        W5 = row_data['W5'] if 'W5' in row_data else None
        W6 = row_data['W6'] if 'W6' in row_data else None

        if External == 7 and (np.isnan(W1) or W1 == 0) and (np.isnan(V) or V == 0) and (np.isnan(Bz) or Bz == 0):
           print("ERROR: No TSY04 parameters found for given time. \nOTSO program will now terminate.")
           exit()
        elif External == 6 and (np.isnan(G3) or G3 == 0) and (np.isnan(V) or V == 0) and (np.isnan(Bz) or Bz == 0):
           print("ERROR: No TSY01S parameters found for given time. \nOTSO program will now terminate.")
           exit()
        elif External == 5 and (np.isnan(G1) or G1 == 0) and (np.isnan(G2) or G2 == 0) and (np.isnan(V) or V == 0) and  (np.isnan(Bz) or Bz == 0):
           print("ERROR: No TSY01 parameters found for given time. \nOTSO program will now terminate.")
           exit()
        elif External == 4 and (np.isnan(V) or V == 0) and (np.isnan(Bz) or Bz == 0):
           print("ERROR: No TSY96 parameters found for given time. \nOTSO program will now terminate.")
           exit()

        if V > 0:
            V = -1*V

        return Date, By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6


def DownloadServerFile(OMNIYEAR):
    source_file = f'{OMNIYEAR}_TSY_Inputs.csv'
    TSY_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ServerData")
    TSY_file = os.path.join(TSY_folder, source_file)

    if not os.path.exists(TSY_file):
        print(f"Data for {OMNIYEAR} does not exist in OTSO files.")
        print(f'Attempting to download data for {OMNIYEAR}')
        OmniPull.PullOMNI(OMNIYEAR)
        DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)),"functions")
        length = len(DIRECTORY)
        if platform.system() == "Windows":
            OTSOLib.gettsy04datawindows(OMNIYEAR, length)
            OmniPull.OMNI_to_csv(OMNIYEAR)
            OmniPull.TSY01(f'{OMNIYEAR}_TSY_Data.csv')
            OmniPull.TSY01(f'omni_{OMNIYEAR}_low_res.csv')
            OmniPull.Combine(f'{OMNIYEAR}_TSY_Data.csv', f'omni_{OMNIYEAR}_low_res.csv',OMNIYEAR)
            OmniPull.Omnidelete(OMNIYEAR)
            print(f'Finished downloading data for {OMNIYEAR}.')
        elif platform.system() == "Linux":
            OTSOLib.gettsy04datalinux(OMNIYEAR, DIRECTORY, length)
            OmniPull.OMNI_to_csv(OMNIYEAR)
            OmniPull.TSY01(f'{OMNIYEAR}_TSY_Data.csv')
            OmniPull.TSY01(f'omni_{OMNIYEAR}_low_res.csv')
            OmniPull.Combine(f'{OMNIYEAR}_TSY_Data.csv', f'omni_{OMNIYEAR}_low_res.csv',OMNIYEAR)
            OmniPull.Omnidelete(OMNIYEAR)
            print(f'Finished downloading data for {OMNIYEAR}.')

    return


def DownloadServerFileLowRes(OMNIYEAR):
    source_file = f'{OMNIYEAR}_TSY_Inputs.csv'
    TSY_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ServerData")
    TSY_file = os.path.join(TSY_folder, os.path.basename(source_file))
    FilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'omni_{OMNIYEAR}_low_res.csv')

    if not os.path.exists(TSY_file):
        print(f"Data for {OMNIYEAR} does not exist in OTSO files.")
        print(f'Attempting to download data for {OMNIYEAR}')
        OmniPull.PullOMNILowRes(OMNIYEAR)
        OmniPull.CombineLowRes(FilePath,OMNIYEAR)
        OmniPull.OmnideleteLowRes(OMNIYEAR)
        print(f'Finished downloading data for {OMNIYEAR}.')


    