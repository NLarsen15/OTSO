import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from datetime import datetime

Date = datetime(2006, 12, 13, 3, 00, 00)

# Oulu
Planet = pd.read_csv("Planet_GLE65_TSY89.csv")

PlanetLat = Planet["Latitude"]
PlanetLong = Planet["Longitude"]
PlanetR = Planet["Rc"]

PlanetLat = np.array([PlanetLat])
PlanetLong = np.array([PlanetLong])
PlanetR = np.array([PlanetR])

PlanetLat = np.ndarray.flatten(PlanetLat)
PlanetLong = np.ndarray.flatten(PlanetLong)
PlanetR = np.ndarray.flatten(PlanetR)

##############################################################

fig = plt.figure(figsize=(12,9))

ax = fig.add_subplot(1, 1, 1,projection=ccrs.PlateCarree())
ax.set_global()
gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, color='black', alpha=0.5, linestyle='-', draw_labels=True)
ax.coastlines()
#ax.add_feature(Nightshade(Date, alpha=0.2))
gl.xlabels_top = None
gl.xlabels_bottom = None
gl.ylabels_left = None
gl.ylabels_right = None
gl.xlines = True
ax.set_extent([-180, 180, -90, 90]) 

ax.set_xticks([-180,-150,-120,-90,-60,-30,0,30,60,90,120,150,180])
ax.set_yticks([-90,-60,-30,0,30,60,90])

vmin = PlanetR.min()
vmax = PlanetR.max()

PlanetDf = pd.DataFrame({'x':PlanetLong, 'y':PlanetLat, 'z':PlanetR})

Z = PlanetDf.pivot_table(index='x', columns='y', values='z').T.values

X_unique = np.sort(PlanetDf.x.unique())
Y_unique = np.sort(PlanetDf.y.unique())
X, Y = np.meshgrid(X_unique, Y_unique)

plt.contourf(X, Y, Z, np.linspace(0.0, 20.0, 20), cmap="plasma", transform=ccrs.PlateCarree())

#plt.title('GLE 65 Planetary Vertical Rigidity Cutoff', fontsize=15)
plt.colorbar(ticks=[0, 4, 8, 12, 16, 20], label='Cutoff Rigidity [GV]')
plt.show()