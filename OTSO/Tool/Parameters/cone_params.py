################################################################################################################
# Picking the stations to be tested.
# Additional stations can be added via the .AddLocation("Name",Latitude,Longitude) function
# If you just want to use custom locations leave List empty.
List = ["Oulu"]
Alt = 20.0 #[km]
Zenith = 0 #[degrees]
Azimuth = 0 #[degrees]

#Custom_Locations = [["Custom_Location_Name", Latitude, Longitude]]
################################################################################################################
# Ending parameters
# Input the values for the minimum altitude and maximum distance travelled by a particle. If either condition is
# met then the computation is terminated and the trajectory is assumed forbidden. 
# For MaxDist and MaxTime enter 0 if you wish for there to be no limit. 
MinAlt = 20 #[km]
MaxDist = 100 #[Re]
MaxTime = 0 #[s]
################################################################################################################
# Solar Wind Conditions
Vx = -500.0 #[km/s] (value should be negative)
Vy = 0.0 #[km/s]
Vz = 0.0 #[km/s]
By = 5 #[nT]
Bz = 5 #[nT]
Density = 1.0 #[cm^-2]
Pdyn = 1.0 #[nPa]
Dst = 0 #[nT]

# G1 and G2 are only needed for TSY01 use (use external TSY01_Constants tool to calculate them)
# or enter the average solar wind speed, By, and Bz over the 1 hour period prior to event
# G3 Used only in TSY01(Storm)
G1 = 0
G2 = 0
G3 = 0

# W1 - W6 are only needed for TSY04 (Parameters can be found at 
# https://geo.phys.spbu.ru/~tsyganenko/empirical-models/magnetic_field/ts05#yearly-input-parameter-files)
W1 = 0
W2 = 0
W3 = 0
W4 = 0 
W5 = 0
W6 = 0
################################################################################################################
# IOPT is picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
IOPT = 2
###############################################################################################################
# Choose the atomic number of the particle you want to test e.g 0 = electron, 1 = proton, 2 = helium
# Choose if you want to reverse the charge 0 = particle, 1 = anti-particle
AtomicNum = 1
AntiCheck = 1
################################################################################################################
# Enter date information (currently available time range 1900-2025)
Year = 2024
Month = 1
Day = 1
Hour = 12
Minute = 0
Second = 0
###############################################################################################################
# Pick the magnetosphere models that you want to use. 
# Internal: 1 = IGRF, 2 = Dipole, 3 = Custom Gauss, 4 = Non-Standard Custom Gauss
# External: 0 = No External Field 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm), 7 = TSY04
Internal = 1
External = 3
###############################################################################################################
# Pick the integration model to use
# 1 = 4th Order Runge-Kutta, 2 = Boris, 3 = Vay, 4 = Higuera-Cary
IntModel = 1
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step in GV
StartRigidity = 20 #[GV]
EndRigidity = 0 #[GV]
RigidityStep = 0.01 #[GV]
###############################################################################################################
# Pick the coordinate system desired for the output
# GDZ, GEO, GSM, GSE, SM, GEI, MAG, SPH (GEO in spherical), RLL 
CoordinateSystem  = "GEO"
###############################################################################################################
# Pick the maximum percentage of the particle's gyrofrequency that can be used as the max time step in the
# computation
MaxStepPercent = 10 #[%]
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
Magnetopause = 3
###############################################################################################################
# Choose the name of the folder that output files will be sent to. Folder created in the current directory
FolderName = "Example Cone Folder"
FileName = "_Cone"
###############################################################################################################
# Select the number of cores for multicore processing
CoreNum = 1
###############################################################################################################