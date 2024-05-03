! ************************************************************************************************************************************
! Integration.f95 - File responsible for preforming the numerical integration for the equations of motion for the CR to compute 
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
subroutine RK4()
USE Particle

real(8) :: a0(3), x0(3), v0(3)
real(8) :: Xnew(3), Vnew(3), xGSM(3)
real(8) :: x1(3), v1(3), a1(3), Vabs, Vend
real(8) :: x2(3), v2(3), a2(3), x3(3), v3(3), a3(3), h1
real(8) :: x1GDZ(3), x2GDZ(3), x3GDZ(3)
real(8) :: x1GSM(3), x2GSM(3), x3GSM(3), XnewGDZ(3)
real(8) :: a0MAG, a1MAG, a2MAG, a3MAG, loop
real(8) :: v0MAG, v1MAG, v2MAG, v3MAG, Verr, LOWVerr, Max

! Verr defines the maximum error allowed per Runge-Kutta step (smaller values = more accuracy, but slower computation time)
Verr = 0.00001
LOWVerr = 0.0000001

x0(1) = Position(1) !Xx
x0(2) = Position(2) !Xy
x0(3) = Position(3) !Xz

v0(1) = Velocity(1) !Vx
v0(2) = Velocity(2) !Vy
v0(3) = Velocity(3) !Vz

v0MAG = ((v0(1)**2.0 + v0(2)**2.0 + v0(3)**2.0))**(0.5)

loop = 0

IF (FinalStep >= 1) THEN
    h = Lasth
END IF

10 h1 = h*0.5
HOLD = h


call AccelerationCalc(Position, velocity, a0)
a0MAG = ((a0(1)**2.0 + a0(2)**2.0 + a0(3)**2.0))**(0.5)
call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)

if (model(1) == 4) then
    call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, x0, xGSM)
end if

! particle position in geocentric

xGSM(1) = xGSM(1)*6371200.0
xGSM(2) = xGSM(2)*6371200.0
xGSM(3) = xGSM(3)*6371200.0


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

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x1GSM, x1GDZ)
end if

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

!IF ((v2MAG - v1MAG)/v1MAG > Verr) THEN
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

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x2GSM, x2GDZ)
end if

call AccelerationCalc(x2GDZ, v2, a2)
a2MAG = ((a2(1)**2.0 + a2(2)**2.0 + a2(3)**2.0))**(0.5)

!IF ((a2MAG - a1MAG)/a1MAG > 0.15) THEN
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

!IF ((v3MAG - v2MAG)/v2MAG > Verr) THEN
!h = h*0.5
!    loop = loop + 1
!    print *, "Beta Fail"
!    print *, "Loop ", loop 
!    GOTO 10
!END IF

x3GSM(1) = x3(1)/6371200.0
x3GSM(2) = x3(2)/6371200.0
x3GSM(3) = x3(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x3GSM, x3GDZ)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x3GSM, x3GDZ)
end if

call AccelerationCalc(x3GDZ, v3, a3)
a3MAG = ((a3(1)**2.0 + a3(2)**2.0 + a3(3)**2.0))**(0.5)

!IF ((a3MAG - a2MAG)/a2MAG > 0.15) THEN
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

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
end if

Vabs = ((Velocity(1)**2.0 + Velocity(2)**2.0 + Velocity(3)**2.0))**(0.5)
call TimeCheck(Vabs)
DistanceTraveled = DistanceTraveled + (h * Vabs)

XnewTemp(1) = Xnew(1)
XnewTemp(2) = Xnew(2)
XnewTemp(3) = Xnew(3)

call OldVariables(Position,Velocity)
secondTotal = secondTotal + h

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
! subroutine Boris:
! Boris method for solving the differential equations of motion for the CR's trajectory.
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
subroutine Boris()
USE Particle
real(8) :: Bfield(3), v_plus(3), v_minus(3), v_prime(3), x0(3), v0(3), XGSM(3), xGDZ_half(3)
real(8) :: tb(3), sb(3), crossed1(3), crossed2(3), scaler, lam, x_half_GSM(3), x_half_GSM_Temp(3)
real(8) :: Xnew(3), Vnew(3), XnewGDZ(3), vabs1, vabs2, Max, LOWVerr, Verr, h1
   
