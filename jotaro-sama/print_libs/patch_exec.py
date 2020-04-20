import lief
#binary  = lief.parse("/usr/bin/ls")
#library = lief.parse("/usr/lib/libc.so.6")

binary = lief.parse("a.out")

print(binary.imported_functions)
#print(library.exported_functions)

hooksfile = ""

for sym in binary.imported_symbols:
    assembly_name = sym.name
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC and "@" not in sym.name and sym.type != "__libc_startmain":
        newname = "logger_" + sym.name
        print(sym)
        hooksfile += """.globl %s
        %s:
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
        # return address
        mov 120(%%rsp), %%rdi
        call pltcov_log@PLT
        #nop

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

        jmp %s
        """ % (newname, newname, assembly_name+"@PLT")
        sym.name = newname

hooks_file = open("hooks.s", "w")
hooks_file.write(hooksfile)
hooks_file.close()

binary.write("hashme")