Run afl-showmap

```
AFL_PRELOAD=./hooks.so ../../AFLplusplus/afl-showmap -o - -- ./hashme
```

Run with env:

```
env LD_PRELOAD=./hooks.so ./hashme 4
```

Compile asm hooks, hook function with instrumented main and afl (ldl added for instrumenting main)

```
gcc hooks.s hook.c ../AFLplusplus/afl-llvm-rt.o -o hooks.so -fPIC -shared -ldl
```

Compile AFL

```
make && make -C llvm_mode
```

For intel syntax in asm, add this at the beginning:
```
.intel_syntax noprefix
```

How to not overflow in assembly:
```
https://github.com/AFLplusplus/AFLplusplus/blob/master/qemu_mode/patches/afl-qemu-common.h#L54
```