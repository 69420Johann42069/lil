#!/usr/bin/env python3
"""Erzeugt die Trägerplatine des Farbmischers als KiCad-8-Leiterplatte.

Nur Python-Standardbibliothek. Ausgabe: farbmixer_traeger.kicad_pcb mit
allen Footprints und Netzen, aber ohne Leiterbahnen. Die Bahnen werden in
KiCad gezogen (Route > Freerouting oder von Hand), danach Gerber für JLCPCB
exportieren. Zusätzlich NETZLISTE.md zum Gegenprüfen.

Bestückung (alles Durchsteck, Steckmodule):
  U1   ESP32 DevKit V1, 30-polig, zwei Buchsenleisten 1x15
  U2..U6  StepStick-Treiber TMC2209 oder A4988, je zwei Buchsenleisten 1x8
  J1   Schraubklemme 2-polig 5,08 mm, 12 V Eingang
  J2   Schraubklemme 4-polig 5,08 mm, Buck-Modul 12 V -> 5 V (IN+, IN-, OUT+, OUT-)
  J3..J7  JST-XH 4-polig, Motoren
  J8..J12 JST-XH 2-polig, Endschalter
  F1   Polyfuse 3 A, radial 5,08 mm
  C1   470 µF 25 V radial 5 mm
  C2..C6  100 µF 25 V radial 2,5 mm, je Treiber an VMOT
  R1   10 kOhm Pullup für Endschalter an GPIO 34
  JP1..JP5  Lötjumper MS1 (bei TMC2209 und A4988 schließen: 1/16 Schritt)
  JP6..JP10 Lötjumper MS2 (schließen)
  JP11..JP15 Lötjumper MS3 bzw. Pin 4 (nur A4988 schließen, TMC2209 offen)
  JP16..JP20 Lötjumper RST-SLP (nur A4988 schließen, TMC2209 offen)
"""
import uuid
from pathlib import Path

OUT = Path(__file__).parent
BOARD_W, BOARD_H = 100.0, 100.0

# Pins pro Station, identisch mit firmware/include/config.h
STEP_GPIO = [13, 14, 27, 26, 25]
DIR_GPIO = [33, 32, 4, 16, 17]
ENDSTOP_GPIO = [18, 19, 21, 22, 34]
ENABLE_GPIO = 23

# ESP32 DevKit V1, 30-polig, Blick von oben, USB unten.
# Linke Reihe von oben nach unten, rechte Reihe von oben nach unten.
# Reihenabstand 25,4 mm. Vor dem Bestellen am eigenen Board nachmessen.
DEVKIT_LEFT = ["3V3", "EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26",
               "D27", "D14", "D12", "GND", "D13"]
DEVKIT_RIGHT = ["VIN", "GND", "D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5",
                "D17", "D16", "D4", "D0", "D2"]
DEVKIT_ROW_PITCH = 25.4

# StepStick, Blick von oben, Reihen 15,24 mm auseinander, 8 Pins je Reihe.
STEPSTICK_LOGIC = ["EN", "MS1", "MS2", "MS3", "RST", "SLP", "STEP", "DIR"]
STEPSTICK_POWER = ["VMOT", "GND", "2B", "2A", "1A", "1B", "VDD", "GND"]
STEPSTICK_ROW_PITCH = 15.24


def gpio_net(n):
    return f"GPIO{n}"


def devkit_pin_net(label):
    table = {"3V3": "+3V3", "GND": "GND", "VIN": "+5V"}
    if label in table:
        return table[label]
    if label.startswith("D"):
        return gpio_net(int(label[1:]))
    return "NC_" + label


# ----------------------------------------------------------------- Netze

nets = {}


def net(name):
    if name not in nets:
        nets[name] = len(nets) + 1
    return nets[name]


net("GND"); net("+12V_IN"); net("+12V"); net("+5V"); net("+3V3"); net(gpio_net(ENABLE_GPIO))
for i in range(5):
    net(gpio_net(STEP_GPIO[i])); net(gpio_net(DIR_GPIO[i])); net(gpio_net(ENDSTOP_GPIO[i]))
    for p in ("1A", "1B", "2A", "2B"):
        net(f"M{i+1}_{p}")
    net(f"MS3_{i+1}"); net(f"RST_{i+1}"); net(f"SLP_{i+1}")

