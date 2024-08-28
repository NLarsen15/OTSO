! ************************************************************************************************************************************
! Particle.f95 - File responsible for the creation of the CR and defining its parameters for the computation, as well as assigning 
! the simulation's date and magnetic field models to be used.
!
! ************************************************************************************************************************************
! subroutine CreateParticle:
! Subroutine responsible for calculating and assigning values to variables relating to the CR itself to be used throughout the
! computations.
!
! INPUT:
! StartPosition - origin of the CR on Earth
! Rigidity - Rigidity of the CR
! Date - Date that the similation is being done for
! Atomic - Atomic number of the CR
! Anti - binary integer 1 or 0. 1 means the CR is is the anti version and the charge is reversed, 0 is a normal particle.
!        e.g. 1 = antiproton, 0 = proton
! mode - Contains data for which magnetic field model shall be used
!
! OUTPUT:
! Updates parameters within the modules for the simulation. Defining the conditions of the simulation.
!
! ************************************************************************************************************************************
subroutine CreateParticle(StartPosition, Rigidity, Date, Atomic, Anti, mode)
USE Particle
USE SolarWind
implicit none
real(8) :: V(3), StartPosition(5), Date(6), Rigidity, Norm(3), VelocityGEO(3)
integer(8) :: Anti, Atomic, mode(2)
real(8) :: LocalVector(3), RotatedVelocity(3), GEOVelocity(3), Re, w

Re = 6371.2

call Reset()

call initialize()

Position(1) = StartPosition(1)
Position(2) = StartPosition(2)
Position(3) = StartPosition(3)
R = Rigidity
year = INT(Date(1))
day = INT(Date(2))
hour = INT(Date(3))
minute = INT(Date(4))
secondINT = INT(Date(5))
secondTotal = real(Date(6))

call RECALC_08(year, day, hour, minute, secondINT, SW(1), SW(2), SW(3))

IF (Anti == 1) THEN
    q_0 = -1.0 * q_0
END IF

IF (Atomic == 0) THEN ! Electron
    A = 1.0
    Z = 1.0
    m = 9.10938356e-31
    q = -1.0 * q

 ELSE IF (Atomic == 1) THEN ! Hydrogen
    A = 1.0
    Z = 1.0
    
 ELSE IF (Atomic == 2) THEN ! Helium
    A = 4.0
    Z = 2.0
    
 ELSE IF (Atomic == 3) THEN ! Lithium
    A = 7.0
    Z = 3.0

 ELSE IF (Atomic == 4) THEN ! Beryllium
    A = 9.0
    Z = 4.0
 
 ELSE IF (Atomic > 4) THEN
    print *, "Values above Z=4 not supported need to be added by user. Please edit the Particle.f95 file accordingly."
    stop
 END IF

 call update(mode)

 call Rigidity2velocity(V)

 call NormalVector(StartPosition, Norm)

 call VelocityComponents(V, Norm)

 if (model(1) /= 4) then
   call CoordinateTransform("GSM", "GEO", year, day, secondTotal, Velocity, VelocityGEO)
 ELSE
   VelocityGEO = Velocity
 end if

 call Vector_Geo2Local(VelocityGEO, StartPosition(2), StartPosition(3), LocalVector)

 call Rotate(LocalVector, StartPosition(4), StartPosition(5), RotatedVelocity)

 call Vector_Local2Geo(RotatedVelocity, StartPosition(2), StartPosition(3), GEOVelocity)

 if (model(1) /= 4) then
   call CoordinateTransform("GEO", "GSM", year, day, secondTotal, GEOVelocity, Velocity)
 ELSE
   Velocity = GEOVelocity
 end if

 w = (velocity(1)*velocity(1) + velocity(2)*velocity(2) + velocity(3)*velocity(3))**(0.5)
 MaxT = Re*1000**(-2.0) / (w/1000)


end subroutine CreateParticle