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

data = pd.read_csv("Trajectory.csv")
R = 6371.2
Re = 1

X = data["X"]
Y = data["Y"]
Z = data["Z"]

xGSM = []
yGSM = []
zGSM = []

fig = plt.figure(figsize=(4,4))

ax = fig.add_subplot(projection='3d')

u = np.linspace(0, 2 * np.pi, 20)
v = np.linspace(0, np.pi, 20)
x = R * np.outer(np.cos(u), np.sin(v))
y = R * np.outer(np.sin(u), np.sin(v))
z = R * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_wireframe(x, y, z, color='blue')

ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")

plt.gca().set_aspect('auto', adjustable='box')

plt.xlim(-10000, 10000)
plt.ylim(-10000, 10000)
ax.set_zlim(-10000, 10000)

ax.plot(X, Y, Z, color = 'black')


plt.show()