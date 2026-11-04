#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rendering und Prüfung des Farbmischers nach hardware/farbmischer_parameter.md (Stand 6).

Aufruf:  python3 render_farbmischer.py              erzeugt rendering_farbmischer.png (Hero, Schnitt, Draufsicht, Maßskizze)
         python3 render_farbmischer.py --pruefung   rechnet nur alle Kollisionsprüfungen aus Abschnitt 15 des Blatts

Nur numpy, matplotlib und Standardbibliothek. Der Hero ist ein eigener Strahlverfolger (analytische Zylinder,
Kegel, Ebenen) mit Umgebungslicht aus Softboxen, weichem Tischschatten und Spiegelung. Schnitt, Draufsicht und
Maßskizze sind exakte 2D-Zeichnungen aus denselben Maßen. Stand 6: kein Licht im Gerät (nichts leuchtet),
alles aus PETG gedruckt, Gold sind gedruckte Gold-PETG-Teile.

Koordinaten wie im Blatt: Ursprung Gerätemitte auf der Tischfläche, +X nach vorne (Nutzerin), +Y von vorne gesehen
nach rechts, +Z oben, Winkel theta von +X aus gegen den Uhrzeigersinn von oben (0 Grad vorne, 90 Grad rechts).
Alle Maße in mm.
"""
import math
import os
import sys
import time
import warnings

import numpy as np

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "rendering_farbmischer.png")

# ============================================================
# Maße aus farbmischer_parameter.md (Stand 6), Abschnitte 3 bis 7 und farbmischer.scad
# ============================================================
PITCH = 360.0 / 7.0            # Platzteilung
RS = 57.0                      # Stationsradius
ML = 1.786                     # mm je ml (Innen-Ø 26,7)

# Höhenkette (Abschnitt 3)
Z_FUSS, Z_GRUND0, Z_GRUND1 = 0.0, 3.0, 7.0
Z_WZ0, Z_WZ1 = 7.5, 20.2
Z_POD0, Z_POD1 = 24.4, 26.0                  # Podestscheibe 1,6 dick (PETG schwarz, Stiel Ø 14 steht frei)
Z_BODEN0, Z_BODEN1 = 26.0, 27.5
Z_BECHER0, Z_BECHER1 = 27.5, 60.5
BECHER_RU, BECHER_RO = 23.5, 31.0
Z_RINNE0, Z_RINNE1, Z_SCHWAMM = 54.0, 64.0, 65.5
Z_RDECKEL = 65.2                             # Rinnendeckel 1,2 dick (Z 64 bis 65,2) mit sechs Löchern Ø 14
Z_LIPPE0, Z_LIPPE1 = 60.0, 68.5
Z_VENTIL0, Z_VENTIL1 = 67.5, 77.5            # Ventilspitze unten, Ventil bis Konusansatz
Z_KONUS1 = 97.5                              # Konus bis Zylinderende
Z_ZYL0, Z_ZYL1 = 97.5, 219.5
Z_FL0, Z_FL1 = 219.5, 222.5                  # Flansch
Z_RING0, Z_RING1 = 97.0, 101.0               # Goldring (Gold-PETG, Ø 202, Z 97 bis 101)
Z_FENSTER0, Z_FENSTER1 = 108.0, 180.0        # unter dem Laufring, Bogenmitte Z 169
Z_FENSTER_M = Z_FENSTER1 - 11.0
Z_LAUF0, Z_LAUF1 = 182.5, 188.5
Z_ROLLE0, Z_ROLLE1 = 188.5, 210.5
Z_BOCK0, Z_BOCK1 = 193.5, 211.0
Z_PLATTE0, Z_PLATTE1 = 211.0, 223.0
Z_KP_LEER = 231.5
Z_KP_50 = 320.8
Z_KP_REST = Z_KP_LEER + 2 * ML
Z_SPARK = 330.8
Z_SMIN = Z_KP_REST
SL_U, SL_H = -10.0, 58.0                     # Schlitten relativ zu S
Z_PORTAL_O = 330.0
Z_FUGE0, Z_FUGE1 = 338.0, 341.0              # Goldband (ersetzt die Lichtfuge), Gold-PETG
Z_KRONE0, Z_KRONE1 = 341.0, 406.8
Z_M1_0, Z_M1_1 = 346.8, 380.8            # NEMA 17, 34 mm
Z_BR0, Z_BR1 = 380.8, 387.8
Z_RIEMEN0, Z_RIEMEN1 = 388.3, 396.3
Z_GT2_OBEN = 404.3                           # GT2-Scheibe 20 Z, 16 hoch, auf Passscheibe 0,5
Z_SPINDEL1 = 403.0
Z_WELLE1 = 395.1                             # Führungswellen 170 lang, oben 14,3 in Brücke und Klemmnabe
Z_KOERPER0, Z_KOERPER1 = 101.0, 338.0
R_KOERPER, WAND = 98.0, 1.6
R_KOERPER_IN = R_KOERPER - WAND              # 96,4
SP, FALZ_T = 0.2, 0.7                        # Spiel je Seite, Falz Zapfen und Muffe je eine halbe Wand
R_GOLDRING_IN = R_KOERPER_IN + FALZ_T + SP   # Goldring innen 97,3 (Sockelfalz geht hindurch, bis r 97,1)
R_SOCKELFALZ = R_KOERPER_IN + FALZ_T         # 97,1
Z_KTEIL = 235.0                              # Körperteilung = Schattenfuge (V-Nut 1,0 breit, 0,5 tief)
FUGE_FASE = 0.5
GOLDRING_GAP = 39.0                          # Goldring am Portal offen (|Y| < 39)
# Portalrahmen (Gold-PETG, 3 breit, 1,5 erhaben), Kontur wie rb_in, rb_out, fw_in, fw_out in farbmischer.scad
RAHMEN_BB, RAHMEN_T = 3.0, 1.5
HW_PORTAL, Z_PORTAL_U, PORTAL_RO, PORTAL_RU = 36.0, 16.0, 24.0, 8.0
FW_HW = 39.4                                 # Fensterrahmen innen: 0,4 außerhalb der Falzkante (Scheibe 78 breit)
FW_Z1 = 333.0 + (FW_HW - 39.0)               # 333,4
FW_RO = 26.0 + (FW_HW - 39.0)                # 26,4 innen (außen 29,4)
Z_RB0, Z_RB1 = 13.0, 97.0                    # Bühnenrahmen
Z_RF0, Z_RF1 = 101.0, FW_Z1 + RAHMEN_BB      # Fensterrahmen 101 bis 336,4
Z_LIPPE_G0, Z_LIPPE_G1 = 45.0, 48.0          # Goldlippe 3 x 1,5 oben auf der Schubladenfront
Z_SCHEIBE_NAHT_A, Z_SCHEIBE_NAHT_I = 215.0, 219.0   # Portalscheibe in zwei Hälften: Fuge außen / innen
R_KRONE, R_RING, R_FUSS_AUSSEN, R_SOCKEL_OBEN = 102.0, 101.0, 102.0, 98.0   # Fuß Ø 204, Kegel auf Ø 196
H_GESAMT = 406.8
Z_FASE = H_GESAMT - 6.0
R_PLATTE = 85.5                              # Karussellplatte Ø 171
STEMPEL_X = 53.0                             # Stempel 4 mm innen von der Spritzenachse (Kraft liegt in der Flanschauflage)
STEMPEL_D = 25.0                             # Stempelfuß Ø 25 (gedruckt, 2 mm Gummiauflage darunter)
SPITZE_KOLBEN = 134.0                        # Kolbenplatte Oberkante minus Kolbenboden (Kolben ganz unten bei Z 97,5)
ZUGANKER_R, ZUGANKER_RAD = 90.5, 2.5
ZUGANKER_W = (32.0, -32.0, 2.5 * PITCH, -2.5 * PITCH)   # +-128,57: Mitte zwischen den Fenstern 2 und 3 bzw. 4 und 5
MUTTER_FL, MUTTER_ECK = 4.0, 8.0 / math.sqrt(3.0)          # M5 SW 8, Schlüsselfläche radial außen in der Sechskanttasche
BALLAST = [(72.0, 69.0), (72.5, -71.0), (66.5, 120.0), (66.5, -120.0)]   # r, theta; Stapel 7 x M20 (Ø 37 x 3), Becher Ø 38
Z_BALLAST1 = 28.0
PLATINE_Y = -81.0
STATION = [None, "Weiß 1", "Gelb", "Magenta", "Cyan", "Schwarz", "Weiß 2"]   # Plätze 0 bis 6

FARBEN = {
    "sockel": "#0A0A0C", "koerper": "#141417", "gold": "#C9A44C", "gold_l": "#E8CB7A", "gold_s": "#8A6A22",
    "rauch": "#2E2E33", "klar": "#E9ECEE", "schublade": "#F4F2EE", "podest": "#1C1C1E", "innen": "#1C1C1E",
    "spritze": "#E9ECEE", "silikon": "#DAD6CC", "gummi": "#2A2A2C", "stahl": "#8C8D91", "messing": "#B08D57",
    "fuss": "#1A1A1A", "becher": "#EEEEEE",
    "cyan": "#0093D3", "magenta": "#D4007A", "gelb": "#FFD200", "weiss": "#F6F4EE", "schwarz": "#1B1A19",
}
STATIONSBUCHSTABE = ["W", "Y", "M", "C", "K", "W"]     # Platz 1 bis 6, eingraviert statt Farbring
PLATZ_FARBE = [None, FARBEN["weiss"], FARBEN["gelb"], FARBEN["magenta"], FARBEN["cyan"], FARBEN["schwarz"], FARBEN["weiss"]]
ZIELFARBE = "#E0583F"          # Beispiel für die Becherfarbe im Rendering (aus Magenta, Gelb und Weiß gemischt)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ============================================================
# Prüfung (Abschnitt 15): exakte 2D-Abstände, 3D als Prismen aus 2D-Form und Z-Intervall
# ============================================================
def _rot(P, a_deg):
    """Punkte P (m,2) um den Ursprung drehen, a_deg skalar oder Feld (n): Ergebnis (n,m,2)."""
    a = np.radians(np.atleast_1d(np.asarray(a_deg, float)))[:, None]
    c, s = np.cos(a), np.sin(a)
    return np.stack([c * P[:, 0] - s * P[:, 1], s * P[:, 0] + c * P[:, 1]], -1)


def b_circle(cx, cy, r, n=240):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(t), cy + r * np.sin(t)], 1)


def b_box(cx, cy, hx, hy, step=0.5):
    nx, ny = max(int(2 * hx / step), 2), max(int(2 * hy / step), 2)
    xs, ys = np.linspace(-hx, hx, nx + 1), np.linspace(-hy, hy, ny + 1)
    pts = [np.stack([xs, np.full_like(xs, -hy)], 1), np.stack([xs, np.full_like(xs, hy)], 1),
           np.stack([np.full_like(ys, -hx), ys], 1), np.stack([np.full_like(ys, hx), ys], 1)]
    return np.vstack(pts) + np.array([cx, cy])


def sd_circle(cx, cy, r):
    return lambda P: np.hypot(P[..., 0] - cx, P[..., 1] - cy) - r


def sd_box(cx, cy, hx, hy, a_deg=0.0):
    """Rechteck mit Mitte (cx,cy), Halbmaße hx,hy, um den Ursprung um a_deg gedreht."""
    t = math.radians(a_deg)
    c, s = math.cos(t), math.sin(t)

    def f(P):
        x = c * P[..., 0] + s * P[..., 1] - cx
        y = -s * P[..., 0] + c * P[..., 1] - cy
        qx, qy = np.abs(x) - hx, np.abs(y) - hy
        return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0)
    return f


def sd_wall(R):
    """Wand außerhalb des Radius R (negativ = in der Wand)."""
    return lambda P: R - np.hypot(P[..., 0], P[..., 1])


def sd_ring(r0, r1, open_deg):
    """Kreisring r0..r1 mit Lücke |theta| < open_deg um 0 Grad (Vorzeichenabstand, negativ innen)."""
    t = math.radians(open_deg)
    e1 = np.array([math.cos(t), math.sin(t)])
    e2 = np.array([math.cos(t), -math.sin(t)])

    def seg(P, e):
        s = np.clip(P[..., 0] * e[0] + P[..., 1] * e[1], r0, r1)
        return np.hypot(P[..., 0] - s * e[0], P[..., 1] - s * e[1])

    def f(P):
        r = np.hypot(P[..., 0], P[..., 1])
        th = np.abs(np.arctan2(P[..., 1], P[..., 0]))
        radial = np.maximum(r0 - r, r - r1)
        in_gap = th < t
        d_gap = np.minimum(seg(P, e1), seg(P, e2))
        return np.where(in_gap, d_gap, radial)
    return f


def sd_slot(r_in_center, hw, r_out):
    """Zylinderschlitz: Halbkreis R=hw um (r_in_center,0), nach außen bis r_out durchgehend (Vereinigung)."""
    sc = sd_circle(r_in_center, 0, hw)
    sb = sd_box((r_in_center + r_out) / 2, 0, (r_out - r_in_center) / 2, hw)
    return lambda P: np.minimum(sc(P), sb(P))


def b_slot(rc, hw, r_out, a_deg=0.0):
    t = np.linspace(math.pi / 2, 3 * math.pi / 2, 120)
    arc = np.stack([rc + hw * np.cos(t), hw * np.sin(t)], 1)
    side = [np.stack([np.linspace(rc, r_out, 40), np.full(40, s * hw)], 1) for s in (1, -1)]
    end = np.stack([np.full(30, r_out), np.linspace(-hw, hw, 30)], 1)
    B = np.vstack([arc] + side + [end])
    return _rot(B, a_deg)[0]


def rrect_pts(cx, hx, hy, r_in, n=60):
    """Flanschtasche radial lang: Mitte (cx,0), Halbmaße hx (radial), hy (tangential), innere Ecken (zur Achse) R r_in,
    äußere Ecken scharf. Randpunkte."""
    pts = []
    t = np.linspace(0, 1, 80)
    pts.append(np.stack([np.full_like(t, cx + hx), -hy + 2 * hy * t], 1))
    pts.append(np.stack([cx + hx - (2 * hx - r_in) * t, np.full_like(t, hy)], 1))
    th = np.linspace(math.pi / 2, math.pi, n)
    pts.append(np.stack([cx - hx + r_in + r_in * np.cos(th), hy - r_in + r_in * np.sin(th)], 1))
    pts.append(np.stack([np.full_like(t, cx - hx), hy - r_in - (2 * hy - 2 * r_in) * t], 1))
    th = np.linspace(math.pi, 1.5 * math.pi, n)
    pts.append(np.stack([cx - hx + r_in + r_in * np.cos(th), -hy + r_in + r_in * np.sin(th)], 1))
    pts.append(np.stack([cx - hx + r_in + (2 * hx - r_in) * t, np.full_like(t, -hy)], 1))
    return np.vstack(pts)


def sd_poly_convex(V):
    """Vorzeichenabstand zu einem konvexen Polygon (Eckpunkte gegen den Uhrzeigersinn), exakt."""
    V = np.asarray(V, float)
    n = len(V)

    def f(P):
        P = np.asarray(P, float)
        dmax = np.full(P.shape[:-1], -1e18)
        dseg = np.full(P.shape[:-1], 1e18)
        for i in range(n):
            a, b = V[i], V[(i + 1) % n]
            e = b - a
            ln = np.hypot(*e)
            if ln < 1e-12:
                continue
            nr = np.array([e[1], -e[0]]) / ln
            dmax = np.maximum(dmax, (P[..., 0] - a[0]) * nr[0] + (P[..., 1] - a[1]) * nr[1])
            tt = np.clip(((P[..., 0] - a[0]) * e[0] + (P[..., 1] - a[1]) * e[1]) / (ln * ln), 0, 1)
            dseg = np.minimum(dseg, np.hypot(P[..., 0] - (a[0] + tt * e[0]), P[..., 1] - (a[1] + tt * e[1])))
        return np.where(dmax <= 0, dmax, dseg)
    return f


def sd_roundrect_yz(hw, z0, z1, r_top, r_bot):
    """Portalöffnung in der (y,z)-Ebene, Vorzeichenabstand (negativ innen)."""
    zm = (z0 + z1) / 2
    hh = (z1 - z0) / 2

    def f(y, z):
        y, z = np.abs(y), z - zm
        r = np.where(z > 0, r_top, r_bot)
        qx, qz = y - (hw - r), np.abs(z) - (hh - r)
        return np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0) - r
    return f


def gap3(sdf, B, zs, zt):
    """Abstand eines bewegten Prismas (Randpunkte B (...,m,2), Z-Intervall zs) zu einem festen (sdf, Intervall zt),
    kleinster Wert über alle Stellungen. Negativ = Durchdringung."""
    d2 = sdf(B).min(axis=-1)
    dz = max(zt[0] - zs[1], zs[0] - zt[1])
    g = np.where((d2 > 0) & (dz > 0), np.hypot(d2, dz), np.maximum(d2, dz))
    return float(np.min(g))


def spritzenteile(kp):
    """Teile einer Spritze an Station bei theta 0: (Name, Randpunkte, z0, z1)."""
    return [
        ("Ventil", b_circle(RS, 0, 4.5, 60), Z_VENTIL0, Z_VENTIL1),
        ("Konus", b_circle(RS, 0, 5.0, 60), Z_VENTIL1, Z_KONUS1),
        ("Zylinder", b_circle(RS, 0, 15.0, 180), Z_ZYL0, Z_ZYL1),
        ("Flansch", b_box(RS, 0, 22.5, 16.0, 0.5), Z_FL0, Z_FL1),
        ("Kolbenstange", b_box(RS, 0, 6.0, 6.0, 0.5), Z_FL1, kp - 3.0),
        ("Kolbenplatte", b_circle(RS, 0, 19.0, 180), kp - 3.0, kp),
    ]


def pruefung(verbose=True):
    t0 = time.time()
    S = Z_SPARK
    rows = []                      # (Nr, Text, Soll, Ist, Blatt, Hinweis)
    extra = []                     # Zusatzprüfungen
    kps = [Z_KP_LEER, Z_KP_REST, (Z_KP_LEER + Z_KP_50) / 2, Z_KP_50]
    phis = np.arange(0, 360, 1.0)

    # ---- Höhenkette neu rechnen
    ketten = []
    fl_o = Z_FL1
    chain = [
        ("Hub 50 ml", 50 * ML, 89.3), ("Kolbenplatte 50 ml", Z_KP_LEER + 50 * ML, Z_KP_50),
        ("Kolbenplatte 2 ml Rest", Z_KP_LEER + 2 * ML, Z_KP_REST), ("S_park = Platte 50 ml + 10", Z_KP_50 + 10.0, Z_SPARK),
        ("Stempelweg S_min bis S_park", Z_SPARK - Z_SMIN, 95.7), ("Schlitten oben in Park", S + SL_U + SL_H, 378.8),
        ("Spritzenspitze (Becherrand 60,5 + 7 + 10)", Z_BECHER1 + 7.0 + 10.0, 77.5),
        ("Zylinder Oberkante (Spitze + 20 + 122)", 77.5 + 20 + 122, Z_ZYL1),
        ("Platte Oberkante (Flansch + 0,5)", fl_o + 0.5, Z_PLATTE1),
        ("Kolbenplatte leer (Flansch + 9)", fl_o + 9.0, Z_KP_LEER),
        ("Motor 1 oben = Brücke unten (34 mm)", Z_M1_0 + 34.0, Z_BR0),
        ("Krone oben (Lager 387,8 + 0,5 + GT2 16 + 0,5 + 2)", Z_BR1 + 0.5 + 16.0 + 0.5 + 2.0, H_GESAMT),
        ("Führungswelle oben (Länge 170)", Z_SMIN + SL_U + 170.0, Z_WELLE1),
        ("Welle unten (S_min - 10)", Z_SMIN + SL_U, 225.1),
    ]
    for n, ist, blatt in chain:
        ketten.append((n, ist, blatt))

    # ---- A) Drehprüfung: Spritzenteile an sechs Stationen, Karussell 0 bis 359 Grad, vier Füllstände
    fest = {
        "Schlitten": (sd_circle(0, 0, 34.0), (S + SL_U, S + SL_U + SL_H)),
        "Führungswelle": (lambda P: np.minimum(sd_circle(0, 22, 5)(P), sd_circle(0, -22, 5)(P)), (Z_SMIN + SL_U, Z_BR0)),
        "Spindel": (sd_circle(0, 0, 4.0), (250.0, Z_BR0)),
        # Stand 6: Ausleger mit Stempel ein gedrucktes Teil: Arm X 28 bis 68, Platte X 28 bis 36, Stempelfuß Ø 25 mit Gummi (Z S bis S + 8)
        "Arm": (sd_box(48.0, 0, 20.0, 12.5), (S + 8.0, S + 16.0)),
        "Platte": (sd_box(32.0, 0, 4.0, 12.5), (S + 8.0, S + 48.0)),
        "Rippen": (sd_box(47.0, 0, 11.0, 12.5), (S + 16.0, S + 36.0)),
        "Stempel": (sd_circle(STEMPEL_X, 0, STEMPEL_D / 2), (S, S + 8.0)),
        "Motor 1": (sd_box(-59.0, 0, 21.15, 21.15), (Z_M1_0, Z_M1_1)),
        "Laufring": (sd_ring(74.5, 86.5, 15.0), (Z_LAUF0, Z_LAUF1)),
        "Feuchtrinne": (sd_ring(45.0, 69.0, 38.0), (Z_RINNE0, Z_RDECKEL)),
        "Schwamm": (sd_ring(48.0, 66.0, 38.0), (Z_RINNE1, Z_SCHWAMM)),
        "Becher": (sd_circle(RS, 0, BECHER_RO), (Z_BECHER0, Z_BECHER1)),
        "Körperwand": (sd_wall(R_KOERPER_IN), (Z_KOERPER0, Z_KOERPER1)),
        "Lippe +40": (sd_box(57.0, 0, 7.0, 0.75, 40.0), (Z_LIPPE0, Z_LIPPE1)),
        "Lippe -40": (sd_box(57.0, 0, 7.0, 0.75, -40.0), (Z_LIPPE0, Z_LIPPE1)),
    }
    for a in ZUGANKER_W:
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        fest["Zuganker %+d" % round(a)] = (sd_circle(ZUGANKER_R * ca, ZUGANKER_R * sa, ZUGANKER_RAD), (Z_GRUND1, Z_BR1))
    res = {}
    for kp in kps:
        for name, B, z0, z1 in spritzenteile(kp):
            for k in range(1, 7):
                P = _rot(B, k * PITCH + phis)
                for fn, (sdf, zt) in fest.items():
                    if fn.startswith("Lippe") and name == "Ventil":
                        continue          # das Ventil darf an der Lippe streifen (Überdeckung 1,0 gewollt)
                    g = gap3(sdf, P, (z0, z1), zt)
                    key = (fn, name)
                    res[key] = min(res.get(key, 1e9), g)
    # Rollenböcke und Rollen drehen mit (sieben, bei (j+0,5)*PITCH)
    bock = b_box(80.0, 0, 5.5, 12.0, 0.5)
    rb = np.hypot(bock[:, 0], bock[:, 1])          # Außenfläche der Böcke als Bogen r 85,5
    bock = bock * np.minimum(1.0, 85.5 / rb)[:, None]
    rolle = b_box(80.0, 0, 3.5, 11.0, 0.5)
    for nm, B, zz in (("Rollenbock", bock, (Z_BOCK0, Z_BOCK1)), ("Rolle", rolle, (Z_ROLLE0, Z_ROLLE1))):
        for j in range(7):
            P = _rot(B, (j + 0.5) * PITCH + phis)
            for fn in ["Körperwand", "Becher", "Feuchtrinne"] + ["Zuganker %+d" % round(a) for a in ZUGANKER_W]:
                sdf, zt = fest[fn]
                key = (fn, nm)
                res[key] = min(res.get(key, 1e9), gap3(sdf, P, zz, zt))
    # Rollenböcke gegen die Zylinder der eigenen Platte (starr zueinander)
    for nm in ("Zylinder", "Flansch", "Konus"):
        B = [t for t in spritzenteile(Z_KP_50) if t[0] == nm][0]
        for k in range(1, 7):
            P = _rot(B[1], k * PITCH + 0.0)[0]
            for j in range(7):
                sdf = sd_box(80.0, 0, 5.5, 12.0, (j + 0.5) * PITCH)
                key = ("Rollenbock eigene Platte", nm)
                res[key] = min(res.get(key, 1e9), gap3(sdf, P[None], (B[2], B[3]), (Z_BOCK0, Z_BOCK1)))
    # Schlitten und Arm tief gegen Nachbar-Kolbenplatten
    for kp in kps:
        for k in (1, 6):
            Bp = b_circle(RS, 0, 19.0, 180)
            P = _rot(Bp, k * PITCH)
            for fn in ("Arm", "Platte", "Stempel", "Schlitten"):
                sdf, zt = fest[fn]
                zt = (0.0, 999.0)
                key = (fn + " tief", "Nachbar-Kolbenplatte")
                res[key] = min(res.get(key, 1e9), gap3(sdf, P, (0, 1), zt))

    # ---- B) Entnahme: Station 1 vorne (phi = -PITCH), Spritze radial nach vorne, 0 bis 130 mm
    dxs = np.arange(0, 131, 1.0)
    phi = -PITCH
    ent = {}
    full = {n: (B, z0, z1) for n, B, z0, z1 in spritzenteile(Z_KP_50)}

    def moved(B):
        return B[None, :, :] + np.stack([dxs, np.zeros_like(dxs)], 1)[:, None, :]

    festE = {
        "Laufringende": (sd_ring(74.5, 86.5, 15.0), (Z_LAUF0, Z_LAUF1)),
        "Feuchtrinne": (sd_ring(45.0, 69.0, 38.0), (Z_RINNE0, Z_RDECKEL)),
        "Schwamm": (sd_ring(48.0, 66.0, 38.0), (Z_RINNE1, Z_SCHWAMM)),
        "Stempel/Arm": (lambda P: np.minimum(sd_circle(STEMPEL_X, 0, STEMPEL_D / 2)(P), sd_box(48, 0, 20, 12.5)(P)), (S, S + 16.0)),
    }
    for j in range(7):
        a = (j + 0.5) * PITCH + phi
        if abs(((a + 180) % 360) - 180) < 40:
            festE["Rollenbock %.1f" % (((a + 180) % 360) - 180)] = (sd_box(80.0, 0, 5.5, 12.0, a), (Z_BOCK0, Z_BOCK1))
    for a in ZUGANKER_W:
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        festE["Zuganker %+d" % round(a)] = (sd_circle(ZUGANKER_R * ca, ZUGANKER_R * sa, ZUGANKER_RAD), (Z_GRUND1, Z_BR1))
    for nm, (B, z0, z1) in full.items():
        P = moved(B)
        for fn, (sdf, zt) in festE.items():
            if nm == "Ventil" and fn == "Laufringende":
                pass
            ent[(fn, nm)] = min(ent.get((fn, nm), 1e9), gap3(sdf, P, (z0, z1), zt))
    # Nachbarn (Plätze 2 bis 6 stehen bei (p-1)*PITCH), nur Zylinder und Platte
    for nm in ("Zylinder", "Kolbenplatte"):
        B, z0, z1 = full[nm]
        for nb in ("Zylinder", "Kolbenplatte"):
            if nb != nm:
                continue
            for p in range(2, 7):
                ang = (p - 1) * PITCH
                rad_n = 15.0 if nb == "Zylinder" else 19.0
                sdf = sd_circle(RS * math.cos(math.radians(ang)), RS * math.sin(math.radians(ang)), rad_n)
                zt = (Z_ZYL0, Z_ZYL1) if nb == "Zylinder" else (Z_KP_50 - 3.0, Z_KP_50)
                ent[("Nachbar " + nb, nm)] = min(ent.get(("Nachbar " + nb, nm), 1e9), gap3(sdf, moved(B), (z0, z1), zt))
    # Portal: Silhouette in der (y,z)-Ebene gegen die Öffnung (Euklidischer Abstand zum Rand)
    portal = sd_roundrect_yz(36.0, 16.0, Z_PORTAL_O, 24.0, 8.0)
    for nm, hw, z0, z1 in (("Zylinder", 15.0, Z_ZYL0, Z_ZYL1), ("Flansch", 16.0, Z_FL0, Z_FL1),
                            ("Kolbenstange", 6.0, Z_FL1, Z_KP_50 - 3.0), ("Kolbenplatte", 19.0, Z_KP_50 - 3.0, Z_KP_50)):
        yy = np.linspace(-hw, hw, 81)
        zz = np.linspace(z0, z1, 41)
        pts = [(y, z) for y in yy for z in (z0, z1)] + [(s * hw, z) for s in (-1, 1) for z in zz]
        d = min(-portal(np.array([p[0]]), np.array([p[1]]))[0] for p in pts)
        ent[("Portal", nm)] = d

    # ---- C) statische 2D-Prüfungen
    # Flanschtaschen 46 x 33, Innenecken R5, benachbart bei PITCH
    TB = rrect_pts(RS, 23.0, 16.5, 5.0)
    TBr = _rot(TB, PITCH)[0]
    pocket_sd = lambda P, ang: None
    # exakte Polygonform der Nachbartasche als konvexes Polygon (Randpunkte der Tasche genügen, 2 Richtungen)
    def poly_from_boundary(B):
        c = B.mean(0)
        order = np.argsort(np.arctan2(B[:, 1] - c[1], B[:, 0] - c[0]))
        return B[order]
    sdfP = sd_poly_convex(poly_from_boundary(_rot(TB, PITCH)[0][::2]))
    g_pocket = float(sdfP(TB).min())
    # Zylinderschlitz: Halbkreis R16 bei r57, nach außen bis Plattenrand r86
    SB = b_slot(RS, 16.0, R_PLATTE, 0.0)
    sdS = sd_slot(RS, 16.0, R_PLATTE)
    sdS_rot = lambda P: sdS(_rot(P.reshape(-1, 2), -PITCH)[0].reshape(P.shape))
    g_slot = float(sdS_rot(SB).min())
    # Rollenbock (j = 0, Winkel PITCH/2) gegen Schlitze der Nachbarstationen (bei 0 und PITCH), Plattenebene darunter
    Bb = _rot(bock, PITCH / 2)[0]
    sd_s0 = sdS
    sd_s1 = lambda P: sdS(_rot(P.reshape(-1, 2), -PITCH)[0].reshape(P.shape))
    g_bock_slot = min(float(sd_s0(Bb).min()), float(sd_s1(Bb).min()))

    # ---- D) Formelwerte
    def cone_r(z):
        return R_FUSS_AUSSEN - (R_FUSS_AUSSEN - R_SOCKEL_OBEN) * (z - Z_GRUND0) / (97.0 - Z_GRUND0)

    cup_r = lambda z: BECHER_RU + (BECHER_RO - BECHER_RU) * (z - Z_BECHER0) / (Z_BECHER1 - Z_BECHER0)
    zk = [(math.hypot(ZUGANKER_R * math.cos(math.radians(a)), ZUGANKER_R * math.sin(math.radians(a)))) for a in ZUGANKER_W]
    ca, sa = ZUGANKER_R * math.cos(math.radians(32)), ZUGANKER_R * math.sin(math.radians(32))
    gap_wz_anker = (ca - 63.35) - ZUGANKER_RAD
    gap_sch_wand = sa - 35.0 - ZUGANKER_RAD
    gap_sch_schiene = sa - 35.0 - ZUGANKER_RAD     # Schienen |Y| 32 bis 35
    platine_ecke = math.hypot(45.0, abs(PLATINE_Y) + 1.0)   # Platine 70 x 90, Ebene Y -81, Z 30 bis 100
    wand_z92 = min(cone_r(97.0) - WAND, R_KOERPER_IN)
    wz_ecke = math.hypot(63.35, 70.0)
    wand_z202 = cone_r(Z_WZ1) - WAND
    motor1_schl = (59.0 - 21.15) - 34.0
    rad70_becher = RS - 23.5 - cup_r(51.0)
    motor2_lager = (57.8 - 21.15) - 20.0
    # Rollen im Stillstand gegen den Rand der Laufringlücke (Rolle +-11 tangential bei r 80, Lücke +-15)
    rolle_luecke = (abs(PITCH / 2) - math.degrees(11.0 / 80.0) - 15.0) * math.pi / 180.0 * 80.0
    # Nachbarventile
    sehne = 2 * RS * math.sin(math.radians(PITCH / 2))
    nachbar_ventil = sehne - BECHER_RO - 4.5
    # neue Prüfungen Stand 5.1
    anker_platte = (ZUGANKER_R - ZUGANKER_RAD) - R_PLATTE
    mutter_wand = R_KOERPER_IN - (ZUGANKER_R + MUTTER_FL)
    lasche_wand = R_KOERPER_IN - 94.5
    fen_halb = 13.0                                   # Fensterscheibe (Klar-PETG) 26 breit
    anker_fenster = min(abs(ZUGANKER_R * math.sin(math.radians(a - p * PITCH))) - ZUGANKER_RAD - fen_halb
                        for a in ZUGANKER_W for p in range(1, 7) if math.cos(math.radians(a - p * PITCH)) > 0)

    def boxd(c, x0, x1, y0, y1):
        return math.hypot(max(x0 - c[0], 0, c[0] - x1), max(y0 - c[1], 0, c[1] - y1))
    bl = []
    for r_, a_ in BALLAST:
        c = (r_ * math.cos(math.radians(a_)), r_ * math.sin(math.radians(a_)))
        rr = 19.0
        bl += [boxd(c, 50.65, 63.35, -70, 10) - rr, boxd(c, 20, 104, -35, 35) - rr, math.hypot(*c) - 20 - rr,
               boxd(c, -78.95 - 3, -36.65 + 3, -21.15 - 12, 21.15 + 12) - rr, 100.0 - math.hypot(*c) - rr]
        for aa in (95, -95, 145, -145):
            bl.append(math.hypot(c[0] - 57 * math.cos(math.radians(aa)), c[1] - 57 * math.sin(math.radians(aa))) - 4 - rr)
        for aa in ZUGANKER_W:
            bl.append(math.hypot(c[0] - ZUGANKER_R * math.cos(math.radians(aa)), c[1] - ZUGANKER_R * math.sin(math.radians(aa))) - 2.5 - rr)
    ballast_min = min(bl)
    # Flanschauflage: Stempelachse muss innerhalb der Auflage (Halbmond bis r 57) liegen
    flansch_hebel = RS - STEMPEL_X
    # neue Prüfungen Stand 6 (gedruckter Ausleger, Goldring)
    ausleger_bruecke = Z_BR0 - (S + 48.0)                         # Platte endet bei S + 48, Brücke unten bei S + 50
    stempel_auf_kp = 19.0 - (abs(RS - STEMPEL_X) + STEMPEL_D / 2)   # Stempelfuß Ø 25 auf Kolbenplatte Ø 38 um die Spritzenachse
    S_ = Z_SMIN                                                   # tiefste Stellung, Stempelunterkante (Gummi) auf der Kolbenplatte bei 235,1
    teile_smin = [(b_box(48.0, 0, 20.0, 12.5), (S_ + 8.0, S_ + 16.0)),      # Arm
                  (b_box(32.0, 0, 4.0, 12.5), (S_ + 8.0, S_ + 48.0)),       # senkrechte Platte
                  (b_circle(STEMPEL_X, 0, STEMPEL_D / 2, 180), (S_, S_ + 8.0))]   # Stempelfuß mit Gummi
    unten_smin = [(sd_circle(0, 0, R_PLATTE), (Z_PLATTE0, Z_PLATTE1)), (sd_ring(74.5, 86.5, 15.0), (Z_LAUF0, Z_LAUF1))]
    ausleger_smin = min(gap3(sdf, B, zs, zt) for B, zs in teile_smin for sdf, zt in unten_smin)
    goldring_falz = R_GOLDRING_IN - R_SOCKELFALZ                  # 97,3 gegen 97,1

    R = res
    E = ent
    # Nummerierung fortlaufend 1 bis 50 (Stand 6), Zuordnung alt (Stand 5.1) -> neu:
    #   1-10 -> 1-10 | neu 11, 12, 13 (Ausleger Park/Brücke, Stempelfuß/Kolbenplatte, Ausleger S_min) | 11-15 -> 14-18 | 17-32 -> 19-34
    #   34 -> 35 | 36-42 -> 36-42 | 44-47 -> 43-46 | neu 47 (Goldring gegen Sockelfalz) | 48, 49 -> 48, 49 | 51 -> 50
    #   entfallen (nur LED): 16 LED-Träger/Kolbenplatte, 33 Motor 1/LED-Träger, 35 Zuganker/LED-Oberkante, 43 Podest/LED-Ring,
    #   50 Vitrinen-LED/Zylinder. Das Blatt-Maß der neuen Zeilen ist der hier gerechnete Wert (das Blatt wird nachgezogen).
    rows_roh = [
        ("Schlitten tiefste Stellung gegen Karussellplatte oben", 2.0, Z_SMIN + SL_U - Z_PLATTE1, 2.07, ""),
        ("Wellenende Ø10 gegen Karussellplatte oben", 2.0, (Z_SMIN + SL_U) - Z_PLATTE1, 2.07, ""),
        ("Laufring (fest, innen r 74,5) gegen Spritzenzylinder beim Drehen", 2.0, R[("Laufring", "Zylinder")], 2.50, "dreht"),
        ("Zuganker gegen Rollenbock beim Drehen", 2.0, min(R[("Zuganker %+d" % round(a), "Rollenbock")] for a in ZUGANKER_W), 2.50, "dreht"),
        ("Zuganker gegen Laufrolle beim Drehen", 2.0, min(R[("Zuganker %+d" % round(a), "Rolle")] for a in ZUGANKER_W), 3.78, "dreht"),
        ("Feuchtrinne gegen Ventil beim Drehen", 2.0, R[("Feuchtrinne", "Ventil")], 2.30, "dreht"),
        ("Schwamm nass gegen Ventil", 1.5, R[("Schwamm", "Ventil")], 2.00, "dreht"),
        ("Schlitten (r 34) gegen Kolbenplatten beim Drehen", 2.0, R[("Schlitten", "Kolbenplatte")], 4.00, "dreht"),
        ("Schlitten tief gegen Nachbar-Kolbenplatten", 2.0, R[("Schlitten tief", "Nachbar-Kolbenplatte")], 4.00, ""),
        ("Stempel in Park gegen Kolbenplatte 50 ml", 10.0, S - Z_KP_50, 10.00, ""),
        ("Ausleger (Arm, Platte S + 48) in Park gegen Brücke (S + 50)", 2.0, ausleger_bruecke, 2.00, ""),
        ("Stempelfuß Ø 25 (X 53) ganz auf Kolbenplatte Ø 38 (Rand)", 1.5, stempel_auf_kp, 2.50, ""),
        ("Ausleger in S_min gegen Karussellplatte und Laufring", 2.0, ausleger_smin, 12.07, ""),
        ("Führungswellen Ø10 gegen Flansch beim Drehen", 2.0, R[("Führungswelle", "Flansch")], 7.93, "dreht"),
        ("Zuganker gegen Flansch beim Drehen", 2.0, min(R[("Zuganker %+d" % round(a), "Flansch")] for a in ZUGANKER_W), 6.91, "dreht"),
        ("Abstreiflippe gegen Konus (nur das Ventil darf streifen)", 2.0, min(R[("Lippe +40", "Konus")], R[("Lippe -40", "Konus")]), 9.00, "dreht"),
        ("Rollenbock gegen Körperwand", 2.0, R[("Körperwand", "Rollenbock")], 10.90, "dreht"),
        ("Arm und Stempel beim Dosieren (tief) gegen Nachbar-Kolbenplatten", 3.0,
         min(R[("Arm tief", "Nachbar-Kolbenplatte")], R[("Stempel tief", "Nachbar-Kolbenplatte")]), 13.07, ""),
        ("Motor 1 Unterkante gegen Kolbenplatte 50 ml", 10.0, Z_M1_0 - Z_KP_50, 26.00, ""),
        ("Ventil gegen Becherrand (senkrecht)", 5.0, Z_VENTIL0 - Z_BECHER1, 7.00, ""),
        ("Nachbarventil beim Dosieren gegen Becherrand (waagrecht)", 5.0, nachbar_ventil, 13.96, ""),
        ("Nächstes Ventil in Parkstellung gegen Becherrand", 5.0, nachbar_ventil, 13.96, ""),
        ("Rolle im Stillstand gegen Rand der Laufringlücke", 2.0, rolle_luecke, 3.96, ""),
        ("Entnahme: Zylinder gegen Laufringende", 3.0, E[("Laufringende", "Zylinder")], 4.28, "Entnahme"),
        ("Entnahme: Zylinder gegen Rollenbock bei ± 25,7", 3.0, min(v for (fn, nm), v in E.items() if fn.startswith("Rollenbock") and nm == "Zylinder"), 6.52, "Entnahme"),
        ("Entnahme: Flansch gegen Rollenbock", 3.0, min(v for (fn, nm), v in E.items() if fn.startswith("Rollenbock") and nm == "Flansch"), 10.13, "Entnahme"),
        ("Entnahme: Kolbenplatte gegen Portalöffnung (seitlich und oben, R 24)", 3.0, E[("Portal", "Kolbenplatte")], 7.63, "Entnahme"),
        ("Entnahme: Kolbenplatte gegen Stempel oben", 3.0, E[("Stempel/Arm", "Kolbenplatte")], 10.00, "Entnahme"),
        ("Entnahme: Kolbenplatte gegen Nachbar-Kolbenplatten", 3.0, E[("Nachbar Kolbenplatte", "Kolbenplatte")], 11.46, "Entnahme"),
        ("Entnahme: Zylinder gegen Nachbarzylinder", 3.0, E[("Nachbar Zylinder", "Zylinder")], 19.46, "Entnahme"),
        ("Entnahme: Ventil und Konus gegen Feuchtrinne", 3.0, min(E[("Feuchtrinne", "Ventil")], E[("Feuchtrinne", "Konus")]), 30.68, "Entnahme"),
        ("Flanschtaschen untereinander (Innenecken R 5)", 2.0, g_pocket, 3.12, ""),
        ("Zylinderschlitze untereinander", 4.0, g_slot, 17.46, ""),
        ("Rollenbock gegen Zylinderschlitz der Platte", 3.0, g_bock_slot, 5.51, ""),
        ("Motor 1 gegen Schlitten in Park", 2.0, motor1_schl, 3.85, ""),
        ("Stellring gegen Schlittentasche (Tasche 9 tief, Eintauchen 6)", 2.0, 9.0 - (S + SL_U + SL_H - (Z_BR0 - 8.0)), 3.00, ""),
        ("GT2-Rad 70 Z gegen Becher (Z 43 bis 51)", 3.0, rad70_becher, 4.66, ""),
        ("Motor 2 gegen Lagerbock", 3.0, motor2_lager, 16.65, ""),
        ("Zuganker -32 gegen Wägezelle", 3.0, gap_wz_anker, 10.90, ""),
        ("Zuganker ± 32 gegen Schublade (Wand | Schiene)", 3.0, min(gap_sch_wand, gap_sch_schiene), 10.46, "Wand %.2f, Schiene %.2f" % (gap_sch_wand, gap_sch_schiene)),
        ("Platinenecke gegen Hülle (Z 97 bis 100)", 2.0, wand_z92 - platine_ecke, 2.86, ""),
        ("Wägezelle festes Ende gegen Sockelwand", 3.0, wand_z202 - wz_ecke, 5.26, ""),
        ("Überlastanschlag unter dem Lastende", 0.8, 0.8, 0.8, "Einstellmaß"),
        ("Zuganker gegen Karussellplatte (Rand r 85,5) beim Drehen", 2.0, anker_platte, 2.50, "dreht"),
        ("Mutter M5 in Tasche (Fläche außen) gegen Körperwand", 1.5, mutter_wand, 1.90, ""),
        ("Laufringlasche (Ende r 94,5) gegen Körperwand", 1.5, lasche_wand, 1.90, ""),
        ("Goldring innen r 97,3 gegen Sockelfalz (r 97,1)", 0.2, goldring_falz, 0.20, ""),
        ("Zuganker seitlich gegen Fensterscheibe (26 breit)", 5.0, anker_fenster, 14.60, ""),
        ("Ballaststapel gegen Nachbarteile (Grundriss)", 2.0, ballast_min, 5.15, ""),
        ("Stempelachse innerhalb der Flanschauflage (bis r 57)", 2.0, flansch_hebel, 4.00, ""),
    ]
    rows += [(i + 1,) + t for i, t in enumerate(rows_roh)]

    # ---- Zusatzprüfungen (Hinweise, nicht im Blatt)
    extra += [
        ("Z1", "Mutter M5 verdreht (Ecke 4,62 außen) gegen Körperwand, falls die Tasche fehlt", 1.0, R_KOERPER_IN - (ZUGANKER_R + MUTTER_ECK)),
        ("Z2", "Feuchtrinnen-Ende (theta +-38) gegen Becherrand (Dosierstellung, Z 54 bis 60,5)", 3.0,
         float(sd_ring(45.0, 69.0, 38.0)(b_circle(RS, 0, cup_r(60.5), 360)).min())),
        ("Z3", "Schubladen-Hinterkante (X 22) gegen Lagerbock (r 20)", 2.0, 22.0 - 20.0),
        ("Z4", "Fenster oben (Z 180) gegen Laufring unten (Z 182,5)", 2.0, Z_LAUF0 - Z_FENSTER1),
    ]
    if verbose:
        _print_pruefung(rows, extra, ketten, time.time() - t0)
    return rows, extra, ketten


def _print_pruefung(rows, extra, ketten, dt):
    line = "=" * 118
    print(line)
    print("PRÜFUNG nach farbmischer_parameter.md, Stand 6, Abschnitt 15 (Maße in mm, negativ = Durchdringung, nichts wird verändert)")
    print("Drehprüfungen: Karussell 0 bis 359 Grad in 1-Grad-Schritten, vier Füllstände (leer, 2 ml Rest, halb, 50 ml), sechs Stationen,")
    print("sieben Rollenböcke und Rollen drehen mit. Entnahme: Station vorne, Spritze radial 0 bis 130 mm. 2D exakt, 3D als Prismen.")
    print(line)
    print("Höhenkette neu gerechnet:")
    for n, ist, blatt in ketten:
        print("  %-46s %8.2f   Blatt %8.2f   %s" % (n, ist, blatt, "ok" if abs(ist - blatt) < 0.06 else "ABWEICHUNG"))
    print(line)
    print("%3s  %-70s %5s %8s %8s  %s" % ("Nr", "Prüfung", "Soll", "Ist", "Blatt", "Ergebnis"))
    print("-" * 118)
    n_ok, dev = 0, []
    for nr, text, soll, ist, blatt, note in rows:
        ok = ist >= soll - 1e-9
        n_ok += ok
        flag = "ok" if ok else "FEHLER"
        if note == "Einstellmaß":
            flag = "ok (Einstellmaß)" if ok else "FEHLER"
        if abs(ist - blatt) > 0.15 and note != "Einstellmaß":
            dev.append((nr, text, ist, blatt))
        extra_note = "" if note in ("", "dreht", "Entnahme", "Einstellmaß") else "  [" + note + "]"
        print("%3d  %-70s %5.1f %8.2f %8.2f  %s%s" % (nr, text[:70], soll, ist, blatt, flag, extra_note))
    print("-" * 118)
    print("Bestanden: %d von %d. Kleinster Abstand über alle Prüfungen mit Soll über 1: %.2f mm (Nr %d)." % (
        n_ok, len(rows), min(r[3] for r in rows if r[2] > 1), min((r for r in rows if r[2] > 1), key=lambda r: r[3])[0]))
    if dev:
        print("\nAbweichung zum Blatt über 0,15 mm (Blatt nachziehen):")
        for nr, text, ist, blatt in dev:
            print("  Nr %2d %-64s hier %7.2f  Blatt %7.2f" % (nr, text[:64], ist, blatt))
    print(line)
    print("Zusatzprüfungen (Hinweise):")
    for nr, text, soll, ist in extra:
        ok = ist >= soll - 1e-9
        print("  %-3s %-86s Soll %4.1f  Ist %7.2f  %s" % (nr, text[:86], soll, ist, "ok" if ok else "FEHLER"))
    print("Laufzeit der Prüfung: %.1f s" % dt)
    print(line)


# ============================================================
# Hero: eigener Strahlverfolger (numpy), Material nach CMF-Abschnitt 4.3
# ============================================================
EPS = 2e-3
A_CAM, E_CAM = 30.0, 15.0            # Kamera: 30 Grad von vorne rechts, 15 Grad von oben


def lin(h):
    return np.array(hex2rgb(h)) ** 2.2


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def band(x, lo, hi, s):
    s = np.maximum(s, 1e-6)
    return smoothstep(lo - s, lo + s, x) * (1 - smoothstep(hi - s, hi + s, x))


def wrap180(a):
    return (a + 180.0) % 360.0 - 180.0


# ---------- Zufallsrauschen für Holz
_RS = np.random.RandomState(7)
_LAT = _RS.rand(512, 512).astype(np.float32)


def vnoise(x, y):
    xi, yi = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = (x - xi).astype(np.float32), (y - yi).astype(np.float32)
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = _LAT[yi & 511, xi & 511]
    b = _LAT[yi & 511, (xi + 1) & 511]
    c = _LAT[(yi + 1) & 511, xi & 511]
    d = _LAT[(yi + 1) & 511, (xi + 1) & 511]
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy


def fbm(x, y, n=4):
    s, amp, f = 0.0, 0.5, 1.0
    for _ in range(n):
        s = s + amp * vnoise(x * f, y * f)
        amp *= 0.5
        f *= 2.03
    return s


# ---------- Umgebungslicht: Softboxen als Flächen in endlicher Entfernung, Tischfläche, Deckenlicht
BOXES = [   # Azimut Mitte, Breite (Grad), Abstand, z von, z bis, Intensität, Farbe
    (A_CAM - 62.0, 44.0, 720.0, -50.0, 1500.0, 8.0, (1.00, 0.96, 0.90)),     # Hauptlicht links vorne
    (A_CAM + 82.0, 26.0, 820.0, -50.0, 1500.0, 3.4, (0.90, 0.95, 1.00)),     # Aufheller rechts
    (A_CAM + 156.0, 14.0, 950.0, -50.0, 1500.0, 7.0, (1.00, 0.98, 0.94)),    # Kante rechts hinten
    (A_CAM - 152.0, 14.0, 950.0, -50.0, 1500.0, 6.0, (1.00, 0.98, 0.94)),    # Kante links hinten
]
TISCH_REFL = np.array([0.50, 0.37, 0.24]) * 0.62
KEY_DIR = np.array([math.cos(math.radians(48)) * math.cos(math.radians(A_CAM - 55.0)),
                    math.cos(math.radians(48)) * math.sin(math.radians(A_CAM - 55.0)), math.sin(math.radians(48))])
KEY_COL = np.array([1.00, 0.95, 0.88]) * 2.3
AMB_COL = np.array([0.56, 0.58, 0.63]) * 0.60


def env(P, D, rough):
    """Strahlungsdichte aus Richtung D (n,3) von Punkt P (n,3), rough in Grad-Weichzeichnung."""
    n = len(P)
    s = 2.0 + 34.0 * rough
    dx, dy, dz = D[:, 0], D[:, 1], D[:, 2]
    hxy = np.hypot(dx, dy) + 1e-9
    az = np.degrees(np.arctan2(dy, dx))
    out = np.zeros((n, 3)) + np.array([0.050, 0.047, 0.045])
    occl = np.zeros(n)
    for ac, w, Rb, z0, z1, inten, col in BOXES:
        zhit = P[:, 2] + dz / hxy * Rb
        win = band(wrap180(az - ac), -w / 2, w / 2, s) * band(zhit, z0, z1, Rb * math.tan(math.radians(s)))
        norm = 1.0 / (1.0 + 0.55 * s / (w / 2))
        out = out + (inten * norm * win)[:, None] * np.array(col)
        occl = np.maximum(occl, win)
    # Decke (große Softbox oben)
    up = dz > 1e-4
    t = np.where(up, (1150.0 - P[:, 2]) / np.maximum(dz, 1e-4), 0.0)
    hx, hy = P[:, 0] + t * dx + 80.0, P[:, 1] + t * dy
    ss = t * math.tan(math.radians(s))
    top = up * band(hx, -520, 520, ss) * band(hy, -520, 520, ss)
    out = out + (4.2 / (1.0 + 0.4 * s / 20.0) * top)[:, None] * np.array([1.0, 0.97, 0.93])
    # Tischfläche (nach unten)
    dn = dz < -1e-4
    tt = np.where(dn, -P[:, 2] / np.minimum(dz, -1e-4), 0.0)
    hxx, hyy = P[:, 0] + tt * dx, P[:, 1] + tt * dy
    far = np.hypot(hxx, hyy)
    tab = dn * (1.0 - occl) * (1.0 - smoothstep(900.0, 2200.0, far) * 0.7)
    out = out + tab[:, None] * TISCH_REFL * 0.85
    return out


def schlick(f0, cosi):
    return f0 + (1.0 - f0) * (1.0 - np.clip(cosi, 0, 1)) ** 5


# ---------- Materialtabelle (Stand 6: alles unlackiertes PETG, nichts leuchtet)
class Mat:
    def __init__(self, albedo, rough=0.5, f0=0.04, metal=False, alpha=1.0, interior=False, spec_scale=1.0):
        self.albedo = np.array(albedo, float)
        self.rough, self.f0, self.metal, self.alpha = rough, f0, metal, alpha
        self.interior, self.spec_scale = interior, spec_scale


GOLD_LIN = lin(FARBEN["gold"])
MATS = {
    "sockel": Mat(lin(FARBEN["sockel"]), 0.15, 0.050),                 # PETG schwarz, glänzend (Rauheit etwa 0,15)
    "krone": Mat(lin(FARBEN["koerper"]), 0.50, 0.050),                 # PETG schwarz matt (Rauheit etwa 0,5)
    "koerper": Mat(lin(FARBEN["koerper"]), 0.50, 0.050),
    "gold": Mat(GOLD_LIN, 0.25, 0.0, metal=True),                      # Gold-PETG (Metall 1,0, Rauheit 0,25)
    "nut": Mat(lin("#050506"), 0.9, 0.0),                             # Schattenfugen (Körperteilung, Fensterfugen)
    "front": Mat(lin(FARBEN["sockel"]), 0.15, 0.050),                  # Schubladenfront glänzend
    "glas": Mat(lin(FARBEN["rauch"]), 0.04, 0.045, alpha=0.45),        # Portalscheibe: Rauch-PETG 2 mm
    "klar": Mat(lin(FARBEN["klar"]), 0.05, 0.045, alpha=0.25),         # Seitenfenster: Klar-PETG 1,6 mm
    "loch": Mat([0, 0, 0], alpha=0.0),
    "lid": Mat(lin(FARBEN["koerper"]), 0.50, 0.050),
    "innen": Mat(lin(FARBEN["innen"]), 0.7, 0.03, interior=True),
    "innen_hell": Mat(lin("#2a2a2e"), 0.7, 0.03, interior=True),
    "stahl": Mat(lin(FARBEN["stahl"]), 0.35, 0.0, metal=True, interior=True),
    "messing": Mat(lin(FARBEN["messing"]), 0.35, 0.0, metal=True, interior=True),
    "barrel": Mat(lin(FARBEN["spritze"]), 0.05, 0.05, alpha=0.20, interior=True),
    "silikon": Mat(lin(FARBEN["silikon"]), 0.3, 0.04, alpha=0.65, interior=True),
    "gummi": Mat(lin(FARBEN["gummi"]), 0.8, 0.03, interior=True),
    "stab": Mat(lin("#d8dbde"), 0.3, 0.04, alpha=0.30, interior=True),
    "becherwand": Mat(lin(FARBEN["becher"]), 0.15, 0.05, alpha=0.5, interior=True),
    "schublade": Mat(lin(FARBEN["schublade"]), 0.45, 0.04, interior=True),   # PETG weiß, nicht emissiv
    "podest": Mat(lin(FARBEN["podest"]), 0.4, 0.04, interior=True),          # PETG schwarz
    "schwamm": Mat(lin("#d9d3c0"), 0.9, 0.02, interior=True),
}
for _k, _h in (("cyan", FARBEN["cyan"]), ("magenta", FARBEN["magenta"]), ("gelb", FARBEN["gelb"]),
               ("weiss", FARBEN["weiss"]), ("schwarz", FARBEN["schwarz"]), ("ziel", ZIELFARBE)):
    MATS["farbe_" + _k] = Mat(lin(_h), 0.22, 0.04, interior=True)
MAT_ID = {k: i for i, k in enumerate(MATS)}
MAT_NAME = list(MATS)


# ---------- Portal, Fenster, Schnittfunktionen
def portal_sdf(y, z):
    zm, hh, hw = (16.0 + Z_PORTAL_O) / 2, (Z_PORTAL_O - 16.0) / 2, 36.0
    y, z = np.abs(y), z - zm
    r = np.where(z > 0, 24.0, 8.0)
    qx, qz = y - (hw - r), np.abs(z) - (hh - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0) - r


def win_sdf(u, z):
    qx, qz = np.abs(u) - 11.0, Z_FENSTER0 - z
    box = np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0)
    arch = np.hypot(u, z - Z_FENSTER_M) - 11.0
    return np.where(z >= Z_FENSTER_M, arch, box)


def fw_sdf(y, z):
    """Innenkante des Fensterrahmens (fw_in der SCAD): |Y| 39,4, Oberkante 333,4, obere Ecken R 26,4, unten R 3 (Vorzeichenabstand)."""
    z0 = 60.0
    zm, hh, hw = (z0 + FW_Z1) / 2, (FW_Z1 - z0) / 2, FW_HW
    y, z = np.abs(y), z - zm
    r = np.where(z > 0, FW_RO, 3.0)
    qx, qz = y - (hw - r), np.abs(z) - (hh - r)
    return np.hypot(np.maximum(qx, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, qz), 0) - r


def rahmen_feld(y, z):
    """Abstand zur Innenkante des jeweiligen Rahmens: Bühnenrahmen (unter Z 99, Innenkante = Portalkante) oder Fensterrahmen."""
    return np.where(z < 99.0, portal_sdf(y, z), fw_sdf(y, z))


M_LOCH, M_RAHMEN, M_GLAS, M_NUT, M_FRONT = 1, 2, 3, 4, 5   # Schnittcodes


def hull_cut(px, py, pz, with_windows=True, with_portal=True):
    """Code je Punkt auf der Außenhülle: 0 fest, 1 Loch, 2 Gold-PETG-Rahmen, 3 Klarfenster, 4 Schattenfuge, 5 Schubladenfront."""
    th = np.degrees(np.arctan2(py, px))
    code = np.zeros(px.shape, int)
    if with_portal:
        front = np.abs(th) < 80.0
        ps = portal_sdf(py, pz)
        inside = front & (ps < 0)
        # Portalrahmen aus Gold-PETG, 3 breit: Bühnenrahmen Z 13 bis 97 (Innenkante = Portalkante), Fensterrahmen Z 101 bis 336,4
        fb = front & (ps >= 0) & (ps < RAHMEN_BB) & (pz >= Z_RB0) & (pz <= Z_RB1)
        fs = fw_sdf(py, pz)
        ff = front & (fs >= 0) & (fs < RAHMEN_BB) & (pz >= Z_RF0) & (pz <= Z_RF1)
        code = np.where(fb | ff, M_RAHMEN, code)
        fr = inside & (np.abs(py) <= 34.0) & (pz >= 17.0) & (pz <= Z_LIPPE_G0)
        code = np.where(inside, M_LOCH, code)
        code = np.where(fr, M_FRONT, code)
    if with_windows:
        for p in range(1, 7):
            dth = wrap180(th - p * PITCH)
            u = R_KOERPER * np.sin(np.radians(dth))
            near = np.abs(dth) < 25.0
            ws = np.where(near, win_sdf(u, pz), 9e9)
            code = np.where(ws < 0, M_GLAS, np.where((ws < 1.0) & (code == 0), M_NUT, code))
    return code


# ---------- Primitive
class Prim:
    interior = False

    def surf(self, P, D):
        raise NotImplementedError


class Frustum(Prim):
    def __init__(self, r0, z0, r1, z1, mat, cx=0.0, cy=0.0, cut=None, interior=False):
        self.r0, self.z0, self.r1, self.z1 = r0, z0, r1, z1
        self.k = (r1 - r0) / (z1 - z0) if z1 != z0 else 0.0
        self.mat, self.cx, self.cy, self.cut, self.interior = mat, cx, cy, cut, interior

    def hit(self, ox, oy, oz, dx, dy, dz, t0):
        x, y = ox - self.cx, oy - self.cy
        k = self.k
        rz = self.r0 + k * (oz - self.z0)
        a = dx * dx + dy * dy - k * k * dz * dz
        b = 2.0 * (x * dx + y * dy - k * dz * rz)
        c = x * x + y * y - rz * rz
        disc = b * b - 4 * a * c
        ok = (disc >= 0) & (np.abs(a) > 1e-12)
        sq = np.sqrt(np.where(ok, disc, 0.0))
        den = np.where(ok, 2 * a, 1.0)
        ta, tb = (-b - sq) / den, (-b + sq) / den
        lo, hi = np.minimum(ta, tb), np.maximum(ta, tb)
        best = np.full(ox.shape, np.inf)
        for t in (lo, hi):
            z = oz + t * dz
            rr = self.r0 + k * (z - self.z0)
            v = ok & (t > t0 + EPS) & (z >= self.z0 - 1e-9) & (z <= self.z1 + 1e-9) & (rr > 0)
            best = np.where(v & (t < best), t, best)
        return best

    def surf(self, P, D):
        x, y = P[:, 0] - self.cx, P[:, 1] - self.cy
        rz = np.hypot(x, y) + 1e-12
        N = np.stack([x / rz, y / rz, -self.k * np.ones_like(x)], 1)
        N /= np.linalg.norm(N, axis=1)[:, None]
        back = (N * D).sum(1) > 0
        N = np.where(back[:, None], -N, N)
        mid = np.full(len(x), MAT_ID[self.mat])
        ex = {"back": back}
        if self.cut is not None:
            code = self.cut(P[:, 0], P[:, 1], P[:, 2])
            ex["code"] = code
            mid = np.where(code == M_LOCH, MAT_ID["loch"], mid)
            mid = np.where(code == M_GLAS, MAT_ID["klar"], mid)
            mid = np.where(code == M_NUT, MAT_ID["nut"], mid)
            mid = np.where(code == M_RAHMEN, MAT_ID["gold"], mid)
            mid = np.where(code == M_FRONT, MAT_ID["front"], mid)
            fr = code == M_RAHMEN
            if fr.any():     # erhabene Rahmenhaut (1,5): Fasen an beiden Rändern kippen die Normale (Kantenglanz)
                th = np.arctan2(P[fr, 1], P[fr, 0])
                eu = np.stack([-np.sin(th), np.cos(th), np.zeros_like(th)], 1)
                ez = np.array([0.0, 0.0, 1.0])
                e = 0.25
                f0 = rahmen_feld(P[fr, 1], P[fr, 2])
                gu = (rahmen_feld(P[fr, 1] + e, P[fr, 2]) - rahmen_feld(P[fr, 1] - e, P[fr, 2])) / (2 * e)
                gz = (rahmen_feld(P[fr, 1], P[fr, 2] + e) - rahmen_feld(P[fr, 1], P[fr, 2] - e)) / (2 * e)
                sgn = np.where(f0 < 0.7, -1.0, np.where(f0 > RAHMEN_BB - 0.7, 1.0, 0.0))
                Nf = N[fr] + 1.1 * sgn[:, None] * (gu[:, None] * eu + gz[:, None] * ez)
                N[fr] = Nf / np.linalg.norm(Nf, axis=1)[:, None]
        return N, mid, ex


class Disc(Prim):
    def __init__(self, z, r0, r1, mat, cx=0.0, cy=0.0, cut=None, interior=False):
        self.z, self.r0, self.r1, self.mat, self.cx, self.cy, self.cut, self.interior = z, r0, r1, mat, cx, cy, cut, interior

    def hit(self, ox, oy, oz, dx, dy, dz, t0):
        ok = np.abs(dz) > 1e-9
        t = np.where(ok, (self.z - oz) / np.where(ok, dz, 1.0), np.inf)
        px, py = ox + t * dx - self.cx, oy + t * dy - self.cy
        r = np.hypot(px, py)
        v = ok & (t > t0 + EPS) & (r >= self.r0) & (r <= self.r1)
        return np.where(v, t, np.inf)

    def surf(self, P, D):
        N = np.zeros_like(P)
        N[:, 2] = np.where(D[:, 2] < 0, 1.0, -1.0)
        mid = np.full(len(P), MAT_ID[self.mat])
        ex = {"back": D[:, 2] > 0}
        if self.cut is not None:
            code = self.cut(P[:, 0], P[:, 1], P[:, 2])
            ex["code"] = code
            mid = np.where(code == M_LOCH, MAT_ID["loch"], mid)
        return N, mid, ex


class Box(Prim):
    def __init__(self, x0, x1, y0, y1, z0, z1, mat, interior=True):
        self.lo = np.array([x0, y0, z0], float)
        self.hi = np.array([x1, y1, z1], float)
        self.mat, self.interior = mat, interior

    def hit(self, ox, oy, oz, dx, dy, dz, t0):
        O = np.stack([ox, oy, oz], 1)
        D = np.stack([dx, dy, dz], 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            inv = 1.0 / np.where(np.abs(D) < 1e-12, 1e-12, D)
        ta, tb = (self.lo - O) * inv, (self.hi - O) * inv
        tn = np.minimum(ta, tb).max(1)
        tf = np.maximum(ta, tb).min(1)
        t = np.where(tn > t0 + EPS, tn, np.where(tf > t0 + EPS, tf, np.inf))
        return np.where(tn <= tf, t, np.inf)

    def surf(self, P, D):
        c = (self.lo + self.hi) / 2
        h = (self.hi - self.lo) / 2
        q = (P - c) / h
        ax = np.argmax(np.abs(q), 1)
        N = np.zeros_like(P)
        N[np.arange(len(P)), ax] = np.sign(q[np.arange(len(P)), ax])
        back = (N * D).sum(1) > 0
        N = np.where(back[:, None], -N, N)
        return N, np.full(len(P), MAT_ID[self.mat]), {"back": back}


class PlaneX(Prim):
    """Portalscheibe (Rauch-PETG), ebene Fläche bei x = xc, innerhalb der Portalöffnung (Z 99 bis 330)."""
    def __init__(self, xc, mat):
        self.xc, self.mat, self.interior = xc, mat, False

    def hit(self, ox, oy, oz, dx, dy, dz, t0):
        ok = np.abs(dx) > 1e-9
        t = np.where(ok, (self.xc - ox) / np.where(ok, dx, 1.0), np.inf)
        py, pz = oy + t * dy, oz + t * dz
        v = ok & (t > t0 + EPS) & (portal_sdf(py, pz) < 0) & (pz >= 99.0)
        return np.where(v, t, np.inf)

    def surf(self, P, D):
        N = np.zeros_like(P)
        N[:, 0] = np.where(D[:, 0] < 0, 1.0, -1.0)
        return N, np.full(len(P), MAT_ID[self.mat]), {"back": D[:, 0] > 0}


# ---------- Textur des Namensschilds (Deckel, 90 x 16, Gold-Schrift)
_TEXT_IMG = None


def text_mask():
    global _TEXT_IMG
    if _TEXT_IMG is None:
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        fig = Figure(figsize=(9.0, 1.6), dpi=100, facecolor="black")        # Seitenverhältnis 90 : 16
        cv = FigureCanvasAgg(fig)
        fig.text(0.5, 0.46, "NAME Atelier", ha="center", va="center", color="white", fontsize=74,
                 family=["Caladea", "Liberation Serif", "DejaVu Serif"])
        cv.draw()
        _TEXT_IMG = np.asarray(cv.buffer_rgba())[:, :, 0].astype(np.float32) / 255.0
    return _TEXT_IMG


# ---------- Szene aufbauen
def build_scene(syr_fill=Z_KP_50, ziel=True):
    ext, intr = [], []
    # Außenhülle
    cutP = lambda x, y, z: hull_cut(x, y, z, with_windows=False)
    cutW = lambda x, y, z: hull_cut(x, y, z, with_windows=True)
    # Goldring und Goldlippe: Ausschnitte (Ring am Portal offen, Lippe nur vor der Front)
    cutRing = lambda x, y, z: np.where((x > 0) & (np.abs(y) < GOLDRING_GAP), M_LOCH, 0)
    cutFalz = lambda x, y, z: np.where((x > 0) & (np.abs(y) < GOLDRING_GAP) & (portal_sdf(y, z) >= 0), 0, M_LOCH)
    cutLip = lambda x, y, z: np.where((x > 0) & (np.abs(y) <= 34.0), 0, M_LOCH)
    ext.append(Frustum(R_FUSS_AUSSEN, Z_GRUND0, R_SOCKEL_OBEN, 97.0, "sockel", cut=cutP))
    # Goldring Ø 202 (Gold-PETG) auf dem Sockel, unten außen 0,8 x 45 Grad Fase (Schattenfuge), am Portal offen
    ext.append(Frustum(R_RING - 0.8, Z_RING0, R_RING, Z_RING0 + 0.8, "gold", cut=cutRing))
    ext.append(Frustum(R_RING, Z_RING0 + 0.8, R_RING, Z_RING1, "gold", cut=cutRing))
    ext.append(Disc(Z_RING1, R_KOERPER, R_RING, "gold", cut=cutRing))
    ext.append(Frustum(R_SOCKELFALZ, Z_RING0, R_SOCKELFALZ, Z_RING1, "sockel", cut=cutFalz))      # Sockelfalz im Ausschnitt des Rings
    # Körper in zwei Hälften, die Teilung bei Z 235 ist die Schattenfuge (V-Nut 1,0 breit, 0,5 tief)
    ext.append(Frustum(R_KOERPER, Z_RING1, R_KOERPER, Z_KTEIL - FUGE_FASE, "koerper", cut=cutW))
    ext.append(Frustum(R_KOERPER, Z_KTEIL - FUGE_FASE, R_KOERPER - FUGE_FASE, Z_KTEIL, "nut", cut=cutW))
    ext.append(Frustum(R_KOERPER - FUGE_FASE, Z_KTEIL, R_KOERPER, Z_KTEIL + FUGE_FASE, "nut", cut=cutW))
    ext.append(Frustum(R_KOERPER, Z_KTEIL + FUGE_FASE, R_KOERPER, 338.0, "koerper", cut=cutW))
    ext.append(Frustum(R_KOERPER, Z_FUGE0, R_KOERPER, Z_FUGE1, "gold"))                            # Goldband
    ext.append(Frustum(R_KRONE, Z_FUGE1, R_KRONE, Z_FASE, "krone"))
    ext.append(Frustum(R_KRONE, Z_FASE, R_KRONE - 6.0, H_GESAMT, "gold"))                          # Kronenring (Fase 6 x 45 Grad)
    ext.append(Disc(H_GESAMT, R_KRONE - 6.0 - 2.0, R_KRONE - 6.0, "gold"))                         # Oberkante des Kronenrings
    ext.append(Disc(H_GESAMT, 0.0, R_KRONE - 6.0 - 2.0, "lid"))                                    # Kronendeckel mit Namensschild
    # Goldlippe 3 x 1,5 oben auf der Schubladenfront
    r_lippe = r_sock(Z_LIPPE_G0) + 1.5
    ext.append(Frustum(r_lippe, Z_LIPPE_G0, r_lippe, Z_LIPPE_G1, "gold", cut=cutLip))
    ext.append(Disc(Z_LIPPE_G1, r_sock(Z_LIPPE_G1), r_lippe, "gold", cut=cutLip))
    ext.append(PlaneX(90.5, "glas"))
    # ---- Innenleben
    I = lambda p: (setattr(p, "interior", True), intr.append(p))[1]
    I(Disc(7.0, 0.0, 100.0, "innen"))                                     # Grundplatte
    I(Frustum(20.0, 7.0, 20.0, 40.0, "innen_hell"))                       # Lagerbock
    I(Disc(40.0, 0.0, 20.0, "innen_hell"))
    I(Frustum(23.5, 43.0, 23.5, 51.0, "innen_hell"))                      # GT2-Rad 70 Z
    I(Disc(51.0, 0.0, 23.5, "innen_hell"))
    # Wägezelle und Stufe der Bühne
    I(Box(50.65, 63.35, -70.0, 10.0, Z_WZ0, Z_WZ1, "stahl"))
    I(Frustum(30.0, Z_POD0, 30.0, Z_POD1, "podest", cx=RS))               # Podestscheibe Ø 60, PETG schwarz
    I(Disc(Z_POD1, 0.0, 30.0, "podest", cx=RS))
    # Schublade (PETG weiß): Boden, Seitenwände
    I(Box(22.0, 104.0, -33.0, 33.0, Z_BODEN0, Z_BODEN1, "schublade"))
    I(Box(22.0, 104.0, -35.0, -33.0, Z_BODEN0, 45.0, "schublade"))
    I(Box(22.0, 104.0, 33.0, 35.0, Z_BODEN0, 45.0, "schublade"))
    # Becher mit Farbe
    I(Frustum(BECHER_RU, Z_BECHER0, BECHER_RO, Z_BECHER1, "becherwand", cx=RS))
    zp = Z_BECHER0 + 22.5
    rp = lambda z: BECHER_RU + (BECHER_RO - BECHER_RU) * (z - Z_BECHER0) / (Z_BECHER1 - Z_BECHER0) - 0.8
    I(Frustum(rp(Z_BECHER0 + 1.0), Z_BECHER0 + 1.0, rp(zp), zp, "farbe_ziel", cx=RS))
    I(Disc(zp, 0.0, rp(zp), "farbe_ziel", cx=RS))
    # Feuchtrinne mit Schwamm
    cutR = lambda x, y, z: np.where(np.abs(np.degrees(np.arctan2(y, x))) < 38.0, M_LOCH, 0)
    I(Frustum(69.0, Z_RINNE0, 69.0, Z_RINNE1, "innen_hell", cut=cutR))
    I(Frustum(45.0, Z_RINNE0, 45.0, Z_RINNE1, "innen_hell", cut=cutR))
    I(Disc(Z_RINNE1, 45.0, 69.0, "innen_hell", cut=cutR))
    I(Disc(Z_RDECKEL, 45.0, 69.0, "innen_hell", cut=cutR))              # Rinnendeckel
    # Karussell
    I(Frustum(R_PLATTE, Z_PLATTE0, R_PLATTE, Z_PLATTE1, "innen"))
    I(Disc(Z_PLATTE1, 0.0, R_PLATTE, "innen"))
    I(Disc(Z_PLATTE0, 0.0, R_PLATTE, "innen"))
    I(Frustum(86.5, Z_LAUF0, 86.5, Z_LAUF1, "innen_hell", cut=cutR))
    I(Frustum(74.5, Z_LAUF0, 74.5, Z_LAUF1, "innen_hell", cut=cutR))
    I(Disc(Z_LAUF1, 74.5, 86.5, "innen_hell", cut=cutR))
    for j in range(7):                                                     # Rollenböcke und Rollen
        a = math.radians((j + 0.5) * PITCH)
        cx, cy = 80.0 * math.cos(a), 80.0 * math.sin(a)
        I(Frustum(7.0, Z_ROLLE0 + 0.0, 7.0, Z_ROLLE1, "stahl", cx=cx, cy=cy))
    # Stößel: Spindel, Führungswellen, Schlitten, Ausleger, Stempel, Motor
    S = Z_SPARK
    I(Frustum(4.0, 250.0, 4.0, Z_BR0, "stahl"))
    for sy in (-22.0, 22.0):
        I(Frustum(5.0, Z_SMIN + SL_U, 5.0, Z_BR0, "stahl", cy=sy))
    I(Frustum(34.0, S + SL_U, 34.0, S + SL_U + SL_H, "innen_hell"))
    I(Disc(S + SL_U, 0.0, 34.0, "innen_hell"))
    # Ausleger mit Stempel: ein gedrucktes PETG-Teil (schwarz matt), darunter 2 mm Gummiauflage
    I(Box(28.0, 36.0, -12.5, 12.5, S + 8.0, S + 48.0, "innen"))          # senkrechte Platte am Schlitten
    I(Box(28.0, 68.0, -12.5, 12.5, S + 8.0, S + 16.0, "innen"))          # waagrechter Arm
    I(Frustum(STEMPEL_D / 2, S + 2.0, STEMPEL_D / 2, S + 8.0, "innen", cx=STEMPEL_X))   # Stempelfuß Ø 25
    I(Frustum(STEMPEL_D / 2, S, STEMPEL_D / 2, S + 2.0, "gummi", cx=STEMPEL_X))         # Gummiauflage
    I(Disc(S, 0.0, STEMPEL_D / 2, "gummi", cx=STEMPEL_X))
    I(Box(-80.15, -37.85, -21.15, 21.15, Z_M1_0, Z_M1_1, "innen_hell"))
    I(Disc(Z_BR0, 0.0, 98.0, "innen"))
    # Zuganker
    for a in ZUGANKER_W:
        I(Frustum(ZUGANKER_RAD, Z_GRUND1, ZUGANKER_RAD, Z_BR1, "stahl",
                  cx=ZUGANKER_R * math.cos(math.radians(a)), cy=ZUGANKER_R * math.sin(math.radians(a))))
    # Innenwand der Hülle von innen: dieselbe Hülle (zweiseitig) liefert die Rückwand
    # Sechs Spritzen mit Farbe, alle voll (Ruhe), Kolbenplatte bei 50 ml
    kp = syr_fill
    piston = kp - SPITZE_KOLBEN
    for p in range(1, 7):
        a = math.radians(p * PITCH)
        cx, cy = RS * math.cos(a), RS * math.sin(a)
        farbe = ["", "weiss", "gelb", "magenta", "cyan", "schwarz", "weiss"][p]
        I(Frustum(15.0, Z_ZYL0, 15.0, Z_ZYL1, "barrel", cx=cx, cy=cy))
        I(Frustum(5.0, Z_VENTIL1, 3.0, Z_KONUS1, "barrel", cx=cx, cy=cy))
        I(Frustum(4.5, Z_VENTIL0, 4.5, Z_VENTIL1, "silikon", cx=cx, cy=cy))
        I(Frustum(13.4, Z_ZYL0 + 0.2, 13.4, piston, "farbe_" + farbe, cx=cx, cy=cy))
        I(Disc(piston, 0.0, 13.4, "farbe_" + farbe, cx=cx, cy=cy))
        I(Box(cx - 5.0, cx + 5.0, cy - 5.0, cy + 5.0, piston, kp - 3.0, "stab"))
        I(Frustum(19.0, kp - 3.0, 19.0, kp, "stab", cx=cx, cy=cy))
        I(Disc(kp, 0.0, 19.0, "stab", cx=cx, cy=cy))
    return ext, intr


# ---------- Tischfläche (Holz) und Schatten
def sd_cylz(P, r, z0, z1):
    d = np.stack([np.hypot(P[:, 0], P[:, 1]) - r, np.abs(P[:, 2] - (z0 + z1) / 2) - (z1 - z0) / 2], 1)
    return np.minimum(np.maximum(d[:, 0], d[:, 1]), 0) + np.hypot(np.maximum(d[:, 0], 0), np.maximum(d[:, 1], 0))


def sdf_env(P):
    return np.minimum(np.minimum(sd_cylz(P, 100.0, 3.0, 97.0), sd_cylz(P, 99.0, 90.0, 341.0)), sd_cylz(P, 101.0, 341.0, H_GESAMT))


def soft_shadow(P, L, k=7.0, steps=26):
    res = np.ones(len(P))
    t = np.full(len(P), 4.0)
    for _ in range(steps):
        Q = P + L * t[:, None]
        h = sdf_env(Q)
        res = np.minimum(res, np.clip(k * h / t, 0.0, 1.0))
        t = t + np.clip(h, 3.0, 70.0)
        if (t > 900).all():
            break
    r = np.clip(res, 0, 1)
    return r * r * (3 - 2 * r)


def holz_albedo(X, Y, dist):
    """Heller Eichentisch, Bretter entlang Y, Fuge alle 150 mm."""
    pl = np.floor((X + 37.0) / 150.0)
    fx = (X + 37.0) - pl * 150.0
    seed = vnoise(pl * 3.7 + 0.5, pl * 1.3 + 9.1)
    fade = 1.0 - smoothstep(500.0, 2600.0, dist) * 0.85
    warp = (fbm(Y * 0.0028 + pl * 3.1, X * 0.012, 3) - 0.5) * 40.0
    ring = np.sin((X + warp + pl * 17.0) * 0.28 + 2.2 * fbm(Y * 0.006, X * 0.03, 3))
    fine = fbm(Y * 0.0045 + pl * 5.3, X * 0.55, 3) - 0.5
    tone = (seed - 0.5) * 0.14 + (fbm(Y * 0.0009 + pl, X * 0.004, 2) - 0.5) * 0.12
    g = 1.0 + tone * 1.4 + fade * (0.085 * ring + 0.32 * fine)
    base = np.array([0.76, 0.56, 0.36])
    col = (base[None, :] * g[:, None]) ** 2.2
    seam = np.exp(-np.minimum(fx, 150.0 - fx) ** 2 / 0.5)
    col = col * (1.0 - 0.55 * seam)[:, None]
    return col


class Hero:
    def __init__(self, W, H, ss=1.5):
        self.W, self.H, self.ss = W, H, ss
        self.ext, self.intr = build_scene()
        self.allp = self.ext + self.intr
        self.WS, self.HS = int(round(W * ss)), int(round(H * ss))
        a, e = math.radians(A_CAM), math.radians(E_CAM)
        self.tgt = np.array([0.0, 0.0, 190.0])
        self.dist = 1480.0
        self.cam = self.tgt + self.dist * np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)])
        fwd = self.tgt - self.cam
        fwd /= np.linalg.norm(fwd)
        right = np.cross(fwd, [0, 0, 1.0])
        right /= np.linalg.norm(right)
        up = np.cross(right, fwd)
        self.fwd, self.right, self.up = fwd, right, up
        self.vspan = 590.0                       # sichtbare Höhe in mm in der Zielebene
        self.fpx = (self.HS / 2) / (self.vspan / 2 / self.dist)
        self.shift_y = -8.0                      # Bildmitte etwas nach unten schieben (Gerät sitzt im Bild)

    def ray_dirs(self, i0, i1):
        ii, jj = np.mgrid[i0:i1, 0:self.WS]
        u = (jj + 0.5 - self.WS / 2) / self.fpx
        v = (self.HS / 2 - (ii + 0.5)) / self.fpx + self.shift_y / self.dist
        D = self.fwd[None, None, :] + u[..., None] * self.right + v[..., None] * self.up
        D /= np.linalg.norm(D, axis=2)[..., None]
        return D.reshape(-1, 3)

    # ---------- Schattierung einer Gruppe gleicher Materialien
    def shade(self, mat, P, N, D, ex):
        m = MATS[mat]
        n = len(P)
        V = -D
        cosv = np.clip((N * V).sum(1), 0.0, 1.0)
        R = D - 2.0 * (N * D).sum(1)[:, None] * N
        irr = AMB_COL[None, :] * (0.55 + 0.45 * np.clip(N[:, 2] * 0.5 + 0.5, 0, 1))[:, None] \
            + KEY_COL[None, :] * np.clip((N * KEY_DIR).sum(1), 0, 1)[:, None]
        if m.interior:
            # Innenteile bekommen nur das Umgebungslicht, das durch die Hülle fällt: die Bühne (unter Z 97) ist nach vorne offen,
            # darüber kommt es durch das Rauch-PETG-Portal und die sechs Klarfenster (etwa ein Drittel)
            zz = P[:, 2]
            irr = irr * (0.30 + 0.58 * smoothstep(112.0, 80.0, zz))[:, None]
        diff = m.albedo[None, :] * irr * (0.0 if m.metal else 1.0)
        sc = m.spec_scale * (0.12 if m.interior else 1.0)
        if m.f0 > 0 or m.metal:
            En = env(P, R, m.rough)
            if m.metal:
                F = m.albedo[None, :] + (1.0 - m.albedo[None, :]) * ((1.0 - cosv) ** 5)[:, None]
                spec = F * En * sc
                if mat == "gold":
                    lum = En.mean(1)
                    sh, li = lin(FARBEN["gold_s"]), lin(FARBEN["gold_l"])
                    base = sh[None, :] + (li - sh)[None, :] * smoothstep(0.02, 0.9, lum)[:, None]
                    spec = base * (0.55 + 0.45 * np.minimum(lum * 2.0, 1.0))[:, None] * 1.1 + 0.25 * En * li[None, :] * np.minimum(lum, 3.0)[:, None]
                    diff = diff * 0
            else:
                F = schlick(m.f0, cosv)[:, None]
                spec = F * En * sc
        else:
            spec = np.zeros((n, 3))
        if mat == "lid":
            # Namensschild 90 x 16 im Deckel (schwarze Basis, Gold-Schrift), Leserichtung von vorne (Zeilenkopf zeigt nach hinten, -X)
            img = text_mask()
            hh, ww = img.shape
            iu = np.clip(((0.5 + P[:, 1] / 90.0) * ww).astype(int), 0, ww - 1)
            iv = np.clip(((0.5 + P[:, 0] / 16.0) * hh).astype(int), 0, hh - 1)
            msk = img[iv, iu]
            gl = lin(FARBEN["gold"]) * (0.8 + 0.8 * np.minimum(En.mean(1) * 3.0, 1.0))[:, None]
            diff = diff * (1 - msk)[:, None] + gl * msk[:, None]
            spec = spec * (1 - msk)[:, None]
        alpha = np.full(n, m.alpha)
        if m.alpha < 1.0:
            # Fresnel-Rand macht Glas an flachen Winkeln deckender
            alpha = np.clip(m.alpha + (1.0 - m.alpha) * (1.0 - cosv) ** 4 * 0.9, 0, 1)
        return diff, spec, alpha

    def closest(self, prims, O, D, t0, idx_sub=None):
        n = len(O)
        best = np.full(n, np.inf)
        bid = np.full(n, -1)
        ox, oy, oz = O[:, 0], O[:, 1], O[:, 2]
        dx, dy, dz = D[:, 0], D[:, 1], D[:, 2]
        for i, p in enumerate(prims):
            t = p.hit(ox, oy, oz, dx, dy, dz, t0)
            m = t < best
            best = np.where(m, t, best)
            bid = np.where(m, i, bid)
        return best, bid

    # ---------- Hauptschleife für einen Strahlblock
    def trace_block(self, D):
        n = len(D)
        O = np.tile(self.cam, (n, 1))
        col = np.zeros((n, 3))
        T = np.ones((n, 3))
        t0 = np.zeros(n)
        inside = np.zeros(n, bool)
        # Begrenzung: nur Strahlen, die den Zylinder r 112, z -5 bis 405 treffen, laufen in den Gerätepfad
        ox, oy, oz = O[:, 0], O[:, 1], O[:, 2]
        a = D[:, 0] ** 2 + D[:, 1] ** 2
        b = 2 * (ox * D[:, 0] + oy * D[:, 1])
        c = ox ** 2 + oy ** 2 - 112.0 ** 2
        disc = b * b - 4 * a * c
        hit = disc > 0
        tt = (-b - np.sqrt(np.maximum(disc, 0))) / (2 * a)
        zh = oz + tt * D[:, 2]
        t_top = (405.0 - oz) / D[:, 2]
        hit &= ((zh >= -5) & (zh <= 405)) | ((D[:, 2] < 0) & ((oz + t_top * D[:, 2]) > -1) &
                                           (np.hypot(ox + t_top * D[:, 0], oy + t_top * D[:, 1]) < 112.0))
        active = np.where(hit)[0]
        esc_idx, esc_O, esc_D, esc_T = [], [], [], []
        for layer in range(9):
            if active.size == 0:
                break
            Oa, Da, t0a = O[active], D[active], t0[active]
            best, bid = self.closest(self.ext, Oa, Da, t0a)
            ins = inside[active]
            if ins.any():
                sel = np.where(ins)[0]
                b2, i2 = self.closest(self.intr, Oa[sel], Da[sel], t0a[sel])
                better = b2 < best[sel]
                best[sel] = np.where(better, b2, best[sel])
                bid[sel] = np.where(better, i2 + len(self.ext), bid[sel])
            missed = ~np.isfinite(best)
            if missed.any():
                mi = active[missed]
                esc_idx.append(mi)
                esc_O.append(O[mi] + t0[mi][:, None] * D[mi])
                esc_D.append(D[mi])
                esc_T.append(T[mi])
            keep = ~missed
            nxt = []
            for pid in np.unique(bid[keep]):
                sel = np.where(keep & (bid == pid))[0]
                gi = active[sel]
                p = self.allp[pid]
                tH = best[sel]
                P = Oa[sel] + tH[:, None] * Da[sel]
                N, mid, ex = p.surf(P, Da[sel])
                diffs = np.zeros((len(sel), 3))
                specs = np.zeros((len(sel), 3))
                alph = np.ones(len(sel))
                for mm in np.unique(mid):
                    s2 = np.where(mid == mm)[0]
                    name = MAT_NAME[mm]
                    exs = {k: v[s2] for k, v in ex.items()}
                    d_, s_, a_ = self.shade(name, P[s2], N[s2], Da[sel][s2], exs) if name != "loch" else \
                        (np.zeros((len(s2), 3)), np.zeros((len(s2), 3)), np.zeros(len(s2)))
                    diffs[s2], specs[s2], alph[s2] = d_, s_, a_
                    if name in ("loch", "glas", "klar"):
                        inside[gi[s2]] = True
                col[gi] += T[gi] * (alph[:, None] * diffs + specs)
                T[gi] = T[gi] * (1.0 - alph)[:, None]
                t0[gi] = tH
            alive = np.zeros(n, bool)
            alive[active[keep]] = True
            alive &= T.max(1) > 0.02
            active = np.where(alive)[0]
        # Strahlen, die nach den Schichten noch Anteil haben, gehen zum Tisch
        if active.size:
            esc_idx.append(active)
            esc_O.append(O[active] + t0[active][:, None] * D[active])
            esc_D.append(D[active])
            esc_T.append(T[active])
        return col, T, (np.concatenate(esc_idx) if esc_idx else np.zeros(0, int),
                              np.vstack(esc_O) if esc_O else np.zeros((0, 3)),
                              np.vstack(esc_D) if esc_D else np.zeros((0, 3)),
                              np.vstack(esc_T) if esc_T else np.zeros((0, 3)))

    # ---------- Tisch und Hintergrund
    def ground(self, O, D, withrefl=True):
        n = len(O)
        out = np.zeros((n, 3))
        down = D[:, 2] < -1e-5
        t = np.where(down, -O[:, 2] / np.where(down, D[:, 2], -1.0), 0.0)
        Pg = O + t[:, None] * D
        dist = np.linalg.norm(Pg - self.cam, axis=1)
        # Hintergrund oben: warmes Grau, Verlauf
        bg = np.array([0.36, 0.30, 0.25])
        res = np.tile(bg, (n, 1))
        gi = np.where(down)[0]
        if gi.size:
            P = Pg[gi]
            alb = holz_albedo(P[:, 0], P[:, 1], dist[gi])
            sh = soft_shadow(P + np.array([0, 0, 0.5]), KEY_DIR)
            sdist = np.maximum(sdf_env(P), 0.0)
            ao = 1.0 - 0.80 * np.exp(-sdist / 30.0) - 0.15 * np.exp(-sdist / 120.0)
            irr = AMB_COL[None, :] * 1.05 * ao[:, None] + KEY_COL[None, :] * (KEY_DIR[2] * sh * (0.25 + 0.75 * ao))[:, None]
            color = alb * irr
            # Lackierte Oberfläche: Spiegelung der Softboxen und des Geräts
            Dg = D[gi]
            cosv = np.clip(-Dg[:, 2], 0, 1)
            F = (0.03 + 0.97 * (1.0 - cosv) ** 5)
            R = Dg * np.array([1, 1, -1.0])
            En = env(P, R, 0.30)
            refl = F[:, None] * En * 0.55
            if withrefl:
                near = np.hypot(P[:, 0], P[:, 1]) < 520.0
                ii = np.where(near)[0]
                if ii.size:
                    cr, hr = self.reflect_device(P[ii], R[ii])
                    refl[ii] = refl[ii] * (1 - hr)[:, None] + (F[ii][:, None] * cr * 0.80) * hr[:, None]
            color = color + refl
            far = smoothstep(750.0, 2300.0, dist[gi])
            color = color * (1 - far)[:, None] + bg[None, :] * far[:, None]
            res[gi] = color
        # Himmel/Hintergrund: oben Verlauf
        up = ~down
        if up.any():
            res[up] = bg
        return res

    def reflect_device(self, P, R):
        """Spiegelbild des Geräts im Tisch: Strahl vom Tischpunkt nach oben gegen die Außenhülle."""
        n = len(P)
        col = np.zeros((n, 3))
        hit = np.zeros(n)
        t0 = np.zeros(n)
        # gestreute Spiegelung: zwei leicht versetzte Strahlen
        rng = np.random.RandomState(3)
        acc = np.zeros((n, 3))
        acch = np.zeros(n)
        ns = 2
        for s in range(ns):
            jit = rng.normal(0, 0.012, (n, 3))
            Dj = R + jit * np.array([1, 1, 0.3])
            Dj /= np.linalg.norm(Dj, axis=1)[:, None]
            best, bid = self.closest(self.ext, P, Dj, t0)
            ok = np.isfinite(best)
            for pid in np.unique(bid[ok]):
                sel = np.where(ok & (bid == pid))[0]
                p = self.ext[pid]
                Q = P[sel] + best[sel][:, None] * Dj[sel]
                N, mid, ex = p.surf(Q, Dj[sel])
                for mm in np.unique(mid):
                    s2 = np.where(mid == mm)[0]
                    name = MAT_NAME[mm]
                    if name in ("loch", "glas", "klar"):
                        c = np.tile(np.array([0.012, 0.012, 0.014]), (len(s2), 1))
                    else:
                        d_, s_, a_ = self.shade(name, Q[s2], N[s2], Dj[sel][s2],
                                                {k: v[s2] for k, v in ex.items()})
                        c = d_ + s_
                    acc[sel[s2]] += c
                acch[sel] += 1.0
        hit = acch / ns
        col = acc / np.maximum(acch, 1.0)[:, None] * (acch > 0)[:, None]
        # Ausblenden mit der Entfernung des Treffers ist über den Fresnel-Faktor schon enthalten
        return col, np.clip(hit, 0, 1)

    # ---------- Bild
    def render(self, verbose=True):
        t0 = time.time()
        H, W = self.HS, self.WS
        img = np.zeros((H, W, 3), np.float32)
        rows = 96
        gnd_O, gnd_D, gnd_I, gnd_T = [], [], [], []
        for i0 in range(0, H, rows):
            i1 = min(H, i0 + rows)
            D = self.ray_dirs(i0, i1)
            col, T, (ei, eO, eD, eT) = self.trace_block(D)
            base = i0 * W
            flat = img.reshape(-1, 3)
            flat[base:base + len(D)] = col
            # Strahlen ohne Trefferweg direkt zum Tisch (außerhalb der Begrenzung)
            all_idx = np.arange(len(D))
            handled = np.zeros(len(D), bool)
            handled[ei] = True
            # Strahlen, die die Begrenzung nie trafen
            ri = all_idx[~handled & (T.min(1) > 0.999)]
            # ei enthält die entkommenen; nicht getroffene Strahlen (hit=False) sind in keiner Liste
            # und haben T = 1 und col = 0
            bound_free = ~handled
            bf = np.where(bound_free & (col.sum(1) == 0) & (T.min(1) > 0.999))[0]
            gnd_I.append(np.concatenate([ei + base, bf + base]))
            gnd_O.append(np.vstack([eO, np.tile(self.cam, (len(bf), 1))]))
            gnd_D.append(np.vstack([eD, D[bf]]))
            gnd_T.append(np.vstack([eT, np.ones((len(bf), 3))]))
            if verbose:
                print("   Hero Zeilen %d bis %d, %.0f s" % (i0, i1, time.time() - t0), flush=True)
        gi = np.concatenate(gnd_I)
        gO, gD, gT = np.vstack(gnd_O), np.vstack(gnd_D), np.vstack(gnd_T)
        flat = img.reshape(-1, 3)
        chunk = 200000
        for s in range(0, len(gi), chunk):
            sl = slice(s, s + chunk)
            c = self.ground(gO[sl], gD[sl])
            flat[gi[sl]] += (gT[sl] * c).astype(np.float32)
            if verbose:
                print("   Tisch %d von %d, %.0f s" % (s, len(gi), time.time() - t0), flush=True)
        self.raw = img
        return img


# ============================================================
# Nachbearbeitung des Hero (Bloom, Tonwerte, Vignette) und Zeichnungen in 2D
# ============================================================
def tonemap(raw):
    """Tonwerte und Vignette (Stand 6: kein Glühen, nichts leuchtet, daher kein Bloom)."""
    img = raw.astype(np.float64)
    exposure = 1.18
    c = 1.0 - np.exp(-exposure * np.clip(img, 0, None))
    # leichte S-Kurve für Kontrast
    c = np.clip(c, 0, 1)
    c = c * c * (3 - 2 * c) * 0.35 + c * 0.65
    c = c ** (1 / 2.2)
    H, W = c.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    r2 = ((xx - W / 2) / (W / 2)) ** 2 * 0.8 + ((yy - H * 0.47) / (H / 2)) ** 2 * 0.7
    c = c * (1.0 - 0.30 * np.clip(r2 - 0.25, 0, 1.5))[..., None]
    return np.clip(c, 0, 1)


def downsample(img, W, H):
    try:
        from PIL import Image
        im = Image.fromarray((img * 255 + 0.5).astype(np.uint8))
        return np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float64) / 255.0
    except Exception:
        fy, fx = img.shape[0] / H, img.shape[1] / W
        yi = np.clip((np.arange(H) * fy).astype(int), 0, img.shape[0] - 1)
        xi = np.clip((np.arange(W) * fx).astype(int), 0, img.shape[1] - 1)
        return img[yi][:, xi]


# ============================================================
# Zeichenstil
# ============================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Wedge, PathPatch, FancyBboxPatch, Ellipse, Arc, FancyArrowPatch
from matplotlib.path import Path
from matplotlib import font_manager as _fm

PAPER = "#F3EFE7"
CARD = "#FBF9F4"
INK = "#1D1B19"
INK2 = "#5E5A53"
INK3 = "#9A948A"
GOLDC = FARBEN["gold"]
GOLDD = "#9C7B2E"
CUT = "#2A2A2F"
CUT_EDGE = "#0B0B0D"
STEELC = "#A9ABB1"
WEISSC = FARBEN["schublade"]          # PETG weiß (Schublade)
SILIC = "#E4DDC9"
GLASC = "#6C6C74"

_FONTS = {f.name for f in _fm.fontManager.ttflist}


def pick(*names):
    for n in names:
        if n in _FONTS:
            return n
    return "DejaVu Sans"


SANS = pick("Inter", "Liberation Sans", "Carlito", "DejaVu Sans")
SERIF = pick("Caladea", "Liberation Serif", "DejaVu Serif")
plt.rcParams["font.family"] = SANS
plt.rcParams["axes.unicode_minus"] = False


def dez(x, n=1):
    """Deutsche Dezimalschreibweise."""
    return ("%." + str(n) + "f") % x if False else (("%." + str(n) + "f") % x).replace(".", ",")


def lighten(h, f):
    c = np.array(hex2rgb(h))
    return tuple(np.clip(c + (1 - c) * f, 0, 1))


def darken(h, f):
    c = np.array(hex2rgb(h))
    return tuple(np.clip(c * (1 - f), 0, 1))


class Pane:
    """Zeichenfläche in Pixelkoordinaten der Figur (Ursprung links oben)."""
    def __init__(self, fig, x, y, w, h, FW, FH):
        self.fig, self.x, self.y, self.w, self.h, self.FW, self.FH = fig, x, y, w, h, FW, FH

    def axes(self, xlim=None, ylim=None, equal=True, inset=(0, 0, 0, 0)):
        l, t, r, b = inset
        ax = self.fig.add_axes([(self.x + l) / self.FW, 1 - (self.y + self.h - b) / self.FH,
                                (self.w - l - r) / self.FW, (self.h - t - b) / self.FH])
        ax.set_axis_off()
        if xlim is not None:
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
        if equal:
            ax.set_aspect("equal", adjustable="box")
        return ax


def card(fig, x, y, w, h, FW, FH, fc=CARD, ec="#DAD3C5", lw=1.0):
    ax = fig.add_axes([0, 0, 1, 1], facecolor="none")
    ax.set_xlim(0, FW)
    ax.set_ylim(FH, 0)
    ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=10", fc=fc, ec=ec, lw=lw))
    return ax


def label_text(ax, x, y, s, size=11, color=INK, weight="normal", ha="left", va="center", family=None, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va, family=family or SANS, **kw)


def spread_labels(zs, zmin, zmax, gap):
    """Zielhöhen so verteilen, dass der Abstand mindestens gap beträgt (sortiert absteigend)."""
    order = np.argsort(zs)[::-1]
    pos = np.array(zs, float)[order]
    for i in range(1, len(pos)):
        pos[i] = min(pos[i], pos[i - 1] - gap)
    if pos[0] > zmax:
        pos += zmax - pos[0]
    if pos[-1] < zmin:
        # von unten her nach oben schieben
        pos[-1] = zmin
        for i in range(len(pos) - 2, -1, -1):
            pos[i] = max(pos[i], pos[i + 1] + gap)
        if pos[0] > zmax:
            gap2 = (zmax - zmin) / max(len(pos) - 1, 1)
            pos = zmax - gap2 * np.arange(len(pos))
    out = np.zeros(len(pos))
    out[order] = pos
    return out


# ============================================================
# 2) Schnitt in der XZ-Ebene (Y = 0), Dosierstellung: Cyan (Platz 4) vorne
# ============================================================
KP_D = 276.2                 # Kolbenplatte Oberkante beim Dosieren (etwa 25 ml Rest)
CUP_FILL = 15.0              # Füllhöhe im Becher (mm)


def r_sock(z):
    return R_FUSS_AUSSEN - (R_FUSS_AUSSEN - R_SOCKEL_OBEN) * (z - Z_GRUND0) / (97.0 - Z_GRUND0)


def cup_r(z):
    return BECHER_RU + (BECHER_RO - BECHER_RU) * (z - Z_BECHER0) / (Z_BECHER1 - Z_BECHER0)


def draw_schnitt(ax):
    """Zeichnet den Schnitt, liefert Beschriftungsankerpunkte (x, z, Titel, Detail, Seite)."""
    S = KP_D                                  # Stempel liegt auf der Kolbenplatte
    pb = KP_D - SPITZE_KOLBEN                 # Kolbenboden
    cyan = FARBEN["cyan"]

    def R(x0, x1, z0, z1, fc, ec=CUT_EDGE, lw=0.6, z=5, alpha=1.0, hatch=None, ls="-"):
        ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha, hatch=hatch, ls=ls))

    def P(pts, fc, ec=CUT_EDGE, lw=0.6, z=5, alpha=1.0, closed=True):
        ax.add_patch(Polygon(pts, closed=closed, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha))

    def Ln(xs, zs, c=INK, lw=0.7, z=6, ls="-", alpha=1.0):
        ax.plot(xs, zs, color=c, lw=lw, zorder=z, ls=ls, alpha=alpha, solid_capstyle="butt")

    # ---- Tisch
    ax.add_patch(Rectangle((-112, -14), 224, 14, fc="#D8BE95", ec="none", zorder=0))
    Ln([-150, 150], [0, 0], c="#7A6240", lw=1.2, z=1)
    # ---- Hüllenfläche (Rauminnere als helle Fläche)
    sil = [(-r_sock(3), 3), (-r_sock(97), 97), (-R_KOERPER, 97), (-R_KOERPER, 341), (-R_KRONE, 341), (-R_KRONE, Z_FASE),
           (-96, H_GESAMT), (96, H_GESAMT), (R_KRONE, Z_FASE), (R_KRONE, 341), (R_KOERPER, 341), (R_KOERPER, 97), (r_sock(97), 97),
           (r_sock(3), 3)]
    P(sil, "#ECE7DC", ec="none", z=1)
    # ---- Hülle, hinten (X < 0)
    P([(-r_sock(3), 3), (-r_sock(97), 97), (-r_sock(97) + WAND, 97), (-r_sock(3) + WAND, 3)], CUT, z=7)
    # Goldring (Gold-PETG) auf dem Sockel, innen r 97,3, unten außen 0,8 Fase; Sockelfalz geht bis Z 104 hindurch
    P([(-R_GOLDRING_IN, Z_RING0), (-(R_RING - 0.8), Z_RING0), (-R_RING, Z_RING0 + 0.8), (-R_RING, Z_RING1), (-R_GOLDRING_IN, Z_RING1)],
      GOLDC, ec=GOLDD, lw=0.4, z=9)
    R(-R_SOCKELFALZ, -R_KOERPER_IN, Z_RING0, Z_RING1 + 3.0, CUT, z=7, lw=0.3)
    # Körper mit Schattenfuge bei Z 235 (V-Nut 1,0 breit, 0,5 tief, Kerbe an der Außenkante)
    R(-R_KOERPER, -R_KOERPER_IN, 101.0, 338.0, CUT, z=7)
    ue = 2.4      # Kerbe im Bild 2,4fach überhöht (wahre Größe 1,0 x 0,5 wäre nur etwa 1 Pixel)
    P([(-R_KOERPER - 0.3, Z_KTEIL - ue * FUGE_FASE - 0.3), (-R_KOERPER + ue * FUGE_FASE, Z_KTEIL), (-R_KOERPER - 0.3, Z_KTEIL + ue * FUGE_FASE + 0.3)],
      CARD, ec="none", z=10)
    # Goldband (Gold-PETG, Wand 1,6) Z 338 bis 341 mit Steckern 2 mm in Körper und Krone (Wand 1,2)
    R(-R_KOERPER, -R_KOERPER + 1.6, Z_FUGE0, Z_FUGE1, GOLDC, ec=GOLDD, lw=0.4, z=9)
    R(-(R_KOERPER_IN - SP), -(R_KOERPER_IN - SP - 1.2), Z_FUGE0 - 2.0, Z_FUGE0, GOLDC, ec=GOLDD, lw=0.3, z=9)
    R(-(R_KOERPER_IN - SP), -(R_KOERPER_IN - SP - 1.2), Z_FUGE1, Z_FUGE1 + 2.0, GOLDC, ec=GOLDD, lw=0.3, z=9)
    # Krone (schwarzer Körper, Hohlprofil nach der SCAD) mit Kronenring aus Gold-PETG auf der Fase
    for sg in (-1, 1):
        kr = [(99.6, Z_FUGE1), (R_KRONE, Z_FUGE1), (R_KRONE, Z_FASE), (R_KRONE - 2.0, Z_FASE), (R_KRONE - 8.0, H_GESAMT), (0, H_GESAMT),
              (0, H_GESAMT - 2.0), (R_KRONE - 8.4, H_GESAMT - 2.0), (R_KRONE - 4.4, Z_FASE), (R_KRONE - 4.4, Z_FASE - 3.0), (99.6, Z_FASE - 3.0)]
        P([(sg * x, z) for x, z in kr], "#0E0E11", z=8)
        P([(sg * R_KRONE, Z_FASE), (sg * (R_KRONE - 6.0), H_GESAMT), (sg * (R_KRONE - 8.0), H_GESAMT), (sg * (R_KRONE - 2.0), Z_FASE)],
          GOLDC, ec=GOLDD, lw=0.4, z=9)
    # Namensschild 90 x 16 x 1,2 in der Krone: schwarze Basis, Gold-Schrift (hier im Schnitt als Streifen angedeutet)
    R(-8, 8, H_GESAMT - 1.2, H_GESAMT - 0.6, "#050506", ec="none", z=9)
    R(-6, 6, H_GESAMT - 0.6, H_GESAMT, GOLDC, ec="none", z=9)
    # ---- Hülle, vorne (X > 0): nur unterhalb und oberhalb des Portals
    P([(r_sock(3), 3), (r_sock(16), 16), (r_sock(16) - WAND, 16), (r_sock(3) - WAND, 3)], CUT, z=7)
    R(R_KOERPER_IN, R_KOERPER, Z_PORTAL_O, 338.0, CUT, z=7)
    # Portalrahmen aus Gold-PETG, 3 breit, 1,5 erhaben: oben der Balken des Fensterrahmens Z 333,4 bis 336,4, unten der Bühnenrahmen Z 13 bis 16
    R(R_KOERPER, R_KOERPER + RAHMEN_T, FW_Z1, Z_RF1, GOLDC, ec=GOLDD, lw=0.4, z=9)
    P([(r_sock(Z_RB0), Z_RB0), (r_sock(Z_RB0) + RAHMEN_T, Z_RB0), (r_sock(Z_PORTAL_U) + RAHMEN_T, Z_PORTAL_U), (r_sock(Z_PORTAL_U), Z_PORTAL_U)],
      GOLDC, ec=GOLDD, lw=0.4, z=9)
    R(R_KOERPER_IN, R_KOERPER, Z_FUGE0, Z_FUGE1, GOLDC, ec=GOLDD, lw=0.4, z=9)                   # Goldband
    R(R_KOERPER_IN - SP - 1.2, R_KOERPER_IN - SP, Z_FUGE0 - 2.0, Z_FUGE0, GOLDC, ec=GOLDD, lw=0.3, z=9)
    R(R_KOERPER_IN - SP - 1.2, R_KOERPER_IN - SP, Z_FUGE1, Z_FUGE1 + 2.0, GOLDC, ec=GOLDD, lw=0.3, z=9)
    R(R_KOERPER, R_KRONE, 341.0, 341.8, "#222", ec="none", z=8)
    # Portalscheibe, Rauch-PETG 2 mm, zwei Hälften mit Überlappung (Fuge außen Z 215, innen Z 219, hinter der Karussellplatte)
    xi, xm, xa = 88.5, 89.5, 90.5
    R(xi, xa, 99.0, Z_SCHEIBE_NAHT_A, GLASC, ec="none", z=9, alpha=0.9)
    R(xi, xm, Z_SCHEIBE_NAHT_A, Z_SCHEIBE_NAHT_I, GLASC, ec="none", z=9, alpha=0.9)
    R(xm, xa, Z_SCHEIBE_NAHT_A, Z_SCHEIBE_NAHT_I, "#7E7E86", ec="none", z=9, alpha=0.9)
    R(xi, xa, Z_SCHEIBE_NAHT_I, 333.0, GLASC, ec="none", z=9, alpha=0.9)
    ax.add_patch(Rectangle((xi, 99.0), xa - xi, 333.0 - 99.0, fc="none", ec="#444", lw=0.5, zorder=9))
    Ln([xm, xa], [Z_SCHEIBE_NAHT_A] * 2, c="#444", lw=0.5, z=10)
    Ln([xi, xm], [Z_SCHEIBE_NAHT_I] * 2, c="#444", lw=0.5, z=10)
    Ln([xm, xm], [Z_SCHEIBE_NAHT_A, Z_SCHEIBE_NAHT_I], c="#444", lw=0.5, z=10)
    # Schubladenfront (folgt der Sockelkontur, glänzend) mit Goldlippe 3 x 1,5 oben
    P([(r_sock(17) - 8, 17), (r_sock(17), 17), (r_sock(45), 45), (r_sock(45) - 8, 45)], "#0B0B0D", z=8)
    P([(r_sock(Z_LIPPE_G0) - 3.0, Z_LIPPE_G0), (r_sock(Z_LIPPE_G0) + 1.5, Z_LIPPE_G0), (r_sock(Z_LIPPE_G0) + 1.5, Z_LIPPE_G1),
       (r_sock(Z_LIPPE_G0) - 3.0, Z_LIPPE_G1)], GOLDC, ec=GOLDD, lw=0.4, z=9)
    # ---- Grundplatte, Füße, Ballast (hinter der Ebene), Zuganker (hinter der Ebene)
    R(-100, 100, Z_GRUND0, Z_GRUND1, "#3A3A40", z=6)
    for sx in (-1, 1):
        R(sx * 79.7 - 6, sx * 79.7 + 6, 0, 3, "#222", ec="none", z=3, alpha=0.7)
    for r_, a in BALLAST[:3]:
        cx = r_ * math.cos(math.radians(a))
        R(cx - 18.5, cx + 18.5, Z_GRUND1, Z_BALLAST1, "#BBBDC2", ec="#7C7E84", lw=0.5, z=3, alpha=0.75)
    for a in ZUGANKER_W[::2]:
        cx = ZUGANKER_R * math.cos(math.radians(a))
        R(cx - 2.5, cx + 2.5, Z_GRUND1, Z_BR1, "#C7C9CE", ec="#8C8D91", lw=0.4, z=3, alpha=0.8)
        for zm in (Z_LAUF0 - 4.0, Z_LAUF1, 331.0, Z_BR0 - 4.0):
            R(cx - 4.0, cx + 4.0, zm, zm + 4.0, "#A9ABB1", ec="#6E7076", lw=0.3, z=3, alpha=0.8)   # Muttern M5
        R(cx - 5.0, cx + 5.0, 333.0, 336.0, "#3A3A40", ec="none", z=3, alpha=0.8)                   # Fugenhalter unter dem Goldband
    # ---- Lagerbock, Welle, Lager
    R(-20, -11, 7, 40, "#3A3A40", z=6)
    R(11, 20, 7, 40, "#3A3A40", z=6)
    R(-11, 11, 10, 17, "#76787E", z=6, lw=0.4)
    R(-11, 11, 33, 40, "#76787E", z=6, lw=0.4)
    R(-4, 4, 9, 221, STEELC, ec="#55575C", lw=0.5, z=7)
    # GT2-Rad 70 Z mit Nabe und Magnet
    R(-23.5, 23.5, 43, 51, "#3C3C42", z=6)
    R(-10, 10, 41, 43, "#3C3C42", z=6)
    for k in range(-5, 6):
        R(k * 4 - 0.7, k * 4 + 0.7, 51, 52, "#3C3C42", ec="none", z=6)
    R(13, 17, 41.4, 43, "#D63A3A", ec="none", z=7)
    R(13.5, 16.5, 39.9, 41.4, "#2E7BD0", ec="none", z=7)                # Hall-Sensor unter dem Magneten
    # Motor 2 (Pancake) mit Riemenscheibe und Riemen
    R(-78.95, -36.65, 17, 40, "#4A4A50", z=6)
    R(-59.3, -56.3, 40, 51, STEELC, ec="none", z=6)
    R(-65.8, -49.8, 43, 51, "#6E7076", z=6, lw=0.4)
    Ln([-49.8, -23.5], [43.4, 43.4], c="#222", lw=1.0)
    Ln([-49.8, -23.5], [50.6, 50.6], c="#222", lw=1.0)
    # ---- Wägezelle, Podest, Schublade, Becher
    R(50.65, 63.35, Z_WZ0, Z_WZ1, "#C9CCD2", ec="#6E7076", lw=0.6, z=6, hatch="////")
    R(53, 61, 6.0, Z_WZ0 - 0.0, "#F0B040", ec="none", z=6)
    R(50, 64, Z_WZ1, Z_POD0, FARBEN["podest"], ec="#888", lw=0.4, z=6)                    # Stiel Ø 14
    R(27, 87, Z_POD0, Z_POD1, FARBEN["podest"], ec="#8A867C", lw=0.5, z=7)                # Podest Ø 60, PETG schwarz
    R(22, r_sock(27.5) - 8, Z_BODEN0, Z_BODEN1, WEISSC, ec="#8A867C", lw=0.5, z=7)        # Schublade PETG weiß
    R(22, r_sock(40), 27.5, 45, WEISSC, ec="#9A968C", lw=0.4, z=4, alpha=0.55)           # Seitenwand hinter der Ebene
    # Becher
    cwall = [(RS - BECHER_RU, Z_BECHER0), (RS - BECHER_RO, Z_BECHER1), (RS - BECHER_RO + 0.9, Z_BECHER1),
             (RS - BECHER_RU + 0.9, Z_BECHER0 + 0.9), (RS + BECHER_RU - 0.9, Z_BECHER0 + 0.9), (RS + BECHER_RO - 0.9, Z_BECHER1),
             (RS + BECHER_RO, Z_BECHER1), (RS + BECHER_RU, Z_BECHER0)]
    P(cwall, "#E8E8E8", ec="#8A8A8A", lw=0.5, z=8, alpha=0.95)
    zf = Z_BECHER0 + 0.9 + CUP_FILL
    zielc = "#8E3B76"
    P([(RS - cup_r(Z_BECHER0 + 0.9) + 0.9, Z_BECHER0 + 0.9), (RS - cup_r(zf) + 0.9, zf), (RS + cup_r(zf) - 0.9, zf),
       (RS + cup_r(Z_BECHER0 + 0.9) - 0.9, Z_BECHER0 + 0.9)], zielc, ec="none", z=7)
    # ---- Feuchtrinne (hinten geschnitten), Schwamm
    R(-69, -45, Z_RINNE0, Z_RINNE0 + 2, "#2B2B30", z=6)
    R(-69, -45, Z_RINNE1, Z_RDECKEL, "#2B2B30", z=6)                     # Deckel
    R(-69, -67, Z_RINNE0, Z_RINNE1, "#2B2B30", z=6)
    R(-47, -45, Z_RINNE0, Z_RINNE1, "#2B2B30", z=6)
    R(-67, -47, Z_RINNE0 + 2, Z_RINNE1, "#D9D3C0", ec="#8A8470", lw=0.4, z=6)
    R(-67, -47, Z_RINNE0 + 2, Z_RINNE0 + 7, "#9CC9E4", ec="none", z=6, alpha=0.85)
    # ---- Karussell: Platte, Nabe, Laufring, Rolle (hinten bei 180 Grad), Kragen
    plate = [(-R_PLATTE, Z_PLATTE0), (41, Z_PLATTE0), (41, Z_FL0), (34, Z_FL0), (34, Z_PLATTE1), (-R_PLATTE, Z_PLATTE1)]
    P(plate, "#34343A", z=6)
    R(-15, 15, 205, Z_PLATTE0, "#34343A", z=6)
    R(-86.5, -74.5, Z_LAUF0, Z_LAUF1, "#4C4C54", z=6)
    R(-83.5, -76.5, Z_ROLLE0, Z_ROLLE1, STEELC, ec="#55575C", lw=0.5, z=7)
    R(-85.5, -74.5, Z_BOCK0, Z_PLATTE0, "#4C4C54", ec="none", z=5, alpha=0.65)
    R(-81.0, -79.0, 197.0, 202.0, "#E0A030", ec="none", z=8)
    # ---- Spritze Platz 4 (Cyan) vorne
    R(RS - 15, RS + 15, Z_ZYL0, Z_ZYL1, "#DCE6EC", ec="#6A7A84", lw=0.6, z=5, alpha=0.55)
    R(RS - 13.4, RS + 13.4, Z_ZYL0 + 0.1, pb, cyan, ec="none", z=6)
    R(RS - 13.4, RS + 13.4, pb, pb + 7, "#18181A", ec="none", z=7)
    R(RS - 6, RS + 6, pb + 7, KP_D - 3, "#F2F4F5", ec="#7A858C", lw=0.5, z=7)
    R(RS - 19, RS + 19, KP_D - 3, KP_D, "#E6EAEC", ec="#6A7A84", lw=0.6, z=8)
    R(RS - 22.5, RS + 22.5, Z_FL0, Z_FL1, "#E6EAEC", ec="#6A7A84", lw=0.6, z=8)
    P([(RS - 4, Z_KONUS1), (RS + 4, Z_KONUS1), (RS + 3, Z_VENTIL1), (RS - 3, Z_VENTIL1)], "#DCE6EC", ec="#6A7A84", lw=0.6, z=6)
    P([(RS - 4.5, Z_VENTIL1), (RS + 4.5, Z_VENTIL1), (RS + 3.6, 70.0), (RS + 0.7, Z_VENTIL0), (RS - 0.7, Z_VENTIL0), (RS - 3.6, 70.0)],
      FARBEN["silikon"], ec="#8D8670", lw=0.6, z=7)
    # Farbfaden und Tropfen
    R(RS - 0.7, RS + 0.7, zf + 1.0, Z_VENTIL0 - 0.2, cyan, ec="none", z=7)
    ax.add_patch(Circle((RS, zf + 0.9), 1.6, fc=cyan, ec="none", zorder=7))
    # ---- Stößel
    # Ausleger mit Stempel: ein gedrucktes PETG-Teil (schwarz matt), Platte X 28 bis 36, Arm bis X 68, Stempelfuß Ø 25, Gummi 2 mm
    AUSL = "#1C1C1E"
    R(28, 36, S + 8, S + 48, AUSL, ec="#000", lw=0.5, z=8)
    R(28, 68, S + 8, S + 16, AUSL, ec="#000", lw=0.5, z=8)
    R(STEMPEL_X - STEMPEL_D / 2, STEMPEL_X + STEMPEL_D / 2, S + 2, S + 8, AUSL, ec="#000", lw=0.5, z=8)
    R(STEMPEL_X - STEMPEL_D / 2, STEMPEL_X + STEMPEL_D / 2, S, S + 2, "#5A5A5E", ec="#000", lw=0.4, z=9)      # Gummiauflage
    P([(36, S + 16), (58, S + 16), (36, S + 36)], "#8E8E96", ec="#55575C", lw=0.4, z=7, alpha=0.7)             # Stützrippe hinter der Ebene
    for zs in (S + 24, S + 40):      # zwei M4 in Gewindeeinsätzen im Schlitten, Senkung in der Platte
        R(20, 34, zs - 2, zs + 2, "#8C8D91", ec="#55575C", lw=0.3, z=9)
        R(32, 36, zs - 3.4, zs + 3.4, "#8C8D91", ec="#55575C", lw=0.3, z=9)
    R(-34, 28, S + SL_U, S + SL_U + SL_H, "#3C3C42", z=6)
    R(-11, 11, S + 35.5, S + 39.0, FARBEN["messing"], ec="#6B5530", lw=0.4, z=8)          # Flansch Messingmutter
    R(-5, 5, S + 20.5, S + 35.5, FARBEN["messing"], ec="#6B5530", lw=0.4, z=8)
    R(-5, 5, Z_SMIN + SL_U, Z_WELLE1, STEELC, ec="#55575C", lw=0.4, z=4)                   # Führungswelle dahinter
    R(-4, 4, 250.0, Z_SPINDEL1, "#C8CAD0", ec="#55575C", lw=0.5, z=9)
    R(-8, 8, 372.8, Z_BR0, STEELC, ec="#55575C", lw=0.4, z=9)
    for sy in (-22, 22):
        pass
    R(-5.5, 5.5, S + SL_U - 3, S + 18, "#BFC1C7", ec="#70727A", lw=0.4, z=4, alpha=0.9)      # Führungswelle (nicht geschnitten, y = 22)
    # ---- Brücke, Riemen, Motor 1
    R(-98, 98, Z_BR0, Z_BR1, "#34343A", z=6)
    R(-5, 5, Z_BR0, Z_BR1, "#76787E", z=7)
    for xm in (0.0, -59.0):
        R(xm - 8, xm + 8, Z_RIEMEN0, Z_RIEMEN1, "#6E7076", z=7, lw=0.4)
        R(xm - 6.5, xm + 6.5, Z_RIEMEN1, Z_GT2_OBEN, "#6E7076", z=7, lw=0.4)   # Nabe
    for sx in (-1, 1):
        R(sx * 22 - 10, sx * 22 + 10, Z_BR1, Z_BR1 + 10.0, "#34343A", z=5, alpha=0.7)   # Klemmnaben dahinter
    Ln([-51, -8], [Z_RIEMEN0 + 1.2, Z_RIEMEN0 + 1.2], c="#222", lw=1.0)
    Ln([-51, -8], [Z_RIEMEN1 - 1.2, Z_RIEMEN1 - 1.2], c="#222", lw=1.0)
    R(-80.15, -37.85, Z_M1_0, Z_M1_1, "#4A4A50", z=6)
    R(-60.5, -57.5, Z_M1_1, Z_GT2_OBEN - 0.5, STEELC, ec="none", z=7)
    # ---- Geisterspritzen (volle Spritzen hinter der Ebene, y > 0)
    ghost = [(51.43, FARBEN["schwarz"]), (102.86, FARBEN["weiss"])]
    for th, fcol in ghost:
        cx = RS * math.cos(math.radians(th))
        R(cx - 15, cx + 15, Z_ZYL0, Z_ZYL1, "#DCE6EC", ec="#9AA8B0", lw=0.5, z=2, alpha=0.5)
        R(cx - 13.4, cx + 13.4, Z_ZYL0, Z_KP_50 - SPITZE_KOLBEN, fcol, ec="none", z=2, alpha=0.55)
        R(cx - 5, cx + 5, Z_KP_50 - SPITZE_KOLBEN, Z_KP_50 - 3, "#EEF0F2", ec="#9AA8B0", lw=0.4, z=2, alpha=0.6)
        R(cx - 19, cx + 19, Z_KP_50 - 3, Z_KP_50, "#E6EAEC", ec="#9AA8B0", lw=0.5, z=2, alpha=0.7)
        R(cx - 22.5, cx + 22.5, Z_FL0, Z_FL1, "#E6EAEC", ec="#9AA8B0", lw=0.4, z=2, alpha=0.7)
        P([(cx - 4, Z_KONUS1), (cx + 4, Z_KONUS1), (cx + 3, Z_VENTIL1), (cx - 3, Z_VENTIL1)], "#DCE6EC", ec="#9AA8B0", lw=0.4, z=2, alpha=0.6)
        R(cx - 4.5, cx + 4.5, Z_VENTIL0, Z_VENTIL1, "#DAD6CC", ec="#9AA8B0", lw=0.4, z=2, alpha=0.6)
    # ---- Maßpfeile am Rand (Schnittebene, vorne)
    # Pfeil "vorne"
    ax.annotate("", xy=(205, -44), xytext=(160, -44), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.0, mutation_scale=9), zorder=2)
    ax.text(182, -37, "vorne", fontsize=9.5, color=INK2, ha="center", va="center", zorder=2)

    # ---- Beschriftungen: (x, z, Titel, Detail, Seite)
    L = [
        (-99.0, 395.0, "Krone, abnehmbar", "PETG matt, Kronenring Gold-PETG", "l"),
        (-30.0, 392.0, "Riemen GT2 20 : 20", "Scheiben 16 hoch, Brücke mit 608", "l"),
        (-59.0, 365.0, "Motor 1, NEMA 17", "34 mm, hängt unter der Brücke", "l"),
        (-98.0, 339.5, "Goldband, Gold-PETG", "Z 338 bis 341, Fugenhalter darunter", "l"),
        (-100.8, 235.0, "Schattenfuge Körperteilung", "V-Nut 1,0 x 0,5, Z 235 (Kerbe überhöht)", "l"),
        (-97.2, 275.0, "Körper Ø 196", "PETG matt, Wand 1,6", "l"),
        (-80.0, 200.0, "Laufrolle 608 und Laufring", "7 Rollen", "l"),
        (-60.0, 217.0, "Karussellplatte Ø 171", "PETG schwarz, Nabe zentriert", "l"),
        (-4.0, 150.0, "Karussellwelle Ø 8", "Lagerbock mit zwei 608", "l"),
        (-100.5, 99.0, "Goldring Ø 202, Gold-PETG", "unten Fase 0,8, am Portal offen", "l"),
        (-58.0, 60.0, "Feuchtrinne mit Deckel", "Schwamm nass, 6 Löcher Ø 14", "l"),
        (-22.0, 47.0, "GT2-Rad 70 Z", "1 : 3,5, Magnet für Hall", "l"),
        (-58.0, 29.0, "Motor 2, Pancake 23 mm", "Karussell, Silikondämpfer", "l"),
        (-44.0, 14.5, "Ballast 0,48 kg", "4 Stapel M20, hinter der Ebene", "l"),
        (-99.5, 70.0, "Sockel, glänzend", "PETG, Kegel Ø 204 auf 196", "l"),
        (4.0, 362.0, "Spindel T8, Steigung 2", "selbsthemmend, Stellring oben", "r"),
        (24.0, 304.0, "Schlitten mit Messingmutter", "2 x LM10LUU auf Wellen Ø 10", "r"),
        (32.0, 318.0, "Ausleger mit Stempel, PETG (ein Teil)", "schwarz matt, Gummi 2 mm, 2 x M4", "r"),
        (99.0, 335.0, "Portalrahmen, Gold-PETG", "3 breit, 1,5 erhaben", "r"),
        (89.5, 260.0, "Portalscheibe, Rauch-PETG 2 mm", "78 x 234, zwei Hälften, Magnete", "r"),
        (70.0, KP_D - 1.5, "Kolbenplatte Ø 38", "Stempel 4 mm innen", "r"),
        (70.0, 150.0, "Spritze 60 ml, Cyan", "Nutzfüllung 50 ml, Füllmarke", "r"),
        (76.0, 221.0, "Flansch in der Tasche", "Rastzunge, Einlaufschräge", "r"),
        (58.5, 72.0, "Entenschnabelventil", "Spitze 7 mm über dem Becherrand", "r"),
        (RS + 22.0, 40.0, "Becher 60 ml, Zielfarbe", "Sitz konisch, bis 50 g", "r"),
        (91.0, 46.0, "Schublade, Front mit Goldlippe", "PETG weiß, Lippe Gold-PETG 3 x 1,5", "r"),
        (57.0, 22.0, "Podest Ø 60, PETG schwarz", "liegt zum Wiegen auf der Wägezelle", "r"),
        (57.0, 14.0, "Wägezelle 500 g", "unter Podest und Schublade", "r"),
        (-12.7 + 12.0, 262.0, "Volle Spritzen", "hinter der Schnittebene", "r"),
    ]
    return L


def draw_schnitt_beschriftung(ax, L, zmin=-8.0, zmax=412.0, xl=-128.0, xr=128.0, fs=9.6, gap=17.0):
    for side, xt, ha in (("l", xl, "right"), ("r", xr, "left")):
        items = [it for it in L if it[4] == side]
        zs = spread_labels([it[1] for it in items], zmin + 8, zmax, gap)
        for (ax_, az_, t1, t2, _), zt in zip(items, zs):
            sg = -1 if side == "l" else 1
            xe = xt + (-sg) * 0
            ax.plot([ax_, xt - sg * 6.0], [az_, zt], color=INK2, lw=0.55, zorder=20)
            ax.add_patch(Circle((ax_, az_), 1.35, fc=INK, ec="white", lw=0.4, zorder=21))
            ax.text(xt - sg * 4.0, zt + 3.8, t1, fontsize=fs, color=INK, ha=ha, va="center", fontweight="bold", zorder=22, bbox=dict(fc=CARD, ec="none", pad=0.8))
            ax.text(xt - sg * 4.0, zt - 3.4, t2, fontsize=fs - 1.6, color=INK2, ha=ha, va="center", zorder=22, bbox=dict(fc=CARD, ec="none", pad=0.8))


# ============================================================
# 3) Draufsicht (ohne Krone und Brücke), Ruhestellung: Platz 0 vorne
# ============================================================
def pl(r, th_deg):
    """Gerät (Radius, theta von +X gegen den Uhrzeigersinn von oben) nach Zeichenebene (x = Y rechts, y = -X, vorne unten)."""
    t = math.radians(th_deg)
    return (r * math.sin(t), -r * math.cos(t))


def pxy(X, Y):
    return (Y, -X)


def rot_xy(pts, a_deg):
    t = math.radians(a_deg)
    c, s = math.cos(t), math.sin(t)
    return [(c * x - s * y, s * x + c * y) for x, y in pts]


def slot_poly(th_deg, rout=R_PLATTE):
    """Zylinderschlitz mit Halbkreisende (Mitte r 57, R 16), nach außen offen, als Polygon in der Zeichenebene."""
    pts = []
    for a in np.linspace(math.pi / 2, 3 * math.pi / 2, 24):
        pts.append((RS + 16 * math.cos(a), 16 * math.sin(a)))
    pts += [(rout, -16), (rout, 16)]
    # Reihenfolge: Halbkreis von +y über -x nach -y, dann außen
    pts = [(x, y) for x, y in pts]
    return [pxy(*p) for p in rot_xy(pts, th_deg)]


def pocket_poly(th_deg, rout=R_PLATTE):
    """Flanschtasche 46 x 33, Innenecken R5, nach außen bis zum Rand."""
    pts = []
    x0, x1, hy, ri = RS - 23.0, rout, 16.5, 5.0
    pts.append((x1, -hy))
    pts.append((x1, hy))
    pts.append((x0 + ri, hy))
    for a in np.linspace(math.pi / 2, math.pi, 8):
        pts.append((x0 + ri + ri * math.cos(a), hy - ri + ri * math.sin(a)))
    pts.append((x0, -hy + ri))
    for a in np.linspace(math.pi, 1.5 * math.pi, 8):
        pts.append((x0 + ri + ri * math.cos(a), -hy + ri + ri * math.sin(a)))
    return [pxy(*p) for p in rot_xy(pts, th_deg)]


def draw_draufsicht(ax):
    # Sockel, Goldring
    ax.add_patch(Circle((0, 0), R_FUSS_AUSSEN, fc="#E4DED0", ec="#B7AF9E", lw=0.8, zorder=1))
    # Goldring Ø 202 (Gold-PETG, innen r 97,3), am Portal offen (|Y| < 39)
    ga = math.degrees(math.asin(GOLDRING_GAP / R_RING))
    ax.add_patch(Wedge((0, 0), R_RING, ga - 90, 360 - ga - 90, width=R_RING - R_GOLDRING_IN, fc=GOLDC, ec=GOLDD, lw=0.5, zorder=3))
    # Bühnenrahmen auf dem Sockelkegel (|Y| 36 bis 39, Z 13 bis 97), von oben als schmale Leisten neben dem Portal
    for sg in (-1, 1):
        x0, x1 = sorted((sg * HW_PORTAL, sg * (HW_PORTAL + RAHMEN_BB)))
        ax.add_patch(Rectangle((x0, -R_FUSS_AUSSEN + 0.5), x1 - x0, R_FUSS_AUSSEN - R_KOERPER - 0.5, fc=GOLDC, ec=GOLDD, lw=0.4, zorder=3))
    # Körperwand mit Portal und Fenstern (Lücken)
    gaps = [(-math.degrees(math.asin(36.0 / R_KOERPER)), math.degrees(math.asin(36.0 / R_KOERPER)), "portal")]
    half_w = math.degrees(math.asin(11.0 / R_KOERPER))
    for p in range(1, 7):
        gaps.append((p * PITCH - half_w, p * PITCH + half_w, "fenster"))
    gaps.sort()
    segs = []
    prev = gaps[0][1]
    for g0, g1, _ in gaps[1:]:
        segs.append((prev, g0))
        prev = g1
    segs.append((prev, gaps[0][0] + 360.0))
    for a0, a1 in segs:
        ax.add_patch(Wedge((0, 0), R_KOERPER + 0.0, a0 - 90, a1 - 90, width=WAND + 0.2, fc="#111114", ec="#111114", lw=0.3, zorder=4))
    for g0, g1, kind in gaps:
        if kind == "fenster":
            ax.add_patch(Wedge((0, 0), R_KOERPER, g0 - 90, g1 - 90, width=WAND, fc=FARBEN["klar"], ec="#333", lw=0.4, zorder=4))
        else:
            # Fensterrahmen (Gold-PETG, |Y| 39,4 bis 42,4, 1,5 erhaben) links und rechts vom Portal
            for sg in (-1, 1):
                aa = sorted((math.degrees(math.asin(FW_HW / R_KOERPER)), math.degrees(math.asin((FW_HW + RAHMEN_BB) / R_KOERPER))))
                a0, a1 = (aa[0], aa[1]) if sg > 0 else (-aa[1], -aa[0])
                ax.add_patch(Wedge((0, 0), R_KOERPER + RAHMEN_T, a0 - 90, a1 - 90, width=WAND + RAHMEN_T, fc=GOLDC, ec=GOLDD, lw=0.4, zorder=5))
    ax.add_patch(Circle((0, 0), R_KOERPER_IN, fc="#F2EEE4", ec="none", zorder=2))
    # Verdeckte Teile darunter (gestrichelt)
    dash = dict(ls=(0, (4, 3)), lw=0.9, zorder=6)
    ax.add_patch(Rectangle((-35, -107), 70, 85, fc="none", ec="#8A857A", **dash))                    # Schublade
    ax.add_patch(Circle(pxy(RS, 0), BECHER_RO, fc=ZIELFARBE, ec="#8A857A", alpha=0.0, lw=0.9, ls=(0, (4, 3)), zorder=6))
    ax.add_patch(Circle(pxy(RS, 0), BECHER_RO, fc="none", ec="#8A857A", **dash))
    # Feuchtrinne r 45 bis 69, offen vorne +-38
    for r in (45.0, 69.0):
        ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=38 - 90 + 0, theta2=-38 - 90 + 360, ec="#5C8DB3", **dash))
    for sg in (-1, 1):
        ax.plot(*zip(pl(45, sg * 38), pl(69, sg * 38)), color="#5C8DB3", lw=0.9, ls=(0, (4, 3)), zorder=6)
    # Abstreiflippen +-40
    for sg in (-1, 1):
        ax.plot(*zip(pl(50, sg * 40), pl(64, sg * 40)), color="#B8860B", lw=2.4, zorder=7, solid_capstyle="butt")
    # Motor 2 (unter der Platte, hinten)
    ax.add_patch(Rectangle(pxy(-36.65, -21.15)[::-1] if False else (-21.15, 36.65), 42.3, 42.3, fc="none", ec="#8A857A", **dash))
    # Karussellplatte
    ax.add_patch(Circle((0, 0), R_PLATTE, fc="#34343A", ec="#16161A", lw=1.0, zorder=8))
    for p in range(1, 7):
        th = p * PITCH
        ax.add_patch(Polygon(pocket_poly(th), closed=True, fc="#44444C", ec="none", zorder=9))
        ax.add_patch(Polygon(slot_poly(th), closed=True, fc="#F2EEE4", ec="#16161A", lw=0.7, zorder=10))
        # Stationsbuchstabe (C, M, Y, W, K, W) 0,6 tief eingraviert neben der Tasche, Leserichtung von vorne
        lx, ly_ = pxy(*rot_xy([(76.0, 16.5 + 8.2)], th)[0])
        ax.text(lx, ly_, STATIONSBUCHSTABE[p - 1], fontsize=11, fontweight="bold", color="#8A8A94", ha="center", va="center",
                rotation=th, rotation_mode="anchor", zorder=11, family=SANS)
    # Laufringlücke (verdeckt)
    for sg in (-1, 1):
        ax.plot(*zip(pl(74.5, sg * 15), pl(86.5, sg * 15)), color="#8A857A", lw=1.0, ls=(0, (3, 2)), zorder=11)
    ax.add_patch(Arc((0, 0), 2 * 80.5, 2 * 80.5, theta1=-15 - 90, theta2=15 - 90, ec="#C8C2B4", lw=1.0, ls=(0, (3, 2)), zorder=11))
    # Spritzen: Flansch, Kolbenplatte
    for p in range(1, 7):
        th = p * PITCH
        fl = [(RS - 22.5, -16), (RS + 22.5, -16), (RS + 22.5, 16), (RS - 22.5, 16)]
        ax.add_patch(Polygon([pxy(*q) for q in rot_xy(fl, th)], closed=True, fc="#E6EAEC", ec="#7A858C", lw=0.6, alpha=0.95, zorder=12))
        cx, cy = pl(RS, th)
        ax.add_patch(Circle((cx, cy), 19.0, fc=lighten(PLATZ_FARBE[p], 0.0), ec="#E6EAEC", lw=1.6, zorder=13))
        ax.add_patch(Circle((cx, cy), 19.0, fc="none", ec="#7A858C", lw=0.6, zorder=14))
        dark = p in (5,)
        ax.text(cx, cy, str(p), fontsize=15, fontweight="bold", color="white" if p in (3, 4, 5) else INK, ha="center", va="center",
                zorder=15, family=SANS)
    # Platz 0, leer: gestrichelter Kreis
    cx, cy = pl(RS, 0)
    ax.add_patch(Circle((cx, cy), 19.0, fc="none", ec="#EDE8DC", lw=1.2, ls=(0, (3, 2)), zorder=13))
    ax.text(cx - 0.0, cy + 7.5, "0", fontsize=15, fontweight="bold", color="#EDE8DC", ha="center", va="center", zorder=15)
    # Stößel: Schlitten, Wellen, Spindel, Ausleger, Stempel, Motor 1
    ax.add_patch(Rectangle((-21.15, 37.85), 42.3, 42.3, fc="#4A4A50", ec="#16161A", lw=0.8, alpha=0.95, zorder=14))
    ax.add_patch(Circle((0, 0), 34.0, fc="#17171A", ec="#000", lw=0.8, alpha=0.62, zorder=16))
    for sy in (-22.0, 22.0):
        ax.add_patch(Circle((sy, 0), 5.0, fc="#C8CAD0", ec="#55575C", lw=0.6, zorder=17))
    ax.add_patch(Circle((0, 0), 4.0, fc="#E6E8EC", ec="#55575C", lw=0.6, zorder=18))
    ax.add_patch(Rectangle((-12.5, -68.0), 25.0, 40.0, fc="#1C1C1E", ec="#55575C", lw=0.6, alpha=0.95, zorder=17))     # Ausleger, PETG
    for y0 in (-12.5, 9.5):
        ax.add_patch(Rectangle((y0, -58.0), 3.0, 22.0, fc="#34343A", ec="#55575C", lw=0.4, zorder=17.5))               # Stützrippen
    ax.add_patch(Circle(pxy(STEMPEL_X, 0), STEMPEL_D / 2, fc="#2A2A2C", ec="#000", lw=0.6, zorder=18))                  # Stempel mit Gummi
    # Zuganker
    for a in ZUGANKER_W:
        x, y = pl(ZUGANKER_R, a)
        ax.add_patch(Circle((x, y), ZUGANKER_RAD, fc="#C8CAD0", ec="#55575C", lw=0.6, zorder=9))
    for r_, a in BALLAST:
        ax.add_patch(Circle(pl(r_, a), 18.5, fc="none", ec="#8A857A", **dash))
    # Winkelstrahlen und Beschriftung der Plätze
    for p in range(0, 7):
        th = p * PITCH
        ax.plot(*zip(pl(0, th), pl(132, th)), color="#B5AEA0", lw=0.5, ls=(0, (1, 3)), zorder=2)
        x, y = pl(143 if p else 138, th)
        names = ["leer, Park", "Weiß 1", "Gelb", "Magenta", "Cyan", "Schwarz", "Weiß 2"]
        col = "#EDE8DC" if p == 0 else PLATZ_FARBE[p]
        if p == 0:
            ax.text(x, y + 0, "0  leer, Park", fontsize=10.5, fontweight="bold", color=INK, ha="center", va="center", zorder=20)
            ax.text(x, y - 11, "theta 0°", fontsize=8.8, color=INK2, ha="center", va="center", zorder=20)
        else:
            ax.add_patch(Circle((x - (0 if False else 0), y), 6.0, fc=col, ec="#555", lw=0.6, zorder=20)) if False else None
            ax.text(x, y + 5.0, "%d  %s" % (p, names[p]), fontsize=10.5, fontweight="bold", color=INK, ha="center", va="center", zorder=20)
            ax.text(x, y - 5.5, "theta %s°" % dez(th, 1), fontsize=8.8, color=INK2, ha="center", va="center", zorder=20)
    # Pfeil vorne
    ax.annotate("", xy=(0, -172), xytext=(0, -163), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=14), zorder=20)
    # Drehrichtung (positiv gegen den Uhrzeigersinn)
    arr = FancyArrowPatch(pl(170, 328), pl(170, 352), connectionstyle="arc3,rad=0.12", arrowstyle="-|>", mutation_scale=12,
                          color=GOLDD, lw=1.6, zorder=20)
    ax.add_patch(arr)
    # aktive Station
    ax.annotate("aktive Station\nüber dem Becher", xy=pxy(RS + 6, 14.0), xytext=(96, -138), fontsize=9.5, color=INK, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7), zorder=21)


# ============================================================
# 4) Maßskizze mit Größenvergleich
# ============================================================
def draw_masse(ax):
    ink, ink2 = INK, INK2
    ax.add_patch(Rectangle((-160, -20), 640, 20, fc="#E1CDA9", ec="none", zorder=0))
    ax.plot([-160, 480], [0, 0], color="#8A7350", lw=1.2, zorder=1)
    # Silhouette
    sil = [(-r_sock(3), 3), (-r_sock(97), 97), (-R_RING, 97.0), (-R_RING, 101.0), (-R_KOERPER, 101.0), (-R_KOERPER, 341.0),
           (-R_KRONE, 341.0), (-R_KRONE, Z_FASE), (-96, H_GESAMT), (96, H_GESAMT), (R_KRONE, Z_FASE), (R_KRONE, 341.0),
           (R_KOERPER, 341.0), (R_KOERPER, 101.0), (R_RING, 101.0), (R_RING, 97.0), (r_sock(97), 97), (r_sock(3), 3)]
    ax.add_patch(Polygon(sil, closed=True, fc="#17171A", ec="#000", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((-R_RING, Z_RING0), 2 * R_RING, Z_RING1 - Z_RING0, fc=GOLDC, ec="none", zorder=4))        # Goldring
    ax.add_patch(Rectangle((-R_KOERPER, Z_FUGE0), 2 * R_KOERPER, Z_FUGE1 - Z_FUGE0, fc=GOLDC, ec="none", zorder=4))   # Goldband
    ax.plot([-R_KRONE, -96], [Z_FASE, H_GESAMT], color=GOLDC, lw=1.6, zorder=5)                                        # Kronenring
    ax.plot([R_KRONE, 96], [Z_FASE, H_GESAMT], color=GOLDC, lw=1.6, zorder=5)
    ax.plot([-R_KOERPER, R_KOERPER], [Z_KTEIL, Z_KTEIL], color="#000", lw=0.8, zorder=5)                               # Schattenfuge
    # Portal und Fenster als helle Andeutung
    ax.add_patch(FancyBboxPatch((-12, 16), 24, 314, boxstyle="round,pad=0,rounding_size=6", fc="#2E2E33", ec=GOLDC, lw=0.8, zorder=5, alpha=0.9))
    # Maßlinien
    def dim_v(x, z0, z1, text, side=1, off=0.0):
        ax.annotate("", xy=(x, z1), xytext=(x, z0), arrowprops=dict(arrowstyle="<|-|>", color=ink, lw=1.0, mutation_scale=8,
                                                                    shrinkA=0, shrinkB=0), zorder=8)
        ax.text(x + side * 7, (z0 + z1) / 2, text, fontsize=11, color=ink, rotation=90, ha="center", va="center", fontweight="bold", zorder=9)

    def dim_h(z, x0, x1, text, above=True):
        ax.annotate("", xy=(x1, z), xytext=(x0, z), arrowprops=dict(arrowstyle="<|-|>", color=ink, lw=1.0, mutation_scale=8,
                                                                    shrinkA=0, shrinkB=0), zorder=8)
        ax.text((x0 + x1) / 2, z + (7 if above else -8), text, fontsize=11, color=ink, ha="center", va="center", fontweight="bold", zorder=9)

    # Höhe
    ax.plot([-R_KRONE - 4, -128], [H_GESAMT, H_GESAMT], color=ink2, lw=0.6, zorder=2)
    ax.plot([-R_FUSS_AUSSEN - 4, -128], [0, 0], color=ink2, lw=0.6, zorder=2)
    dim_v(-124, 0, H_GESAMT, "406,8", side=-1)
    # Durchmesser
    dim_h(-18, -R_FUSS_AUSSEN, R_FUSS_AUSSEN, "Ø 204 Fußkante", above=False)
    dim_h(H_GESAMT + 13, -R_KRONE, R_KRONE, "Ø 204 Krone")
    ax.plot([-R_KRONE, -R_KRONE], [H_GESAMT - 3, H_GESAMT + 17], color=ink2, lw=0.5, zorder=2)
    ax.plot([R_KRONE, R_KRONE], [H_GESAMT - 3, H_GESAMT + 17], color=ink2, lw=0.5, zorder=2)
    ax.plot([-R_FUSS_AUSSEN, -R_FUSS_AUSSEN], [-22, 4], color=ink2, lw=0.5, zorder=2)
    ax.plot([R_FUSS_AUSSEN, R_FUSS_AUSSEN], [-22, 4], color=ink2, lw=0.5, zorder=2)
    ax.annotate("Körper Ø 196", xy=(R_KOERPER, 330), xytext=(R_KOERPER + 22, 330), fontsize=10.5, color=ink, va="center", ha="left",
                fontweight="bold", arrowprops=dict(arrowstyle="-", color=ink2, lw=0.7), zorder=9)
    ax.text(R_KOERPER + 22, 315, "Sockel 98 : Körper 237 : Krone 66", fontsize=8.6, color=ink2, va="center", ha="left", zorder=9)
    ax.text(R_KOERPER + 22, 303, "Verhältnis etwa 1 : 2,4 : 0,7", fontsize=8.6, color=ink2, va="center", ha="left", zorder=9)
    # Handy (stehend, 147,6 x 71,6 x 7,8)
    px0, pw, ph = 168.0, 71.6, 147.6
    ax.add_patch(FancyBboxPatch((px0, 0), pw, ph, boxstyle="round,pad=0,rounding_size=9", fc="#2B2D33", ec="#0E0E10", lw=1.0, zorder=3))
    ax.add_patch(FancyBboxPatch((px0 + 3.2, 3.2), pw - 6.4, ph - 6.4, boxstyle="round,pad=0,rounding_size=6", fc="#EFEAE0", ec="none", zorder=4))
    ax.add_patch(Circle((px0 + pw / 2, ph - 10), 2.0, fc="#111", ec="none", zorder=5))
    for k, c in enumerate(("#0093D3", "#D4007A", "#FFD200", "#E0583F")):
        ax.add_patch(Circle((px0 + 14 + k * 14.5, ph * 0.52), 5.2, fc=c, ec="none", zorder=5))
    ax.add_patch(Rectangle((px0 + 10, ph * 0.26), pw - 20, 14, fc=ZIELFARBE, ec="none", zorder=5))
    ax.text(px0 + pw / 2, -9, "Handy\n148 × 72", fontsize=9.2, color=ink2, ha="center", va="top", zorder=9)
    # Kaffeetasse (Ø 82 x 95, Henkel)
    mx, mw, mh = 276.0, 82.0, 95.0
    ax.add_patch(Polygon([(mx - mw / 2, mh), (mx + mw / 2, mh), (mx + mw / 2 - 7, 4), (mx + mw / 2 - 12, 0), (mx - mw / 2 + 12, 0), (mx - mw / 2 + 7, 4)],
                         closed=True, fc="#F4F1EA", ec="#3B3935", lw=1.0, zorder=3))
    ax.add_patch(Ellipse((mx, mh), mw, 9, fc="#5A3A22", ec="#3B3935", lw=0.8, zorder=4))
    ax.add_patch(Arc((mx + mw / 2 - 1, mh * 0.55), 40, 52, theta1=-80, theta2=80, ec="#3B3935", lw=4.0, zorder=2))
    ax.add_patch(Arc((mx + mw / 2 - 1, mh * 0.55), 40, 52, theta1=-80, theta2=80, ec="#F4F1EA", lw=2.0, zorder=2.5))
    ax.text(mx, -9, "Kaffeetasse\nØ 82 × 95", fontsize=9.2, color=ink2, ha="center", va="top", zorder=9)
    # Portionsbecher (Ø 62 x 33, Mischbecher), daneben A4-Breite als Linie
    bx = 392.0
    ax.add_patch(Polygon([(bx - 31, 33), (bx + 31, 33), (bx + 23.5, 0), (bx - 23.5, 0)], closed=True, fc="#EEEEEE", ec="#3B3935", lw=0.9, zorder=3, alpha=0.95))
    ax.add_patch(Polygon([(bx - 27.8, 21), (bx + 27.8, 21), (bx + 23.2, 1.0), (bx - 23.2, 1.0)], closed=True, fc=ZIELFARBE, ec="none", zorder=4))
    ax.text(bx, -9, "Mischbecher\nØ 62 × 33", fontsize=9.2, color=ink2, ha="center", va="top", zorder=9)
    # Maßstab 100 mm
    ax.plot([168, 268], [262, 262], color=ink, lw=2.0, zorder=9, solid_capstyle="butt")
    for x in (168, 218, 268):
        ax.plot([x, x], [258, 266], color=ink, lw=1.2, zorder=9)
    ax.text(218, 274, "100 mm", fontsize=9.6, color=ink, ha="center", va="center", fontweight="bold")
    ax.text(168, 236, "Grundfläche Ø 204: schmaler als ein\nA4-Blatt (210 mm), passt auf jeden\nSchreibtisch. 3,8 kg mit Ballast.", fontsize=9.3,
            color=INK2, ha="left", va="top", linespacing=1.35)


# ============================================================
# Zusammenbau der Tafel
# ============================================================
FW, FH = 2800, 1700


def tafel(ss=1.5, verbose=True):
    t0 = time.time()
    fig = plt.figure(figsize=(FW / 100, FH / 100), dpi=100, facecolor=PAPER)
    bg = fig.add_axes([0, 0, 1, 1])
    bg.set_xlim(0, FW)
    bg.set_ylim(FH, 0)
    bg.set_axis_off()

    # ---- Kopfzeile
    bg.text(48, 62, "Farbmischer", fontsize=46, family=SERIF, color=INK, ha="left", va="center")
    bg.text(48, 118, "Stand 6 · schwarzer Flakon mit Goldlinien · Ø 204 × 407 mm · sechs Spritzen, zwei Motoren, alles aus PETG gedruckt",
            fontsize=13.5, color=INK2, ha="left", va="center")
    bg.plot([48, FW - 48], [148, 148], color=GOLDC, lw=1.4)
    stats = [("406,8 mm", "Höhe"), ("Ø 204 mm", "Fuß und Krone"), ("3,8 kg", "mit Ballast"), ("6 × 50 ml", "Farbvorrat"), ("2", "Motoren")]
    x = FW - 48
    for big, small in stats[::-1]:
        bg.text(x, 56, big, fontsize=19, color=INK, ha="right", va="center", fontweight="bold")
        bg.text(x, 90, small, fontsize=10.5, color=INK2, ha="right", va="center")
        x -= 190

    # ---- Karten
    top = None
    y0, hh = 170, 1480
    card(fig, 960, y0, 1040, hh, FW, FH)
    card(fig, 2020, y0, 740, 790, FW, FH)
    card(fig, 2020, 980, 740, 670, FW, FH)

    # ---- 1) Hero
    top = fig.add_axes([0, 0, 1, 1], facecolor='none', zorder=50)
    top.set_xlim(0, FW); top.set_ylim(FH, 0); top.set_axis_off()
    hero = Hero(900, hh, ss=ss)
    raw = hero.render(verbose=verbose)
    img = downsample(tonemap(raw), 900, hh)
    axh = fig.add_axes([40 / FW, 1 - (y0 + hh) / FH, 900 / FW, hh / FH])
    axh.imshow(img, aspect="auto", interpolation="lanczos")
    axh.set_axis_off()
    top.add_patch(Rectangle((40, y0), 900, hh, fc="none", ec="#CFC7B6", lw=1.0, zorder=5))
    top.add_patch(Rectangle((40, y0), 900, 62, fc=(0, 0, 0, 0.45), ec="none", zorder=6))
    top.text(64, y0 + 31, "1", fontsize=18, color=GOLDC, ha="left", va="center", fontweight="bold", zorder=7, family=SERIF)
    top.text(92, y0 + 31, "Das Gerät in Ruhe auf dem Schreibtisch", fontsize=13.5, color="white", ha="left", va="center",
            zorder=7)
    top.add_patch(Rectangle((40, y0 + hh - 66), 900, 66, fc=(0, 0, 0, 0.45), ec="none", zorder=6))
    top.text(64, y0 + hh - 44, "Sockel und Front glänzend, Körper und Krone matt, Goldteile gedruckt aus Gold-PETG,", fontsize=12, color="white",
            ha="left", va="center", zorder=7)
    top.text(64, y0 + hh - 20, "Rauch-PETG-Portal, sechs Klarfenster, auf der Bühne der Becher in der Zielfarbe.",
            fontsize=12, color="#E8E2D2", ha="left", va="center", zorder=7)

    # ---- 2) Schnitt
    top.text(986, y0 + 34, "2", fontsize=18, color=GOLDD, ha="left", va="center", fontweight="bold", family=SERIF)
    top.text(1014, y0 + 34, "Schnitt durch die Mitte (Ebene Y = 0), Dosierstellung: Cyan wird gedrückt", fontsize=13.5, color=INK, ha="left", va="center")
    sc = 2.5
    axs_rect = (960, y0 + 64, 1040, int(487 * sc))
    pane = Pane(fig, *axs_rect, FW, FH)
    axs = pane.axes(xlim=(-226, 226), ylim=(-62, 425))
    L = draw_schnitt(axs)
    draw_schnitt_beschriftung(axs, L, zmin=-54.0, zmax=418.0, xl=-112.0, xr=112.0, fs=10.6, gap=18.0)
    # Hinweis vorne und Legende der Werkstoffe
    ly = y0 + 64 + int(487 * sc) + 14
    top.text(986, ly + 8, "Werkstoffe und Farben (CMF)", fontsize=11.5, color=INK, ha="left", va="center", fontweight="bold")
    chips = [("Hochglanz schwarz (PETG)", FARBEN["sockel"]), ("Seidenmatt schwarz (PETG)", FARBEN["koerper"]), ("Gold-PETG", FARBEN["gold"]),
             ("Rauch-PETG 2 mm", FARBEN["rauch"]), ("Klar-PETG", FARBEN["klar"]), ("PETG weiß", FARBEN["schublade"]),
             ("Innenteile PETG", FARBEN["innen"]), ("Stahl verzinkt", FARBEN["stahl"]), ("Messing", FARBEN["messing"]),
             ("Silikon/Gummi", FARBEN["silikon"])]
    for i, (nm, col) in enumerate(chips):
        cx = 986 + (0, 240, 482, 628, 812)[i % 5]
        cy = ly + 42 + (i // 5) * 36
        top.add_patch(Rectangle((cx, cy - 11), 22, 22, fc=col, ec="#8A857A", lw=0.8, zorder=5))
        top.text(cx + 30, cy, nm, fontsize=10, color=INK, ha="left", va="center")
    top.text(986, ly + 118, "Schnittflächen dunkel, Teile hinter der Ebene hell und durchscheinend. Maße in Millimetern. Z = 0 ist die Tischfläche.",
            fontsize=9.6, color=INK2, ha="left", va="center")

    # ---- 3) Draufsicht
    top.text(2046, y0 + 34, "3", fontsize=18, color=GOLDD, ha="left", va="center", fontweight="bold", family=SERIF)
    top.text(2074, y0 + 34, "Draufsicht ohne Krone und Brücke, Ruhestellung", fontsize=13.5, color=INK, ha="left", va="center")
    pane = Pane(fig, 2020, y0 + 56, 740, 640, FW, FH)
    axd = pane.axes(xlim=(-185, 185), ylim=(-174, 146))
    draw_draufsicht(axd)
    ly = y0 + 56 + 640 + 6
    items = [("gestrichelt", "verdeckt: Schublade, Becher, Motor 2, Ballast, Laufringlücke ± 15°", "#8A857A"),
             ("blau", "Feuchtrinne, vorne offen ± 38°", "#5C8DB3"), ("gold", "Abstreiflippen ± 40°, Goldring und Portalrahmen", "#B8860B"), ("pfeil", "Pfeil unten links: Drehrichtung + (gegen den Uhrzeigersinn)", GOLDD)]
    for i, (a, b, c) in enumerate(items):
        top.plot([2046, 2072], [ly + 10 + i * 19] * 2, color=c, lw=2.0 if i else 1.2, ls=(0, (4, 3)) if i == 0 else "-")
        top.text(2084, ly + 10 + i * 19, b, fontsize=10, color=INK, ha="left", va="center")

    # ---- 4) Maße
    top.text(2046, 980 + 34, "4", fontsize=18, color=GOLDD, ha="left", va="center", fontweight="bold", family=SERIF)
    top.text(2074, 980 + 34, "Maße und Größenvergleich", fontsize=13.5, color=INK, ha="left", va="center")
    pane = Pane(fig, 2020, 980 + 52, 740, 610, FW, FH)
    axm = pane.axes(xlim=(-165, 445), ylim=(-44, 470))
    draw_masse(axm)

    # ---- Fuß
    top.text(48, FH - 26, "Nach hardware/farbmischer_parameter.md, Stand 6. Rendering mit eigenem Strahlverfolger, Schnitt, Draufsicht und Maße als Zeichnung "
            "aus denselben Parametern. Koordinaten: +X vorne, +Y rechts, Z = 0 Tischfläche.", fontsize=10, color=INK3, ha="left", va="center")
    fig.savefig(OUT_PNG, dpi=100, facecolor=PAPER)
    plt.close(fig)
    if verbose:
        print("gespeichert: %s  (%.0f s)" % (OUT_PNG, time.time() - t0))


def main():
    if "--pruefung" in sys.argv:
        rows, extra, ketten = pruefung()
        bad = [r for r in rows if r[3] < r[2] - 1e-9]
        sys.exit(1 if bad else 0)
    tafel()


if __name__ == "__main__":
    main()
