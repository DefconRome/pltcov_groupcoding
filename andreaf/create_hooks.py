import lief
import sys

elf = lief.parse(sys.argv[1])

print(".text")
print()

for idx, sym in enumerate(elf.imported_symbols):
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC and "@" not in sym.name and sym.name != "__libc_start_main":
        print("""
.globl __pltcov_hook_%d
__pltcov_hook_%d:
  push %%rax
  push %%rbx
  push %%rcx
  push %%rdx
  push %%rsi
  push %%rdi
  push %%rbp
  push %%r8
  push %%r9
  push %%r10
  push %%r11
  push %%r12
  push %%r13
  push %%r14
  push %%r15
  movq 120(%%rsp), %%rdi
  call __pltcov_log@PLT
  pop %%r15
  pop %%r14
  pop %%r13
  pop %%r12
  pop %%r11
  pop %%r10
  pop %%r9
  pop %%r8
  pop %%rbp
  pop %%rdi
  pop %%rsi
  pop %%rdx
  pop %%rcx
  pop %%rbx
  pop %%rax
  jmp %s@PLT
""" % (idx, idx, sym.name))
        sym.name = "__pltcov_hook_%d" % idx

elf.write("patched.elf")
