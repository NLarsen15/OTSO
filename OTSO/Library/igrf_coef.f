!***************************************************************************************************
! Copyright 2000 D. Boscher, 2004 S. Bourdarie
!
! This file is part of IRBEM-LIB.
!
!    IRBEM-LIB is free software: you can redistribute it and/or modify
!    it under the terms of the GNU Lesser General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    IRBEM-LIB is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU Lesser General Public License for more details.
!
!    You should have received a copy of the GNU Lesser General Public License
!    along with IRBEM-LIB.  If not, see <http://www.gnu.org/licenses/>.
!
!
! VERSION: IGRF13
!
! [EOS TRANS. AGU APRIL 21, 1992, P. 182]
!  Additional IGRF References:
!  (J. GEOMAG. GEOELECTR.(1982), V.34, P.313-315,
!  GEOMAGN. AND AERONOMY (1986), V.26, P.523-525).
!
!------INPUT PARAMETERS:
!  iyr - YEAR NUMBER (FROM 1900 UP TO 2025)
!----- OUTPUT PARAMETERS:
!  g,h - coefficients for the igrf model interpolated (or extrapolated)
!  to the epoch of iyr
!
!
       subroutine get_igrf_coeffs(year,gnew,hnew,ierr)
       USE CUSTOMGAUSS
       USE GEOPACK2
C
      IMPLICIT NONE
      REAL*8 year, ierr
      REAL*8 Gnew(105),Hnew(105)
      INTEGER *4 N
       
       DO N=1,105
              Gnew(N)=G(N)
              Hnew(N)=H(N)
       ENDDO
c
C
c
       return
       end
