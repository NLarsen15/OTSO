subroutine ccm(lambda, phi, North, East, Down)
implicit none

real(8) :: lambda, phi, North(3), East(3), Down(3)

North(1) = -sin(lambda)*cos(phi)
North(2) = -sin(lambda)*sin(phi)
North(3) = cos(lambda)

East(1) = -sin(phi)
East(2) = cos(phi)
East(3) = 0

Down(1) = -cos(lambda)*cos(phi)
Down(2) = -cos(lambda)*sin(phi)
Down(3) = -sin(lambda)

end subroutine ccm

subroutine VectorConversion(North, East, Down, Vector, NewVector)
implicit none

real(8) :: North(3), East(3), Down(3)
real(8) :: Vector(3), NewVector(3)

NewVector(1) = (Vector(1)*North(1)) + (Vector(2)*East(1)) + (Vector(3)*Down(1))
NewVector(2) = (Vector(1)*North(2)) + (Vector(2)*East(2)) + (Vector(3)*Down(2))
NewVector(3) = (Vector(1)*North(3)) + (Vector(2)*East(3)) + (Vector(3)*Down(3))

end subroutine VectorConversion


subroutine Vector_Local2Geo(Vector, latitude, longitude, NewVector)
implicit none
    
real(8) :: Vector(3), NewVector(3), latitude, longitude
real(8) :: lambda, phi, North(3), East(3), Down(3)
real(8), parameter :: pi  = 4 * atan(1.0_8)
    
!f2py intent(in) Vector, latitude, longitude
!f2py intent(out) NewVector
    
lambda = (pi / 180.0)*latitude
phi = (pi / 180.0)*longitude
    
call ccm(lambda, phi, North, East, Down)
    
call VectorConversion(North, East, Down, Vector, NewVector)
    
end subroutine Vector_Local2Geo

subroutine Vector_Geo2Local(Vector, latitude, longitude, NewVector)
implicit none
real(8) :: Vector(3), NewVector(3), latitude, longitude
real(8) :: lambda, phi, North(3), East(3), Down(3)
real(8), parameter :: pi  = 4 * atan(1.0_8)
   
!f2py intent(in) Vector, latitude, longitude
!f2py intent(out) NewVector
       
lambda = (pi / 180.0)*latitude
phi = (pi / 180.0)*longitude
       
call ccm(lambda, phi, North, East, Down)
   
NewVector(1) = (Vector(1) * North(1)) + (Vector(2)*North(2)) + (Vector(3)*North(3))
NewVector(2) = (Vector(1) * East(1)) + (Vector(2)*East(2)) + (Vector(3)*East(3))
NewVector(3) = (Vector(1) * Down(1)) + (Vector(2)*Down(2)) + (Vector(3)*Down(3))
   
end subroutine Vector_Geo2Local

subroutine LatGDZ2GEO(position, latGEO)
implicit none

real(8) :: position(3), h, f, a, mu, lat, latGEO
real(8), parameter :: pi  = 4 * atan(1.0_8)
real(8) :: e, N

IF (position(2) == 0.0) THEN
    latGEO = 0.0
 ELSE IF (position(2) /= 0.0) THEN
    

 mu = (pi/180.0) * position(2)
 h = position(1)*1000.0
 f = 1.0/298.257223563
 a = 6378137.0

 e = f/(2.0-f)
 N = a / (1.0-(e*(sin(mu)**2.0)))**(0.5)


 lat = atan((1-e)*( N / N + h )* tan(mu))

 lat = lat * (180.0/pi)

 IF (lat < 0.0) THEN
    latGEO = -90 - lat
 ELSE IF (lat > 0.0 ) THEN
    latGEO = 90 - lat
 END IF

END IF

end subroutine LatGDZ2GEO

subroutine Rotate(Vector, Zenith, Azimuth, NewVector)
implicit none
real(8) :: Vector(3), Zenith, Azimuth, NewVector(3), TempVector(3), NewZenith, NewAzimuth
real(8), parameter :: pi  = 4 * atan(1.0_8)

NewZenith = -(pi / 180.0)*Zenith
NewAzimuth = (pi / 180.0)*Azimuth

TempVector(1) = Vector(1)*cos(NewZenith) + Vector(3)*sin(NewZenith)
TempVector(2) = Vector(2)
TempVector(3) = -Vector(1)*sin(NewZenith) + Vector(3)*cos(NewZenith)

NewVector(1) = TempVector(1)*cos(NewAzimuth) - TempVector(2)*sin(NewAzimuth)
NewVector(2) = TempVector(1)*sin(NewAzimuth) + TempVector(2)*cos(NewAzimuth)
NewVector(3) = TempVector(3)

end subroutine Rotate