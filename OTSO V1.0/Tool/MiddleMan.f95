! **********************************************************************************************************************
! OTSO Functions:
!            This file contains the three main functions included within the OTSO tool.
!            Trajectory - will output the trajectory of a particle within the magetosphere to a file
!            Cone - Will compute effective cutoff rigidity and asymptotic cone of any given location.
!                   All data is output into a file with a name of the user's choosing.
!            Planet -  Calcuates the effective cutoff rigidity for any location on the Earth without doing
!                      asymptotic computations. Should be used with the Planet.py script.
!
! **********************************************************************************************************************
! Subroutine MagStrength:
!            subroutine that will tell you the strength of the magnetic field at any given point within the 
!            magnetosphere. Output is in GSM coordinates.
!
! **********************************************************************************************************************
subroutine MagStrength(Pin, Date, CoordIN, mode, I, Wind, Bfield)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE GEOPACK1
    USE GEOPACK2
    implicit none
    
    real(8) :: Pin(3), Pout(3), Wind(10), Bfield(3), Date(6)
    character(len = 3) :: CoordIN
    integer(4) :: I
    integer(8) :: mode(2)

    !f2py intent(in) Pin, Date, CoordIN, I, Wind
    !f2py intent(out) Bfield

    year = Date(1)
    day = Date(2)
    hour = Date(3)
    minute = Date(4)
    secondINT = Date(5)
    secondTotal = real(Date(6))

    call initializeWind(Wind, I, mode)

    call MagneticFieldAssign(mode)
    
    call CoordinateTransform(CoordIN, "GSM", year, day, secondTotal, Pin, Pout)

    call MagFieldCheck(Pout, Bfield)

    print *, "Magnetic Field Strength in GSM Coordinates:"

    print *, Bfield
    
    end subroutine MagStrength

! **********************************************************************************************************************
! Subroutine CoordTrans:
!            subroutine that uses the IBREM database of coordinate transforms to convert coordinates into
!            a new coordinate system.
!
! **********************************************************************************************************************
subroutine CoordTrans(Pin, year, day, sec, CoordIN, CoordOUT, Pout)
    implicit none
    
    real(8) :: sec, Pin(3), Pout(3)
    character(len = 3) :: CoordIN, CoordOUT 
    integer(8) :: year, day
    
    !f2py intent(in) Pin, sec, year, day, CoordIN, CoordOUT
    !f2py intent(out) Pout
    
    call CoordinateTransform(CoordIN, CoordOUT, year, day, sec, Pin, Pout)
    
    end subroutine CoordTrans

