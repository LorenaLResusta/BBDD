#!/usr/bin/env python3
"""Regenera la sección «Banco de ejercicios» de content.es/ud02-modelo-er/ud02-practicas.md
a partir de los datos de ud02_banco_1.py y ud02_banco_2.py.
Los SVG de solución se generan antes con gen_svgs.py y gen_leyenda.py."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ud02_banco_1, ud02_banco_2

MD = os.path.join(HERE, "..", "content.es", "ud02-modelo-er", "ud02-practicas.md")
ALL = sorted(ud02_banco_1.EJS + ud02_banco_2.EJS, key=lambda e: e["n"])

BLOQUES = [
    (1, 4, "Bloque 1 · Fundamentos", "●○○",
     "Entidades, atributos, identificadores, relaciones 1:N y N:M, atributos de relación y una primera relación reflexiva.",
     "Diagrama y supuestos"),
    (5, 12, "Bloque 2 · Intermedio", "●●○",
     "Relaciones 1:1, N:M reflexivas, entidades débiles, atributos compuestos, multivaluados y derivados, y varias relaciones entre las mismas entidades.",
     "Justificar decisiones y escribir restricciones textuales"),
    (13, 19, "Bloque 3 · Integración", "●●○ → ●●●",
     "Relaciones ternarias, dos relaciones entre las mismas entidades, listas de materiales, cardinalidades máximas concretas y primera especialización.",
     "Clasificar jerarquías, analizar ternarias y diccionario parcial"),
    (20, 25, "Bloque 4 · EER avanzado", "●●●",
     "Varias especializaciones en un mismo modelo, cadenas de entidades débiles, ternarias con atributos y casos de integración completos.",
     "Diccionario de datos, restricciones y tablas previstas"),
]


def nivel(n):
    return 1 if n <= 4 else (2 if n <= 15 else 3)


def anchor(h):
    h = h.lower()
    h = re.sub(r"[^\w\s-]", "", h, flags=re.UNICODE)
    return re.sub(r"\s", "-", h)


def quote(paras):
    return "\n>\n".join("> " + p for p in paras)


def render(e):
    n = e["n"]
    o = []
    o.append(f"### Ejercicio {n} · {e['titulo']}\n")
    o.append(f'{{{{< practica num="{n}" etiqueta="Ejercicio" tipo="Autónoma" duracion="{e["dur"]}" nivel="{nivel(n)}" '
             f'ra="{e["ra"]}" sgbd="draw.io o papel" entrega="{e["entrega"]}" >}}}}\n')
    o.append("#### Objetivo\n\n" + e["objetivo"] + "\n")
    o.append("#### Contexto\n\n" + e["contexto"] + "\n")
    o.append("#### Enunciado\n\n" + quote(e["enun"]) + "\n")
    o.append("#### Tareas\n\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(e["tareas"], 1)) + "\n")
    o.append("#### Comprobación\n\n" + "\n".join(f"- [ ] {c}" for c in e["comp"]) + "\n")
    if e.get("err"):
        o.append("#### Errores habituales\n\n> [!WARNING]\n" + "\n".join(f"> - {x}" for x in e["err"]) + "\n")
    if e.get("pista"):
        t, txt = e["pista"]
        o.append(f'{{{{% details title="{t}" %}}}}\n{txt}\n{{{{% /details %}}}}\n')
    o.append("#### Ampliación\n\n" + e["amp"] + "\n")
    m = e["model"]
    o.append('{{% details title="Solución: diagrama EER en notación de Chen (inténtalo antes de abrirla)" %}}\n')
    o.append(f'{{{{< figura src="ud02/ej{n:02d}.svg" alt="{m.desc}" caption="Ejercicio {n}: {m.title}" >}}}}\n')
    o.append("**Decisiones de diseño**\n\n" + "\n".join(f"- {d}" for d in e["dec"]) + "\n")
    o.append("**Supuestos semánticos**\n\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(e["sup"], 1)) + "\n")
    o.append("{{% /details %}}\n")
    return "\n".join(o)


def tabla_resumen():
    filas = ["| Práctica | Tipo | Nivel | CE principales |", "|---|---|---|---|"]
    return filas


def main():
    s = open(MD, encoding="utf-8").read()
    cut = s.index("## Banco de ejercicios")
    head = s[:cut]

    # tabla inicial: sustituye la fila genérica por una por bloque
    fila_vieja = "| [Banco de ejercicios](#banco-de-ejercicios) | Autónoma | ●○○ a ●●● | RA6 |"
    nuevas = []
    for a, b, titulo, niv, _, _ in BLOQUES:
        nuevas.append(f"| [Banco · {titulo.split('· ')[1]} (ejercicios {a}-{b})](#{anchor(titulo)}) | Autónoma | {niv} | RA6.a, RA6.d, RA6.e, RA6.h |")
    if fila_vieja in head:
        head = head.replace(fila_vieja, "\n".join(nuevas))
    elif "Banco · Fundamentos" in head:
        head = re.sub(r"\| \[Banco · Fundamentos.*?\n(?=\n)", "", head, flags=re.S)  # ya aplicado: se deja tal cual
    out = [head.rstrip() + "\n\n---\n"]

    out.append("""## Banco de ejercicios

