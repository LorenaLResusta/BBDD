#!/usr/bin/env python3
"""Leyenda de la notación EER de Chen usada en la UD02."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from chen_eer import *

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "ud02", "chen-eer-leyenda.svg")
W, H = 940, 470
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d" font-family="DejaVu Sans, Verdana, Arial, sans-serif">',
     '<title id="t">Leyenda de la notación EER de Chen</title>',
     '<desc id="d">Símbolos para entidad, entidad débil, relación, relación identificadora, atributos, jerarquía de especialización y cardinalidad (mín, máx).</desc>',
     f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>']


def text(x, y, s, size=12, color=TXT, anchor="middle", bold=False):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"{" font-weight=\"700\"" if bold else ""}>{s}</text>')


def cap(x, y, s):
    text(x, y, s, 12, "#cbd5e1")


def ent(cx, cy, w=96, h=38, weak=False, name="ENTIDAD"):
    o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="{ENT_F}" stroke="{ENT_S}" stroke-width="2"/>')
    if weak:
        o.append(f'<rect x="{cx - w / 2 + 5}" y="{cy - h / 2 + 5}" width="{w - 10}" height="{h - 10}" fill="none" stroke="{ENT_S}" stroke-width="2"/>')
    text(cx, cy + 4, name, 12, TXT, bold=True)


def rel(cx, cy, w=100, h=48, ident=False, name="relación"):
    def pts(k):
        return f"{cx},{cy - h / 2 + k} {cx + w / 2 - k * w / h},{cy} {cx},{cy + h / 2 - k} {cx - w / 2 + k * w / h},{cy}"
    o.append(f'<polygon points="{pts(0)}" fill="{REL_F}" stroke="{REL_S}" stroke-width="2"/>')
    if ident:
        o.append(f'<polygon points="{pts(7)}" fill="none" stroke="{REL_S}" stroke-width="2"/>')
    text(cx, cy + 4, name, 11, TXT, bold=True)


def att(cx, cy, name="atributo", w=96, h=30, dash=False, mv=False, k=False, kp=False):
    d = ' stroke-dasharray="5 3"' if dash else ""
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="{ATT_F}" stroke="{ATT_S}" stroke-width="2"{d}/>')
    if mv:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - 5}" ry="{h / 2 - 5}" fill="none" stroke="{ATT_S}" stroke-width="1.6"/>')
    text(cx, cy + 4, name, 12)
    if k or kp:
        tw_ = tw(name)
        da = ' stroke-dasharray="4 3"' if kp else ""
        o.append(f'<line x1="{cx - tw_ / 2}" y1="{cy + 8}" x2="{cx + tw_ / 2}" y2="{cy + 8}" stroke="{TXT}" stroke-width="1.4"{da}/>')


def line(x1, y1, x2, y2):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LINE}" stroke-width="1.6"/>')


# fila 1
text(40, 36, "ELEMENTOS", 13, "#7dd3fc", "start", True)
ent(110, 82); cap(110, 120, "Entidad")
ent(290, 82, weak=True, name="DÉBIL"); cap(290, 120, "Entidad débil")
rel(480, 82); cap(480, 120, "Relación")
rel(680, 82, ident=True, name="identif."); cap(680, 120, "Relación identificadora")
# fila 2
att(110, 180); cap(110, 214, "Atributo")
att(290, 180, "clave", k=True); cap(290, 214, "Identificador (clave)")
att(480, 180, "discriminador", w=116, kp=True); cap(480, 214, "Discriminador (débil o repetible)")
att(690, 180, "teléfono", mv=True); cap(690, 214, "Multivaluado")
att(850, 180, "edad", dash=True); cap(850, 214, "Derivado")
# fila 3: compuesto + jerarquía + cardinalidad
att(110, 290, "dirección"); att(50, 350, "calle", w=64); att(168, 350, "ciudad", w=70)
line(95, 305, 62, 336); line(125, 305, 158, 336)
cap(110, 392, "Compuesto")
# jerarquía
ent(350, 262, name="SUPERCLASE", w=110)
o.append(f'<g stroke="{LINE}" stroke-width="1.6"><line x1="344" y1="281" x2="344" y2="316"/><line x1="356" y1="281" x2="356" y2="316"/></g>')
o.append(f'<circle cx="350" cy="332" r="16" fill="{ISA_F}" stroke="{ISA_S}" stroke-width="2"/>')
text(350, 337, "d", 14, TXT, bold=True)
line(338, 342, 292, 372); line(362, 342, 408, 372)
ent(280, 392, name="SUBCLASE", w=100); ent(420, 392, name="SUBCLASE", w=100)
import math
for (px, py, qx, qy) in ((338, 342, 292, 372), (362, 342, 408, 372)):
    L = math.hypot(qx - px, qy - py); ux, uy = (qx - px) / L, (qy - py) / L
    cx, cy = qx - ux * 14, qy - uy * 14
    a = math.degrees(math.atan2(uy, ux))
    o.append(f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({a:.1f})"><rect x="-6" y="-8" width="9" height="16" fill="{BG}"/><path d="M3 -7 A7 7 0 0 0 3 7" fill="none" stroke="{ISA_S}" stroke-width="2"/></g>')
cap(350, 436, "Especialización: d disyunta · o solapada")
cap(350, 452, "Doble línea = participación total")
# cardinalidad
ent(600, 300, name="CLIENTE", w=100)
rel(740, 300, name="realiza")
ent(880, 300, name="PEDIDO", w=100)
line(650, 300, 690, 300); line(790, 300, 830, 300)
text(668, 292, "(1,1)", 12, CARD, bold=True)
text(812, 292, "(0,N)", 12, CARD, bold=True)
text(740, 346, "Cardinalidad (mín, máx)", 12, "#cbd5e1")
text(740, 368, "(0,N) junto a PEDIDO: un cliente tiene de 0 a N pedidos", 11, CARD)
text(740, 386, "(1,1) junto a CLIENTE: un pedido es de exactamente 1 cliente", 11, CARD)
text(740, 420, "El par junto a una entidad cuenta ESA entidad", 11, "#cbd5e1")
text(740, 436, "por cada instancia de la otra.", 11, "#cbd5e1")
o.append("</svg>")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(o))
print(OUT)
