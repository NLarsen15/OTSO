################################################################################################################
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
# Starting conditions for the simulations
Alt = 20.0 #[km]
################################################################################################################
# Picking the cutoff computation to be conducted
# 0 = Vertical cutoff rigidity, 1 = Apparent cutoff rigidity
CutoffComputation = 0
################################################################################################################
# Pick whether you wish to do bulk computations over space weather conditions or gaussian coefficients
# 0 = (Space weather) Bulk_Space_Weather_Params.csv used, 1 = (Gaussian) Bulk_Gaussian_Coefficients.csv used 
Bulkcomp = 0
################################################################################################################
# Ending parameters
# Input the values for the minimum altitude and maximum distance travelled by a particle. If either condition is
# met then the computation is terminated and the trajectory is assumed forbidden.
# For MaxDist and MaxTime enter 0 if you wish for there to be no limit. 
MinAlt = 20 #[km]
MaxDist = 100 #[Re]
MaxTime = 0 #[s]
################################################################################################################
# Choose the atomic number of particle you want to test e.g 0 = electron, 1 = proton, 2 = helium
# Choose if you want to reverse the charge 0 = particle, 1 = anti-particle
AtomicNum = 1
AntiCheck = 1
################################################################################################################
# Pick the magnetosphere models that you want to use. 
# Internal: 1 = IGRF, 2 = Dipole, 3 = Custom Gauss, 4 = Non-Standard Custom Gauss
# External: 0 = No External Field, 1 = TSY87(short), 2 = TSY87(long), 3 = TSY89, 4 = TSY96, 5 = TSY01, 6 = TSY01(Storm), 7 = TSY04
Internal = 1
External = 3
###############################################################################################################
# Pick the integration model to use
# 1 = 4th Order Runge-Kutta, 2 = Boris Method, 3 = Vay, 4 = Higuera-Cary
IntModel = 3
###############################################################################################################
# Pick the start and end rigidity for the computation, as well as the step
StartRigidity = 20 #[GV]
EndRigidity = 0 #[GV]
RigidityStep = 0.1 #[GV]
###############################################################################################################
# Rigidity Scan (will quickly scan the rigidity range for an estimate of the effective cutoff, then will
# start the main computation around the estimated effective cutoff)
# 0 = No Scan, 1 = Scan
RigidityScan = 1
###############################################################################################################
# Pick the maximum percentage of the particles gyrofrequency that can be used as the max time step in the
# computation
MaxStepPercent = 10 #[%]
###############################################################################################################
# Choose model magnetopause
# 0 = 25Re Sphere, 1 = Aberrated Formisano, 2 = Sibeck, 3 = Kobel
Magnetopause = 3
###############################################################################################################
# Choose name of folder that output files will be sent to. Folder created in results directory
FolderName = "Example Planet Bulk Folder "
###############################################################################################################
# Select the number of cores that the computation will be performed over
CoreNum = 1
###############################################################################################################