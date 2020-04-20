import lief
import sys
import os

binary = lief.parse(sys.argv[1])

idx = 0
hooks = []

for sym in binary.imported_symbols:
	if sym.type == lief.ELF.SYMBOL_TYPES.FUNC:
		old_name  = sym.name
		if "@@" in old_name:
			continue
		if "__libc_start_main" in old_name:
			continue

		hook_name = "__hook_%d" % idx
		idx += 1

		hooks.append (
			(
				hook_name,
				old_name
			)
		)

		sym.name = hook_name
binary.write("patched.bin")

asm_file = open("hook.s", "w")
for hook_name, _ in hooks:
	asm_file.write(".globl %s\n" % hook_name)

asm_file.write("\n\n")
asm_file.write(".section .text\n\n")

for hook_name, fun_name in hooks:
	asm_file.write("%s:\n" % hook_name)
	asm_file.write("  push %rax\n")
	asm_file.write("  push %rbx\n")
	asm_file.write("  push %rcx\n")
	asm_file.write("  push %rdx\n")
	asm_file.write("  push %rbp\n")
	asm_file.write("  push %rdi\n")
	asm_file.write("  push %rsi\n")
	asm_file.write("  push %r8\n")
	asm_file.write("  push %r9\n")
	asm_file.write("  push %r10\n")
	asm_file.write("  push %r11\n")
	asm_file.write("  push %r12\n")
	asm_file.write("  push %r13\n")
	asm_file.write("  push %r14\n")
	asm_file.write("  push %r15\n")
	asm_file.write("  movq 120(%rsp), %rdi\n")
	asm_file.write("  call pltcov_log@plt\n")
	asm_file.write("  pop %r15\n")
	asm_file.write("  pop %r14\n")
	asm_file.write("  pop %r13\n")
	asm_file.write("  pop %r12\n")
	asm_file.write("  pop %r11\n")
	asm_file.write("  pop %r10\n")
	asm_file.write("  pop %r9\n")
	asm_file.write("  pop %r8\n")
	asm_file.write("  pop %rsi\n")
	asm_file.write("  pop %rdi\n")
	asm_file.write("  pop %rbp\n")
	asm_file.write("  pop %rdx\n")
	asm_file.write("  pop %rcx\n")
	asm_file.write("  pop %rbx\n")
	asm_file.write("  pop %rax\n")
	asm_file.write("  jmp %s@plt\n\n" % fun_name)
asm_file.close()

# os.system("gcc hook.s logger.c -o hook.so -fPIC -shared")