Verr = 0.00001
LOWVerr = 0.0000001
    
x0(1) = Position(1) !Xx
x0(2) = Position(2) !Xy
x0(3) = Position(3) !Xz

call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)

if (model(1) == 4) then
    call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, x0, xGSM)
end if

xGSM(1) = xGSM(1)*6371200.0
xGSM(2) = xGSM(2)*6371200.0
xGSM(3) = xGSM(3)*6371200.0
    
v0(1) = Velocity(1) !Vx
v0(2) = Velocity(2) !Vy
v0(3) = Velocity(3) !Vz
    
Vabs1 = (v0(1)*v0(1) + v0(2)*v0(2) + v0(3)*v0(3))**(0.5)

IF (FinalStep >= 1) THEN
    h = Lasth
END IF
    
10 h1 = h*0.5

x_half_GSM(1) = xGSM(1) + (v0(1)/2.0)*h
x_half_GSM(2) = xGSM(2) + (v0(2)/2.0)*h
x_half_GSM(3) = xGSM(3) + (v0(3)/2.0)*h

lam = (1.0 - ((Vabs1/c)**2))**(-0.5)
scaler = (Q*h)/(2.0*lam*M)


x_half_GSM_Temp(1) = x_half_GSM(1)/6371200.0
x_half_GSM_Temp(2) = x_half_GSM(2)/6371200.0
x_half_GSM_Temp(3) = x_half_GSM(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)
end if

call MagneticField(xGDZ_half, Bfield)
call VecScale(scaler,Bfield,tb)
    
sb(1) = (2*tb(1))/(1+(tb(1)*tb(1)))
sb(2) = (2*tb(2))/(1+(tb(2)*tb(2)))
sb(3) = (2*tb(3))/(1+(tb(3)*tb(3)))
    
v_minus(1) = v0(1)
v_minus(2) = v0(2)
v_minus(3) = v0(3)
    
call VecCross(v_minus, tb, crossed1)
call VecAddition(v_minus, crossed1, v_prime)
call VecCross(v_prime, sb, crossed2)
call VecAddition(v_minus, crossed2, v_plus)
    
Xnew(1) = x_half_GSM(1) + (v_plus(1)*h)/(2)
Xnew(2) = x_half_GSM(2) + (v_plus(2)*h)/(2)
Xnew(3) = x_half_GSM(3) + (v_plus(3)*h)/(2)
    
Vnew(1) = v_plus(1)
Vnew(2) = v_plus(2)
Vnew(3) = v_plus(3)
    
XnewTemp(1) = Xnew(1)/6371200.0
XnewTemp(2) = Xnew(2)/6371200.0
XnewTemp(3) = Xnew(3)/6371200.0
    
call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
end if


call TimeCheck(Vabs1)
DistanceTraveled = DistanceTraveled + (h * Vabs1)
    
Vabs2 = ((Vnew(1)**2.0 + Vnew(2)**2.0 + Vnew(3)**2.0))**(0.5)

secondTotal = secondTotal + h
    
IF ((Vabs2 - Vabs1)/Vabs1 > Verr) THEN
    secondTotal = secondTotal - h
    DistanceTraveled = DistanceTraveled - (h * Vabs1)
    h = h*0.5
    GOTO 10
END IF

IF ((Vabs2 - Vabs1)/Vabs1 < LOWVerr) THEN
    h = h*1.1
END IF

call OldVariables(Position,Velocity)
    
XnewTemp(1) = Xnew(1)
XnewTemp(2) = Xnew(2)
XnewTemp(3) = Xnew(3)
    
Velocity(1) = Vnew(1)
Velocity(2) = Vnew(2)
Velocity(3) = Vnew(3)
    
