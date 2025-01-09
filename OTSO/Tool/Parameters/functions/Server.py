from . import MiddleMan as OTSOLib
from . import OmniPull
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys

def GetServerData(Date, External):
    OMNIYEAR = int(Date.year)
    RoundedDate = (Date + timedelta(minutes=5 - Date.minute % 5)).replace(second=0, microsecond=0)
    Date, By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6 = ExtractServerData(RoundedDate, External)

    return By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6


def ExtractServerData(RoundedDate,External):
    year = RoundedDate.year
    source_file = f'{year}_TSY_Inputs.csv'
    TSY_folder = os.path.join(os.getcwd(), "Parameters", "functions", "ServerData")
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

        if External == 7 and W1 == np.nan:
          print("ERROR: No TSY04 parameters found for given time. \nOTSO program will now terminate.")
          exit()
        elif External == 6 and G3 == np.nan:
          print("ERROR: No TSY01S parameters found for given time. \nOTSO program will now terminate.")
          exit()
        elif External == 5 and (G1 == np.nan or G2 == np.nan):
          print("ERROR: No TSY01 parameters found for given time. \nOTSO program will now terminate.")
          exit()

        if V > 0:
            V = -1*V

        return Date, By, Bz, V, Density, Pdyn, Kp, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6


def DownloadServerFile(OMNIYEAR):
    source_file = f'{OMNIYEAR}_TSY_Inputs.csv'
    TSY_folder = os.path.join(os.getcwd(), "Parameters", "functions", "ServerData")
    TSY_file = os.path.join(TSY_folder, os.path.basename(source_file))

    if not os.path.exists(TSY_file):
        while True:
            user_input = input(f"Data for {OMNIYEAR} does not exist in OTSO files.\nWould you like OTSO to attempt to download data from online?\nNote: this can take up to 30 minutes.\nPlease enter (YES/NO): ")
            if user_input == 'YES':
                    print(f'Attempting to download data for {OMNIYEAR}')
                    OmniPull.PullOMNI(OMNIYEAR)
                    OTSOLib.gettsy04data(OMNIYEAR)
                    OmniPull.OMNI_to_csv(OMNIYEAR)
                    OmniPull.TSY01(f'{OMNIYEAR}_TSY_Data.csv')
                    OmniPull.TSY01(f'omni_{OMNIYEAR}_low_res.csv')
                    OmniPull.Combine(f'{OMNIYEAR}_TSY_Data.csv', f'omni_{OMNIYEAR}_low_res.csv',OMNIYEAR)
                    OmniPull.Omnidelete(OMNIYEAR)
                    print(f'Finished downloading data for {OMNIYEAR}.\nPlease try running OTSO computation again.')
                    exit()
            elif user_input == 'NO':
                    print('OTSO computation will now terminate.')
                    exit()
            else:
                print("Invalid input. Please respond with YES or NO.")

    