# ----------------------------------------------------------------- Footprints

footprints = []
netlist_rows = []


def pad(num, x, y, netname, size=1.7, drill=1.0, shape="circle", smd=False):
    n = net(netname) if netname else 0
    nstr = f' (net {n} "{netname}")' if netname else ""
    if smd:
        return (f'    (pad "{num}" smd rect (at {x:.3f} {y:.3f}) (size {size} {size}) '
                f'(layers "F.Cu" "F.Mask"){nstr})')
    return (f'    (pad "{num}" thru_hole {shape} (at {x:.3f} {y:.3f}) (size {size} {size}) '
            f'(drill {drill}) (layers "*.Cu" "*.Mask"){nstr})')


def footprint(ref, value, lib, x, y, pads, rot=0, outline=None):
    uid = uuid.uuid4()
    lines = [f'  (footprint "{lib}" (layer "F.Cu") (uuid "{uid}") (at {x:.3f} {y:.3f} {rot})',
             f'    (property "Reference" "{ref}" (at 0 -3 {rot}) (layer "F.SilkS") '
             f'(uuid "{uuid.uuid4()}") (effects (font (size 1 1) (thickness 0.15))))',
             f'    (property "Value" "{value}" (at 0 3 {rot}) (layer "F.Fab") '
             f'(uuid "{uuid.uuid4()}") (effects (font (size 1 1) (thickness 0.15))))',
             f'    (property "Footprint" "{lib}" (at 0 0) (layer "F.Fab") (hide yes) '
             f'(uuid "{uuid.uuid4()}") (effects (font (size 1 1) (thickness 0.15))))']
    if outline:
        w, h = outline
        lines.append(f'    (fp_rect (start {-w/2:.3f} {-h/2:.3f}) (end {w/2:.3f} {h/2:.3f}) '
                     f'(stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS") (uuid "{uuid.uuid4()}"))')
    lines += pads
    lines.append("  )")
    footprints.append("\n".join(lines))


def header_row(ref, names, nets_, x0, y0, pitch=2.54, start=1, vertical=True):
    pads = []
    for i, (nm, nn) in enumerate(zip(names, nets_)):
        px, py = (0, i * pitch) if vertical else (i * pitch, 0)
        pads.append(pad(start + i, px, py, nn, shape="rect" if i == 0 and start == 1 else "circle"))
        netlist_rows.append((ref, start + i, nm, nn or "NC"))
    return pads


# ESP32 DevKit (U1): zwei Buchsenleisten, Pins 1..15 links, 16..30 rechts
ux, uy = 12.0, 18.0
left = header_row("U1", DEVKIT_LEFT, [devkit_pin_net(l) for l in DEVKIT_LEFT], 0, 0)
right = header_row("U1", DEVKIT_RIGHT, [devkit_pin_net(l) for l in DEVKIT_RIGHT], 0, 0, start=16)
right = [p.replace("(at 0.000", f"(at {DEVKIT_ROW_PITCH:.3f}") for p in right]
footprint("U1", "ESP32 DevKit V1 30p", "Farbmixer:ESP32_DevKit_30", ux, uy, left + right,
          outline=(DEVKIT_ROW_PITCH + 3.0, 15 * 2.54 + 2))

