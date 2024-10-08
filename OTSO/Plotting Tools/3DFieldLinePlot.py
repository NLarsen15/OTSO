import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# This code will read all csv files within a folder and show them in 3d space.
# copy this code to your desired folder or add the folder directory.
# A plot will be created showing the magnetic field lines around the Earth

# You can replace the os.getcwd() with your own directory path otherwise it will use the current directory
folder_path = os.getcwd() 
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

R = 6371.2
Re = 1

xGSM = []
yGSM = []
zGSM = []

fig = plt.figure(figsize=(10,10))

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

for file in csv_files:
        file_path = os.path.join(folder_path, file)
        
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Extract XYZ coordinates
        X = df['X']
        Y = df['Y']
        Z = df['Z']

        ax.plot(X, Y, Z, color = 'black', zorder = 10000)


plt.show()