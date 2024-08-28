import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

################################################################################################
# Change csv file to desired csv file
data = pd.read_csv("Oulu.csv")
################################################################################################
# Plotting
last_row = data.iloc[-1].copy()

row_string = ','.join(str(value) for value in last_row if pd.notna(value))
items = row_string.split(", ")

for item in items:
    key, value = item.split(":")
    key = key.strip()
    value = float(value)
    
    if key == "Ru":
        Ru = value
    elif key == "Rc":
        Rc = value
    elif key == "Rl":
        Rl = value

df = data.drop(data.index[-1])
data = df.astype(float)
diff = data['Rigidity(GV)'].diff()

R = data["Rigidity(GV)"]
Rmax = R.max()
data.loc[data['Filter'] == -1, 'Filter'] = 0
filter = data["Filter"]
filter2 = []

current = 0

for x in filter:
    if (x == -1):
        x = 0

for x in filter:
    b = 1 - x
    filter2.append(b)

lowlim = Rl - 0.1
if lowlim < 0:
    lowlim = 0

highlim = Ru + 0.1
if highlim > Rmax:
    highlim = Rmax

plt.bar(R, filter2, bottom=None, width = diff, color="black")
plt.xlabel("Rigidity [GV]", fontsize = 20)
plt.plot([], [], ' ', label="Ru: " + str(Ru))
plt.plot([], [], ' ', label="Rc: " + str(Rc))
plt.plot([], [], ' ', label="Rl:  " + str(Rl))
#plt.title("Example Title", fontsize = 20)
plt.xlim([lowlim, highlim])
plt.xticks(fontsize= 18)
plt.tight_layout()
plt.legend()
ax = plt.gca()
ax.axes.yaxis.set_visible(False)
ax.set_ylim([0, 1])

plt.show()