# StepSticks U2..U6 mit Kondensator, Motorstecker und Jumpern
positions = [(55, 12), (76, 12), (55, 42), (76, 42), (55, 72)]
for i, (sx, sy) in enumerate(positions):
    ref = f"U{i+2}"
    logic_nets = [gpio_net(ENABLE_GPIO), "+3V3", "+3V3", f"MS3_{i+1}", f"RST_{i+1}", f"SLP_{i+1}",
                  gpio_net(STEP_GPIO[i]), gpio_net(DIR_GPIO[i])]
    # MS1/MS2 laufen über Lötjumper nach +3V3: Pin selbst bekommt eigenes Netz
    logic_nets[1] = f"MS1_{i+1}"; logic_nets[2] = f"MS2_{i+1}"
    power_nets = ["+12V", "GND", f"M{i+1}_2B", f"M{i+1}_2A", f"M{i+1}_1A", f"M{i+1}_1B", "+3V3", "GND"]
    a = header_row(ref, STEPSTICK_LOGIC, logic_nets, 0, 0)
    b = header_row(ref, STEPSTICK_POWER, power_nets, 0, 0, start=9)
    b = [p.replace("(at 0.000", f"(at {STEPSTICK_ROW_PITCH:.3f}") for p in b]
    footprint(ref, f"StepStick {i+1}", "Farbmixer:StepStick", sx, sy, a + b,
              outline=(STEPSTICK_ROW_PITCH + 3.0, 8 * 2.54 + 2))
    # Elko 100 µF an VMOT/GND, Raster 2,5 mm
    cref = f"C{i+2}"
    footprint(cref, "100u 25V", "Farbmixer:C_Radial_2.5", sx + 7.6, sy - 5.0,
              [pad(1, -1.25, 0, "+12V", shape="rect"), pad(2, 1.25, 0, "GND")], outline=(6.5, 6.5))
    netlist_rows += [(cref, 1, "+", "+12V"), (cref, 2, "-", "GND")]
    # Motorstecker JST-XH 4 am rechten Rand neben dem Treiber
    jref = f"J{i+3}"
    mx = sx + STEPSTICK_ROW_PITCH + 6.0
    pads = header_row(jref, ["1A", "1B", "2A", "2B"],
                      [f"M{i+1}_1A", f"M{i+1}_1B", f"M{i+1}_2A", f"M{i+1}_2B"], 0, 0, pitch=2.5)
    footprint(jref, f"Motor {i+1} XH-4", "Farbmixer:JST_XH_4", mx, sy + 2.0, pads, outline=(5.8, 12.0))
    # Lötjumper: MS1, MS2 -> +3V3 ; MS3 -> +3V3 ; RST-SLP
    jx = sx - 5.5
    for k, (jref2, na, nb) in enumerate([
            (f"JP{i+1}", f"MS1_{i+1}", "+3V3"), (f"JP{i+6}", f"MS2_{i+1}", "+3V3"),
            (f"JP{i+11}", f"MS3_{i+1}", "+3V3"), (f"JP{i+16}", f"RST_{i+1}", f"SLP_{i+1}")]):
        jy = sy + 2.54 + k * 4.0
        footprint(jref2, "SJ", "Farbmixer:SolderJumper", jx, jy,
                  [pad(1, -0.9, 0, na, size=1.2, smd=True), pad(2, 0.9, 0, nb, size=1.2, smd=True)])
        netlist_rows += [(jref2, 1, "A", na), (jref2, 2, "B", nb)]

# Endschalter J8..J12 (JST-XH 2) am unteren Rand
for i in range(5):
    jref = f"J{i+8}"
    pads = header_row(jref, ["SIG", "GND"], [gpio_net(ENDSTOP_GPIO[i]), "GND"], 0, 0, pitch=2.5, vertical=False)
    footprint(jref, f"Endstop {i+1} XH-2", "Farbmixer:JST_XH_2", 10 + i * 9.0, 93.0, pads, outline=(7.5, 5.8))

# LED-Ring WS2812 (J13): 5 V, GND, Daten GPIO 5
pads = header_row("J13", ["5V", "GND", "DATA"], ["+5V", "GND", gpio_net(5)], 0, 0, pitch=2.5, vertical=False)
footprint("J13", "LED-Ring XH-3", "Farbmixer:JST_XH_3", 62.0, 93.0, pads, outline=(10.0, 5.8))

# Pullup für GPIO 34 (kein interner Pullup)
footprint("R1", "10k", "Farbmixer:R_Axial_7.62", 36.0, 80.0,
          [pad(1, -3.81, 0, gpio_net(34), shape="rect"), pad(2, 3.81, 0, "+3V3")], outline=(9.0, 2.5))
netlist_rows += [("R1", 1, "", gpio_net(34)), ("R1", 2, "", "+3V3")]

