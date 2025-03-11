#!/bin/bash
cd Library
gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC
ar cr OTSOlib.a *.o
mv *.mod ../Tool/Parameters/functions
mv *.a ../Tool/Parameters/functions
rm *.o
cd ..
cd Tool/Parameters/functions
f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a
if [ $? -eq 0 ]; then
    echo
    echo                                 @@@@@@                                
    echo                         @@@     @@   @@    @@@@                         
    echo               @@@@     @@  @@    @@@@@    @@  @@     @@@               
    echo              @@  @@    @@@@@@      @      @@@@@@    @@  @@             
    echo              @@@@@@      @@@      @@@      @@@      @@@@@@             
    echo                 @@@       @@     @@@@@    @@@       @@@                
    echo                  @@@@     @@@@  @@@ @@@  @@@@     @@@@                 
    echo                   @@@@@@ @@ @@@@@    @@@@@@ @  @@@@@@                  
    echo              @    @@  @@@@@   @@       @@   @@@@@ @@@    @             
    echo           @@@@@@  @@@       @     @@      @       @@  @@@@@@@         
    echo              @     @@  @@@@@@@@@@@@@@@@@@@@@@@@@  @@     @             
    echo                    @@@@@@@                   @@@@@@@                   
    echo            @@@@@@  @@      @@@@@@@@@@@@@@@@       @   @@@@@@          
    echo         @@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@       
    echo        @@@        @@@@@@@@        @@         @@@@@@@@        @@@      
    echo       @@      @@   @@       @@          @@        @@   @@     @@@     
    echo       @@    @@@@@@@            @@@   @@@           @@@@@@@@    @@     
    echo       @@@  @@@@@                                      @@@@@@  @@@     
    echo       @@@   @@@  @@     @@ @   @@     @    @ @      @@  @@@   @@@     
    echo        @@@@ @@@@@     @  @@@@@@@@ @      @@@@@ @@@@       
    echo           @@@@@  @     @@@  @@          @@@ @@@@        @@@@@          
    echo           @@@@       @@    @@   @@@@@@@   @@    @@       @@@@          
    echo         @@@@           @  @@  @@       @  @@@  @           @@@@        
    echo         @@@       @  @  @@@@  @@@@@@@@@@@  @@ @     @       @@@        
    echo       @@@@ @    @@     @ @@@   @@@@@@@@@   @@  @     @  @    @@@@      
    echo         @     @@         @@     @@@@@@@     @@       @@@@  @  @        
    echo        @@@@  @@@ @   @  @@@        @        @@   @   @ @@   @@@@       
    echo       @@@@  @ @ @@  @@  @@      @@@@@@      @@@  @@  @  @ @ @@@@@      
    echo      @ @@   @ @@@  @@   @@    @@@@@@@@@@@   @@@   @@ @@@@ @  @@@ @     
    echo        @@ @   @@@@ @     @@@@@@         @@@@@@     @ @@@@  @@ @@       
    echo       @@@@@    @@@ @  @   @@@             @@@  @@  @ @@@    @@@@       
    echo       @@@@@    @@@@@@ @    @@@ @       @ @@@    @ @@@@@@    @@@@@      
    echo      @@@@@@    @@@@@@@@@     @@@@@@@@@@@@@ @   @@@@@@@@@    @@@@@@     
    echo    @@@@@@ @@   @@ @@@@@@@  @  @@@@@@@@@@@  @  @@@@@@@ @@   @@ @@@@@    
    echo       @@   @   @@  @@@  @@ @@  @@@@@@@@@  @@ @@ @@@@  @  @ @  @@@      
    echo      @@@  @  @   @  @ @ @@@@@@  @@@@@@@  @@@@@ @@@@  @   @  @ @@@      
    echo       @@@@@  @       @  @ @@@@@@ @@@@@@@@@@@@    @       @  @@@@@      
    echo       @@@@@@ @@           @@@@@@@@@@@@@@@@@@            @@ @@@@@@      
    echo        @@ @@@@@@ @@  @@    @@ @@@@@@@@@@@ @     @   @  @@ @@  @@       
    echo         @  @@@@@  @@  @@     @  @@@@@@@  @     @@  @@  @@@@@ @@        
    echo             @@@@@@ @@  @       @  @@@  @      @@  @@ @@@@@@            
    echo              @@@@@@@@@@@@@   @           @   @@@@@@@@@@@@              
    echo                  @@@@@@@@@@@  @        @@  @@@@@@@@@@@ @                
    echo                    @@@@ @@@@@@ @@     @@ @@@@@@@@@@@                    
    echo                       @@  @@@@@@@@@ @@@@@@@@@  @@                       
    echo                             @ @@@@@@@@@@@ @                             
    echo                                 @@@@@@@                                
    echo                                   @@@ 
    echo 
    echo "OTSO compilation complete"
else
    echo "OTSO compilation failed"
fi
rm *.mod
rm *.a