Veinticinco ejercicios para practicar el diseño conceptual, **ordenados de menor a mayor dificultad** en cuatro bloques. Cada ejercicio tiene el mismo formato que las prácticas (objetivo, contexto, enunciado, tareas, comprobación, errores habituales y ampliación) y una **solución desplegable** dibujada en notación EER de Chen.

| Bloque | Ejercicios | Qué introduce | Además del diagrama se pide |
|---|---|---|---|""")
    for a, b, titulo, niv, intro, pide in BLOQUES:
        out.append(f"| {titulo.split('· ')[1]} {niv} | {a}-{b} | {intro} | {pide} |")
    out.append("""
{{< figura src="ud02/chen-eer-leyenda.svg" alt="Leyenda de la notación EER de Chen: entidad, entidad débil, relación, atributos, jerarquía y cardinalidad" caption="Leyenda de la notación EER de Chen usada en las soluciones" >}}

> [!IMPORTANT]
> **Convenio de cardinalidades.** El par (mín, máx) escrito **junto a una entidad** indica con cuántas instancias de **esa** entidad se relaciona una instancia de la otra. Es el mismo convenio de la [teoría](/ud02-modelo-er/ud02-teoria#71-equivalencia-entre-la-notación-de-chen-y-la-pata-de-gallo). En una relación ternaria, el par junto a una entidad cuenta cuántas instancias de ella corresponden a cada pareja de las otras dos.

> [!TIP]
> **Cómo trabajar un ejercicio.** Aplica el método de arriba, dibuja en papel o en draw.io, rellena la lista de comprobación y solo entonces despliega la solución. Si tu diagrama difiere, no significa que esté mal: compara los **supuestos**. Dos diseños distintos son válidos si responden igual a las reglas del enunciado.

> [!NOTE]
> Los atributos se escriben en `snake_case` sin acentos para que sirvan de nombres de columna en la [UD03](/ud03-modelo-relacional/ud03-teoria). Una línea doble marca la participación total de una entidad débil en su relación identificadora y de la superclase en una especialización total. El subrayado discontinuo también señala el atributo de una relación que permite repetir la misma combinación de entidades (por ejemplo, la fecha de una multa).
""")
    for a, b, titulo, niv, intro, pide in BLOQUES:
        out.append(f"\n---\n\n## {titulo}\n\n{intro}\n")
        for e in ALL:
            if a <= e["n"] <= b:
                out.append(render(e))
                out.append("\n---\n")
    text = "\n".join(out).rstrip().rstrip("-").rstrip() + "\n"
    open(MD, "w", encoding="utf-8").write(text)
    print("escrito", len(text.splitlines()), "líneas")


if __name__ == "__main__":
    main()
