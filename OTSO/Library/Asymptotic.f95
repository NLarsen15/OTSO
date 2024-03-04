! ************************************************************************************************************************************
! Asymptotic.f95 - File responsible for calculating the asymptotic positions at a given point in the magnetosphere.
!
! ************************************************************************************************************************************
! subroutine AsymptoticDirection:
! Subroutine used to calculate the asymptotic latitude and longitude based on the coordinates of the CR.
!
! INPUT:
! Values from the particle module are used
!
! OUTPUT:
! lat - asymptotic latitude
! long - asymptotic longitude
!
! ************************************************************************************************************************************
subroutine AsymptoticDirection(Lat, Long)
USE Particle
implicit none
real(8) :: Lat, Long, E, top, bottom
real(8) :: GSW(3), GEO(3), XGEO(3), theta
real(8) :: GEOsph(3), NewLat, tr, tTHETA, tPHI
real(8), parameter :: pi  = 4 * atan(1.0_8)

call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, Position, XGEO)

call GSWGSM_08 (Velocity(1),Velocity(2),Velocity(3),GSW(1),GSW(2),GSW(3),-1)

call GEOGSW_08 (GEO(1),GEO(2),GEO(3),GSW(1),GSW(2),GSW(3),-1)

call SPHCAR_08(GEOsph(1),GEOsph(2),GEOsph(3),XGEO(1), XGEO(2), XGEO(3), -1)

if (model(1) == 4) then
    GEO(1) = Velocity(1)
    GEO(2) = Velocity(2)
    GEO(3) = Velocity(3)
end if

call BCARSP_08(XGEO(1),XGEO(2),XGEO(3),GEO(1),GEO(2),GEO(3),tr,tTHETA,tPHI)

theta = GEOsph(2)
NewLat = 90 - (theta / (pi/180))

top = -tTHETA*sin(theta) + tr*cos(theta)
bottom = (tPHI**2 + (tTHETA*cos(theta) + tr*sin(theta))**2)**(0.5)

Lat = atan2(top,bottom)

E = atan2(tPHI,(tTHETA*cos(theta) + tr*sin(theta)))

Long = GEOsph(3) + E

Long = Long/(pi/180)

IF(Long > 360) THEN
    Long = Long - 360
ELSE IF(Long < 0) THEN
    Long = 360 + Long
END IF

Lat = Lat/(pi/180)

end subroutine AsymptoticDirection