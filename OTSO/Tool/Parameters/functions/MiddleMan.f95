! **********************************************************************************************************************
! OTSO Functions:
!            This file contains the three main functions included within the OTSO tool.
!            Trajectory - will output the trajectory of a particle within the magnetosphere to a file
!            Cone - Will compute effective cutoff rigidity and asymptotic cone of any given location.
!                   All data is output into a file with a name of the user's choosing.
!            Planet -  Calculates the effective cutoff rigidity for any location on the Earth without doing
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
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: Pin(3), Pout(3), Wind(17), Bfield(3), Date(6)
    character(len = 3) :: CoordIN
    integer(4) :: I
    integer(8) :: mode(2)

    year = INT(Date(1))
    day = INT(Date(2))
    hour = INT(Date(3))
    minute = INT(Date(4))
    secondINT = INT(Date(5))
    secondTotal = real(Date(6))

    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

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
    
    call CoordinateTransform(CoordIN, CoordOUT, year, day, sec, Pin, Pout)
    
    end subroutine CoordTrans

! **********************************************************************************************************************
! Subroutine Trajectory:
!            subroutine that calculates the trajectory of a cosmic ray within different input
!            magnetic field models.
!            The output data is in the user given coordinate system.
!            Will also state if the cosmic ray has an allowed or forbidden trajectory.
!            Accepted Condition: cosmic ray encounters the magnetopause
!            Forbidden Conditions: - cosmic ray encounters the Earth (20km above Earth's surface)
!                                  - cosmic ray travels over 100Re without escaping or encountering Earth
!                                  - cosmic ray is simulated for a given period of time
!
! **********************************************************************************************************************
subroutine trajectory(PositionIN, Rigidity, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End)
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE IntegrationFunctions
USE Magnetopause
USE CUSTOMGAUSS
implicit none

real(8) :: PositionIN(5), Rigidity, Date(6), End(3)
real(8) :: Wind(17), Re, Lat, Long, GyroPercent
real(8) :: Xnew(3), XnewConverted(3)
integer(8) :: mode(2), IntMode, Anti, AtomicNumber
integer(4) :: I, Limit, Pause
character(len=50) :: FileName
character(len=3) :: CoordSystem

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
    print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
ELSE IF (PositionIN(5) > 360) THEN
    print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
    print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
    stop
END IF

call CreateParticle(PositionIN, Rigidity, Date, AtomicNumber, Anti, mode)

call initializeWind(Wind, I, mode)
call initializeCustomGauss(mode)

call MagneticFieldAssign(mode)
call MagnetopauseAssign(Pause)
call IntegrationAssign(IntMode)

call FirstTimeStep()

open(unit=10,file=FileName,status='replace')
write(10,"(a)")"X,Y,Z"

do while (Result == 0) 
call IntegrationPointer
call EscapeCheck()
call FinalStepCheck()
Xnew(1) = XnewTemp(1)/1000
Xnew(2) = XnewTemp(2)/1000
Xnew(3) = XnewTemp(3)/1000

call CoordinateTransform("GSM", CoordSystem, year, day, secondTotal, Xnew, XnewConverted)

if (model(1) == 4) then
    if (CoordSystem == "GEO") then
        XnewConverted = Xnew
    else
        call CoordinateTransform("GEO", CoordSystem, year, day, secondTotal, Xnew, XnewConverted)
    end if
end if

write(10,'(*(G0.6,:,","))') XnewConverted

IF (Position(1) < End(1) ) THEN
    print *, "This is Forbidden", "      Encountered Earth"
    call AsymptoticDirection(Lat, Long)
    print *, Lat, Long
    Limit = 1
    EXIT
END IF

IF (End(2) == 0) THEN
    
ELSE IF ( DistanceTraveled/1000.0 > End(2)*Re) THEN
    print *, "This is Forbidden", "      Exceeded Travel Distance Without Escape"
    print *, DistanceTraveled
    call AsymptoticDirection(Lat, Long)
    print *, Lat, Long
    Limit = 1
    EXIT
END IF

IF (End(3) == 0) THEN

ELSE IF ( TimeElapsed > End(3)) THEN
    print *, "This is Forbidden", "      Exceeded Maximum Time"
    print *, TimeElapsed
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
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            within different input magnetic field models and determines the Asymptotic Latitude and
!            Longitude. Will create a csv file in which the asymptotic cone data is stored.
!            Accepted Condition: cosmic ray encounters the model magnetopause
!            Forbidden Conditions: - cosmic ray encounters the Earth (20km above Earth's surface)
!                                  - cosmic ray travels over 100Re without escaping or encountering Earth
!                                  - cosmic ray is simulated for a given period of time
!
! **********************************************************************************************************************
subroutine cone(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE IntegrationFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(3)
    real(8) :: Wind(17), Re, Lat, Long, GyroPercent
    real(8) :: Geofile(3)
    integer(8) :: mode(2), IntMode, Anti, AtomicNumber
    integer(4) :: I, Limit, bool, Pause, stepNum
    character(len=50) :: FileName
    character(len=3) :: CoordSystem
    
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent

    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    IF (PositionIN(4) > 90.0) THEN
        print *, "ERROR: Please enter a zenith angle between 0 and 90 degrees"
        stop
    END IF
    
    IF (PositionIN(5) < 0) THEN
        print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    ELSE IF (PositionIN(5) > 360) THEN
        print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    END IF

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Rigidity(GV),Filter,Latitude,Longitude,X,Y,Z"

    do while (R > EndRigidity)

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)

    call FirstTimeStep()
    
    do while (Result == 0) 
    
    call IntegrationPointer()

    call EscapeCheck()

    call FinalStepCheck()
    
    IF (Position(1) < End(1) ) THEN
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

    IF (End(2) == 0) THEN
        
    ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
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

    IF (End(3) == 0) THEN
        
    ELSE IF (TimeElapsed > End(3)) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, lat, Long, "Forbidden",  "      Maximum Time Exceeded" !(Prints the outputs to the command module while running (Can lead to delays with multi-core proccessing))
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
    
    stepNum = stepNum + 1

    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
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
! Subroutine ConeGauss:
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            using custom Gaussian coefficients for the IGRF model and determines the Asymptotic Latitude and
!            Longitude. Will create a csv file in which the asymptotic cone data is stored.
!            Accepted Condition: cosmic ray encounters the model magnetopause
!            Forbidden Conditions: - cosmic ray encounters the Earth (20km above Earth's surface)
!                                  - cosmic ray travels over 100Re without escaping or encountering Earth
!                                  - cosmic ray is simulated for a given period of time
!
! **********************************************************************************************************************
subroutine conegauss(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End, gOTSO,hOTSO)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE IntegrationFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(3)
    real(8) :: Wind(17), Re, Lat, Long, GyroPercent
    real(8) :: Geofile(3)
    real(8) :: gOTSO(105), hOTSO(105)
    integer(8) :: mode(2), IntMode, Anti, AtomicNumber
    integer(4) :: I, Limit, bool, Pause, stepNum
    character(len=50) :: FileName
    character(len=3) :: CoordSystem
    
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent

    Ginput = gOTSO
    Hinput = hOTSO
    Gausschoice = 1
    mode(1) = 4 

    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    IF (PositionIN(4) > 90.0) THEN
        print *, "ERROR: Please enter a zenith angle between 0 and 90 degrees"
        stop
    END IF
    
    IF (PositionIN(5) < 0) THEN
        print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    ELSE IF (PositionIN(5) > 360) THEN
        print *, "ERROR: Please enter an azimuth angle between 0 and 360 degrees"
        print *, "N = 0, E = 90, S = 180, and W = 270 (degrees)"
        stop
    END IF

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Rigidity(GV),Filter,Latitude,Longitude,X,Y,Z"

    do while (R > EndRigidity)

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)

    call FirstTimeStep()
    
    do while (Result == 0) 
    
    call IntegrationPointer()

    call EscapeCheck()

    call FinalStepCheck()
    
    IF (Position(1) < End(1) ) THEN
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

    IF (End(2) == 0) THEN
        
    ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
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

    IF (End(3) == 0) THEN
        
    ELSE IF (TimeElapsed > End(3)) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, lat, Long, "Forbidden",  "      Maximum Time Exceeded" !(Prints the outputs to the command module while running (Can lead to delays with multi-core proccessing))
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
    
    stepNum = stepNum + 1

    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
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

end subroutine conegauss

! **********************************************************************************************************************
! Subroutine Cutoff:
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            within different input magnetic field models and determines the cutoff rigidity.
!            Will create a csv file in which the asymptotic cone data is stored.
!            Output can be the vertical cutoff or apparent cutoff
!            Apparent cutoff computation is roughly 9 times as long as vertical
!
! **********************************************************************************************************************
subroutine cutoff(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End, Rcomputation, scanchoice)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE IntegrationFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityScan, RigidityStep, Date(6), End(3)
    real(8) :: Wind(17), Re, Lat, Long, GyroPercent, EndLoop
    real(8) :: Geofile(3), RuMemory(9), RlMemory(9), RefMemory(9), Rigidity(3)
    real(8) :: Zenith(9), Azimuth(9), sumrl, sumru, sumref
    integer(8) :: mode(2), IntMode, Anti, AtomicNumber
    integer(4) :: I, Limit, bool, Pause, stepNum, loop, Rcomputation, scanchoice, scan, LastCheck
    character(len=50) :: FileName
    character(len=3) :: CoordSystem
    
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    loop = 1
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent
    sumrl = 0
    sumref = 0
    sumru = 0
    LastCheck = 0
    FailCheck = 0

    Rigidity(1) = StartRigidity
    Rigidity(2) = EndRigidity
    Rigidity(3) = RigidityStep

    RigidityScan = 0.50
    RigidityStep = 0.50

    Zenith(1) = 0
    Zenith(2) = 30
    Zenith(3) = 30
    Zenith(4) = 30
    Zenith(5) = 30
    Zenith(6) = 30
    Zenith(7) = 30
    Zenith(8) = 30
    Zenith(9) = 30

    Azimuth(1) = 0
    Azimuth(2) = 0
    Azimuth(3) = 45
    Azimuth(4) = 90
    Azimuth(5) = 135
    Azimuth(6) = 180
    Azimuth(7) = 225
    Azimuth(8) = 270
    Azimuth(9) = 315

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF


    IF (Rcomputation == 0) THEN
        EndLoop = 1.0
    ELSE
        EndLoop = 9.0
    END IF

    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Zenith,Azimuth,Ru,Rc,Rl"

    do while (loop <= EndLoop)
   
    100 do while (R > EndRigidity)

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)
    
    IF (R < Rigidity(3)) THEN
        R = EndRigidity
        GOTO 50
    END IF

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))
    
    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)

    call FirstTimeStep()
    test = 0

    do while (Result == 0)
    
    call IntegrationPointer()

    call EscapeCheck()

    call FinalStepCheck()
    
    IF (Position(1) < End(1) ) THEN
        bool = -1
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Returned to Earth"
        EXIT
    END IF

    IF (End(2) == 0) THEN
        
    ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Trapped"
        EXIT
    END IF

    IF (End(3) == 0) THEN
        
    ELSE IF (TimeElapsed > End(3)) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Time Elapsed"
        EXIT
    END IF
    
    IF (Result == 1) THEN
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        forbiddencount = 0
        bool = 1
        RL = R
        !print *, R, " ", "Escaped"
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    
    end do

    stepNum = stepNum + 1

    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
        IF(NeverFail == 0) THEN
            IF(LastCheck == 1) THEN
                R = EndRigidity
            END IF
            IF(LastCheck == 0) THEN
                R = Rigidity(3)
                LastCheck = 1
                stepNum = stepNum - 1
            END IF
        END IF
    END IF
    50 Result = 0

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    end do

    call EffectiveRigidity(RigidityStep)

    IF (scan == 0) THEN
        scan = 1
        StartRigidity = RU + 2.0*RigidityScan
        EndRigidity = RL - 2.0*RigidityScan
        IF (EndRigidity < 0) THEN
            EndRigidity = 0
        END IF
        R = StartRigidity
        RigidityStep = Rigidity(3)
        Limit = 0
        Acount = 0
        Result = 0
        forbiddencount = 0
        SubResult = 0
        stepNum = 0
        IF(NeverFail == 1) THEN
            NeverFail = 0
            GOTO 100
        ELSE IF(NeverFail == 0) THEN
            RU = 0
            RL = 0
            Ref = 0
        END IF
    END IF

    RlMemory(loop) = Rl
    RefMemory(loop) = Ref
    RuMemory(loop) = Ru

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
        StartRigidity = Rigidity(1)
        EndRigidity = Rigidity(2)
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF

    write(10,'(*(G0.6,:""))')PositionIN(4), ",", PositionIN(5), ",", Ru, ",", Ref, ",", Rl 

    loop = loop + 1
    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    forbiddencount = 0
    NeverFail = 0
    SubResult = 0
    LastCheck = 0
    FailCheck = 0

    end do

    IF(Rcomputation /= 0) THEN
        sumrl = RLMemory(1)/2.0
        do i = 2, 9
            sumrl = sumrl + RLMemory(i)/16.0
        end do
        sumru = RUMemory(1)/2.0
        do i = 2, 9
            sumru = sumru + RUMemory(i)/16.0
        end do
        sumref = RefMemory(1)/2.0
        do i = 2, 9
            sumref = sumref + RefMemory(i)/16.0
        end do

        RU = sumru
        RL = sumrl
        Ref = sumref
    END IF

    print *, "Ru:", RU
    print *, "Rl:", RL
    print *, "Rc:", Ref

    write(10,'(*(G0.6,:""))')"Ru:", RU, ",  Rc:", Ref, ",  Rl:", RL 

    Close(10, STATUS='KEEP') 

