#/bin/sh
gcc -lm hashme.c
python3 patch_exec.py
gcc hooks.s hook.c ../AFLplusplus/afl-llvm-rt.o -o hooks.so -fPIC -shared -ldl
env LD_PRELOAD=./hooks.so ./hashme 4
AFL_PRELOAD=./hooks.so ../../AFLplusplus/afl-showmap -o - -- ./hashme
