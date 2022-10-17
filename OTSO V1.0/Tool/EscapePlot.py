import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import MiddleMan as LarsenLib
from Classes import Stations
from Classes import SolarWind
from Classes import Date
from Classes import Cores
from dateutil import parser
from datetime import datetime, timedelta


######################################################################
EventDate = datetime(2003, 10, 29, 21, 00, 00)
DateCreate = Date(EventDate)
DateArray = DateCreate.GetDate()
######################################################################

#data = pd.read_csv("PositionData.csv")
R = 6371.2
Re = 1

dataescape = pd.read_csv("ApatityOTSO.csv")
dataescape = dataescape[dataescape['Filter'] == 1]

Ex = dataescape["Xgeo"]
Ey = dataescape["Ygeo"]
Ez = dataescape["Zgeo"]

xGSM = []
yGSM = []
zGSM = []

for a,b,c in zip(Ex,Ey,Ez):
    NewPosition = LarsenLib.coordtrans([a,b,c], DateArray[0], DateArray[1], DateArray[5], "GEO", "GSM")
    xGSM.append(NewPosition[0])
    yGSM.append(NewPosition[1])
    zGSM.append(NewPosition[2])


# data = pd.read_csv("PositionData.csv")
# R = 6371.2
# Re = 1

# X = data["X"]
# Y = data["Y"]
# Z = data["Z"]

# xGSMT = []
# yGSMT = []
# zGSMT = []

# for a,b,c in zip(X,Y,Z):
#     NewPosition = LarsenLib.coordtrans([a/R,b/R,c/R], DateArray[0], DateArray[1], DateArray[5], "GEO", "GSM")
#     xGSMT.append(NewPosition[0])
#     yGSMT.append(NewPosition[1])
#     zGSMT.append(NewPosition[2])


dataescape = pd.read_csv("Apatity.csv")
dataescape = dataescape[dataescape['Filter'] == 1]

Ex1 = dataescape["Xgeo"]
Ey1 = dataescape["Ygeo"]
Ez1 = dataescape["Zgeo"]

xGSM1 = []
yGSM1 = []
zGSM1 = []

for a,b,c in zip(Ex1,Ey1,Ez1):
    NewPosition = LarsenLib.coordtrans([a,b,c], DateArray[0], DateArray[1], DateArray[5], "GEO", "GSM")
    xGSM1.append(NewPosition[0])
    yGSM1.append(NewPosition[1])
    zGSM1.append(NewPosition[2])



fig = plt.figure(figsize=(4,4))

ax = fig.add_subplot(projection='3d')

u = np.linspace(0, 2 * np.pi, 20)
v = np.linspace(0, np.pi, 20)
x = Re * np.outer(np.cos(u), np.sin(v))
y = Re * np.outer(np.sin(u), np.sin(v))
z = Re * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_wireframe(x, y, z, color='blue')

ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")

plt.gca().set_aspect('auto', adjustable='box')

plt.xlim(-100, 100)
plt.ylim(-100, 100)
ax.set_zlim(-100, 100)

#ax.scatter(Ex, Ey, Ez, color = 'black')
ax.scatter(xGSM, yGSM, zGSM, color = 'black')
ax.scatter(xGSM1, yGSM1, zGSM1, color = 'red')
#ax.scatter(xGSMT, yGSMT, zGSMT, color = 'black')

plt.show()