end subroutine cutoff

! **********************************************************************************************************************
! Subroutine Flight:
!            subroutine that calculates the cutoff rigidity along a given flight path under given
!            magnetic field models.
!            Will create a csv file in which the time, latitude, longitude, altitude, and cutoff rigidity is stored.
!            Can compute either vertical cutoff or apparent cutoff.
!            Apparent cutoff computation is roughly 9 times as long as vertical
!
! **********************************************************************************************************************
subroutine flight(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End, Rcomputation, scanchoice)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE IntegrationFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityScan, RigidityStep, Date(6), End(3)
    real(8) :: Wind(17), Re, Lat, Long, GyroPercent, EndLoop
    real(8) :: Geofile(3), RuMemory(9), RlMemory(9), RefMemory(9), Rigidity(3)
    real(8) :: Zenith(9), Azimuth(9), sumrl, sumru, sumref
    integer(8) :: mode(2), IntMode, Anti, AtomicNumber, FileNamePosition
    integer(4) :: I, Limit, bool, Pause, stepNum, loop, Rcomputation, scanchoice, scan, LastCheck
    character(len=50) :: FileName
    character(len=3) :: CoordSystem
    character(len=19) :: datetime_string
    
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    loop = 1
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent
    sumrl = 0
    sumref = 0
    sumru = 0
    LastCheck = 0
    FailCheck = 0

    Rigidity(1) = StartRigidity
    Rigidity(2) = EndRigidity
    Rigidity(3) = RigidityStep

    RigidityScan = 0.50
    RigidityStep = 0.50

    Zenith(1) = 0
    Zenith(2) = 30
    Zenith(3) = 30
    Zenith(4) = 30
    Zenith(5) = 30
    Zenith(6) = 30
    Zenith(7) = 30
    Zenith(8) = 30
    Zenith(9) = 30

    Azimuth(1) = 0
    Azimuth(2) = 0
    Azimuth(3) = 45
    Azimuth(4) = 90
    Azimuth(5) = 135
    Azimuth(6) = 180
    Azimuth(7) = 225
    Azimuth(8) = 270
    Azimuth(9) = 315

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF


    IF (Rcomputation == 0) THEN
        EndLoop = 1.0
    ELSE
        EndLoop = 9.0
    END IF

    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Time,Latitude,Longitude,Altitude,Rl,Rc,Ru"

    do while (loop <= EndLoop)
   
    100 do while (R > EndRigidity)

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    IF (R < Rigidity(3)) THEN
        R = EndRigidity
        GOTO 50
    END IF

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))
    
    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)

    call FirstTimeStep()
    test = 0

    do while (Result == 0)
    
    call IntegrationPointer()

    call EscapeCheck()

    call FinalStepCheck()
    
    IF (Position(1) < End(1) ) THEN
        bool = -1
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Returned to Earth"
        EXIT
    END IF

    IF (End(2) == 0) THEN
        
    ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Trapped"
        EXIT
    END IF

    IF (End(3) == 0) THEN
        
    ELSE IF (TimeElapsed > End(3)) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        !print *, R, " ", "Time Elapsed"
        EXIT
    END IF
    
    IF (Result == 1) THEN
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        forbiddencount = 0
        bool = 1
        RL = R
        !print *, R, " ", "Escaped"
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    
    end do
    
    stepNum = stepNum + 1

    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
        IF(NeverFail == 0) THEN
            IF(LastCheck == 1) THEN
                R = EndRigidity
            END IF
            IF(LastCheck == 0) THEN
                R = Rigidity(3)
                LastCheck = 1
                stepNum = stepNum - 1
            END IF
        END IF
    END IF
    50 Result = 0

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    end do

    call EffectiveRigidity(RigidityStep)

    IF (scan == 0) THEN
        scan = 1
        StartRigidity = RU + 2.0*RigidityScan
        EndRigidity = RL - 2.0*RigidityScan
        IF (EndRigidity < 0) THEN
            EndRigidity = 0
        END IF
        R = StartRigidity
        RigidityStep = Rigidity(3)
        Limit = 0
        Acount = 0
        Result = 0
        forbiddencount = 0
        SubResult = 0
        stepNum = 0
        IF(NeverFail == 1) THEN
            NeverFail = 0
            GOTO 100
        ELSE IF(NeverFail == 0) THEN
            RU = 0
            RL = 0
            Ref = 0
        END IF
    END IF

    RlMemory(loop) = Rl
    RefMemory(loop) = Ref
    RuMemory(loop) = Ru

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
        StartRigidity = Rigidity(1)
        EndRigidity = Rigidity(2)
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF

    loop = loop + 1
    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    forbiddencount = 0
    NeverFail = 0
    SubResult = 0
    LastCheck = 0
    FailCheck = 0

    end do

    IF(Rcomputation /= 0) THEN
        sumrl = RLMemory(1)/2.0
        do i = 2, 9
            sumrl = sumrl + RLMemory(i)/16.0
        end do
        sumru = RUMemory(1)/2.0
        do i = 2, 9
            sumru = sumru + RUMemory(i)/16.0
        end do
        sumref = RefMemory(1)/2.0
        do i = 2, 9
            sumref = sumref + RefMemory(i)/16.0
        end do

        RU = sumru
        RL = sumrl
        Ref = sumref
    END IF

    FileName = trim(FileName )
    FileNamePosition = index(FileName , ".csv")
    datetime_string = FileName(1:FileNamePosition-1)

    write(10,'(*(G0.6,:""))') datetime_string, "," , PositionIN(2), "," , PositionIN(3), "," ,PositionIN(1), &
    ",", RU, ",", Ref, "," , RL 

    Close(10, STATUS='KEEP') 

