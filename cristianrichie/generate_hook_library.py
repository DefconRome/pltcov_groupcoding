#!/usr/bin/env python3 

import lief
from sys import argv
import subprocess


binary = lief.parse(argv[1])

for i, sym in enumerate(binary.imported_symbols):
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC:

        hook_name = "__pltcov_hook_" + str(i)

        code = """
.globl %s

%s:
    pushq %%rax
    pushq %%rbx
    pushq %%rcx
    pushq %%rdx
    pushq %%rsi
    pushq %%rdi
    pushq %%rbp
    pushq %%r8
    pushq %%r9
    pushq %%r10
    pushq %%r11
    pushq %%r12
    pushq %%r13
    pushq %%r14
    pushq %%r15

    movq 120(%%rsp), %%rdi
    call __pltcov_logger

    popq  %%r15
    popq  %%r14
    popq  %%r13
    popq  %%r12
    popq  %%r11
    popq  %%r10
    popq  %%r9
    popq  %%r8
    popq  %%rbp
    popq  %%rdi
    popq  %%rsi
    popq  %%rdx
    popq  %%rcx
    popq  %%rbx
    popq  %%rax

    jmp   %s@PLT
    """ % (hook_name, hook_name, sym.name)

        print(code)

        sym.name = hook_name

binary.write(argv[1] + ".patched")

