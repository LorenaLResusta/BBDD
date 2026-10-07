#!/usr/bin/env python3
"""Generador de diagramas EER en notación de Chen (SVG), con maquetación propia.

No necesita Graphviz: entidades y relaciones se colocan en una rejilla (col, fila)
y los atributos se reparten automáticamente alrededor de su propietario.

Convenio (el mismo que la teoría de la UD02):
  * (mín,máx) junto a una entidad = con cuántas instancias de ESA entidad se
    relaciona una instancia de la entidad del otro extremo.
  * En relaciones ternarias solo se indica la cardinalidad máxima (N, M, P).

Atributos (cadenas):  "*dni" identificador · "~num" clave parcial · "+tel" multivaluado
  "/edad" derivado · "dir{calle,cp}" compuesto · "nombre" simple
"""
import math
import re
from html import escape
from PIL import ImageFont

BG = "#0f172a"
C_ENT = ("#075985", "#38bdf8")
C_REL = ("#047857", "#34d399")
C_ATT = ("#312e81", "#a5b4fc")
C_SUB = ("#0f172a", "#fbbf24")
C_LINE = "#94a3b8"
C_CARD = "#fbbf24"
C_ROLE = "#cbd5e1"
TXT = "#f8fafc"
FAM = "Arial, Helvetica, sans-serif"

_F = {}
def tw(text, size, bold=False):
    key = (size, bold)
    if key not in _F:
        _F[key] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""), size * 4)
    return _F[key].getlength(text) / 4 * 0.93


class Node:
    def __init__(self, kind, name, label, x=0, y=0):
        self.kind, self.name, self.label = kind, name, label
        self.x, self.y = x, y
        self.w = self.h = 0
        self.attrs = []          # (spec) pendientes
        self.weak = False
        self.ident = False
        self.lines = [label]
        self.opts = {}

    # geometría de borde: punto de salida desde el centro hacia (tx, ty)
    def border(self, tx, ty):
        dx, dy = tx - self.x, ty - self.y
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        a, b = self.w / 2, self.h / 2
        if self.kind in ("ent", "box"):
            s = min(a / abs(ux) if ux else 1e9, b / abs(uy) if uy else 1e9)
        elif self.kind == "rel":
            s = 1 / (abs(ux) / a + abs(uy) / b)
        else:  # elipse / círculo
            s = 1 / math.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return self.x + ux * s, self.y + uy * s

    def rect(self, pad=0):
        return (self.x - self.w / 2 - pad, self.y - self.h / 2 - pad, self.x + self.w / 2 + pad, self.y + self.h / 2 + pad)


def _split(label, maxc):
    if len(label) <= maxc or " " not in label:
        return [label]
    words, lines, cur = label.split(" "), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


