! ************************************************************************************************************************************
! MagneticFieldFunctions.f95 - Module file containing pointers to different magnetospheric magnetic field models. This module
! assigns and external and internal model to appropriate pointers to be repeatedly used throughout the computations. This avoids 
! reapeating slower IF ELSE statements over the thousands of itterations needed for the compuations.
!
! For information on each of the magnetic field models used in this file please refer to the respective files within the
! libary folder.
!
! ************************************************************************************************************************************
! subroutine MagneticField:
! Subroutine that computes the external and internal magnetic field strengths and combines them to obtain a total magnetic field
! strength at any given point within the magnetosphere.
!
! INPUT:
! X1 - Position of the CR [GDZ coordinates]
!
! OUTPUT:
! BfieldFinal - Magnetic field strength [T]
!
! ************************************************************************************************************************************
module MagneticFieldFunctions
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
implicit none

procedure (funcInternal), pointer :: InternalMagPointer => null ()
procedure (funcExternal), pointer :: ExternalMagPointer => null ()

abstract interface
function funcInternal(DUMMY1)
   real(8) :: funcInternal(3)
   real(8), intent (in) :: DUMMY1(3)
end function funcInternal
function funcExternal(DUMMY2)
    real(8) :: funcExternal(3)
    real(8), intent (in) :: DUMMY2(3)
 end function funcExternal
