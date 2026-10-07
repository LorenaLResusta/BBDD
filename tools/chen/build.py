#!/usr/bin/env python3
"""Genera assets/images/chen-2-NN.svg. Uso: python3 tools/chen/build.py [num ...]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from specs_ud02 import SPECS
OUT = os.path.join(HERE, "..", "..", "assets", "images")
nums = [int(a) for a in sys.argv[1:]] or sorted(SPECS)
for n in nums:
    d = SPECS[n]()
    d.render(os.path.join(OUT, "chen-2-leyenda.svg" if n == 0 else f"chen-2-{n:02d}.svg"))
    print("ok", n)
