! ************************************************************************************************************************************
! Runge_Kutta.f95 - File responsible for preforming the numerical integration for the equations of motion for the CR to compute 
! the trajectory. Subroutines to compute a rough time-step value are included also.
! ************************************************************************************************************************************
! subroutine RK4:
! 4th order Runge-Kutta method for solving the differential equations of motion for the CR's trajectory.
!
! INPUT:
! Variables used from the particle module 
!
! OUTPUT:
! Xnew - New position of CR [GSM coordinates]
! Vnew - New velocity of CR [m/s]
! XnewGDZ - New position of CR [GDZ coordinates]
!
! ************************************************************************************************************************************
subroutine RK4(Xnew, Vnew, XnewGDZ)
USE Particle

real(8) :: a0(3), x0(3), v0(3)
real(8) :: Xnew(3), Vnew(3), xGSM(3)
real(8) :: x1(3), v1(3), a1(3), Vabs, Vend
real(8) :: x2(3), v2(3), a2(3), x3(3), v3(3), a3(3), h1
real(8) :: x1GDZ(3), x2GDZ(3), x3GDZ(3), XnewTemp(3)
real(8) :: x1GSM(3), x2GSM(3), x3GSM(3), XnewGDZ(3)
real(8) :: a0MAG, a1MAG, a2MAG, a3MAG, loop
real(8) :: v0MAG, v1MAG, v2MAG, v3MAG, Verr, LOWVerr, Max

! Verr defines the maximum error allowed per Runge-Kutta step (smaller values = more accuracy, but slower computation time)
Verr = 0.0001
LOWVerr = 0.000001

x0(1) = Position(1) !Xx
x0(2) = Position(2) !Xy
x0(3) = Position(3) !Xz

v0(1) = Velocity(1) !Vx
v0(2) = Velocity(2) !Vy
v0(3) = Velocity(3) !Vz

v0MAG = ((v0(1)**2.0 + v0(2)**2.0 + v0(3)**2.0))**(0.5)

loop = 0

10 h1 = h*0.5
HOLD = h


call AccelerationCalc(Position, velocity, a0)
a0MAG = ((a0(1)**2.0 + a0(2)**2.0 + a0(3)**2.0))**(0.5)
call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)

! particle position in geocentric

xGSM(1) = xGSM(1)*6371200.0
xGSM(2) = xGSM(2)*6371200.0
xGSM(3) = xGSM(3)*6371200.0

!I now have particle position in GEO and the Acceleration in GEO

! n1 position
x1(1) = xGSM(1) + h1*v0(1)
x1(2) = xGSM(2) + h1*v0(2)
x1(3) = xGSM(3) + h1*v0(3)

v1(1) = v0(1) + h1*a0(1)
v1(2) = v0(2) + h1*a0(2)
v1(3) = v0(3) + h1*a0(3)

v1MAG = ((v1(1)**2.0 + v1(2)**2.0 + v1(3)**2.0))**(0.5)

IF (v1MAG > c) THEN
    h = h*0.5
!    loop = loop + 1
!    print *, "Faster than Light"
!    print *, "Loop ", loop 
    GOTO 10
END IF

!IF ((v1MAG - v0MAG)/v0MAG > Verr) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Beta Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

x1GSM(1) = x1(1)/6371200.0
x1GSM(2) = x1(2)/6371200.0
x1GSM(3) = x1(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x1GSM, x1GDZ)
call AccelerationCalc(x1GDZ, v1, a1)
a1MAG = ((a1(1)**2.0 + a1(2)**2.0 + a1(3)**2.0))**(0.5)

!IF ((a1MAG - a0MAG)/a0MAG > 0.15) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Acceleration Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

!n2 position
x2(1) = xGSM(1) + h1*v1(1)
x2(2) = xGSM(2) + h1*v1(2)
x2(3) = xGSM(3) + h1*v1(3)

v2(1) = v0(1) + h1*a1(1)
v2(2) = v0(2) + h1*a1(2)
v2(3) = v0(3) + h1*a1(3)

v2MAG = ((v2(1)**2.0 + v2(2)**2.0 + v2(3)**2.0))**(0.5)

IF ((v2MAG) > c) THEN
    h = h*0.5
