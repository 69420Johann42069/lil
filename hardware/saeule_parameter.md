# Säule: Parameterblatt für Rendering und Druckteile

Rundes Design nach Vorbild YSL Rouge Sur Mesure: eine schlanke Säule, Kartuschen (Spritzen) werden von oben eingesetzt, der Mischbecher sitzt unten in der Mitte und wird durch ein Fenster an der Vorderseite entnommen. Die Motoren sitzen oben unter der Haube, damit unten Platz für die zusammenlaufenden Düsen und den Becher bleibt.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (zum Fenster). Stationen bei 36°, 108°, 180°, 252°, 324°, vorne liegt keine Station, sondern das Fenster.

## Stationsachse

Jede Station ist um `neigung` = 6° gekippt: unten (Düse) innen, oben (Motor) außen. Der Weg entlang der Achse heißt s, s = 0 an der Düsenspitze, s wächst nach oben. Radius der Achse: r(s) = 22 + s * sin(6°). Weltkoordinaten: z(s) = 105 + s * cos(6°), Radialabstand r(s), Stationswinkel wie oben. Alle Teile einer Station liegen in diesem lokalen System (lokal Z = s, lokal X tangential, lokal Y radial nach außen).

| Element | s (lokal Z) | Lage quer | Werte |
|---|---|---|---|
| Düse Luer | 0 bis 15 | Achse | Ø 4 außen |
| Spritzenzylinder 60 ml | 15 bis 140 | Achse | Ø 30, Flansch 45 x 32 x 3 bei s = 137 bis 140 |
| Kolbenplatte | 145 (ganz gedrückt) bis 235 (ganz gezogen) | Achse | Ø 30 x 4, Stahlscheibe M10 (Ø 20 x 2) oben aufgeklebt, Kolbenstange 12 x 12 Kreuzprofil |
| Spritzenhalter | 118 bis 142 | Achse, klemmt an Welle und Spindel | von oben einsetzbar: Flanschtasche 45,6 x 32,6 x 3,6 nach oben offen, Zylinderdurchlass Ø 31, Rastlasche 1,2 dick hält den Flansch gegen Hochrutschen, Halterblock tangential höchstens 44 breit |
| Kolbenschlitten | Unterkante bei s = 149 (gedrückt) bis 239 (gezogen), Höhe 30 | Welle und Spindel | ein LM8UU (Ø 15, Länge 24) auf der Welle, Flanschmutter T8 (Ø 22, 4 x M3 auf Lochkreis 16) für die Spindel, Arm nach innen zur Achse mit Magnet Ø 10 x 3 in der Unterseite über der Kolbenplatte, Armdicke 8, Schlitten tangential höchstens 44 breit |
| Linearwelle 8 mm | 149 bis 289 | lokal X = -12, lokal Y = +10 | Länge 140, oben in der Motorplatte in einem Sackloch 7,8, unten frei (Welle endet am untersten Schlittenstand) |
| Spindel T8, 2 mm | 149 bis 289 | lokal X = +12, lokal Y = +10 | Länge 140 plus Kupplung, unten frei, oben über Kupplung 5 auf 8 (Ø 19, Länge 25, s = 289 bis 314) am Motor |
| Endschalter | am Schlitten-Obenanschlag, s = 270 | neben dem Schlitten | Mikroschalter 20 x 10 x 6,5 an der Unterseite der Motorplatte, Nase am Schlitten |
| Motorplatte | s = 281 bis 289 | Ring | Innendurchmesser 90, Außendurchmesser 168, Dicke 8, je Station ein keilförmiger Aufsatz, dessen Oberseite senkrecht zur Stationsachse steht, mit NEMA-Lochbild, Bundloch 22,6, Kupplungsdurchgang Ø 21 und Wellensackloch |
| Motor NEMA 17 | s = 289 bis 329 | Achse auf der Spindel (lokal X +12, Y +10) | Flansch 42,3, Länge 40, Welle nach unten |

Radien in Weltkoordinaten, aus r(s): Düse 22, Zylinderoberkante 36,6, Kolben gezogen 46,6, Motorplatte 52,2, Spindel und Motorachse 62,2, Motoraußenkante 83,4. Sehne der fünf Motoren auf Radius 62,2: 73 mm, Luft zwischen den Motoren 31 mm. Sehne auf Zylinderhöhe: 43 mm bei Ø 30, Luft 13 mm. Schlittenzone (r 43): Sehne 50, deshalb Schlitten höchstens 44 breit.

Welthöhen: Düsenspitze z = 105, Flansch z = 244, Motorplatte Oberkante z = 392, Motoroberkante z = 432.

## Sockel (Z 0 bis 120)

| Größe | Wert |
|---|---|
| Standfuß | Ø 190, Höhe 25, Elektronikfach innen 110 x 110 x 20 für die Trägerplatine, Kabeldurchlass nach oben, Buchse 12 V hinten bei 180° |
| Sockelschale | Zylinder Ø 180, Z 25 bis 120, Wand 2,4 |
| Becherraum | Zylinder Ø 84, Boden bei Z = 30 |
| Mischbecher (Kaufteil) | Ø 70, Höhe 60, Rand bei Z = 90 |
| Fenster vorne (0°) | Breite 90, Höhe 80, Unterkante Z = 28, oben halbrund, Messing-Akzentring 4 mm breit als gedruckter Rahmen (im Rendering messingfarben) |
| Düsen | enden bei Z = 105, also 15 mm über dem Becherrand, auf Radius 22 |

## Gehäuse

| Teil | Wert |
|---|---|
| Außendurchmesser | 180, Wand 2,4, Innenradius 87,6 (Motoraußenkante 83,4 plus 4 Luft) |
| Mittelschale | Z 120 bis 300, in vordere und hintere Halbschale geteilt, je 180 hoch |
| Oberschale | Z 300 bis 400, trägt die Motorplatte bei Z 384 bis 392 (Auflagering innen) |
| Haube (Krone) | Z 400 bis 450, abnehmbar, Steckverbindung Nut und Feder 2 mm, innen Platz für die Motoren bis Z 432, LED-Ring WS2812 Ø 50 in der Haubenmitte nach unten leuchtend in die Säule |
| Gesamt | Ø 180 (Fuß 190), Höhe 450 mit Haube |
| Farbgebung Rendering | Schalen cremeweiß, Haube und Fuß dunkelgrau, Fensterrahmen messing |

Varianten: Mit 30-ml-Spritzen (Zylinder 105, Hub 75) wird die Säule 35 mm niedriger, 415 mm. Mit `neigung` lässt sich der Düsenradius einstellen, 6° ergibt 22 mm.

## Handhabung

1. Haube abnehmen (die Motoren bleiben an der Motorplatte, nur die Haube hebt ab).
2. Schlitten der Station per App ganz nach oben fahren. Die Spritze mit dem Kolben nach oben senkrecht herausziehen, der Magnet löst sich von der Stahlscheibe.
3. Gefüllte Spritze von oben einsetzen, bis der Flansch in der Tasche einrastet.
4. Schlitten per App herunterfahren, der Magnet koppelt auf der Stahlscheibe, Referenz ist der Endschalter oben.
5. Becher durchs Fenster einstellen, Farbe wählen, dosieren, Becher entnehmen, umrühren.

Nachfüllen ohne Ausbau: Spritze oben lassen, Luer-Kappe abnehmen, Flasche ansetzen geht nicht, deshalb Spritze herausnehmen (Schritt 2) und am Tisch befüllen.
