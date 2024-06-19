import os
import psutil
import pandas as pd
import glob
import multiprocessing as mp

def ParamCheck(Alt, Year, Internal, EndParams):
       if EndParams[0] > Alt:
        print("ERROR: Inputted minimum altitude is larger than starting altitude. Value must be less than or equal to the starting altitude. Please check inputs. \nOTSO program will now terminate.")
        exit()

       if Internal == 1:
         if Year<1900 or Year>2025:
          print("ERROR: IGRF 13 model currently only works for dates between 1900 to 2025. Please select a date within this range to use the IGRF model")
          exit()



def PlanetFile(final_directory):

 files = os.path.join(final_directory, "*.csv")
 files = glob.glob(files)
 df = pd.concat(map(pd.read_csv, files), ignore_index=True)
 df_sorted = df.sort_values(by=[df.columns[0], df.columns[1]])
 os.makedirs(final_directory, exist_ok=True)  
 df_sorted.to_csv(final_directory + '/Planet.csv', index=False)

 for i in files:
   os.remove(i) 

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