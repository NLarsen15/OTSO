import math


def TSY01_Constants(By,Bz,V,N):
    G1 = 0
    G2 = 0
    G3 = 0

    By = By
    Bz = Bz
    V = V
    W = 1

    B = (By*By + Bz*Bz)**(0.5)
    h = (((B/40)**(2))/(1 + B/40))

    if(By == 0 and Bz == 0):
        phi = 0
    else:
        phi = math.atan2(By,Bz)
        if(phi <= 0):
            phi = phi + 2*math.pi

    if(Bz < 0):
        Bs = abs(Bz)
    elif Bz >= 0:
        Bs = 0
    
    G1 = G1 + (W)*V*h*(math.sin(phi/2)**3)
    G2 = G2 + (0.005)*(W)*(V)*Bs
    G3 = G3 + (N*V*Bs)/2000

    return G1, G2, G3
    