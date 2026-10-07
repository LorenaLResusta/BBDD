#!/usr/bin/env python3
"""Leyenda de la notación EER usada en clase (rombos blancos/negros, ID/E, T/P-D/S)."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from chen_eer import BG, FRAME, INK, AGG_S, CARD, tw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "ud02", "chen-eer-leyenda.svg")
W, H = 980, 600
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d" font-family="DejaVu Sans, Verdana, Arial, sans-serif">',
     '<title id="t">Leyenda de la notación EER usada en clase</title>',
     '<desc id="d">Entidad, entidad débil con ID o E, relaciones 1:1 (rombo blanco), 1:N (mitad blanco y mitad negro) y N:M (rombo negro), ternaria, atributos (clave, clave alternativa, discriminador, multivaluado, derivado, compuesto), generalización con T/P y D/S, y agregación.</desc>',
     f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{FRAME}"/>']


def text(x, y, s, size=12, color=INK, anchor="middle", bold=False, italic=False):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'
             f'{" font-weight=\"700\"" if bold else ""}{" font-style=\"italic\"" if italic else ""}>{s}</text>')


def cap(x, y, s):
    text(x, y, s, 11.5, "#334155")


def title(x, y, s):
    text(x, y, s, 13, "#1e3a8a", "start", True)


def line(x1, y1, x2, y2, w=1.4):
    o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}"/>')


def ent(cx, cy, name="ENTIDAD", w=104, h=38, weak=False):
    o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    if weak:
        o.append(f'<rect x="{cx - w / 2 + 4}" y="{cy - h / 2 + 4}" width="{w - 8}" height="{h - 8}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    text(cx, cy + 4.5, name, 12, bold=True)


def rombo(cx, cy, left_black, right_black, hw=34, hh=21):
    L, T, R, B = (cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)
    pts = lambda ps: " ".join(f"{x},{y}" for x, y in ps)
    o.append(f'<polygon points="{pts([L, T, B])}" fill="{INK if left_black else "#fff"}"/>')
    o.append(f'<polygon points="{pts([R, T, B])}" fill="{INK if right_black else "#fff"}"/>')
    o.append(f'<polygon points="{pts([L, T, R, B])}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    line(cx, cy - hh, cx, cy + hh, 1)


def card(x, y, s):
    w = tw(s) + 8
    o.append(f'<rect x="{x - w / 2}" y="{y - 9}" width="{w}" height="17" rx="3" fill="#fff"/>')
    text(x, y + 4.5, s, 12, CARD, bold=True)


def binaria(y, ca, cb, lb, rb, name, a="A", b="B", lt="1", rt="N"):
    ent(80, y, a, 70); ent(400, y, b, 70)
    line(115, y, 206, y); line(274, y, 365, y)
    rombo(240, y, lb, rb)
    text(240, y - 28, name, 12, bold=True, italic=True)
    text(198, y - 8, lt, 11); text(282, y - 8, rt, 11)
    card(150, y, ca); card(330, y, cb)


def att(cx, cy, name, w=None, k=False, kp=False, ak=False, mv=False, d=False):
    w = w or max(tw(name) + 22, 60)
    dash = ' stroke-dasharray="5 3"' if d else ""
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="14" fill="#fff" stroke="{INK}" stroke-width="1.4"{dash}/>')
    if mv:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - 4}" ry="10" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    text(cx, cy + 4, name, 12)
    if k or kp or ak:
        t = tw(name)
        da = ' stroke-dasharray="4 3"' if kp else (' stroke-dasharray="1.5 2.5"' if ak else "")
        o.append(f'<line x1="{cx - t / 2}" y1="{cy + 8}" x2="{cx + t / 2}" y2="{cy + 8}" stroke="{INK}" stroke-width="{1.8 if ak else 1.3}"{da}/>')


# ---------------------------------------------------------------- columna izquierda: relaciones
title(30, 34, "RELACIONES Y CARDINALIDADES")
binaria(80, "(0,1)", "(0,1)", False, False, "1:1", lt="1", rt="1")
cap(240, 118, "Rombo blanco: los dos máximos son 1")
binaria(170, "(1,1)", "(0,N)", False, True, "1:N")
cap(240, 208, "Mitad negra junto a la entidad con máximo N")
binaria(260, "(0,N)", "(1,N)", True, True, "N:M", lt="N")
cap(240, 298, "Rombo negro: los dos máximos son N")

# ternaria
ent(90, 380, "A", 60); ent(390, 380, "B", 60); ent(240, 470, "C", 60)
cx, cy, R = 240, 388, 40
top, bl, br = (cx, cy - R), (cx - 0.866 * R, cy + 0.5 * R), (cx + 0.866 * R, cy + 0.5 * R)
c = (cx, cy)
pts = lambda ps: " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)
o.append(f'<polygon points="{pts([c, top, bl])}" fill="{INK}"/>')   # cara izquierda → A (N)
o.append(f'<polygon points="{pts([c, top, br])}" fill="{INK}"/>')   # cara derecha → B (N)
o.append(f'<polygon points="{pts([c, bl, br])}" fill="#fff"/>')     # cara inferior → C (1)
o.append(f'<polygon points="{pts([top, bl, br])}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
for v in (top, bl, br):
    line(cx, cy, v[0], v[1], 1)
mA = ((top[0] + bl[0]) / 2, (top[1] + bl[1]) / 2); mB = ((top[0] + br[0]) / 2, (top[1] + br[1]) / 2); mC = (cx, cy + 0.5 * R)
line(120, 380, mA[0], mA[1]); line(360, 380, mB[0], mB[1]); line(240, 451, mC[0], mC[1])
text(240, 336, "ternaria N:M:1", 12, bold=True, italic=True)
card(155, 378, "(0,N)"); card(325, 378, "(0,N)"); card(266, 440, "(1,1)")
cap(240, 510, "Un sector por entidad, con el mismo criterio de color")

# dependencia
ent(80, 560, "FUERTE", 80); ent(400, 560, "DÉBIL", 80, weak=True)
line(120, 560, 206, 560); line(274, 560, 360, 560)
rombo(240, 560, False, True)
card(150, 560, "(1,1)"); card(328, 560, "(0,N)")
text(342, 540, "ID", 11, bold=True)
cap(240, 592, "Entidad débil: ID = identificación · E = existencia")

# ---------------------------------------------------------------- columna derecha: atributos, jerarquía, agregación
title(520, 34, "ATRIBUTOS")
att(580, 80, "atributo"); cap(580, 112, "Simple")
att(700, 80, "clave", k=True); cap(700, 112, "Identificador")
att(830, 80, "nif", ak=True); cap(830, 112, "Clave alternativa")
att(580, 150, "nº_línea", kp=True); cap(580, 182, "Discriminador")
att(700, 150, "teléfono", mv=True); cap(700, 182, "Multivaluado")
att(830, 150, "edad", d=True); cap(830, 182, "Derivado")
att(905, 225, "dirección")
att(860, 270, "calle", 58); att(950, 270, "cp", 46)
line(890, 238, 868, 256); line(920, 238, 942, 256)
cap(905, 300, "Compuesto")

title(520, 230, "GENERALIZACIÓN")
ent(640, 270, "SUPERCLASE", 116)
o.append(f'<polygon points="640,289 634,302 646,302" fill="{INK}"/>')
line(640, 302, 640, 330)
o.append(f'<circle cx="640" cy="330" r="3.2" fill="{INK}"/>')
line(640, 330, 575, 370); line(640, 330, 705, 370)
ent(575, 388, "SUB_1", 80); ent(705, 388, "SUB_2", 80)
text(668, 324, "T,D", 12, bold=True)
cap(640, 428, "T total / P parcial · D disjunta / S solapada")

title(520, 470, "AGREGACIÓN")
o.append(f'<rect x="520" y="486" width="300" height="74" fill="none" stroke="{AGG_S}" stroke-width="2"/>'
         f'<rect x="525" y="491" width="290" height="64" fill="none" stroke="{AGG_S}" stroke-width="1.2"/>')
ent(570, 523, "A", 50); ent(770, 523, "B", 50)
line(595, 523, 636, 523); line(704, 523, 745, 523)
rombo(670, 523, True, True)
line(820, 523, 864, 523)
ent(915, 523, "C", 60)
cap(700, 584, "La relación A–B se trata como una entidad")

o.append("</svg>")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(o))
print("ok", OUT)
