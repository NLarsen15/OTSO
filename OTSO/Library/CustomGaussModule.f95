module CUSTOMGAUSS
COMMON /CUSTGAUSS/CUSTG(105),CUSTH(105)
REAL(8) :: CUSTG,CUSTH
INTEGER(4) :: CUSTGAUSS


!Currently set to 1970 IGRF coefficents as an example. To change, please replace
!with your own coefficients.

DATA CUSTG/0.D0,-30220.D0,-2068.D0,-1781.D0,3000.D0,1611.D0,1287.D0, &
-2091.D0,1278.D0,838.D0,952.D0,800.D0,461.D0,-395.D0,234.D0, &
-216.D0,359.D0,262.D0,-42.D0,-160.D0,-56.D0,43.D0,64.D0,15.D0, &
-212.D0,2.D0,3.D0,-112.D0,72.D0,-57.D0,1.D0,14.D0,-22.D0,-2.D0, &
13.D0,-2.D0,14.D0,6.D0,-2.D0,-13.D0,-3.D0,5.D0,0.D0,11.D0,3.D0, &
8.D0,10.D0,2.D0,-12.D0,10.D0,-1.D0,0.D0,3.D0,1.D0,-1.D0,-3.D0, &
-3.D0,2.D0,-5.D0,-1.D0,6.D0,4.D0,1.D0,0.D0,3.D0,-1.D0,39*0.D0/
DATA CUSTH/0.D0,0.D0,5737.D0,0.D0,-2047.D0,25.D0,0.D0,-366.D0, &
251.D0,-196.D0,0.D0,167.D0,-266.D0,26.D0,-279.D0,0.D0,26.D0, &
139.D0,-139.D0,-91.D0,83.D0,0.D0,-12.D0,100.D0,72.D0,-37.D0,-6.D0, &
1.D0,0.D0,-70.D0,-27.D0,-4.D0,8.D0,23.D0,-23.D0,-11.D0,0.D0,7.D0, &
-15.D0,6.D0,-17.D0,6.D0,21.D0,-6.D0,-16.D0,0.D0,-21.D0,16.D0,6.D0, &
-4.D0,-5.D0,10.D0,11.D0,-2.D0,1.D0,0.D0,1.D0,1.D0,3.D0,4.D0,-4.D0, &
0.D0,-1.D0,3.D0,1.D0,-4.D0,39*0.D0/
SAVE
contains

subroutine initializeCustomGauss(model)
integer(8) :: model(2)
              
IF (model(1) == 3) THEN
    CUSTGAUSS = 1
ELSE
    CUSTGAUSS = 0
END IF
        
end subroutine initializeCustomGauss
end module CUSTOMGAUSS

