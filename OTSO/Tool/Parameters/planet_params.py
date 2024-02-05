################################################################################################################
# Select the step size that will be taken in longitude and latitude across the entire globe
LatStep = -1
LongStep = 1

# Select the range of latitudes for the computation 90 and -90 will cover an entire meridian line
MaxLat = 90
MinLat = -90

# Select the range of longitude for the computation 360 and 0 will cover an entire parallel
MaxLong = 359
MinLong = 0
################################################################################################################
# Starting conditions for the simulations
Alt = 20.0
################################################################################################################
# Picking the cutoff computation to be conducted
# 0 = Vertical cutoff rigidity, 1 = Apparent cutoff rigidity
CutoffComputation = 0
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
################################################################################################################
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
# Internal: 1 = IGRF, 2 = Dipole, 3 = Custom IGRF
# External: 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm), 7 = TSY04
Internal = 1
External = 3
###############################################################################################################
# Pick the integration model to use
# 1 = 4th Order Runge-Kutta, 2 = Boris Method, 3 = Vay, 4 = Higuera-Cary
IntModel = 1
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step
StartRigidity = 20
EndRigidity = 0
RigidityStep = 0.01
###############################################################################################################
# Rigidity Scan (will quickly scan the rigidity range for an estimate of the effective cutoff, then will
# start the main computation around the estimated effective cutoff)
# 0 = No Scan, 1 = Scan
RigidityScan = 0
###############################################################################################################
# Pick the maximum percentage of the particles gyrofrequency that can be used as the max time step in the
# computation
MaxStepPercent = 0.1
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
Magnetopause = 3
###############################################################################################################
# Choose name of folder that output files will be sent to. Folder created in results directory
FolderName = "Planet Example Folder"
###############################################################################################################
# Select the number of cores that the computation will be performed over
CoreNum = 1
###############################################################################################################