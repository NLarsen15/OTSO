! ************************************************************************************************************************************
! Magnetopause.f95 - File responsible for the implimentation of magnetopause models to act as the external boundary of the
! computation. This is important as the CR is assumed to have escaped if it encounters the magnetopause. There are multiple different
! models for the magnetopause based on different spacecraft data and assumptions. Some of these models are included, more can be
! easily added. 
!
! ************************************************************************************************************************************
! subroutine EscapeCheck:
! Subroutine that checks if the CR has escaped the magnetosphere by determining if the CR is within the model magnetopause or not.
!
! INPUT:
! Type - Integer value that determines the model magnetopause to be used.
!
! OUTPUT:
! Result - Integer that determines if the CR is within the magnetosphere. 0 = within the magnetosphere, 1 = outside the magnetosphere 
!
! ************************************************************************************************************************************
subroutine EscapeCheck()
USE MagnetoPause
USE Particle
USE GEOPACK1
USE GEOPACK2
USE MagnetopauseFunctions
implicit none

Result = PausePointer()

end subroutine EscapeCheck

subroutine FinalStepCheck()
USE Particle
implicit none

IF (FinalStep == 1) THEN
    FinalStep = 2
    IF (Result == 0) THEN
    Position(1) = OLDPosition(1)
    Position(2) = OLDPosition(2)
    Position(3) = OLDPosition(3)

    Velocity(1) = OLDVelocity(1)
    Velocity(2) = OLDVelocity(2)
    Velocity(3) = OLDVelocity(3)

    secondTotal = OLDsecondTotal
    Lasth = (h/150)
    END IF
END IF

end subroutine FinalStepCheck

subroutine MidCheck()
USE MagnetoPause
USE Particle
USE GEOPACK1
USE GEOPACK2
USE MagnetopauseFunctions

IF (FinalStep == 1) THEN
    MidLoop = 0
    
    NEWPosition(1) = Position(1)
    NEWPosition(2) = Position(2)
    NEWPosition(3) = Position(3)

    NEWVelocity(1) = Velocity(1)
    NEWVelocity(2) = Velocity(2)
    NEWVelocity(3) = Velocity(3)

    HALFPosition(1) = (OLDPosition(1) + NEWPosition(1))/2
    HALFPosition(2) = (OLDPosition(2) + NEWPosition(2))/2
    HALFPosition(3) = (OLDPosition(3) + NEWPosition(3))/2

    HALFVelocity(1) = (OLDVelocity(1) + NEWVelocity(1))/2
    HALFVelocity(2) = (OLDVelocity(2) + NEWVelocity(2))/2
    HALFVelocity(3) = (OLDVelocity(3) + NEWVelocity(3))/2

    Position(1) = HALFPosition(1)
    Position(2) = HALFPosition(2)
    Position(3) = HALFPosition(3)

    Velocity(1) = HALFVelocity(1)
    Velocity(2) = HALFVelocity(2)
    Velocity(3) = HALFVelocity(3)
    
    Do WHILE (MidLoop < 500)

        Position(1) = HALFPosition(1)
        Position(2) = HALFPosition(2)
        Position(3) = HALFPosition(3)

        Velocity(1) = HALFVelocity(1)
        Velocity(2) = HALFVelocity(2)
        Velocity(3) = HALFVelocity(3)
        call EscapeCheck()
        IF (Result == 1) THEN

            NEWPosition(1) = Position(1)
            NEWPosition(2) = Position(2)
            NEWPosition(3) = Position(3)

            NEWVelocity(1) = Velocity(1)
            NEWVelocity(2) = Velocity(2)
            NEWVelocity(3) = Velocity(3)
    
            call MidCheckLower()

        ELSE
            OLDPosition(1) = Position(1)
            OLDPosition(2) = Position(2)
            OLDPosition(3) = Position(3)

            OLDVelocity(1) = Velocity(1)
            OLDVelocity(2) = Velocity(2)
            OLDVelocity(3) = Velocity(3)

            call MidCheckUpper()

        END IF
        MidLoop = MidLoop + 1
    END DO
    Result = 1

END IF
end subroutine MidCheck


subroutine MidCheckUpper()
USE MagnetoPause
USE Particle
USE GEOPACK1
USE GEOPACK2
USE MagnetopauseFunctions

HALFPosition(1) = (OLDPosition(1) + NEWPosition(1))/2
HALFPosition(2) = (OLDPosition(2) + NEWPosition(2))/2
HALFPosition(3) = (OLDPosition(3) + NEWPosition(3))/2

HALFVelocity(1) = (OLDVelocity(1) + NEWVelocity(1))/2
HALFVelocity(2) = (OLDVelocity(2) + NEWVelocity(2))/2
HALFVelocity(3) = (OLDVelocity(3) + NEWVelocity(3))/2

end subroutine MidCheckUpper

subroutine MidCheckLower()
USE MagnetoPause
USE Particle
USE GEOPACK1
USE GEOPACK2
USE MagnetopauseFunctions


HALFPosition(1) = (OLDPosition(1) + NEWPosition(1))/2
HALFPosition(2) = (OLDPosition(2) + NEWPosition(2))/2
HALFPosition(3) = (OLDPosition(3) + NEWPosition(3))/2

HALFVelocity(1) = (OLDVelocity(1) + NEWVelocity(1))/2
HALFVelocity(2) = (OLDVelocity(2) + NEWVelocity(2))/2
HALFVelocity(3) = (OLDVelocity(3) + NEWVelocity(3))/2

end subroutine MidCheckLower

