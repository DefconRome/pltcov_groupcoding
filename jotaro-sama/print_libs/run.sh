#/bin/sh
gcc hashme.c -lm
python3 patch_exec.py a.out
gcc hooks.s hook.c ../../AFLplusplus/afl-llvm-rt.o -o hooks.so -fPIC -shared -ldl
env LD_PRELOAD=./hooks.so ./hashme 4
AFL_PRELOAD=./hooks.so ../../AFLplusplus/afl-showmap -o - -- ./hashme
