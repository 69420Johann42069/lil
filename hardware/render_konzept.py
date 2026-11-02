#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konzept-Rendering des Spritzenpumpen-Turms aus den Maßen von spritzenpumpe.scad.

Nur matplotlib und Standardbibliothek. Schreibt rendering.png (1600 x 800 px)
neben dieses Skript. Variablennamen und Formeln folgen der SCAD-Datei.

Koordinaten wie in der SCAD-Datei: X mittig, Y = 0 hinten, Y+ nach vorne,
Z = 0 Tisch. Fuer die Darstellung wird das Modell um 180 Grad um Z gedreht
(x, y) -> (-x, -y), damit die Kameras azim = -50 und azim = 0 von vorne und
von der rechten Seite des Bedieners schauen (der Bediener steht bei Y+).
Das ist eine Drehung, keine Spiegelung.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ============================================================
# Variablen aus spritzenpumpe.scad
# ============================================================
stationen = 5
spiel = 0.3

# Spritze 60 ml
syr_zyl_d = 30
syr_flansch_b = 45      # lange Achse, liegt in Y
syr_flansch_t = 3
syr_flansch_h = 32      # kurze Achse, liegt in X
syr_stange_b = 12
syr_l = 90
kolben_d = 30
kolben_t = 4

# NEMA 17
nema_flansch = 42.3
nema_l = 40
nema_welle_l = 24

# Spindel, Mutter
sp_d = 8
mutter_flansch_d = 22
mutter_flansch_t = 3.5
mutter_koerper_d = 10.2
spindel_frei_d = 9.2

# Welle, Lager
welle_d = 8
welle_pass = 7.8
wellen_tiefe = 10
wellen_abstand = 22
lm_d = 15
lm_l = 24
lm_spiel = 0.2

# Kupplung
kupp_d = 19
kupp_l = 25
kupp_einschub = 12

# Endschalter
es_l = 20
es_b = 10
es_t = 6.5
es_y = 19
es_hub = 1
es_sitz = 2
nase_b = 5
nase_h = 8

# Station
station_abstand = 44
hub = 80

# Schale
schale_b = 200
schale_t = 90
schale_h = 35
schale_spiel = 2
duese_luft = 10
bp_t = 4
mulde_t = 1.5
mulde_spiel = 0.5
schale_motor_luft = 2.5
syr_abstand_platte = 3

# Sockel
sk_pl = 12
sk_wand = 3

# Schlitten
sl_wand = 2
sl_links = 8.4
lm_sitz_boden = 2
ar_boden = 3
ar_decke = 3
ar_wand = 3
ar_vorn = 10
ar_rippe_b = 18

# Spritzenhalter
sh_boden = 5
sh_decke = 3
sh_hinten = 4
sh_vorn = 20
sh_steg_b = 16
sh_rippe_b = 10
sh_rippe_h = 40
sh_klemm_wand = 6

# Kopf
kp_t = 10
kp_rand = 3
lager_d = 22
lager_t = 7

# ============================================================
# Abgeleitete Maße (gleiche Formeln wie in der SCAD-Datei)
# ============================================================
lm_bohr = lm_d + lm_spiel
wa = wellen_abstand


def sk_breite(n):
    return sk_xl + (n - 1) * station_abstand + sk_xr


def sx(i, n):
    return -sk_breite(n) / 2 + sk_xl + i * station_abstand


def xn(n):
    return (sx(0, n) + sx(n - 1, n)) / 2


def kp_breite(n):
    return (n - 1) * station_abstand + kp_links + kp_rechts


schacht_b = schale_b + 2 * schale_spiel
schacht_t = schale_t + 2 * schale_spiel
schale_z0 = bp_t - mulde_t
schale_ok = schale_z0 + schale_h
duese_z = schale_ok + duese_luft

sk_luft = schale_ok + schale_motor_luft
sk_h = sk_pl + nema_l + sk_luft
sk_fuehr_h = sk_luft - 1
sk_xl = nema_flansch / 2 + sk_wand + 0.5
sk_xr = max(sk_xl, wa + welle_pass / 2 + sk_wand)
y_a = nema_flansch / 2 + sk_wand + 0.5
sk_pt = y_a + nema_flansch / 2 + sk_wand
y_syr = sk_pt + syr_zyl_d / 2 + spiel + syr_abstand_platte
dy = y_syr - y_a
y_sch0 = y_syr - schacht_t / 2
sk_t = y_syr + schacht_t / 2

