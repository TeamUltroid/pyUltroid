import sys

run_as_module = False

if sys.argv[0].endswith("pyUltroid/__main__.py"):
    run_as_module = True
    from .init import *
