import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from datetime import datetime, timedelta


#Date = datetime(2021, 10, 28, 16, 00, 00)
# Oulu
Data = pd.read_csv("OuluOulu Example 2.csv")

LastIndex = Data[Data['Filter'].lt(1)].index[0]
CroppedData = Data[Data.index < LastIndex]

Lat = Data["Latitude"]
Long = Data["Longitude"]

Lat = CroppedData["Latitude"]
Long = CroppedData["Longitude"]

Lat = pd.to_numeric(Lat, errors='coerce')

#row = TOulu.iloc[10000]
#OuluLat = row["Latitude"]
#OuluLat = pd.to_numeric(OuluLat, errors='coerce')
#OuluLong = row["Longitude"]

#if (OuluLong > 180):
#    OuluLong = OuluLong - 360
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

# Plotting

plt.scatter(Long, Lat, color='red', marker='.', s=0.5)
#plt.text(OuluLong,OuluLat,"Oulu", color='black')

#plt.title('Oulu Asymptotic Cone GLE73', fontsize=20)

plt.show()