sl_rechts = wa + lm_bohr / 2 + sl_wand
sl_b = sl_links + sl_rechts
sl_huell = max(sl_links, mutter_flansch_d / 2) + sl_rechts
sl_t = max(lm_bohr + 2 * sl_wand, mutter_flansch_d + 2)
sl_h = 2 * lm_l + lm_sitz_boden + 1
ar_b = kolben_d + 2 * spiel + 2 * ar_wand
ar_h = ar_boden + kolben_t + 2 * spiel + ar_decke

sh_h = sh_boden + syr_flansch_t + spiel + sh_decke
sh_b = station_abstand - 4
kl_x0 = -(spindel_frei_d / 2 + 4)
kl_x1 = wa + welle_d / 2 + sh_klemm_wand
kl_y = welle_d / 2 + 4
sh_y_block = dy - syr_flansch_b / 2 - spiel - sh_hinten

kp_links = lager_d / 2 + 3
kp_rechts = wa + welle_pass / 2 + kp_rand
kp_wtiefe = kp_t - 2
ky0 = y_a - (lager_d / 2 + 4)
ky1 = y_a + es_y + es_b / 2 + 4

fl_z = duese_z + syr_l
sh_z0 = fl_z - sh_boden
hc_z = sh_z0 + sh_h
sl_z_min = hc_z + 1
sl_z_max = sl_z_min + hub
nase_oben = sl_z_max + sl_h + nase_h
kp_z0 = nase_oben + es_hub + es_t - es_sitz
turm_h = kp_z0 + kp_t

kupp_z0 = sk_h - sk_pl + nema_welle_l - kupp_l / 2
sp_z0 = kupp_z0 + kupp_l - kupp_einschub
sp_z1 = kp_z0 + lager_t - 1
w_z0 = sk_h - wellen_tiefe
w_z1 = kp_z0 + kp_wtiefe

# ============================================================
# Darstellungsparameter (nicht in der SCAD-Datei)
# ============================================================
HUB_ANTEIL = 0.5                  # Schlitten steht bei halbem Hub
sl_z = sl_z_min + HUB_ANTEIL * hub
KONUS_H = 20                      # Höhe von Düse und Konus an der Spritze (Annahme)
DUESE_D = 6                       # Düsendurchmesser (Annahme)
DUESE_L = 8                       # Länge des Düsenröhrchens (Annahme)
KOLBEN_GUMMI_H = 5                # Dicke des Gummikolbens (Annahme)
STANGE_DICKE = 2.5                # Kreuzprofil der Kolbenstange (Annahme)
WAND_SCHALE = 3                   # Wandstärke der Schale (Annahme)

FARBEN_REIHE = ["C", "M", "Y", "W", "K"]
INHALT = {"C": "#17b4e6", "M": "#d4237f", "Y": "#f3d21c", "W": "#fbfbfb", "K": "#1c1c1e"}

C_DRUCK = "#d2d2d2"       # Druckteile hellgrau
C_MOTOR = "#56565c"       # Motoren dunkelgrau
C_SILBER = "#c4c8cd"      # Spindel und Welle
C_SCHALE = "#eadfc5"      # Schale hellbeige
C_SCHLITTEN = "#8c8c8c"   # Kolbenschlitten mittelgrau
C_MESSING = "#c7ab6c"     # Flanschmutter
C_KUPPLUNG = "#7d8794"
C_SCHALTER = "#b4574b"
C_KOLBEN = "#ececec"
C_GUMMI = "#585c62"
C_GLAS = "#ffffff"

# ============================================================
# Geometrie: Flaechenliste (Modellkoordinaten, mm)
# ============================================================


class Face:
    __slots__ = ("v", "n", "rgb", "alpha", "glass", "tag")

    def __init__(self, v, n, rgb, alpha, glass, tag):
        self.v = v
        self.n = n
        self.rgb = rgb
        self.alpha = alpha
        self.glass = glass
        self.tag = tag


FACES = []
TAG = [""]


def _add(v, n, rgb, alpha=1.0, glass=False):
    FACES.append(Face(v, n, rgb, alpha, glass, TAG[0]))


def _tiles(a0, a1, tile):
    if not tile:
        return [(a0, a1)]
    k = max(1, math.ceil((a1 - a0) / tile - 1e-9))
    st = (a1 - a0) / k
    return [(a0 + j * st, a0 + (j + 1) * st) for j in range(k)]


