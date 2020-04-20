all: compile

compile:
	python3 hook.py ${INPUT_EXE}
	gcc hook.s pltcov.c ../AFLplusplus/afl-llvm-rt.o -o hook.so -fPIC -shared -ldl 
	chmod +x ./patched.bin

run: compile
	LD_PRELOAD=./hook.so ./patched.bin

showmap: compile
	AFL_PRELOAD=./hook.so ../AFLplusplus/afl-showmap -o - -- ./patched.bin

clean:
	rm -f hook.so patched.bin 
