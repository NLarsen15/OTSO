import numpy as np
import PIL
from PIL import Image, ImageTk
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

data = pd.read_csv("Trajectory.csv")
R = 6371.2
Re = 1

# Earth
bm = PIL.Image.open('bluemarble.jpg')
bm = np.array(bm.resize([d for d in bm.size]))/256.
lons = np.linspace(-180, 180, bm.shape[1]) * np.pi/180 
lats = np.linspace(-90, 90, bm.shape[0])[::-1] * np.pi/180 

X = data["X"]
Y = data["Y"]
Z = data["Z"]

xGSM = []
yGSM = []
zGSM = []

fig = plt.figure(figsize=(4,4))

ax = fig.add_subplot(projection='3d')

x = R * np.outer(np.cos(lons), np.cos(lats)).T
y = R * np.outer(np.sin(lons), np.cos(lats)).T
z = R * np.outer(np.ones(np.size(lons)), np.sin(lats)).T
ax.plot_surface(x, y, z, rstride=4, cstride=4, facecolors = bm)
#ax.cla()

ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")

plt.gca().set_aspect('auto', adjustable='box')

plt.xlim(-100000, 100000)
plt.ylim(-100000, 100000)
ax.set_zlim(-100000, 100000)

ax.plot(X, Y, Z, color = 'red')


plt.show()