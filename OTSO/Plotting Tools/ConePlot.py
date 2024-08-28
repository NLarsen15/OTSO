import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from datetime import datetime, timedelta

# Defining the Figure
##############################################################
fig = plt.figure(figsize=(12,9))

Date = datetime(2006, 12, 13, 3, 00, 00)
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

# Plotting (Change read in csv files as desired)
###############################################################################################
# Oulu

Data = pd.read_csv("Oulu.csv")
Data = Data.drop(Data.index[-1])
Data = Data.astype(float)
first_instance_index = Data.index[Data['Filter'] != 1].min()
if not pd.isna(first_instance_index):
    Data = Data.iloc[:first_instance_index + 1]
Data = Data[Data['Filter'] == 1]

Lat = Data["Latitude"]
Long = Data["Longitude"]

Lat = pd.to_numeric(Lat, errors='coerce')
plt.scatter(Long, Lat, marker='.', s=0.5, label = "Oulu")

###############################################################################################
# Rome

Data = pd.read_csv("Rome.csv")
Data = Data.drop(Data.index[-1])
Data = Data.astype(float)
first_instance_index = Data.index[Data['Filter'] != 1].min()
if not pd.isna(first_instance_index):
    Data = Data.iloc[:first_instance_index + 1]
Data = Data[Data['Filter'] == 1]

Lat = Data["Latitude"]
Long = Data["Longitude"]

Lat = pd.to_numeric(Lat, errors='coerce')
plt.scatter(Long, Lat, marker='.', s=0.5, label = "Rome")

################################################################################################

plt.show()