Position(1) = XnewGDZ(1)
Position(2) = XnewGDZ(2)
Position(3) = XnewGDZ(3)
    
call NewMax(Max)
    
IF (h > Max) THEN
    h = Max
END IF
    
end subroutine Boris

! ************************************************************************************************************************************
! subroutine Vay:
! Vay method for solving the differential equations of motion for the CR's trajectory.
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
subroutine Vay()
USE Particle
implicit None
real(8) :: Bfield(3), x0(3), v0(3), XGSM(3), x_half_GSM(3), Un(3) 
real(8) :: Un_half(3), Uprime(3), Un_plus(3)
real(8) :: tau(3), tau1(3), Ustar, crossed1(3), scale1(3) 
real(8) :: x_half_GSM_Temp(3), xGDZ_half(3), scaler, lamN
real(8) :: Xnew(3), Vnew(3), XnewGDZ(3), vabs1, vabs2, Max
real(8) :: LOWVerr, Verr, h1, sigma, LamNPrime, oneoverlamda
real(8) :: tauDot, UprimeDot, LamndaN1, tnew(3), tnewDot, sfinal
real(8) :: Fcalc1, Fcalc2(3), Fcalc3(3), Fcalc4(3), Fcalc5(3)
    
Verr = 0.00001
LOWVerr = 0.0000001
    
x0(1) = Position(1) !Xx
x0(2) = Position(2) !Xy
x0(3) = Position(3) !Xz
    
call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)

if (model(1) == 4) then
    call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, x0, xGSM)
end if

xGSM(1) = xGSM(1)*6371200.0
xGSM(2) = xGSM(2)*6371200.0
xGSM(3) = xGSM(3)*6371200.0
    
v0(1) = Velocity(1) !Vx
v0(2) = Velocity(2) !Vy
v0(3) = Velocity(3) !Vz
    
Vabs1 = (v0(1)*v0(1) + v0(2)*v0(2) + v0(3)*v0(3))**(0.5)

IF (FinalStep >= 1) THEN
    h = Lasth
END IF
    
10 h1 = h*0.5

!Half update position x(n+1/2)
x_half_GSM(1) = xGSM(1) + (v0(1)/2.0)*h
x_half_GSM(2) = xGSM(2) + (v0(2)/2.0)*h
x_half_GSM(3) = xGSM(3) + (v0(3)/2.0)*h
    
lamN = (1.0 - ((Vabs1/c)**2))**(-0.5)
scaler = (Q*h)/(2.0*M)

Un(1) = v0(1)*lamN
Un(2) = v0(2)*lamN
Un(3) = v0(3)*lamN

x_half_GSM_Temp(1) = x_half_GSM(1)/6371200.0
x_half_GSM_Temp(2) = x_half_GSM(2)/6371200.0
x_half_GSM_Temp(3) = x_half_GSM(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)
end if

call MagneticField(xGDZ_half, Bfield)

call VecCross(v0, Bfield, crossed1)
call VecScale(scaler,crossed1,scale1)
call VecAddition(Un,scale1,Un_half)

!U(n+1/2) now determined
    
!UPrime
Uprime(1) = Un_half(1)
Uprime(2) = Un_half(2)
Uprime(3) = Un_half(3)

!Tau
call VecScale(scaler,Bfield,tau)

!Ustar
call VecScale((1.0/c),tau,tau1)
call VecDot(Uprime,tau1,Ustar)

!Lamnda prime
call VecDot(Uprime,Uprime,UprimeDot)
LamNPrime = (1.0 +(UprimeDot/(c*c)))**(0.5)

!Sigma
call VecDot(tau,tau,tauDot)
Sigma = (LamNPrime*LamNPrime) - tauDot

!Lamnda(n+1)
LamndaN1 = ((Sigma + (((Sigma*Sigma) + 4*(tauDot + (Ustar*Ustar)))**(0.5)))/2.0)**(0.5)

