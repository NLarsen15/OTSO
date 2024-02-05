module IntegrationFunctions
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
implicit none

procedure (funcIntegration), pointer :: IntegrationPointer

abstract interface
subroutine funcIntegration()
end subroutine funcIntegration
end interface

contains

  subroutine function4RK() ! 4th Order Runge-Kutta

    call RK4()
    return
  end subroutine function4RK

  subroutine functionBoris() ! Boris Method

    call Boris()
    return
  end subroutine functionBoris

  subroutine functionVay() ! Vay Method

    call Vay()
    return
  end subroutine functionVay

  subroutine functionHC() ! Higuera-Cary Method

    call HC()
    return
  end subroutine functionHC




  subroutine IntegrationAssign(Intmode)
  implicit none
  integer(8) :: IntMode
    
  IF (IntMode == 1) THEN
    IntegrationPointer => function4RK ! 4th Order Runge-Kutta
  ELSE IF (IntMode == 2) THEN
    IntegrationPointer => functionBoris  ! Boris Method
  ELSE IF (IntMode == 3) THEN
    IntegrationPointer => functionVay  ! Vay Method
  ELSE IF (IntMode == 4) THEN
    IntegrationPointer => functionHC  ! Higuera-Cary Method
  ELSE
    print *, "Please enter valid integration method"
  END IF
  
  
      
    end subroutine IntegrationAssign
   
 end module IntegrationFunctions