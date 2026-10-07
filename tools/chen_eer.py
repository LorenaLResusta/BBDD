#!/usr/bin/env python3
"""Generador de diagramas EER en notación de Chen (SVG).

Describe el modelo con objetos Python (entidades, relaciones, jerarquías) y el
script calcula la posición de los elementos y escribe un SVG con el mismo
aspecto que el resto de diagramas del sitio (fondo oscuro).

Convenio de cardinalidades (el mismo de la teoría de la UD02):
    la pareja (mín, máx) escrita JUNTO A UNA ENTIDAD indica con cuántas
    instancias de esa entidad se relaciona una instancia de la otra.

Elementos:
    Entidad            rectángulo          Entidad débil     rectángulo doble
    Relación           rombo               Relación ident.   rombo doble
    Atributo           óvalo               Clave             subrayado continuo
    Discriminador      subrayado discont.  Multivaluado      óvalo doble
    Derivado           óvalo discontinuo   Compuesto         óvalo con sub-óvalos
    Jerarquía (ISA)    círculo d / o       Subclase          línea con ⊂
    Participación total en la jerarquía    línea doble hacia el círculo
"""
import json
import math
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from PIL import ImageFont

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_f_reg = ImageFont.truetype(FONT_REG, 12)
_f_bold = ImageFont.truetype(FONT_BOLD, 13)

BG = "#0f172a"
LINE = "#94a3b8"
ENT_F, ENT_S = "#075985", "#38bdf8"
REL_F, REL_S = "#047857", "#34d399"
ATT_F, ATT_S = "#312e81", "#a5b4fc"
ISA_F, ISA_S = "#92400e", "#fbbf24"
CARD = "#fde68a"
TXT = "#f8fafc"


# ---------------------------------------------------------------- modelo
@dataclass
class A:
    """Atributo. k=clave, kp=discriminador, mv=multivaluado, d=derivado."""
    name: str
    k: bool = False
    kp: bool = False
    mv: bool = False
    d: bool = False
    comp: list = field(default_factory=list)  # lista de nombres (atributo compuesto)


def K(n):  return A(n, k=True)
def KP(n): return A(n, kp=True)
def MV(n): return A(n, mv=True)
def D(n):  return A(n, d=True)
def C(n, *subs): return A(n, comp=list(subs))


@dataclass
class E:
    name: str
    attrs: list = field(default_factory=list)
    weak: bool = False


@dataclass
class R:
    """Relación. ends = [(entidad, '(mín,máx)', rol|None), ...]"""
    name: str
    ends: list
    attrs: list = field(default_factory=list)
    ident: bool = False  # relación identificadora (rombo doble)


@dataclass
class ISA:
    sup: str
    subs: list
    kind: str = "d"      # d disjunta · o solapada
    total: bool = False


@dataclass
class Model:
    title: str
    desc: str
    ents: list
    rels: list = field(default_factory=list)
    isas: list = field(default_factory=list)


# ---------------------------------------------------------------- medidas
def tw(text, bold=False):
    return (_f_bold if bold else _f_reg).getlength(text)


def attr_size(a_name):
    w = tw(a_name) + 22
    return max(w, 54), 28


def ent_size(name):
    return max(tw(name, True) + 34, 84), 42


def rel_size(name):
    w = tw(name, True) + 40
    return max(w, 84), 52


class Node:
    def __init__(self, kind, label, w, h):
        self.kind, self.label, self.w, self.h = kind, label, w, h
        self.x = self.y = 0.0
        self.obj = None
        self.attrs = []    # nodos atributo colgados


def support(kind, w, h, ang):
    """Distancia del centro al borde de la forma en la dirección ang."""
    c, s = math.cos(ang), math.sin(ang)
    hw, hh = w / 2, h / 2
    if kind in ("ent",):
        if abs(c) * hh > abs(s) * hw:
            return hw / max(abs(c), 1e-9)
        return hh / max(abs(s), 1e-9)
    if kind == "rel":
        return 1 / max(abs(c) / hw + abs(s) / hh, 1e-9)
    # elipse / círculo
    return 1 / math.sqrt((c / hw) ** 2 + (s / hh) ** 2)