! **********************************************************************************************************************
! Subroutine Trajectory:
!            subroutine that calculates the trajectory of a cosmic ray within different input
!            magnetic field models. The trajectory is output in a csv file named "Trajectory".
!            The output data is in the Cartesian Geocentric coordinate system.
!            Will also state if the cosmic ray has an allowed or forbidden trajectory.
!            Accepted Condition: cosmic ray encounters the magetopause
!            Forbidden Conditions: - cosmic ray encounters the Earth (20km above Earth's surface)
!                                  - cosmic ray travels over 100Re without escaping or enountering Earth
! **********************************************************************************************************************
subroutine trajectory(PositionIN, Rigidity, Date, mode, AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End)
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE Magnetopause
implicit none

real(8) :: PositionIN(5), Rigidity, Date(6), End(2)
real(8) :: Wind(10), Re, Lat, Long, GyroPercent
real(8) :: Xnew(3), Vnew(3), XnewGDZ(3), XnewConverted(3)
integer(8) :: mode(2), Anti, AtomicNumber
integer(4) :: I, Limit, Pause
character(len=50) :: FileName
character(len=3) :: CoordSystem


!f2py intent(in) PositionIN, Rigidity, Date, mode, AtomicNumber, Anti
!f2py intent(out) Xnew, Vnew, XnewGDZ

Re = 6371.2
Limit = 0
Acount = 0
Result = 0
SubResult = 0
MaxGyroPercent = GyroPercent

IF (PositionIN(4) > 90.0) THEN
    print *, "ERROR: Please enter a zenith angle between 0 and 90 degrees"
    stop
END IF

IF (PositionIN(5) < 0) THEN
    print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
ELSE IF (PositionIN(5) > 360) THEN
    print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
END IF

call CreateParticle(PositionIN, Rigidity, Date, AtomicNumber, Anti, mode)

call initializeWind(Wind, I, mode)

call MagneticFieldAssign(mode)
call MagnetopauseAssign(Pause)

call FirstTimeStep()

open(unit=10,file=FileName,status='replace')
write(10,"(a)")"X,Y,Z"

do while (Result == 0) 
call RK4(Xnew, Vnew, XnewGDZ)

call EscapeCheck()
!print *, XnewGDZ(1), XnewGDZ(2), XnewGDZ(3)

Xnew(1) = Xnew(1)/1000
Xnew(2) = Xnew(2)/1000
Xnew(3) = Xnew(3)/1000

call CoordinateTransform("GSM", CoordSystem, year, day, secondTotal, Xnew, XnewConverted)

write(10,'(*(G0.6,:,","))') XnewConverted

IF ( Position(1) < End(1) ) THEN
    print *, "This is Forbidden", "      Encountered Earth"
    call AsymptoticDirection(Lat, Long)
    print *, Lat, Long
    Limit = 1
    EXIT
END IF

IF ( DistanceTraveled/1000.0 > End(2)*Re) THEN
    print *, "This is Forbidden", "      Exceeded Travel Distance Without Escape"
    print *, DistanceTraveled
    call AsymptoticDirection(Lat, Long)
    print *, Lat, Long
    Limit = 1
    EXIT
END IF


IF (Result == 1)  THEN
    print *, "This is Allowed", "      Successfully Escaped"
    call AsymptoticDirection(Lat, Long)
    print *, "Escape Position"
    print *, Lat, Long
    EXIT
END IF

end do

Close(10, STATUS='KEEP') 

end subroutine trajectory

! **********************************************************************************************************************
! Subroutine Cone:
!            subroutine that calculates the trajectory of a cosmic rays across a range of rigidities
!            within different input magnetic field models and determines the Asympototic Latitude and
!            Longitude. Will create a csv file in which the asymptotic cone data is stored.
!            Accepted Condition: cosmic ray encounters the model magnetopause
!            Forbidden Conditions: - cosmic ray encounters the Earth (20km above Earth's surface)
!                                  - cosmic ray travels over 100Re without escaping or enountering Earth
!
! **********************************************************************************************************************
subroutine cone(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, AtomicNumber, Anti, &
    I, Wind, Pause, FileName, CoordSystem, GyroPercent, End)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(2)
    real(8) :: Wind(10), Re, Lat, Long, GyroPercent
    real(8) :: Xnew(3), Vnew(3), XnewGDZ(3), Geofile(3)
    integer(8) :: mode(2), Anti, AtomicNumber
    integer(4) :: I, Limit, bool, Pause
    character(len=50) :: FileName
    character(len=3) :: CoordSystem

    !f2py intent(in) PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, AtomicNumber, Anti, I, Wind, Type, FileName
    !f2py intent(out) Xnew, Vnew, XnewGDZ
    
    R = StartRigidity
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent

    IF (PositionIN(4) > 90.0) THEN
        print *, "ERROR: Please enter a zenith angle between 0 and 90 degrees"
        stop
    END IF
    
    IF (PositionIN(5) < 0) THEN
        print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    ELSE IF (PositionIN(5) > 360) THEN
        print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    END IF

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Rigidity(GV),Filter,Latitude,Longitude,X,Y,Z"

    do while (R > EndRigidity)

    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)

    call FirstTimeStep()
    
    do while (Result == 0) 
    
    call RK4(Xnew, Vnew, XnewGDZ)

    call EscapeCheck()
    
    IF ( Position(1) < End(1) ) THEN
        bool = -1
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, lat, Long, "Forbidden", "      Encountered Earth" !(Prints the outputs to the command module while running (Can lead to delays with multi-core proccessing))
        write(10,'(*(G0.6,:,","))') R, bool, Lat, Long, GEOfile(1), GEOfile(2), GEOfile(3)
        EXIT
    END IF

    IF ( DistanceTraveled/1000.0 > End(2) * Re) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, lat, Long, "Forbidden",  "      Exceeded Travel Distance Without Escape" !(Prints the outputs to the command module while running (Can lead to delays with multi-core proccessing))
        write(10,'(*(G0.6,:,","))') R, bool, Lat, Long, GEOfile(1), GEOfile(2), GEOfile(3)
        EXIT
    END IF
    
    IF (Result == 1) THEN
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        forbiddencount = 0
        bool = 1
        !print *, R, lat, Long !(Prints the outputs to the command module while running (Can lead to delays with multi-core proccessing))
        write(10,'(*(G0.6,:,","))') R, bool, Lat, Long, GEOfile(1), GEOfile(2), GEOfile(3)
        RL = R
        FailCheck = 0
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    
    end do
    
    R = R - RigidityStep
    IF(R < RigidityStep) THEN
        R = EndRigidity
    END IF
    Result = 0

    end do

    call EffectiveRigidity(RigidityStep)

    print *, "Ru:", RU
    print *, "Rl:", RL
    print *, "Rc:", Ref

    write(10,'(*(G0.6,:""))')"Ru:", RU, ",  Rc:", Ref, ",  Rl:", RL 

    Close(10, STATUS='KEEP') 

    
    end subroutine cone

! **********************************************************************************************************************
! Subroutine Planet:
!            subroutine that calculates the trajectory of a cosmic rays across a range of rigidities
!            within different input magnetic field models and determines the effective cutoff rigidity for
!            a range of latitude and longitudes. Typically done over the entire planet.
!            Will create a csv file and will in the calculated rigidities for the locations.
!            This code works with the Planet.py tool to assign large amounts of locations across multiple cores.
!
! **********************************************************************************************************************
subroutine planet(PositionIN, Rigidity, Date, mode, AtomicNumber, Anti, I, Wind, Pause, FileName, GyroPercent, End)
USE Particle
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE Magnetopause
implicit none
            
real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(2)
real(8) :: Wind(10), Re, Rigidity(3), GyroPercent
real(8) :: Xnew(3), Vnew(3), XnewGDZ(3)
integer(8) :: mode(2), Anti, AtomicNumber
integer(4) :: I, Limit, bool, Pause
character(len=30) :: FileName
            
!f2py intent(in) PositionIN, Rigidity, Date, mode, AtomicNumber, Anti, I, Wind
!f2py intent(out) Xnew, Vnew, XnewGDZ
            
StartRigidity = Rigidity(1)
EndRigidity = Rigidity(2)
RigidityStep = Rigidity(3)


R = StartRigidity
Ru = StartRigidity
Re = 6371.2
Limit = 0
Acount = 0
Result = 0
NeverFail = 0
forbiddencount = 0
Step = RigidityStep
SubResult = 0
MaxGyroPercent = GyroPercent
        
IF (PositionIN(4) > 90.0) THEN
    print *, "ERROR: Please enter a zenith angle between 0 and 90 degrees"
    stop
END IF
            
IF (PositionIN(5) < 0) THEN
    print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
ELSE IF (PositionIN(5) > 360) THEN
    print *, "ERROR: Please enter a azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
END IF
        
open(unit=10,file=FileName,action='write',position='append')

do while (R > EndRigidity)
        
    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
            
    call initializeWind(Wind, I, mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
            
    call FirstTimeStep()
            
    do while (Result == 0) 
            
        call RK4(Xnew, Vnew, XnewGDZ)
        
        call EscapeCheck()
            
        IF ( Position(1) < End(1) ) THEN
            bool = -1
            Limit = 1
            forbiddencount = forbiddencount + 1
            NeverFail = 1
            FailCheck = 1
            EXIT
        END IF
        
        IF ( DistanceTraveled/1000.0 > End(2) * Re) THEN
            bool = 0
            Limit = 1
            forbiddencount = forbiddencount + 1
            NeverFail = 1
            FailCheck = 1
            EXIT
        END IF
            
        IF (Result == 1) THEN
            forbiddencount = 0
            bool = 1
            RL = R
            FailCheck = 0
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    end do
            
    R = R - RigidityStep
    IF(R < RigidityStep) THEN
        R = EndRigidity
    END IF
    Result = 0
        
end do
        
call EffectiveRigidity(RigidityStep)
        
print *, "Latitude: ", PositionIN(2), "    Longitude: ", PositionIN(3), "    Ru: ", RU, "    Rc: ", Ref, "    Rl: ", RL
        
write(10,'(*(G0.6,:,","))') PositionIN(2), PositionIN(3), RU, Ref, RL

Close(10, STATUS='KEEP') 
        
end subroutine planet