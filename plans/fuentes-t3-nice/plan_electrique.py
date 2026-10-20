"""Plan d'implantation électrique – T3 Nice Saint-Roch (client : A. Fuentes).

Géométrie reprise du croquis du diagnostiqueur (réf. 2139 C), remise à l'horizontale.
Unités : mètres (cotes approximatives, relevé à confirmer lors de la visite).
Génère plan_electrique_T3_Nice_Fuentes.pdf (page 1 : plan, page 2 : récapitulatif).
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_electrique_T3_Nice_Fuentes.pdf")

WALL = 0.16
C_PC, C_SPEC, C_LUM, C_CMD, C_COM, C_TAB = "#1f5fbf", "#d9480f", "#e8a800", "#222222", "#2b8a3e", "#c92a2a"
FACE = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

# ---------------------------------------------------------------- géométrie
OUTER = [(0, 0), (0, 6.82), (14.04, 6.82), (14.04, 1.60), (6.41, 1.60), (6.41, 0)]
# (x1, y1, x2, y2, [ouvertures (début, fin) le long du mur])
WALLS = [
    (0, 0, 0, 6.82, []),
    (0, 6.82, 14.04, 6.82, []),
    (6.41, 0, 6.41, 1.60, []),
    (0, 0, 6.41, 0, [(5.62, 6.05)]),  # porte palière
    (2.01, 0, 2.01, 3.63, [(1.58, 2.00)]),  # SdB
    (0, 2.81, 2.01, 2.81, []),
    (0, 3.63, 8.42, 3.63, [(2.37, 2.80), (4.42, 4.87), (7.22, 7.70)]),
    (2.01, 1.22, 3.21, 1.22, [(2.31, 2.80)]),  # WC
    (3.21, 0, 3.21, 2.42, []),
    (3.21, 3.63, 3.21, 6.82, []),
    (3.21, 2.42, 5.22, 2.42, []),
    (6.41, 2.42, 8.42, 2.42, []),
    (5.22, 0, 5.22, 3.63, [(1.18, 1.60), (2.81, 3.22)]),
    (6.03, 3.63, 6.03, 6.82, []),
    (8.42, 1.60, 8.42, 4.42, [(2.81, 3.22)]),  # cuisine
    (8.42, 4.42, 12.44, 4.42, []),
    (11.64, 1.60, 11.64, 4.42, [(2.63, 4.03)]),  # baie cuisine
    (12.44, 4.42, 12.44, 6.82, [(4.83, 6.46)]),  # baie séjour
    (6.41, 1.60, 14.04, 1.60, []),
    (14.04, 1.60, 14.04, 6.82, []),
]
WINDOWS = [  # (x1, y1, x2, y2)
    (1.60, 6.82, 2.83, 6.82), (3.62, 6.82, 4.84, 6.82), (7.37, 6.82, 8.55, 6.82),
    (11.64, 2.63, 11.64, 4.03), (12.44, 4.83, 12.44, 6.46),
]
# (charnière x, y, rayon, angle départ, angle fin)
DOORS = [
    (6.05, 0, 0.43, 90, 180), (2.01, 2.00, 0.42, 180, 270), (2.80, 3.63, 0.43, 180, 270),
    (4.87, 3.63, 0.45, 0, 90), (7.70, 3.63, 0.48, 0, 90), (2.80, 1.22, 0.49, 0, 90),
    (5.22, 1.60, 0.42, 180, 270), (5.22, 3.22, 0.41, 180, 270), (8.42, 3.22, 0.41, 270, 360),
]
SHAFTS = [(0, 2.81, 2.01, 3.63), (6.41, 1.60, 8.42, 2.42)]
ROOMS = [  # nom, surface, x, y
    ("CHAMBRE 1", "10,29 m²", 1.6, 5.75), ("CHAMBRE 2", "9,14 m²", 4.62, 5.75),
    ("SÉJOUR", "19,83 m²", 9.3, 6.15), ("CUISINE", "9,26 m²", 10.65, 3.15),
    ("SALLE DE BAINS", "4,48 m²", 1.0, 1.2), ("WC", "1,34 m²", 2.61, 0.42),
    ("DÉGAGEMENT", "2,89 m²", 2.62, 2.0), ("ENTRÉE", "10,64 m²", 5.82, 2.05),
    ("RANGEMENT", "", 4.22, 0.45), ("BALCON", "7,50 m²", 13.25, 3.0),
]


# ---------------------------------------------------------------- symboles
def frame(x, y, face, off=0.0):
    nx, ny = FACE[face]
    return (x + nx * off, y + ny * off), (nx, ny), (-ny, nx)


def pt(o, n, t, v, u=0.0):
    return (o[0] + n[0] * v + t[0] * u, o[1] + n[1] * v + t[1] * u)


def prise(ax, x, y, face, color=C_PC, label=None, double=False):
    shifts = (-0.13, 0.13) if double else (0.0,)
    for s in shifts:
        o, n, t = frame(x, y, face)
        o = pt(o, n, t, 0, s)
        ang = math.degrees(math.atan2(n[1], n[0]))
        c = pt(o, n, t, 0.17)
        ax.plot(*zip(o, c), color=color, lw=1.2, zorder=6)
        ax.add_patch(Arc(pt(o, n, t, 0.17), 0.26, 0.26, angle=ang, theta1=-90, theta2=90, color=color, lw=1.6, zorder=6))
        ax.plot(*zip(pt(o, n, t, 0.17, -0.13), pt(o, n, t, 0.17, 0.13)), color=color, lw=1.6, zorder=6)
    if label:
        lx, ly = pt(*frame(x, y, face)[:1], *frame(x, y, face)[1:], 0.55)
        ax.text(lx, ly, label, color=color, fontsize=5.6, ha="center", va="center", zorder=7, fontweight="bold")


def specialise(ax, x, y, face, label):
    o, n, t = frame(x, y, face)
    c = pt(o, n, t, 0.2)
    ax.add_patch(Rectangle((c[0] - 0.13, c[1] - 0.13), 0.26, 0.26, facecolor="white", edgecolor=C_SPEC, lw=1.6, zorder=6))
    ax.plot([c[0] - 0.13, c[0] + 0.13], [c[1] - 0.13, c[1] + 0.13], color=C_SPEC, lw=1.0, zorder=7)
    lx, ly = pt(o, n, t, 0.55)
    ax.text(lx, ly, label, color=C_SPEC, fontsize=5.4, ha="center", va="center", zorder=7, fontweight="bold", linespacing=0.95)


def com(ax, x, y, face, txt, color=C_COM):
    o, n, t = frame(x, y, face)
    c = pt(o, n, t, 0.18)
    ax.add_patch(Polygon([pt(o, n, t, 0.05, -0.15), pt(o, n, t, 0.05, 0.15), pt(o, n, t, 0.31, 0)],
                         closed=True, facecolor=color, edgecolor=color, zorder=6))
    lx, ly = pt(o, n, t, 0.48)
    ax.text(lx, ly, txt, color=color, fontsize=5.6, ha="center", va="center", fontweight="bold", zorder=7)


def lum(ax, x, y, r=0.17, color=C_LUM, label=None):
    ax.add_patch(Circle((x, y), r, facecolor="#fff3bf", edgecolor="#7a5c00", lw=1.3, zorder=6))
    d = r * 0.707
    ax.plot([x - d, x + d], [y - d, y + d], color="#7a5c00", lw=1.1, zorder=7)
    ax.plot([x - d, x + d], [y + d, y - d], color="#7a5c00", lw=1.1, zorder=7)
    if label:
        ax.text(x, y - r - 0.13, label, fontsize=5.2, ha="center", va="center", color="#7a5c00", zorder=7)


def applique(ax, x, y, face, label=None):
    o, n, t = frame(x, y, face)
    c = pt(o, n, t, 0.2)
    ax.plot(*zip(o, pt(o, n, t, 0.06)), color="#7a5c00", lw=1.2, zorder=6)
    lum(ax, c[0], c[1], r=0.13)
    if label:
        lx, ly = pt(o, n, t, 0.52)
        ax.text(lx, ly, label, fontsize=5.2, ha="center", va="center", color="#7a5c00", zorder=7)


def commande(ax, x, y, face, kind="S"):
    """S simple, D double allumage, V va-et-vient, B bouton poussoir, L voyant."""
    o, n, t = frame(x, y, face)
    c = pt(o, n, t, 0.16)
    if kind == "B":
        ax.add_patch(Circle(c, 0.09, facecolor="white", edgecolor=C_CMD, lw=1.3, zorder=6))
        ax.add_patch(Circle(c, 0.035, facecolor=C_CMD, edgecolor=C_CMD, zorder=7))
        return c
    ax.add_patch(Circle(c, 0.07, facecolor=C_CMD, edgecolor=C_CMD, zorder=6))
    if kind == "L":
        ax.add_patch(Circle(c, 0.035, facecolor="#ffd43b", edgecolor="none", zorder=7))
    d = pt((0, 0), n, t, 0.17, 0.10)
    lines = {"S": [0], "L": [0], "D": [-0.05, 0.05], "V": [0]}[kind]
    for s in lines:
        a = (c[0] + t[0] * s, c[1] + t[1] * s)
        ax.plot([a[0], a[0] + d[0]], [a[1], a[1] + d[1]], color=C_CMD, lw=1.2, zorder=6)
    if kind == "V":
        ax.plot([c[0], c[0] - d[0]], [c[1], c[1] - d[1]], color=C_CMD, lw=1.2, zorder=6)
    return c


def link(ax, a, b):
    ax.plot([a[0], b[0]], [a[1], b[1]], color="#868e96", lw=0.7, ls=(0, (3, 2)), zorder=5)


def daaf(ax, x, y):
    ax.add_patch(Circle((x, y), 0.13, facecolor="white", edgecolor=C_TAB, lw=1.3, zorder=6))
    ax.text(x, y, "D", color=C_TAB, fontsize=6, ha="center", va="center", fontweight="bold", zorder=7)


# ---------------------------------------------------------------- plan
def draw_plan(ax):
    ax.add_patch(Polygon(OUTER, closed=True, facecolor="#fbfbf8", edgecolor="none", zorder=0))
    ax.add_patch(Polygon([(11.64, 1.60), (14.04, 1.60), (14.04, 6.82), (12.44, 6.82), (12.44, 4.42), (11.64, 4.42)],
                         closed=True, facecolor="#eef3f6", edgecolor="#adb5bd", zorder=1, hatch="..", lw=0))
    for x1, y1, x2, y2 in SHAFTS:
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor="#e9ecef", edgecolor="#495057", lw=0.6, zorder=1))
        ax.plot([x1, x2], [y1, y2], color="#868e96", lw=0.6, zorder=1)
        ax.plot([x1, x2], [y2, y1], color="#868e96", lw=0.6, zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, "gaine", fontsize=5, ha="center", va="center", color="#495057",
                bbox=dict(fc="#e9ecef", ec="none", pad=0.5), zorder=2)

    for x1, y1, x2, y2, gaps in WALLS:
        horiz = y1 == y2
        a, b = (x1, x2) if horiz else (y1, y2)
        cuts = [a] + [v for g in sorted(gaps) for v in g] + [b]
        for s, e in zip(cuts[0::2], cuts[1::2]):
            if horiz:
                ax.add_patch(Rectangle((s - WALL / 2, y1 - WALL / 2), e - s + WALL, WALL, color="#212529", zorder=3, lw=0))
            else:
                ax.add_patch(Rectangle((x1 - WALL / 2, s - WALL / 2), WALL, e - s + WALL, color="#212529", zorder=3, lw=0))
    for x1, y1, x2, y2 in WINDOWS:
        if y1 == y2:
            ax.add_patch(Rectangle((x1, y1 - WALL / 2), x2 - x1, WALL, facecolor="#a5d8ff", edgecolor="#1c7ed6", lw=0.8, zorder=4))
        else:
            ax.add_patch(Rectangle((x1 - WALL / 2, y1), WALL, y2 - y1, facecolor="#a5d8ff", edgecolor="#1c7ed6", lw=0.8, zorder=4))
    for hx, hy, r, t1, t2 in DOORS:
        ax.add_patch(Arc((hx, hy), 2 * r, 2 * r, theta1=t1, theta2=t2, color="#868e96", lw=0.7, zorder=2))
        a = math.radians(t2 if t1 % 180 == 0 else t1)
        ax.plot([hx, hx + r * math.cos(a)], [hy, hy + r * math.sin(a)], color="#868e96", lw=0.7, zorder=2)

    for name, area, x, y in ROOMS:
        ax.text(x, y, name, fontsize=7 if name == "DÉGAGEMENT" else 8.5, ha="center", va="center", fontweight="bold", color="#343a40",
                zorder=2, bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.85) if name == "BALCON" else None)
        if area:
            ax.text(x, y - 0.27, area, fontsize=7, ha="center", va="center", color="#6c757d", zorder=2)

    # ---- Tableau / GTL (entrée, à côté de la porte palière)
    ax.add_patch(Rectangle((6.03, 0.28), 0.30, 1.05, facecolor=C_TAB, edgecolor="#7d1a1a", lw=1, zorder=6))
    ax.text(6.18, 0.80, "GTL", color="white", fontsize=5.6, rotation=90, ha="center", va="center", fontweight="bold", zorder=7)
    ax.annotate("Tableau électrique\n+ coffret de communication\n(GTL)", xy=(6.33, 0.80), xytext=(7.55, 0.80),
                fontsize=6.5, color=C_TAB, fontweight="bold", va="center", ha="left",
                arrowprops=dict(arrowstyle="-|>", color=C_TAB, lw=0.9))

    # ---- SÉJOUR : 8 PC, 2 RJ45, 1 TV
    for x in (6.65, 9.25, 11.2):
        prise(ax, x, 6.82, "S")
    prise(ax, 6.03, 4.55, "E")
    prise(ax, 6.03, 6.05, "E")
    com(ax, 6.03, 5.3, "E", "RJ45")
    prise(ax, 10.05, 4.42, "N", double=True)
    com(ax, 10.6, 4.42, "N", "RJ45")
    com(ax, 10.95, 4.42, "N", "TV")
    prise(ax, 12.05, 4.42, "N")
    s1 = (7.25, 5.3)
    s2 = (10.6, 5.45)
    lum(ax, *s1)
    lum(ax, *s2)
    v1 = commande(ax, 7.95, 3.63, "N", "V")
    v2 = commande(ax, 12.44, 4.66, "W", "V")
    link(ax, v1, s1)
    link(ax, s1, s2)
    link(ax, v2, s2)
    specialise(ax, 10.2, 6.82, "S", "CLIM\n(exist.)")

    # ---- BALCON : 1 PC étanche + 1 applique étanche, commande à voyant depuis le séjour
    prise(ax, 12.44, 6.62, "E", color="#0b7285", label="IP44")
    ap = (12.64, 4.62)
    applique(ax, 12.44, 4.62, "E", label="IP44")
    lv = commande(ax, 12.44, 4.30, "W", "L")
    link(ax, lv, ap)

    # ---- CHAMBRE 1 : 5 PC, 1 RJ45
    prise(ax, 0, 4.3, "E")
    prise(ax, 0, 6.2, "E")
    prise(ax, 0.95, 6.82, "S")
    com(ax, 0.55, 6.82, "S", "RJ45")
    prise(ax, 3.21, 5.0, "W")
    prise(ax, 3.21, 6.3, "W")
    c1 = (1.6, 5.0)
    lum(ax, *c1)
    link(ax, commande(ax, 2.18, 3.63, "N", "S"), c1)

    # ---- CHAMBRE 2 : 5 PC, 1 RJ45
    prise(ax, 3.21, 4.3, "E")
    prise(ax, 3.21, 6.2, "E")
    prise(ax, 5.35, 6.82, "S")
    com(ax, 5.75, 6.82, "S", "RJ45")
    prise(ax, 6.03, 4.1, "W")
    prise(ax, 6.03, 5.6, "W")
    c2 = (4.62, 5.0)
    lum(ax, *c2)
    link(ax, commande(ax, 4.25, 3.63, "N", "S"), c2)

    # ---- CUISINE : 6 PC + circuits spécialisés
    prise(ax, 9.05, 1.60, "N", double=True)
    prise(ax, 10.95, 1.60, "N", double=True)
    prise(ax, 9.25, 4.42, "S")
    prise(ax, 10.25, 4.42, "S")
    specialise(ax, 8.42, 2.05, "E", "FRIGO\n20A")
    specialise(ax, 9.55, 1.60, "N", "PLAQUE\n32A")
    specialise(ax, 10.3, 1.60, "N", "FOUR\n20A")
    specialise(ax, 11.4, 1.60, "N", "LV\n20A")
    specialise(ax, 11.2, 4.42, "S", "LL\n20A")
    specialise(ax, 9.55, 2.55, "N", "HOTTE")
    ax.plot([9.55, 9.55], [2.15, 2.62], color=C_SPEC, lw=0.6, ls=":", zorder=5)
    k = (9.75, 3.75)
    lum(ax, *k)
    app_pt = (10.4, 2.44)
    ax.add_patch(Rectangle((9.9, 2.4), 1.5, 0.08, facecolor="#ffe066", edgecolor="#7a5c00", lw=0.7, zorder=5))
    ax.text(10.65, 2.58, "éclairage plan de travail", fontsize=5, ha="center", color="#7a5c00", zorder=7)
    cd = commande(ax, 8.42, 3.45, "E", "D")
    link(ax, cd, k)
    link(ax, cd, app_pt)

    # ---- ENTRÉE + couloir : télérupteur 3 BP, 2 PC
    e1 = (5.82, 1.25)
    e2 = (7.45, 3.02)
    lum(ax, *e1)
    lum(ax, *e2)
    b1 = commande(ax, 5.40, 0, "N", "B")
    b2 = commande(ax, 8.25, 3.63, "S", "B")
    b3 = commande(ax, 5.22, 2.55, "E", "B")
    link(ax, b1, e1)
    link(ax, b3, e1)
    link(ax, b2, e2)
    link(ax, e1, e2)
    prise(ax, 5.22, 0.55, "E")
    prise(ax, 6.95, 2.42, "N")

    # ---- DÉGAGEMENT : 1 PC, éclairage en va-et-vient, détecteur de fumée
    d = (3.9, 3.0)
    lum(ax, *d)
    daaf(ax, 4.7, 3.0)
    ax.text(4.7, 2.75, "DAAF", fontsize=5, ha="center", color=C_TAB, zorder=7)
    vd1 = commande(ax, 5.22, 3.42, "W", "V")
    vd2 = commande(ax, 2.01, 2.45, "E", "V")
    link(ax, vd1, d)
    link(ax, vd2, d)
    prise(ax, 4.15, 2.42, "N")

    # ---- RANGEMENT
    r = (4.22, 1.2)
    lum(ax, *r)
    link(ax, commande(ax, 5.22, 0.95, "E", "S"), r)

    # ---- WC
    w = (2.61, 0.72)
    lum(ax, *w, r=0.13)
    link(ax, commande(ax, 3.0, 1.22, "N", "S"), w)

    # ---- SALLE DE BAINS (implantation hors volumes, à adapter au plan sanitaire)
    sb = (1.0, 1.85)
    lum(ax, *sb)
    applique(ax, 0.6, 0, "N")
    ax.text(0.9, 0.25, "applique miroir (classe II)", fontsize=4.8, ha="left", va="center", color="#7a5c00", zorder=7)
    cs = commande(ax, 2.01, 1.30, "E", "D")
    link(ax, cs, sb)
    link(ax, cs, (0.6, 0.2))
    prise(ax, 2.01, 2.45, "W", label="hors vol.")
    specialise(ax, 1.0, 2.81, "S", "SÈCHE-\nSERV.")

    ax.set_xlim(-0.6, 14.6)
    ax.set_ylim(-0.75, 7.35)
    ax.set_aspect("equal")
    ax.axis("off")


def legend(ax):
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.05, 0.05), 3.9, 11.9, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="white", edgecolor="#ced4da", lw=1))
    ax.text(2, 11.55, "LÉGENDE", fontsize=11, ha="center", fontweight="bold", color="#212529")
    rows = [
        (lambda a, x, y: prise(a, x - 0.2, y, "E"), "Prise de courant 16 A 2P+T"),
        (lambda a, x, y: prise(a, x - 0.15, y, "N", double=True), "Prise double 16 A 2P+T"),
        (lambda a, x, y: prise(a, x - 0.2, y, "E", color="#0b7285"), "Prise étanche IP44 (balcon)"),
        (lambda a, x, y: specialise(a, x - 0.2, y, "E", ""), "Circuit spécialisé / sortie de câble"),
        (lambda a, x, y: com(a, x - 0.2, y, "E", ""), "Prise RJ45 cat. 6 / prise TV"),
        (lambda a, x, y: lum(a, x, y), "Point lumineux plafond (DCL)"),
        (lambda a, x, y: applique(a, x - 0.2, y, "E"), "Applique murale (DCL)"),
        (lambda a, x, y: commande(a, x - 0.16, y, "E", "S"), "Interrupteur simple allumage"),
        (lambda a, x, y: commande(a, x - 0.16, y, "E", "D"), "Interrupteur double allumage"),
        (lambda a, x, y: commande(a, x - 0.16, y, "E", "V"), "Interrupteur va-et-vient"),
        (lambda a, x, y: commande(a, x - 0.16, y, "E", "L"), "Interrupteur à voyant"),
        (lambda a, x, y: commande(a, x - 0.16, y, "E", "B"), "Bouton poussoir (télérupteur)"),
        (lambda a, x, y: daaf(a, x, y), "Détecteur de fumée (DAAF)"),
        (lambda a, x, y: a.add_patch(Rectangle((x - 0.15, y - 0.2), 0.3, 0.4, color=C_TAB)), "Tableau électrique / GTL"),
        (lambda a, x, y: link(a, (x - 0.3, y), (x + 0.3, y)), "Liaison commande → éclairage"),
    ]
    y = 10.85
    for fn, txt in rows:
        fn(ax, 0.55, y)
        ax.text(1.05, y, txt, fontsize=7.4, va="center", color="#343a40")
        y -= 0.62
    ax.text(0.3, 1.25, "Abréviations : LV lave-vaisselle · LL lave-linge ·\nCLIM climatisation existante (à vérifier) ·\n"
            "hors vol. = hors volumes de la salle de bains",
            fontsize=6.3, va="center", color="#495057", linespacing=1.4)


def header(fig, subtitle):
    fig.text(0.03, 0.955, "MAUREL'EC", fontsize=20, fontweight="bold", color="#1f5fbf")
    fig.text(0.03, 0.932, "Électricité générale · maurelec.btp@gmail.com · 06 12 31 67 03", fontsize=8, color="#495057")
    fig.text(0.97, 0.958, "Plan d'implantation électrique – Avant-projet", fontsize=15, fontweight="bold", ha="right", color="#212529")
    fig.text(0.97, 0.935, subtitle, fontsize=9, ha="right", color="#495057")
    fig.add_artist(plt.Line2D([0.03, 0.97], [0.922, 0.922], color="#1f5fbf", lw=1.5))


def footer(fig, page):
    fig.text(0.03, 0.025, "Implantation indicative établie d'après le croquis du diagnostic (réf. 2139 C) – cotes non contractuelles. "
             "Positions définitives à valider avec le client lors de la visite et selon le plan de cuisine / salle de bains. "
             "Installation conforme NF C 15-100.", fontsize=6.6, color="#6c757d")
    fig.text(0.97, 0.025, f"Page {page}/2", fontsize=7, ha="right", color="#6c757d")


SUB = "Client : M. Augustin Fuentes · Appartement T3 ~68 m² · Nice Saint-Roch · Octobre 2026"


def page_plan(pdf):
    fig = plt.figure(figsize=(16.54, 11.69))
    header(fig, SUB)
    draw_plan(fig.add_axes([0.02, 0.08, 0.74, 0.83]))
    legend(fig.add_axes([0.775, 0.09, 0.2, 0.81]))
    fig.text(0.39, 0.115, "← façade / fenêtres en haut du plan · balcon à droite · palier en bas →", fontsize=7, ha="center", color="#868e96")
    footer(fig, 1)
    pdf.savefig(fig)
    plt.close(fig)


PIECES = [
    ("Séjour", "8", "–", "2 + 1 TV", "2 DCL (va-et-vient)", "Alim. clim existante à vérifier"),
    ("Chambre 1", "5", "–", "1", "1 DCL", ""),
    ("Chambre 2", "5", "–", "1", "1 DCL", ""),
    ("Cuisine", "6 (dont 4 sur plan de travail)", "Plaque 32A, four, LV, LL, frigo, hotte", "–", "1 DCL + plan de travail", "Positions selon plan cuisiniste"),
    ("Entrée / couloir", "2", "–", "–", "2 DCL (télérupteur, 3 BP)", "GTL : tableau + coffret com."),
    ("Dégagement", "1", "–", "–", "1 DCL (va-et-vient)", "Détecteur de fumée"),
    ("Salle de bains", "1 (hors volumes)", "Sèche-serviettes", "–", "1 DCL + applique miroir", "Liaison équipotentielle"),
    ("WC", "–", "–", "–", "1 DCL", ""),
    ("Rangement", "–", "–", "–", "1 DCL", ""),
    ("Balcon", "1 étanche IP44", "–", "–", "1 applique IP44 (voyant)", ""),
    ("TOTAL", "29 prises", "8 circuits", "4 RJ45 + 1 TV", "13 points lumineux", ""),
]

CIRCUITS = [
    ("ID1 · 63 A 30 mA type A", [
        ("1", "Plaque de cuisson induction", "32 A", "6 mm²"),
        ("2", "Lave-linge", "20 A", "2,5 mm²"),
        ("3", "Prises chambres 1 et 2 (10 PC)", "20 A", "2,5 mm²"),
        ("4", "Éclairage nuit (chambres, dégagement, SdB, WC, rangement)", "10 A", "1,5 mm²"),
        ("5", "Sèche-serviettes", "16 A", "1,5 mm²"),
    ]),
    ("ID2 · 40 A 30 mA type A", [
        ("6", "Four", "20 A", "2,5 mm²"),
        ("7", "Lave-vaisselle", "20 A", "2,5 mm²"),
        ("8", "Réfrigérateur", "20 A", "2,5 mm²"),
        ("9", "Prises cuisine plan de travail (6 PC)", "20 A", "2,5 mm²"),
        ("10", "Hotte", "16 A", "1,5 mm²"),
    ]),
    ("ID3 · 40 A 30 mA type A", [
        ("11", "Prises séjour (8 PC)", "20 A", "2,5 mm²"),
        ("12", "Prises entrée, dégagement, SdB, balcon (5 PC)", "20 A", "2,5 mm²"),
        ("13", "Éclairage jour (séjour, entrée, cuisine, balcon)", "10 A", "1,5 mm²"),
        ("14", "Climatisation (existante – à vérifier)", "20 A", "2,5 mm²"),
        ("15", "Coffret de communication (VDI)", "2 A", "1,5 mm²"),
    ]),
]


def table(ax, x, y, widths, rows, head, fs=8, rh=0.042, head_color="#1f5fbf"):
    cx = x
    for w, h in zip(widths, head):
        ax.add_patch(Rectangle((cx, y - rh), w, rh, facecolor=head_color, edgecolor="white", lw=1))
        ax.text(cx + 0.006, y - rh / 2, h, fontsize=fs, color="white", va="center", fontweight="bold")
        cx += w
    for i, row in enumerate(rows):
        yy = y - rh * (i + 2)
        bold = row[0] == "TOTAL"
        cx = x
        for w, val in zip(widths, row):
            ax.add_patch(Rectangle((cx, yy), w, rh, facecolor="#e7f0fd" if bold else ("#f8f9fa" if i % 2 else "white"),
                                   edgecolor="#dee2e6", lw=0.6))
            ax.text(cx + 0.006, yy + rh / 2, val, fontsize=fs, va="center", color="#212529",
                    fontweight="bold" if bold else "normal")
            cx += w
    return y - rh * (len(rows) + 1)


def page_recap(pdf):
    fig = plt.figure(figsize=(16.54, 11.69))
    header(fig, SUB)
    ax = fig.add_axes([0.03, 0.06, 0.94, 0.85])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0, 0.975, "1. Équipements par pièce", fontsize=13, fontweight="bold", color="#212529")
    end = table(ax, 0, 0.955, [0.13, 0.17, 0.22, 0.1, 0.18, 0.2], PIECES,
                ["Pièce", "Prises 16 A", "Circuits spécialisés", "RJ45 / TV", "Éclairage", "Remarques"], rh=0.033)

    y = end - 0.05
    ax.text(0, y, "2. Tableau électrique proposé (3 rangées · 13 modules, réserve ≥ 20 %)", fontsize=13, fontweight="bold", color="#212529")
    y -= 0.02
    col_x = [0, 0.335, 0.67]
    for (title, rows), cx in zip(CIRCUITS, col_x):
        ax.add_patch(Rectangle((cx, y - 0.04), 0.32, 0.04, facecolor=C_TAB, edgecolor="white"))
        ax.text(cx + 0.008, y - 0.02, title, fontsize=9, color="white", fontweight="bold", va="center")
        table(ax, cx, y - 0.04, [0.025, 0.205, 0.04, 0.05], rows, ["N°", "Circuit", "Disj.", "Section"],
              fs=7.2, rh=0.033, head_color="#495057")

    y -= 0.04 + 0.033 * 6 + 0.05
    ax.text(0, y, "3. Points complémentaires", fontsize=13, fontweight="bold", color="#212529")
    notes = [
        "Dépose / condamnation de l'ancienne installation (tableau à fusibles, goulottes apparentes).",
        "Distribution des circuits dans le faux plafond technique (6 à 8 cm) avec descentes encastrées dans les cloisons ; "
        "solutions discrètes (moulures / plinthes techniques) sur les murs béton.",
        "Mise à la terre : contrôle de la prise de terre et de la liaison équipotentielle principale ; liaison équipotentielle locale en salle de bains.",
        "Coffret de communication grade 2 TV dans la GTL : 4 prises RJ45 cat. 6 (séjour ×2, chambres ×1) + 1 prise TV.",
        "Repérage complet du tableau, essais (isolement, continuité, déclenchement des différentiels) et remise du schéma.",
        "Options possibles : prises USB en chevet, éclairage LED encastré en faux plafond, interrupteurs connectés, prise recharge balcon.",
    ]
    for n in notes:
        y -= 0.03
        ax.text(0.005, y, "•  " + n, fontsize=8.2, color="#343a40", va="top")
    footer(fig, 2)
    pdf.savefig(fig)
    plt.close(fig)


if __name__ == "__main__":
    with PdfPages(OUT) as pdf:
        page_plan(pdf)
        page_recap(pdf)
    print(OUT)
