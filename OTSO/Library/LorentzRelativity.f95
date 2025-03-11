! ************************************************************************************************************************************
! LorentzRelativity.f95 - File containing the subroutine responsible for using the lorentz equation to calculate the force and
! acceleration that a charged particle experiences.
!
! ************************************************************************************************************************************
! subroutine Lorentz:
! Subroutine that calulates the acceleration that a charged particle moving at relativistic speeds 
! experiences within a magnetic field.
!
! INPUT: vnew - Velocity [m/s]
!        b - Magnetic field strength [nT]
!
! OUTPUT: Accel - Acceleration expereinced by CR [m/s^2]
! 
! ************************************************************************************************************************************
subroutine Lorentz(vnew, b, Accel)
USE Particle
implicit none

real(8) :: vnew(3), vabs, b(3)
real(8) :: Accel(3), lam
    
!f2py intent(in) vnew, b
!f2py intent(out) Accel
   
vabs = (vnew(1)*vnew(1) + vnew(2)*vnew(2) + vnew(3)*vnew(3))**(0.5)

IF (vabs > c) THEN
    print *, "ERROR: Particle has exceeded light speed. Please check timestep value"
    stop
END IF

lam = (1 - ((vabs/c)**2))**(-0.5)

Accel(1) = (Q*(vnew(2)*b(3) - b(2)*vnew(3)))/(lam*M)
Accel(2) = (Q*(vnew(3)*b(1) - b(3)*vnew(1)))/(lam*M)
Accel(3) = (Q*(vnew(1)*b(2) - b(1)*vnew(2)))/(lam*M)
    
    
end subroutine Lorentz


subroutine TimeCheck(Vabs)
USE Particle
implicit none

real(8) :: Vabs, lam

lam = (1 - ((Vabs/c)**2))**(-0.5)
    
TimeElapsed = TimeElapsed + h*lam        
        
end subroutine TimeCheck