# ---------------------------------------------------------------- layout
def build_nodes(m: Model):
    nodes, edges = {}, []
    for e in m.ents:
        w, h = ent_size(e.name)
        n = Node("ent", e.name, w, h)
        n.obj = e
        nodes["E:" + e.name] = n
    for i, r in enumerate(m.rels):
        w, h = rel_size(r.name)
        n = Node("rel", r.name, w, h)
        n.obj = r
        nodes[f"R:{i}"] = n
        for j, (en, card, role) in enumerate(r.ends):
            edges.append((f"E:{en}", f"R:{i}", dict(card=card, role=role, idx=j, rel=r)))
    for i, s in enumerate(m.isas):
        n = Node("isa", s.kind, 32, 32)
        n.obj = s
        nodes[f"I:{i}"] = n
        edges.append((f"E:{s.sup}", f"I:{i}", dict(total=s.total, isa="sup")))
        for sb in s.subs:
            edges.append((f"I:{i}", f"E:{sb}", dict(isa="sub")))
    return nodes, edges


def natt(a):
    return 1 + len(a.comp)


def layout_radius(n):
    obj = n.obj
    if n.kind == "isa":
        return 34
    cnt = sum(natt(a) for a in obj.attrs) if hasattr(obj, "attrs") else 0
    if n.kind == "ent":
        return max(n.w / 2 + 12, 24 + 8 * cnt + n.w * 0.1)
    recursiva = len({e[0] for e in obj.ends}) < len(obj.ends)
    return max(n.w / 2 + 24 + (46 if recursiva else 0), 22 + 10 * cnt)


def run_neato(nodes, edges, seed, spread):
    lines = ["graph G {", f'graph [start={seed}, overlap=prism, sep="+6", splines=false];',
             "node [shape=box, fixedsize=true, label=\"\"];"]
    rad = {k: layout_radius(n) for k, n in nodes.items()}
    for k, n in nodes.items():
        d = rad[k] * 2 / 72
        lines.append(f'"{k}" [width={d:.3f}, height={d:.3f}];')
    for a, b, info in edges:
        ln = (rad[a] + rad[b]) * spread / 72
        lines.append(f'"{a}" -- "{b}" [len={ln:.3f}];')
    lines.append("}")
    with tempfile.NamedTemporaryFile("w", suffix=".dot", delete=False) as f:
        f.write("\n".join(lines))
        path = f.name
    out = subprocess.run(["neato", "-Tjson", path], capture_output=True, text=True)
    os.unlink(path)
    if out.returncode != 0:
        raise RuntimeError(out.stderr)
    data = json.loads(out.stdout)
    for o in data["objects"]:
        x, y = map(float, o["pos"].split(","))
        nodes[o["name"]].x, nodes[o["name"]].y = x, -y
    return rad



import random


def refine(nodes, edges, rad, iters=3500, seed=0):
    """Recocido simulado sobre el esqueleto: compacta y evita solapes/cruces."""
    rnd = random.Random(seed)
    keys = list(nodes)
    idx = {k: i for i, k in enumerate(keys)}
    P = [[nodes[k].x, nodes[k].y] for k in keys]
    R = [rad[k] for k in keys]
    E_ = [(idx[a], idx[b]) for a, b, _ in edges]

    def cost():
        c = 0.0
        n = len(P)
        for i in range(n):
            for j in range(i + 1, n):
                d = math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1])
                need = (R[i] + R[j]) * 1.0
                if d < need:
                    c += (need - d) ** 2 * 1.6
        for a, b in E_:
            c += math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]) * 0.9
        for i in range(len(E_)):
            a, b = E_[i]
            for j in range(i + 1, len(E_)):
                x, y = E_[j]
                if len({a, b, x, y}) < 4:
                    continue
                if seg_inter(P[a], P[b], P[x], P[y]):
                    c += 4000
            for k in range(n):
                if k in (a, b):
                    continue
                # distancia del nodo k al segmento ab
                ax, ay = P[a]; bx, by = P[b]
                dx, dy = bx - ax, by - ay
                L2 = dx * dx + dy * dy or 1
                t = max(0, min(1, ((P[k][0] - ax) * dx + (P[k][1] - ay) * dy) / L2))
                dd = math.hypot(P[k][0] - (ax + t * dx), P[k][1] - (ay + t * dy))
                lim = R[k] * 0.55 + 14
                if dd < lim:
                    c += (lim - dd) ** 2 * 3
        xs0 = min(P[i][0] - R[i] for i in range(n)); xs1 = max(P[i][0] + R[i] for i in range(n))
        ys0 = min(P[i][1] - R[i] for i in range(n)); ys1 = max(P[i][1] + R[i] for i in range(n))
        Wd, Ht = xs1 - xs0, ys1 - ys0
        c += Wd * Ht * 0.004
        if Ht > Wd * 0.9:
            c += (Ht - Wd * 0.9) * 8
        if Wd > Ht * 2.0:
            c += (Wd - Ht * 2.0) * 8
        return c

    cur = cost()
    T0 = 60.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.5
        i = rnd.randrange(len(P))
        ox, oy = P[i]
        step = 8 + 90 * (1 - it / iters)
        P[i][0] += rnd.gauss(0, step)
        P[i][1] += rnd.gauss(0, step)
        nc = cost()
        if nc < cur or rnd.random() < math.exp((cur - nc) / (T * 12)):
            cur = nc
        else:
            P[i][0], P[i][1] = ox, oy
    for k, p in zip(keys, P):
        nodes[k].x, nodes[k].y = p
    return cur


