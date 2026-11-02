#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konzept-Rendering des Farbmischer-Revolvers nach revolver_parameter.md (Stand 2).

Nur numpy, matplotlib und Standardbibliothek. Für Mesh-Bausteine und den Z-Buffer-Rasterizer wird
render_saeule.py importiert (die Datei bleibt unverändert, es wird kein Bytecode geschrieben).

Aufruf:  python3 render_revolver.py              -> rendering_revolver.png (1800 x 900)
         python3 render_revolver.py --pruefung   -> nur Maß- und Kollisionsprüfung auf der Konsole

Modell: Z nach oben, Z = 0 Tischplatte, Winkel 0 Grad (Fenster, aktive Station) liegt auf +X.
Stationsfenster: lokal x = radial nach außen, y = tangential (+ gegen den Uhrzeigersinn von oben), z = Welt-Z.

Annahmen, wo das Blatt nichts festlegt (nur Darstellung):
  - Kolbenstange 125 lang, Stopfen 5, Platte 4 dick; Flanschmutter Ø16 im Block; Endschalter mit Nase am Schlitten
  - Brücke Ø164 liegt 3 mm innerhalb der Schale, zwischen Oberschale (Z 418) und Haube (Z 426) ist der Brückenrand sichtbar
  - Abtropfring als C-Ring r 22 bis 80, Oberkante Z 90, Winkelbereich 41 bis 319 Grad
  - In Ansicht 2 sind die Schalen nur als gestrichelte Kontur angedeutet