def _face(fixed, val, ra, rb, n, rgb, alpha, glass, tile):
    axes = [0, 1, 2]
    axes.remove(fixed)
    ia, ib = axes
    for a0, a1 in _tiles(ra[0], ra[1], tile):
        for b0, b1 in _tiles(rb[0], rb[1], tile):
            verts = []
            for a, b in ((a0, b0), (a1, b0), (a1, b1), (a0, b1)):
                p = [0.0, 0.0, 0.0]
                p[fixed] = val
                p[ia] = a
                p[ib] = b
                verts.append(tuple(p))
            _add(verts, n, rgb, alpha, glass)


def box(x0, x1, y0, y1, z0, z1, color, alpha=1.0, glass=False, tile=None):
    rgb = to_rgb(color)
    for fixed, val, ra, rb, n in (
        (0, x1, (y0, y1), (z0, z1), (1, 0, 0)),
        (0, x0, (y0, y1), (z0, z1), (-1, 0, 0)),
        (1, y1, (x0, x1), (z0, z1), (0, 1, 0)),
        (1, y0, (x0, x1), (z0, z1), (0, -1, 0)),
        (2, z1, (x0, x1), (y0, y1), (0, 0, 1)),
        (2, z0, (x0, x1), (y0, y1), (0, 0, -1)),
    ):
        _face(fixed, val, ra, rb, n, rgb, alpha, glass, tile)


def revolve(cx, cy, profile, color, alpha=1.0, glass=False, n=32,
            cap_bottom=True, cap_top=True, zstep=None):
    """Drehkörper aus Polygonringen. profile = [(r, z), ...] von unten nach oben."""
    rgb = to_rgb(color)
    pts = []
    for (r0, z0), (r1, z1) in zip(profile[:-1], profile[1:]):
        k = 1
        if zstep and abs(z1 - z0) > zstep:
            k = math.ceil(abs(z1 - z0) / zstep)
        for j in range(k):
            f0, f1 = j / k, (j + 1) / k
            pts.append((r0 + (r1 - r0) * f0, z0 + (z1 - z0) * f0,
                        r0 + (r1 - r0) * f1, z0 + (z1 - z0) * f1, r1 - r0, z1 - z0))
    for ra, za, rb, zb, dr, dz in pts:
        ln = math.hypot(dr, dz) or 1.0
        nr, nz = dz / ln, -dr / ln
        for s in range(n):
            t0 = 2 * math.pi * s / n
            t1 = 2 * math.pi * (s + 1) / n
            tm = (t0 + t1) / 2
            v = [(cx + ra * math.cos(t0), cy + ra * math.sin(t0), za),
                 (cx + ra * math.cos(t1), cy + ra * math.sin(t1), za),
                 (cx + rb * math.cos(t1), cy + rb * math.sin(t1), zb),
                 (cx + rb * math.cos(t0), cy + rb * math.sin(t0), zb)]
            _add(v, (nr * math.cos(tm), nr * math.sin(tm), nz), rgb, alpha, glass)
    for (r, z, nz, on) in ((profile[0][0], profile[0][1], -1, cap_bottom),
                           (profile[-1][0], profile[-1][1], 1, cap_top)):
        if on and r > 0:
            v = [(cx + r * math.cos(2 * math.pi * s / n),
                  cy + r * math.sin(2 * math.pi * s / n), z) for s in range(n)]
            _add(v, (0, 0, nz), rgb, alpha, glass)


def cyl(cx, cy, r, z0, z1, color, alpha=1.0, glass=False, n=32, zstep=None,
        cap_bottom=True, cap_top=True):
    revolve(cx, cy, [(r, z0), (r, z1)], color, alpha, glass, n, cap_bottom, cap_top, zstep)


def prism(outline, z0, z1, color, alpha=1.0):
    """Gerades Prisma über einem (auch konkaven) Umriss in der XY-Ebene."""
    rgb = to_rgb(color)
    area = sum(outline[i][0] * outline[(i + 1) % len(outline)][1]
               - outline[(i + 1) % len(outline)][0] * outline[i][1]
               for i in range(len(outline)))
    pts = list(outline) if area > 0 else list(reversed(outline))
    m = len(pts)
    for i in range(m):
        p, q = pts[i], pts[(i + 1) % m]
        dx, dy_ = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy_)
        if ln < 1e-9:
            continue
        v = [(p[0], p[1], z0), (q[0], q[1], z0), (q[0], q[1], z1), (p[0], p[1], z1)]
        _add(v, (dy_ / ln, -dx / ln, 0), rgb, alpha)
    _add([(x, y, z1) for x, y in pts], (0, 0, 1), rgb, alpha)
    _add([(x, y, z0) for x, y in pts], (0, 0, -1), rgb, alpha)


