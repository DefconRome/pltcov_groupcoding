import lief
#binary  = lief.parse("/usr/bin/ls")
#library = lief.parse("/usr/lib/libc.so.6")

binary = lief.parse("a.out")

print(binary.imported_functions)
#print(library.exported_functions)

for sym in binary.imported_symbols:
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC:
        if sym.name == "log":
            print(sym)
            sym.name = "exp"
    
binary.write("hashme")