!tnew
oneoverlamda = 1.0/LamndaN1


call VecScale(oneoverlamda,tau,tnew)

!Sfinal
call VecDot(tnew,tnew,tnewDot)

Sfinal = 1.0/(1.0+tnewDot)

!Un+1 computation

call VecDot(Uprime,tnew, Fcalc1)
call VecScale(Fcalc1,tnew, Fcalc2)
call VecCross(UPrime,tnew,Fcalc3)
call VecAddition(Fcalc2,Fcalc3,Fcalc4)
call VecAddition(Fcalc4, Uprime,Fcalc5)
call VecScale(Sfinal,Fcalc5,Un_plus)

Vnew(1) = Un_plus(1)/LamndaN1
Vnew(2) = Un_plus(2)/LamndaN1
Vnew(3) = Un_plus(3)/LamndaN1

Xnew(1) = x_half_GSM(1) + (Vnew(1)*h)/2
Xnew(2) = x_half_GSM(2) + (Vnew(2)*h)/2
Xnew(3) = x_half_GSM(3) + (Vnew(3)*h)/2

XnewTemp(1) = Xnew(1)/6371200.0
XnewTemp(2) = Xnew(2)/6371200.0
XnewTemp(3) = Xnew(3)/6371200.0
    
call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
end if

call TimeCheck(Vabs1)
DistanceTraveled = DistanceTraveled + (h * Vabs1)
    
Vabs2 = ((Vnew(1)**2.0 + Vnew(2)**2.0 + Vnew(3)**2.0))**(0.5)

secondTotal = secondTotal + h
    
IF ((Vabs2 - Vabs1)/Vabs1 > Verr) THEN
    secondTotal = secondTotal - h
    DistanceTraveled = DistanceTraveled - (h * Vabs1)
    h = h*0.5
    GOTO 10
END IF

IF ((Vabs2 - Vabs1)/Vabs1 < LOWVerr) THEN
    h = h*1.1
END IF

call OldVariables(Position,Velocity)
    
XnewTemp(1) = Xnew(1)
XnewTemp(2) = Xnew(2)
XnewTemp(3) = Xnew(3)
    
Velocity(1) = Vnew(1)
Velocity(2) = Vnew(2)
Velocity(3) = Vnew(3)
    
Position(1) = XnewGDZ(1)
Position(2) = XnewGDZ(2)
Position(3) = XnewGDZ(3)
    
call NewMax(Max)
    
IF (h > Max) THEN
    h = Max
END IF
    
end subroutine Vay


! ************************************************************************************************************************************
! subroutine HC:
! Higuera-Cary method for solving the differential equations of motion for the CR's trajectory.
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
subroutine HC()
USE Particle
implicit None
real(8) :: Bfield(3), x0(3), v0(3), XGSM(3), x_half_GSM(3)
real(8) :: tau(3), Ustar
real(8) :: x_half_GSM_Temp(3), xGDZ_half(3), scaler, lamminus, lamplus
real(8) :: Xnew(3), Vnew(3), XnewGDZ(3), vabs1, vabs2, Max
real(8) :: LOWVerr, Verr, h1, sigma, lamnew, LamN, UnNewDotsquare, UminusDotsquare
real(8) :: tauDot, tnew(3), tnewDot, sfinal, UnNew(3), UnNewDot
real(8) :: Uminus(3), Uplus(3), UminusDot, finalcalc1(3)
real(8) :: Fcalc1, Fcalc2(3), Fcalc3(3), Fcalc4(3), Fcalc5(3)
    
Verr = 0.00001
LOWVerr = 0.0000001
    
x0(1) = Position(1) !Xx
x0(2) = Position(2) !Xy
x0(3) = Position(3) !Xz
    
call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)

if (model(1) == 4) then
    call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, x0, xGSM)
end if

xGSM(1) = xGSM(1)*6371200.0
xGSM(2) = xGSM(2)*6371200.0
xGSM(3) = xGSM(3)*6371200.0
    
