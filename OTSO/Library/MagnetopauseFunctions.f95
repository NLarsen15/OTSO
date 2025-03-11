! MagnetopauseFunctions.f95 - Module file containing pointers to different magnetopauuse models. This module
! assigns a model to appropriate pointers to be repeatedly used throughout the computations. This avoids 
! reapeating slower IF ELSE statements over the thousands of itterations needed for the compuations.
!
! For information on each of the magnetopause models used in this file please refer to the respective 
! papers listed below:
!
! ************************************************************************************************************************************
module MagnetopauseFunctions
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
USE MagnetoPause
implicit none

procedure (funcPause), pointer :: PausePointer => null ()

abstract interface
function funcPause()
   integer(4) :: funcPause
end function funcPause
end interface

 
 contains

  function functionSphere() ! 25Re Sphere
    integer(4) :: functionSphere
    real(8) :: GSEPosition(3), x1, y1, z1, TestResult

    call CoordinateTransform("GDZ", "GSE", year, day, secondTotal, Position, GSEPosition)

    if (model(1) == 4) then
      call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, Position, GSEPosition)
    end if
    
    TestResult = -1
    Result = 0
    x1 = GSEPosition(1)
    y1 = GSEPosition(2)
    z1 = GSEPosition(3)

    TestResult = (z1**2 + y1**2 + x1**2)**(0.5) - (25)

    IF (TestResult < 0) THEN
      functionSphere = 0
    ELSE IF (TestResult >= 0) THEN
      functionSphere = 1
      IF (FinalStep == 0) THEN
        FinalStep = 1
        TestResult = -1
      END IF
    END IF
    
    return
  end function functionSphere

  function functionLargeSphere() ! 25Re Sphere
    integer(4) :: functionLargeSphere
    real(8) :: GSEPosition(3), x1, y1, z1, TestResult

    call CoordinateTransform("GDZ", "GSE", year, day, secondTotal, Position, GSEPosition)

    if (model(1) == 4) then
      call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, Position, GSEPosition)
    end if
    
    TestResult = -1
    Result = 0
    x1 = GSEPosition(1)
    y1 = GSEPosition(2)
    z1 = GSEPosition(3)

    TestResult = (z1**2 + y1**2 + x1**2)**(0.5) - (100)

    IF (TestResult < 0) THEN
      functionLargeSphere = 0
    ELSE IF (TestResult >= 0) THEN
      functionLargeSphere = 1
      IF (FinalStep == 0) THEN
        FinalStep = 1
        TestResult = -1
      END IF
    END IF
    
    return
  end function functionLargeSphere

  function functionAberratedFormisano() ! Aberrated Formisano Model
    integer(4) :: functionAberratedFormisano
    real(8) :: a11, a22, a33, a13, a23, a34, a14, a12, a24, a44
    real(8) :: GSEPosition(3), x1, y1, z1, TestResult

    call CoordinateTransform("GDZ", "GSE", year, day, secondTotal, Position, GSEPosition)

    TestResult = -1
    Result = 0
    x1 = GSEPosition(1)
    y1 = GSEPosition(2)
    z1 = GSEPosition(3)

    a11 = 0.65
    a22 = 1
    a33 = 1.16
    a13 = -0.28
    a23 = -0.11
    a34 = -0.36
    a14 = 21.41
    a12 = 0.03
    a24 = 0.46
    a44 = -221

    TestResult = a11*(x1**2) + a22*(y1**2) + a33*(z1**2) + a12*(x1*y1) + a13*x1*z1 + a23*y1*z1 + a14*x1 + a24*y1 + a34*z1 + (a44)
    IF (x1 < -60) THEN
        TestResult = 1
        IF (FinalStep == 0) THEN
          FinalStep = 1
          TestResult = -1
        END IF
    END IF

    IF (TestResult < 0) THEN
      functionAberratedFormisano = 0
    ELSE IF (TestResult >= 0) THEN
      functionAberratedFormisano = 1
    END IF

    return
  end function functionAberratedFormisano

  function functionSibeck() ! Sibeck Model
    integer(4) :: functionSibeck
    real(8) :: a11, a22, a33, a14
    real(8) :: GSMPosition(3), x1, y1, z1, TestResult, p, Rvalue

    call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, Position, GSMPosition)
    
    TestResult = -1
    Result = 0
    x1 = GSMPosition(1)
    y1 = GSMPosition(2)
    z1 = GSMPosition(3)

    p = PDYN * 10.0**(9.0)
    IF (p >= 0.54 .AND. p < 0.87) THEN
        a11 = 0.19
        a22 = 19.3
        a33 = -272.4
        a14 =  0.705
    ELSE IF (p >= 0.87 .AND. p < 1.47) THEN
        a11 = 0.19
        a22 = 18.7
        a33 = -243.9
        a14 = 1.17
    ELSE IF (p >= 1.47 .AND. p < 2.60) THEN
        a11 = 0.14
        a22 = 18.2
        a33 = -217.2
        a14 = 2.04
    ELSE IF (p >= 2.60 .AND. p < 4.90) THEN
        a11 = 0.15
        a22 = 17.3
        a33 = -187.4
        a14 = 3.75
    ELSE IF (p >= 4.90 .AND. p < 9.90) THEN
        a11 = 0.18
        a22 = 14.2
        a33 = -139.2
        a14 = 7.4
    ELSE IF (p < 0.54 .OR. p > 9.90)  THEN
        a11 = 0.14
        a22 = 18.2
        a33 = -217.2
        a14 = 2.04
        IF (PDYN == 0) THEN
            p = a14
        END IF
    END IF

    Rvalue = (z1**2 + y1**2)**(0.5)
    TestResult = Rvalue**2 + (a11)*(x1**2) + a22*x1*((a14/p)**(1.0/6.0)) + (a33)*((a14/p)**(1.0/3.0))

    IF (x1 < -50) THEN
        TestResult = 1
        IF (FinalStep == 0) THEN
          FinalStep = 1
          TestResult = -1
        END IF
    END IF

    IF (TestResult < 0) THEN
      functionSibeck = 0
    ELSE IF (TestResult >= 0) THEN
      functionSibeck = 1
    END IF

    return
  end function functionSibeck

  function functionKobel() ! Kobel Model
    integer(4) :: functionKobel
    real(8) :: Ak, Bk(7), Fk(7), rho2, kpar, sink, cosk
    real(8) :: x1rot, y1rot, z1rot, rhorot
    real(8) :: GSMPosition(3), x1, y1, z1, TestResult, DIP

    TestResult = -1
    Result = 0
    dip = PSI

    Ak = -0.0545
    Bk(1) = 11.7
    Bk(2) = 11.1
    Bk(3) = 10.8
    Bk(4) = 10.4
    Bk(5) = 10.4
    Bk(6) = 10.2
    Bk(7) = 10.2

    Fk(1) = 20.0
    Fk(2) = 15.0
    Fk(3) = 6.67
    Fk(4) = 10.0
    Fk(5) = 5.0
    Fk(6) = 6.0
    Fk(7) = 6.0

    call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, Position, GSMPosition)
    x1 = GSMPosition(1)
    y1 = GSMPosition(2)
    z1 = GSMPosition(3)

    rho2 = y1*y1 + z1*z1

    if (rho2 > 900) THEN
        TestResult = 1
        IF (FinalStep == 0) THEN
          FinalStep = 1
          TestResult = -1
        END IF
    end if

    if (x1 < -60) THEN
        TestResult = 1
        IF (FinalStep == 0) THEN
          FinalStep = 1
          TestResult = -1
        END IF
    end if

    kpar = DIP/Fk(IOPT)
    sink = SIN(kpar)
    cosk = COS(kpar)

    x1rot = x1*cosk + z1*sink
    y1rot = y1
    z1rot = (-x1)*sink + z1*cosk

    rhorot = y1rot*y1rot + z1rot*z1rot

    

    IF (x1rot > Ak*rhorot + Bk(IOPT)) THEN
        TestResult = 1
        IF (FinalStep == 0) THEN
          FinalStep = 1
          TestResult = -1
        END IF
    END IF

    IF (TestResult < 0) THEN
      functionKobel = 0
    ELSE IF (TestResult >= 0) THEN
      functionKobel = 1
    END IF

    return
  end function functionKobel
 
  function functionTSY() ! Magnetopause models used within the Tsyganenko models
    integer(4) :: functionTSY
    real(8) :: GSMPosition(3), x1, y1, z1, TestResult

    call CoordinateTransform("GSE", "GSM", year, day, secondTotal, GSMPosition, GSMPosition)
    TestResult = -1
    Result = 0
    x1 = GSMPosition(1)
    y1 = GSMPosition(2)
    z1 = GSMPosition(3)
  
    IF (SubResult == 1) THEN
      TestResult = 1
      IF (FinalStep == 0) THEN
        FinalStep = 1
        TestResult = -1
      END IF
    END IF

    IF (x1 < -50) THEN
      TestResult = 1
      IF (FinalStep == 0) THEN
        FinalStep = 1
        TestResult = -1
      END IF
    END IF

    IF (TestResult < 0) THEN
      functionTSY = 0
    ELSE IF (TestResult >= 0) THEN
      functionTSY = 1
    END IF
  
    return
  end function functionTSY

