! ************************************************************************************************************************************
! MagnetopauseMod.f95 - Module file containing the MagnetoPause module. This module stores values that are important to the modelling
! of the magnetopause used as the exterior boundry of the magnetosphere. Used within the Magnetopause.f95 file.
!
! ************************************************************************************************************************************
module MagnetoPause
    real(8) :: a11, a22, a33, a14, a12, a13, a23, a24, a44, a34, MaxR, p, r0, alpha, Dp, DpAv, scale, k, sig0, A1, x0
    real(8) :: Angle, radial, xprime, s, t, dip, rotation, theta, xtemp, ytemp, ztemp, NewX, NewY, NewZ
    real(8) :: ResultCheck, sig, sign, Xtemp1, Ytemp1, Ztemp1, SubResult
    SAVE
    contains
    
end module MagnetoPause