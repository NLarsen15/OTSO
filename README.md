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

Installation instructions for OTSO outside of the Anaconda environment will be provided in the future. 
Currently Linux is the only OS where OTSO has been reliably installed without the use of Anaconda.

## Current Issues

OTSO is designed around the Anaconda framework and utilises numpy distutils with f2py for compilation. Numpy has moved on from distutils in favor of meson as a compilation tool when using f2py, and this new version of numpy is provided as default in newer anaconda releases. Currently, attempts to compile OTSO with the new numpy and Anaconda have been unsuccessful. A temporary solution is to download an older release of Anaconda with the old numpy distribution included. To do this, go to [the old Anaconda releases repository](https://repo.anaconda.com/archive/) and download an older version of Anaconda. OTSO was developed on the 2022 release, so finding and installing anaconda via the installer labelled `Anaconda3-2022.10` will fix this issue. Ensure that numpy version 1.21.5 is installed.

Once a successful install of OTSO has been conducted using the new meson f2py the instructions will be added to this repository so users may use whatever version of Anaconda they desire.

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
  - Run the `Windows_OTSO_Compiler.cmd` file located within the OTSO folder (the folder containing user manual) downloaded. If the previous steps have been completed correctly this should compile OTSO and it will be usable.
  - Alternatively, you may instead run the `makefile` using the command `make` within the same terminal if you have make installed on your system. 

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
  - Open a terminal to the main OTSO directory (the folder containing user manual) and run the bash `Linux_and_Mac_OTSO_Compiler.sh` file. Enter `bash Linux_and_Mac_OTSO_Compiler.sh` in the terminal and run.
  - Alternatively, you may instead run the `makefile` using the command `make` within the same terminal if you have make installed on your system. 

**Manual**
  - Open a terminal in the Library folder within OTSO. Enter `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC` into the terminal and run.
  - Next run the command `ar cr OTSOlib.a *.o` in the same terminal.
  - Copy all files that end with `.mod` and the `OTSOlib.a` file into the functions folder which can be found in the Parameters folder within the Tool directory.
  - Lastly, open a terminal within the functions folder and run the command `f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a`

**Without Anaconda**
1. If Python is not already on your system follow these steps
  - Enter `sudo apt-get install python` into your terminal to get the latest Python verison installed. (note this will install Python3)
  - Download the Python3 development tools by entering `sudo apt-get install python3-dev` into the command terminal.
  - Install the Numpy package needed to use f2py by entering `sudo apt-get install python3-numpy` into the same terminal
2. Download gfortran onto your linux system by entering `sudo apt-get install gfortran` into your command terminal.
3. You can then compile OTSO using the same methods outlined above in the manual install instructions, however in the last step you must enter `f2py3 -c -m MiddleMan MiddleMan.f95 OTSOlib.a` instead. If you wish to use the `Linux_and_Mac_OTSO_Compiler.sh` compiler you will need to edit the code slightly. Open the compiler file and change the `f2py` command to `f2py3` the compiler will now work for you if you run it.
  - You may need to grant your computer permission before you can execute the `Linux_and_Mac_OTSO_Compiler.sh` file. To do this have the terminal open in the directory containing the compiler file and enter `chmod 755`, the file should now be able to run on your system.
  
## Mac

Easiest way to install OTSO on Mac is outlined below. Links to online tutorials are provided as well as plain summaries for each step bellow.
Note OTSO was tested on the Monterey, Ventura, and Sonoma OS releases, as such the following instructions will be for installing OTSO on these versions of Mac OS. It is possible the use of older Mac OS releases could change the installation procedure. 

1. Install Anaconda on your Mac system. Follow these [instructions](https://docs.anaconda.com/anaconda/install/mac-os/) to download Anaconda on Mac. The Anaconda installer can be found [here](https://www.anaconda.com/products/distribution#macos).

2. Install Gfortran onto your Mac system using Anaconda. Follow these [instructions](https://anaconda.org/conda-forge/gfortran). A Summary is given bellow.
   - Open a terminal, enter in the command `conda install conda-forge::gfortran` and run.
   - Gfortran should now be installed on your OS.

3. OTSO must now be compiled in order to run. This can be done automatically via the provided bash file or manually.

**Automatic**
  - Open a terminal to the main OTSO directory (the folder containing user manual) and run the bash `Linux_and_Mac_OTSO_Compiler.sh` file. Enter `bash Linux_and_Mac_OTSO_Compiler.sh` in the terminal and run. 
  - Alternatively, you may instead run the `makefile` using the command `make` within the same terminal if you have make installed on your system. 

**Manual**
  - Open a terminal in the Library folder within OTSO. Enter `gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC` into the terminal and run.
  - Next run the command `ar cr OTSOlib.a *.o` in the same terminal.
  - Copy all files that end with `.mod` and the `OTSOlib.a` file into the functions folder which can be found in the Parameters folder within the Tool directory.
  - Lastly, open a terminal within the Tool folder and run the command `f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a`

## How to Use
If the compilation process has been completed without issue OTSO should now be ready to use. Within the `Tool/Parameters` folder there are python scripts that the user should edit to fit the simulations they wish to conduct (cone_params.py, trajectory_params.py, cutoff_params.py, and planet_params.py), please refer to the OTSO user manual for a more detailed decription. Once the input variables have been edited the user should run the python script in an Anaconda prompt / terminal within the Tool folder directory (e.g. `python Cone.py` will run the cone script used to compute asymptotic cones). Results from OTSO will be stored in a created folder called Results.

## Troubleshooting
- If there are errors in the compilation step for OTSO double check you have an up to date version of your fortran compiler, this may involve uninstalling your current version and re-instaling from scratch.
- Another issue you may encounter is a python 2 and python 3 conflict. If you are using python 3 for example f2py may need you to specify python 3 by typing `f2py3` during the compilation process, instead of just `f2py`.
- (As more issues are found I will endeavour to keep this troubleshooting section up to date with any fixes for potential issues users may encounter)

## Acknowledgments
**Publication Acknowledgments**

If you have used OTSO within your work, we kindly ask that you include it in the acknowledgement section of your publication. Two example acknowledgments are provided below depending on if you used the official release on Zenodo or GitHub repository:
1. "We acknowledge the use of the OTSO tool, the latest official release of which can be found at [https://doi.org/10.5281/zenodo.7515928](https://doi.org/10.5281/zenodo.7515928)".
2. "We acknowledge the use of the OTSO tool, the GitHub repository of which can be found at [https://github.com/NLarsen15/OTSO](https://github.com/NLarsen15/OTSO)".

**Community Acknowledgments**

We would like to acknowledge the use of the fantastic IRBEM library in the development of OTSO, which proved an invaluable asset and greatly sped up development. The latest release of the IRBEM library can be found at [https://doi.org/10.5281/zenodo.6867552](https://doi.org/10.5281/zenodo.6867552.). We would also like to thank N. Tsyganenko for the development of the external magnetic field models and their code which are used within OTSO.
A wider thanks goes to the space physics community who, through the use of OTSO, provide invaluable feedback, advice on improvements, and bug reporting. All discussions and advice have aided in the continual development and improvement of OTSO, allowing it to fulfil its aim of being a community-driven open-source tool. We express our gratitude to Dr. Christian Steigies of the University of Kiel for creating and generously sharing a custom makefile for OTSO for ease of installation that has been adapted and incorporated into this tool. 

## Publications Using OTSO
- Walter, M., Gnebner, C., Heber, B., Herbst, K., Krüger, H., Krüger, H. G., et al. (2024). Measurements of cosmic rays by a mini-neutron monitor at Neumayer III from 2014 to 2017. Space Weather, 22, e2023SW003596. https://doi.org/10.1029/2023SW003596
- Larsen, N., & Mishev, A. (2024). Relationship between NM data and radiation dose at aviation altitudes during GLE events. Space Weather, 22, e2024SW003885. https://doi.org/10.1029/2024SW003885
- Mishev, A., Koldobskiy, S., Larsen, N. et al. (2024). Spectra and Anisotropy of Solar Energetic Protons During GLE #65 on 28 October, 2003 and GLE #66 on 29 October, 2003. Sol Phys 299, 24. https://doi.org/10.1007/s11207-024-02269-z
- Larsen, N., & Mishev, A. (2023). Analysis of the ground level enhancement GLE 60 on 15 April 2001, and its space weather effects: Comparison with dosimetric measurements. Space Weather, 21, e2023SW003488. https://doi.org/10.1029/2023SW003488
- **Larsen, N., Mishev, A., & Usoskin, I. (2023). A new open-source geomagnetosphere propagation tool (OTSO) and its applications. Journal of Geophysical Research: Space Physics, 128, e2022JA031061. https://doi.org/10.1029/2022JA031061**
- Mishev, A., Binios, A., Turunen, E. et al. (2022). Measurements of natural radiation with an MDU Liulin type device at ground and in the atmosphere at various conditions in the Arctic region, Radiation Measurements, Volume 154, 106757, ISSN 1350-4487. https://doi.org/10.1016/j.radmeas.2022.106757
- Mishev, A., Kocharov, L., Koldobskiy, A. et al. (2022) High-Resolution Spectral and Anisotropy Characteristics of Solar Protons During the GLE N∘73 on 28 October 2021 Derived with Neutron-Monitor Data Analysis. Sol Phys 297, 88. https://doi.org/10.1007/s11207-022-02026-0

