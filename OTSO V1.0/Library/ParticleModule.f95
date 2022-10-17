! ***************************************************************************************************************
! ParticleModule.f95 - Contains constants that are to be accessed throughout the computation as well as some
! simple routines that allow for the reset and update of said values.
!
!
! ***************************************************************************************************************

module Particle
real(8) :: Position(3), Velocity(3)
real(8) :: M, Q, Z, A, q_0, m_0, E_0, R, lambda, c
integer(8) :: year, day, hour, minute, secondINT, model(2), Acount, forbiddencount, NeverFail, FailCheck
real(8) :: secondTotal, DistanceTraveled, h, hOLD, RU, RL, Ref, MaxT, step, MaxGyroPercent
integer(4) :: Result
SAVE
contains



! ***************************************************************************************************************
! subroutine initialize:
! Defines the values for the elementary charge, speed of light, proton mass (neutron mass is assumed the same),
! and hOLD (a value that is used when determining the integration time-step)
!
! ***************************************************************************************************************
subroutine initialize()

q_0 = 1.6021766208e-19
m_0 = 1.672621898e-27
c = 299792458.0
hOLD = 0.0

end subroutine initialize



! ***************************************************************************************************************
! subroutine reset:
! Resets all the CR and integration values to 0 to insure that no data is carried over from prior computations.
!
! ***************************************************************************************************************
subroutine Reset()

M = 0
Q = 0
Z = 0
A = 0
q_0 = 0
m_0 = 0
E_0 = 0
lambda = 0
c = 0
h = 0
hOLD = 0
MaxT = 0

end subroutine Reset
      


! ***************************************************************************************************************
! subroutine update:
! Computes the rest energy, lorentz factor, mass, and charge of CR. Sets the distance travelled by the CR to 0
! at the start of the computation and assigns the magnetic field models to be used in the computation.
!
! ***************************************************************************************************************
subroutine update(mode)
integer(8) :: mode(2)

E_0 = (m_0 * (299792458.0**2)) * (6.242e9)
lambda = (((R*Z/(E_0 * A))**2) + 1)**(0.5)
M = m_0 * A
Q = q_0 * Z
DistanceTraveled = 0.0
model(1) = mode(1)
model(2) = mode(2)
          
end subroutine update

end module Particle