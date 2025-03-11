import numpy as np

class Solar_Wind:
 def __init__(self, Vx, Vy, Vz, By, Bz, Density, Pdyn, Dst, G1, G2, G3, W1, W2, W3, W4, W5, W6):
    self.Vx = Vx
    self.Vy = Vy
    self.Vz = Vz
    self.By = By
    self.Bz = Bz
    self.Density = Density
    self.Pdyn = Pdyn
    self.Dst = Dst
    self.G1 = G1
    self.G2 = G2
    self.G3 = G3
    self.W1 = W1
    self.W2 = W2
    self.W3 = W3
    self.W4 = W4
    self.W5 = W5
    self.W6 = W6

    self.WindArray = np.array([self.Vx, self.Vy, self.Vz, self.By, self.Bz, self.Density, self.Pdyn, self.Dst, self.G1, self.G2, self.G3, self.W1, self.W2, self.W3, self.W4, self.W5, self.W6])

 def GetWind(self):
    return self.WindArray