!    loop = loop + 1
!    print *, "Faster than Light"
!    print *, "Loop ", loop 
    GOTO 10
END IF

!IF ((v2MAG - v0MAG)/v0MAG > Verr) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Beta Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

x2GSM(1) = x2(1)/6371200.0
x2GSM(2) = x2(2)/6371200.0
x2GSM(3) = x2(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x2GSM, x2GDZ)
call AccelerationCalc(x2GDZ, v2, a2)
a2MAG = ((a2(1)**2.0 + a2(2)**2.0 + a2(3)**2.0))**(0.5)

!IF ((a2MAG - a0MAG)/a0MAG > 0.15) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Acceleration Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

!n3 position
x3(1) = xGSM(1) + h*v2(1)
x3(2) = xGSM(2) + h*v2(2)
x3(3) = xGSM(3) + h*v2(3)

v3(1) = v0(1) + h*a2(1)
v3(2) = v0(2) + h*a2(2)
v3(3) = v0(3) + h*a2(3)

v3MAG = ((v3(1)**2.0 + v3(2)**2.0 + v3(3)**2.0))**(0.5)

IF ((v3MAG) > c) THEN
    h = h*0.5
!    loop = loop + 1
!    print *, "Faster than Light"
!    print *, "Loop ", loop 
    GOTO 10
END IF

!IF ((v3MAG - v0MAG)/v0MAG > Verr) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Beta Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

x3GSM(1) = x3(1)/6371200.0
x3GSM(2) = x3(2)/6371200.0
x3GSM(3) = x3(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x3GSM, x3GDZ)
call AccelerationCalc(x3GDZ, v3, a3)
a3MAG = ((a3(1)**2.0 + a3(2)**2.0 + a3(3)**2.0))**(0.5)

!IF ((a3MAG - a0MAG)/a0MAG > 0.15) THEN
!    h = h*0.5
!    loop = loop + 1
!    print *, "Acceleration Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

!n4 position

Xnew(1) = xGSM(1) + ( h * ( ( v0(1) + 2*v1(1) + 2*v2(1) + v3(1))/ 6.0 ) )
Xnew(2) = xGSM(2) + ( h * ( ( v0(2) + 2*v1(2) + 2*v2(2) + v3(2))/ 6.0 ) )
Xnew(3) = xGSM(3) + ( h * ( ( v0(3) + 2*v1(3) + 2*v2(3) + v3(3))/ 6.0 ) )

Vnew(1) = v0(1) + ( h * ( ( a0(1) + 2*a1(1) + 2*a2(1) + a3(1))/ 6.0 ) )
Vnew(2) = v0(2) + ( h * ( ( a0(2) + 2*a1(2) + 2*a2(2) + a3(2))/ 6.0 ) )
Vnew(3) = v0(3) + ( h * ( ( a0(3) + 2*a1(3) + 2*a2(3) + a3(3))/ 6.0 ) )

Vend = ((Vnew(1)**2.0 + Vnew(2)**2.0 + Vnew(3)**2.0))**(0.5)

IF ((Vend - v0MAG)/v0MAG > Verr) THEN
    h = h*0.5
!    loop = loop + 1
!    print *, "Beta Fail"
!    print *, "Loop ", loop 
    GOTO 10
END IF

XnewTemp(1) = Xnew(1)/6371200.0
XnewTemp(2) = Xnew(2)/6371200.0
XnewTemp(3) = Xnew(3)/6371200.0

secondTotal = secondTotal + h

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)

Vabs = ((Velocity(1)**2.0 + Velocity(2)**2.0 + Velocity(3)**2.0))**(0.5)
DistanceTraveled = DistanceTraveled + (h * Vabs)

Velocity(1) = Vnew(1)
Velocity(2) = Vnew(2)
Velocity(3) = Vnew(3)

Position(1) = XnewGDZ(1)
Position(2) = XnewGDZ(2)
Position(3) = XnewGDZ(3)

call NewMax(Max)

!h = h*1.1

IF ((Vend - v0MAG)/v0MAG < LOWVerr) THEN
    h = h*1.1
END IF

IF (h > Max) THEN
    h = Max
END IF

end subroutine RK4

