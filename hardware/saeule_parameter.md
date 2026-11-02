# Säule: Parameterblatt für Rendering und Druckteile

Rundes Design nach Vorbild YSL Rouge Sur Mesure: eine schlanke Säule, Kartuschen (Spritzen) werden von oben eingesetzt, der Mischbecher sitzt unten in der Mitte und wird durch ein Fenster an der Vorderseite entnommen.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Stationen auf einem Kreis, Winkel 0° zeigt nach vorne (zum Fenster), Stationen bei 36°, 108°, 180°, 252°, 324°, damit vorne keine Station, sondern das Fenster liegt.

## Gesamt

| Größe | Wert |
|---|---|
| Außendurchmesser Säule | 170 |
| Gesamthöhe ohne Deckel | 350 |
| Deckel (Haube) Höhe | 25, Durchmesser 170, sitzt oben auf |
| Schalenwandstärke Gehäuse | 2,4 |
| Stationen | 5 |
| Radius Stationsring (Spritzenachse am Halter, oben) | 60 |
| Neigung jeder Station nach innen | 10°, Achse kippt von außen oben nach innen unten |
| Radius Düsenspitze (unten) | etwa 22, ergibt sich aus Neigung und Länge |

## Sockel (Z 0 bis 95)

| Größe | Wert |
|---|---|
| Sockelhöhe | 95 |
| Becherraum | Zylinder Ø 80, Höhe 75, zentriert, Boden bei Z = 5 |
| Fenster vorne (0°) | Breite 85, Höhe 75, Unterkante Z = 5, mit Rundung oben |
| Mischbecher (Kaufteil) | Ø 70, Höhe 60 (kleines Glas oder Becher) |
| Düsen enden bei | Z = 90, also 25 mm über dem Becherrand bei Z 65 |
| Motoren NEMA 17 | Flansch 42,3, Länge 40, Achse auf dem Stationsring bei Radius 60, Achse geneigt wie die Station, Motor hängt unter der Motorplatte |
| Motorplatte | Ring, Innendurchmesser 84 (Becherraum plus Wand), Außendurchmesser 165, Dicke 8, Oberkante Z = 95 |
| Motor-Unterkante | etwa Z = 45, Motoren liegen außerhalb des Becherraums (Innenkante Motor bei Radius 39, Becherraum Radius 40 mit Wand 2 ergibt knapp, bei Kollision Stationsring auf 62 setzen) |
| Elektronik | Die Trägerplatine (100 x 100) passt nicht zwischen die Motoren. Sie liegt im Standfuß unter der Säule (Fuß Ø 190, Höhe 25, Fach 110 x 110 x 20). Der Sockel beginnt deshalb bei Z = 25, alle Z-Werte dieses Abschnitts um 25 anheben. |

## Station (je 5, identisch, um 72° gedreht)

Lokales Koordinatensystem der Station: Ursprung auf dem Stationsring bei Radius 60 und Z = 95 (Motorplattenoberkante, vor dem Anheben um den Fuß). Lokale Z-Achse um 10° nach innen geneigt. Innerhalb der Station liegen Spritze, Spindel und Welle nebeneinander auf einer Tangente (quer zur Radialrichtung), damit der Außendurchmesser klein bleibt:

| Element | Lage tangential (lokal X) | Werte |
|---|---|---|
| Spritze 60 ml Luer-Lock | X = 0 | Zylinder Ø 30, Länge 125 ohne Kolben, Flansch 45 x 32 x 3, Kolbenplatte Ø 30 x 4, Kolbenstange 12, Hub 90, Düse Luer 15 lang |
| Spindel T8, 2 mm Steigung | X = +24 | Ø 8, Flanschmutter Ø 22 am Schlitten, Kupplung 5 auf 8, Ø 19, Länge 25, unten am Motor |
| Linearwelle 8 mm | X = -22 | Ø 8, zwei LM8UU (Ø 15, Länge 24) übereinander im Schlitten |
| Spritzenhalter | am Flansch | Von oben einsetzbar: Flansch fällt in eine Tasche, nach unten durch den Zylinder-Durchlass Ø 31 gestützt, Rastfeder hält gegen Hochrutschen. Halter sitzt bei lokal Z = 125 bis 140 (Flansch oben am Zylinder, Zylinder reicht von Z 0 bis 125, Düse von Z -15 bis 0) |
| Kolbenschlitten | greift Kolbenplatte | Arm mit Magnet Ø 10 x 3 (Neodym) in der Unterseite, auf der Kolbenplatte klebt eine Stahlscheibe M10. Kein U-Griff, deshalb von oben frei entnehmbar. Schlitten fährt von lokal Z 140 (Kolben ganz gedrückt, plus Totweg) bis Z 235 (Kolben ganz gezogen) |
| Endschalter | oben am Kopfring | Schlitten oben = Referenz |
| Kopfring | lokal Z = 245 bis 255 | Ring Innendurchmesser 90, Außendurchmesser 165, hält Wellen- und Spindelenden (608-Lager für Spindel), Endschalter |
| Motor | lokal Z = -8 bis -48 unter der Motorplatte | Welle zeigt nach oben, Kupplung Z 0 bis 25 |

Wellenlänge rechnerisch etwa 255, Spindel etwa 230 (Kaufmaß 250 bzw. 250).

## Gehäuse

| Teil | Wert |
|---|---|
| Standfuß | Ø 190, Höhe 25, Elektronikfach innen 110 x 110 x 20, Kabeldurchlass nach oben, Buchse 12 V hinten |
| Sockelschale | Zylinder Ø 170, Z 25 bis 120 (95 hoch), Fenster vorne, Lüftungsschlitze hinten |
| Mittelschale | Zylinder Ø 170, Z 120 bis 300, in zwei Hälften (vorne, hinten) gedruckt, je 180 hoch |
| Oberschale | Zylinder Ø 170, Z 300 bis 375, trägt den Kopfring |
| Haube | Z 375 bis 400, abnehmbar, Steckverbindung, darunter LED-Ring (WS2812, 12 LEDs, Ø 50) zeigt die Zielfarbe |
| Farbgebung Rendering | Schalen cremeweiß, Haube und Fuß dunkelgrau, Akzentring am Fenster messing |

Mit Fuß: Gesamthöhe 400 mm, Durchmesser 170 mm (Fuß 190 mm).

## Handhabung

1. Haube abnehmen, Schlitten der Station per App nach oben fahren.
2. Spritze senkrecht herausziehen (Magnet löst sich), neue gefüllte Spritze einsetzen, bis der Flansch einrastet.
3. Schlitten per App herunterfahren, Magnet koppelt auf der Stahlscheibe.
4. Becher durchs Fenster einstellen, Farbe wählen, dosieren, Becher entnehmen, umrühren.
