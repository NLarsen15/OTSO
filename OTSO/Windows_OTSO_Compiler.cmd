echo off
@setlocal enableextensions enabledelayedexpansion

if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit

call cd Library/
call gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC
call ar cr OTSOlib.a *.o
call cd ..
call xcopy ".\Library\*.mod" ".\Tool\Parameters\functions" /Y
call xcopy ".\Library\*.a" ".\Tool\Parameters\functions" /Y


set searchVal=\anaconda3\Scripts\activate.bat
set f2pysearchVal=\anaconda3\Scripts\f2py-script.py
set "UserPath=\All Users\"
set activate_path=\
set f2py_path=\
set count=0

    if exist Recompile.txt (
    for /F "tokens=*" %%a in (Recompile.txt) do (
    set /a count+=1
    set RecompileVar[!count!]=%%a
    )
    call !RecompileVar[1]!
    call cd Tool/Parameters/functions
    call python !RecompileVar[2]!  -c --fcompiler=gnu95 --compiler=mingw32 -m MiddleMan MiddleMan.f95 OTSOlib.a
    if errorlevel 1 (
    echo OTSO compilation failed
    ) else (
    echo OTSO compilation complete
    )
    del *.mod
    del *.a
    call cd ..
    call cd ..
    call cd ..
    call cd Library/
    del *.o
    del *.mod
    del *.a
) else (
    for %%a in (c d e f g h) do (
        if exist "%%a:" dir "%%a:\activate.bat"2>NUL /b /s /a-d do echo >> Activate_Text.txt
    )
    for /F "tokens=*" %%I in (Activate_Text.txt) do (
    set str=%%I 
    Echo.!str! | findstr /R /I /C:"All Users">nul
    if not !errorlevel!==0 ( Echo.!str! | findstr /I /C:"!searchVal!">nul
    if !errorlevel!==0 ( set activate_path=!str! & echo !activate_path!)
    ))
    

    for %%b in (c d e f g h) do (
        if exist "%%b:" dir "%%b:\f2py-script.py"2>NUL /b /s /a-d do echo >> F2PY_Text.txt
    )
    for /F "tokens=*" %%C in (F2PY_Text.txt) do (
    set str=%%C
    Echo.!str! | findstr /R /I /C:"All Users">nul
    if not !errorlevel!==0 ( Echo.!str! | findstr /I /C:"!f2pysearchVal!">nul
    if !errorlevel!==0 ( set f2py_path=!str! & echo !f2py_path!)
    ))

    call !activate_path!
    Echo.!activate_path! > Recompile.TXT
    Echo.!f2py_path! >> Recompile.TXT
    call cd Tool/Parameters/functions
    call python !f2py_path! -c --fcompiler=gnu95 --compiler=mingw32 -m MiddleMan MiddleMan.f95 OTSOlib.a
    if errorlevel 1 (
    echo OTSO compilation failed
    ) else (
    echo OTSO compilation complete
    )
    del *.mod
    del *.a
    call cd ..
    call cd ..
    call cd ..
    del Activate_Text.txt
    del F2PY_Text.txt
    call cd Library/
    del *.o
    del *.mod
    del *.a
)
PAUSE