def notch_outline(cx, xh, y0, y1, yc, r, k=14):
    """Rechteck x = cx +- xh, y0..y1 ohne Langloch (Radius r, Kreis bei yc, nach vorne offen)."""
    o = [(cx - xh, y0), (cx + xh, y0), (cx + xh, y1), (cx + r, y1), (cx + r, yc)]
    for s in range(1, k):
        t = math.pi * s / k
        o.append((cx + r * math.cos(t), yc - r * math.sin(t)))
    o += [(cx - r, yc), (cx - r, y1), (cx - xh, y1)]
    return o


def segments(z0, z1, excl):
    cur = [(z0, z1)]
    for e0, e1 in excl:
        nxt = []
        for a, b in cur:
            if e1 <= a or e0 >= b:
                nxt.append((a, b))
                continue
            if e0 > a:
                nxt.append((a, e0))
            if e1 < b:
                nxt.append((e1, b))
        cur = nxt
    return [(a, b) for a, b in cur if b - a > 1e-6]


# ============================================================
# Aufbau der Szene
# ============================================================
def build_sockel():
    sb = sk_breite(stationen)
    pxl = xn(stationen) - schacht_b / 2
    pxr = xn(stationen) + schacht_b / 2
    TAG[0] = "sockel"
    box(-sb / 2, sb / 2, 0, sk_wand, 0, sk_h, C_DRUCK, tile=10)                       # Rückwand
    box(-sb / 2, -sb / 2 + sk_wand, sk_wand, sk_pt, 0, sk_h, C_DRUCK, tile=10)        # Seitenwand links
    box(sb / 2 - sk_wand, sb / 2, sk_wand, sk_pt, 0, sk_h, C_DRUCK, tile=10)          # Seitenwand rechts
    box(-sb / 2 + sk_wand, sb / 2 - sk_wand, sk_wand, sk_pt, sk_h - sk_pl, sk_h, C_DRUCK, tile=10)  # Motorplatte
    # Führungswände neben dem Schacht
    box(-sb / 2 + sk_wand, pxl, sk_wand, sk_pt, 0, sk_fuehr_h, C_DRUCK, tile=10)
    box(-sb / 2, pxl, sk_pt, sk_t, 0, sk_fuehr_h, C_DRUCK, tile=10)
    box(pxr, sb / 2 - sk_wand, sk_wand, sk_pt, 0, sk_fuehr_h, C_DRUCK, tile=10)
    box(pxr, sb / 2, sk_pt, sk_t, 0, sk_fuehr_h, C_DRUCK, tile=10)

    # Bodenplatte mit Mulde
    TAG[0] = "bodenplatte"
    bw = schacht_b - 2 * spiel
    by0 = sk_wand + spiel
    bx0 = xn(stationen) - bw / 2
    bx1 = xn(stationen) + bw / 2
    by1 = sk_t - spiel
    mw = schale_b + 2 * mulde_spiel
    mx0 = xn(stationen) - mw / 2
    mx1 = xn(stationen) + mw / 2
    my0 = y_syr - schale_t / 2 - mulde_spiel
    box(bx0, bx1, by0, by1, 0, bp_t - mulde_t, C_DRUCK, tile=10)
    box(bx0, bx1, by0, my0, bp_t - mulde_t, bp_t, C_DRUCK, tile=10)          # hinterer Anschlag
    box(bx0, mx0, my0, by1, bp_t - mulde_t, bp_t, C_DRUCK)                   # Randstreifen links
    box(mx1, bx1, my0, by1, bp_t - mulde_t, bp_t, C_DRUCK)                   # Randstreifen rechts

    # Schale als offene Wanne
    TAG[0] = "schale"
    sx0 = xn(stationen) - schale_b / 2
    sx1 = xn(stationen) + schale_b / 2
    sy0 = y_syr - schale_t / 2
    sy1 = y_syr + schale_t / 2
    w = WAND_SCHALE
    box(sx0, sx1, sy0, sy0 + w, schale_z0, schale_ok, C_SCHALE, tile=10)
    box(sx0, sx1, sy1 - w, sy1, schale_z0, schale_ok, C_SCHALE, tile=10)
    box(sx0, sx0 + w, sy0 + w, sy1 - w, schale_z0, schale_ok, C_SCHALE, tile=10)
    box(sx1 - w, sx1, sy0 + w, sy1 - w, schale_z0, schale_ok, C_SCHALE, tile=10)
    box(sx0 + w, sx1 - w, sy0 + w, sy1 - w, schale_z0, schale_z0 + w, C_SCHALE, tile=10)