class Diagram:
    COLW, ROWH = 250, 190

    def __init__(self, name, title="", colw=None, rowh=None):
        self.name, self.title = name, title
        if colw: self.COLW = colw
        if rowh: self.ROWH = rowh
        self.nodes = {}
        self.order = []
        self.edges = []      # dict
        self.attr_nodes = []
        self.aggs = []
        self.extra_text = []
        self._n = 0

    # ------------------------------------------------------------ construcción
    def _pos(self, pos):
        return (60 + pos[0] * self.COLW, 60 + pos[1] * self.ROWH)

    def entity(self, name, attrs=(), weak=False, pos=(0, 0)):
        n = Node("ent", name, name, *self._pos(pos))
        n.weak = weak
        n.w = max(96, tw(name, 14, True) + 30) + (8 if weak else 0)
        n.h = 40 + (8 if weak else 0)
        n.attrs = list(attrs)
        self.nodes[name] = n; self.order.append(name)
        return n

    def relation(self, name, ends, attrs=(), identifying=False, pos=(0, 0), rid=None):
        rid = rid or name
        n = Node("rel", rid, name, *self._pos(pos))
        n.ident = identifying
        n.lines = _split(name, 13)
        w = max(tw(l, 11, True) for l in n.lines)
        n.w = w * 1.45 + 34 + (10 if identifying else 0)
        n.h = 54 + 14 * (len(n.lines) - 1) + (10 if identifying else 0)
        n.attrs = list(attrs)
        self.nodes[rid] = n; self.order.append(rid)
        for e in ends:
            ent, card = e[0], e[1]
            role = e[2] if len(e) > 2 else None
            self.edges.append(dict(a=rid, b=ent, card=card, role=role, kind="rel"))
        return n

    def specialization(self, sup, subs, kind="d", total=False, pos=(0, 0), sid=None):
        sid = sid or f"ISA{len(self.nodes)}"
        n = Node("sub", sid, kind, *self._pos(pos))
        n.w = n.h = 30
        self.nodes[sid] = n; self.order.append(sid)
        self.edges.append(dict(a=sup, b=sid, kind="sup", total=total))
        for s in subs:
            self.edges.append(dict(a=sid, b=s, kind="sub"))
        return n

    def aggregate(self, name, members, label=""):
        self.aggs.append(dict(name=name, members=members, label=label))
        box = Node("box", name, label)
        self.nodes[name] = box
        return box

    # ------------------------------------------------------------ atributos
    def _make_attr(self, spec, small=False):
        m = re.match(r"^([*~+/])?(.*)$", spec.strip())
        mark, rest = m.group(1), m.group(2)
        kids = []
        mc = re.match(r"^([^{]+)\{(.*)\}$", rest)
        if mc:
            rest, kids = mc.group(1), [c for c in mc.group(2).split(",") if c]
        fs = 10 if small else 11
        a = Node("att", rest, rest)
        a.w = tw(rest, fs) + 22 + (8 if mark == "+" else 0)
        a.h = 26 + (6 if mark == "+" else 0)
        a.opts = dict(mark=mark, fs=fs, kids=kids)
        return a

    def _free_angles(self, owner, k):
        used = []
        for e in self.edges:
            if e["a"] == owner.name or e["b"] == owner.name:
                o = self.nodes[e["b"] if e["a"] == owner.name else e["a"]]
                ang0 = math.atan2(o.y - owner.y, o.x - owner.x)
                used.append(ang0)
                if sum(1 for x in self.edges if {x["a"], x["b"]} == {e["a"], e["b"]}) > 1:
                    used += [ang0 + math.radians(32), ang0 - math.radians(32)]
        for (px, py) in getattr(owner, "parents", []):
            used.append(math.atan2(py - owner.y, px - owner.x))
        # candidatos cada 10º, puntuados por distancia al ángulo usado más cercano
        cands = []
        for i in range(36):
            ang = -math.pi + i * math.pi / 18
            dmin = min([abs((ang - u + math.pi) % (2 * math.pi) - math.pi) for u in used] or [math.pi])
            cands.append((ang, dmin))
        free = [c for c in cands if c[1] > math.radians(38)]
        if len(free) < k:
            free = sorted(cands, key=lambda c: -c[1])[: max(k, 6)]
        free.sort(key=lambda c: c[0])
        # repartir k ángulos de forma uniforme entre los libres
        if len(free) <= k:
            return [c[0] for c in free]
        step = len(free) / k
        return [free[int(i * step + step / 2)][0] for i in range(k)]

    def _blocked(self, a, placed, owner):
        r = a.rect(4)
        for o in self.nodes.values():
            if o.w and _ov(r, o.rect(6)):
                return True
        for p in placed:
            if _ov(r, p.rect(4)):
                return True
        for rr in self._reserved:
            if _ov(r, rr):
                return True
        for e in self.edges:
            A, B = self.nodes[e["a"]], self.nodes[e["b"]]
            if e["kind"] in ("rel", "sup", "sub"):
                if _seg_rect((A.x, A.y), (B.x, B.y), r):
                    return True
        for (s, t) in self._attr_edges:
            if _seg_rect(s, t, r):
                return True
        return False

    def _place_attrs(self):
        placed = []
        self._attr_edges = []
        self._reserved = []
        for e in self.edges:
            if e["kind"] != "rel":
                continue
            A, B = self.nodes[e["a"]], self.nodes[e["b"]]
            p, q = A.border(B.x, B.y), B.border(A.x, A.y)
            x, y = p[0] + (q[0] - p[0]) * 0.78, p[1] + (q[1] - p[1]) * 0.78
            self._reserved.append((x - 26, y - 14, x + 26, y + 14))
        for name in self.order:
            owner = self.nodes[name]
            if not owner.attrs:
                continue
            self._place_for(owner, owner.attrs, placed)
        self.attr_nodes = placed

    def _place_for(self, owner, specs, placed, base=None):
        k = len(specs)
        angs = self._free_angles(owner, k)
        if base is not None:
            pass
        for spec, ang in zip(specs, angs):
            a = self._make_attr(spec, small=(owner.kind == "att"))
            a.owner = owner
            a.parents = [(owner.x, owner.y)]
            r0 = max(owner.w, owner.h) / 2 + a.w / 2 * abs(math.cos(ang)) + a.h / 2 * abs(math.sin(ang)) + 22
            best = None
            for dr in range(0, 260, 10):
                for da in (0, 8, -8, 16, -16, 24, -24):
                    an = ang + math.radians(da)
                    a.x = owner.x + math.cos(an) * (r0 + dr)
                    a.y = owner.y + math.sin(an) * (r0 + dr) * 0.92
                    if not self._blocked(a, placed, owner):
                        best = (a.x, a.y); break
                if best: break
            if not best:
                a.x = owner.x + math.cos(ang) * r0; a.y = owner.y + math.sin(ang) * r0
            placed.append(a)
            self._attr_edges.append(((owner.x, owner.y), (a.x, a.y)))
            if a.opts["kids"]:
                self._place_for(a, a.opts["kids"], placed)

    # ------------------------------------------------------------ render
    def _ctrl(self, A, B, bend):
        mx, my = (A.x + B.x) / 2, (A.y + B.y) / 2
        dx, dy = B.x - A.x, B.y - A.y
        d = math.hypot(dx, dy) or 1
        return mx - dy / d * bend, my + dx / d * bend

    def render(self, path):
        self._place_attrs()
        out = []
        # agregaciones: rectángulos
        aggbox = {}
        for ag in self.aggs:
            ms = [self.nodes[m] for m in ag["members"]]
            for m in ms:
                pass
            x0 = min(m.rect()[0] for m in ms) - 26; y0 = min(m.rect()[1] for m in ms) - 22
            x1 = max(m.rect()[2] for m in ms) + 26; y1 = max(m.rect()[3] for m in ms) + 22
            # incluir atributos de los miembros
            for a in self.attr_nodes:
                top = a
                while hasattr(top, "owner"):
                    top = top.owner
                if top.name in ag["members"]:
                    x0 = min(x0, a.rect()[0] - 8); y0 = min(y0, a.rect()[1] - 8)
                    x1 = max(x1, a.rect()[2] + 8); y1 = max(y1, a.rect()[3] + 8)
            b = self.nodes[ag["name"]]
            b.x, b.y, b.w, b.h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
            aggbox[ag["name"]] = (x0, y0, x1, y1, ag["label"])

        for ag in aggbox.values():
            x0, y0, x1, y1, lab = ag
            out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" rx="14" fill="none" '
                       f'stroke="{C_SUB[1]}" stroke-width="1.6" stroke-dasharray="7 5"/>')
            if lab:
                out.append(f'<text x="{x0+10:.1f}" y="{y0+14:.1f}" font-size="11" fill="{C_SUB[1]}" font-style="italic">{escape(lab)}</text>')

        # aristas de atributos
        for a in self.attr_nodes:
            o = a.owner
            p, q = o.border(a.x, a.y), a.border(o.x, o.y)
            out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{C_LINE}" stroke-width="1.2"/>')

        # aristas principales
        same = {}
        for e in self.edges:
            same.setdefault(frozenset((e["a"], e["b"])) if e["a"] != e["b"] else None, []).append(e)
        labels = []
        pair_count = {}
        for e in self.edges:
            A, B = self.nodes[e["a"]], self.nodes[e["b"]]
            key = (e["a"], e["b"])
            idx = pair_count.get(key, 0); pair_count[key] = idx + 1
            n_same = sum(1 for x in self.edges if (x["a"], x["b"]) == key)
            bend = 0
            if n_same > 1:
                bend = (idx - (n_same - 1) / 2) * 90
            if e["b"] in aggbox_names(self) and e["a"] not in aggbox_names(self):
                pass
            tx, ty = (B.x, B.y)
            if bend:
                cx, cy = self._ctrl(A, B, bend)
                p = A.border(cx, cy); q = B.border(cx, cy)
                path_d = f'M{p[0]:.1f},{p[1]:.1f} Q{cx:.1f},{cy:.1f} {q[0]:.1f},{q[1]:.1f}'
                pt = lambda t: ((1-t)**2*p[0]+2*(1-t)*t*cx+t*t*q[0], (1-t)**2*p[1]+2*(1-t)*t*cy+t*t*q[1])
                out.append(f'<path d="{path_d}" fill="none" stroke="{C_LINE}" stroke-width="1.8"/>')
            else:
                p = A.border(B.x, B.y); q = B.border(A.x, A.y)
                pt = lambda t, p=p, q=q: (p[0] + (q[0]-p[0]) * t, p[1] + (q[1]-p[1]) * t)
                if e["kind"] == "sup" and e.get("total"):
                    dx, dy = q[0]-p[0], q[1]-p[1]; d = math.hypot(dx, dy) or 1
                    ox, oy = -dy/d*2.6, dx/d*2.6
                    for s in (1, -1):
                        out.append(f'<line x1="{p[0]+ox*s:.1f}" y1="{p[1]+oy*s:.1f}" x2="{q[0]+ox*s:.1f}" y2="{q[1]+oy*s:.1f}" stroke="{C_LINE}" stroke-width="1.5"/>')
                else:
                    out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{C_LINE}" stroke-width="1.8"/>')
            if e["kind"] == "rel":
                # etiqueta cerca de la entidad (extremo q)
                t = 0.78
                x, y = pt(t)
                ox, oy = self._perp(pt(0.7), pt(0.85), 12)
                txt = e["card"] or ""
                labels.append((x + ox, y + oy, txt, True))
                if e.get("role"):
                    xm, ym = pt(0.5)
                    ox, oy = self._perp(pt(0.45), pt(0.55), -13 if not bend else (17 if bend > 0 else -17))
                    labels.append((xm + ox, ym + oy, e["role"], False))
        # nodos
        for name in self.order:
            n = self.nodes[name]
            out.append(self._node_svg(n))
        for a in self.attr_nodes:
            out.append(self._attr_svg(a))
        for (x, y, txt, is_card) in labels:
            if is_card:
                w = tw(txt, 12, True) + 6
                out.append(f'<rect x="{x-w/2:.1f}" y="{y-9:.1f}" width="{w:.1f}" height="16" rx="3" fill="{BG}" opacity=".88"/>'
                           f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="12" font-weight="700" fill="{C_CARD}">{escape(txt)}</text>')
            else:
                w = tw(txt, 10) + 6
                out.append(f'<rect x="{x-w/2:.1f}" y="{y-8:.1f}" width="{w:.1f}" height="14" rx="3" fill="{BG}" opacity=".88"/>'
                           f'<text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle" font-size="10" font-style="italic" fill="{C_ROLE}">{escape(txt)}</text>')
        # tamaño
        xs, ys = [], []
        for n in list(self.nodes.values()) + self.attr_nodes:
            if n.w:
                r = n.rect(); xs += [r[0], r[2]]; ys += [r[1], r[3]]
        for ag in aggbox.values():
            xs += [ag[0], ag[2]]; ys += [ag[1], ag[3]]
        x0, y0, x1, y1 = min(xs) - 18, min(ys) - 18, max(xs) + 18, max(ys) + 18
        W, H = x1 - x0, y1 - y0
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
               f'role="img" aria-label="{escape(self.title or self.name)}" font-family="{FAM}">'
               f'<title>{escape(self.title or self.name)}</title>'
               f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{W:.0f}" height="{H:.0f}" fill="{BG}"/>' + "".join(out) + "</svg>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)

    @staticmethod
    def _perp(p, q, d):
        dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy) or 1
        return -dy / L * d, dx / L * d

    def _node_svg(self, n):
        x, y = n.x, n.y
        if n.kind == "ent":
            s = (f'<rect x="{x-n.w/2:.1f}" y="{y-n.h/2:.1f}" width="{n.w:.1f}" height="{n.h:.1f}" fill="{C_ENT[0]}" stroke="{C_ENT[1]}" stroke-width="2"/>')
            if n.weak:
                s += (f'<rect x="{x-n.w/2+4:.1f}" y="{y-n.h/2+4:.1f}" width="{n.w-8:.1f}" height="{n.h-8:.1f}" fill="none" stroke="{C_ENT[1]}" stroke-width="1.6"/>')
            s += f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="{TXT}">{escape(n.label)}</text>'
            return s
        if n.kind == "rel":
            def dia(k):
                a, b = n.w / 2 - k, n.h / 2 - k
                return f'{x:.1f},{y-b:.1f} {x+a:.1f},{y:.1f} {x:.1f},{y+b:.1f} {x-a:.1f},{y:.1f}'
            s = f'<polygon points="{dia(0)}" fill="{C_REL[0]}" stroke="{C_REL[1]}" stroke-width="2"/>'
            if n.ident:
                s += f'<polygon points="{dia(6)}" fill="none" stroke="{C_REL[1]}" stroke-width="1.6"/>'
            y0 = y - 7 * (len(n.lines) - 1) + 4
            for i, ln in enumerate(n.lines):
                s += f'<text x="{x:.1f}" y="{y0+i*14:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="{TXT}">{escape(ln)}</text>'
            return s
        if n.kind == "sub":
            return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{C_SUB[0]}" stroke="{C_SUB[1]}" stroke-width="2"/>'
                    f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="{C_SUB[1]}">{escape(n.label)}</text>')
        return ""

    def _attr_svg(self, a):
        o = a.opts
        x, y = a.x, a.y
        s = (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{a.w/2:.1f}" ry="{a.h/2:.1f}" fill="{C_ATT[0]}" stroke="{C_ATT[1]}" stroke-width="1.4"'
             + (' stroke-dasharray="5 3"' if o["mark"] == "/" else "") + "/>")
        if o["mark"] == "+":
            s += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{a.w/2-4:.1f}" ry="{a.h/2-4:.1f}" fill="none" stroke="{C_ATT[1]}" stroke-width="1.2"/>'
        s += f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="{o["fs"]}" fill="{TXT}">{escape(a.label)}</text>'
        if o["mark"] in ("*", "~"):
            w = tw(a.label, o["fs"])
            dash = ' stroke-dasharray="3 2"' if o["mark"] == "~" else ""
            s += f'<line x1="{x-w/2:.1f}" y1="{y+7:.1f}" x2="{x+w/2:.1f}" y2="{y+7:.1f}" stroke="{TXT}" stroke-width="1.1"{dash}/>'
        return s


def aggbox_names(d):
    return {a["name"] for a in d.aggs}


def _ov(r1, r2):
    return not (r1[2] < r2[0] or r2[2] < r1[0] or r1[3] < r2[1] or r2[3] < r1[1])


def _seg_rect(p, q, r):
    # ¿el segmento pq corta el rectángulo r? (Liang-Barsky)
    x0, y0 = p; dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - r[0]), (dx, r[2] - x0), (-dy, y0 - r[1]), (dy, r[3] - y0)):
        if pp == 0:
            if qq < 0: return False
        else:
            t = qq / pp
            if pp < 0:
                if t > t1: return False
                t0 = max(t0, t)
            else:
                if t < t0: return False
                t1 = min(t1, t)
    return True
