# -*- coding: utf-8 -*-
"""Reúne los ejercicios del banco de la UD02 en el orden final y los numera."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ud02_banco_1, ud02_banco_2, ud02_banco_3


def todos():
    base = {e["n"]: dict(e) for e in ud02_banco_1.EJS + ud02_banco_2.EJS}
    for e in ud02_banco_3.EJS:
        base[e["k"]] = dict(e)
    out = []
    for i, k in enumerate(ud02_banco_3.ORDEN, 1):
        e = dict(base[k])
        e["n"] = i
        e["orig"] = k
        out.append(e)
    return out


def bloques():
    """[(primero, último), ...] según TAM_BLOQUES."""
    res, a = [], 1
    for t in ud02_banco_3.TAM_BLOQUES:
        res.append((a, a + t - 1))
        a += t
    return res