end subroutine flight

! **********************************************************************************************************************
! Subroutine CutoffGauss:
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            using custom Gaussian coefficients for the IGRF model and determines the cutoff rigidity.
!            Will create a csv file in which the cutoff data is stored.
!            Output can be the vertical cutoff or apparent cutoff
!            Apparent cutoff computation is roughly 9 times as long as vertical
!
! **********************************************************************************************************************
subroutine cutoffgauss(PositionIN, StartRigidity, EndRigidity, RigidityStep, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End, Rcomputation, scanchoice, &
    gOTSO,hOTSO)
    USE Particle
    USE SolarWind
    USE MagneticFieldFunctions
    USE MagnetopauseFunctions
    USE IntegrationFunctions
    USE GEOPACK1
    USE GEOPACK2
    USE Magnetopause
    USE CUSTOMGAUSS
    implicit none
    
    real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityScan, RigidityStep, Date(6), End(3)
    real(8) :: Wind(17), Re, Lat, Long, GyroPercent, EndLoop
    real(8) :: Geofile(3), RuMemory(9), RlMemory(9), RefMemory(9), Rigidity(3)
    real(8) :: Zenith(9), Azimuth(9), sumrl, sumru, sumref
    real(8) :: gOTSO(105), hOTSO(105)
    integer(8) :: mode(2), IntMode, Anti, AtomicNumber
    integer(4) :: I, Limit, bool, Pause, stepNum, loop, Rcomputation, scanchoice, scan, LastCheck
    character(len=50) :: FileName
    character(len=3) :: CoordSystem
    
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    loop = 1
    forbiddencount = 0
    NeverFail = 0
    Step = RigidityStep
    SubResult = 0
    MaxGyroPercent = GyroPercent
    sumrl = 0
    sumref = 0
    sumru = 0
    LastCheck = 0
    FailCheck = 0

    Ginput = gOTSO
    Hinput = hOTSO
    Gausschoice = 1
    mode(1) = 4 

    Rigidity(1) = StartRigidity
    Rigidity(2) = EndRigidity
    Rigidity(3) = RigidityStep

    RigidityScan = 0.50
    RigidityStep = 0.50

    Zenith(1) = 0
    Zenith(2) = 30
    Zenith(3) = 30
    Zenith(4) = 30
    Zenith(5) = 30
    Zenith(6) = 30
    Zenith(7) = 30
    Zenith(8) = 30
    Zenith(9) = 30

    Azimuth(1) = 0
    Azimuth(2) = 0
    Azimuth(3) = 45
    Azimuth(4) = 90
    Azimuth(5) = 135
    Azimuth(6) = 180
    Azimuth(7) = 225
    Azimuth(8) = 270
    Azimuth(9) = 315

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF


    IF (Rcomputation == 0) THEN
        EndLoop = 1.0
    ELSE
        EndLoop = 9.0
    END IF

    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    open(unit=10,file=FileName,status='replace')
    write(10,"(a)")"Zenith,Azimuth,Ru,Rc,Rl"

    do while (loop <= EndLoop)
   
    100 do while (R > EndRigidity)

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))

    IF (R < Rigidity(3)) THEN
        R = EndRigidity
        GOTO 50
    END IF

    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
    
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)

    call FirstTimeStep()
    
    do while (Result == 0) 
    
    call IntegrationPointer()

    call EscapeCheck()

    call FinalStepCheck()
    
    IF (Position(1) < End(1) ) THEN
        bool = -1
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        EXIT
    END IF

    IF (End(2) == 0) THEN
        
    ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        EXIT
    END IF

    IF (End(3) == 0) THEN
        
    ELSE IF (TimeElapsed > End(3)) THEN
        bool = 0
        Limit = 1
        forbiddencount = forbiddencount + 1
        NeverFail = 1
        FailCheck = 1
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        EXIT
    END IF
    
    IF (Result == 1) THEN
        call AsymptoticDirection(Lat, Long)
        call CoordinateTransform("GDZ", CoordSystem, year, day, secondTotal, Position, GEOfile)
        forbiddencount = 0
        bool = 1
        RL = R
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    
    end do
    
    stepNum = stepNum + 1

    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
        IF(NeverFail == 0) THEN
            IF(LastCheck == 1) THEN
                R = EndRigidity
            END IF
            IF(LastCheck == 0) THEN
                R = Rigidity(3)
                LastCheck = 1
                stepNum = stepNum - 1
            END IF
        END IF
    END IF
    50 Result = 0

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    end do

    call EffectiveRigidity(RigidityStep)

    IF (scan == 0) THEN
        scan = 1
        StartRigidity = RU + 2.0*RigidityScan
        EndRigidity = RL - 2.0*RigidityScan
        IF (EndRigidity < 0) THEN
            EndRigidity = 0
        END IF
        R = StartRigidity
        RigidityStep = Rigidity(3)
        Limit = 0
        Acount = 0
        Result = 0
        forbiddencount = 0
        SubResult = 0
        stepNum = 0
        IF(NeverFail == 1) THEN
            NeverFail = 0
            GOTO 100
        ELSE IF(NeverFail == 0) THEN
            RU = 0
            RL = 0
            Ref = 0
        END IF
    END IF

    RlMemory(loop) = Rl
    RefMemory(loop) = Ref
    RuMemory(loop) = Ru

    IF (scanchoice == 1) THEN
        scan = 0
        RigidityStep = RigidityScan
        StartRigidity = Rigidity(1)
        EndRigidity = Rigidity(2)
    ELSE
        scan = 1
        RigidityStep = Rigidity(3)
    END IF

    write(10,'(*(G0.6,:""))')PositionIN(4), ",", PositionIN(5), ",", Ru, ",", Ref, ",", Rl 

    loop = loop + 1
    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)
    R = real(StartRigidity, kind = selected_real_kind(15,307))
    Re = 6371.2
    Limit = 0
    Acount = 0
    Result = 0
    stepNum = 0
    forbiddencount = 0
    NeverFail = 0
    SubResult = 0
    LastCheck = 0
    FailCheck = 0

    end do

    IF(Rcomputation /= 0) THEN
        sumrl = RLMemory(1)/2.0
        do i = 2, 9
            sumrl = sumrl + RLMemory(i)/16.0
        end do
        sumru = RUMemory(1)/2.0
        do i = 2, 9
            sumru = sumru + RUMemory(i)/16.0
        end do
        sumref = RefMemory(1)/2.0
        do i = 2, 9
            sumref = sumref + RefMemory(i)/16.0
        end do

        RU = sumru
        RL = sumrl
        Ref = sumref
    END IF

    print *, "Ru:", RU
    print *, "Rl:", RL
    print *, "Rc:", Ref

    write(10,'(*(G0.6,:""))')"Ru:", RU, ",  Rc:", Ref, ",  Rl:", RL 

    Close(10, STATUS='KEEP') 

