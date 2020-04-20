import lief

binary  = lief.parse("main")
for sim in binary.imported_symbols:
	if sim.type == lief.ELF.SYMBOL_TYPES.FUNC:
		if sim.name == "puts":
			sim.name = "system"
binary.write("main.obj")

