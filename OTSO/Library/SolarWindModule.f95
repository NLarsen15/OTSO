!*********************************************************************************************************************************
! SolarWindModule.f95 - Module file that contains the solar wind data that is used throughout the computation. Also contains
! the subroutine that initializes this data
!
!********************************************************************************************************************************
module SolarWind
real(8) :: SW(3), IMF(2), Dst, PDYN, clock, B, Bs, PI, hb, G1, G2
integer(4) :: IOPT
real(8), Dimension(10) :: parmod
SAVE
contains


!*********************************************************************************************************************************
! subroutine InitializeWind:
! Subroutine designed to assign values to the solar wind variables within the solar wind module. Solar wind data and magnetospheric
! condition data is needed to accuratly model the magnetopshere at the time the user wants the computation to take place.
!
!
! INPUT:
! X(10) - list of important solar wind parameters
!         X(1) - Solar wind velocity (x axis) [km/s]
!         X(2) - Solar wind velocity (y axis) [km/s]
!         X(3) - Solar wind velocity (z axis) [km/s]
!         X(4) - IMF (y axis) [nT]
!         X(5) - IMF (z axis) [nT]
!         X(6) - Solar wind density [cm^-2]
!         X(7) - Dst Index [nT]
!         X(8) - G1 (Needed for the use of Tsyganenko 2001)
!         X(9) - G2 (Needed for the use of Tsyganenko 2001)
!         X(10) - G3 (Needed for the use of Tsyganenko 2001 - Storm)
!
! D - IOPT
! Model - Magnetic field models to be used
!
! OUTPUT:
! Solar wind variables within the module are assigned values for use throughout the computations
!
!********************************************************************************************************************************
subroutine initializeWind(X,D,model)
real(8) :: X(16), Vmax
integer(4) :: D
integer(8) :: model(2)

PI = 4.D0*DATAN(1.D0)

IF (X(1) == 0.0) THEN
 SW(1) = -400.0
 SW(2) = 0.0
 SW(3) = 0.0
ELSE
 SW(1) = X(1)
 SW(2) = X(2)
 SW(3) = X(3)
END IF

IMF(1) = X(4)
IMF(2) = X(5)

B = (X(4)**2 + X(5)**2)**(0.5)
Dst = X(7)
Vmax = (SW(1)**2 + SW(2)**2 + SW(3)**2)**0.5
PDYN = (X(6)*10**6.0) * (1.672621898e-27) * ((Vmax*1000)**2)
hb = ((B/40)**2 / (1 + (B/40)))


clock = ATAN(X(4)/X(5))

IOPT = D

parmod(1) = PDYN*10**(9.0)
parmod(2) = Dst
parmod(3) = X(4)
parmod(4) = X(5)

IF (model(2) == 5) THEN
    parmod(5) = X(8)
    parmod(6) = X(9)
END IF

IF (model(2) == 6) THEN
    parmod(5) = X(9)
    parmod(6) = X(10)
END IF

IF (model(2) == 7) THEN
    parmod(5) = X(11)
    parmod(6) = X(12)
    parmod(7) = X(13)
    parmod(8) = X(14)
    parmod(9) = X(15)
    parmod(10) = X(16)
END IF


end subroutine initializeWind


end module SolarWind