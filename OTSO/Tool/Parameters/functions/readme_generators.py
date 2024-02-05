
from datetime import date
import os
import shutil

def READMECone(UsedStationstemp, RigidityArray, EventDate, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent, EndParams):
      FileName = "OTSO_CONE_RUN_INFO.txt"
      file = open(FileName, "w")

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"

      if (IntModel == 1):
         IntegrationMethod = "4th Order Runge-Kutta Method"
      elif (IntModel == 2):
         IntegrationMethod = "Boris Method"
      elif (IntModel == 3):
         IntegrationMethod = "Vay Method"
      elif (IntModel == 4):
         IntegrationMethod = "Higuera-Cary Method"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"
      elif (model[1] == 7):
         External = "Tsyganenko 04"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"
      elif (model[1] == 7):
         PauseModel = "Tsyganenko 04 Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Output Coordinate System:"+ "\n")
      file.write(str(CoordinateSystem)+ "\n")
      file.write("\n")
      file.write("Integration Method:"+ "\n")
      file.write(str(IntegrationMethod)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Minimum Altitude: " + str(EndParams[0])+ "\n")
      file.write("Max Distance: " + str(EndParams[1])+ "\n")
      file.write("Max Time: " + str(EndParams[2])+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(UsedStationstemp[0][3]) + "km \n")
      file.write("Zenith = " + str(UsedStationstemp[0][4]) + "\n")
      file.write("Azimuth = " + str(UsedStationstemp[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("Start = " + str(RigidityArray[0]) + " [GV]"+ "\n")
      file.write("End = " + str(RigidityArray[1]) + " [GV]"+ "\n")
      file.write("Step = " + str(RigidityArray[2]) + " [GV]"+ "\n")
      file.write("\n")
      file.write("Stations:"+ "\n")

      for i in UsedStationstemp:
         file.write(str(i[0])+"," + " Latitude: " + str(i[1])+"," + " Longitude: " + str(i[2])+ "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return

def READMECutoff(UsedStationstemp, RigidityArray, EventDate, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent, EndParams, Rcomp, Rscan):
      FileName = "OTSO_CUTOFF_RUN_INFO.txt"
      file = open(FileName, "w")

      if (Rcomp == 0):
         CutoffComp = "Vertical Cutoff Rigidity"
      else:
         CutoffComp = "Apparent Cutoff Rigidity"

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"

      if (Rscan == 0):
         RigidityScan = "No Rigidity Scan"
      else:
         RigidityScan = "Rigidity Scan Used"

      if (IntModel == 1):
         IntegrationMethod = "4th Order Runge-Kutta Method"
      elif (IntModel == 2):
         IntegrationMethod = "Boris Method"
      elif (IntModel == 3):
         IntegrationMethod = "Vay Method"
      elif (IntModel == 4):
         IntegrationMethod = "Higuera-Cary Method"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"
      elif (model[1] == 7):
         External = "Tsyganenko 04"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"
      elif (model[1] == 7):
         PauseModel = "Tsyganenko 04 Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Cutoff Computed: "+ str(CutoffComp) + "\n")
      file.write("\n")
      file.write("Output Coordinate System:"+ "\n")
      file.write("\n")
      file.write(str(CoordinateSystem)+ "\n")
      file.write("Rigidity Scan:"+ "\n")
      file.write(str(RigidityScan)+ "\n")
      file.write("\n")
      file.write("Integration Method:"+ "\n")
      file.write(str(IntegrationMethod)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Minimum Altitude: " + str(EndParams[0])+ "\n")
      file.write("Max Distance: " + str(EndParams[1])+ "\n")
      file.write("Max Time: " + str(EndParams[2])+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(UsedStationstemp[0][3]) + "km \n")
      file.write("Zenith = " + str(UsedStationstemp[0][4]) + "\n")
      file.write("Azimuth = " + str(UsedStationstemp[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("Start = " + str(RigidityArray[0]) + " [GV]"+ "\n")
      file.write("End = " + str(RigidityArray[1]) + " [GV]"+ "\n")
      file.write("Step = " + str(RigidityArray[2]) + " [GV]"+ "\n")
      file.write("\n")
      file.write("Stations:"+ "\n")

      for i in UsedStationstemp:
         file.write(str(i[0])+"," + " Latitude: " + str(i[1])+"," + " Longitude: " + str(i[2])+ "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return



def READMETrajectory(UsedStationstemp, Rigidity, EventDate, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, CoordinateSystem, Printtime, MaxStepPercent, EndParams):
      FileName = "OTSO_TRAJECTORY_RUN_INFO.txt"
      file = open(FileName, "w")

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"

      if (IntModel == 1):
         IntegrationMethod = "4th Order Runge-Kutta Method"
      elif (IntModel == 2):
         IntegrationMethod = "Boris Method"
      elif (IntModel == 3):
         IntegrationMethod = "Vay Method"
      elif (IntModel == 4):
         IntegrationMethod = "Higuera-Cary Method"


      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"
      elif (model[1] == 7):
         External = "Tsyganenko 04"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"
      elif (model[1] == 7):
         PauseModel = "Tsyganenko 04 Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Output Coordinate System:"+ "\n")
      file.write(str(CoordinateSystem)+ "\n")
      file.write("Integration Method:"+ "\n")
      file.write(str(IntegrationMethod)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Minimum Altitude: " + str(EndParams[0])+ "\n")
      file.write("Max Distance: " + str(EndParams[1])+ "\n")
      file.write("Max Time: " + str(EndParams[2])+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(UsedStationstemp[0][3]) + "km \n")
      file.write("Zenith = " + str(UsedStationstemp[0][4]) + "\n")
      file.write("Azimuth = " + str(UsedStationstemp[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("R = " + str(Rigidity) + " [GV]"+ "\n")
      file.write("\n")
      file.write("Stations:"+ "\n")

      for i in UsedStationstemp:
         file.write(str(i[0])+"," + " Latitude: " + str(i[1])+"," + " Longitude: " + str(i[2])+ "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      result_directory = os.path.join(current_directory,"Results")
      final_directory = os.path.join(result_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return

def READMEPlanet(Data, Rigidity, EventDate, model, IntModel, AtomicNum, AntiCheck, IOPT, WindArray, Magnetopause, FileDescriptors, Printtime, LatStep, LongStep, MaxStepPercent, EndParams, Rcomp, Rscan):
      FileName = "OTSO_PLANET_RUN_INFO.txt"
      file = open(FileName, "w")

      if (Rcomp == 0):
         CutoffComp = "Vertical Cutoff Rigidity"
      else:
         CutoffComp = "Apparent Cutoff Rigidity"

      if (Rscan == 0):
         RigidityScan = "No Rigidity Scan"
      else:
         RigidityScan = "Rigidity Scan Used"

      if (AntiCheck == 1):
         particle = "anti-particle"
      else:
         particle = "Normal Particle"

      if (IntModel == 1):
         IntegrationMethod = "4th Order Runge-Kutta Method"
      elif (IntModel == 2):
         IntegrationMethod = "Boris Method"
      elif (IntModel == 3):
         IntegrationMethod = "Vay Method"
      elif (IntModel == 4):
         IntegrationMethod = "Higuera-Cary Method"

      if (model[0] == 1):
         Internal = "IGRF"
      else:
         Internal = "Dipole"

      if (model[1] == 0):
         External = "No External Field"
      elif (model[1] == 1):
         External = "Tsyganenko 87 Short"
      elif (model[1] == 2):
         External = "Tsyganenko 87 Long"
      elif (model[1] == 3):
         External = "Tsyganenko 89"
      elif (model[1] == 4):
         External = "Tsyganenko 96"
      elif (model[1] == 5):
         External = "Tsyganenko 01"
      elif (model[1] == 6):
         External = "Tsyganenko 01 Storm"
      elif (model[1] == 7):
         External = "Tsyganenko 04"

      if (Magnetopause == 0):
         PauseModel = "25Re Sphere"
      elif (Magnetopause == 1):
         PauseModel = "Aberrated Formisano Model"
      elif (Magnetopause == 2):
         PauseModel = "Sibeck Model"
      elif (Magnetopause == 3):
         PauseModel = "Kobel Model"
      elif (model[1] == 4):
         PauseModel = "Tsyganenko 96 Magnetopause Model"
      elif (model[1] == 5):
         PauseModel = "Tsyganenko 01 Magnetopause Model"
      elif (model[1] == 6):
         PauseModel = "Tsyganenko 01 Storm Magnetopause Model"
      elif (model[1] == 7):
         PauseModel = "Tsyganenko 04 Magnetopause Model"

      today = date.today()
      file.write("Date of OTSO computation: " + str(today) + "\n")
      file.write("Total computation time: " + str(Printtime) + " seconds"+ "\n")
      file.write("\n")
      file.write("Cutoff Computed: "+ str(CutoffComp) + "\n")
      file.write("\n")
      file.write("Rigidity Scan:"+ "\n")
      file.write(str(RigidityScan)+ "\n")
      file.write("\n")
      file.write("Integration Method:"+ "\n")
      file.write(str(IntegrationMethod)+ "\n")
      file.write("\n")
      file.write("Input Variables:"+ "\n")
      file.write("\n")
      file.write("Simulation Date: " + EventDate.strftime("%d/%m/%Y, %H:%M:%S")+ "\n")
      file.write("\n")
      file.write("Max Time Step [% of gyrofrequency]: " + str(MaxStepPercent)+ "\n")
      file.write("\n")
      file.write("Minimum Altitude: " + str(EndParams[0])+ "\n")
      file.write("Max Distance: " + str(EndParams[1])+ "\n")
      file.write("Max Time: " + str(EndParams[2])+ "\n")
      file.write("\n")
      file.write("Start Altitude = " + str(Data[0][3]) + "km \n")
      file.write("Zenith = " + str(Data[0][4]) + "\n")
      file.write("Azimuth = " + str(Data[0][5]) + "\n")
      file.write("\n")
      file.write("IOPT = " + str(IOPT)+ "\n")
      file.write("\n")
      file.write("Solar Wind Speed [km/s]:"+ "\n")
      file.write("Vx = " + str(WindArray[0])+ "\n")
      file.write("Vy = " + str(WindArray[1])+ "\n")
      file.write("Vz = " + str(WindArray[2])+ "\n")
      file.write("\n")
      file.write("IMF [nT]:"+ "\n")
      file.write("By = " + str(WindArray[3])+ "\n")
      file.write("Bz = " + str(WindArray[4])+ "\n")
      file.write("\n")
      file.write("Density = " + str(WindArray[5]) + " cm^-2"+ "\n")
      file.write("\n")
      file.write("Dst = " + str(WindArray[6]) + " nT"+ "\n")
      file.write("\n")
      file.write("G1 = " + str(WindArray[7])+ "\n")
      file.write("G2 = " + str(WindArray[8])+ "\n")
      file.write("G3 = " + str(WindArray[9])+ "\n")
      file.write("\n")
      file.write("Atomic Number = " + str(AtomicNum)+ "\n")
      file.write("\n")
      file.write("Particle Type = " + str(particle)+ "\n")
      file.write("\n")
      file.write("Magnetic Field Models:"+ "\n")
      file.write("Internal Model = " + str(Internal)+ "\n")
      file.write("External Model = " + str(External)+ "\n")
      file.write("\n")
      file.write("Magnetopause Model = " + str(PauseModel)+ "\n")
      file.write("\n")
      file.write("Rigidity"+ "\n")
      file.write("R = " + str(Rigidity) + " [GV]"+ "\n")
      file.write("Latitude and Longitude Steps"+ "\n")
      file.write("Latitude = " + str(LatStep) + " degree steps" + "\n")
      file.write("Longitude = " + str(LongStep) + " degree steps" + "\n")
    
      file.close()
      
      current_directory = os.getcwd()
      final_directory = os.path.join(current_directory, FileDescriptors[1])
      if not os.path.exists(final_directory):
       os.makedirs(final_directory)

      final_directory = os.path.join(final_directory, FileName)
      shutil.move(os.path.join(current_directory, FileName), final_directory )
      return