end subroutine cutoffgauss

! **********************************************************************************************************************
! Subroutine Planet:
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            within different input magnetic field models and determines the effective cutoff rigidity for
!            a range of latitude and longitudes. Typically done over the entire planet.
!            Will create a csv file with the calculated rigidities for the locations.
!            This code works with the Planet.py tool to assign large amounts of locations across multiple cores.
!            A planet.csv file will be produced storing the data for latitude, longitude, and cutoff
!
! **********************************************************************************************************************
subroutine planet(PositionIN, Rigidity, Date, mode, IntMode, AtomicNumber, Anti, I, Wind, Pause, &
     FileName, GyroPercent, End, Rcomputation, scanchoice)
USE Particle
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE IntegrationFunctions
USE Magnetopause
USE CUSTOMGAUSS
implicit none
real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(3)
real(8) :: Wind(17), Re, Rigidity(3), GyroPercent, RigidityScan, Zenith(9), Azimuth(9)
real(8) :: RuMemory(9), RlMemory(9), RefMemory(9), EndLoop, sumrl, sumru, sumref
integer(8) :: mode(2), IntMode, Anti, AtomicNumber
integer(4) :: I, Limit, bool, Pause, scan, stepNum, Rcomputation, loop, scanchoice, LastCheck
character(len=30) :: FileName

