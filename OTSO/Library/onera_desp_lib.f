!***************************************************************************************************
! Copyright 2004, 2008 S. Bourdarie
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
C-----------------------------------------------------------------------------
C Wrappers and procedures for ONERA_DESP_LIB
C-----------------------------------------------------------------------------

c Wrapper and procedure to access many coordinate transformation form the
c ONERA library
c
c =======================================================================
c GEO2GSM
c
c Routine to transform Cartesian GEO to cartesian GSM coordinates
c
c  INPUTS: iyr = integer year
c          idoy = integer day of year
c          secs = UT in seconds
c          xGEO = 3D array of cartesian position in GEO (Re)
c
c OUTPUTS: psi: angle for GSM coordinate
c         xGSM: 3D array of cartesian position in GSM  (Re)
c
c CALLING SEQUENCE from IDL:
c  result = call_external(lib_name,  $            ;The sharable object file
c           'geo2gsm_', $                         ;The entry point
c           iyr,idoy,secs,psi,xGEO,xGSM, $               ;return values (6)
c           /f_value)                             ;function returns a float.
c
c =======================================================================
c GSM2GEO
c
c Routine to transform Cartesian GSM to cartesian GEO coordinates
c
c  INPUTS: iyr = integer year
c          idoy = integer day of year
c          secs = UT in seconds
c          xGSM = 3D array of cartesian position in GSM (Re)
c
c OUTPUTS: psi: angle for GSM coordinate
c         xGEO: 3D array of cartesian position in GEO (Re)
c
c CALLING SEQUENCE from IDL:
c  result = call_external(lib_name,  $            ;The sharable object file
c           'gsm2geo_', $                         ;The entry point
c           iyr,idoy,secs,psi,xGSM,xGEO, $               ;return values (6)
c           /f_value)                             ;function returns a float.
c
c
c =======================================================================
c GDZ2GEO
c
c Routine to transform GEODEZIC coordinates to cartesian GEO coordinates
c
c  INPUTS: lati = latitude (degres)
c          longi = longitude (degres)
c          alti = altitude (km)
c
c OUTPUTS: xx = xGEO (Re)
c          yy = yGEO (Re)
c          zz = zGEO (Re)
c
c CALLING SEQUENCE from IDL:
c  result = call_external(lib_name,  $            ;The sharable object file
c           'gdz2geo_', $                         ;The entry point
c           lati,longi,alti,xx,yy,zz, $               ;return values (6)
c           /f_value)                             ;function returns a float.
c
c
c =======================================================================
c GEO2GDZ
c
c Routine to transform cartesian GEO coordinates to GEODEZIC coordinates
c
c INPUTS: xx = xGEO (Re)
c          yy = yGEO (Re)
c          zz = zGEO (Re)
c
c OUTPUTS: lati = latitude (degres)
c          longi = longitude (degres)
c          alti = altitude (km)
c
c
c CALLING SEQUENCE from IDL:
c  result = call_external(lib_name,  $            ;The sharable object file
c           'geo2gdz_', $                         ;The entry point
c           xx,yy,zz,lati,longi,alti, $               ;return values (6)
c           /f_value)                             ;function returns a float.
c
c =======================================================================
c --------------------------------------------------------------------
c
        SUBROUTINE geo2gsm1(iyr,idoy,secs,psi,xGEO,xGSM)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGSM(3)

      dyear=iyr+0.5d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GEO_GSM(xGEO,xGSM)
        end
c --------------------------------------------------------------------
c
        SUBROUTINE gsm2geo1(iyr,idoy,secs,psi,xGSM,xGEO)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGSM(3)


      dyear=iyr+0.5d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GSM_GEO(xGSM,xGEO)

        end
c --------------------------------------------------------------------
c
        SUBROUTINE geo2gse1(iyr,idoy,secs,xGEO,xGSE)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGSE(3)

        dyear=iyr+0.5d0
        psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GEO_GSE(xGEO,xGSE)
        end

