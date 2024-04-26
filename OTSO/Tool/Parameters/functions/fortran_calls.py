from . import MiddleMan as OTSOLib
import time
import os
import shutil
from datetime import datetime
import pandas as pd
import glob
import csv

def fortrancallCone(Data, Core, RigidityArray, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams):
    
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      NMname = Station

      StartRigidity = RigidityArray[0]
      EndRigidity = RigidityArray[1]
      RigidityStep = RigidityArray[2]
      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      FileName = NMname + FileGLE + ".csv"
      OTSOLib.cone(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams)
      print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return

def fortrancallCutoff(Data, Core, RigidityArray, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan):
    
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      NMname = Station

      StartRigidity = RigidityArray[0]
      EndRigidity = RigidityArray[1]
      RigidityStep = RigidityArray[2]
      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      FileName = NMname + FileGLE + ".csv"
      OTSOLib.cutoff(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan)
      print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return

def fortrancallTrajectory(Data, Core, Rigidity, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams):
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      NMname = Station

      FileName = NMname + FileGLE + ".csv"
      OTSOLib.trajectory(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams)
      print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return


def fortrancallPlanet(Data, Rigidity, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent, EndParams, Rcomp, Rscan):

   final_directory = FileDescriptors[1]
   FileName = Data[0] + ".csv"

   NorthPoleCheck = 0
   SouthPoleCheck = 0

   f = open(FileName, 'w')
   writer = csv.writer(f)
   header = ['Latitude', 'Longitude', 'Ru', 'Rc', 'Rl']
   writer.writerow(header)
   f.close()

   AtomicNum = ParticleArray[0]
   AntiCheck = ParticleArray[1]


   for lon in(Data[2]):
      for lat in(Data[1]):

       Position = [Data[3],lat,lon,Data[4],Data[5]]
       Core = Data[6]
       if (lat == 90 and NorthPoleCheck == 1) or (lat == -90 and SouthPoleCheck == 1):
          pass
       else:
        OTSOLib.planet(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, MaxStepPercent, EndParams, Rcomp, Rscan)
        now = datetime.now()
        CurrentTime = now.strftime("%H:%M:%S")
        print(CurrentTime)

       if (lat == 90):
         NorthPoleCheck = 1
       if (lat == -90):
         SouthPoleCheck = 1



   current_directory = os.getcwd()
   result_directory = os.path.join(current_directory,"Results")
   final_directory = os.path.join(result_directory, FileDescriptors[0])
   if not os.path.exists(final_directory):
      os.makedirs(final_directory)

   final_directory = os.path.join(final_directory, FileName)
   shutil.move(os.path.join(current_directory, FileName), final_directory)