Zenith(1) = 0
Zenith(2) = 30
Zenith(3) = 30
Zenith(4) = 30
Zenith(5) = 30
Zenith(6) = 30
Zenith(7) = 30
Zenith(8) = 30
Zenith(9) = 30

Azimuth(1) = 0
Azimuth(2) = 0
Azimuth(3) = 45
Azimuth(4) = 90
Azimuth(5) = 135
Azimuth(6) = 180
Azimuth(7) = 225
Azimuth(8) = 270
Azimuth(9) = 315
            
StartRigidity = Rigidity(1)
EndRigidity = Rigidity(2)
RigidityScan = 0.50
RigidityStep = 0.50

R = StartRigidity
Ru = StartRigidity
Re = 6371.2
Limit = 0
Acount = 0
Result = 0
loop = 1
NeverFail = 0
stepNum = 0
forbiddencount = 0
Step = RigidityStep
SubResult = 0
MaxGyroPercent = GyroPercent
LastCheck = 0
FailCheck = 0

IF (scanchoice == 1) THEN
    scan = 0
    RigidityStep = RigidityScan
ELSE
    scan = 1
    RigidityStep = Rigidity(3)
END IF

sumref = 0
sumrl = 0
sumru = 0

PositionIN(4) = Zenith(loop)
PositionIN(5) = Azimuth(loop)


