#!/bin/bash

if [ -z $1 ] 
then
        echo "Error: missing ELF name."
else

        python3 generate_hook_library.py $1 > pltcov-rt.S 
        gcc pltcov-rt.S pltcov-rt.c ../AFLplusplus/afl-llvm-rt.o -o pltcov-rt.so -ldl -fPIC -shared

        LD_PRELOAD=./pltcov-rt.so ./$1.patched
        AFL_PRELOAD=./pltcov-rt.so ../AFLplusplus/afl-showmap -o - -- ./$1.patched
fi
