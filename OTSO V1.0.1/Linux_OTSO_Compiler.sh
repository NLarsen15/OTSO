#!/bin/bash
cd Library
gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC
ar cr OTSOlib.a *.o
mv *.mod ../Tool
mv *.a ../Tool
rm *.o
cd ..
cd Tool
f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a
echo "OTSO Compilation Complete"