end interface

 
 contains

  function functionIGRF(x) ! Internal IGRF model
    real(8) :: functionIGRF(3), INTERNALGSW(3), INTERNALGSM(3)
    real(8), intent (in) :: x(3)
  
    call IGRF_GSW_08(x(1), x(2), x(3), INTERNALGSW(1), INTERNALGSW(2), INTERNALGSW(3))
    call GSWGSM_08(INTERNALGSM(1), INTERNALGSM(2), INTERNALGSM(3), INTERNALGSW(1), INTERNALGSW(2), INTERNALGSW(3), 1)

    functionIGRF = INTERNALGSM
    return
  end function functionIGRF

  function functionDIP(x) ! Internal dipole model
    real(8) :: functionDIP(3), INTERNALGSW(3), INTERNALGSM(3)
    real(8), intent (in) :: x(3)
  
    call DIP_08(x(1), x(2), x(3), INTERNALGSW(1), INTERNALGSW(2), INTERNALGSW(3))
    call GSWGSM_08(INTERNALGSM(1), INTERNALGSM(2), INTERNALGSM(3), INTERNALGSW(1), INTERNALGSW(2), INTERNALGSW(3), 1)

    functionDIP = INTERNALGSM
    return
  end function functionDIP

  function functionNoEx(x) !No external field
    real(8) :: functionNoEx(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
  
    TSYGSM(1) = 0
    TSYGSM(2) = 0
    TSYGSM(3) = 0

    functionNoEx = TSYGSM
  
    return
  end function functionNoEx

 function function87S(x) ! Tsyganenko 1987 short
   real(8) :: function87S(3), TSYGSM(3)
   real(8), intent (in) :: x(3)
 
   call TSY87S(IOPT, x(1), x(2), x(3), TSYGSM(1), TSYGSM(2), TSYGSM(3))
   function87S = TSYGSM
 
   return
 end function function87S
 
  function function87L(x) ! Tsyganenko 1987 long
    real(8) :: function87L(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
  
    call TSY87L(IOPT, x(1), x(2), x(3), TSYGSM(1), TSYGSM(2), TSYGSM(3))
    function87L = TSYGSM
  
    return
  end function function87L

  function function89(x) ! Tsyganenko 1989
    real(8) :: function89(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
  
    call T89D_DP(IOPT, parmod, PSI, x(1), x(2), x(3), TSYGSM(1), TSYGSM(2), TSYGSM(3))
    function89 = TSYGSM
  
    return
  end function function89

  function function89Mag(x) ! Tsyganenko 1989
    real(8) :: function89Mag(3), TSYGSM(3)
    real, dimension(10) :: parmod2
    real(8), intent (in) :: x(3)
    real :: GSMx(3), PSItemp, TSYfield(3)

    parmod2 = parmod
    GSMx(1) = x(1) 
    GSMx(2) = x(2)
    GSMx(3) = x(3)
    PSItemp = PSI
    call T89C_M(IOPT, parmod2, PSItemp, GSMx(1), GSMx(2), GSMx(3), TSYfield(1), TSYfield(2), TSYfield(3))
    TSYGSM(1) = TSYfield(1)
    TSYGSM(2) = TSYfield(2)
    TSYGSM(3) = TSYfield(3)
    function89Mag = TSYGSM
  
    return
  end function function89Mag

  function function96(x) ! Tsyganenko 1996
    real(8) :: function96(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
    real, dimension(10) :: parmod2
    real :: GSMx(3), PSItemp, TSYfield(3)

    parmod2 = parmod
    GSMx(1) = x(1) 
    GSMx(2) = x(2)
    GSMx(3) = x(3)
    PSItemp = PSI
  
    call T96_01(IOPT, parmod2, PSItemp, GSMx(1), GSMx(2), GSMx(3), TSYfield(1), TSYfield(2), TSYfield(3))
    TSYGSM(1) = TSYfield(1)
    TSYGSM(2) = TSYfield(2)
    TSYGSM(3) = TSYfield(3)
    function96 = TSYGSM
  
    return
  end function function96

  function function01(x) ! Tsyganenko 2001
    real(8) :: function01(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
    real, dimension(10) :: parmod2
    real :: GSMx(3), PSItemp, TSYfield(3)

    parmod2 = parmod
    GSMx(1) = x(1) 
    GSMx(2) = x(2)
    GSMx(3) = x(3)
    PSItemp = PSI
  
    call T01_01(IOPT, parmod2, GSMx(1), GSMx(2), GSMx(3), TSYfield(1), TSYfield(2), TSYfield(3))
    TSYGSM(1) = TSYfield(1)
    TSYGSM(2) = TSYfield(2)
    TSYGSM(3) = TSYfield(3)
    function01 = TSYGSM
  
    return
  end function function01

  function function01S(x) ! Tsyganenko 2001 storm-time variation
    real(8) :: function01S(3), TSYGSM(3)
    real(8), intent (in) :: x(3)
  
    call T01_S(parmod, x(1), x(2), x(3), TSYGSM(1), TSYGSM(2), TSYGSM(3))
    function01S = TSYGSM
  
    return
  end function function01S

! ************************************************************************************************************************************
! subroutine MagneticFieldAssign:
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
  subroutine MagneticFieldAssign(mode)
  implicit none
  integer(8) :: mode(2)

  call RECALC_08(year, day, hour, minute, secondINT, SW(1), SW(2), SW(3))
  
  IF (mode(1) == 1) THEN
    InternalMagPointer => functionIGRF ! IGRF
  ELSE IF (mode(1) == 2) THEN
    InternalMagPointer => functionDIP  ! DIPOLE
  ELSE
    print *, "Please enter valid internal magnetic field model"
  END IF

  IF (mode(2) == 0) THEN
    ExternalMagPointer => functionNoEx ! NO EXTERNAL FIELD
  ELSE IF (mode(2) == 1) THEN
    ExternalMagPointer => function87S  ! TSYGANENKO 87 SHORT
  ELSE IF (mode(2) == 2) THEN
    ExternalMagPointer => function87L  ! TSYGANENKO 87 LONG
  ELSE IF (mode(2) == 3) THEN
    ExternalMagPointer => function89   ! TSYGANENKO 89
  ELSE IF (mode(2) == 4) THEN
    ExternalMagPointer => function96   ! TSYGANENKO 96
  ELSE IF (mode(2) == 5) THEN
    ExternalMagPointer => function01   ! TSYGANENKO 01
  ELSE IF (mode(2) == 6) THEN
    ExternalMagPointer => function01S  ! TSYGANENKO 01 STORM
  ELSE IF (mode(2) == 7) THEN
    ExternalMagPointer => function89Mag  ! TSYGANENKO 01 STORM
  ELSE
    print *, "Please enter valid external magnetic field model"
  END IF


    
  end subroutine MagneticFieldAssign
 
 end module MagneticFieldFunctions