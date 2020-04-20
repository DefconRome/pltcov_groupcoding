import lief
import sys

elf = lief.parse(sys.argv[1])

for idx, sym in enumerate(elf.imported_symbols):
    if sym.type == lief.ELF.SYMBOL_TYPES.FUNC:
        print(sym.name)

