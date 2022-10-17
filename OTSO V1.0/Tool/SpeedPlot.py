import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from datetime import datetime, timedelta



Data = pd.read_csv("Speed Tests.csv")

GyroPercent = Data['Gyrofrequency Percentage']
Time = Data['Time']
Rl = Data['Rl']
Rc = Data['Rc']
Ru = Data['Ru']


fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

twin1 = ax.twinx()

p1, = ax.plot(GyroPercent,Time, "black", label="Time [s]")
p2, = twin1.plot(GyroPercent, Rc, "red", label="Effective Cut-off Rigidity [GV]")

ax.set_xlabel("Gyrofrequency Max Percentage")
ax.set_ylabel("Time [s]")
twin1.set_ylabel("Effective Cut-off Rigidity [GV]")

ax.yaxis.label.set_color(p1.get_color())
#twin1.yaxis.label.set_color(p2.get_color())

tkw = dict(size=4, width=1.5)
#ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
#twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
#ax.tick_params(axis='x', **tkw)

ax.legend(handles=[p1, p2], loc='upper center')
plt.tight_layout()
plt.show()