! ************************************************************************************************************************************
! subroutine MagnetopuaseAssign:
! Subroutine that assigns the functions for specific magnetic field models to an internal and external pointer. To be used within
! the MagneticField subroutine (MagneticField.f95).
!
! INPUT:
! mode - integer array of length 2 containg information on the models to be used. (e.g. [1,3] = IGRF and Tsyganenko1989)
!
! OUTPUT:
! InternalMagPointer and ExternalMagPointer are assigned appropriate magnetic field models to be used.
!
! ************************************************************************************************************************************
  subroutine MagnetopauseAssign(Pause)
  USE Particle
  implicit none
  integer(4) :: Pause

  IF (Pause == 0) THEN
    PausePointer => functionSphere ! 25Re Sphere
  ELSE IF (Pause == 100) THEN
    PausePointer => functionSphere ! 100Re Sphere
  ELSE IF (Pause == 1) THEN
    PausePointer => functionAberratedFormisano  ! Aberrated Formisano Model
  ELSE IF (Pause == 2) THEN
    PausePointer => functionSibeck  ! Sibeck Model
  ELSE IF (Pause == 3) THEN
    PausePointer => functionKobel   ! Kobel Model
  ELSE IF (model(2) == 4) THEN
    PausePointer => functionTSY  ! TSYGANENKO models
  ELSE IF (model(2) == 5) THEN
    PausePointer => functionTSY  ! TSYGANENKO models
  ELSE IF (model(2) == 6) THEN
    PausePointer => functionTSY  ! TSYGANENKO models
  ELSE IF (model(2) == 7) THEN
    PausePointer => functionTSY  ! TSYGANENKO models
  ELSE
    print *, "Please enter valid magnetopause model"
  END IF


    
  end subroutine MagnetopauseAssign
 
 end module MagnetopauseFunctions