! ************************************************************************************************************************************
! MagneticField.f95 - File containing the subroutine responsible for calculating the magnetic field strength.
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
subroutine MagneticField(X1, BfieldFinal)
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
USE MagneticFieldFunctions

real(8) :: BfieldFinal(3), X1(3), EXTERNALGSM(3), Bfield(3), INTERNALGSM(3), xGSM(3)

call CoordinateTransform("GDZ", "GSM", year, day, secondTotal, X1, xGSM)

if (model(1) == 4) then
    call CoordinateTransform("GDZ", "GEO", year, day, secondTotal, X1, xGSM)
end if

INTERNALGSM = InternalMagPointer(xGSM)
EXTERNALGSM = ExternalMagPointer(xGSM)

Bfield(1) = INTERNALGSM(1) + EXTERNALGSM(1)
Bfield(2) = INTERNALGSM(2) + EXTERNALGSM(2)
Bfield(3) = INTERNALGSM(3) + EXTERNALGSM(3)

Bfield(1) = Bfield(1) * 10.0**(-9)
Bfield(2) = Bfield(2) * 10.0**(-9) 
Bfield(3) = Bfield(3) * 10.0**(-9)

BfieldFinal(1) = DBLE(Bfield(1))
BfieldFinal(2) = DBLE(Bfield(2))
BfieldFinal(3) = DBLE(Bfield(3))


end subroutine MagneticField

! ************************************************************************************************************************************
! subroutine MagFieldCheck:
! Subroutine that computes the external and internal magnetic field strengths and combines them to obtain a total magnetic field
! strength at any given point within the magnetosphere. (Used specifically for the MagStrength subroutine)
!
! INPUT:
! X1 - Position of the CR [GDZ coordinates]
!
! OUTPUT:
! BfieldFinal - Magnetic field strength [T]
!
! ************************************************************************************************************************************
subroutine MagFieldCheck(xGSM, BfieldFinal)
    USE Particle
    USE GEOPACK1
    USE GEOPACK2
    USE SolarWind
    USE MagneticFieldFunctions
    
    real(8) :: BfieldFinal(3), EXTERNALGSM(3), Bfield(3), INTERNALGSM(3), xGSM(3)
    
    INTERNALGSM = InternalMagPointer(xGSM)
    EXTERNALGSM = ExternalMagPointer(xGSM)
    
    Bfield(1) = INTERNALGSM(1) + EXTERNALGSM(1)
    Bfield(2) = INTERNALGSM(2) + EXTERNALGSM(2)
    Bfield(3) = INTERNALGSM(3) + EXTERNALGSM(3)
    
    Bfield(1) = Bfield(1) * 10.0**(-9)
    Bfield(2) = Bfield(2) * 10.0**(-9) 
    Bfield(3) = Bfield(3) * 10.0**(-9)
    
    BfieldFinal(1) = DBLE(Bfield(1))
    BfieldFinal(2) = DBLE(Bfield(2))
    BfieldFinal(3) = DBLE(Bfield(3))
    
    end subroutine MagFieldCheck