v0(1) = Velocity(1) !Vx
v0(2) = Velocity(2) !Vy
v0(3) = Velocity(3) !Vz
    
Vabs1 = (v0(1)*v0(1) + v0(2)*v0(2) + v0(3)*v0(3))**(0.5)

IF (FinalStep >= 1) THEN
    h = Lasth
END IF
    
10 h1 = h*0.5

!Half update position x(n+1/2)
x_half_GSM(1) = xGSM(1) + (v0(1)/2.0)*h
x_half_GSM(2) = xGSM(2) + (v0(2)/2.0)*h
x_half_GSM(3) = xGSM(3) + (v0(3)/2.0)*h
    
lamN = (1.0 - ((Vabs1/c)**2))**(-0.5)
scaler = (Q*h)/(2.0*M)

Uminus(1) = v0(1)*lamN
Uminus(2) = v0(2)*lamN
Uminus(3) = v0(3)*lamN

x_half_GSM_Temp(1) = x_half_GSM(1)/6371200.0
x_half_GSM_Temp(2) = x_half_GSM(2)/6371200.0
x_half_GSM_Temp(3) = x_half_GSM(3)/6371200.0

call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x_half_GSM_Temp, xGDZ_half)
end if

call MagneticField(xGDZ_half, Bfield)

call VecScale(scaler,Bfield,tau)
call VecDot(Uminus,tau,Ustar)
Ustar = (Ustar / c)

call VecDot(Uminus,Uminus,UminusDot)
lamminus = (1.0 +(UminusDot/(c*c)))**(0.5)

call VecDot(tau,tau,tauDot)
Sigma = (lamminus*lamminus) - tauDot

lamplus = ((Sigma + (((Sigma*Sigma) + 4*(tauDot + (Ustar*Ustar)))**(0.5)))/2.0)**(0.5)

call VecScale((1.0/lamplus),tau,tnew)

call VecDot(tnew,tnew,tnewDot)
Sfinal = 1.0/(1.0+tnewDot)

!Un+1 computation

call VecDot(Uminus,tnew, Fcalc1)
call VecScale(Fcalc1,tnew, Fcalc2)
call VecCross(Uminus,tnew,Fcalc3)
call VecAddition(Fcalc2,Fcalc3,Fcalc4)
call VecAddition(Fcalc4, Uminus,Fcalc5)
call VecScale(Sfinal,Fcalc5,Uplus)

call VecCross(Uplus, tnew, finalcalc1)
call VecAddition(Uplus,finalcalc1,UnNew)

call VecDot(UnNew, UnNew, UnNewDot)

lamnew = (1 + ((UnNewDot)/(c*c)))**(0.5)

Vnew(1) = UnNew(1)/lamnew
Vnew(2) = UnNew(2)/lamnew
Vnew(3) = UnNew(3)/lamnew

Xnew(1) = x_half_GSM(1) + (Vnew(1)*h)/(2)
Xnew(2) = x_half_GSM(2) + (Vnew(2)*h)/(2)
Xnew(3) = x_half_GSM(3) + (Vnew(3)*h)/(2)

XnewTemp(1) = Xnew(1)/6371200.0
XnewTemp(2) = Xnew(2)/6371200.0
XnewTemp(3) = Xnew(3)/6371200.0
    
call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)

if (model(1) == 4) then
    call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
end if

call TimeCheck(Vabs1)
DistanceTraveled = DistanceTraveled + (h * Vabs1)
    
Vabs2 = ((Vnew(1)**2.0 + Vnew(2)**2.0 + Vnew(3)**2.0))**(0.5)

secondTotal = secondTotal + h

IF (Vabs2 > c) THEN
    secondTotal = secondTotal - h
    DistanceTraveled = DistanceTraveled - (h * Vabs1)
    h = h*0.5
    GOTO 10
END IF
    
