################################################################################################################
# Picking the stations to be tested.
# Additional stations can be added via the .AddLocation("Name",Latitude,Longitude) function
# If you just want to use custom locations leave List empty.
List = ["Oulu"]
Alt = 20.0
Zenith = 0
Azimuth = 0

#Custom_Locations = [["Custom_Location_Name", Latitude, Longitude]]
################################################################################################################
# Ending parameters
# Input the values for the minimum altitude and maximum distance travelled by a particle. If either condition is
# met then the computation is terminated and the trajectory is assumed forbidden.
# For MaxDist and MaxTime enter 0 if you wish for there to be no limit. 
MinAlt = 20.0 #[km]
MaxDist = 100 #[Re]
MaxTime = 0 #[s]
################################################################################################################
# Solar Wind Conditions
Vx = -500.0 #[km/s]
Vy = 0.0 #[km/s]
Vz = 0.0 #[km/s]
By = 5 #[nT]
Bz = 5 #[nT]
Density = 1.0 #[cm^-2]
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
# IOPT is Picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
IOPT = 5
###############################################################################################################
# Choose the atomic number of particle you want to test e.g 0 = electron, 1 = proton, 2 = helium
# Choose if you want to reverse the charge 0 = particle, 1 = anti-particle
AtomicNum = 1
AntiCheck = 1
################################################################################################################
# Enter date to be investigated as a datetime under EventDate
Year = 2024
Month = 1
Day = 1
Hour = 12
Minute = 0
Second = 0
###############################################################################################################
# Pick the magnetosphere models that you want to use. 
# Internal: 1 = IGRF, 2 = Dipole, 3 = Custom Gauss, 4 = Non-Standard Custom Gauss
# External: 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm), 7 = TSY04(Second Number in model Array)
Internal = 1
External = 3
###############################################################################################################
# Pick the integration model to use
# 1 = 4th Order Runge-Kutta, 2 = Boris, 3 = Vay, 4 = Higuera-Cary
IntModel = 1
###############################################################################################################
# Pick the rigidity for the computation
Rigidity = 10 #[GV]
###############################################################################################################
# Pick the coordinate system desired for the output
# GDZ, GEO, GSM , GSE, SM, GEI, MAG, SPH (GEO in spherical), RLL 
CoordinateSystem  = "GEO"
###############################################################################################################
# Pick the maximum percentage of the particles gyrofrequency that can be used as the max time step in the
# computation
MaxStepPercent = 0.1
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
Magnetopause = 3
###############################################################################################################
# Choose name of folder that output files will be sent to. Folder created in current directory
FolderName = "Example Trajectory Folder"
FileName = "_Trajectory"
###############################################################################################################
# Select number of cores for multicore processing
CoreNum = 1
###############################################################################################################