! ************************************************************************************************************************************
! subroutine TimeStep:
! Subroutine that calculates the time-step size for the integration. Value is taken to be 5% of the gyration time for the CR in
! the magnetic field present at that point in space, magnetic field is assumed unform.
! Similar method is used in Smart and Shea (1981) except the time step is taken to be 1% of gyration time in their work.
!
! INPUT:
! B - Magnetic field stength [T]
!
! OUTPUT:
! Time-step value (h) is updated within the particle module
!
! REFERENCES:
! (1) Smart, D.F., Shea, M.A., 1981. Optimum Step Length Control for Cosmic-Ray Trajectory Calculations,
!     in: International Cosmic Ray Conference, p. 208.
!
! ************************************************************************************************************************************
subroutine TimeStep(B)
USE Particle
implicit none

real(8) :: B(3), MaxMulti, Max
real(8) :: p, Vmag, Bmag

Bmag = ((B(1)**2.0 + B(2)**2.0 + B(3)**2.0))**(0.5)
Bmag = Bmag * 10000.0
Vmag = ((Velocity(1)**2.0 + Velocity(2)**2.0 + Velocity(3)**2.0))**(0.5)
Vmag = Vmag / 1000.0

p = 33.33 * (R/Bmag)

h = (0.01 * p) / Vmag

MaxMulti = MaxGyroPercent
Max = (MaxMulti*p)/Vmag

IF (HOLD == 0) THEN
    h = h
ELSE IF (h > HOLD * 1.1) THEN
    h = HOLD*1.1
END IF

IF (h > Max ) THEN
    h = Max
END IF
end subroutine TimeStep

! ************************************************************************************************************************************
! subroutine FirstTimeStep:
! Subroutine that calculates the initial time-step size for the begining of the integration by calling the TimeStep subroutine.
!
! INPUT:
! Values from particle module
!
! OUTPUT:
! Time-step value (h) is updated within the particle module
!
! ************************************************************************************************************************************
subroutine FirstTimeStep()
USE particle
implicit none
real(8) :: Bfield(3)
    
call MagneticField(Position, Bfield)
call TimeStep(Bfield)

end subroutine FirstTimeStep

! ************************************************************************************************************************************
! subroutine NewMax:
! Subroutine that calls the functions in order to calculate the maximum time-step value.
!
! INPUT:
! Values from particle module
!
! OUTPUT:
! Max - Maximum time-step value [s]
!
! ************************************************************************************************************************************
subroutine NewMax(Max)
USE Particle
implicit none
real(8) :: Max, Bfield(3)

call MagneticField(Position, Bfield)
call TimeStepMax(Bfield,Max)

end subroutine NewMax

! ************************************************************************************************************************************
! subroutine TimeStepMax:
! Subroutine that calculates the maximum time-step size for the integration for a given magnetic field strength.
! The max value is taken to be 5% of the gyration time for the CR in the magnetic field present at that point in space, 
! magnetic field is assumed unform. This allows the time-step to grow as the CR enters weaker areas of magnetic field strength.
! Smart and Shea (1981) method is used except the max time step is taken to be 1.5% of gyration time in their work.
! Changing the value of the MaxMulti variable will alter the size of the maximum time-step and will impact the accuracy of the 
! computation accordingly.
!
! INPUT:
! B - Magnetic field stength [T]
!
! OUTPUT:
! Time-step value (h) is updated within the particle module
!
! REFERENCES:
! (1) Smart, D.F., Shea, M.A., 1981. Optimum Step Length Control for Cosmic-Ray Trajectory Calculations,
!     in: International Cosmic Ray Conference, p. 208.
!
! ************************************************************************************************************************************
subroutine TimeStepMax(B, Max)
USE Particle
implicit none
    
real(8) :: B(3), MaxMulti, Max
real(8) :: p, Vmag, Bmag
    
Bmag = ((B(1)**2.0 + B(2)**2.0 + B(3)**2.0))**(0.5)
Bmag = Bmag * 10000.0
Vmag = ((Velocity(1)**2.0 + Velocity(2)**2.0 + Velocity(3)**2.0))**(0.5)
Vmag = Vmag / 1000.0
    
p = 33.33 * (R/Bmag)
    
MaxMulti = MaxGyroPercent
Max = (MaxMulti*p)/Vmag
    
end subroutine TimeStepMax