IF ((Vabs2 - Vabs1)/Vabs1 > Verr) THEN
    secondTotal = secondTotal - h
    DistanceTraveled = DistanceTraveled - (h * Vabs1)
    h = h*0.5
    GOTO 10
END IF

IF ((Vabs2 - Vabs1)/Vabs1 < LOWVerr) THEN
    h = h*1.1
END IF

call OldVariables(Position,Velocity)
    
XnewTemp(1) = Xnew(1)
XnewTemp(2) = Xnew(2)
XnewTemp(3) = Xnew(3)
    
Velocity(1) = Vnew(1)
Velocity(2) = Vnew(2)
Velocity(3) = Vnew(3)
    
Position(1) = XnewGDZ(1)
Position(2) = XnewGDZ(2)
Position(3) = XnewGDZ(3)
    
call NewMax(Max)
    
IF (h > Max) THEN
    h = Max
END IF
        
end subroutine HC

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

Firsth = h

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

! ************************************************************************************************************************************
! subroutine RK4_FieldTrace:
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
subroutine RK4_FieldTrace(Bfield)
    USE Particle
    
    real(8) :: x0(3)
    real(8) :: Xnew(3), xGSM(3)
    real(8) :: x1(3), x2(3), x3(3)
    real(8) :: x0GDZ(0), x1GDZ(3), x2GDZ(3), x3GDZ(3)
    real(8) :: x0GSM(3), x1GSM(3), x2GSM(3), x3GSM(3), XnewGDZ(3)
    real(8) :: Bfield(3), Newx0(3)
    real(8) :: Bfield0(3), Bfield0Mag, Bfield0unit(3)
    real(8) :: Bfield1(3), Bfield1Mag, Bfield1unit(3)
    real(8) :: Bfield2(3), Bfield2Mag, Bfield2unit(3)
    real(8) :: Bfield3(3), Bfield3Mag, Bfield3unit(3)
    
    x0(1) = Position(1) !Xx
    x0(2) = Position(2) !Xy
    x0(3) = Position(3) !Xz

    h = 10000
    
    call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, x0, xGSM)
    
    if (model(1) == 4) then
        call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, x0, xGSM)
    end if

    call MagneticField(x0, Bfield0)

    
    ! particle position in geocentric
    
    xGSM(1) = xGSM(1)*6371200.0
    xGSM(2) = xGSM(2)*6371200.0
    xGSM(3) = xGSM(3)*6371200.0

    
    Bfield0Mag = ((Bfield0(1)**2.0 + Bfield0(2)**2.0 + Bfield0(3)**2.0))**(0.5)
    Bfield0unit(1) = Bfield0(1)/Bfield0Mag
    Bfield0unit(2) = Bfield0(2)/Bfield0Mag
    Bfield0unit(3) = Bfield0(3)/Bfield0Mag
    
    ! n1 position
    Newx0(1) = xGSM(1) + (h)*Bfield0unit(1)
    Newx0(2) = xGSM(2) + (h)*Bfield0unit(2)
    Newx0(3) = xGSM(3) + (h)*Bfield0unit(3)


    x0GSM(1) = Newx0(1)/6371200.0
    x0GSM(2) = Newx0(2)/6371200.0
    x0GSM(3) = Newx0(3)/6371200.0

    call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x0GSM, x0GDZ)
    
    if (model(1) == 4) then
        call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x0GSM, x0GDZ)
    end if
 
    call MagneticField(x0GDZ, Bfield1)
 
    Bfield1Mag = ((Bfield1(1)**2.0 + Bfield1(2)**2.0 + Bfield1(3)**2.0))**(0.5)
    Bfield1unit(1) = Bfield1(1)/Bfield1Mag
    Bfield1unit(2) = Bfield1(2)/Bfield1Mag
    Bfield1unit(3) = Bfield1(3)/Bfield1Mag
    
    ! n1 position
    x1(1) = xGSM(1) + (h/2.0)*Bfield1unit(1)
    x1(2) = xGSM(2) + (h/2.0)*Bfield1unit(2)
    x1(3) = xGSM(3) + (h/2.0)*Bfield1unit(3)
    
    x1GSM(1) = x1(1)/6371200.0
    x1GSM(2) = x1(2)/6371200.0
    x1GSM(3) = x1(3)/6371200.0
    
    call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x1GSM, x1GDZ)
    
    if (model(1) == 4) then
        call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x1GSM, x1GDZ)
    end if
    
    call MagneticField(x1GDZ, Bfield2)

    Bfield2Mag = ((Bfield2(1)**2.0 + Bfield2(2)**2.0 + Bfield2(3)**2.0))**(0.5)
    Bfield2unit(1) = Bfield2(1)/Bfield2Mag
    Bfield2unit(2) = Bfield2(2)/Bfield2Mag
    Bfield2unit(3) = Bfield2(3)/Bfield2Mag
    
    ! n1 position
    x2(1) = xGSM(1) + (h/2.0)*Bfield2unit(1)
    x2(2) = xGSM(2) + (h/2.0)*Bfield2unit(2)
    x2(3) = xGSM(3) + (h/2.0)*Bfield2unit(3)
    
    x2GSM(1) = x2(1)/6371200.0
    x2GSM(2) = x2(2)/6371200.0
    x2GSM(3) = x2(3)/6371200.0
    
    call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x2GSM, x2GDZ)
    
    if (model(1) == 4) then
        call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x2GSM, x2GDZ)
    end if
    
    call MagneticField(x2GDZ, Bfield3)

    Bfield3Mag = ((Bfield3(1)**2.0 + Bfield3(2)**2.0 + Bfield3(3)**2.0))**(0.5)
    Bfield3unit(1) = Bfield3(1)/Bfield3Mag
    Bfield3unit(2) = Bfield3(2)/Bfield3Mag
    Bfield3unit(3) = Bfield3(3)/Bfield3Mag
    
    ! n1 position
    x3(1) = xGSM(1) + h*Bfield3unit(1)
    x3(2) = xGSM(2) + h*Bfield3unit(2)
    x3(3) = xGSM(3) + h*Bfield3unit(3)
    
    x3GSM(1) = x3(1)/6371200.0
    x3GSM(2) = x3(2)/6371200.0
    x3GSM(3) = x3(3)/6371200.0
    
    call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, x3GSM, x3GDZ)
    
    if (model(1) == 4) then
        call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, x3GSM, x3GDZ)
    end if

    Xnew(1) = xGSM(1) + ( h * ( ( Bfield0unit(1) + 2*Bfield1unit(1) + 2*Bfield2unit(1) + Bfield3unit(1))/ 6.0 ) )
    Xnew(2) = xGSM(2) + ( h * ( ( Bfield0unit(2) + 2*Bfield1unit(2) + 2*Bfield2unit(2) + Bfield3unit(2))/ 6.0 ) )
    Xnew(3) = xGSM(3) + ( h * ( ( Bfield0unit(3) + 2*Bfield1unit(3) + 2*Bfield2unit(3) + Bfield3unit(3))/ 6.0 ) )

    XnewTemp(1) = Xnew(1)/6371200.0
    XnewTemp(2) = Xnew(2)/6371200.0
    XnewTemp(3) = Xnew(3)/6371200.0

    call CoordinateTransform("GSM", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
    
    if (model(1) == 4) then
        call CoordinateTransform("GEO", "GDZ", year, day, secondTotal, XnewTemp, XnewGDZ)
    end if
    
    XnewTemp(1) = Xnew(1)
    XnewTemp(2) = Xnew(2)
    XnewTemp(3) = Xnew(3)

    call MagneticField(XnewGDZ, Bfield)
    
    Position(1) = XnewGDZ(1)
    Position(2) = XnewGDZ(2)
    Position(3) = XnewGDZ(3)
    
    DistanceTraveled = DistanceTraveled + h

    end subroutine RK4_FieldTrace