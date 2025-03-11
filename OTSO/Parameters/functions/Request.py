import requests
import pandas as pd
import time
import os
import json
from datetime import datetime, timedelta
from .Extract import *
from .Gvalues import *

output_directory = os.path.dirname(os.path.realpath(__file__)) 

def fetch_data_Space(urlSpace):
    try:
        response = requests.get(urlSpace)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching data: {e}")
        return None
    
def fetch_data_Mag(urlMag):
    try:
        response = requests.get(urlMag)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching data: {e}")
        return None

def fetch_data_Dst(urlDst):
    try:
        responseDst = requests.get(urlDst)
        responseDst.raise_for_status()  
        return responseDst.text  
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching data: {e}")
        return None
    
def fetch_data_Kp(urlKp):
    try:
        responseKp = requests.get(urlKp)
        responseKp.raise_for_status()  
        return responseKp.text  
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching data: {e}")
        return None

def get_next_version():
    existing_files = os.listdir(output_directory)
    version_numbers = []

    for file_name in existing_files:
        if file_name.startswith("space_data_") and (file_name.endswith(".csv") or file_name.endswith(".json")):
            try:
                version = int(file_name.split('_')[-1].split('.')[0])
                version_numbers.append(version)
            except ValueError:
                continue
    
    if version_numbers:
        return max(version_numbers) + 1
    else:
        return 1

def save_to_json_space(data, version):
    json_file = os.path.join(output_directory, f'space_data.json')
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def save_to_json_magnetic(data, version):
    json_file = os.path.join(output_directory, f'Magnetic_data.json')
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def save_to_txt_Dst(data, version):
    Dst_file = os.path.join(output_directory, f'Dst_data.txt')
    with open(Dst_file, "w") as fileDst:
            fileDst.write(data)

def save_to_txt_Kp(data, version):
    Kp_file = os.path.join(output_directory, f'Kp_data.txt')
    with open(Kp_file, "w") as fileKp:
            fileKp.write(data)

def save_to_csv_Space(data, version):
    csv_file = os.path.join(output_directory, f'space_data.csv')
    try:
        if isinstance(data, list) and all(isinstance(row, list) for row in data):
            headers = data[0]
            rows = data[1:]

            df = pd.DataFrame(rows, columns=headers)
            df['fetch_timestamp'] = pd.Timestamp.now()
            df.to_csv(csv_file, index=False)

    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")

def save_to_csv_Mag(data, version):
    csv_file = os.path.join(output_directory, f'Magnetic_data.csv')
    try:
        if isinstance(data, list) and all(isinstance(row, list) for row in data):
            headers = data[0]
            rows = data[1:]
            
            df = pd.DataFrame(rows, columns=headers)
            df['fetch_timestamp'] = pd.Timestamp.now()
            df.to_csv(csv_file, index=False)

    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")

def Get_Data(current_time):

    os.makedirs(output_directory, exist_ok=True)

    #current_time = datetime.utcnow()
    #current_time = current_time - timedelta(hours=3)
    current_month = f"{current_time.month:02d}"
    current_year = current_time.year
    curretnt_year_two_digits = current_year % 100

    dststring1 = str(current_year)+str(current_month)
    dststring2 = str(curretnt_year_two_digits)+str(current_month)
    
    urlSpace = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'
    urlMag = 'https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json'
    urlDst = 'https://wdc.kugi.kyoto-u.ac.jp/dst_realtime/'+dststring1+'/dst'+dststring2+'.for.request'
    urlKp = 'https://kp.gfz-potsdam.de/app/files/Kp_ap_nowcast.txt'

    data_Space = fetch_data_Space(urlSpace)
    data_Mag = fetch_data_Mag(urlMag)
    data_Dst = fetch_data_Dst(urlDst)
    data_Kp = fetch_data_Kp(urlKp)
    if data_Space:
        version = get_next_version()
        save_to_json_space(data_Space, version)
        save_to_json_magnetic(data_Space, version)
        save_to_csv_Space(data_Space, version)
        save_to_csv_Mag(data_Mag, version)
        save_to_txt_Dst(data_Dst, version)
        save_to_txt_Kp(data_Kp, version)
    else:
        print("Failed to obtain online data")
    
    DstFile = os.path.join(output_directory, f'Dst_data.txt')
    Dst,daily_dst = extract_dst_value(DstFile, current_time)
    Speed,Density = extract_solar_wind(current_time)
    By, Bz = extract_magnetic(current_time)
    Kp,IOPT = extract_kp_index(current_time)
    G1,G2,G3 = TSY01_Constants(By,Bz,-1*Speed,Density)
    Speed = round(Speed,3)
    Density = round(Density,3)
    By = round(By,3)
    Bz = round(Bz,3)
    G1 = round(G1,3)
    G2 = round(G2,3)
    G3 = round(G3,3)

    return Dst, Speed, Density, By, Bz, IOPT, G1, G2, G3, Kp
