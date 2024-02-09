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

OTSO works on Windows, Linux, and Mac OS. Instructions for installing OTSO on each of these are located below.

## Installation

In order for OTSO to be installed and operate correctly, one must have a fortran compiler and python installed.
OTSO has been designed to work alongside the Anaconda python software as this makes OTSO much easier to use.

Installation instructions for OTSO outside of the anaconda environment will be provided in an update in the near future.

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
  - Run the `Windows_OTSO_Compiler.cmd` file located within the OTSO folder downloaded. If the previous steps have been completed correctly this should compile OTSO and it will be usable.

**Manual**
  - Open up an anaconda prompt to the Library folder directory.
  - Compile the library using the command `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC` within this anaconda prompt terminal.
  - Within the same terminal enter `ar cr OTSOlib.a *.o` to create the static library.
  - Copy all files that end with `.mod` and the `OTSOlib.a` file into the functions folder which can be found in the Parameters folder within the Tool directory.
  - Find the location of the `f2py-script.py` file on your computer and copy the complete path to this file (it should be located in your anaconda3 directory similar to `c:\User\anaconda3\Scripts\f2py-script.py`). We recommend copying this path to a `.txt` file within the OTSO folder for future reference. 
  - Open a new anaconda prompt, or change the directory in the already open one, to the Tool folder within OTSO and run the command `python [YOUR F2PY FILE PATH] -c --fcompiler=gnu95 --compiler=mingw32 -m MiddleMan MiddleMan.f95 OTSOlib.a`, replacing [YOUR F2PY FILE PATH] with the path to the `f2py-script.py` file on your computer.
  
## Linux

Easiest way to install OTSO on Linux is outlined below. Links to online tutorials are provided as well as plain summaries for each step bellow.
Note OTSO was tested on the Ubuntu OS and the following instructions will be for installing OTSO on this OS. It is possible the use of a different Linux OS could change the installation procedure. 

1. Install Gfortran onto your Linux system. Follow these [instructions](https://fortran-lang.org/en/learn/os_setup/install_gfortran/). A Summary is given bellow.
   - Open a terminal, enter in the command `sudo apt install gfortran` and run.
   - Gfortran should now be installed on your OS.

2. Install Anaconda on your Linux system. If you are using Ubuntu follow these [instructions](https://www.hostinger.com/tutorials/how-to-install-anaconda-on-ubuntu/). For other Linux OS use the following [instructions](https://docs.anaconda.com/anaconda/install/linux/). 
   - Open a terminal and enter the command `sudo apt-get update` to syncronise all repositories.
   - Change the directory to /tmp using the command `cd /tmp`
   - Ensure that wget is installed on your computer. Running `sudo apt-get install wget` within the same terminal will install wget if you don't already have it.
   - To download the Anaconda installer run the command `wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh`.
   - To check the integrity of the package enter `sha256sum Anaconda3-2022.05-Linux-x86_64.sh` into the terminal. If no errors are produced then proceed to the next step.
   - To install Anaconda run the command `bash Anaconda3-2022.05-Linux-x86_64.sh` in the same terminal.
   - You will now be prompted to read the licence agreement and accept the terms as well as choose the installation directory. Your home directory should already be selected and it is recommended you select this directory to install Anaconda too.
   - The installation is now complete. Close the terminal you are using. Future terminals that you open should have `(base)` at the start of the command line, this means that Anaconda is working and that you have access to all the packages within Anaconda.

3. OTSO must now be compiled in order to run. This can be done automatically via the provided bash file or manually.

**Automatic**
  - Open a terminal to the main OTSO directory and run the bash `Linux_and_Mac_OTSO_Compiler.sh` file. Enter `bash Linux_snd_Mac_OTSO_Compiler.sh` in the terminal and run. 

**Manual**
  - Open a terminal in the Library folder within OTSO. Enter `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC` into the terminal and run.
  - Next run the command `ar cr OTSOlib.a *.o` in the same terminal.
  - Copy all files that end with `.mod` and the `OTSOlib.a` file into the functions folder which can be found in the Parameters folder within the Tool directory.
  - Lastly, open a terminal within the Tool folder and run the command `f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a`
  
## Mac

Easiest way to install OTSO on Mac is outlined below. Links to online tutorials are provided as well as plain summaries for each step bellow.
Note OTSO was tested on the Monterey, Ventura, and Sonoma OS releases, as such the following instructions will be for installing OTSO on these versions of Mac OS. It is possible the use of older Mac OS releases could change the installation procedure. 

1. Install Anaconda on your Mac system. Follow these [instructions](https://docs.anaconda.com/anaconda/install/mac-os/) to download Anaconda on Mac. The Anaconda installer can be found [here](https://www.anaconda.com/products/distribution#macos).

2. Install Gfortran onto your Mac system using Anaconda. Follow these [instructions](https://anaconda.org/conda-forge/gfortran). A Summary is given bellow.
   - Open a terminal, enter in the command `conda install conda-forge::gfortran` and run.
   - Gfortran should now be installed on your OS.

3. OTSO must now be compiled in order to run. This can be done automatically via the provided bash file or manually.

**Automatic**
  - Open a terminal to the main OTSO directory and run the bash `Linux_and_Mac_OTSO_Compiler.sh` file. Enter `bash Linux_and_Mac_OTSO_Compiler.sh` in the terminal and run. 

**Manual**
  - Open a terminal in the Library folder within OTSO. Enter `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC` into the terminal and run.
  - Next run the command `ar cr OTSOlib.a *.o` in the same terminal.
  - Copy all files that end with `.mod` and the `OTSOlib.a` file into the functions folder which can be found in the Parameters folder within the Tool directory.
  - Lastly, open a terminal within the Tool folder and run the command `f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a`

## How to Use
If the compilation process has been completed without issue OTSO should now be ready to use. Within the `Tool/Parameters` folder there are python scripts that the user should edit to fit the simulations they wish to conduct (cone_params.py, trajectory_params.py, cutoff_params.py, and planet_params.py), please refer to the OTSO user manual for a more detailed decription. Once the input variables have been edited the user should run the python script in an Anaconda prompt / terminal within the Tool folder directory (e.g. `python Cone.py` will run the cone script used to compute asymptotic cones). Results from OTSO will be stored in a created folder called Results.

## Troubleshooting
- If there are errors in the compilation step for OTSO double check you have an up to date version of your fortran compiler, this may involve uninstalling your current version and re-instaling from scratch.
- Another issue you may encounter is a python 2 and python 3 conflict. If you are using python 3 for example f2py may need you to specify python 3 by typing `f2py3` during the compilation process, instead of just f2py`.
- (As more issues are found I will endeavour to keep this troubleshooting section up to date with any fixes for potential issues users may encounter)

## Publications Using OTSO
- Larsen, N., Mishev, A., & Usoskin, I. (2023). A new open-source geomagnetosphere propagation tool (OTSO) and its applications. Journal of Geophysical Research: Space Physics, 128, e2022JA031061. https://doi.org/10.1029/2022JA031061
- Larsen, N., & Mishev, A. L. (2023). Analysis of the ground level enhancement GLE 60 on 15 April 2001, and its space weather effects: Comparison with dosimetric measurements. Space Weather, 21, e2023SW003488. https://doi.org/10.1029/2023SW003488
