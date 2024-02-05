from cmath import atan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import math

#data = pd.read_csv("GLE66_TSY01_DATA.csv")

#IMFy = data["IMFy"]
#IMFz = data["IMFz"]
#Speed = data["Speed"]

#################################################################
# Control Test
# G1 = 5.55
# G2 = 10
IMFy = [-2.83]
IMFz = [0.48]
Speed = [648.2]
Density = [1.47]
#############################################################

G1 = 0
G2 = 0
G3 = 0

for (By, Bz, V, N) in zip(IMFy, IMFz, Speed, Density):
    By = By
    Bz = Bz
    V = V
    W = 1/len(IMFy)


    B = (By*By + Bz*Bz)**(0.5)
    h = (((B/40)**(2))/(1 + B/40))

    if(By == 0 and Bz == 0):
        phi = 0
    else:
        phi = math.atan2(By,Bz)
        if(phi <= 0):
            phi = phi + 2*math.pi

    if(Bz < 0):
        Bs = abs(Bz)
    elif Bz >= 0:
        Bs = 0
    
    G1 = G1 + (W)*V*h*(math.sin(phi/2)**3)
    G2 = G2 + (0.005)*(W)*(V)*Bs
    G3 = G3 + (N*V*Bs)/2000
    
print("G1 = " + str(G1))
print("G2 = " + str(G2))
print("G3 = " + str(G3))

    