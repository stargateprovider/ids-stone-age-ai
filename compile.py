import py_compile, sys

folder = sys.argv[1]+"/" if len(sys.argv) > 1 else ""

for fname in ("players", "game", "genData",):
    py_compile.compile(fname+".py", folder+fname+".pyc", optimize=2)
