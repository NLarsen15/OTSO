################################################################################################################
# Picking the stations to be tested.
# Additional stations can be added via the .AddLocation("Name",Latitude,Longitude) function
# If you just want to use custom locations leave List empty.
List = ["Oulu"]
Alt = 20.0 #[km]

#Custom_Locations = [["Custom_Location_Name3", -70, 0]]
#################################################################################################################
# Choose if you want to trace magnetic field lines for the whole planet instead of individial stations
# Planet: 0 = no planet computation, 1 = planet computation
Planet = 1
# Select the step size that will be taken in longitude and latitude across the entire globe
LatStep = -10
LongStep = 10

# Select the range of latitudes for the computation 90 and -90 will cover an entire meridian line
MaxLat = 90
MinLat = -90

# Select the range of longitude for the computation 360 and 0 will cover an entire parallel
MaxLong = 360
MinLong = 0
################################################################################################################
# Solar Wind Conditions
Vx = -500.0 #[km/s]
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
# IOPT is Picked depending on the Kp index at the time picked
# Take IOPT = kp + 1
# Exception if Kp>=6 IOPT = 7
IOPT = 2
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
# External: 0 = No External Field, 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm), 7 = TSY04(Second Number in model Array)
Internal = 1
External = 3
###############################################################################################################
# Pick the coordinate system desired for the output
# GDZ, GEO, GSM , GSE, SM, GEI, MAG, SPH (GEO in spherical), RLL 
CoordinateSystem  = "GEO"
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel, 100 = 100Re Sphere
Magnetopause = 3
###############################################################################################################
# Choose name of folder that output files will be sent to. Folder created in current directory
FolderName = "Trace Example Folder"
###############################################################################################################
# Select number of cores for multicore processing
CoreNum = 1
###############################################################################################################