def build_station(i):
    X = sx(i, stationen)
    Ya = y_a
    Ys = y_syr
    lab = FARBEN_REIHE[(stationen - 1 - i) % len(FARBEN_REIHE)]   # von vorne links nach rechts C M Y W K
    pre = "st%d_" % i

    # --- Motor unter der Platte, Kupplung
    TAG[0] = pre + "motor"
    h = nema_flansch / 2
    box(X - h, X + h, Ya - h, Ya + h, sk_h - sk_pl - nema_l, sk_h - sk_pl, C_MOTOR, tile=10)
    TAG[0] = pre + "kupplung"
    cyl(X, Ya, kupp_d / 2, kupp_z0, kupp_z0 + kupp_l, C_KUPPLUNG)

    # --- Höhen von Schlitten und Spritzenhalter
    sl_top = sl_z + sl_h + mutter_flansch_t
    ex_halter = (sh_z0, hc_z)
    ex_schlitten = (sl_z, sl_top)
    ex_kopf = (kp_z0, turm_h)

    # --- Spindel und Welle (nur dort, wo sie sichtbar sind)
    TAG[0] = pre + "spindel"
    for a, b in segments(kupp_z0 + kupp_l, sp_z1, [ex_halter, ex_schlitten, ex_kopf]):
        cyl(X, Ya, sp_d / 2, a, b, C_SILBER, n=24, zstep=20)
    TAG[0] = pre + "welle"
    for a, b in segments(sk_h, w_z1, [ex_halter, ex_schlitten, ex_kopf]):
        cyl(X + wa, Ya, welle_d / 2, a, b, C_SILBER, n=24, zstep=20)

    # --- Spritzenhalter (lokal um die Spindelachse, Z ab sh_z0)
    TAG[0] = pre + "halter"
    z0 = sh_z0
    y_pb = dy - syr_flansch_b / 2 - spiel
    y_b0 = y_pb - sh_hinten
    y_b1 = dy + sh_vorn
    tw = syr_flansch_h / 2 + spiel
    box(X + kl_x0, X + kl_x1, Ya - kl_y, Ya + kl_y, z0, z0 + sh_h, C_DRUCK)               # Wellenklemme
    box(X - sh_steg_b / 2, X + sh_steg_b / 2, Ya + kl_y, Ya + y_b0, z0, z0 + sh_h, C_DRUCK)  # Steg
    box(X - sh_rippe_b / 2, X + sh_rippe_b / 2, Ya + kl_y, Ya + y_b0, z0 - sh_rippe_h, z0, C_DRUCK)  # Tragrippe
    prism([(X + px, Ya + py) for px, py in
           notch_outline(0, sh_b / 2, y_b0, y_b1, dy, syr_zyl_d / 2 + spiel)],
          z0, z0 + sh_boden, C_DRUCK)                                                     # Boden mit Zylinderschlitz
    box(X - sh_b / 2, X + sh_b / 2, Ya + y_b0, Ya + y_pb, z0 + sh_boden,
        z0 + sh_boden + syr_flansch_t + spiel, C_DRUCK)                                  # Rückwand der Flanschtasche
    for sgn in (-1, 1):                                                                  # Seitenwände der Tasche
        xa, xb = sorted((sgn * tw, sgn * sh_b / 2))
        box(X + xa, X + xb, Ya + y_pb, Ya + y_b1, z0 + sh_boden,
            z0 + sh_boden + syr_flansch_t + spiel, C_DRUCK)
    prism([(X + px, Ya + py) for px, py in
           notch_outline(0, sh_b / 2, y_b0, y_b1, dy, syr_stange_b / 2 + spiel)],
          z0 + sh_boden + syr_flansch_t + spiel, z0 + sh_h, C_DRUCK)                     # Decke mit Stangenschlitz

    # --- Schlitten
    TAG[0] = pre + "schlitten"
    y_p0 = dy - (kolben_d / 2 + spiel + ar_wand)
    box(X - sl_links, X + sl_rechts, Ya - sl_t / 2, Ya + sl_t / 2, sl_z, sl_z + sl_h, C_SCHLITTEN)
    box(X - ar_rippe_b / 2, X + ar_rippe_b / 2, Ya + sl_t / 2, Ya + y_p0, sl_z, sl_z + sl_h, C_SCHLITTEN)
    prism([(X + px, Ya + py) for px, py in
           notch_outline(0, ar_b / 2, y_p0, dy + ar_vorn, dy, syr_stange_b / 2 + spiel)],
          sl_z, sl_z + ar_boden, C_SCHLITTEN)                                            # Boden mit Stangenschlitz
    prism([(X + px, Ya + py) for px, py in
           notch_outline(0, ar_b / 2, y_p0, dy + ar_vorn, dy, kolben_d / 2 + spiel)],
          sl_z + ar_boden, sl_z + ar_boden + kolben_t + 2 * spiel, C_SCHLITTEN)          # U-Aufnahme
    box(X - ar_b / 2, X + ar_b / 2, Ya + y_p0, Ya + dy + ar_vorn,
        sl_z + ar_h - ar_decke, sl_z + ar_h, C_SCHLITTEN)                                # Decke
    box(X - nase_b / 2, X + nase_b / 2, Ya + es_y - nase_b / 2, Ya + es_y + nase_b / 2,
        sl_z + sl_h, sl_z + sl_h + nase_h, C_SCHLITTEN)                                  # Schaltnase
    TAG[0] = pre + "mutter"
    cyl(X, Ya, mutter_flansch_d / 2, sl_z + sl_h, sl_z + sl_h + mutter_flansch_t, C_MESSING, n=32)

    # --- Spritze (Zylinder halbtransparent, Inhalt farbig)
    plate_z0 = sl_z + ar_boden + spiel
    zp = plate_z0 - (fl_z + syr_flansch_t - (duese_z + KONUS_H))   # Unterkante Gummikolben
    inhalt = INHALT[lab]
    TAG[0] = pre + "inhalt"
    revolve(X, Ys, [(DUESE_D / 2 - 0.8, duese_z), (DUESE_D / 2 - 0.8, duese_z + DUESE_L),
                    (syr_zyl_d / 2 - 1, duese_z + KONUS_H), (syr_zyl_d / 2 - 1, zp)],
            inhalt, n=36)
    TAG[0] = pre + "kolben"
    cyl(X, Ys, syr_zyl_d / 2 - 1, zp, zp + KOLBEN_GUMMI_H, C_GUMMI, n=36)
    TAG[0] = pre + "stange"
    box(X - syr_stange_b / 2, X + syr_stange_b / 2, Ys - STANGE_DICKE / 2, Ys + STANGE_DICKE / 2,
        zp + KOLBEN_GUMMI_H, plate_z0, C_KOLBEN, tile=14)
    box(X - STANGE_DICKE / 2, X + STANGE_DICKE / 2, Ys - syr_stange_b / 2, Ys + syr_stange_b / 2,
        zp + KOLBEN_GUMMI_H, plate_z0, C_KOLBEN, tile=14)
    TAG[0] = pre + "kolbenplatte"
    cyl(X, Ys, kolben_d / 2, plate_z0, plate_z0 + kolben_t, C_KOLBEN, n=36)
    TAG[0] = pre + "spritze"
    revolve(X, Ys, [(DUESE_D / 2, duese_z), (DUESE_D / 2, duese_z + DUESE_L),
                    (syr_zyl_d / 2, duese_z + KONUS_H), (syr_zyl_d / 2, fl_z)],
            C_GLAS, alpha=0.30, glass=True, n=36, cap_top=False)
    box(X - syr_flansch_h / 2, X + syr_flansch_h / 2, Ys - syr_flansch_b / 2, Ys + syr_flansch_b / 2,
        fl_z, fl_z + syr_flansch_t, C_GLAS, alpha=0.45, glass=True)

    # --- Endschalter unter dem Kopf
    TAG[0] = pre + "schalter"
    box(X - es_l / 2, X + es_l / 2, Ya + es_y - es_b / 2, Ya + es_y + es_b / 2,
        kp_z0 - (es_t - es_sitz), kp_z0, C_SCHALTER)