IF (Rcomputation == 0) THEN
    EndLoop = 1.0
ELSE
    EndLoop = 9.0
END IF
        
open(unit=10,file=FileName,action='write',position='append')
write(10,"(a)")"Latitude,Longitude,Ru,Rc,Rl"
do while (loop <= EndLoop)
100 do while (R > EndRigidity)

    R = real(R, kind = selected_real_kind(10,307))
    RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))
    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

    IF (R < Rigidity(3)) THEN
        R = EndRigidity
        GOTO 50
    END IF

    call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)        
    call initializeWind(Wind, I, mode)
    call initializeCustomGauss(mode)

    call MagneticFieldAssign(mode)
    call MagnetopauseAssign(Pause)
    call IntegrationAssign(IntMode)
            
    call FirstTimeStep()
            
    do while (Result == 0) 
            
        call IntegrationPointer
        
        call EscapeCheck()

        call FinalStepCheck()
            
        IF (Position(1) < End(1)) THEN
            bool = -1
            Limit = 1
            forbiddencount = forbiddencount + 1
            NeverFail = 1
            FailCheck = 1
            EXIT
        END IF
        
        IF (End(2) == 0) THEN
            
        ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
            bool = 0
            Limit = 1
            forbiddencount = forbiddencount + 1
            NeverFail = 1
            FailCheck = 1
            EXIT
        END IF

        IF (End(3) == 0) THEN
            
        ELSE IF (TimeElapsed > End(3)) THEN
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
        IF (Limit == 0) THEN
            RU = R
        ELSE IF (Limit == 1) THEN
            Acount = Acount + 1
        END IF
        EXIT
    END IF
    end do

    stepNum = stepNum + 1
            
    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
        IF(NeverFail == 0) THEN
            IF(LastCheck == 1) THEN
                R = EndRigidity
            END IF
            IF(LastCheck == 0) THEN
                R = Rigidity(3)
                LastCheck = 1
                stepNum = stepNum - 1
            END IF
        END IF
    END IF
    50 Result = 0

    PositionIN(4) = Zenith(loop)
    PositionIN(5) = Azimuth(loop)

end do
        
call EffectiveRigidity(RigidityStep)

IF (scan == 0) THEN
    scan = 1
    StartRigidity = RU + 2.0*RigidityScan
    EndRigidity = RL - 2.0*RigidityScan
    IF (EndRigidity < 0) THEN
        EndRigidity = 0
    END IF
    R = StartRigidity
    RigidityStep = Rigidity(3)
    Limit = 0
    Acount = 0
    Result = 0
    forbiddencount = 0
    SubResult = 0
    stepNum = 0
    IF(NeverFail == 1) THEN
        NeverFail = 0
        GOTO 100
    ELSE IF(NeverFail == 0) THEN
        RU = 0
        RL = 0
        Ref = 0
    END IF
END IF

RlMemory(loop) = Rl
RefMemory(loop) = Ref
RuMemory(loop) = Ru

loop = loop + 1
R = real(StartRigidity, kind = selected_real_kind(15,307))
Re = 6371.2
Limit = 0
Acount = 0
Result = 0
stepNum = 0
forbiddencount = 0
NeverFail = 0
SubResult = 0
LastCheck = 0
FailCheck = 0

IF (scanchoice == 1) THEN
    scan = 0
    RigidityStep = RigidityScan
    StartRigidity = Rigidity(1)
    EndRigidity = Rigidity(2)
ELSE
    scan = 1
    RigidityStep = Rigidity(3)
END IF

IF(Rcomputation /= 0) THEN
    sumrl = RLMemory(1)/2.0
    do i = 2, 9
        sumrl = sumrl + RLMemory(i)/16.0
    end do
    sumru = RUMemory(1)/2.0
    do i = 2, 9
        sumru = sumru + RUMemory(i)/16.0
    end do
    sumref = RefMemory(1)/2.0
    do i = 2, 9
        sumref = sumref + RefMemory(i)/16.0
    end do

    RU = sumru
    RL = sumrl
    Ref = sumref