# Stromversorgung: Klemme 12 V, Polyfuse, Elko, Buck-Klemme
footprint("J1", "12V IN 5.08", "Farbmixer:Terminal_2_5.08", 8.0, 68.0,
          [pad(1, 0, 0, "+12V_IN", size=2.6, drill=1.3, shape="rect"), pad(2, 5.08, 0, "GND", size=2.6, drill=1.3)],
          outline=(10.2, 8.0))
netlist_rows += [("J1", 1, "+12V", "+12V_IN"), ("J1", 2, "GND", "GND")]
footprint("F1", "Polyfuse 3A", "Farbmixer:Fuse_Radial_5.08", 8.0, 78.0,
          [pad(1, -2.54, 0, "+12V_IN", shape="rect"), pad(2, 2.54, 0, "+12V")], outline=(8.0, 4.0))
netlist_rows += [("F1", 1, "", "+12V_IN"), ("F1", 2, "", "+12V")]
footprint("C1", "470u 25V", "Farbmixer:C_Radial_5.0", 20.0, 78.0,
          [pad(1, -2.5, 0, "+12V", shape="rect"), pad(2, 2.5, 0, "GND")], outline=(10.5, 10.5))
netlist_rows += [("C1", 1, "+", "+12V"), ("C1", 2, "-", "GND")]
bk = header_row("J2", ["IN+", "IN-", "OUT+", "OUT-"], ["+12V", "GND", "+5V", "GND"], 0, 0, pitch=5.08, vertical=False)
bk = [p.replace("(size 1.7 1.7) (drill 1.0)", "(size 2.6 2.6) (drill 1.3)") for p in bk]
footprint("J2", "Buck 12V->5V 5.08", "Farbmixer:Terminal_4_5.08", 10.0, 58.0, bk, outline=(20.4, 8.0))

# Montagelöcher M3
for k, (mx, my) in enumerate([(3.5, 3.5), (BOARD_W - 3.5, 3.5), (3.5, BOARD_H - 3.5), (BOARD_W - 3.5, BOARD_H - 3.5)]):
    footprint(f"H{k+1}", "M3", "Farbmixer:MountingHole_3.2", mx, my,
              [pad(1, 0, 0, None, size=6.0, drill=3.2)])

# ----------------------------------------------------------------- Datei

layers = """  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (44 "Edge.Cuts" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )"""

net_lines = ['  (net 0 "")'] + [f'  (net {n} "{name}")' for name, n in sorted(nets.items(), key=lambda kv: kv[1])]
edge = (f'  (gr_rect (start 0 0) (end {BOARD_W} {BOARD_H}) (stroke (width 0.1) (type default)) '
        f'(fill none) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))')
title = (f'  (gr_text "Farbmixer Traegerplatine" (at 50 97 0) (layer "F.SilkS") (uuid "{uuid.uuid4()}") '
         f'(effects (font (size 1.5 1.5) (thickness 0.2))))')

doc = "\n".join([
    '(kicad_pcb (version 20240108) (generator "farbmixer_generate_pcb") (generator_version "8.0")',
    '  (general (thickness 1.6) (legacy_teardrops no))',
    '  (paper "A4")',
    layers,
    '  (setup (pad_to_mask_clearance 0) (allow_soldermask_bridges_in_footprints no)',
    '    (pcbplotparams (layerselection 0x00010fc_ffffffff) (plot_on_all_layers_selection 0x0000000_00000000)))',
    *net_lines,
    *footprints,
    edge,
    title,
    ')',
])
(OUT / "farbmixer_traeger.kicad_pcb").write_text(doc, encoding="utf-8")

# Netzliste als Tabelle
md = ["# Netzliste Trägerplatine", "", "Erzeugt von generate_pcb.py. Pinnummern wie auf der Platine.", "",
      "| Bauteil | Pin | Name | Netz |", "|---|---|---|---|"]
for ref, num, name, nn in netlist_rows:
    md.append(f"| {ref} | {num} | {name} | {nn} |")
(OUT / "NETZLISTE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print(f"{len(footprints)} Footprints, {len(nets)} Netze, {len(netlist_rows)} Pins")
print("Klammerbalance:", doc.count("("), doc.count(")"))
