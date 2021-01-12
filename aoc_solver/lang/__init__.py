import os, pkgutil

for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
    __import__(".".join(["aoc_solver", "lang", module]))