END IF

end do

sumrl = 0
sumru = 0
sumref = 0


print *, "Latitude: ", PositionIN(2), "    Longitude: ", PositionIN(3), "    Ru: ", RU, "    Rc: ", Ref, "    Rl: ", RL
        
write(10,'(*(G0.6,:,","))') PositionIN(2), PositionIN(3), RU, Ref, RL

Close(10, STATUS='KEEP') 
        
end subroutine planet

! **********************************************************************************************************************
! Subroutine FieldTrace:
!            subroutine that traces the magnetic field lines within different inputted
!            magnetic field models. The field lines are output in csv files named within a zip file.
! **********************************************************************************************************************
subroutine FieldTrace(PositionIN, Rigidity, Date, mode, IntMode, & 
    AtomicNumber, Anti, I, Wind, Pause, FileName, CoordSystem, GyroPercent, End)
USE Particle
USE GEOPACK1
USE GEOPACK2
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE IntegrationFunctions
USE Magnetopause
USE CUSTOMGAUSS
implicit none

real(8) :: PositionIN(5), Rigidity, Date(6), End(3)
real(8) :: Wind(17), Re, GyroPercent
real(8) :: Xnew(3), XnewConverted(3), Bfield(3)
integer(8) :: mode(2), IntMode, Anti, AtomicNumber
integer(4) :: I, Limit, Pause
character(len=50) :: FileName
character(len=3) :: CoordSystem

Re = 6371.2
Limit = 0
Acount = 0
Result = 0
SubResult = 0
MaxGyroPercent = GyroPercent

call CreateParticle(PositionIN, Rigidity, Date, AtomicNumber, Anti, mode)

call initializeWind(Wind, I, mode)
call initializeCustomGauss(mode)

call MagneticFieldAssign(mode)
call MagnetopauseAssign(Pause)
call IntegrationAssign(IntMode)

open(unit=10,file=FileName,status='replace')
write(10,"(a)")"X,Y,Z,Bx,By,Bz"

do while (Result == 0) 
call RK4_FieldTrace(Bfield)
call EscapeCheck()
Xnew(1) = XnewTemp(1)/1000
Xnew(2) = XnewTemp(2)/1000
Xnew(3) = XnewTemp(3)/1000

call CoordinateTransform("GSM", CoordSystem, year, day, secondTotal, Xnew, XnewConverted)

if (model(1) == 4) then
    if (CoordSystem == "GEO") then
        XnewConverted = Xnew
    else
        call CoordinateTransform("GEO", CoordSystem, year, day, secondTotal, Xnew, XnewConverted)
    end if
end if

IF ( DistanceTraveled/1000.0 > End(2)*Re) THEN
    Limit = 1
    EXIT
END IF

write(10,'(*(G0.6,:,","))') XnewConverted, Bfield

IF (Position(1) < End(1) ) THEN
    EXIT
END IF

IF (Result == 1)  THEN
    EXIT
END IF

end do

Close(10, STATUS='KEEP') 

end subroutine FieldTrace

! **********************************************************************************************************************
! Subroutine PlanetGauss:
!            subroutine that calculates the trajectory of a cosmic ray across a range of rigidities
!            using custom Gaussian coefficients for the IGRF model and determines the cutoff rigidity for
!            a range of latitude and longitudes. Typically done over the entire planet.
!            Will create a csv file with the calculated rigidities for the locations.
!            This code works with the Planet.py tool to assign large amounts of locations across multiple cores.
!            A planet.csv file will be produced storing the data for latitude, longitude, and cutoff
!
! **********************************************************************************************************************
subroutine planetgauss(PositionIN, Rigidity, Date, mode, IntMode, AtomicNumber, Anti, I, Wind, Pause, &
    FileName, GyroPercent, End, Rcomputation, scanchoice,gOTSO,hOTSO)
USE Particle
USE SolarWind
USE MagneticFieldFunctions
USE MagnetopauseFunctions
USE IntegrationFunctions
USE Magnetopause
USE CUSTOMGAUSS
implicit none
real(8) :: PositionIN(5), StartRigidity, EndRigidity, RigidityStep, Date(6), End(3)
real(8) :: Wind(17), Re, Rigidity(3), GyroPercent, RigidityScan, Zenith(9), Azimuth(9)
real(8) :: RuMemory(9), RlMemory(9), RefMemory(9), EndLoop, sumrl, sumru, sumref
real(8) :: gOTSO(105), hOTSO(105)
integer(8) :: mode(2), IntMode, Anti, AtomicNumber
integer(4) :: I, Limit, bool, Pause, scan, stepNum, Rcomputation, loop, scanchoice, LastCheck
character(len=30) :: FileName

Ginput = gOTSO
Hinput = hOTSO

Gausschoice = 1
mode(1) = 4 

Zenith(1) = 0
Zenith(2) = 30
Zenith(3) = 30
Zenith(4) = 30
Zenith(5) = 30
Zenith(6) = 30
Zenith(7) = 30
Zenith(8) = 30
Zenith(9) = 30

Azimuth(1) = 0
Azimuth(2) = 0
Azimuth(3) = 45
Azimuth(4) = 90
Azimuth(5) = 135
Azimuth(6) = 180
Azimuth(7) = 225
Azimuth(8) = 270
Azimuth(9) = 315
           
StartRigidity = Rigidity(1)
EndRigidity = Rigidity(2)
RigidityScan = 0.50
RigidityStep = 0.50