def build_kopf():
    TAG[0] = "kopf"
    x0 = sx(0, stationen) - kp_links
    x1 = sx(stationen - 1, stationen) + kp_rechts
    box(x0, x1, ky0, ky1, kp_z0, kp_z0 + kp_t, C_DRUCK, tile=10)


def build_scene():
    build_sockel()
    for i in range(stationen):
        build_station(i)
    build_kopf()


# ============================================================
# Kontrolle der Geometrie (Konsole)
# ============================================================
def bbox(prefixes):
    pts = [p for f in FACES if any(f.tag.endswith(s) or f.tag == s for s in prefixes) for p in f.v]
    xs, ys, zs = zip(*pts)
    return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))


def selfcheck():
    zmin = min(p[2] for f in FACES for p in f.v)
    zmax = max(p[2] for f in FACES for p in f.v)
    ymin = min(p[1] for f in FACES for p in f.v)
    ymax = max(p[1] for f in FACES for p in f.v)
    xmin = min(p[0] for f in FACES for p in f.v)
    xmax = max(p[0] for f in FACES for p in f.v)
    print("Turmhoehe %.2f, Sockel %.2f x %.2f, Gesamt B %.2f T %.2f H %.2f" %
          (turm_h, sk_breite(stationen), sk_t, xmax - xmin, ymax - ymin, zmax - zmin))
    print("z_min aller Flaechen %.2f (Tisch = 0), y_min %.2f" % (zmin, ymin))
    sx0 = xn(stationen) - schale_b / 2
    sx1 = xn(stationen) + schale_b / 2
    sy0 = y_syr - schale_t / 2
    sy1 = y_syr + schale_t / 2
    for i in range(stationen):
        (xa, xb), (ya, yb), (za, zb) = bbox(["st%d_inhalt" % i])
        cx = sx(i, stationen)
        ok = sx0 < cx < sx1 and sy0 < y_syr < sy1 and za >= schale_ok
        print("Spritze %d: Duese x=%.1f y=%.1f z=%.1f, ueber Schale (x %.1f..%.1f, y %.1f..%.1f, OK %.1f): %s"
              % (i, cx, y_syr, za, sx0, sx1, sy0, sy1, schale_ok, "ja" if ok else "NEIN"))
        (_, _), (_, _), (pz0, pz1) = bbox(["st%d_kolbenplatte" % i])
        (_, _), (_, _), (sz0, sz1) = bbox(["st%d_schlitten" % i])
        print("   Kolbenplatte z %.1f..%.1f, Schlitten-Aufnahme z %.1f..%.1f (Boden Oberkante %.1f, Decke Unterkante %.1f)"
              % (pz0, pz1, sl_z, sl_z + ar_h, sl_z + ar_boden, sl_z + ar_h - ar_decke))


