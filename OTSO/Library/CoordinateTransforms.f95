subroutine CoordinateValue(CoordIN, CoordOUT, integers)
    implicit none

    character(len = 3) :: CoordIN, CoordOUT
    integer(4) :: integers(2)

    IF (CoordIN == 'GDZ') THEN
        integers(1) = 0
     ELSE IF (CoordIN == 'GEO') THEN
        integers(1) = 1
     ELSE IF (CoordIN == 'GSM') THEN
        integers(1) = 2
     ELSE IF (CoordIN == 'GSE') THEN
        integers(1) = 3
     ELSE IF (CoordIN == 'SM') THEN
        integers(1) = 4
     ELSE IF (CoordIN == 'GEI') THEN
        integers(1) = 5
     ELSE IF (CoordIN == 'MAG') THEN
        integers(1) = 6
     ELSE IF (CoordIN == 'SPH') THEN
        integers(1) = 7
     ELSE IF (CoordIN == 'RLL') THEN
        integers(1) = 8
     END IF


     IF (CoordOUT == 'GDZ') THEN
        integers(2) = 0
     ELSE IF (CoordOUT == 'GEO') THEN
        integers(2) = 1
     ELSE IF (CoordOUT == 'GSM') THEN
        integers(2) = 2
     ELSE IF (CoordOUT == 'GSE') THEN
        integers(2) = 3
     ELSE IF (CoordOUT == 'SM') THEN
        integers(2) = 4
     ELSE IF (CoordOUT == 'GEI') THEN
        integers(2) = 5
     ELSE IF (CoordOUT == 'MAG') THEN
        integers(2) = 6
     ELSE IF (CoordOUT == 'SPH') THEN
        integers(2) = 7
     ELSE IF (CoordOUT == 'RLL') THEN
        integers(2) = 8
     END IF

end subroutine CoordinateValue


subroutine CoordinateTransform(CoordIN, CoordOUT, dateYear, dateDay, dateSec, xIN, xOUT)
    implicit none

    integer(8) :: dateYear, dateDay
    real(8) :: xIN(3), xOUT(3), dateSec
    character(len = 3) :: CoordIN, CoordOUT
    integer(4) :: integers(2)

    !f2py intent(in) CoordIN, CoordOUT, dateYear, dateDay, dateSec, xIN
    !f2py intent(out) xOUT

    call CoordinateValue(CoordIN, CoordOUT, integers)

    call coord_trans1(integers(1), integers(2), dateYear, dateDay, dateSec, xIN, xOUT)

end subroutine CoordinateTransform
