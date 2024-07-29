! ***************************************************************************************************************
! ParticleModule.f95 - Contains constants that are to be accessed throughout the computation as well as some
! simple routines that allow for the reset and update of said values.
!
!
! ***************************************************************************************************************

module Particle
real(8) :: Position(3), Velocity(3), XnewTemp(3)
real(8) :: M, Q, Z, A, q_0, m_0, E_0, R, lambda, c, OLDsecondTotal, Lasth
integer(8) :: year, day, hour, minute, secondINT, model(2), Acount, forbiddencount, NeverFail, FailCheck, FinalStep
real(8) :: secondTotal, DistanceTraveled, TimeElapsed, h, hOLD, RU, RL, Ref, MaxT, step, Firsth, MaxGyroPercent
real(8) :: OLDPosition(3), OLDVelocity(3), NEWPosition(3), NEWVelocity(3), HALFPosition(3), HALFVelocity(3)
integer(4) :: Result, MidLoop, test
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
h = 0
FinalStep = 0

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
FinalStep = 0

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
TimeElapsed = 0.0
model(1) = mode(1)
model(2) = mode(2)
          
end subroutine update

subroutine OldVariables(Position1, Velocity1)
real(8) :: Position1(3), Velocity1(3)

OLDPosition(1) = Position1(1)
OLDPosition(2) = Position1(2)
OLDPosition(3) = Position1(3)

OLDVelocity(1) = Velocity1(1)
OLDVelocity(2) = Velocity1(2)
OLDVelocity(3) = Velocity1(3)

OLDsecondTotal = secondTotal

end subroutine OldVariables

end module Particle