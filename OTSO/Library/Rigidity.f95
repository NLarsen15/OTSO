! ********************************************************************************************************************
! Rigidity.f95 - File containing the subroutine to compute the effective rigidity.
!
!
! ********************************************************************************************************************
! subroutine EffectiveRigidity:
!
! Subroutine takes in the rigidity step size and uses this along with the number of accepted trajectories within
! the penumbra to calulate the effective rigidity. Value is updated within the particle module.
!
! INPUT:
! Rstep - rigidity step size
!
! OUTPUT:
! Ref - effective rigidity
!
!
!
! ********************************************************************************************************************
subroutine EffectiveRigidity(Rstep)
USE Particle
implicit none
real(8) :: Rstep

IF (RU == RL) THEN
    Ref = RU
    RU = RU
    RL = RU
END IF

IF (NeverFail == 0) THEN
    Ref = 0
    RU = 0
    RL = 0
END IF

IF (RU /= RL) THEN
    IF (NeverFail == 1) THEN
        IF (Acount /= 0) THEN
            Acount = Acount
            Ref = RU - (Acount*Rstep)
        END IF
    END IF
END IF

IF (FailCheck == 0) THEN
    Ref = 0
    RU = 0
    RL = 0
END IF

end subroutine EffectiveRigidity