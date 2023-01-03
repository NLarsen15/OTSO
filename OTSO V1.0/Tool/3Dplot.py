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
R = 6371.2
Re = 1

data = pd.read_csv("Oulu1.csv")
X1 = data["X"]/R
Y1 = data["Y"]/R
Z1 = data["Z"]/R

data = pd.read_csv("Oulu0.6.csv")
X06 = data["X"]/R
Y06 = data["Y"]/R
Z06 = data["Z"]/R

data = pd.read_csv("Oulu0.5.csv")
X05 = data["X"]/R
Y05 = data["Y"]/R
Z05 = data["Z"]/R

data = pd.read_csv("Oulu0.4.csv")
X04 = data["X"]/R
Y04 = data["Y"]/R
Z04 = data["Z"]/R

data = pd.read_csv("Oulu0.3.csv")
X03 = data["X"]
Y03 = data["Y"]
Z03 = data["Z"]

data = pd.read_csv("Oulu0.2.csv")
X02 = data["X"]/R
Y02 = data["Y"]/R
Z02 = data["Z"]/R

data = pd.read_csv("Oulu0.1.csv")
X01 = data["X"]/R
Y01 = data["Y"]/R
Z01 = data["Z"]/R

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

ax.set_xlabel("$X_{GEO}$ [Re]")

ax.set_ylabel("$Y_{GEO}$ [Re]")

ax.set_zlabel("$Z_{GEO}$ [Re]")

plt.gca().set_aspect('auto', adjustable='box')

plt.xlim(-20, 20)
plt.ylim(-20, 20)
ax.set_zlim(-20, 20)

ax.plot(X1, Y1, Z1, color = 'red')
#ax.plot(X06, Y06, Z06, color = 'red')
#ax.plot(X05, Y05, Z05, color = 'green')
ax.plot(X04, Y04, Z04, color = 'green')
#ax.plot(X03, Y03, Z03, color = 'red')
#ax.plot(X02, Y02, Z02, color = 'red')
ax.plot(X01, Y01, Z01, color = 'purple')



plt.show()