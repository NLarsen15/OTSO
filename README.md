# OTSO
Oulu - Open-source geomagneToSphere prOpagation tool

OTSO is a geophysics tool used to compute the trajectories of cosmic rays within the Earth's magnetosphere. 
These computations are used to determine physical values, such as cut-off rigidities and asymptotic cones for locations on the Earth, 
that are needed by the cosmic ray research community.
OTSO provides the user with free reign to select from a plethora of input parameters for tests, such as geomagetospheric conditions, 
as well as offering various magnetospheric models to choose from. 

OTSO is developed using fortran and python. A knowledge of fortran is not needed to use the tool, however, it is required if the user wishes to edit the internal code of the tool (e.g. to add new magnetosphere models). 

OTSO is open-source. Therefore, additions and suggestions from the community are welcome. 

This is a base release for the tool and bugs are to be expected. I ask the community to please inform me of any bugs they may encounter or provide solutions that can be added to the base code of OTSO.

## Installation

This base release of OTSO has only been tested on the Windows OS.
Once OTSO has been tested on more operating systems its installation instructions will be updated accordingly.

In order for OTSO to be installed and operate correctly, one must have a fortran compiler and python installed.
OTSO has been designed to work alongside the anaconda python software as this makes OTSO much easier to use.

## Windows OS

The easiest way to install OTSO on windows is outlined below.

1. Download and install [Anaconda](https://www.anaconda.com/) on your system.

2. Download and install [MSYS2](https://www.msys2.org/) on your system. To install the fortran compiler follow the steps below.
   - First enter `pacman -Syu` into the MSYS2 terminal to update the packages
   - After this is finished MSYS2 will close, open up the terminal again and repeat the first step until no more updates are needed.
   - To install the fortran compiler, enter `pacman -S --needed base-devel mingw-w64-x86_64-toolchain` into the MSYS2 terminal. Select the default option of `all` when prompted.
   - The last step for installing the fortran compiler is to add the directory where the `.exe` file for gfortran is to the environment path variables. The file is typically found at `C:\msys64\mingw64\bin`, but this can vary depending on where you decided to install MSYS2. To add this directory to the environment path variables you can follow these [instructions](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

3. In order to run on your computer, OTSO needs to be compiled. This can either be done automatically or manually. We suggest using the automatic compilation first and only attempting the manual way if the former method fails.

**Automatic**
  - Run the `OTSOCompiler.cmd` file located within the OTSO folder downloaded. If the previous steps have been completed correctly this should compile OTSO and it will be usable.

**Manual**
  - Open up an anaconda prompt to the Library folder directory.
  - Compile the library using the command `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f` within this anaconda prompt terminal.
  - Within the same terminal enter `ar cr OTSOlib.a *.o` to create the static library.
  - Copy the `OTSOlib.a` file and all the `.mod` files into the Tool folder.
  - Find the location of the `f2py-script.py` file on your computer and copy the complete path to this file (it should be located in your anaconda3 directory similar to `c:\User\anaconda3\Scripts\f2py-script.py`). We recommend copying this path to a `.txt` file within the OTSO folder for future reference. 
  - Open a new anaconda prompt, or change the directory in the already open one, to the Tool folder within OTSO and run the command `python [YOUR F2PY FILE PATH] -c --fcompiler=gnu95 --compiler=mingw32 -m MiddleMan MiddleMan.f95 OTSOlib.a`, replacing the [YOUR F2PY FILE PATH] with the path to the `f2py-script.py` file on your computer.

# How to Use
If the compilation process has been completed without issue OTSO should now be ready to use. Within the Tool folder there are python scripts that the user should edit to fit the simulations they wish to conduct, please refer to the OTSO user manual for a more detailed decription. Once the input variables have been edited the user should run the python script in an anaconda prompt within the Tool folder directory (e.g. `python Cone.py` will run the cone script).

