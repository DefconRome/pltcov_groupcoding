#!/bin/sh

make -C ../AFLplusplus
make -C ../AFLplusplus/llvm_mode

gcc test.c -o test

python3 create_hooks.py ./test > pltcov-hooks.S

chmod +x patched.elf

gcc -fPIC -shared pltcov-hooks.S pltcov-rt.c ../AFLplusplus/afl-llvm-rt.o -o libpltcov.so -ldl

echo 'a' | env AFL_PRELOAD=./libpltcov.so ../AFLplusplus/afl-showmap -o - -- ./patched.elf
