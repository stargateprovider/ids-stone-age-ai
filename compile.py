import py_compile

for fname in ("players", "game", "genData",):
    py_compile.compile(fname+".py", fname+".pyc", optimize=2)