def edge_angles(nodes, edges, key):
    n = nodes[key]
    res = []
    for a, b, info in edges:
        if a == key or b == key:
            o = nodes[b] if a == key else nodes[a]
            res.append(math.atan2(o.y - n.y, o.x - n.x))
    return res


def ang_dist(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def place_attrs(nodes, edges):
    """Reparte los atributos en el círculo alrededor de cada entidad/relación."""
    attr_nodes = []
    for key, n in list(nodes.items()):
        if n.kind not in ("ent", "rel") or not n.obj.attrs:
            continue
        taken = edge_angles(nodes, edges, key)
        k = len(n.obj.attrs)
        chosen = []
        cands = [i * math.pi / 36 for i in range(72)]
        # tamaños para ordenar: primero atributos largos en horizontales
        for _ in range(k):
            best, bs = None, -1
            for c in cands:
                items = taken + chosen
                clear = min(ang_dist(c, t) for t in items) if items else math.pi
                # las aristas pesan más: no queremos atributos sobre ellas
                clear_edge = min((ang_dist(c, t) for t in taken), default=math.pi)
                score = min(clear, clear_edge * 1.6)
                if score > bs:
                    best, bs = c, score
            chosen.append(best)
        chosen.sort()
        attrs = list(n.obj.attrs)
        # los atributos más anchos van a las direcciones más horizontales
        order = sorted(range(k), key=lambda i: abs(math.cos(chosen[i])))
        sizes = sorted(range(k), key=lambda i: -attr_size(attrs[i].name)[0])
        assign = {}
        for rank, ci in enumerate(order[::-1]):
            assign[ci] = sizes[rank]
        for ci in range(k):
            a = attrs[assign[ci]]
            ang = chosen[ci]
            w, h = attr_size(a.name)
            gap = 26 if n.kind == "ent" else 22
            r = support(n.kind, n.w, n.h, ang) + support("att", w, h, ang) + gap
            if k > 5 and ci % 2:
                r += 22
            an = Node("att", a.name, w, h)
            an.obj = a
            an.x, an.y = n.x + r * math.cos(ang), n.y + r * math.sin(ang)
            an.parent = n
            an.owner, an.r, an.ang = n, r, ang
            n.attrs.append(an)
            attr_nodes.append(an)
            # atributos compuestos: hijos más afuera en abanico
            if a.comp:
                m = len(a.comp)
                used = []
                for j, sub in enumerate(a.comp):
                    sw, sh = attr_size(sub)
                    bestsa, bsc = ang, -9
                    for k2 in range(-14, 15):
                        off = k2 * 0.09
                        cand = ang + off
                        ce = min((ang_dist(cand, t) for t in taken), default=math.pi)
                        cc = min((ang_dist(cand, u) for u in used), default=math.pi)
                        sc = min(ce * 1.3, cc * 1.0, 0.9) - 0.12 * abs(off)
                        if sc > bsc:
                            bestsa, bsc = cand, sc
                    sa = bestsa
                    used.append(sa)
                    sr = r + support("att", w, h, sa) + support("att", sw, sh, sa) + 18
                    sn = Node("att", sub, sw, sh)
                    sn.obj = A(sub)
                    sn.x, sn.y = n.x + sr * math.cos(sa), n.y + sr * math.sin(sa)
                    sn.parent = an
                    sn.owner, sn.r, sn.ang = n, sr, sa
                    an.attrs.append(sn)
                    attr_nodes.append(sn)
    return attr_nodes



def relax_attrs(nodes, attr_nodes, edges=(), rounds=60):
    """Aparta los óvalos que se pisan entre sí o con otras formas."""
    allv = list(nodes.values()) + attr_nodes
    skel = [(p, q) for p, q, _, _ in skel_segments(nodes, edges)]
    def tot(an):
        t = 0.0
        segs = [((an.parent.x, an.parent.y), (an.x, an.y))] + [((an.x, an.y), (c.x, c.y)) for c in an.attrs]
        for sg in segs:
            for sk in skel:
                if seg_inter(sg[0], sg[1], sk[0], sk[1]):
                    t += 3000
            for v in allv:
                if v is an or v is an.parent or v in an.attrs or v is getattr(an.parent, "parent", None):
                    continue
                if v.kind == "att" and (v.parent is an):
                    continue
                if seg_hits_box(sg[0], sg[1], v, 3):
                    t += 1500
        for v in allv:
            if v is an or v is an.parent:
                continue
            if getattr(an.parent, "parent", None) is v:
                continue
            t += overlap_area(an, v, 6)
        return t
    def put(an, r, ang):
        an.r, an.ang = r, ang
        an.x = an.owner.x + r * math.cos(ang)
        an.y = an.owner.y + r * math.sin(ang)
    for _ in range(rounds):
        moved = False
        for an in attr_nodes:
            cur = tot(an)
            if cur <= 0:
                continue
            r0, a0 = an.r, an.ang
            best = (cur, r0, a0)
            for dr in (0, 10, 22, 36, 52):
                for da in (0, 0.1, -0.1, 0.22, -0.22, 0.36, -0.36):
                    if dr == 0 and da == 0:
                        continue
                    put(an, r0 + dr, a0 + da)
                    c = tot(an)
                    if c < best[0] - 1e-6:
                        best = (c, r0 + dr, a0 + da)
            put(an, best[1], best[2])
            if best[0] < cur:
                moved = True
        if not moved:
            break


def box(n):
    return (n.x - n.w / 2, n.y - n.h / 2, n.x + n.w / 2, n.y + n.h / 2)


def overlap_area(a, b, pad=3):
    ax0, ay0, ax1, ay1 = box(a)
    bx0, by0, bx1, by1 = box(b)
    w = min(ax1, bx1) - max(ax0, bx0) + pad
    h = min(ay1, by1) - max(ay0, by0) + pad
    return w * h if w > 0 and h > 0 else 0


def seg_inter(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = ccw(p1, p2, p3), ccw(p1, p2, p4)
    d3, d4 = ccw(p3, p4, p1), ccw(p3, p4, p2)
    return d1 * d2 < 0 and d3 * d4 < 0


def seg_hits_box(p, q, n, shrink=4):
    x0, y0, x1, y1 = box(n)
    x0 += shrink; y0 += shrink; x1 -= shrink; y1 -= shrink
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        if seg_inter(p, q, corners[i], corners[(i + 1) % 4]):
            return True
    inside = lambda pt: x0 < pt[0] < x1 and y0 < pt[1] < y1
    return inside(p) or inside(q)


def skel_segments(nodes, edges):
    """Segmentos del esqueleto; las aristas duplicadas (reflexivas) se curvan."""
    groups = {}
    for a, b, info in edges:
        groups.setdefault(frozenset((a, b)), []).append((a, b))
    segs, seen = [], {}
    for a, b, info in edges:
        key = frozenset((a, b))
        k = len(groups[key])
        gi = seen.get(key, 0); seen[key] = gi + 1
        na, nb = nodes[a], nodes[b]
        if k > 1:
            curve = (gi - (k - 1) / 2) * 70
            dx, dy = nb.x - na.x, nb.y - na.y
            L = math.hypot(dx, dy) or 1
            c = ((na.x + nb.x) / 2 - dy / L * curve, (na.y + nb.y) / 2 + dx / L * curve)
            mid = Node("mid", "", 1, 1); mid.x, mid.y = c
            segs.append(((na.x, na.y), c, na, mid))
            segs.append((c, (nb.x, nb.y), mid, nb))
        else:
            segs.append(((na.x, na.y), (nb.x, nb.y), na, nb))
    return segs


def all_edges_geometry(nodes, edges, attr_nodes):
    segs = skel_segments(nodes, edges)
    for an in attr_nodes:
        segs.append(((an.parent.x, an.parent.y), (an.x, an.y), an.parent, an))
    return segs


def penalty(nodes, edges, attr_nodes):
    allv = list(nodes.values()) + attr_nodes
    p = 0.0
    for i in range(len(allv)):
        for j in range(i + 1, len(allv)):
            p += overlap_area(allv[i], allv[j]) * 4.0
    segs = all_edges_geometry(nodes, edges, attr_nodes)
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            a, b = segs[i], segs[j]
            if len({id(a[2]), id(a[3]), id(b[2]), id(b[3])}) < 4:
                continue
            if seg_inter(a[0], a[1], b[0], b[1]):
                p += 4000
    for (p1, p2, na, nb) in segs:
        for v in allv:
            if v is na or v is nb:
                continue
            if seg_hits_box(p1, p2, v):
                p += 3000
    # etiquetas de cardinalidad que pisan otros nodos
    for a, b, info in edges:
        if "card" not in info:
            continue
        ent = nodes[a] if a.startswith("E:") else nodes[b]
        oth = nodes[b] if a.startswith("E:") else nodes[a]
        bp = boundary_point(ent, (oth.x, oth.y))
        d = math.hypot(oth.x - bp[0], oth.y - bp[1]) or 1
        t = min(0.85, 30 / d)
        lx, ly = bp[0] + (oth.x - bp[0]) * t, bp[1] + (oth.y - bp[1]) * t
        lab = Node("lab", "", 42, 18); lab.x, lab.y = lx, ly
        for v in allv:
            if v is ent or v is oth:
                continue
            p += overlap_area(lab, v, 0) * 6
    xs = [v.x for v in allv]; ys = [v.y for v in allv]
    Wd, Ht = max(xs) - min(xs), max(ys) - min(ys)
    p += Wd * Ht * 0.006
    if Ht > Wd * 1.25:
        p += (Ht - Wd * 1.25) * 40
    if Wd > Ht * 2.2:
        p += (Wd - Ht * 2.2) * 40
    return p


def solve(m: Model, tries=14):
    best = None
    for seed in range(1, tries + 1):
        nodes, edges = build_nodes(m)
        try:
            rad = run_neato(nodes, edges, seed, 0.8)
        except Exception:
            continue
        refine(nodes, edges, rad, seed=seed)
        at = place_attrs(nodes, edges)
        relax_attrs(nodes, at, edges)
        p = penalty(nodes, edges, at)
        if best is None or p < best[0]:
            best = (p, nodes, edges, at, seed, 0.8)
    return best


# ---------------------------------------------------------------- dibujo
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def boundary_point(n, toward, extra=0):
    ang = math.atan2(toward[1] - n.y, toward[0] - n.x)
    d = support(n.kind if n.kind in ("ent", "rel") else "att", n.w, n.h, ang) + extra
    return n.x + d * math.cos(ang), n.y + d * math.sin(ang)


def parallel(p, q, off):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * off, dx / L * off
    return (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)


def label(x, y, text, color=CARD, size=12, italic=False, bold=True):
    w = tw(text) + 8
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="700"' if bold else ""
    return (f'<rect x="{x - w / 2:.1f}" y="{y - 9:.1f}" width="{w:.1f}" height="17" rx="4" fill="{BG}" opacity="0.92"/>'
            f'<text x="{x:.1f}" y="{y + 4.5:.1f}" font-size="{size}" fill="{color}" text-anchor="middle"{st}{wt}>{esc(text)}</text>')


def render(m: Model, best):
    _, nodes, edges, attr_nodes, seed, spread = best
    out_els, lines, shapes, texts = [], [], [], []
    allv = list(nodes.values()) + attr_nodes
    # aristas atributo
    for an in attr_nodes:
        p = boundary_point(an.parent, (an.x, an.y))
        q = boundary_point(an, (an.parent.x, an.parent.y))
        lines.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')

    # aristas esqueleto
    pair_count = {}
    for a, b, info in edges:
        pair_count.setdefault(frozenset((a, b)), []).append(info)
    done = {}
    for a, b, info in edges:
        na, nb = nodes[a], nodes[b]
        key = frozenset((a, b))
        group = pair_count[key]
        gi = done.get(key, 0)
        done[key] = gi + 1
        curve = 0
        if len(group) > 1:
            curve = (gi - (len(group) - 1) / 2) * 70
        c = ((na.x + nb.x) / 2, (na.y + nb.y) / 2)
        if curve:
            dx, dy = nb.x - na.x, nb.y - na.y
            L = math.hypot(dx, dy) or 1
            c = (c[0] - dy / L * curve, c[1] + dx / L * curve)
            tgt_a, tgt_b = c, c
        else:
            tgt_a, tgt_b = (nb.x, nb.y), (na.x, na.y)
        p = boundary_point(na, tgt_a)
        q = boundary_point(nb, tgt_b)
        double = info.get("total") or (
            "rel" in info and False)
        # entidad débil en relación identificadora → doble línea
        if "rel" in info:
            ent = nodes[a] if a.startswith("E:") else nodes[b]
            rel = info["rel"]
            if rel.ident and ent.obj.weak:
                double = True
        if curve:
            path = f'M{p[0]:.1f} {p[1]:.1f} Q{c[0] * 2 - (p[0] + q[0]) / 2:.1f} {c[1] * 2 - (p[1] + q[1]) / 2:.1f} {q[0]:.1f} {q[1]:.1f}'
            lines.append(f'<path d="{path}" fill="none"/>')
            ctrl = (c[0] * 2 - (p[0] + q[0]) / 2, c[1] * 2 - (p[1] + q[1]) / 2)
            def bez(t):
                return ((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * ctrl[0] + t * t * q[0],
                        (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * ctrl[1] + t * t * q[1])
            pt_at = lambda ent_is_p, dist: bez(min(0.9, dist / max(1, math.hypot(q[0] - p[0], q[1] - p[1]))) if ent_is_p else 1 - min(0.9, dist / max(1, math.hypot(q[0] - p[0], q[1] - p[1]))))
        else:
            if double:
                for off in (-2.6, 2.6):
                    pp, qq = parallel(p, q, off)
                    lines.append(f'<line x1="{pp[0]:.1f}" y1="{pp[1]:.1f}" x2="{qq[0]:.1f}" y2="{qq[1]:.1f}"/>')
            else:
                lines.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')
            def pt_at(ent_is_p, dist, p=p, q=q):
                L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
                t = min(0.85, dist / L)
                if not ent_is_p:
                    t = 1 - t
                return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
        # etiquetas
        if "card" in info:
            ent_is_a = a.startswith("E:")
            ent_pt_is_p = ent_is_a
            ent_node = na if ent_is_a else nb
            dist = 30
            x, y = pt_at(ent_pt_is_p, dist)
            texts.append(label(x, y, info["card"]))
            if info.get("role"):
                L = math.hypot(q[0] - p[0], q[1] - p[1])
                x2, y2 = pt_at(ent_pt_is_p, max(dist + 38, L * 0.55))
                texts.append(label(x2, y2, info["role"], color="#cbd5e1", italic=True, bold=False, size=11))
        elif info.get("isa") == "sub":
            # símbolo de subconjunto ⊂ junto a la subclase, abierto hacia el círculo
            L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1
            ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
            cx, cy = q[0] - ux * 22, q[1] - uy * 22
            ang = math.degrees(math.atan2(uy, ux))
            shapes.append(f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({ang:.1f})">'
                          f'<rect x="-6" y="-8" width="9" height="16" fill="{BG}" stroke="none"/>'
                          f'<path d="M3 -7 A7 7 0 0 0 3 7" fill="none" stroke="{ISA_S}" stroke-width="2"/></g>')

    # formas
    for key, n in nodes.items():
        if n.kind == "ent":
            e = n.obj
            x0, y0, x1, y1 = box(n)
            shapes.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{n.w:.1f}" height="{n.h:.1f}" fill="{ENT_F}" stroke="{ENT_S}" stroke-width="2"/>')
            if e.weak:
                shapes.append(f'<rect x="{x0 + 5:.1f}" y="{y0 + 5:.1f}" width="{n.w - 10:.1f}" height="{n.h - 10:.1f}" fill="none" stroke="{ENT_S}" stroke-width="2"/>')
            texts.append(f'<text x="{n.x:.1f}" y="{n.y + 5:.1f}" font-size="13" font-weight="700" text-anchor="middle" fill="{TXT}">{esc(n.label)}</text>')
        elif n.kind == "rel":
            r = n.obj
            pts = lambda k: f"{n.x:.1f},{n.y - n.h / 2 + k:.1f} {n.x + n.w / 2 - k * n.w / n.h:.1f},{n.y:.1f} {n.x:.1f},{n.y + n.h / 2 - k:.1f} {n.x - n.w / 2 + k * n.w / n.h:.1f},{n.y:.1f}"
            shapes.append(f'<polygon points="{pts(0)}" fill="{REL_F}" stroke="{REL_S}" stroke-width="2"/>')
            if r.ident:
                shapes.append(f'<polygon points="{pts(7)}" fill="none" stroke="{REL_S}" stroke-width="2"/>')
            texts.append(f'<text x="{n.x:.1f}" y="{n.y + 4.5:.1f}" font-size="12" font-weight="700" text-anchor="middle" fill="{TXT}">{esc(n.label)}</text>')
        elif n.kind == "isa":
            shapes.append(f'<circle cx="{n.x:.1f}" cy="{n.y:.1f}" r="16" fill="{ISA_F}" stroke="{ISA_S}" stroke-width="2"/>')
            texts.append(f'<text x="{n.x:.1f}" y="{n.y + 5:.1f}" font-size="14" font-weight="700" text-anchor="middle" fill="{TXT}">{n.label}</text>')
    for an in attr_nodes:
        a = an.obj
        dash = ' stroke-dasharray="5 3"' if a.d else ""
        shapes.append(f'<ellipse cx="{an.x:.1f}" cy="{an.y:.1f}" rx="{an.w / 2:.1f}" ry="{an.h / 2:.1f}" fill="{ATT_F}" stroke="{ATT_S}" stroke-width="2"{dash}/>')
        if a.mv:
            shapes.append(f'<ellipse cx="{an.x:.1f}" cy="{an.y:.1f}" rx="{an.w / 2 - 5:.1f}" ry="{an.h / 2 - 5:.1f}" fill="none" stroke="{ATT_S}" stroke-width="1.6"/>')
        texts.append(f'<text x="{an.x:.1f}" y="{an.y + 4:.1f}" font-size="12" text-anchor="middle" fill="{TXT}">{esc(an.label)}</text>')
        if a.k or a.kp:
            w = tw(an.label)
            da = ' stroke-dasharray="4 3"' if a.kp else ""
            texts.append(f'<line x1="{an.x - w / 2:.1f}" y1="{an.y + 8:.1f}" x2="{an.x + w / 2:.1f}" y2="{an.y + 8:.1f}" stroke="{TXT}" stroke-width="1.4"{da}/>')

    allv2 = allv
    minx = min(v.x - v.w / 2 for v in allv2) - 24
    maxx = max(v.x + v.w / 2 for v in allv2) + 24
    miny = min(v.y - v.h / 2 for v in allv2) - 24
    maxy = max(v.y + v.h / 2 for v in allv2) + 24
    W, H = maxx - minx, maxy - miny
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx:.0f} {miny:.0f} {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-labelledby="t d" font-family="DejaVu Sans, Verdana, Arial, sans-serif">',
           f'<title id="t">{esc(m.title)}</title><desc id="d">{esc(m.desc)}</desc>',
           f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{W:.0f}" height="{H:.0f}" rx="10" fill="{BG}"/>',
           f'<g stroke="{LINE}" stroke-width="1.6" fill="none">' + "".join(lines) + "</g>"]
    # las líneas dobles de ISA total
    svg += shapes + texts + ["</svg>"]
    return "\n".join(svg), (W, H)


def draw(m: Model, path, tries=8):
    best = solve(m, tries)
    svg, size = render(m, best)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return best[0], size


if __name__ == "__main__":
    demo = Model(
        "Demo", "Demo",
        [E("EMPLEADO", [K("dni"), A("nombre"), C("direccion", "calle", "ciudad"), MV("telefono")]),
         E("DEPARTAMENTO", [K("codigo"), A("nombre")]),
         E("HIJO", [KP("nombre"), A("fecha_nac")], weak=True)],
        [R("trabaja", [("EMPLEADO", "(0,N)", None), ("DEPARTAMENTO", "(1,1)", None)]),
         R("dirige", [("EMPLEADO", "(0,1)", "jefe"), ("EMPLEADO", "(0,N)", "subordinado")]),
         R("tiene", [("EMPLEADO", "(1,1)", None), ("HIJO", "(0,N)", None)], ident=True)],
        [])
    print(draw(demo, "/tmp/demo.svg", 20))
