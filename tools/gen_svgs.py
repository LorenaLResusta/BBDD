#!/usr/bin/env python3
"""Genera los SVG de solución del banco de ejercicios de la UD02."""
import sys, os
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import ud02_banco_1, ud02_banco_2
from chen_eer import draw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "ud02")
ALL = ud02_banco_1.EJS + ud02_banco_2.EJS


def job(e):
    nodes = len(e["model"].ents) + len(e["model"].rels)
    tries = 30 if nodes < 12 else 45
    p, sz = draw(e["model"], os.path.join(OUT, f"ej{e['n']:02d}.svg"), tries)
    return e["n"], round(p), [round(x) for x in sz]


if __name__ == "__main__":
    only = {int(x) for x in sys.argv[1:]}
    todo = [e for e in ALL if not only or e["n"] in only]
    with Pool(6) as pool:
        for r in pool.imap_unordered(job, todo):
            print(r, flush=True)
