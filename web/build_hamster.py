#!/usr/bin/env python3
"""Erzeugt hamster.js aus hamster.png.

Das Sprite steckt als data-URI in einer Skriptdatei, weil die Seite die Pixel
per Canvas einfärbt. Bilder von file:// markieren den Canvas als "tainted",
dann bliebe der Hamster beim Doppelklick auf index.html weiß. Skripte laden
auch von file://, eine data-URI ist immer same-origin.

Aufruf:  python3 build_hamster.py
"""
import base64, os
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'hamster.png'), 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')
with open(os.path.join(here, 'hamster.js'), 'w', encoding='ascii') as f:
    f.write("// Automatisch erzeugt von build_hamster.py aus hamster.png, nicht von Hand aendern.\n")
    f.write("window.HAMSTER_SPRITE = 'data:image/png;base64," + b64 + "';\n")
print('hamster.js', os.path.getsize(os.path.join(here, 'hamster.js')), 'Bytes')