# ============================================================
# Darstellung
# ============================================================
def vnorm(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


def vdot(a, b):
    return sum(x * y for x, y in zip(a, b))


def M(p):
    """Modell -> Plot: Drehung um 180 Grad um Z."""
    return (-p[0], -p[1], p[2])


def collection_for(elev, azim):
    e, a = math.radians(elev), math.radians(azim)
    c = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
    r = (-math.sin(a), math.cos(a), 0.0)
    u = (-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e))
    light = vnorm(tuple(0.62 * c[k] + 0.50 * u[k] - 0.45 * r[k] for k in range(3)))
    polys, fcs, ecs = [], [], []
    for f in FACES:
        n = M(f.n)
        if not f.glass and vdot(n, c) <= 1e-9:
            continue                                   # abgewandte Flächen geschlossener Körper
        k = 0.58 + 0.42 * max(0.0, vdot(n, light))
        col = tuple(min(1.0, ch * k) for ch in f.rgb)
        polys.append([M(p) for p in f.v])
        if f.glass:
            fcs.append(col + (f.alpha,))
            ecs.append((0.55, 0.58, 0.63, 0.55))
        else:
            fcs.append(col + (1.0,))
            ecs.append(tuple(ch * 0.90 for ch in col) + (1.0,))
    coll = Poly3DCollection(polys, facecolors=fcs, edgecolors=ecs, linewidths=0.25)
    return coll


def breite_gesamt():
    n = stationen
    x_min = min(-sk_breite(n) / 2, sx(0, n) + min(kl_x0, -sl_links, -mutter_flansch_d / 2, -kp_links))
    x_max = max(sk_breite(n) / 2, sx(n - 1, n) + max(kl_x1, sl_rechts, kp_rechts))
    return x_max - x_min