R = StartRigidity
Ru = StartRigidity
Re = 6371.2
Limit = 0
Acount = 0
Result = 0
loop = 1
NeverFail = 0
stepNum = 0
forbiddencount = 0
Step = RigidityStep
SubResult = 0
MaxGyroPercent = GyroPercent
LastCheck = 0
FailCheck = 0

IF (scanchoice == 1) THEN
   scan = 0
   RigidityStep = RigidityScan
ELSE
   scan = 1
   RigidityStep = Rigidity(3)
END IF

sumref = 0
sumrl = 0
sumru = 0

PositionIN(4) = Zenith(loop)
PositionIN(5) = Azimuth(loop)

IF (Rcomputation == 0) THEN
   EndLoop = 1.0
ELSE
   EndLoop = 9.0
END IF
       
open(unit=10,file=FileName,action='write',position='append')
write(10,"(a)")"Latitude,Longitude,Ru,Rc,Rl"
do while (loop <= EndLoop)
100 do while (R > EndRigidity)

   R = real(R, kind = selected_real_kind(10,307))
   RigidityStep = real(RigidityStep, kind = selected_real_kind(10,307))
   PositionIN(4) = Zenith(loop)
   PositionIN(5) = Azimuth(loop)

    IF (R < Rigidity(3)) THEN
        R = EndRigidity
        GOTO 50
    END IF

   call CreateParticle(PositionIN, R, Date, AtomicNumber, Anti, mode)
           
   call initializeWind(Wind, I, mode)
   call initializeCustomGauss(mode)

   call MagneticFieldAssign(mode)
   call MagnetopauseAssign(Pause)
   call IntegrationAssign(IntMode)
           
   call FirstTimeStep()
           
   do while (Result == 0) 
           
       call IntegrationPointer
       
       call EscapeCheck()

       call FinalStepCheck()
           
       IF (Position(1) < End(1)) THEN
           bool = -1
           Limit = 1
           forbiddencount = forbiddencount + 1
           NeverFail = 1
           FailCheck = 1
           EXIT
       END IF
       
       IF (End(2) == 0) THEN
           
       ELSE IF (DistanceTraveled/1000.0 > End(2) * Re) THEN
           bool = 0
           Limit = 1
           forbiddencount = forbiddencount + 1
           NeverFail = 1
           FailCheck = 1
           EXIT
       END IF

       IF (End(3) == 0) THEN
           
       ELSE IF (TimeElapsed > End(3)) THEN
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
       IF (Limit == 0) THEN
           RU = R
       ELSE IF (Limit == 1) THEN
           Acount = Acount + 1
       END IF
       EXIT
   END IF
   end do

   stepNum = stepNum + 1
           
    R = (StartRigidity - (stepNum*RigidityStep))
    IF(R < EndRigidity) THEN
        R = EndRigidity
    ELSE IF (R < RigidityStep) THEN
        IF(NeverFail == 0) THEN
            IF(LastCheck == 1) THEN
                R = EndRigidity
            END IF
            IF(LastCheck == 0) THEN
                R = Rigidity(3)
                LastCheck = 1
                stepNum = stepNum - 1
            END IF
        END IF
    END IF
   50 Result = 0
       
end do

PositionIN(4) = Zenith(loop)
PositionIN(5) = Azimuth(loop)
       
call EffectiveRigidity(RigidityStep)

IF (scan == 0) THEN
   scan = 1
   StartRigidity = RU + 2.0*RigidityScan
   EndRigidity = RL - 2.0*RigidityScan
   IF (EndRigidity < 0) THEN
       EndRigidity = 0
   END IF
   R = StartRigidity
   RigidityStep = Rigidity(3)
   Limit = 0
   Acount = 0
   Result = 0
   forbiddencount = 0
   SubResult = 0
   stepNum = 0
   IF(NeverFail == 1) THEN
       NeverFail = 0
       GOTO 100
   ELSE IF(NeverFail == 0) THEN
       RU = 0
       RL = 0
       Ref = 0
   END IF
END IF

RlMemory(loop) = Rl
RefMemory(loop) = Ref
RuMemory(loop) = Ru

loop = loop + 1
R = real(StartRigidity, kind = selected_real_kind(15,307))
Re = 6371.2
Limit = 0
Acount = 0
Result = 0
stepNum = 0
forbiddencount = 0
NeverFail = 0
SubResult = 0
LastCheck = 0
FailCheck = 0

IF (scanchoice == 1) THEN
   scan = 0
   RigidityStep = RigidityScan
   StartRigidity = Rigidity(1)
   EndRigidity = Rigidity(2)
ELSE
   scan = 1
   RigidityStep = Rigidity(3)
END IF

IF(Rcomputation /= 0) THEN
   sumrl = RLMemory(1)/2.0
   do i = 2, 9
       sumrl = sumrl + RLMemory(i)/16.0
   end do
   sumru = RUMemory(1)/2.0
   do i = 2, 9
       sumru = sumru + RUMemory(i)/16.0
   end do
   sumref = RefMemory(1)/2.0
   do i = 2, 9
       sumref = sumref + RefMemory(i)/16.0
   end do

   RU = sumru
   RL = sumrl
   Ref = sumref
END IF

end do

sumrl = 0
sumru = 0
sumref = 0


print *, "Latitude: ", PositionIN(2), "    Longitude: ", PositionIN(3), "    Ru: ", RU, "    Rc: ", Ref, "    Rl: ", RL
       
write(10,'(*(G0.6,:,","))') PositionIN(2), PositionIN(3), RU, Ref, RL

Close(10, STATUS='KEEP') 
       
end subroutine planetgauss
