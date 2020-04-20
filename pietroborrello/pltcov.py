#!/usr/bin/env python3

import sys
import os
import stat
import lief
from subprocess import check_call
binary  = lief.parse(sys.argv[1])

hook_basename = "pltcov__{func}__hook"

stub_func = '''
.globl {stub_name}
{stub_name}:
    push rax;
    push rbx;
    push rcx;
    push rdx;
    push rdi;
    push rsi;
    push rbp;
    push r8;
    push r9;
    push r10;
    push r11;
    push r12;
    push r13;
    push r14;
    push r15;
    mov rdi, qword ptr [rsp + 120]
    call pltcov__instrument@PLT;
    pop r15;
    pop r14;
    pop r13;
    pop r12;
    pop r11;
    pop r10;
    pop r9;
    pop r8;
    pop rbp;
    pop rsi;
    pop rdi;
    pop rdx;
    pop rcx;
    pop rbx;
    pop rax;
    jmp offset {original_func}@PLT;
'''

pltcov_library_source = '''
.intel_syntax noprefix

'''

for sym in binary.imported_symbols:
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC and "@" not in sym.name and sym.name[:2] != '__':
        new_name = hook_basename.format(func="puts")
        pltcov_library_source += stub_func.format(stub_name=new_name, original_func=sym.name)
        sym.name = new_name

with open("pltcov.s", 'w') as f:
    f.write(pltcov_library_source)

check_call("gcc -Os -fPIC -shared pltcov.s hook.c ../AFLplusplus/afl-llvm-rt.o -ldl -o libpltcov.so", shell=True)

binary.write(sys.argv[1] + '.patched')
os.chmod(sys.argv[1] + '.patched', stat.S_IWRITE | stat.S_IEXEC | stat.S_IREAD)