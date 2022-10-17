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
integer(4) :: Escape

Result = PausePointer()

end subroutine EscapeCheck