def fmt(v):
    return ("%.1f" % v).replace(".", ",")


def dim_line(ax, p0, p1, tick, label, lab_pos, rot=0):
    q0, q1 = M(p0), M(p1)
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], [q0[2], q1[2]], color="#3a3f47", lw=0.9, zorder=50)
    for q in (p0, p1):
        a = M((q[0] - tick[0], q[1] - tick[1], q[2] - tick[2]))
        b = M((q[0] + tick[0], q[1] + tick[1], q[2] + tick[2]))
        ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color="#3a3f47", lw=0.9, zorder=50)
    t = M(lab_pos)
    ax.text(t[0], t[1], t[2], label, fontsize=9, ha="center", va="center", color="#1f2329",
            zorder=51, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.9))


def make_view(fig, rect, elev, azim, titel, zoom, mit_breite):
    ax = fig.add_axes(rect, projection="3d")
    ax.set_proj_type("ortho")
    ax.view_init(elev=elev, azim=azim)
    ax.add_collection3d(collection_for(elev, azim))

    sb = sk_breite(stationen)
    XA, XB = -sb / 2 - 34, sb / 2 + 34
    YA, YB = -6, sk_t + 34
    ZA, ZB = -20, turm_h + 12
    ax.set_xlim(-XB, -XA)
    ax.set_ylim(-YB, -YA)
    ax.set_zlim(ZA, ZB)
    ax.set_box_aspect((XB - XA, YB - YA, ZB - ZA), zoom=zoom)
    ax.set_axis_off()

    xd = -sb / 2 - 16          # Seite zum Betrachter (rechte Seite des Bedieners)
    yd = sk_t + 16             # Front
    if mit_breite:
        dim_line(ax, (-sb / 2, yd, 0), (sb / 2, yd, 0), (0, 4, 0),
                 "Breite " + fmt(sb) + " mm (Sockel)", (0, yd, -11))
    dim_line(ax, (xd, 0, 0), (xd, sk_t, 0), (4, 0, 0),
             "Tiefe " + fmt(sk_t) + " mm", (xd, sk_t / 2, -11))
    xh = sb / 2 + 16           # Höhenmaß auf der freien Seite (Bedienerseite links)
    dim_line(ax, (xh, yd, 0), (xh, yd, turm_h), (4, 0, 0),
             "Höhe " + fmt(turm_h) + " mm", (xh, yd, turm_h / 2))
    fig.text(rect[0] + rect[2] / 2, rect[1] + rect[3] + 0.012, titel, ha="center", va="bottom",
             fontsize=11, color="#2b3036")
    return ax


def main():
    build_scene()
    selfcheck()
    fig = plt.figure(figsize=(16, 8), dpi=100, facecolor="white")
    fig.suptitle("Farbmischer, Konzept-Rendering aus den SCAD-Maßen", fontsize=16,
                 fontweight="bold", y=0.975, color="#1f2329")
    make_view(fig, [0.0, 0.09, 0.5, 0.80], 25, -50,
              "Isometrisch von vorne oben (elev 25, azim -50)", 1.22, True)
    make_view(fig, [0.5, 0.09, 0.5, 0.80], 0, 0,
              "Seitenansicht von rechts (elev 0, azim 0)", 1.45, False)

    sb = sk_breite(stationen)
    fig.text(0.5, 0.058,
             "Gesamt: Breite %s mm (Sockel; %s mm mit Wellenklemme), Tiefe %s mm, Höhe %s mm   |   Kopfplatte %s mm breit, "
             "Düsen %s mm über dem Tisch, Schlitten bei halbem Hub (%s mm)"
             % (fmt(sb), fmt(breite_gesamt()), fmt(sk_t), fmt(turm_h), fmt(kp_breite(stationen)), fmt(duese_z),
                fmt(hub * HUB_ANTEIL)),
             ha="center", va="center", fontsize=10, color="#1f2329")
    fig.text(0.5, 0.030,
             "Spritzen von vorne links nach rechts: Cyan, Magenta, Gelb, Weiß, Schwarz   |   "
             "Vereinfachte Körper: ohne Bohrungen, Lager, Schrauben und Kabelkanal, Schale als offene Wanne, Ansicht von rechts = Bedienerseite",
             ha="center", va="center", fontsize=8.5, color="#59606a")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rendering.png")
    fig.savefig(out, dpi=100, facecolor="white")
    print("geschrieben:", out)


if __name__ == "__main__":
    main()
