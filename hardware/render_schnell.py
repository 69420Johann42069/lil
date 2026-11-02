#!/usr/bin/env python3
"""Grobes Schnell-Rendering der Säule (Stand 5), nur Zylinder, keine Details."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(9, 7), dpi=110)
ax = fig.add_subplot(111, projection="3d")
ax.view_init(elev=15, azim=18)

def zyl(r, z0, z1, farbe, n=48, alpha=1.0, von=0, bis=360):
    t = np.radians(np.linspace(von, bis, n))
    T, Z = np.meshgrid(t, [z0, z1])
    ax.plot_surface(r * np.cos(T), r * np.sin(T), Z, color=farbe, alpha=alpha, linewidth=0, shade=True)
    for z in (z0, z1):
        tt = np.radians(np.linspace(von, bis, n))
        ax.plot_trisurf(np.r_[0, r * np.cos(tt)], np.r_[0, r * np.sin(tt)], np.full(n + 1, z), color=farbe, alpha=alpha, linewidth=0)

creme, dunkel, messing = "#e9e2d2", "#3a3a3c", "#b08d57"
zyl(109, 0, 25, dunkel)                 # Fuß
zyl(104, 25, 120, creme)                # Sockel
zyl(104, 120, 300, creme, von=60, bis=372)   # Drehhülse mit Öffnung bei 36 Grad
zyl(104, 300, 420, creme)               # Oberschale
zyl(104, 420, 470, dunkel)              # Haube
# Fenster vorne (0 Grad): dunkle Fläche plus Messingrahmen
for r, f, w in ((104.6, "#2b2b2b", 24), (105.0, messing, 27)):
    zyl(r, 28, 100, f, von=-w, bis=w)
zyl(37, 30, 90, "#cfd8dc", alpha=0.8)   # Becher
# Spritze in der Hülsenöffnung
a = np.radians(36)
for r, z0, z1, f in ((15, 120, 245, "#1aa0d8"), (6, 245, 330, "#999"), (15, 330, 334, "#555")):
    t = np.linspace(0, 2 * np.pi, 24)
    T, Z = np.meshgrid(t, [z0, z1])
    ax.plot_surface(42 * np.cos(a) + r * np.cos(T), 42 * np.sin(a) + r * np.sin(T), Z, color=f, linewidth=0)

ax.set_box_aspect((1, 1, 2.2))
ax.set_xlim(-110, 110); ax.set_ylim(-110, 110); ax.set_zlim(0, 480)
ax.set_axis_off()
ax.set_title("Farbmischer Säule, Stand 5, grob: Ø 208 mm, Höhe 470 mm\nvorne Fenster mit Becher, seitlich Drehhülse mit Öffnung und Spritze", fontsize=10)
fig.tight_layout()
fig.savefig("/home/user/lil/hardware/rendering_schnell.png", facecolor="white")
print("ok")
