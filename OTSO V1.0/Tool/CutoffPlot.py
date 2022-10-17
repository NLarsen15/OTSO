import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches

data = pd.read_csv("OuluOulu Example.csv")

R = data["Rigidity(GV)"]
data.loc[data['Filter'] == -1, 'Filter'] = 0
filter = data["Filter"]
filter2 = []

Ru = 0.738
Rl = 0.474
Rc = 0.636

current = 0

for x in filter:
    if (x == -1):
        x = 0

for x in filter:
    b = 1 - x
    filter2.append(b)



plt.bar(R, filter2, bottom=None, width = 0.001, color="black")
plt.xlabel("Rigidity [GV]", fontsize = 20)
plt.plot([], [], ' ', label="Ru: 0.789")
plt.plot([], [], ' ', label="Rc: 0.679")
plt.plot([], [], ' ', label="Rl:  0.508")
#plt.title("Example Oulu Cut-off", fontsize = 20)
plt.xlim([0.4, 0.85])
plt.xticks(fontsize= 18)
plt.tight_layout()
plt.legend()
ax = plt.gca()
ax.axes.yaxis.set_visible(False)
ax.set_ylim([0, 1])

plt.show()