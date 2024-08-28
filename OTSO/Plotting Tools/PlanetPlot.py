import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
import matplotlib.ticker as mticker

################################################################################################
# Change csv file to desired csv file
df = pd.read_csv('Planet.csv')
###############################################################################################


lats = df['Latitude'].values
lons = df['Longitude'].values
totals = df['Rc'].values

grid_lon, grid_lat = np.meshgrid(
    np.linspace(lons.min(), lons.max(), 100),
    np.linspace(lats.min(), lats.max(), 100)
)

grid_total = griddata((lats, lons), totals, (grid_lat, grid_lon), method='linear')

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()},figsize=(10, 8))
ax.set_global()

# Add coastlines and other features
ax.coastlines()
#ax.add_feature(cfeature.BORDERS, linestyle=':')
#ax.add_feature(cfeature.LAND, edgecolor='black')
#ax.add_feature(cfeature.OCEAN, edgecolor='black')
#ax.add_feature(cfeature.LAKES, alpha=0.65)
#ax.add_feature(cfeature.RIVERS)

################################################################################################
# Change the colour bar range as desired
contour_levels = np.arange(0, 20.5, 0.5)
################################################################################################

contour = ax.contourf(grid_lon, grid_lat, grid_total, levels = contour_levels, transform=ccrs.PlateCarree(), cmap = 'viridis', vmin = 0, vmax = 20)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2,  color='grey', alpha=0.2, linestyle='--', zorder = 100)


gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])

gl.xlabel_style = {'size': 15}
gl.ylabel_style = {'size': 15}

gl.xformatter = plt.FuncFormatter(lambda x, _: f"{int(x)}°")
gl.yformatter = plt.FuncFormatter(lambda y, _: f"{int(y)}°")

gl.bottom_labels = gl.right_labels = False
gl.ylabels_right = None

cbar = plt.colorbar(contour, ax=ax, orientation='horizontal', pad=0.03, aspect=40, shrink=1.0)
cbar.set_ticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
cbar.set_label('Pc [GV]', fontsize=20)
cbar.ax.tick_params(labelsize=15)

plt.show()