"""
import math
import os
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import render_saeule as rs          # Mesh, cyl, box, revolve, shell_surface, ring_prism, View, render_panel, Scene, Frame

# ============================================================
# Maße aus revolver_parameter.md, Stand 2 (mm)
# ============================================================
R_A, WAND = 85.0, 2.4                              # Schalen Ø170
R_I = R_A - WAND                                   # 82,6
FUSS_D, FUSS_H = 185.0, 25.0
Z_BODEN = 30.0
Z_SOCKEL1, Z_MITTE1 = 120.0, 300.0                 # Mittelschale Z 120..300, Oberschale 300..418 (zwei Teile)
Z_RING0, Z_RING1, RING_R = 245.0, 259.0, 80.0      # Karussellplatte Ø160 (gerändelt, messingfarben)
SLOT_Z, SLOT_B, SLOT_W = (242.0, 262.0), 60.0, -60.0   # Daumenschlitz 20 hoch x 60 breit bei -60 Grad
Z_OBER1 = 418.0
Z_BR0, Z_BR1, BR_R = 418.0, 426.0, 82.0            # Brücke Ø164
Z_MOT0, Z_MOT1, NEMA = 426.0, 466.0, 42.3
Z_HAUBE0, Z_HAUBE1 = 426.0, 480.0                  # Haube Ø170 über Motor und Brücke
FENSTER_B, FENSTER_H, FENSTER_Z0, RAHMEN_B = 70.0, 80.0, 28.0, 4.0
BECHER_D, BECHER_H, BECHER_Z0, BECHERRAUM_D = 60.0, 60.0, 30.0, 64.0
Z_DUESE = 105.0
ST_R = 50.0
ST_WINKEL = [0, 72, 144, 216, 288]
ST_NAMEN = ["C", "M", "Y", "W", "K"]
ZYL_D = 30.0
FL_R, FL_T = 32.0, 45.0                            # Flansch radial 32, tangential 45
TA_R, TA_T, TA_TIEF, DURCHLASS_D, LOCH_D = 32.6, 45.6, 3.6, 31.0, 40.0
Z_TASCHE = Z_RING1 - TA_TIEF                       # 255,4 Taschenboden
Z_FL0, Z_FL1 = Z_TASCHE, Z_TASCHE + 3.0            # Flansch 3 dick, sitzt im Taschenboden
STOP_T, ROD_L, PL_T, PL_D = 5.0, 125.0, 4.0, 30.0
PB_STAND = {"C": 340.0, "M": 324.0, "Y": 301.0, "W": 336.0, "K": 313.0}   # Kolbenplatte Unterkante (voll = 340, Oberkante 344)
SPINDEL_Y, WELLE_Y, WS_D = 20.0, -20.0, 8.0
SPINDEL_Z, WELLE_Z = (262.0, 400.0), (262.0, 424.0)
KUPP_Z, KUPP_D = (393.0, 418.0), 19.0
STEMPEL_D, STEMPEL_Z = 26.0, (346.0, 361.0)        # Stempel oben (Stand oberste Stellung), Hub 96
SL_BLOCK = (-11.0, 11.0, -28.0, 28.0, 361.0, 391.0)   # x0, x1, y0, y1, z0, z1 (tangential 56)
HUB = 96.0
AUSS_D = 50.0                                      # Brückenaussparungen Ø50 nur bei 144, 216, 288
AUSS_WINKEL = [144, 216, 288]
MOTOR_Y = SPINDEL_Y                                # Motor über der Spindel

C_CREME, C_CREME_IN = "#efe6d0", "#d9cfb6"
C_DUNKEL, C_MESSING = "#4b4e54", "#c9a64e"
INHALT = {"C": "#17b4e6", "M": "#d4237f", "Y": "#f3d21c", "W": "#f4f2ec", "K": "#1c1c1e"}


# ============================================================
# 2D-Geometrie für die Prüfung (exakt: Polygone und Kreise)
# ============================================================
def _er(a):
    t = math.radians(a)
    return np.array([math.cos(t), math.sin(t)])


def _et(a):
    t = math.radians(a)
    return np.array([-math.sin(t), math.cos(t)])


def rect(a, dr, dt, hr, ht):
    """Rechteck im Stationssystem der Station a: Mitte bei Radius ST_R + dr, tangential dt, Halbmaße hr, ht."""
    c = (ST_R + dr) * _er(a) + dt * _et(a)
    er, et = _er(a), _et(a)
    return ("P", np.array([c - hr * er - ht * et, c + hr * er - ht * et, c + hr * er + ht * et, c - hr * er + ht * et]))


def circ(a, dr, dt, R):
    return ("C", (ST_R + dr) * _er(a) + dt * _et(a), R)


def _seg_dist(p, a, b):
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1)
    return float(np.linalg.norm(p - (a + t * ab)))


def _poly_sdf(p, P):
    n = len(P)
    inside, dmax = True, -1e18
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        e = b - a
        nrm = np.array([e[1], -e[0]]) / np.linalg.norm(e)      # nach außen (CCW)
        d = float(np.dot(p - a, nrm))
        dmax = max(dmax, d)
    if dmax <= 0:
        return dmax
    return min(_seg_dist(p, P[i], P[(i + 1) % n]) for i in range(n))


def _pp_gap(P, Q):
    best = -1e18
    for A, B in ((P, Q), (Q, P)):
        n = len(A)
        for i in range(n):
            a, b = A[i], A[(i + 1) % n]
            e = b - a
            nrm = np.array([e[1], -e[0]]) / np.linalg.norm(e)
            sep = min(float(np.dot(v - a, nrm)) for v in B)
            best = max(best, sep)
    if best <= 0:
        return best
    d = 1e18
    for A, B in ((P, Q), (Q, P)):
        for v in A:
            for i in range(len(B)):
                d = min(d, _seg_dist(v, B[i], B[(i + 1) % len(B)]))
    return d


def gap2(A, B):
    """Abstand zweier 2D-Formen; negativ = Durchdringung (Tiefe der kleinsten Verschiebung)."""
    if A[0] == "C" and B[0] == "C":
        return float(np.linalg.norm(A[1] - B[1])) - A[2] - B[2]
    if A[0] == "C":
        return _poly_sdf(A[1], B[1]) - A[2]
    if B[0] == "C":
        return _poly_sdf(B[1], A[1]) - B[2]
    return _pp_gap(A[1], B[1])


def f(x, n=2):
    return ("%+." + str(n) + "f") % x


def hole_gap(shape, a, R):
    """Luft einer Form in einer runden Aussparung (Radius R, Mitte auf der Stationsachse a); negativ = ragt über den Rand."""
    if shape[0] == "C":
        return R - (float(np.linalg.norm(shape[1] - ST_R * _er(a))) + shape[2])
    return R - max(float(np.linalg.norm(v - ST_R * _er(a))) for v in shape[1])


def pruefung():
    print("=" * 88)
    print("PRÜFUNG nach revolver_parameter.md, Stand 2  (Maße in mm, negativ = Kollision, nichts wird behoben)")
    print("=" * 88)
    sehne = 2 * ST_R * math.sin(math.radians(36))
    g = gap2(circ(0, 0, 0, ZYL_D / 2), circ(72, 0, 0, ZYL_D / 2))
    print("[1] Luft zwischen Spritzenzylindern Ø%.0f: Sehne %.2f, Luft %s  (Blatt: Sehne 58,8, 29)" % (ZYL_D, sehne, f(g)))
    fl = lambda a: rect(a, 0, 0, FL_R / 2, FL_T / 2)
    tasche = lambda a: rect(a, 0, 0, TA_R / 2, TA_T / 2)
    print("[2] Luft zwischen Flanschen %.0f x %.0f (tangential, Eckenrechnung exakt): 72° versetzt %s, 144° versetzt %s"
          "  (Blatt: gedreht 2,9)" % (FL_T, FL_R, f(gap2(fl(0), fl(72))), f(gap2(fl(0), fl(144)))))
    print("    Flanschtaschen %.1f x %.1f untereinander (72°): %s (Blatt: 2,2);  Flansch in Tasche: je Seite %.1f tangential, %.1f radial"
          % (TA_T, TA_R, f(gap2(tasche(0), tasche(72))), (TA_T - FL_T) / 2, (TA_R - FL_R) / 2))
    r_becher = ST_R + BECHER_D / 2
    print("[3] Becher Ø%.0f unter Station bei Radius %.0f: Außenkante bei Radius %.1f gegen Schaleninnenradius %.1f: Luft %s"
          "   (Becherraum Ø%.0f, Außenkante %.0f: %s)" % (BECHER_D, ST_R, r_becher, R_I, f(R_I - r_becher),
                                                          BECHERRAUM_D, ST_R + BECHERRAUM_D / 2, f(R_I - ST_R - BECHERRAUM_D / 2)))
    motor = rect(0, 0, MOTOR_Y, NEMA / 2, NEMA / 2)
    kupp = circ(0, 0, MOTOR_Y, KUPP_D / 2)
    stempel = circ(0, 0, 0, STEMPEL_D / 2)
    x0, x1, y0, y1, bz0, bz1 = SL_BLOCK
    block = rect(0, (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2)
    spindel = circ(0, 0, SPINDEL_Y, WS_D / 2)
    welle = circ(0, 0, WELLE_Y, WS_D / 2)
    plat0 = circ(0, 0, 0, PL_D / 2)

    def teile(a):
        return {"Flansch": rect(a, 0, 0, FL_R / 2, FL_T / 2), "Zylinder": circ(a, 0, 0, ZYL_D / 2),
                "Kolbenplatte": circ(a, 0, 0, PL_D / 2)}

    print("[4] Einsetzen von oben (Spritze mit Flansch %.0f x %.0f, Kolben hochgezogen bis Z 344, senkrecht nach oben durch die "
          "Brückenaussparung Ø%.0f;" % (FL_T, FL_R, AUSS_D))
    print("    der Hubweg überstreicht Z 255 bis über %.0f, also Kupplung Z %.0f..%.0f und Motor Z %.0f..%.0f; Prüfung im Grundriss)"
          % (Z_BR1, KUPP_Z[0], KUPP_Z[1], Z_MOT0, Z_MOT1))
    allmin = 1e9
    for a in AUSS_WINKEL:
        t = teile(a)
        z = {(tn, bn): gap2(t[tn], b) for tn in t for bn, b in (("Motor", motor), ("Kupplung", kupp))}
        allmin = min(allmin, min(z.values()))
        print("    Station %3d°: Flansch gegen Motor %s, Kupplung %s | Zylinder: Motor %s, Kupplung %s | Kolbenplatte: Motor %s, Kupplung %s" % (
            a, f(z[("Flansch", "Motor")]), f(z[("Flansch", "Kupplung")]), f(z[("Zylinder", "Motor")]),
            f(z[("Zylinder", "Kupplung")]), f(z[("Kolbenplatte", "Motor")]), f(z[("Kolbenplatte", "Kupplung")])))
    print("    kleinster Wert (144°, 216°, 288°): %s;  Station 72° ohne Aussparung (Einsetzen dort nicht vorgesehen), Info: Flansch gegen Motor %s, Kupplung %s"
          % (f(allmin), f(gap2(teile(72)["Flansch"], motor)), f(gap2(teile(72)["Flansch"], kupp))))
    print("    Flansch %.0f x %.0f in Aussparung Ø%.0f (Ecken, Halbdiagonale %.1f): %s;  Zylinder/Kolbenplatte Ø30 in Ø%.0f: %s"
          % (FL_T, FL_R, AUSS_D, math.hypot(FL_T / 2, FL_R / 2), f(hole_gap(teile(144)["Flansch"], 144, AUSS_D / 2)), AUSS_D,
             f(hole_gap(teile(144)["Zylinder"], 144, AUSS_D / 2))))
    r_mc = max(math.hypot(*(ST_R * _er(0) + MOTOR_Y * _et(0) + np.array([sx, sy]) * NEMA / 2)) for sx in (-1, 1) for sy in (-1, 1))
    print("    Motorecke Radius %.2f gegen Brückenrand r %.0f: %s, gegen Haubeninnenradius %.1f: %s"
          % (r_mc, BR_R, f(BR_R - r_mc), R_I, f(R_I - r_mc)))
    print("[5] Stempel Ø%.0f (Z 250 bis 361) gegen Nachbarspritzen (Grundriss; Teile liegen im Z-Bereich 250..344):" % STEMPEL_D)
    for a in ST_WINKEL[1:]:
        t = teile(a)
        print("    Station %3d°: Flansch %s, Zylinder %s, Kolbenplatte %s | Schlitten-Block (%.0f x %.0f) gegen Flansch %s"
              % (a, f(gap2(stempel, t["Flansch"])), f(gap2(stempel, t["Zylinder"])), f(gap2(stempel, t["Kolbenplatte"])),
                 x1 - x0, y1 - y0, f(gap2(block, t["Flansch"]))))
    print("[6] Spindel T8 (tangential +%.0f) und Welle Ø8 (tangential %.0f) gegen Kolbenplatte Ø%.0f der aktiven Station: "
          "Spindel %s, Welle %s   (Achsabstand %.0f, Platte r %.0f + Welle r %.0f = %.0f)"
          % (SPINDEL_Y, WELLE_Y, PL_D, f(gap2(spindel, plat0)), f(gap2(welle, plat0)), SPINDEL_Y, PL_D / 2, WS_D / 2,
             PL_D / 2 + WS_D / 2))
    for a in ST_WINKEL[1:]:
        t = teile(a)
        print("    gegen Station %3d°: Spindel: Flansch %s, Zylinder %s, Platte %s | Welle: Flansch %s, Zylinder %s, Platte %s" % (
            a, f(gap2(spindel, t["Flansch"])), f(gap2(spindel, t["Zylinder"])), f(gap2(spindel, t["Kolbenplatte"])),
            f(gap2(welle, t["Flansch"])), f(gap2(welle, t["Zylinder"])), f(gap2(welle, t["Kolbenplatte"]))))
    fl0 = rect(0, 0, 0, FL_R / 2, FL_T / 2)
    print("[7] Neu in Stand 2:")
    print("    Führungsunterkante Z %.0f (Spindel) / %.0f (Welle) gegen Karussell-Oberkante Z %.0f: %s, gegen Flansch-Oberkante Z %.1f: %s"
          "  (Flansch dreht frei darunter durch; im Grundriss läge Spindel %s, Welle %s im Flansch)"
          % (SPINDEL_Z[0], WELLE_Z[0], Z_RING1, f(SPINDEL_Z[0] - Z_RING1, 1), Z_FL1, f(SPINDEL_Z[0] - Z_FL1, 1),
             f(gap2(spindel, fl0)), f(gap2(welle, fl0))))
    print("    Kupplung Z %.0f..%.0f gegen Schlittenblock oben (Oberkante Z %.0f, oberste Stellung): %s  (Grundriss überdeckt sich: %s, nur Z trennt)"
          % (KUPP_Z[0], KUPP_Z[1], bz1, f(KUPP_Z[0] - bz1, 1), f(gap2(kupp, block))))
    zs0 = STEMPEL_Z[0] - HUB
    zb0 = bz0 - HUB
    print("    Stempel unterste Stellung (Z %.0f..%.0f): gegen Flanschdurchlass Ø%.0f radial %s (Stempel darf hinein);"
          % (zs0, zs0 + (STEMPEL_Z[1] - STEMPEL_Z[0]), DURCHLASS_D, f(DURCHLASS_D / 2 - STEMPEL_D / 2)))
    print("    Block unterste Stellung (Z %.0f..%.0f) gegen Karussell-Oberkante Z %.0f: %s (Block %.0f tangential, Durchlass Ø%.0f, Tasche %.1f breit: ragt darüber hinaus); "
          "gegen Flansch-Oberkante %s"
          % (zb0, zb0 + bz1 - bz0, Z_RING1, f(zb0 - Z_RING1, 1), y1 - y0, DURCHLASS_D, TA_T, f(zb0 - Z_FL1, 1)))
    print("    Stempel-Unterkante Z %.0f gegen Kolbenplatte (Z 250 bis 254, Blatt) Oberkante 254: %s (Maßangabe des Blatts: Platte und Stempel beide ab 250)"
          % (zs0, f(254.0 - zs0, 1).replace("+", "-")))
    print("=" * 88)


# ============================================================
# Zusätzliche Mesh-Bausteine
# ============================================================
def circle_pts(cx, cy, R, n=64):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + R * np.cos(t), cy + R * np.sin(t)], 1)


def _orient(P, ccw):
    P = np.asarray(P, float)
    area = 0.5 * np.sum(P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1])
    return P if (area > 0) == ccw else P[::-1]


def _inside(pt, P):
    """Punkt in beliebigem Polygon (Strahlverfahren)."""
    x, y = pt
    c = False
    n = len(P)
    for i in range(n):
        (x0, y0), (x1, y1) = P[i], P[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def _isect_t(a, b, c, d):
    r, s_ = b - a, d - c
    den = r[0] * s_[1] - r[1] * s_[0]
    if abs(den) < 1e-12:
        return None
    t = ((c[0] - a[0]) * s_[1] - (c[1] - a[1]) * s_[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return t if (1e-9 < t < 1 - 1e-9 and -1e-9 <= u <= 1 + 1e-9) else None


def union_loops(polys):
    """Vereinigung konvexer Polygone (CCW), Rückgabe: Randschleifen (außen und ggf. innen)."""
    segs = []
    for i, P in enumerate(polys):
        for k in range(len(P)):
            a, b = P[k], P[(k + 1) % len(P)]
            ts = [0.0, 1.0]
            for j, Q in enumerate(polys):
                if j != i:
                    for m in range(len(Q)):
                        t = _isect_t(a, b, Q[m], Q[(m + 1) % len(Q)])
                        if t is not None:
                            ts.append(t)
            ts = sorted(set(round(t, 9) for t in ts))
            for t0, t1 in zip(ts[:-1], ts[1:]):
                p0, p1 = a + (b - a) * t0, a + (b - a) * t1
                mid = (p0 + p1) / 2
                if all(_poly_sdf(mid, Q) > 1e-6 for j, Q in enumerate(polys) if j != i):
                    segs.append((tuple(np.round(p0, 4)), tuple(np.round(p1, 4))))
    nb = {}
    for p0, p1 in segs:
        nb.setdefault(p0, []).append(p1)
        nb.setdefault(p1, []).append(p0)
    seen, loops = set(), []
    for start in nb:
        if start in seen:
            continue
        loop, cur, prev = [start], start, None
        seen.add(start)
        while True:
            nxt = [q for q in nb[cur] if q != prev and q not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            loop.append(cur)
        loops.append(np.array(loop, float))
    return loops


def extrude(outer, holes, z0, z1):
    """Prisma aus Außenkontur und Löchern (Polygone, 2D, gerade-ungerade-Regel) zwischen z0 und z1.
    Deckflächen über Trapezzerlegung in x-Streifen, Wände flach."""
    raw = [np.asarray(outer, float)] + [np.asarray(h, float) for h in holes]
    polys = []
    for i, P in enumerate(raw):
        depth = sum(_inside(P[0], Q) for j, Q in enumerate(raw) if j != i)
        polys.append(_orient(P, depth % 2 == 0))
    A = np.vstack(polys)
    B = np.vstack([np.roll(P, -1, axis=0) for P in polys])
    xs = np.unique(np.round(A[:, 0], 7))
    keep = np.abs(B[:, 0] - A[:, 0]) > 1e-9
    Ak, Bk = A[keep], B[keep]
    lo, hi = np.minimum(Ak[:, 0], Bk[:, 0]), np.maximum(Ak[:, 0], Bk[:, 0])
    sl = (Bk[:, 1] - Ak[:, 1]) / (Bk[:, 0] - Ak[:, 0])
    quads = []
    for xa, xb in zip(xs[:-1], xs[1:]):
        if xb - xa < 1e-7:
            continue
        idx = np.where((lo <= xa + 1e-7) & (hi >= xb - 1e-7))[0]
        ya = Ak[idx, 1] + (xa - Ak[idx, 0]) * sl[idx]
        yb = Ak[idx, 1] + (xb - Ak[idx, 0]) * sl[idx]
        o = np.argsort(ya + yb)
        ya, yb = ya[o], yb[o]
        for i in range(0, len(idx) - 1, 2):
            quads.append(((xa, ya[i]), (xb, yb[i]), (xb, yb[i + 1]), (xa, ya[i + 1])))
    Q = np.asarray(quads, float)                          # (n, 4, 2)
    n = len(Q)
    m = rs.Mesh()
    for z, nz in ((z1, 1.0), (z0, -1.0)):
        V = np.concatenate([Q, np.full((n, 4, 1), z)], axis=2).reshape(-1, 3)
        base = 4 * np.arange(n)
        F = np.concatenate([np.stack([base, base + 1, base + 2], 1), np.stack([base, base + 2, base + 3], 1)])
        m.add(V, np.tile([0.0, 0.0, nz], (len(V), 1)), F)
    # Wände
    for P in polys:
        a, b = P, np.roll(P, -1, axis=0)
        e = b - a
        ln = np.linalg.norm(e, axis=1)
        ok = ln > 1e-9
        a, b, e, ln = a[ok], b[ok], e[ok], ln[ok]
        nrm = np.stack([e[:, 1] / ln, -e[:, 0] / ln, np.zeros(len(a))], 1)
        k = len(a)
        V = np.concatenate([np.stack([a[:, 0], a[:, 1], np.full(k, z0)], 1), np.stack([b[:, 0], b[:, 1], np.full(k, z0)], 1),
                            np.stack([b[:, 0], b[:, 1], np.full(k, z1)], 1), np.stack([a[:, 0], a[:, 1], np.full(k, z1)], 1)])
        N = np.tile(nrm, (4, 1))
        i = np.arange(k)
        F = np.concatenate([np.stack([i, k + i, 2 * k + i], 1), np.stack([i, 2 * k + i, 3 * k + i], 1)])
        m.add(V, N, F)
    return m


def knurl_pts(R, depth=0.7, teeth=150):
    t = np.linspace(0, 2 * np.pi, 2 * teeth, endpoint=False)
    r = np.where(np.arange(2 * teeth) % 2 == 0, R, R - depth)
    return np.stack([r * np.cos(t), r * np.sin(t)], 1)


def rect_pts(a, dr, dt, hr, ht):
    return rect(a, dr, dt, hr, ht)[1]


def c_ring(r0, r1, a0, a1, z0, z1, n=90):
    """Kreisringsektor von a0 bis a1 (Grad) als Prisma."""
    t = np.radians(np.linspace(a0, a1, n))
    P = np.vstack([np.stack([r1 * np.cos(t), r1 * np.sin(t)], 1), np.stack([r0 * np.cos(t[::-1]), r0 * np.sin(t[::-1])], 1)])
    return extrude(P, [], z0, z1)


def fenster_umriss(d, k=24):
    w = FENSTER_B / 2 + d
    zb, cz = max(FENSTER_Z0 - d, FUSS_H), FENSTER_Z0 + FENSTER_H - FENSTER_B / 2
    pts = [(w, zb), (w, cz)]
    for j in range(1, k):
        t = math.pi * j / k
        pts.append((w * math.cos(t), cz + w * math.sin(t)))
    pts += [(-w, cz), (-w, zb)]
    return pts


def rahmen_mesh():
    """Messingrahmen des Fensters: Frontfläche 4 mm breit, dazu Innen- und Außenlippe."""
    a, b = fenster_umriss(-0.8), fenster_umriss(-0.8 + RAHMEN_B)
    rf = R_A + 0.8
    cw = np.array([R_A, 0.0, FENSTER_Z0 + FENSTER_H / 2])
    m = rs.Mesh()

    def pt(u, z, r):
        ph = math.asin(max(-1, min(1, u / R_A)))
        return np.array([r * math.cos(ph), r * math.sin(ph), z])

    def quad(p, mode):
        nrm = np.cross(p[1] - p[0], p[2] - p[0])
        ln = np.linalg.norm(nrm)
        if ln < 1e-9:
            return
        nrm /= ln
        c = sum(p) / 4
        if mode == "front" and np.dot(nrm, np.array([c[0], c[1], 0])) < 0:
            nrm = -nrm
        if mode == "in" and np.dot(nrm, cw - c) < 0:
            nrm = -nrm
        if mode == "out" and np.dot(nrm, cw - c) > 0:
            nrm = -nrm
        rs._quad(m, p, nrm)

    for i in range(len(a)):
        j = (i + 1) % len(a)
        quad([pt(*a[i], rf), pt(*a[j], rf), pt(*b[j], rf), pt(*b[i], rf)], "front")
        quad([pt(*a[i], rf), pt(*a[j], rf), pt(*a[j], R_I), pt(*a[i], R_I)], "in")
        quad([pt(*b[i], rf), pt(*b[j], rf), pt(*b[j], R_A - 0.2), pt(*b[i], R_A - 0.2)], "out")
    return m


def fenster_maske(thc, zc):
    u = R_A * np.sin(np.radians(thc))
    cz = FENSTER_Z0 + FENSTER_H - FENSTER_B / 2
    ok = (np.abs(thc) <= 90) & (np.abs(u) <= FENSTER_B / 2) & (zc >= FENSTER_Z0)
    return ok & ((zc <= cz) | (u ** 2 + (zc - cz) ** 2 <= (FENSTER_B / 2) ** 2))


def station_frame(a):
    t = math.radians(a)
    er, et = np.array([math.cos(t), math.sin(t), 0.0]), np.array([-math.sin(t), math.cos(t), 0.0])
    return rs.Frame(ST_R * er, [er, et, np.array([0.0, 0.0, 1.0])])


# ============================================================
# Szene
# ============================================================
def schale(sc, grp, zs, mask=None, th=None, col_out=C_CREME, col_in=C_CREME_IN):
    th = np.linspace(-180, 180, 181) if th is None else th
    pid = sc.nid()
    sc.add(rs.shell_surface(R_A, 1, th, zs, mask), grp, col_out, pid=pid)
    sc.add(rs.shell_surface(R_I, -1, th, zs, mask), grp, col_in, pid=pid)
    return pid


def slot_maske(thc, zc):
    u = R_A * np.sin(np.radians(thc - SLOT_W))
    return (np.abs(thc - SLOT_W) <= 90) & (np.abs(u) <= SLOT_B / 2) & (zc >= SLOT_Z[0]) & (zc <= SLOT_Z[1])


def slot_kanten():
    """Wandstärke an den Schlitzkanten (Seiten, Unter- und Oberkante)."""
    d = math.asin(SLOT_B / 2 / R_A)
    t0, t1 = math.radians(SLOT_W) - d, math.radians(SLOT_W) + d
    m = rs.Mesh()
    P = lambda t, R, z: (R * math.cos(t), R * math.sin(t), z)
    for t, sg in ((t0, 1.0), (t1, -1.0)):
        rs._quad(m, [P(t, R_I, SLOT_Z[0]), P(t, R_A, SLOT_Z[0]), P(t, R_A, SLOT_Z[1]), P(t, R_I, SLOT_Z[1])],
                 (-sg * math.sin(t), sg * math.cos(t), 0.0))
    ts = np.linspace(t0, t1, 16)
    for z, nz in ((SLOT_Z[0], 1.0), (SLOT_Z[1], -1.0)):
        for ta, tb in zip(ts[:-1], ts[1:]):
            rs._quad(m, [P(ta, R_I, z), P(ta, R_A, z), P(tb, R_A, z), P(tb, R_I, z)], (0.0, 0.0, nz))
    return m


def build_scene():
    sc = rs.Scene()
    sc.add(rs.revolve([(125, 0), (0, 0)], 96), "ground", "#eceef1")
    sc.add(rs.revolve([(108, 0.05), (0, 0.05)], 96), "ground", "#dcdfe4")
    # Fuß Ø185, dunkelgrau, mit Boden des Sockels
    sc.add(rs.revolve([(0, 0), (FUSS_D / 2, 0), (FUSS_D / 2, 21), (FUSS_D / 2 - 3.5, FUSS_H), (0, FUSS_H)], 120),
           "fuss", C_DUNKEL, ks=0.12)
    sc.add(rs.cyl(0, 0, R_I, FUSS_H, Z_BODEN, 120, (False, True)), "boden", "#3a3d43")
    # Becher Ø60 auf Radius 50, Höhe 60 (Kaufteil, Glas), mit etwas Mischfarbe
    bx = ST_R
    sc.add(rs.cyl(bx, 0, BECHER_D / 2 - 0.6, BECHER_Z0, BECHER_Z0 + 2.0, 56), "becher", "#dbe6ee")
    sc.add(rs.cyl(bx, 0, BECHER_D / 2 - 1.0, BECHER_Z0 + 2.0, BECHER_Z0 + 14.0, 56), "becher", "#a64d8f", ks=0.3)
    sc.add(rs.cyl(bx, 0, BECHER_D / 2, BECHER_Z0, BECHER_Z0 + BECHER_H, 72, (False, False)), "becher", "#9fc4dc",
           alpha=0.38, ks=0.2)
    z_top = BECHER_Z0 + BECHER_H
    sc.add(rs.revolve([(BECHER_D / 2 - 1.8, z_top - 0.8), (BECHER_D / 2 + 0.2, z_top - 0.8), (BECHER_D / 2 + 0.2, z_top),
                       (BECHER_D / 2 - 1.8, z_top), (BECHER_D / 2 - 1.8, z_top - 0.8)], 72, cx=bx), "becher", "#7fa9c4")
    # Sockelschale Z 25 bis 120 mit Fenster
    wth = math.degrees(math.asin(FENSTER_B / 2 / R_A))
    th = np.unique(np.concatenate([np.arange(-180, -33, 3.0), np.arange(-33, 33.001, 0.5), [-wth, wth],
                                   np.arange(33, 180.001, 3.0)]))
    cz = FENSTER_Z0 + FENSTER_H - FENSTER_B / 2
    zs = np.unique(np.concatenate([[FUSS_H, FENSTER_Z0], np.arange(FENSTER_Z0, FENSTER_Z0 + FENSTER_H + 1, 1.0),
                                   [cz, Z_SOCKEL1]]))
    zs = zs[zs <= Z_SOCKEL1]
    schale(sc, "sockel", zs, fenster_maske, th)
    sc.add(rahmen_mesh(), "rahmen", C_MESSING, ks=0.35)
    # Mittelschale Z 120 bis 300 mit Daumenschlitz 20 x 60 bei -60 Grad
    d = math.degrees(math.asin(SLOT_B / 2 / R_A))
    th = np.unique(np.concatenate([np.arange(-180, 180.001, 3.0), np.arange(-90, -29.99, 0.5), [SLOT_W - d, SLOT_W + d]]))
    zs = np.unique(np.concatenate([[Z_SOCKEL1, Z_MITTE1], np.arange(SLOT_Z[0], SLOT_Z[1] + 0.1, 1.0), [200.0]]))
    pid = schale(sc, "mittel", zs, slot_maske, th)
    sc.add(slot_kanten(), "mittel", C_CREME, pid=pid)
    sc.add(rs.ring_prism(rs.circ_r(R_I - 0.1), rs.circ_r(65.0), 238.0, Z_RING0, n=120), "laufring", C_CREME_IN)
    # Karussellplatte Z 245..259, Ø160, gerändelt, messingfarben; Taschen von oben, Durchlässe Ø31
    pid = sc.nid()
    loch = circle_pts(0, 0, LOCH_D / 2, 48)
    kn = knurl_pts(RING_R)
    unten = [loch] + [circle_pts(*(ST_R * _er(a)), DURCHLASS_D / 2, 40) for a in ST_WINKEL]
    oben = [loch] + union_loops([rect_pts(a, 0, 0, TA_R / 2, TA_T / 2) for a in ST_WINKEL])
    sc.add(extrude(kn, unten, Z_RING0, Z_TASCHE), "karussell", C_MESSING, pid=pid, ks=0.35)
    sc.add(extrude(kn, oben, Z_TASCHE, Z_RING1), "karussell", C_MESSING, pid=pid, ks=0.35)
    # Oberschale Z 300 bis 418 (cremeweiß), Oberkante als Ring
    schale(sc, "ober", np.linspace(Z_MITTE1, Z_OBER1, 6))
    sc.add(rs.revolve([(R_I, Z_OBER1), (R_A, Z_OBER1)], 120), "ober", C_CREME)
    # Haube Ø170 (Z 426 bis 480), dunkelgrau
    sc.add(rs.revolve([(R_A, Z_HAUBE0), (R_A, Z_HAUBE1 - 5), (R_A - 5, Z_HAUBE1), (0, Z_HAUBE1)], 120), "kappe", C_DUNKEL, ks=0.12)
    # Abtropfring unter den vier inaktiven Stationen (C-Ring, Boden und Rand, Oberkante Z 90)
    pid = sc.nid()
    sc.add(c_ring(22, 80, 41, 319, 86.0, 88.0), "tray", "#c4cad1", pid=pid)
    sc.add(c_ring(78.2, 80, 41, 319, 88.0, 90.0), "tray", "#c4cad1", pid=pid)
    sc.add(c_ring(22, 23.8, 41, 319, 88.0, 90.0), "tray", "#c4cad1", pid=pid)
    # Brücke Ø164 mit Aussparungen Ø50 nur bei 144, 216, 288
    sc.add(extrude(circle_pts(0, 0, BR_R, 180), [circle_pts(*(ST_R * _er(a)), AUSS_D / 2, 56) for a in AUSS_WINKEL],
                   Z_BR0, Z_BR1), "bruecke", "#c7cbd1")
    # Motor NEMA 17 auf der Spindelachse
    fr0 = station_frame(0)
    h = NEMA / 2
    sc.add(rs.box(-h, h, MOTOR_Y - h, MOTOR_Y + h, Z_MOT0, Z_MOT0 + 5), "motor", "#8d9097", frame=fr0, ks=0.25)
    sc.add(rs.box(-h, h, MOTOR_Y - h, MOTOR_Y + h, Z_MOT0 + 5, Z_MOT1 - 4), "motor", "#3b3e44", frame=fr0)
    sc.add(rs.box(-h, h, MOTOR_Y - h, MOTOR_Y + h, Z_MOT1 - 4, Z_MOT1), "motor", "#8d9097", frame=fr0, ks=0.25)
    # Stößel (aktive Station vorne): Spindel, Welle, Kupplung, Schlitten mit Stempel, Endschalter mit Nase
    g = "stoessel"
    sc.add(rs.cyl(0, SPINDEL_Y, WS_D / 2, *SPINDEL_Z, 20), g, "#b9bec5", frame=fr0, ks=0.5)
    sc.add(rs.cyl(0, WELLE_Y, WS_D / 2, *WELLE_Z, 20), g, "#d0d4da", frame=fr0, ks=0.5)
    sc.add(rs.cyl(0, SPINDEL_Y, KUPP_D / 2, *KUPP_Z, 28), g, "#a3abb5", frame=fr0, ks=0.5)
    pid = sc.nid()
    bx0, bx1, by0, by1, bz0, bz1 = SL_BLOCK
    sc.add(rs.box(bx0, bx1, by0, by1, bz0, bz1), g, "#d98c4a", pid=pid, frame=fr0)
    sc.add(rs.cyl(0, 0, STEMPEL_D / 2, *STEMPEL_Z, 40), g, "#8d9097", frame=fr0, ks=0.3)
    sc.add(rs.cyl(0, SPINDEL_Y, 8.0, bz0 - 3, bz0 + 4, 28), g, C_MESSING, frame=fr0, ks=0.3)    # Flanschmutter
    sc.add(rs.box(-24.0, -14.0, -10.0, 0.0, Z_BR0 - 6.5, Z_BR0), g, "#b4574b", frame=fr0)       # Endschalter
    sc.add(rs.box(-23.0, -15.0, -7.0, -3.0, bz1, Z_BR0 - 6.5), g, "#d98c4a", frame=fr0)         # Nase
    for k, a in enumerate(ST_WINKEL):
        build_station(sc, a, ST_NAMEN[k])
    return sc


def build_station(sc, a, name):
    fr = station_frame(a)
    g = "station"
    pb = PB_STAND[name]
    stop0 = pb - ROD_L - STOP_T
    # Düse und Spritzenschulter
    sc.add(rs.revolve([(1.0, Z_DUESE), (2.4, Z_DUESE + 3), (5.0, Z_DUESE + 9), (14.8, 120.0)], 28), g, "#d2d6db", frame=fr, ks=0.3)
    # Inhalt, Gummistopfen, Kolbenstange (Kreuzprofil), Kolbenplatte Ø30
    sc.add(rs.cyl(0, 0, ZYL_D / 2 - 0.9, 120.0, stop0, 40), g, INHALT[name], frame=fr, ks=0.15)
    sc.add(rs.cyl(0, 0, ZYL_D / 2 - 0.9, stop0, stop0 + STOP_T, 40), g, "#4a4d52", frame=fr)
    pid = sc.nid()
    r0, r1 = stop0 + STOP_T, pb
    sc.add(rs.box(-6, 6, -1.25, 1.25, r0, r1), g, "#f1f1f1", pid=pid, frame=fr)
    sc.add(rs.box(-1.25, 1.25, -6, 6, r0, r1), g, "#f1f1f1", pid=pid, frame=fr)
    sc.add(rs.cyl(0, 0, PL_D / 2, pb, pb + PL_T, 40), g, "#f6f6f6", frame=fr)
    # Zylinder (Glas) und Flansch 45 x 32 in der Tasche
    sc.add(rs.cyl(0, 0, ZYL_D / 2, 120.0, Z_FL0, 48, (False, False)), g, "#d8e6ee", alpha=0.22, frame=fr, ks=0.3)
    sc.add(rs.box(-FL_R / 2, FL_R / 2, -FL_T / 2, FL_T / 2, Z_FL0, Z_FL1), g, "#e3edf2", alpha=0.75, frame=fr)


# ============================================================
# Ansichten und Beschriftung
# ============================================================
GRUPPEN = {
    1: {"ground", "fuss", "boden", "becher", "sockel", "rahmen", "mittel", "karussell", "ober", "kappe"},
    2: {"ground", "fuss", "boden", "becher", "laufring", "karussell", "tray", "station", "stoessel", "bruecke", "motor"},
    3: {"fuss", "ober", "karussell", "station", "stoessel", "bruecke", "motor"},
}


def dim_h(ax, xa, y0, y1, text, ink):
    ax.plot([xa, xa], [y0, y1], color=ink, lw=1.1)
    for y in (y0, y1):
        ax.plot([xa - 6, xa + 6], [y, y], color=ink, lw=1.1)
    ax.text(xa + 10, (y0 + y1) / 2, text, rotation=90, ha="left", va="center", fontsize=12, color=ink)


def dim_w(ax, xl, xr, y, text, ink, dy):
    ax.plot([xl, xr], [y, y], color=ink, lw=1.1)
    for x in (xl, xr):
        ax.plot([x, x], [y - 5, y + 5], color=ink, lw=1.1)
    ax.text((xl + xr) / 2, y + dy, text, ha="center", va="center", fontsize=12, color=ink)


def labels_seite(ax, items, tx, ha, soft, ink, abstand=24):
    items = sorted(items, key=lambda it: it[1][1])
    ys = []
    for _, (_, py_) in items:
        ys.append(py_ if not ys else max(py_, ys[-1] + abstand))
    for (txt, (px_, py_)), ty in zip(items, ys):
        ax.plot([tx + (4 if ha == "right" else -4), px_], [ty, py_], color=soft, lw=0.9)
        ax.plot([px_], [py_], "o", color=soft, ms=3)
        ax.text(tx, ty, txt, ha=ha, va="center", fontsize=11, color=ink)


def polar(v, R, a, z):
    t = math.radians(a)
    return v.px(np.array([R * math.cos(t), R * math.sin(t), z]))


def ellipse(ax, v, R, z, **kw):
    t = np.linspace(0, 2 * np.pi, 120)
    xy = [v.px(np.array([R * math.cos(x), R * math.sin(x), z])) for x in t]
    ax.plot([p[0] for p in xy], [p[1] for p in xy], **kw)


def overlays(ax, views):
    ink, soft = "#1f2329", "#59606a"
    ax.text(900, 38, "Farbmischer Revolver, ein Motor, Konzept-Rendering", ha="center", va="center", fontsize=22,
            fontweight="bold", color=ink)
    for x, t in ((300, "1  Außenansicht, geschlossen"), (900, "2  Innenleben ohne Schalen und Haube"),
                 (1500, "3  Draufsicht ohne Haube")):
        ax.text(x, 80, t, ha="center", va="center", fontsize=13, color="#2b3036")
    for x in (600, 1200):
        ax.plot([x, x], [70, 840], color="#e3e5e8", lw=1)

    # --- Ansicht 1: Maße
    v1 = views[1]
    xa, ya = v1.px(106 * v1.r)
    _, yb = v1.px(106 * v1.r + np.array([0, 0, Z_HAUBE1]))
    dim_h(ax, xa, ya, yb, "Höhe %.0f" % Z_HAUBE1, ink)
    xl, _ = v1.px(-R_A * v1.r)
    xr, _ = v1.px(R_A * v1.r)
    _, yt = v1.px(np.array([0, 0, Z_HAUBE1]))
    dim_w(ax, xl, xr, yt - v1.S * R_A * math.sin(v1.e) - 18, "Durchmesser %.0f" % (2 * R_A), ink, -14)
    xl, _ = v1.px(-FUSS_D / 2 * v1.r)
    xr, _ = v1.px(FUSS_D / 2 * v1.r)
    _, yf = v1.px(np.array([0, 0, 0.0]))
    dim_w(ax, xl, xr, yf + v1.S * FUSS_D / 2 * math.sin(v1.e) + 20, "Fuß %.0f" % FUSS_D, ink, 15)
    pr = polar(v1, RING_R + 1, SLOT_W, 252)
    ax.plot([pr[0], 100], [pr[1], pr[1] - 100], color=soft, lw=0.9)
    ax.plot([pr[0]], [pr[1]], "o", color=soft, ms=3)
    ax.text(12, pr[1] - 134, "Drehring Ø %.0f, Messing,\ngerändelt, durch Schlitz\n20 x 60 bei %.0f° drehbar" % (2 * RING_R, SLOT_W),
            ha="left", va="center", fontsize=10.5, color=ink)
    pf = polar(v1, R_A, -22, 95)
    ax.plot([pf[0], 452], [pf[1], pf[1]], color=soft, lw=0.9)
    ax.plot([pf[0]], [pf[1]], "o", color=soft, ms=3)
    ax.text(456, pf[1], "Fenster mit\nBecher und\nMessingrahmen", ha="left", va="center", fontsize=10.5, color=ink)

    # --- Ansicht 2: Beschriftungen
    v2 = views[2]
    f0 = station_frame(0)
    f1, f4 = station_frame(72), station_frame(288)
    links = [("Brücke, 3 Aussparungen Ø50", polar(v2, 76, 190, Z_BR1)),
             ("Stößelschlitten", v2.px(f0.w((0, -28, 376)))),
             ("Führungswelle Ø8", v2.px(f0.w((0, WELLE_Y, 330)))),
             ("Karussellplatte Ø160", polar(v2, 80, 235, 252)),
             ("Abtropfring", polar(v2, 74, 250, 88)),
             ("Becher Ø60", v2.px(f0.w((0, 24, 70))))]
    rechts = [("Motor NEMA 17", v2.px(f0.w((0, MOTOR_Y + 21, 446)))),
              ("Spindel T8", v2.px(f0.w((0, SPINDEL_Y, 330)))),
              ("Kolbenplatte", v2.px(f1.w((0, 12, PB_STAND['M'] + 2)))),
              ("Spritze 60 ml", v2.px(f1.w((0, 12, 160)))),
              ("Laufring", polar(v2, 76, 20, 241)),
              ("Stempel Ø26", v2.px(f0.w((13, 0, 353)))),
              ("Düse, Station vorne", v2.px(f0.w((0, 0, 108))))]
    labels_seite(ax, links, 752, "right", soft, ink)
    labels_seite(ax, rechts, 1048, "left", soft, ink)
    for z in (Z_SOCKEL1, Z_MITTE1, Z_OBER1, Z_HAUBE0, Z_HAUBE1):
        ellipse(ax, v2, R_A, z, color="#9aa1ab", lw=0.8, ls=(0, (4, 4)), alpha=0.8)
    for z in (FUSS_H,):
        ellipse(ax, v2, R_A, z, color="#9aa1ab", lw=0.8, ls=(0, (4, 4)), alpha=0.8)
    for sgn in (-1, 1):
        a, b = v2.px(sgn * R_A * v2.r + np.array([0, 0, FUSS_H])), v2.px(sgn * R_A * v2.r + np.array([0, 0, Z_HAUBE1]))
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#9aa1ab", lw=0.8, ls=(0, (4, 4)), alpha=0.8)
    ax.text(900, 852, "gestrichelt: Schalen und Haube nur als Kontur", ha="center", va="center", fontsize=10.5, color=soft)
    ax.text(900, 868, "Inhalt: C, M, Y, Weiß, Schwarz auf 0°, 72°, 144°, 216°, 288°", ha="center", va="center", fontsize=10.5, color=soft)

    # --- Ansicht 3: Fensterrichtung, Stationen, Aussparungen
    v3 = views[3]
    arc = [polar(v3, R_A + 4, t, Z_OBER1) for t in np.linspace(-30, 30, 25)]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], color=C_MESSING, lw=4, solid_capstyle="round")
    p0, p1 = polar(v3, 95, 0, Z_OBER1), polar(v3, 113, 0, Z_OBER1)
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color="#8a6a12", lw=2.2))
    ax.text(p1[0], p1[1] + 20, "vorne, Fenster (0°)", ha="center", va="center", fontsize=12, fontweight="bold", color="#7a5a00")
    for a, nm in zip(ST_WINKEL, ST_NAMEN):
        x, y = polar(v3, 106, a, Z_OBER1)
        if a == 0:
            x, y = polar(v3, 106, 0, Z_OBER1)
            x += 52
        tc = "white" if nm in ("K", "M") else ink
        ax.text(x, y, "%s  %d°" % (nm, a), ha="center", va="center", fontsize=11, fontweight="bold", color=tc,
                bbox=dict(boxstyle="round,pad=0.25", fc=INHALT[nm], ec="#6b7078", lw=0.8))
    for a in ST_WINKEL:                                   # Spritzenumriss unter der Brücke (Flansch, gestrichelt)
        P = rect(a, 0, 0, FL_R / 2, FL_T / 2)[1]
        xy = [v3.px(np.array([p[0], p[1], Z_BR1])) for p in list(P) + [P[0]]]
        ax.plot([q[0] for q in xy], [q[1] for q in xy], color="#2f6f9a", lw=1.0, ls=(0, (3, 2)))
    th = np.linspace(0, 2 * np.pi, 73)
    xy = [v3.px(np.array([ST_R + PL_D / 2 * math.cos(t), PL_D / 2 * math.sin(t), Z_BR1])) for t in th]
    ax.plot([q[0] for q in xy], [q[1] for q in xy], color="#2f6f9a", lw=1.0, ls=(0, (2, 2)))
    xy = [v3.px(np.array([ST_R + BECHER_D / 2 * math.cos(t), BECHER_D / 2 * math.sin(t), Z_BR1])) for t in th]
    ax.plot([q[0] for q in xy], [q[1] for q in xy], color="#2f6f9a", lw=1.0, ls=(0, (6, 3)))
    ax.text(1500, 852, "gestrichelt, unter der Brücke: Flansch 45 x 32,", ha="center", va="center", fontsize=10.5, color=soft)
    ax.text(1500, 868, "Kolbenplatte Ø30 vorne und Becherrand Ø60", ha="center", va="center", fontsize=10.5, color=soft)
    ax.text(900, 888, "Durchmesser %.0f  |  Höhe %.0f  |  Fuß %.0f  |  Stationsradius %.0f, fünf Stationen im Abstand 72°"
            % (2 * R_A, Z_HAUBE1, FUSS_D, ST_R), ha="center", va="center", fontsize=11, color=ink)


def main():
    t0 = time.time()
    sc = build_scene()
    zmin = min(it.V[:, 2].min() for it in sc.items)
    zmax = max(it.V[:, 2].max() for it in sc.items)
    print("Szene: %d Teile, %d Dreiecke, Z %.1f bis %.1f (%.1f s)"
          % (len(sc.items), sum(len(it.F) for it in sc.items), zmin, zmax, time.time() - t0))
    views = {1: rs.View(-35.0, 20, 1.30, 290, 774),
             2: rs.View(-35.0, 24, 1.30, 900, 738),
             3: rs.View(0.0, 90, 2.3, 1500, 462)}
    alpha = {1: None, 2: None, 3: {"motor": 0.35, "bruecke": 1.0}}
    canvas = np.ones((900, 1800, 3), np.float32)
    for k in (1, 2, 3):
        t1 = time.time()
        canvas[:, (k - 1) * 600:k * 600] = rs.render_panel(sc, GRUPPEN[k], views[k], 600, 900, 2, alpha[k], (k - 1) * 600)
        print("  Ansicht %d gerendert in %.1f s" % (k, time.time() - t1))
    fig = plt.figure(figsize=(18, 9), dpi=100, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(canvas, extent=(0, 1800, 900, 0), interpolation="nearest")
    ax.set_xlim(0, 1800)
    ax.set_ylim(900, 0)
    ax.axis("off")
    overlays(ax, views)
    out = os.path.join(HERE, "rendering_revolver.png")
    fig.savefig(out, dpi=100, facecolor="white")
    print("geschrieben:", out, "(%.1f s)" % (time.time() - t0))


if __name__ == "__main__":
    if "--pruefung" in sys.argv:
        pruefung()
    else:
        main()
