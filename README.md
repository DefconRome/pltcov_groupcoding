# pltcov_groupcoding

Group coding repository of PltCov, a tool to instrument ELF binaries for fuzzing with ngram coverage of imported APIs

Slides: https://docs.google.com/presentation/d/1BqkUwnXPji32ZP2kCcv1Ra1br9hSPb4nQpEzLUdhVsE/edit?usp=sharing

## Requirements

+ git clone https://github.com/AFLplusplus/AFLplusplus
+ pip3 install lief
+ clang

## Useful links

+ https://lief.quarkslab.com/doc/stable/tutorials/04_elf_hooking.html
+ https://gist.github.com/apsun/1e144bf7639b22ff0097171fa0f8c6b1
+ https://en.wikipedia.org/wiki/X86_calling_conventions#System_V_AMD64_ABI
+ https://github.com/bitsecurerlab/afl-sensitive/blob/elf_and_lava/afl-n4/qemu_mode/patches/afl-qemu-cpu-inl.h#L230
+ https://github.com/AFLplusplus/AFLplusplus/blob/master/llvm_mode/afl-llvm-rt.o.c#L62

## DC11396 Group Coding HowTo

Group Coding is an experiment at DC11396. Each partecipant will code its own version of the tool (sharing tips with others in livestream) following an idea proposed by the group origanizers.

The workflow is the following:

+ Fork this repo.
+ Add a folder with your name or nickname. You are allowed only to create/delete/modify files in this directory.
+ Open immediately a pull request (with you name or nickname as title). The PR will be automatically updated with the code that you pushed in your fork.
+ At the end of the event, @andreafioraldi will merge *all* pull requests.
+ During the following the week, the best portions of code produced by all will be merged to create the first version of the tool (in another repo of this organization).

