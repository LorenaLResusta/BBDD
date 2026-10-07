#!/usr/bin/env python3
"""Diagramas EER de las tareas de transformación de la UD03 (assets/images/ud03/).
Uso: python3 tools/ud03_tareas.py"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chen_eer import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "images", "ud03")

MODELOS = {}

# Tarea: casas rurales, variante con personas que viven y poseen casas
MODELOS["tarea-rurales-b"] = Model(
    "Casas rurales: variante con residentes y propietarios",
    "PROVINCIA tiene CIUDAD (débil, ID). CASA depende en existencia de CIUDAD (E). PERSONA vive en CASA (N:1). PERSONA posee CASA (N:M con fecha de compra).",
    [E("PROVINCIA", [K("nombre")]),
     E("CIUDAD", [KP("nombre")], weak=True),
     E("CASA", [K("id_casa"), A("precio"), A("valoración")], weak=True),
     E("PERSONA", [K("id_persona"), A("nombre")])],
    [R("situada en", [("PROVINCIA", "(1,1)", None), ("CIUDAD", "(1,N)", None)], ident=True),
     R("localizada en", [("CIUDAD", "(1,1)", None), ("CASA", "(0,N)", None)], exist="CASA"),
     R("vive en", [("CASA", "(0,1)", None), ("PERSONA", "(0,N)", None)]),
     R("posee", [("CASA", "(0,N)", None), ("PERSONA", "(1,N)", None)], [A("fecha_compra")])],
    pos={"PROVINCIA": (6.2, 0), "situada en": (4.2, 0), "CIUDAD": (2.3, 0), "localizada en": (2.3, 1.7),
         "CASA": (2.3, 3.4), "vive en": (4.2, 2.7), "posee": (4.2, 4.2), "PERSONA": (6.2, 3.4)})

# Tarea: esquema abstracto 1 (agregación C-R4-B, ternaria R2, jerarquía P,D)
MODELOS["tarea-abstracto-1"] = Model(
    "Esquema abstracto 1",
    "A es débil de C (R1, ID) y reflexiva R3. F y G especializan A (P,D). R2 es ternaria A-D-E (1:1:N). La agregación de C-R4-B se relaciona con D (R5).",
    [E("A", [KP("a0"), A("a1")], weak=True),
     E("F", [A("f0")]), E("G", []),
     E("C", [K("c0"), A("c1")]), E("B", [K("b0"), A("b1")]),
     E("D", [K("d0"), A("d1")]), E("E", [K("e0"), A("e1")])],
    [R("R1", [("A", "N", None), ("C", "1", None)], ident="A"),
     R("R3", [("A", "1", None), ("A", "N", None)]),
     R("R4", [("C", "N", None), ("B", "1", None)]),
     R("R5", [("AGR", "N", None), ("D", "1", None)]),
     R("R2", [("A", "1", None), ("D", "1", None), ("E", "N", None)])],
    [ISA("A", ["F", "G"], "d", False)],
    aggs=[AGG("AGR", ["C", "R4", "B"])],
    pos={"A": (0, 0), "R3": (-1.7, 0), "R1": (2.0, -0.6), "C": (4.0, -0.6), "R4": (5.6, -0.6), "B": (7.2, -0.6),
         "ISA:A": (0, 1.3), "F": (-1.0, 2.4), "G": (1.0, 2.4), "R2": (3.2, 1.4), "E": (3.2, 2.9),
         "R5": (5.6, 1.4), "D": (5.6, 2.9)})

# Tarea: esquema abstracto 2 (agregación C-R4-D, ternaria R6, 1:1 con atributo m)
MODELOS["tarea-abstracto-2"] = Model(
    "Esquema abstracto 2",
    "A es débil de C (R1, ID). F y E especializan A (P,D). R2 reflexiva 1:N sobre F. R3 N:M F-E. La agregación C-R4-D (N:M, D depende en existencia de R4) se relaciona 1:1 con A (R5, atributo m, E). R6 ternaria C-D-B (1:N:N).",
    [E("A", [KP("a0"), A("a1")], weak=True),
     E("F", [A("f0")]), E("E", [A("e0"), A("e1")]),
     E("C", [K("c0"), A("c1")]), E("D", [K("d0"), A("d1")], weak=True),
     E("B", [K("b0"), A("b1")])],
    [R("R1", [("A", "N", None), ("C", "1", None)], ident="A"),
     R("R5", [("A", "1", None), ("AGR", "1", None)], [A("m")], exist="AGR"),
     R("R4", [("C", "N", None), ("D", "N", None)], exist="D"),
     R("R6", [("C", "1", None), ("D", "N", None), ("B", "N", None)]),
     R("R3", [("F", "N", None), ("E", "N", None)]),
     R("R2", [("F", "1", None), ("F", "N", None)])],
    [ISA("A", ["F", "E"], "d", False)],
    aggs=[AGG("AGR", ["C", "R4", "D"])],
    pos={"A": (0, 0), "R1": (2.4, -1.4), "C": (4.6, -1.4), "R4": (4.6, 0), "D": (4.6, 1.4),
         "R5": (2.4, 0.1), "R6": (6.6, 0), "B": (8.4, 0),
         "ISA:A": (0, 1.3), "F": (-0.9, 2.5), "E": (1.6, 2.5), "R3": (0.35, 3.3), "R2": (-2.4, 2.5)})

# Tarea: esquema abstracto 3 (agregación C-R4-D, ternaria reflexiva R1, jerarquía T,S)
MODELOS["tarea-abstracto-3"] = Model(
    "Esquema abstracto 3",
    "G es débil de B (R5, ID). R6 1:1 G-H. La agregación C-R4-D (C N, D 1) se relaciona con G (R3, atributo m, E) y N:M con F (R2). F y E especializan A (T,S). R1 es una ternaria F-F-E (N:1:1).",
    [E("B", [K("b0"), A("b1")]),
     E("G", [KP("g0"), A("g1")], weak=True),
     E("H", [K("h0"), A("h1")]),
     E("C", [K("c0"), A("c1")]), E("D", [K("d0"), A("d1")]),
     E("A", [K("a0"), A("a1")]), E("F", [A("f0")]), E("E", [A("e0"), A("e1")])],
    [R("R5", [("B", "1", None), ("G", "N", None)], ident="G"),
     R("R6", [("G", "1", None), ("H", "1", None)]),
     R("R3", [("G", "1", None), ("AGR", "N", None)], [A("m")], exist="AGR"),
     R("R4", [("C", "N", None), ("D", "1", None)]),
     R("R2", [("AGR", "N", None), ("F", "N", None)]),
     R("R1", [("F", "N", None), ("F", "1", None), ("E", "1", None)])],
    [ISA("A", ["F", "E"], "o", True)],
    aggs=[AGG("AGR", ["C", "R4", "D"])],
    pos={"B": (0, -1.6), "R5": (0, -0.5), "G": (0, 0.6), "R6": (0.8, 1.8), "H": (1.6, 3.0),
         "R3": (1.9, 0.6), "C": (3.8, -0.4), "R4": (3.8, 0.6), "D": (3.8, 1.6),
         "R2": (5.9, 0.6), "F": (7.6, 0.6), "A": (8.4, -1.4), "ISA:A": (8.4, -0.4), "E": (10.0, 0.6), "R1": (8.8, 2.0)})


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for k, m in MODELOS.items():
        if only and k not in only:
            continue
        print(k, draw(m, os.path.join(OUT, k + ".svg"), 1))
