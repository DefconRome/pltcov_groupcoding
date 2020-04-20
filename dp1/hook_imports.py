#!/usr/bin/env python3

import subprocess
import lief
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <elf file>")
    quit()

binary = lief.ELF.parse(sys.argv[1])

stub = """
.globl %s
%s:
    push %%rax
    push %%rbx
    push %%rcx
    push %%rdx
    push %%rbp
    push %%rsi
    push %%rdi
    push %%r8
    push %%r9
    push %%r10
    push %%r11
    push %%r12
    push %%r13
    push %%r14
    push %%r15
    
    # pass our return address to the instrumentation function
    movq 120(%%rsp), %%rdi
    call pltcov_instrument@PLT

    pop %%r15
    pop %%r14
    pop %%r13
    pop %%r12
    pop %%r11
    pop %%r10
    pop %%r9
    pop %%r8
    pop %%rdi
    pop %%rsi
    pop %%rbp
    pop %%rdx
    pop %%rcx
    pop %%rbx
    pop %%rax

    jmp %s@PLT
"""

sim_count = 0
output_asm = ""

def patch(sim):
    global sim_count, output_asm

    old_sim = sim.name
    new_sim = f'__pltcov_hook{str(sim_count)}'
    output_asm += stub % (new_sim, new_sim, old_sim)
    sim.name = new_sim

    sim_count += 1


hook_blacklist = [
    "__libc_start_main"
]

for sim in binary.imported_symbols:
    if sim.type == lief.ELF.SYMBOL_TYPES.FUNC:
        if '@' not in sim.name and sim.name not in hook_blacklist:
            patch(sim)



binary.write(f'{sys.argv[1]}_hooked')
subprocess.run(['chmod', '+x', f'{sys.argv[1]}_hooked'])

with open('hooks.s','w') as fout:
    fout.write(output_asm)

subprocess.run('gcc hooks.s pltcov.c ../AFLplusplus/afl-llvm-rt.o -o hook.so -fPIC -shared -ldl', shell=True)