c --------------------------------------------------------------------
c
        SUBROUTINE gse2geo1(iyr,idoy,secs,xGSE,xGEO)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGSE(3)


      dyear=iyr+0.5d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GSE_GEO(xGSE,xGEO)
        end
c --------------------------------------------------------------------
c
        SUBROUTINE geo2gei1(iyr,idoy,secs,xGEO,xGEI)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGEI(3)

       dyear=iyr+0.5d0
       psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GEO_GEI(xGEO,xGEI)
        end
c
c --------------------------------------------------------------------
c
        SUBROUTINE gei2geo1(iyr,idoy,secs,xGEI,xGEO)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xGEI(3)

        dyear=iyr+0.5d0
        psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GEI_GEO(xGEI,xGEO)
        end
c --------------------------------------------------------------------
c
        SUBROUTINE geo2sm1(iyr,idoy,secs,xGEO,xSM)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xSM(3)

       dyear=iyr+0.5d0
       psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GEO_SM(xGEO,xSM)
        end
c
c --------------------------------------------------------------------
c
        SUBROUTINE sm2geo1(iyr,idoy,secs,xSM,xGEO)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGEO(3),xSM(3)

        dyear=iyr+0.5d0
        psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL SM_GEO(xSM,xGEO)
        end

c
c --------------------------------------------------------------------
c
        SUBROUTINE gsm2sm1(iyr,idoy,secs,xGSM,xSM)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi
      REAL*8    xGSM(3),xSM(3)

        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL GSM_SM(xGSM,xSM)
        end

c --------------------------------------------------------------------
c
        SUBROUTINE sm2gsm1(iyr,idoy,secs,xSM,xGSM)
      INTEGER*4 iyr,idoy
      REAL*8    secs,psi,dyear
      REAL*8    xGSM(3),xSM(3)

        dyear=iyr+0.5d0
        psi=0.d0
        call initize ! sets rad, pi used by various routines

        CALL INIT_DTD(dyear)
        CALL INIT_GSM(iyr,idoy,secs,psi)
        CALL SM_GSM(xSM,xGSM)
        end

c --------------------------------------------------------------------
c
        SUBROUTINE geo2mag1(iyr,xGEO,xMAG)
      INTEGER*4 iyr
      REAL*8    dyear
      REAL*8    xGEO(3),xMAG(3)

      dyear=iyr+0.5d0
        CALL INIT_DTD(dyear)
        CALL GEO_MAG(xGEO,xMAG)
        end

c --------------------------------------------------------------------
c
        SUBROUTINE mag2geo1(iyr,xMAG,xGEO)
      INTEGER*4 iyr
      REAL*8    dyear
      REAL*8    xGEO(3),xMAG(3)

      dyear=iyr+0.5d0
        CALL INIT_DTD(dyear)
        CALL MAG_GEO(xMAG,xGEO)
        end
C-----------------------------------------------------------------------------

!---------------------------------------------------------------------------------------------------
!                              Introduced in version 4.1
!
! CREATION: S. Bourdarie - March 2007
! MODIFICATION: None
!
! DESCRIPTION: Wrapper to call DATE_AND_TIME2DECY from IDL, converts the IDL parameters to
!              standard FORTRAN passed by reference arguments.
!
! INPUT: argc-> number of argument (long integer)
!        argv -> reference argument
!
! CALLING SEQUENCE: result=call_external(lib_name, 'DATE_AND_TIME2DECY_IDL_', Year,Month,Day,hour,minute,second,decy, /f_value)
!---------------------------------------------------------------------------------------------------
      REAL*4 FUNCTION DATE_AND_TIME2DECY_IDL(argc, argv)
!
      INCLUDE 'wrappers.inc'
!
      j = INT(loc(argc),4)                    ! Obtains the number of arguments (argc)
                                       ! Because argc is passed by VALUE.
c

      call DATE_AND_TIME2DECY(%VAL(argv(1)), %VAL(argv(2)),
     * %VAL(argv(3)),
     * %VAL(argv(4)),%VAL(argv(5)), %VAL(argv(6)), %VAL(argv(7)))

      DATE_AND_TIME2DECY_IDL= 9.9

      RETURN
      END
