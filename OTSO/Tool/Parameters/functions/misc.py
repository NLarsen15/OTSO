import os
import psutil
import pandas as pd
import glob
import multiprocessing as mp
import shutil

def ParamCheck(Alt, Year, Internal, EndParams):
       if EndParams[0] > Alt:
        print("ERROR: Inputted minimum altitude is larger than starting altitude. Value must be less than or equal to the starting altitude. Please check inputs. \nOTSO program will now terminate.")
        exit()

       if Internal == 1:
         if Year<1900 or Year>2025:
          print("ERROR: IGRF 13 model currently only works for dates between 1900 to 2025. Please select a date within this range to use the IGRF model")
          exit()



def PlanetFile(final_directory):
 
 planetfile = "Planet.csv"
 Planetfile_path = os.path.join(final_directory, planetfile)
 if os.path.isfile(Planetfile_path):
    os.remove(Planetfile_path)

 files = os.path.join(final_directory, "*.csv")
 files = glob.glob(files)
 df = pd.concat(map(pd.read_csv, files), ignore_index=True)
 df_sorted = df.sort_values(by=[df.columns[0], df.columns[1]])
 os.makedirs(final_directory, exist_ok=True)  
 df_sorted.to_csv(final_directory + '/Planet.csv', index=False)

 for i in files:
   os.remove(i)

def FlightFile(final_directory):
 
 planetfile = "Flight.csv"
 Planetfile_path = os.path.join(final_directory, planetfile)
 if os.path.isfile(Planetfile_path):
    os.remove(Planetfile_path)

 files = glob.glob(os.path.join(final_directory, "*.csv"))
 files = [f for f in files if not f.endswith("Flight_Params.csv")]
 df = pd.concat(map(pd.read_csv, files), ignore_index=True)
 df['Time'] = pd.to_datetime(df['Time'], format='%d-%m-%Y %H-%M-%S')
 df_sorted = df.sort_values(by=[df.columns[0]])
 os.makedirs(final_directory, exist_ok=True)  
 df_sorted.to_csv(final_directory + '/Flight.csv', index=False)

 for i in files:
   os.remove(i)

def FlightCopy(final_directory):
 
 current_directory = os.getcwd()
 planetfile = "Parameters\\Flight_Params.csv"
 Planetfile_path = os.path.join(current_directory, planetfile)
 
 shutil.copy2(Planetfile_path, final_directory)

def CheckCoreNumPlanet(x):
  NewCore = x
  if(psutil.cpu_count(logical=False) < x):
    print("ERROR: You have entered an invalid number of cores")
    print("You have " + str(psutil.cpu_count(logical=False)) + " and have tried to use " + str(x) + " cores")
    print("To ensure operational integrity of your computer OTSO will run using 2 less than the max cores available, with a minumum value of 1.")
    NewCore = psutil.cpu_count(logical=False) - 2
    if NewCore <= 0:
      NewCore = 1
  return NewCore

def day_of_year_to_date(doy, year):
    # Define days in each month for both leap and non-leap years
    days_in_months_non_leap = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_months_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Check if the year is a leap year
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        days_in_months = days_in_months_leap
    else:
        days_in_months = days_in_months_non_leap

    # Initialize variables to accumulate days and find the month
    accumulated_days = 0
    month = 0

    # Find the month and day corresponding to the day of the year (DOY)
    for i in range(12):
        accumulated_days += days_in_months[i]
        if doy <= accumulated_days:
            month = i + 1
            day = doy - (accumulated_days - days_in_months[i])
            break

    # Return the month and day as a tuple
    return (month, day)