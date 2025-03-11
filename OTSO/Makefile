#! /usr/bin/make
# Original Author: Christian Steigies (28/6/2024)
# Slightly modified by Nicholas Larsen to work easier within the existing OTSO framework (19/09/2024)

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

all: lib install clean

lib:
> @cd ./Library
> @gfortran -c *Module.f95 *Functions.f95 *.for *.f95 *.f -fPIC
> @ar cr OTSOlib.a *.o
> @mv *.mod ../Tool/Parameters/functions
> @mv *.a ../Tool/Parameters/functions

install: lib
> @cd ./Tool/Parameters/functions
> @set +e; f2py -c -m MiddleMan MiddleMan.f95 OTSOlib.a
> if [ $$? -eq 0 ]; then \
>     printf "%s\n" $(ASCII_ART); \
>     echo "OTSO compilation complete"; \
> else \
>     echo "OTSO compilation failed"; \
>     echo "Attempting again with different configuration"; \
>     @set +e; f2py -c --fcompiler=gnu95 --compiler=mingw32 -m MiddleMan MiddleMan.f95 OTSOlib.a
>     if [ $$? -eq 0 ]; then \
>     printf "%s\n" $(ASCII_ART); \
>     echo "OTSO compilation complete"; \
>     else \
>     echo "OTSO compilation failed"; \
>     fi; set -e
> fi; set -e

clean:
> @rm -f ./Library/*.o
> @rm -f ./Tool/Parameters/functions/*.mod
> @rm -f ./Tool/Parameters/functions/*.a

ASCII_ART := \
"                                                                       "\
"                                 @@@@@@                                " \
"                         @@@     @@   @@    @@@@                         " \
"               @@@@     @@  @@    @@@@@    @@  @@     @@@               " \
"              @@  @@    @@@@@@      @      @@@@@@    @@  @@             " \
"              @@@@@@      @@@      @@@      @@@      @@@@@@             " \
"                 @@@       @@     @@@@@    @@@       @@@                " \
"                  @@@@     @@@@  @@@ @@@  @@@@     @@@@                 " \
"                   @@@@@@ @@ @@@@@    @@@@@@ @  @@@@@@                  " \
"              @    @@  @@@@@   @@       @@   @@@@@ @@@    @             " \
"           @@@@@@  @@@       @     @@      @       @@  @@@@@@@         " \
"              @     @@  @@@@@@@@@@@@@@@@@@@@@@@@@  @@     @             " \
"                    @@@@@@@                   @@@@@@@                   " \
"            @@@@@@  @@      @@@@@@@@@@@@@@@@       @   @@@@@@          " \
"         @@@@@ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@       " \
"        @@@        @@@@@@@@        @@         @@@@@@@@        @@@      " \
"       @@      @@   @@       @@          @@        @@   @@     @@@     " \
"       @@    @@@@@@@            @@@   @@@           @@@@@@@@    @@     " \
"       @@@  @@@@@                                      @@@@@@  @@@     " \
"       @@@   @@@  @@     @@ @   @@     @    @ @      @@  @@@   @@@     " \
"        @@@@ @@@@@     @  @@@@@@@@     @@@@@@@@ @      @@@@@ @@@@       " \
"           @@@@@  @     @@@  @@          @@@ @@@@        @@@@@          " \
"           @@@@       @@    @@   @@@@@@@   @@    @@       @@@@          " \
"         @@@@           @  @@  @@       @  @@@  @           @@@@        " \
"         @@@       @  @  @@@@  @@@@@@@@@@@  @@ @     @       @@@        " \
"       @@@@ @    @@     @ @@@   @@@@@@@@@   @@  @     @  @    @@@@      " \
"         @     @@         @@     @@@@@@@     @@       @@@@  @  @        " \
"        @@@@  @@@ @   @  @@@        @        @@   @   @ @@   @@@@       " \
"       @@@@  @ @ @@  @@  @@      @@@@@@      @@@  @@  @  @ @ @@@@@      " \
"      @ @@   @ @@@  @@   @@    @@@@@@@@@@@   @@@   @@ @@@@ @  @@@ @     " \
"        @@ @   @@@@ @     @@@@@@         @@@@@@     @ @@@@  @@ @@       " \
"       @@@@@    @@@ @  @   @@@             @@@  @@  @ @@@    @@@@       " \
"       @@@@@    @@@@@@ @    @@@ @       @ @@@    @ @@@@@@    @@@@@      " \
"      @@@@@@    @@@@@@@@@     @@@@@@@@@@@@@ @   @@@@@@@@@    @@@@@@     " \
"    @@@@@@ @@   @@ @@@@@@@  @  @@@@@@@@@@@  @  @@@@@@@ @@   @@ @@@@@    " \
"       @@   @   @@  @@@  @@ @@  @@@@@@@@@  @@ @@ @@@@  @  @ @  @@@      " \
"      @@@  @  @   @  @ @ @@@@@@  @@@@@@@  @@@@@ @@@@  @   @  @ @@@      " \
"       @@@@@  @       @  @ @@@@@@ @@@@@@@@@@@@    @       @  @@@@@      " \
"       @@@@@@ @@           @@@@@@@@@@@@@@@@@@            @@ @@@@@@      " \
"        @@ @@@@@@ @@  @@    @@ @@@@@@@@@@@ @     @   @  @@ @@  @@       " \
"         @  @@@@@  @@  @@     @  @@@@@@@  @     @@  @@  @@@@@ @@        " \
"             @@@@@@ @@  @       @  @@@  @      @@  @@ @@@@@@            " \
"              @@@@@@@@@@@@@   @           @   @@@@@@@@@@@@              " \
"                  @@@@@@@@@@@  @        @@  @@@@@@@@@@@ @                " \
"                    @@@@ @@@@@@ @@     @@ @@@@@@@@@@@                    " \
"                       @@  @@@@@@@@@ @@@@@@@@@  @@                       " \
"                             @ @@@@@@@@@@@ @                            " \
"                                 @@@@@@@                                " \
"                                   @@@   " \
"                                         "

.PHONY: all library purge clean install

