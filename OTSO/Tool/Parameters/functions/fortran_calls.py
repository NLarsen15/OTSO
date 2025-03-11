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

def fortrancallConeGauss(Data, Core, RigidityArray, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams, Gauss):
    g = Gauss[0]
    h = Gauss[1]
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
      OTSOLib.conegauss(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams, g, h)
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

      shutil.move(os.path.join(current_directory, FileName), final_directory)
    
    return

def fortrancallCutoffGauss(Data, Core, RigidityArray, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan, Gauss):
    g = Gauss[0]
    h = Gauss[1]
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
      OTSOLib.cutoffgauss(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan, g, h)
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
  
def fortrancallFlight(Data, Core, RigidityArray, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan):
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
    OTSOLib.flight(Position, StartRigidity, EndRigidity, RigidityStep, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams, Rcomp, Rscan)
    #print(Station + " " + Core)
    newstop = time.time()
    Printtime = round((newstop-newstart),3)
    #print(Station + " - Time Taken: " + str(Printtime) + " seconds")


    current_directory = os.getcwd()
    result_directory = os.path.join(current_directory,"Results")
    final_directory = os.path.join(result_directory, FileDescriptors[1])
    if not os.path.exists(final_directory):
     os.makedirs(final_directory)

    final_directory = os.path.join(final_directory, FileName)

    shutil.move(os.path.join(current_directory, FileName), final_directory)
  
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
  for x in Data:
      
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      NMname = Station

      FileName = NMname + ".csv"
      OTSOLib.planet(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, MaxStepPercent, EndParams, Rcomp, Rscan)
      now = datetime.now()
      CurrentTime = now.strftime("%H:%M:%S")
      print(CurrentTime)

      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[0])
      if not os.path.exists(final_directory):
         os.makedirs(final_directory)
   
      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory)
   
def fortrancallTrace(Data, Core, Rigidity, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams):
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
      OTSOLib.fieldtrace(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams)
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

def fortrancallTracePlanet(Data, Core, Rigidity, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, MaxStepPercent, EndParams):
    final_directory = FileDescriptors[1]
    for x in Data:
      
      newstart = time.time()
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      FileGLE = FileDescriptors[0]
      final_directory = FileDescriptors[2]

      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      NMname = Station

      FileName = str(x[0]) + ".csv"
      OTSOLib.fieldtrace(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, CoordinateSystem, MaxStepPercent, EndParams)
      #print(Station + " " + Core)
      newstop = time.time()
      Printtime = round((newstop-newstart),3)
      #print(Station + " - Time Taken: " + str(Printtime) + " seconds")


      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
    
    return

def fortrancallPlanetGauss(Data, Rigidity, DateArray, model, IntModel, ParticleArray, IOPT, WindArray, Magnetopause, FileDescriptors, MaxStepPercent, EndParams, Rcomp, Rscan, Gauss):
  final_directory = FileDescriptors[1]
  g = Gauss[0]
  h = Gauss[1]
  for x in Data:
      
      Position = [x[3],x[1],x[2],x[4],x[5]]
      Station = x[0]

      AtomicNum = ParticleArray[0]
      AntiCheck = ParticleArray[1]

      NMname = Station

      FileName = NMname + ".csv"
      OTSOLib.planetgauss(Position, Rigidity, DateArray, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileName, MaxStepPercent, EndParams, Rcomp, Rscan, g, h)
      now = datetime.now()
      CurrentTime = now.strftime("%H:%M:%S")
      print(CurrentTime)

      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[0])
      if not os.path.exists(final_directory):
         os.makedirs(final_directory)
   
      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory)