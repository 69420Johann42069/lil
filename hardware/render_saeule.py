#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konzept-Rendering der runden Farbmischer-Säule nach saeule_parameter.md (Stand 5).

Nur numpy, matplotlib und Standardbibliothek. Schreibt rendering_saeule.png (1800 x 900 px)
neben dieses Skript und druckt die Maß- und Kollisionsprüfung auf die Konsole.

Modellkoordinaten: Z nach oben, Z = 0 ist die Tischplatte, Winkel 0 Grad (Fenster, vorne) liegt auf +X.
Stationsachse exakt nach dem Blatt:  r(s) = 32 + s*sin(4 Grad),  z(s) = 105 + s*cos(4 Grad).
Lokales System einer Station: Z = Achse (s), Y = radial nach außen (senkrecht zur Achse),
X = Y x Z (tangential).  Weltpunkt = (r(s) + y*cos4) auf er, x auf Tangente, z(s) - y*sin4.

Darstellung: eigener kleiner Z-Buffer-Rasterizer (numpy), Text und Maßlinien mit matplotlib.
Programmaufruf:  python3 render_saeule.py            -> Prüfung + PNG
                 python3 render_saeule.py --pruefung -> nur Prüfung
"""
import math
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# ============================================================
# Maße aus saeule_parameter.md (mm), Stand 5
# ============================================================
D_AUSSEN = 208.0
R_A = D_AUSSEN / 2
WAND = 2.4
R_I = R_A - WAND                      # 92.6
FUSS_D, FUSS_H = 218.0, 25.0
Z_SOCKEL1, Z_MITTE1, Z_OBER1, Z_HAUBE1 = 120.0, 300.0, 420.0, 470.0
Z_HAUBE_INNEN = 455.0                 # Haube innen frei bis hier
OEFF_B, OEFF_Z0, OEFF_Z1, OEFF_WINKEL = 60.0, 150.0, 290.0, 36.0   # Öffnung der Drehhülse
SAEULE_R, SAEULE_D, SAEULE_WINKEL = 90.0, 10.0, (0, 144, 216)      # Tragsäulen (Z 120 bis Motorplatte)
BECHER_D, BECHER_H, BECHER_Z0 = 75.0, 60.0, 30.0
BR_D = 84.0
FENSTER_B, FENSTER_H, FENSTER_Z0 = 90.0, 80.0, 28.0
RAHMEN_B = 4.0
PLATTE_ID, PLATTE_AD, PLATTE_Z0, PLATTE_Z1 = 90.0, 196.0, 404.0, 412.0

NEIG = math.radians(4.0)
SN, CS = math.sin(NEIG), math.cos(NEIG)
R_DUESE, Z_DUESE = 32.0, 105.0
ST_WINKEL = [36, 108, 180, 252, 324]
ST_NAMEN = ["C", "M", "Y", "W", "K"]


def r_ax(s):
    return R_DUESE + s * SN


def z_ax(s):
    return Z_DUESE + s * CS


# Station, lokal (s = lokal Z, x tangential, y radial)
S_DUESE = (0.0, 15.0)
S_ZYL, ZYL_D = (15.0, 140.0), 30.0
S_FLANSCH, FL_X, FL_Y = (137.0, 140.0), 45.0, 32.0   # lange Flanschseite tangential
HALT_D, HALT_Z0, HALT_Z1 = 198.0, 233.0, 247.0       # Halterplatte, eine Scheibe, Welt-Z
S_HALTER = (128.0, 142.0)                            # dieselbe Scheibe in s der Station
DURCHLASS_D, LOCH_D = 31.0, 40.0                     # Durchlässe, Mittelloch für Kabel
TASCHE_X, TASCHE_Y, TASCHE_BODEN = 45.6, 32.6, 136.8  # Schlitz 31 radial offen, Flanschtasche nach außen offen
TASCHE_T = S_HALTER[1] - TASCHE_BODEN
KOLB_D, KOLB_T = 30.0, 4.0
DISC_D, DISC_T = 20.0, 2.0
STANGE_B, STANGE_DICKE = 12.0, 2.5
STANGE_L, GUMMI_T = 120.0, 5.0        # Darstellungsannahmen: Stange Platte -> Gummi
SB_MIN, SB_MAX = 151.0, 241.0         # Schlitten-Unterkante gedrückt / gezogen
FUELL = 0.6                           # dargestellte Kolbenstellung (Anteil des Hubs)
WELLE_XY, SPINDEL_XY = (-18.0, 21.0), (0.0, 21.0)
WELLE_S, SPINDEL_S, WS_D = (149.0, 306.0), (149.0, 285.0), 8.0
KUPP_S0, KUPP_S1, KUPP_D = 275.0, 300.0, 19.0
MOTOR_S0, MOTOR_S1, NEMA = 308.0, 348.0, 42.3
MOTOR_XY = SPINDEL_XY                 # Motor auf der Spindelachse
SCH_H = 30.0
SCH_BLOCK = (-27.5, 13.0, 2.0, 32.0)   # x0, x1, y0, y1 (tangential 40,5, deckt Lager und Mutter ab)
SCH_ARM = (-9.0, 9.0, -8.0, 2.0, 8.0)  # x0, x1, y0, y1, Dicke 8
LM_D, LM_L, LM_OFF = 15.0, 24.0, 5.0   # LM8UU ab sb+5
MUTTER_D, MUTTER_T = 22.0, 4.0         # Flanschmutter in der Schlittenunterseite (sb bis sb+4)
SCHALTER_S = (293.5, 300.0)            # Mikroschalter 20 x 10 x 6,5 unter der Motorplatte
SCHALTER_XY = (12.0, 22.0, 8.0, 28.0)  # Lage quer: Annahme (Blatt: neben dem Schlitten)

C_CREME, C_CREME_IN = "#efe6d0", "#d9cfb6"
C_DUNKEL, C_MESSING = "#4b4e54", "#c9a64e"
INHALT = {"C": "#17b4e6", "M": "#d4237f", "Y": "#f3d21c", "W": "#f4f2ec", "K": "#1c1c1e"}


# ============================================================
# Prüfung (Maße und Kollisionen), unabhängig vom Rendering
# ============================================================
class Frame:
    def __init__(self, o, a):
        self.O = np.asarray(o, float)
        self.A = np.asarray(a, float)          # Zeilen: X, Y, Z

    def w(self, v):
        return self.O + np.asarray(v, float) @ self.A

    def n(self, v):
        return np.asarray(v, float) @ self.A


def station_frame(a_deg):
    a = math.radians(a_deg)
    er, ez = np.array([math.cos(a), math.sin(a), 0.0]), np.array([0.0, 0.0, 1.0])
    zax = SN * er + CS * ez
    yax = CS * er - SN * ez
    xax = np.cross(yax, zax)
    return Frame(R_DUESE * er + Z_DUESE * ez, [xax, yax, zax])


def sdf_cyl(P, p0, p1, R):
    a = p1 - p0
    L = np.linalg.norm(a)
    a = a / L
    d = P - (p0 + p1) / 2
    ax = d @ a
    rad = np.linalg.norm(d - np.outer(ax, a), axis=1)
    q0, q1 = rad - R, np.abs(ax) - L / 2
    return np.minimum(np.maximum(q0, q1), 0) + np.hypot(np.maximum(q0, 0), np.maximum(q1, 0))


def sdf_box(P, c, A, h):
    q = np.abs((P - c) @ A.T) - h
    return np.linalg.norm(np.maximum(q, 0), axis=1) + np.minimum(q.max(1), 0)


def solid_cyl(fr, cx, cy, R, s0, s1):
    return {"t": "cyl", "p0": fr.w((cx, cy, s0)), "p1": fr.w((cx, cy, s1)), "R": R}


def solid_box(fr, x0, x1, y0, y1, s0, s1):
    return {"t": "box", "c": fr.w(((x0 + x1) / 2, (y0 + y1) / 2, (s0 + s1) / 2)), "A": fr.A,
            "h": np.array([(x1 - x0) / 2, (y1 - y0) / 2, (s1 - s0) / 2])}


def sdf(sol, P):
    if sol["t"] == "cyl":
        return sdf_cyl(P, sol["p0"], sol["p1"], sol["R"])
    return sdf_box(P, sol["c"], sol["A"], sol["h"])


def samples(sol, h=1.5):
    pts = []
    if sol["t"] == "cyl":
        p0, p1, R = sol["p0"], sol["p1"], sol["R"]
        a = p1 - p0
        L = np.linalg.norm(a)
        a = a / L
        t = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.99 else np.cross(a, [1.0, 0, 0])
        t /= np.linalg.norm(t)
        u = np.cross(a, t)
        ang = np.linspace(0, 2 * np.pi, max(8, int(2 * np.pi * R / h)), endpoint=False)
        for z in np.linspace(0, L, max(2, int(L / h) + 1)):
            pts.append(p0 + a * z + R * (np.outer(np.cos(ang), t) + np.outer(np.sin(ang), u)))
        for rr in np.arange(0, R + 1e-9, h):
            for z in (0, L):
                n = max(1, int(2 * np.pi * rr / h))
                an = np.linspace(0, 2 * np.pi, n, endpoint=False)
                pts.append(p0 + a * z + rr * (np.outer(np.cos(an), t) + np.outer(np.sin(an), u)))
    else:
        c, A, hh = sol["c"], sol["A"], sol["h"]
        for ax in range(3):
            o = [i for i in range(3) if i != ax]
            g1 = np.linspace(-hh[o[0]], hh[o[0]], max(2, int(2 * hh[o[0]] / h) + 1))
            g2 = np.linspace(-hh[o[1]], hh[o[1]], max(2, int(2 * hh[o[1]] / h) + 1))
            G1, G2 = np.meshgrid(g1, g2)
            for sg in (-1, 1):
                loc = np.zeros((G1.size, 3))
                loc[:, ax], loc[:, o[0]], loc[:, o[1]] = sg * hh[ax], G1.ravel(), G2.ravel()
                pts.append(c + loc @ A)
    return np.vstack(pts)


def gap(sa, sb, h=1.5):
    """Kleinster Abstand zweier Körper (negativ = Durchdringung, Tiefe der tiefsten Stützpunkte)."""
    return min(sdf(sb, samples(sa, h)).min(), sdf(sa, samples(sb, h)).min())




def station_solids(fr, sb):
    """Alle Körper einer Station; sb = Unterkante des Schlittens (s)."""
    spl = sb - KOLB_T - DISC_T                           # Kolbenplatte Unterkante (Scheibe endet bei sb)
    S = {}
    S["Düse"] = solid_cyl(fr, 0, 0, 2, *S_DUESE)
    S["Zylinder"] = solid_cyl(fr, 0, 0, ZYL_D / 2, *S_ZYL)
    S["Flansch"] = solid_box(fr, -FL_X / 2, FL_X / 2, -FL_Y / 2, FL_Y / 2, *S_FLANSCH)
    S["Kolbenplatte"] = solid_cyl(fr, 0, 0, KOLB_D / 2, spl, spl + KOLB_T)
    S["Stahlscheibe"] = solid_cyl(fr, 0, 0, DISC_D / 2, spl + KOLB_T, spl + KOLB_T + DISC_T)
    S["Kolbenstange"] = solid_box(fr, -STANGE_B / 2, STANGE_B / 2, -STANGE_B / 2, STANGE_B / 2,
                                  spl - STANGE_L, spl)
    S["Welle"] = solid_cyl(fr, *WELLE_XY, WS_D / 2, *WELLE_S)
    S["Spindel"] = solid_cyl(fr, *SPINDEL_XY, WS_D / 2, *SPINDEL_S)
    S["Kupplung"] = solid_cyl(fr, *SPINDEL_XY, KUPP_D / 2, KUPP_S0, KUPP_S1)
    S["Motor"] = solid_box(fr, MOTOR_XY[0] - NEMA / 2, MOTOR_XY[0] + NEMA / 2,
                           MOTOR_XY[1] - NEMA / 2, MOTOR_XY[1] + NEMA / 2, MOTOR_S0, MOTOR_S1)
    x0, x1, y0, y1 = SCH_BLOCK
    S["Schlitten-Block"] = solid_box(fr, x0, x1, y0, y1, sb, sb + SCH_H)
    ax0, ax1, ay0, ay1, at = SCH_ARM
    S["Schlitten-Arm"] = solid_box(fr, ax0, ax1, ay0, ay1, sb, sb + at)
    S["LM8UU"] = solid_cyl(fr, *WELLE_XY, LM_D / 2, sb + LM_OFF, sb + LM_OFF + LM_L)
    S["Flanschmutter"] = solid_cyl(fr, *SPINDEL_XY, MUTTER_D / 2, sb, sb + MUTTER_T)
    S["Magnet"] = solid_cyl(fr, 0, 0, 5, sb, sb + 3)
    S["Endschalter"] = solid_box(fr, *SCHALTER_XY[:2], *SCHALTER_XY[2:], *SCHALTER_S)
    return S


SCHLITTEN = ["Schlitten-Block", "Schlitten-Arm", "LM8UU", "Flanschmutter", "Magnet"]
# gewollte Berührungen / Einbauten (keine Kollision im Sinn der Prüfung)
GEWOLLT = {frozenset(p) for p in [
    ("Düse", "Zylinder"), ("Zylinder", "Flansch"),
    ("Kolbenplatte", "Kolbenstange"), ("Kolbenplatte", "Stahlscheibe"),
    ("Kolbenstange", "Zylinder"), ("Kolbenstange", "Flansch"),
    ("Spindel", "Flanschmutter"), ("Welle", "LM8UU"), ("Welle", "Schlitten-Block"),
    ("Spindel", "Schlitten-Block"), ("Flanschmutter", "Schlitten-Block"), ("LM8UU", "Schlitten-Block"),
    ("Magnet", "Schlitten-Arm"), ("Magnet", "Schlitten-Block"), ("Schlitten-Arm", "Schlitten-Block"),
    ("Spindel", "Kupplung")]}

SIN36 = math.sin(math.radians(36))


def zyl_luft(s):
    return 2 * r_ax(s) * SIN36 - ZYL_D


def pruefung():
    print("=" * 78)
    print("PRÜFUNG nach saeule_parameter.md, Stand 5  (Maße in mm, negativ = Durchdringung)")
    print("=" * 78)
    frs = [station_frame(a) for a in ST_WINKEL]
    fr = frs[0]
    mitte = (SB_MIN + SB_MAX) / 2
    # 1 Düsenradius
    tip = fr.w((0, 0, 0))
    ok = all(abs(r_ax(s) - np.hypot(*fr.w((0, 0, s))[:2])) < 1e-9 for s in (0, 15, 140, 308, 348))
    print("[1] Düsenradius: %.2f  (Düsenspitze Z %.2f; Blatt 32 / 105; Achsformel gegen Frame %s)"
          % (math.hypot(tip[0], tip[1]), tip[2], "ok" if ok else "ABWEICHUNG"))
    # 2 Motorecke gegen Innenradius
    ec = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for s in (MOTOR_S0, MOTOR_S1):
                p = fr.w((MOTOR_XY[0] + sx * NEMA / 2, MOTOR_XY[1] + sy * NEMA / 2, s))
                ec.append((math.hypot(p[0], p[1]), p[2], s))
    r_fl = max(c[0] for c in ec if c[2] == MOTOR_S0)
    r_top = max(c[0] for c in ec if c[2] == MOTOR_S1)
    zmax = max(c[1] for c in ec)
    print("[2] Motorecke (Radius zur Säulenachse): Flanschebene s 308 = %.2f, Oberseite s 348 = %.2f (Blatt 97,9 bei s 308, 100,7 oben)"
          % (r_fl, r_top))
    print("    gegen Innenradius %.1f: Luft Flanschebene %+.2f, Oberseite %+.2f" % (R_I, R_I - r_fl, R_I - r_top))
    # 3 Motorabstand Körper zu Körper
    def mbox(f):
        return solid_box(f, MOTOR_XY[0] - NEMA / 2, MOTOR_XY[0] + NEMA / 2, MOTOR_XY[1] - NEMA / 2,
                         MOTOR_XY[1] + NEMA / 2, MOTOR_S0, MOTOR_S1)
    gm = gap(mbox(frs[0]), mbox(frs[1]), 0.5)
    c0, c1 = frs[0].w((*MOTOR_XY, 328)), frs[1].w((*MOTOR_XY, 328))
    print("[3] Motorabstand Körper zu Körper (36° gegen 108°): %+.2f  (Achsabstand %.1f, Blatt: Luft 45)"
          % (gm, np.linalg.norm(c1 - c0)))
    # 4 Zylinder
    gz = gap(station_solids(frs[0], SB_MIN)["Zylinder"], station_solids(frs[1], SB_MIN)["Zylinder"], 0.7)
    print("[4] Luft zwischen Zylindern Ø30: s=15 %+.2f (r %.2f), s=140 %+.2f (r %.2f); Blatt 8,8 / -;"
          " Zylinder gegen Zylinder (3D) %+.2f" % (zyl_luft(15), r_ax(15), zyl_luft(140), r_ax(140), gz))
    # 5 Kolbenplatte gegen Welle und Spindel
    gw = min(gap(station_solids(fr, sb)["Kolbenplatte"], station_solids(fr, sb)["Welle"], 0.7)
             for sb in (SB_MIN, mitte, SB_MAX))
    gs = min(gap(station_solids(fr, sb)["Kolbenplatte"], station_solids(fr, sb)["Spindel"], 0.7)
             for sb in (SB_MIN, mitte, SB_MAX))
    print("[5] Luft Kolbenplatte Ø30 zu Welle %+.2f und zu Spindel %+.2f (Achsabstand %.1f / %.1f)"
          % (gw, gs, math.hypot(*WELLE_XY), math.hypot(*SPINDEL_XY)))
    # 6 Kupplung gegen Motor und gegen Schlitten oben
    S = station_solids(fr, SB_MAX)
    gkm = gap(S["Kupplung"], S["Motor"], 0.5)
    gks = {nm: gap(S["Kupplung"], S[nm], 0.7) for nm in SCHLITTEN}
    nm_min = min(gks, key=gks.get)
    print("[6] Kupplung (s 275..300) gegen Motor (s 308..348): %+.2f  (Motorplatte s 300..308 dazwischen)" % gkm)
    print("    Kupplung gegen Schlitten in oberster Stellung (Unterkante s %.0f, Oberkante %.0f): %+.2f (%s)"
          % (SB_MAX, SB_MAX + SCH_H, gks[nm_min], nm_min))
    print("    Kupplung gegen Welle %+.2f, gegen Endschalter %+.2f"
          % (gap(S["Kupplung"], S["Welle"], 0.7), gap(S["Kupplung"], S["Endschalter"], 0.7)))
    # 7 Schlitten gegen Nachbarstation
    paare = {}
    sbs = (SB_MIN, mitte, SB_MAX)
    for sbi in sbs:
        for sbj in sbs:
            A, B = station_solids(frs[0], sbi), station_solids(frs[1], sbj)
            B2, A2 = station_solids(frs[1], sbi), station_solids(frs[0], sbj)
            for na in SCHLITTEN:
                for nb, sol in B.items():
                    g = gap(A[na], sol, 2.0)
                    if g < paare.get((na, nb), (1e9,))[0]:
                        paare[(na, nb)] = (g, sbi, sbj)
                for nb, sol in A2.items():
                    g = gap(B2[na], sol, 2.0)
                    if g < paare.get((na, nb), (1e9,))[0]:
                        paare[(na, nb)] = (g, sbi, sbj)
    print("[7] Schlitten gegen Nachbarstation (kleinste Abstände aller Hubstellungen, Stützpunkte 2 mm):")
    for k, v in sorted(paare.items(), key=lambda kv: kv[1][0])[:4]:
        print("    %-16s gegen %-13s %+6.1f  (Schlitten s=%.0f, Nachbar s=%.0f)" % (k[0], k[1], v[0], v[1], v[2]))
    print("    kleinster Wert: %+.1f   (Schlitten tangential %.1f breit, Blatt höchstens 42)"
          % (min(v[0] for v in paare.values()), SCH_BLOCK[1] - SCH_BLOCK[0]))
    # 8 Motoroberkante gegen Haubeninnenraum
    print("[8] Motoroberkante höchster Punkt Z %.2f gegen Haubeninnenraum %.0f: %+.2f  (Blatt 452)"
          % (zmax, Z_HAUBE_INNEN, Z_HAUBE_INNEN - zmax))
    # 9 weitere Durchdringungen innerhalb einer Station
    print("[9] Weitere Durchdringungen in einer Station (Stützpunktnäherung, Schlitten %.0f/%.0f/%.0f):" % sbs)
    found = {}
    for sbi in sbs:
        Sx = station_solids(fr, sbi)
        names = list(Sx)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if frozenset((names[i], names[j])) in GEWOLLT:
                    continue
                g = gap(Sx[names[i]], Sx[names[j]], 1.0)
                if g < -0.05:
                    k = (names[i], names[j])
                    found[k] = min(found.get(k, 0), g)
    for k, v in sorted(found.items(), key=lambda kv: kv[1]):
        print("    %-14s gegen %-16s %+6.1f" % (k[0], k[1], v))
    if not found:
        print("    keine")
    # 10 Flansch und radialer Einschubweg
    S0, S1 = station_solids(frs[0], SB_MIN), station_solids(frs[1], SB_MIN)
    gf = gap(S0["Flansch"], S1["Flansch"], 0.5)
    print("[10] Flansch 45 x 32 gegen Nachbarflansch: %+.2f  (Blatt: Ecken etwa 6 auseinander)" % gf)
    BIG = 130.0

    def verschoben(f, t):
        return Frame(f.O + t * f.A[1], f.A)

    def sbox(f, x0, x1, y0, y1, s0, s1):
        return solid_box(f, x0, x1, y0, y1, s0, s1)

    ts = list(range(0, 141, 10))
    # Schlitz 31 gegen Zylinder 30 (Plattenmaterial neben dem Schlitz, Zylinder schiebt nach außen)
    wl = [sbox(fr, DURCHLASS_D / 2, 60, 0, BIG, *S_HALTER), sbox(fr, -60, -DURCHLASS_D / 2, 0, BIG, *S_HALTER)]
    g_sl = min(gap(solid_cyl(verschoben(fr, t), 0, 0, ZYL_D / 2, *S_ZYL), w, 1.0) for t in ts for w in wl)
    # Tasche 45,6 x 32,6 gegen Flansch 45 x 32: Seitenwände, Anschlag innen, Boden (Plattenmaterial unter der Tasche)
    tw = {"Wand": [sbox(fr, TASCHE_X / 2, 60, -TASCHE_Y / 2, BIG, TASCHE_BODEN, S_HALTER[1]),
                   sbox(fr, -60, -TASCHE_X / 2, -TASCHE_Y / 2, BIG, TASCHE_BODEN, S_HALTER[1])],
          "Anschlag": [sbox(fr, -60, 60, -60, -TASCHE_Y / 2, TASCHE_BODEN, S_HALTER[1])],
          "Boden": [sbox(fr, DURCHLASS_D / 2, 60, -TASCHE_Y / 2, BIG, S_HALTER[0], TASCHE_BODEN),
                    sbox(fr, -60, -DURCHLASS_D / 2, -TASCHE_Y / 2, BIG, S_HALTER[0], TASCHE_BODEN)]}
    g_ta = {}
    for nm, bl in tw.items():
        g_ta[nm] = min(gap(sbox(verschoben(fr, t), -FL_X / 2, FL_X / 2, -FL_Y / 2, FL_Y / 2, *S_FLANSCH), w, 0.7)
                       for t in ts for w in bl)
    print("     Schlitz 31 gegen Zylinder 30: %+.2f je Seite;  Tasche gegen Flansch: Wand %+.2f, Anschlag %+.2f, Boden %+.2f"
          % (g_sl, g_ta["Wand"], g_ta["Anschlag"], g_ta["Boden"]))
    # Tragsäulen gegen Einschubweg (alle fünf Stationen, Zylinder und Flansch) und gegen Motoren
    saeulen = []
    for a in SAEULE_WINKEL:
        x_, y_ = SAEULE_R * math.cos(math.radians(a)), SAEULE_R * math.sin(math.radians(a))
        saeulen.append({"t": "cyl", "p0": np.array([x_, y_, Z_SOCKEL1]), "p1": np.array([x_, y_, PLATTE_Z0]),
                        "R": SAEULE_D / 2})
    g_se, wo = 1e9, ""
    for k_, f in enumerate(frs):
        for t in ts:
            for nm, mk in (("Zylinder", lambda ff: solid_cyl(ff, 0, 0, ZYL_D / 2, *S_ZYL)),
                           ("Flansch", lambda ff: sbox(ff, -FL_X / 2, FL_X / 2, -FL_Y / 2, FL_Y / 2, *S_FLANSCH))):
                for ia, sa in enumerate(saeulen):
                    g_ = gap(mk(verschoben(f, t)), sa, 2.0)
                    if g_ < g_se:
                        g_se, wo = g_, "%s %d° gegen Säule %d°" % (nm, ST_WINKEL[k_], SAEULE_WINKEL[ia])
    g_sm = min(gap(sa, mbox(f), 1.0) for sa in saeulen for f in frs)
    print("     Tragsäulen Ø10 gegen Einschubweg: %+.2f (%s);  gegen Motoren: %+.2f (Säulenoberkante Z %.0f, Motorflansch ab Z %.1f)"
          % (g_se, wo, g_sm, PLATTE_Z0, min(c[1] for c in ec if c[2] == MOTOR_S0)))
    # Hülsenöffnung gegen den Einschubweg (Station 36°, Öffnung davor) und gegen die Halterplatte
    a0 = math.radians(ST_WINKEL[0])
    perp = np.array([-math.sin(a0), math.cos(a0)])
    marg = {"unten": 1e9, "oben": 1e9, "breite": 1e9}
    for t in range(0, 141, 2):
        Sv = station_solids(verschoben(fr, t), SB_MAX)
        for nm in ("Düse", "Zylinder", "Flansch", "Kolbenplatte", "Stahlscheibe", "Kolbenstange"):
            Pp = samples(Sv[nm], 2.0)
            rho = np.hypot(Pp[:, 0], Pp[:, 1])
            Q = Pp[(rho >= R_I) & (rho <= R_A)]
            if len(Q):
                marg["unten"] = min(marg["unten"], (Q[:, 2] - OEFF_Z0).min())
                marg["oben"] = min(marg["oben"], (OEFF_Z1 - Q[:, 2]).min())
                marg["breite"] = min(marg["breite"], (OEFF_B / 2 - np.abs(Q[:, :2] @ perp)).min())
    print("     Hülsenöffnung (60 breit, Z %.0f..%.0f) gegen Einschubweg der Spritze samt Kolben: unten %+.1f, oben %+.1f, seitlich %+.1f"
          % (OEFF_Z0, OEFF_Z1, marg["unten"], marg["oben"], marg["breite"]))
    print("     Hülsenöffnung gegen Halterplatte (Z %.0f..%.0f): Reserve unten %+.1f, oben %+.1f; Plattenrand r %.1f gegen Hülse innen %.1f: %+.1f"
          % (HALT_Z0, HALT_Z1, HALT_Z0 - OEFF_Z0, OEFF_Z1 - HALT_Z1, HALT_D / 2, R_I, R_I - HALT_D / 2))
    # Info: Kolben (Platte, Stange) auf dem Einschubweg gegen Welle und Spindel
    Sst = station_solids(fr, SB_MAX)
    gk = {}
    for nm in ("Kolbenplatte", "Kolbenstange"):
        for ob in ("Welle", "Spindel"):
            gk[(nm, ob)] = min(gap(station_solids(verschoben(fr, t), SB_MAX)[nm], Sst[ob], 1.0) for t in range(0, 61, 4))
    print("     Info Kolben auf dem Einschubweg (Schlitten oben): Kolbenplatte gegen Welle %+.1f, Spindel %+.1f; Kolbenstange gegen Welle %+.1f, Spindel %+.1f"
          % (gk[("Kolbenplatte", "Welle")], gk[("Kolbenplatte", "Spindel")], gk[("Kolbenstange", "Welle")], gk[("Kolbenstange", "Spindel")]))
    # Halterplatte (Stern): Steg Mittelloch und Tragsäulenbohrung zur Tasche
    mloch = {"t": "cyl", "p0": np.array([0, 0, HALT_Z0]), "p1": np.array([0, 0, HALT_Z1]), "R": LOCH_D / 2}
    tvoll = lambda f: sbox(f, -TASCHE_X / 2, TASCHE_X / 2, -TASCHE_Y / 2, BIG, TASCHE_BODEN, S_HALTER[1])
    w_m = min(gap(mloch, tvoll(f), 0.7) for f in frs)
    bohr = [{"t": "cyl", "p0": sa["p0"] * [1, 1, 0] + [0, 0, HALT_Z0], "p1": sa["p0"] * [1, 1, 0] + [0, 0, HALT_Z1], "R": 2.1}
            for sa in saeulen]
    w_b = min(gap(b, tvoll(f), 0.7) for b in bohr for f in frs)
    print("     Halterplatte Ø%.0f (Stern): Steg Mittelloch Ø%.0f zur Tasche %+.2f, Bohrung Ø4,2 (r 90) zur Tasche %+.2f, Plattenrand zur Bohrung %.1f;"
          " Flansch-Unterkante s %.0f gegen Taschenboden %.1f: %+.1f"
          % (HALT_D, LOCH_D, w_m, w_b, HALT_D / 2 - SAEULE_R - 2.1, S_FLANSCH[0], TASCHE_BODEN, S_FLANSCH[0] - TASCHE_BODEN))
    # Motorflansch gegen Ringplatte
    xs = np.linspace(-NEMA / 2, NEMA / 2, 85) + MOTOR_XY[0]
    ys = np.linspace(-NEMA / 2, NEMA / 2, 85) + MOTOR_XY[1]
    XX, YY = np.meshgrid(xs, ys)
    P = fr.w(np.stack([XX.ravel(), YY.ravel(), np.full(XX.size, MOTOR_S0)], 1))
    rr = np.hypot(P[:, 0], P[:, 1])
    im = (rr > PLATTE_ID / 2) & (rr < PLATTE_AD / 2) & (P[:, 2] < PLATTE_Z1)
    tief = (PLATTE_Z1 - P[im, 2]).max() if im.any() else 0.0
    print("     Motorflansch-Unterseite (s 308) gegen Ringplatte (Oberkante Z %.0f, r %.0f..%.0f): %+.2f;"
          " tiefste Flanschecke Z %.2f, niedrige Keilseite %+.2f über Ringoberkante (Blatt: mindestens +6)"
          % (PLATTE_Z1, PLATTE_ID / 2, PLATTE_AD / 2, -tief if tief > 0 else 0.0, P[:, 2].min(), P[:, 2].min() - PLATTE_Z1))
    # 11 größter Radius der Stationsteile ohne Motor
    rm_all, nm_all = 0, ""
    for nm, sol in station_solids(fr, SB_MAX).items():
        if nm == "Motor":
            continue
        Q = samples(sol, 3.0)
        r_ = np.hypot(Q[:, 0], Q[:, 1]).max()
        if r_ > rm_all:
            rm_all, nm_all = r_, nm
    print("[11] Größter Radius aller Stationsteile ohne Motor: %.1f (%s), Innenradius %.1f, Luft %+.1f"
          % (rm_all, nm_all, R_I, R_I - rm_all))
    print("=" * 78)


# ============================================================
# Meshes (lokale Koordinaten)
# ============================================================
class Mesh:
    def __init__(self):
        self.V, self.N, self.F, self.n = [], [], [], 0

    def add(self, V, N, F):
        V, N, F = np.asarray(V, float), np.asarray(N, float), np.asarray(F, int)
        self.V.append(V)
        self.N.append(N)
        self.F.append(F + self.n)
        self.n += len(V)
        return self

    def arrays(self):
        return np.vstack(self.V), np.vstack(self.N), np.vstack(self.F)


def _quad(m, p, nrm):
    m.add(p, [nrm] * 4, [(0, 1, 2), (0, 2, 3)])


def cyl(cx, cy, R, z0, z1, n=28, caps=(True, True)):
    m = Mesh()
    th = np.linspace(0, 2 * np.pi, n + 1)
    c, s = np.cos(th), np.sin(th)
    bot = np.stack([cx + R * c, cy + R * s, np.full(n + 1, z0)], 1)
    top = bot.copy()
    top[:, 2] = z1
    nn = np.stack([c, s, np.zeros(n + 1)], 1)
    i, k = np.arange(n), n + 1
    F = np.concatenate([np.stack([i, i + 1, k + i + 1], 1), np.stack([i, k + i + 1, k + i], 1)])
    m.add(np.vstack([bot, top]), np.vstack([nn, nn]), F)
    for z, nz, on in ((z0, -1, caps[0]), (z1, 1, caps[1])):
        if on:
            ring = bot[:n].copy()
            ring[:, 2] = z
            m.add(np.vstack([[cx, cy, z], ring]), np.tile([0, 0, nz], (n + 1, 1)),
                  np.stack([np.zeros(n, int), 1 + i, 1 + (i + 1) % n], 1))
    return m


def box(x0, x1, y0, y1, z0, z1):
    m = Mesh()
    _quad(m, [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], (1, 0, 0))
    _quad(m, [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)], (-1, 0, 0))
    _quad(m, [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)], (0, 1, 0))
    _quad(m, [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], (0, -1, 0))
    _quad(m, [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1))
    _quad(m, [(x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0)], (0, 0, -1))
    return m


def revolve(profile, n=96, cx=0.0, cy=0.0):
    """Drehkörper um die lokale z-Achse. profile = [(r, z)], Außennormale = (dz, -dr)."""
    m = Mesh()
    th = np.linspace(0, 2 * np.pi, n + 1)
    c, s = np.cos(th), np.sin(th)
    i = np.arange(n)
    for (r0, z0), (r1, z1) in zip(profile[:-1], profile[1:]):
        ln = math.hypot(r1 - r0, z1 - z0)
        if ln < 1e-9:
            continue
        nr, nz = (z1 - z0) / ln, -(r1 - r0) / ln
        a = np.stack([cx + r0 * c, cy + r0 * s, np.full(n + 1, z0)], 1)
        b = np.stack([cx + r1 * c, cy + r1 * s, np.full(n + 1, z1)], 1)
        nn = np.stack([nr * c, nr * s, np.full(n + 1, nz)], 1)
        k = n + 1
        F = np.concatenate([np.stack([i, i + 1, k + i + 1], 1), np.stack([i, k + i + 1, k + i], 1)])
        m.add(np.vstack([a, b]), np.vstack([nn, nn]), F)
    return m


def shell_surface(R, sign, th_edges, z_edges, mask=None):
    th = np.radians(th_edges)
    nth, nz = len(th) - 1, len(z_edges) - 1
    TH, ZZ = np.meshgrid(th, z_edges)
    V = np.stack([R * np.cos(TH), R * np.sin(TH), ZZ], -1).reshape(-1, 3)
    Nn = np.stack([sign * np.cos(TH), sign * np.sin(TH), 0 * TH], -1).reshape(-1, 3)
    J, I = np.meshgrid(np.arange(nz), np.arange(nth), indexing="ij")
    idx = lambda j, i: j * (nth + 1) + i
    a, b, c, d = idx(J, I), idx(J, I + 1), idx(J + 1, I + 1), idx(J + 1, I)
    keep = np.ones(J.shape, bool)
    if mask is not None:
        thc = np.degrees((th[:-1] + th[1:]) / 2)[None, :] + 0 * J
        zc = ((np.asarray(z_edges)[:-1] + np.asarray(z_edges)[1:]) / 2)[:, None] + 0 * I
        keep = ~mask(thc, zc)
    F = np.concatenate([np.stack([a, b, c], -1)[keep], np.stack([a, c, d], -1)[keep]])
    return Mesh().add(V, Nn, F)


def rect_r(hx, hy):
    return lambda th: np.minimum(hx / np.maximum(np.abs(np.cos(th)), 1e-9), hy / np.maximum(np.abs(np.sin(th)), 1e-9))


def circ_r(R):
    return lambda th: np.full_like(th, R)


def ring_prism(outer, inner, z0, z1, corners=(), n=96):
    th = np.concatenate([np.linspace(0, 2 * np.pi, n, endpoint=False), np.asarray(corners, float) % (2 * np.pi)])
    th = np.sort(th)
    th = np.append(th, th[0] + 2 * np.pi)
    ro, ri = outer(th), inner(th)
    ox, oy, ix, iy = ro * np.cos(th), ro * np.sin(th), ri * np.cos(th), ri * np.sin(th)
    K = len(th) - 1
    i, k = np.arange(K), K + 1
    m = Mesh()
    for z, nz in ((z1, 1), (z0, -1)):
        V = np.vstack([np.stack([ox, oy, np.full(K + 1, z)], 1), np.stack([ix, iy, np.full(K + 1, z)], 1)])
        F = np.concatenate([np.stack([i, i + 1, k + i + 1], 1), np.stack([i, k + i + 1, k + i], 1)])
        m.add(V, np.tile([0, 0, nz], (2 * k, 1)), F)
    for px, py, sg in ((ox, oy, 1), (ix, iy, -1)):
        for j in range(K):
            ex, ey = px[j + 1] - px[j], py[j + 1] - py[j]
            ln = math.hypot(ex, ey)
            if ln < 1e-9:
                continue
            _quad(m, [(px[j], py[j], z0), (px[j + 1], py[j + 1], z0), (px[j + 1], py[j + 1], z1), (px[j], py[j], z1)],
                  (sg * ey / ln, -sg * ex / ln, 0))
    return m


def poly_prism(top, bot):
    """Prisma aus vier Deck- und vier Bodenpunkten (Weltkoordinaten), flache Normalen nach außen."""
    top, bot = [np.asarray(p, float) for p in top], [np.asarray(p, float) for p in bot]
    cen = (sum(top) + sum(bot)) / 8
    m = Mesh()
    faces = [top, bot[::-1]] + [[top[i], top[(i + 1) % 4], bot[(i + 1) % 4], bot[i]] for i in range(4)]
    for f in faces:
        nrm = np.cross(f[1] - f[0], f[2] - f[0])
        nrm /= np.linalg.norm(nrm)
        if np.dot(nrm, sum(f) / 4 - cen) < 0:
            nrm = -nrm
        _quad(m, f, nrm)
    return m


# ============================================================
# Szene
# ============================================================
class Item:
    def __init__(self, V, N, F, rgb, alpha, pid, ks, grp):
        self.V, self.N, self.F, self.rgb, self.alpha, self.pid, self.ks, self.grp = V, N, F, rgb, alpha, pid, ks, grp


class Scene:
    def __init__(self):
        self.items, self._pid = [], 0

    def nid(self):
        self._pid += 1
        return self._pid

    def add(self, mesh, grp, color, alpha=1.0, pid=None, ks=0.0, frame=None):
        V, N, F = mesh.arrays()
        if frame is not None:
            V, N = frame.w(V), frame.n(N)
        self.items.append(Item(V, N, F, np.array(to_rgb(color)), alpha, self.nid() if pid is None else pid, ks, grp))


def window_inside(th_deg, z):
    th = np.radians(th_deg)
    u = R_A * np.sin(th)
    cz = FENSTER_Z0 + FENSTER_H - FENSTER_B / 2
    ok = (np.abs(th_deg) <= 90) & (np.abs(u) <= FENSTER_B / 2) & (z >= FENSTER_Z0)
    return ok & ((z <= cz) | (u ** 2 + (z - cz) ** 2 <= (FENSTER_B / 2) ** 2))


def fenster_umriss(d, k=24):
    w, R = FENSTER_B / 2 + d, FENSTER_B / 2 + d
    zb, cz = max(FENSTER_Z0 - d, FUSS_H), FENSTER_Z0 + FENSTER_H - FENSTER_B / 2
    pts = [(w, zb), (w, cz)]
    for j in range(1, k):
        t = math.pi * j / k
        pts.append((R * math.cos(t), cz + R * math.sin(t)))
    pts += [(-w, cz), (-w, zb)]
    return pts


def rahmen_mesh():
    """Messingrahmen: Frontfläche 4 mm breit um das Fenster, plus Innen- und Außenlippe."""
    d_in, d_out = -0.8, -0.8 + RAHMEN_B
    a, b = fenster_umriss(d_in), fenster_umriss(d_out)
    rf = R_A + 0.8
    cw = np.array([R_A, 0.0, FENSTER_Z0 + FENSTER_H / 2])
    m = Mesh()

    def pt(u, z, r):
        ph = math.asin(u / R_A)
        return np.array([r * math.cos(ph), r * math.sin(ph), z])

    def quad(p, mode):
        p = [np.asarray(q) for q in p]
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
        _quad(m, p, nrm)

    for i in range(len(a)):
        j = (i + 1) % len(a)
        quad([pt(*a[i], rf), pt(*a[j], rf), pt(*b[j], rf), pt(*b[i], rf)], "front")
        quad([pt(*a[i], rf), pt(*a[j], rf), pt(*a[j], R_I), pt(*a[i], R_I)], "in")
        quad([pt(*b[i], rf), pt(*b[j], rf), pt(*b[j], R_A - 0.2), pt(*b[i], R_A - 0.2)], "out")
    return m




def halter_mesh(dr=1.0, nth=420):
    """Halterplatte als Stern: Scheibe x 14 (Welt-Z 233..247) mit Mittelloch und fünf um 4 Grad geneigten radialen
    Schlitzen 31 breit, dazu Flanschtaschen (nach außen offen). Polargitter, Zellen innerhalb von Loch oder Tasche werden
    ausgespart; Höhenfeld mit Seitenwänden (Welt-Koordinaten)."""
    Rh = HALT_D / 2
    nr = int(round(Rh / dr))
    rr = np.linspace(0, Rh, nr + 1)
    th = np.linspace(0, 2 * np.pi, nth + 1)
    rc, tc = (rr[:-1] + rr[1:]) / 2, (th[:-1] + th[1:]) / 2
    RC, TC = np.meshgrid(rc, tc, indexing="ij")
    zm = (HALT_Z0 + HALT_Z1) / 2
    hole = np.zeros(RC.shape, bool)
    pocket = np.zeros(RC.shape, bool)
    for a in ST_WINKEL:
        f = station_frame(a)
        P = np.stack([RC * np.cos(TC), RC * np.sin(TC), np.full(RC.shape, zm)], -1)
        L = (P - f.O) @ f.A.T
        lx, ly = L[..., 0], L[..., 1]
        hole |= (lx ** 2 + ly ** 2 <= (DURCHLASS_D / 2) ** 2) | ((np.abs(lx) <= DURCHLASS_D / 2) & (ly >= 0))
        pocket |= (np.abs(lx) <= TASCHE_X / 2) & (ly >= -TASCHE_Y / 2)
    hole |= RC <= LOCH_D / 2
    z_floor = HALT_Z1 - TASCHE_T
    top = np.where(hole, HALT_Z0, np.where(pocket, z_floor, HALT_Z1))
    solid = ~hole
    m = Mesh()
    k = nth + 1
    I, J = np.meshgrid(np.arange(nr), np.arange(nth), indexing="ij")

    def grid(z):
        R_, T_ = np.meshgrid(rr, th, indexing="ij")
        return np.stack([R_ * np.cos(T_), R_ * np.sin(T_), np.full(R_.shape, float(z))], -1).reshape(-1, 3)

    def faces(sel):
        a, b, c, d = I[sel] * k + J[sel], I[sel] * k + J[sel] + 1, (I[sel] + 1) * k + J[sel] + 1, (I[sel] + 1) * k + J[sel]
        return np.concatenate([np.stack([a, b, c], 1), np.stack([a, c, d], 1)])

    for z, sel, nz in ((HALT_Z1, solid & ~pocket, 1), (z_floor, solid & pocket, 1), (HALT_Z0, solid, -1)):
        if sel.any():
            V = grid(z)
            m.add(V, np.tile([0.0, 0.0, nz], (len(V), 1)), faces(sel))
    # Seitenwände: zwischen Zellen verschiedener Höhe und am Rand
    quads, normals = [], []

    def wall(p0, p1, zl, zh, n):
        quads.append([(p0[0], p0[1], zl), (p1[0], p1[1], zl), (p1[0], p1[1], zh), (p0[0], p0[1], zh)])
        normals.append(n)

    pad = np.vstack([top, np.full((1, nth), HALT_Z0)])      # außerhalb des Randes: Höhe Z0
    for i in range(nr):
        for j in range(nth):
            a, b = pad[i, j], pad[i + 1, j]                  # radial nach außen
            if a != b:
                r_, t0, t1 = rr[i + 1], th[j], th[j + 1]
                sg = 1.0 if a > b else -1.0
                wall((r_ * math.cos(t0), r_ * math.sin(t0)), (r_ * math.cos(t1), r_ * math.sin(t1)),
                     min(a, b), max(a, b), (sg * math.cos(tc[j]), sg * math.sin(tc[j]), 0.0))
            a, b = top[i, j], top[i, (j + 1) % nth]          # tangential
            if a != b:
                t_, r0, r1 = th[j + 1], rr[i], rr[i + 1]
                sg = 1.0 if a > b else -1.0
                wall((r0 * math.cos(t_), r0 * math.sin(t_)), (r1 * math.cos(t_), r1 * math.sin(t_)),
                     min(a, b), max(a, b), (-sg * math.sin(t_), sg * math.cos(t_), 0.0))
    if quads:
        Q = np.asarray(quads, float).reshape(-1, 3)
        Nn = np.repeat(np.asarray(normals, float), 4, axis=0)
        n = len(quads)
        F = np.concatenate([np.stack([4 * np.arange(n), 4 * np.arange(n) + 1, 4 * np.arange(n) + 2], 1),
                            np.stack([4 * np.arange(n), 4 * np.arange(n) + 2, 4 * np.arange(n) + 3], 1)])
        m.add(Q, Nn, F)
    return m


def oeffnung_kanten(d_deg):
    """Wandstärke an den Kanten der Hülsenöffnung (Seiten, Unter- und Oberkante)."""
    m = Mesh()
    t0, t1 = math.radians(OEFF_WINKEL - d_deg), math.radians(OEFF_WINKEL + d_deg)
    P = lambda t, R, z: (R * math.cos(t), R * math.sin(t), z)
    for t, sg in ((t0, 1.0), (t1, -1.0)):
        _quad(m, [P(t, R_I, OEFF_Z0), P(t, R_A, OEFF_Z0), P(t, R_A, OEFF_Z1), P(t, R_I, OEFF_Z1)],
              (-sg * math.sin(t), sg * math.cos(t), 0.0))
    ts = np.linspace(t0, t1, 14)
    for z, nz in ((OEFF_Z0, 1.0), (OEFF_Z1, -1.0)):
        for ta, tb in zip(ts[:-1], ts[1:]):
            _quad(m, [P(ta, R_I, z), P(ta, R_A, z), P(tb, R_A, z), P(tb, R_I, z)], (0.0, 0.0, nz))
    return m


def build_scene():
    sc = Scene()
    # Tisch (Z = 0) und weicher Kontaktschatten
    sc.add(revolve([(155, 0), (0, 0)], 96), "ground", "#eceef1")
    sc.add(revolve([(126, 0.05), (0, 0.05)], 96), "ground", "#d9dce1")
    # Fuß, dunkelgrau
    sc.add(revolve([(0, 0), (FUSS_D / 2, 0), (FUSS_D / 2, 21), (FUSS_D / 2 - 3.5, FUSS_H), (0, FUSS_H)], 120),
           "fuss", C_DUNKEL, ks=0.12)
    # Becherraum-Boden und Becher
    sc.add(revolve([(0, FUSS_H), (BR_D / 2, FUSS_H), (BR_D / 2, BECHER_Z0), (0, BECHER_Z0)], 72),
           "becher", "#2f3237")
    sc.add(cyl(0, 0, BECHER_D / 2 - 0.6, BECHER_Z0, BECHER_Z0 + 2.0, 56), "becher", "#dbe6ee")
    sc.add(cyl(0, 0, BECHER_D / 2, BECHER_Z0, BECHER_Z0 + BECHER_H, 72, (False, False)), "becher", "#9fc4dc",
           alpha=0.38, ks=0.2)
    sc.add(revolve([(BECHER_D / 2 - 1.8, BECHER_Z0 + BECHER_H - 0.8), (BECHER_D / 2 + 0.2, BECHER_Z0 + BECHER_H - 0.8),
                    (BECHER_D / 2 + 0.2, BECHER_Z0 + BECHER_H), (BECHER_D / 2 - 1.8, BECHER_Z0 + BECHER_H),
                    (BECHER_D / 2 - 1.8, BECHER_Z0 + BECHER_H - 0.8)], 72), "becher", "#7fa9c4")
    # Sockelschale mit Fenster und Laufring (Lippe 3 breit) für die Hülse
    th_c = np.unique(np.concatenate([np.arange(-180, -36 + 1e-9, 3.0), np.linspace(-36, 36, 121),
                                     np.arange(36, 180 + 1e-9, 3.0)]))
    z_sock = np.linspace(FUSS_H, Z_SOCKEL1, 64)
    for R, sg, col in ((R_A, 1, C_CREME), (R_I, -1, C_CREME_IN)):
        sc.add(shell_surface(R, sg, th_c, z_sock, window_inside), "sockel", col, pid=sc.nid() if sg > 0 else None)
    pid_sock = sc.items[-2].pid
    sc.items[-1].pid = pid_sock
    sc.add(ring_prism(circ_r(R_I), circ_r(R_I - 3.0), Z_SOCKEL1 - 4.0, Z_SOCKEL1), "sockel", C_CREME_IN, pid=pid_sock)
    # Drehhülse Z 120 bis 300 am Stück, Öffnung 60 breit von Z 150 bis 290 bei 36 Grad
    d_oeff = math.degrees(math.asin(OEFF_B / 2 / R_A))
    th_h = np.unique(np.concatenate([np.arange(-180, 180 + 1e-9, 2.0), [OEFF_WINKEL - d_oeff, OEFF_WINKEL + d_oeff]]))
    z_h = [Z_SOCKEL1, OEFF_Z0, OEFF_Z1, Z_MITTE1]
    oeff = lambda thc, zc: (np.abs(thc - OEFF_WINKEL) <= d_oeff) & (zc > OEFF_Z0) & (zc < OEFF_Z1)
    pid = sc.nid()
    sc.add(shell_surface(R_A, 1, th_h, z_h, oeff), "huelse", C_CREME, pid=pid)
    sc.add(shell_surface(R_I, -1, th_h, z_h, oeff), "huelse", C_CREME_IN, pid=pid)
    sc.add(oeffnung_kanten(d_oeff), "huelse", C_CREME, pid=pid)
    # Oberschale Z 300 bis 420 (fest), unten Lippe für die Hülse
    pid = sc.nid()
    th = np.linspace(-180, 180, 121)
    z = np.linspace(Z_MITTE1, Z_OBER1, 6)
    sc.add(shell_surface(R_A, 1, th, z), "oberschale", C_CREME, pid=pid)
    sc.add(shell_surface(R_I, -1, th, z), "oberschale", C_CREME_IN, pid=pid)
    sc.add(revolve([(R_I, Z_OBER1), (R_A, Z_OBER1)], 120), "oberschale", C_CREME, pid=pid)  # Oberkante (Ring)
    sc.add(ring_prism(circ_r(R_I), circ_r(R_I - 3.0), Z_MITTE1, Z_MITTE1 + 4.0), "oberschale", C_CREME_IN, pid=pid)
    # Tragsäulen Ø10 auf Radius 90 (Sockeloberseite bis Motorplatte), durch die Halterplatte läuft die M4-Stange
    for a in SAEULE_WINKEL:
        cx, cy = SAEULE_R * math.cos(math.radians(a)), SAEULE_R * math.sin(math.radians(a))
        pid = sc.nid()
        sc.add(cyl(cx, cy, SAEULE_D / 2, Z_SOCKEL1, HALT_Z0, 24), "saeule", "#8f969f", pid=pid, ks=0.4)
        sc.add(cyl(cx, cy, 2.0, HALT_Z0, HALT_Z1, 12), "saeule", "#b9bec5", pid=pid)
        sc.add(cyl(cx, cy, SAEULE_D / 2, HALT_Z1, PLATTE_Z0, 24), "saeule", "#8f969f", pid=pid, ks=0.4)
    sc.add(rahmen_mesh(), "rahmen", C_MESSING, ks=0.35)
    # Haube (Krone), dunkelgrau
    sc.add(revolve([(R_A, Z_OBER1), (R_A, Z_HAUBE1 - 5), (R_A - 5, Z_HAUBE1), (0, Z_HAUBE1)], 120),
           "haube", C_DUNKEL, ks=0.12)
    # Motorplatte: Ring Ø90 / Ø178, Dicke 8 (Z 404 bis 412)
    sc.add(revolve([(PLATTE_ID / 2, PLATTE_Z0), (PLATTE_AD / 2, PLATTE_Z0), (PLATTE_AD / 2, PLATTE_Z1),
                    (PLATTE_ID / 2, PLATTE_Z1), (PLATTE_ID / 2, PLATTE_Z0)], 120), "platte", "#c7cbd1")
    # Halterplatte: eine Scheibe für alle fünf Stationen
    sc.add(halter_mesh(), "halter", "#2f8f8a", ks=0.15)
    # Stationen
    for k, a in enumerate(ST_WINKEL):
        build_station(sc, a, ST_NAMEN[k])
    return sc


def build_station(sc, a_deg, name):
    fr = station_frame(a_deg)
    sb = SB_MIN + FUELL * (SB_MAX - SB_MIN)
    spl = sb - KOLB_T - DISC_T                  # Kolbenplatte Unterkante (Scheibe endet an der Schlittenunterseite)
    rub1 = spl - STANGE_L                       # Oberkante Gummi
    rub0 = rub1 - GUMMI_T
    g = "station"
    # Düse
    sc.add(cyl(0, 0, 2, *S_DUESE, 16), g, "#d2d6db", frame=fr, ks=0.3)
    # Inhalt (Spritze), Gummistopfen
    sc.add(cyl(0, 0, ZYL_D / 2 - 0.9, S_ZYL[0] + 0.2, rub0, 40), g, INHALT[name], frame=fr, ks=0.15)
    sc.add(cyl(0, 0, ZYL_D / 2 - 0.9, rub0, rub1, 40), g, "#4a4d52", frame=fr)
    # Kolbenstange (Kreuzprofil), Kolbenplatte, Stahlscheibe
    pid = sc.nid()
    sc.add(box(-STANGE_B / 2, STANGE_B / 2, -STANGE_DICKE / 2, STANGE_DICKE / 2, rub1, spl), g, "#f1f1f1", pid=pid, frame=fr)
    sc.add(box(-STANGE_DICKE / 2, STANGE_DICKE / 2, -STANGE_B / 2, STANGE_B / 2, rub1, spl), g, "#f1f1f1", pid=pid, frame=fr)
    sc.add(cyl(0, 0, KOLB_D / 2, spl, spl + KOLB_T, 40), g, "#f6f6f6", frame=fr)
    sc.add(cyl(0, 0, DISC_D / 2, spl + KOLB_T, spl + KOLB_T + DISC_T, 32), g, "#aeb5bd", frame=fr, ks=0.4)
    # Spritzenzylinder und Flansch (Glas); der Halter ist jetzt die gemeinsame Halterplatte
    sc.add(cyl(0, 0, ZYL_D / 2, *S_ZYL, 48), g, "#d8e6ee", alpha=0.22, frame=fr, ks=0.3)
    sc.add(box(-FL_X / 2, FL_X / 2, -FL_Y / 2, FL_Y / 2, *S_FLANSCH), g, "#e3edf2", alpha=0.55, frame=fr)
    # Welle und Spindel
    sc.add(cyl(*WELLE_XY, WS_D / 2, *WELLE_S, 16), g, "#c9cdd3", frame=fr, ks=0.5)
    sc.add(cyl(*SPINDEL_XY, WS_D / 2, *SPINDEL_S, 16), g, "#b9bec5", frame=fr, ks=0.5)
    # Schlitten (Block, Arm), Mutter in der Unterseite
    pid = sc.nid()
    x0, x1, y0, y1 = SCH_BLOCK
    sc.add(box(x0, x1, y0, y1, sb, sb + SCH_H), g, "#d98c4a", pid=pid, frame=fr)
    ax0, ax1, ay0, ay1, at = SCH_ARM
    sc.add(box(ax0, ax1, ay0, ay1, sb, sb + at), g, "#d98c4a", pid=pid, frame=fr)
    sc.add(cyl(*SPINDEL_XY, MUTTER_D / 2, sb, sb + MUTTER_T, 28), g, C_MESSING, frame=fr, ks=0.3)
    # Kupplung 5 auf 8 unter der Motorplatte
    sc.add(cyl(*SPINDEL_XY, KUPP_D / 2, KUPP_S0, KUPP_S1, 28), g, "#a3abb5", frame=fr, ks=0.5)
    # Endschalter an der Unterseite der Motorplatte
    sc.add(box(*SCHALTER_XY, *SCHALTER_S), g, "#b4574b", frame=fr)
    # Keilförmiger Aufsatz der Motorplatte (Oberseite senkrecht zur Stationsachse) und Motor
    hx, hy = NEMA / 2, NEMA / 2
    cc = [(MOTOR_XY[0] - hx, MOTOR_XY[1] - hy), (MOTOR_XY[0] + hx, MOTOR_XY[1] - hy),
          (MOTOR_XY[0] + hx, MOTOR_XY[1] + hy), (MOTOR_XY[0] - hx, MOTOR_XY[1] + hy)]
    top = [fr.w((x, y, MOTOR_S0)) for x, y in cc]
    bot = [np.array([p[0], p[1], PLATTE_Z0]) for p in top]
    sc.add(poly_prism(top, bot), "platte", "#c7cbd1")
    sc.add(box(MOTOR_XY[0] - hx, MOTOR_XY[0] + hx, MOTOR_XY[1] - hy, MOTOR_XY[1] + hy, MOTOR_S0, MOTOR_S0 + 5),
           "motor", "#8d9097", frame=fr, ks=0.25)
    sc.add(box(MOTOR_XY[0] - hx, MOTOR_XY[0] + hx, MOTOR_XY[1] - hy, MOTOR_XY[1] + hy, MOTOR_S0 + 5, MOTOR_S1 - 4),
           "motor", "#3b3e44", frame=fr)
    sc.add(box(MOTOR_XY[0] - hx, MOTOR_XY[0] + hx, MOTOR_XY[1] - hy, MOTOR_XY[1] + hy, MOTOR_S1 - 4, MOTOR_S1),
           "motor", "#8d9097", frame=fr, ks=0.25)


# ============================================================
# Z-Buffer-Rasterizer
# ============================================================
class View:
    def __init__(self, a_m, elev, S, x0, y0):
        self.a, self.e, self.S, self.x0, self.y0 = math.radians(a_m), math.radians(elev), S, x0, y0
        a, e = self.a, self.e
        self.c = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        self.r = np.array([-math.sin(a), math.cos(a), 0.0])
        self.u = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])

    def px(self, p):
        p = np.asarray(p, float)
        return self.x0 + self.S * (p @ self.r), self.y0 - self.S * (p @ self.u)


def render_panel(sc, groups, view, W, H, ss=2, alpha_over=None, xoff=0):
    alpha_over = alpha_over or {}
    c, r, u = view.c, view.r, view.u
    light = 0.62 * c + 0.55 * u - 0.42 * r
    light /= np.linalg.norm(light)
    hv = light + c
    hv /= np.linalg.norm(hv)
    Ws, Hs, S = W * ss, H * ss, view.S * ss
    img = np.ones((Hs, Ws, 3), np.float32)
    zb = np.full((Hs, Ws), -1e9, np.float32)
    pb = np.full((Hs, Ws), -1, np.int32)
    trans = []

    def prep(it):
        sx = ((view.x0 - xoff) * ss + S * (it.V @ r)).tolist()
        sy = (view.y0 * ss - S * (it.V @ u)).tolist()
        d = (it.V @ c).tolist()
        return sx, sy, d

    def shade(it, nx, ny, nz):
        ln = np.sqrt(nx * nx + ny * ny + nz * nz) + 1e-12
        nx, ny, nz = nx / ln, ny / ln, nz / ln
        sg = np.where(nx * c[0] + ny * c[1] + nz * c[2] < 0, -1.0, 1.0)
        nx, ny, nz = nx * sg, ny * sg, nz * sg
        ndl = np.clip(nx * light[0] + ny * light[1] + nz * light[2], 0, 1)
        col = it.rgb[None, :] * (0.46 + 0.62 * ndl)[:, None]
        if it.ks > 0:
            col = col + (it.ks * np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1) ** 40)[:, None]
        return np.clip(col, 0, 1)

    def tris(it, sx, sy, d, F, N, opaque):
        for i0, i1, i2 in F:
            x0, y0, x1, y1, x2, y2 = sx[i0], sy[i0], sx[i1], sy[i1], sx[i2], sy[i2]
            minx, maxx = max(0, int(math.floor(min(x0, x1, x2)))), min(Ws - 1, int(math.ceil(max(x0, x1, x2))))
            miny, maxy = max(0, int(math.floor(min(y0, y1, y2)))), min(Hs - 1, int(math.ceil(max(y0, y1, y2))))
            if minx > maxx or miny > maxy:
                continue
            den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(den) < 1e-12:
                continue
            gx = np.arange(minx, maxx + 1) + 0.5
            gy = (np.arange(miny, maxy + 1) + 0.5)[:, None]
            w0 = ((y1 - y2) * (gx - x2) + (x2 - x1) * (gy - y2)) / den
            w1 = ((y2 - y0) * (gx - x2) + (x0 - x2) * (gy - y2)) / den
            w2 = 1 - w0 - w1
            m = (w0 >= -1e-5) & (w1 >= -1e-5) & (w2 >= -1e-5)
            if not m.any():
                continue
            z = w0 * d[i0] + w1 * d[i1] + w2 * d[i2]
            zsub = zb[miny:maxy + 1, minx:maxx + 1]
            m &= z > zsub
            if not m.any():
                continue
            a0, a1, a2 = w0[m], w1[m], w2[m]
            n0, n1, n2 = N[i0], N[i1], N[i2]
            col = shade(cur, a0 * n0[0] + a1 * n1[0] + a2 * n2[0], a0 * n0[1] + a1 * n1[1] + a2 * n2[1],
                        a0 * n0[2] + a1 * n1[2] + a2 * n2[2])
            sub = img[miny:maxy + 1, minx:maxx + 1]
            if opaque:
                sub[m] = col
                zsub[m] = z[m]
                pb[miny:maxy + 1, minx:maxx + 1][m] = cur.pid
            else:
                al = cur.alpha
                sub[m] = sub[m] * (1 - al) + col * al

    for it in sc.items:
        if it.grp not in groups:
            continue
        al = alpha_over.get(it.grp, it.alpha)
        cur = Item(it.V, it.N, it.F, it.rgb, al, it.pid, it.ks, it.grp)
        sx, sy, d = prep(cur)
        Nl = cur.N.tolist()
        if al >= 1.0:
            nf = cur.N[cur.F].mean(1)
            vis = (nf @ c) > -0.35
            tris(cur, sx, sy, d, cur.F[vis], Nl, True)
        else:
            dm = np.asarray(d)[cur.F].mean(1)
            for t in range(len(cur.F)):
                trans.append((dm[t], cur, t, sx, sy, d, Nl))
    # Kanten (Teilegrenzen und Silhouette)
    P = pb
    diff = np.zeros(P.shape, bool)
    diff[:, :-1] |= P[:, :-1] != P[:, 1:]
    diff[:, 1:] |= P[:, :-1] != P[:, 1:]
    diff[:-1, :] |= P[:-1, :] != P[1:, :]
    diff[1:, :] |= P[:-1, :] != P[1:, :]
    ed = diff.copy()
    ed[:, 1:] |= diff[:, :-1]
    ed[1:, :] |= diff[:-1, :]
    ed &= P >= 0
    img[ed] *= 0.62
    # Transparente Flächen, von hinten nach vorn
    trans.sort(key=lambda t: t[0])
    for _, cur_, t, sx, sy, d, Nl in trans:
        cur = cur_
        tris(cur, sx, sy, d, cur.F[t:t + 1], Nl, False)
    out = img.reshape(H, ss, W, ss, 3).mean((1, 3))
    return out




# ============================================================
# Hauptprogramm
# ============================================================
def main():
    pruefung()
    if "--pruefung" in sys.argv:
        return
    t0 = time.time()
    sc = build_scene()
    zmin = min(it.V[:, 2].min() for it in sc.items)
    zmax = max(it.V[:, 2].max() for it in sc.items)
    print("Szene: %d Teile, %d Dreiecke, kleinstes Z %.2f, größtes Z %.2f"
          % (len(sc.items), sum(len(it.F) for it in sc.items), zmin, zmax))

    F_FRONT = -20.0
    views = {
        1: View(15.0, 20, 1.28, 330, 775),
        2: View(-35 - F_FRONT, 20, 1.28, 930, 775),
        3: View(0.0, 90, 2.05, 1500, 470),
    }
    g1 = {"ground", "fuss", "becher", "sockel", "huelse", "oberschale", "rahmen", "haube", "platte", "halter", "saeule", "station"}
    g2 = {"ground", "fuss", "becher", "sockel", "rahmen", "platte", "halter", "saeule", "station", "motor"}
    g3 = {"fuss", "becher", "sockel", "huelse", "oberschale", "rahmen", "platte", "halter", "saeule", "station", "motor"}
    canvas = np.ones((900, 1800, 3), np.float32)
    for k, groups, ao in ((1, g1, None), (2, g2, {"sockel": 0.2}), (3, g3, {"motor": 0.3})):
        t1 = time.time()
        canvas[:, (k - 1) * 600:k * 600] = render_panel(sc, groups, views[k], 600, 900, 2, ao, (k - 1) * 600)
        print("  Ansicht %d gerendert in %.1f s" % (k, time.time() - t1))

    fig = plt.figure(figsize=(18, 9), dpi=100, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(canvas, extent=(0, 1800, 900, 0), interpolation="nearest")
    ax.set_xlim(0, 1800)
    ax.set_ylim(900, 0)
    ax.axis("off")
    overlays(ax, views, F_FRONT)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rendering_saeule.png")
    fig.savefig(out, dpi=100, facecolor="white")
    print("geschrieben:", out, " (%.1f s)" % (time.time() - t0))


def dim_h(ax, xa, y0, y1, text, ink, rot=True):
    ax.plot([xa, xa], [y0, y1], color=ink, lw=1.1)
    for y in (y0, y1):
        ax.plot([xa - 6, xa + 6], [y, y], color=ink, lw=1.1)
    ax.text(xa - 10, (y0 + y1) / 2, text, rotation=90, ha="right", va="center", fontsize=12, color=ink)


def dim_w(ax, xl, xr, y, text, ink, dy):
    ax.plot([xl, xr], [y, y], color=ink, lw=1.1)
    for x in (xl, xr):
        ax.plot([x, x], [y - 5, y + 5], color=ink, lw=1.1)
    ax.text((xl + xr) / 2, y + dy, text, ha="center", va="center", fontsize=12, color=ink)


def labels_seite(ax, items, tx, ha, soft, ink, abstand=24):
    """items = [(text, (px, py))]; Textlage am Rand tx, vertikal entzerrt, Führungslinie zum Punkt."""
    items = sorted(items, key=lambda it: it[1][1])
    ys = []
    for _, (_, py_) in items:
        y = py_ if not ys else max(py_, ys[-1] + abstand)
        ys.append(y)
    for (txt, (px_, py_)), ty in zip(items, ys):
        ax.plot([tx + (4 if ha == "right" else -4), px_], [ty, py_], color=soft, lw=0.9)
        ax.plot([px_], [py_], "o", color=soft, ms=3)
        ax.text(tx, ty, txt, ha=ha, va="center", fontsize=11, color=ink)


def overlays(ax, views, F_FRONT):
    ink, soft = "#1f2329", "#59606a"
    ax.text(900, 38, "Farbmischer Säule, Konzept-Rendering", ha="center", va="center", fontsize=22,
            fontweight="bold", color=ink)
    for x, t in ((300, "1  Außenansicht, geschlossen"), (900, "2  Ohne Hülse, Oberschale und Haube"),
                 (1500, "3  Draufsicht ohne Haube")):
        ax.text(x, 80, t, ha="center", va="center", fontsize=13, color="#2b3036")
    for x in (600, 1200):
        ax.plot([x, x], [70, 840], color="#e3e5e8", lw=1)

    v1 = views[1]
    # Höhe 470
    xa, ya = v1.px(-134 * v1.r)
    _, yb = v1.px(-134 * v1.r + np.array([0, 0, Z_HAUBE1]))
    dim_h(ax, xa, ya, yb, "Höhe %.0f" % Z_HAUBE1, ink)
    # Durchmesser 190 oben
    xl, _ = v1.px(-R_A * v1.r)
    xr, _ = v1.px(R_A * v1.r)
    _, yt = v1.px(np.array([0, 0, Z_HAUBE1]))
    ytop = yt - v1.S * R_A * math.sin(v1.e) - 20
    dim_w(ax, xl, xr, ytop, "Durchmesser %.0f" % D_AUSSEN, ink, -14)
    # Fuß 200
    xl, _ = v1.px(-FUSS_D / 2 * v1.r)
    xr, _ = v1.px(FUSS_D / 2 * v1.r)
    _, yf = v1.px(np.array([0, 0, 0.0]))
    yfoot = yf + v1.S * FUSS_D / 2 * math.sin(v1.e) + 22
    dim_w(ax, xl, xr, yfoot, "Fuß %.0f" % FUSS_D, ink, 15)

    ao_ = math.radians(OEFF_WINKEL)
    po = v1.px(np.array([R_A * math.cos(ao_), R_A * math.sin(ao_), 225.0]))
    ax.plot([po[0] + 8, 478], [po[1], po[1]], color=soft, lw=0.9)
    ax.plot([po[0]], [po[1]], "o", color=soft, ms=3)
    ax.text(482, po[1], "Hülsenöffnung\n(Station 36°)", ha="left", va="center", fontsize=11, color=ink)

    # Ansicht 2: Beschriftungen mit Führungslinien, Punkte aus dem Modell
    v2 = views[2]
    sbm = SB_MIN + FUELL * (SB_MAX - SB_MIN)
    f_l, f_r = station_frame(324), station_frame(36)      # vorn links / vorn rechts
    rim = lambda a, R, z: np.array([R * math.cos(math.radians(a)), R * math.sin(math.radians(a)), z])
    links = [("Motor NEMA 17", v2.px(f_l.w((*MOTOR_XY, 328)))),
             ("Motorplatte", v2.px(rim(290, PLATTE_AD / 2, 408))),
             ("Schlitten mit Arm", v2.px(f_l.w((0, SCH_ARM[2], sbm + 4)))),
             ("Halterplatte (Stern) Ø %.0f" % HALT_D, v2.px(rim(290, HALT_D / 2, 240))),
             ("Tragsäule Ø 10", v2.px(rim(216, SAEULE_R, 330)))]
    rechts = [("Kupplung", v2.px(f_r.w((*SPINDEL_XY, 287.5)))),
              ("Spindel, Welle", v2.px(f_r.w((*SPINDEL_XY, 255)))),
              ("Spritze 60 ml", v2.px(f_r.w((0, 0, 60)))),
              ("Düse", v2.px(f_r.w((0, 0, 6)))),
              ("Becher Ø %.0f" % BECHER_D, v2.px(rim(-12, BECHER_D / 2, 52)))]
    labels_seite(ax, links, 792, "right", soft, ink)
    labels_seite(ax, rechts, 1074, "left", soft, ink)
    ax.text(900, 858, "Spritzeninhalt: Cyan, Magenta, Gelb, Weiß, Schwarz", ha="center", va="center", fontsize=11, color=soft)

    # Ansicht 3: Fensterrichtung, Stationen, Motoren, Becher
    v3 = views[3]

    def pol(R, a, z):
        t = math.radians(a)
        return v3.px(np.array([R * math.cos(t), R * math.sin(t), z]))

    arc = [pol(R_A + 2.5, t, Z_OBER1) for t in np.linspace(-30, 30, 25)]
    ax.plot([p[0] for p in arc], [p[1] for p in arc], color=C_MESSING, lw=4, solid_capstyle="round")
    p0, p1 = pol(110, 0, Z_OBER1), pol(134, 0, Z_OBER1)
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color="#8a6a12", lw=2.2))
    ax.text(p1[0], p1[1] + 18, "vorne, Fenster (0°)", ha="center", va="center", fontsize=12, fontweight="bold",
            color="#7a5a00")
    for a, nm in zip(ST_WINKEL, ST_NAMEN):
        x, y = pol(124, a, Z_OBER1)
        fc = INHALT[nm]
        tc = "white" if nm in ("K", "M") else ink
        ax.text(x, y, "%s  %d°" % (nm, a), ha="center", va="center", fontsize=11, fontweight="bold", color=tc,
                bbox=dict(boxstyle="round,pad=0.25", fc=fc, ec="#6b7078", lw=0.8))
    for a in ST_WINKEL:
        fr = station_frame(a)
        pts = [fr.w((MOTOR_XY[0] + sx * NEMA / 2, MOTOR_XY[1] + sy * NEMA / 2, MOTOR_S1)) for sx, sy in
               ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1))]
        xy = [v3.px(p) for p in pts]
        ax.plot([q[0] for q in xy], [q[1] for q in xy], color="#2a2d32", lw=1.3)
    th = np.linspace(0, 2 * np.pi, 73)
    xy = [v3.px(np.array([BECHER_D / 2 * math.cos(t), BECHER_D / 2 * math.sin(t), 90.0])) for t in th]
    ax.plot([q[0] for q in xy], [q[1] for q in xy], color="#2f6f9a", lw=1.3, ls="--")
    ax.text(1500, 858, "Motoren halbtransparent, gestrichelt: Becherrand Durchmesser %.0f" % BECHER_D, ha="center",
            va="center", fontsize=11, color=soft)

    ax.text(900, 880, "Durchmesser %.0f  |  Höhe %.0f (mit Haube)  |  Fuß %.0f  |  Stationsachse 4° geneigt: Düse innen, Motor außen"
            % (D_AUSSEN, Z_HAUBE1, FUSS_D), ha="center", va="center", fontsize=11, color=ink)


if __name__ == "__main__":
    main()
