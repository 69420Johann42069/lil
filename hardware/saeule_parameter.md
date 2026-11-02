# Säule: Parameterblatt für Rendering und Druckteile

Rundes Design nach Vorbild YSL Rouge Sur Mesure: eine schlanke Säule, Kartuschen (Spritzen) werden von oben eingesetzt, der Mischbecher sitzt unten in der Mitte und wird durch ein Fenster an der Vorderseite entnommen. Die Motoren sitzen oben unter der Haube, damit unten Platz für die zusammenlaufenden Düsen und den Becher bleibt.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (zum Fenster). Stationen bei 36°, 108°, 180°, 252°, 324°, vorne liegt keine Station, sondern das Fenster.

Stand 4: Neigung 4°, Düsenradius 30, Spindel direkt hinter der Spritze, Welle daneben, beide so weit außen, dass der Spritzenflansch beim Einsetzen von oben daran vorbeikommt, Halterplatte Ø 194 auf dem Auflagering, Außendurchmesser 200. Behebt die Kollisionen der Zahlenprüfungen von Stand 2 und 3 (Motorecken, Zylinder unten, Kupplung im Motor, Kolbenplatte an den Führungen, Flansch an Nachbarflansch, Halterplatte zu klein).

## Stationsachse

Jede Station ist um `neigung` = 4° gekippt: unten (Düse) innen, oben (Motor) außen. Der Weg entlang der Achse heißt s, s = 0 an der Düsenspitze, s wächst nach oben. Radius der Achse: r(s) = 30 + s * sin(4°). Weltkoordinaten: z(s) = 105 + s * cos(4°). Lokales System der Station: lokal Z = s, lokal X tangential, lokal Y radial nach außen.

| Element | s (lokal Z) | Lage quer (X, Y) | Werte |
|---|---|---|---|
| Düse Luer | 0 bis 15 | Achse | Ø 4 außen |
| Spritzenzylinder 60 ml | 15 bis 140 | Achse | Ø 30, Flansch 45 x 32 x 3 bei s = 137 bis 140, lange Flanschseite tangential (radial also ±16, die Führungen beginnen radial erst bei 17, damit die Spritze von oben vorbei passt) |
| Kolbenplatte | 145 bis 149 (ganz gedrückt) bis 235 bis 239 (ganz gezogen) | Achse | Ø 30 x 4, Stahlscheibe M10 (Ø 20 x 2) oben aufgeklebt, Kolbenstange 12 x 12 Kreuzprofil |
| Halterplatte (ein Teil für alle fünf) | 128 bis 142 (an jeder Station) | Scheibe | Scheibe Ø 194 x 14 bei Welt-Z 233 bis 247, liegt auf dem Auflagering der Mittelschale (Innenradius 97,6), fünf um 4° geneigte Durchlässe Ø 31, Flanschtaschen 45,6 x 32,6, Taschenboden bei s = 136,8, nach oben offen, Rastlasche 1,2 dick je Tasche, Mittelloch Ø 40 für Kabel |
| Kolbenschlitten | Unterkante 151 (gedrückt) bis 241 (gezogen), Höhe 30 | an Welle und Spindel | ein LM8UU (Ø 15, Länge 24) auf der Welle, Flanschmutter T8 (Ø 22, 4 x M3 Lochkreis 16) auf der Spindel, Arm nach innen über die Achse mit Magnet Ø 10 x 3 in der Unterseite bei s = 151, Armdicke 8, Schlitten tangential höchstens 42 breit |
| Linearwelle 8 mm | 149 bis 306 | X = -18, Y = +21 | Länge 157 (Kaufmaß 160 oder 200 gekürzt), oben Sackloch 7,8 in der Motorplatte, unten frei |
| Spindel T8, 2 mm | 149 bis 285 | X = 0, Y = +21 | Länge 136 (Kaufmaß 150), unten frei, oben in der Kupplung |
| Kupplung 5 auf 8 | 275 bis 300 | auf der Spindel | Ø 19, Länge 25, sitzt unter der Motorplatte, Motorwelle kommt von oben durch die Platte |
| Lager 608 | in der Motorplatte | auf der Spindelachse | Sitz Ø 22,2 x 7 in der Platte, Spindel oder Motorwelle läuft darin, Kupplung direkt darunter |
| Endschalter | Nase am Schlitten löst bei s = 271 | neben dem Schlitten | Mikroschalter 20 x 10 x 6,5 an der Unterseite der Motorplatte |
| Motorplatte | 300 bis 308 | Ring | Innendurchmesser 90, Außendurchmesser 188, Dicke 8, je Station ein keilförmiger Aufsatz, dessen Oberseite senkrecht zur Stationsachse steht, an der niedrigen Seite mindestens 3 hoch, damit der geneigte Motorflansch nicht in die Platte taucht, mit NEMA-Lochbild, Bundloch 22,6, Lagersitz 608 auf der Spindelachse und Wellensackloch |
| Motor NEMA 17 | 308 bis 348 | Achse = Spindelachse (X 0, Y +21) | Flansch 42,3, Länge 40, Welle nach unten |

Abstände, nachgerechnet: Spindel zur Spritzenachse 21, Welle 27,7, Innenkante beider Führungen radial bei 17, Flansch reicht bis 16, Kolbenplatte bis 15. Radien in Welt: Düse 30, Zylinderunterkante (s 15) 31, Zylinderoberkante 39,8, Achse an der Motorplatte 51,5, Spindel und Motorachse 72,5, Motorecke 96,0.

Sehnen: Zylinder unten 36,4 (Luft 6), Flansch bei s 140 Sehne 46,8 (Flansch 45, Luft 1,8), Schlittenzone r 44 Sehne 52 (Schlitten 40,5), Motoren auf r 72,5 Sehne 85 (Luft 43).

Welthöhen: Düsenspitze z = 105, Flansch z = 245, Halterplatte z = 233 bis 247, Motorplatte Oberkante z = 412, Motoroberkante z = 452.

## Sockel (Z 0 bis 120)

| Größe | Wert |
|---|---|
| Standfuß | Ø 210, Höhe 25, Elektronikfach innen 110 x 110 x 20 für die Trägerplatine, Kabeldurchlass nach oben, Buchse 12 V hinten bei 180° |
| Sockelschale | Zylinder Ø 200, Z 25 bis 120, Wand 2,4 |
| Becherraum | Zylinder Ø 84, Boden bei Z = 30 |
| Mischbecher (Kaufteil) | Ø 75, Höhe 60, Rand bei Z = 90 |
| Fenster vorne (0°) | Breite 90, Höhe 80, Unterkante Z = 28, oben halbrund, Rahmen 4 mm breit als eigenes Druckteil (im Rendering messingfarben) |
| Düsen | enden bei Z = 105, also 15 mm über dem Becherrand, auf Radius 30, Becherradius 37,5 |

## Gehäuse

| Teil | Wert |
|---|---|
| Außendurchmesser | 200, Wand 2,4, Innenradius 97,6 (Motorecke 96,0 plus 1,6 Luft) |
| Mittelschale | Z 120 bis 300, in vordere und hintere Halbschale geteilt, je 180 hoch, innen bei Z 233 ein Auflagering 4 breit für die Halterplatte |
| Oberschale | Z 300 bis 420, trägt die Motorplatte bei Z 404 bis 412 (Auflagering innen) |
| Haube (Krone) | Z 420 bis 470, abnehmbar, Steckverbindung Nut und Feder 2 mm, innen frei bis Z 455 für die Motoren, LED-Ring WS2812 Ø 50 in der Haubenmitte nach unten leuchtend |
| Gesamt | Ø 200 (Fuß 210), Höhe 470 mit Haube |
| Farbgebung Rendering | Schalen cremeweiß, Haube und Fuß dunkelgrau, Fensterrahmen messing |

Varianten: Mit 30-ml-Spritzen (Zylinder 105, Hub 75) wird die Säule 35 mm niedriger, 435 mm.

## Handhabung

1. Haube abnehmen (die Motoren bleiben auf der Motorplatte, nur die Haube hebt ab).
2. Schlitten der Station per App ganz nach oben fahren. Die Spritze am Kolben senkrecht herausziehen, der Magnet löst sich von der Stahlscheibe.
3. Gefüllte Spritze von oben einsetzen, bis der Flansch in der Tasche einrastet.
4. Schlitten per App herunterfahren, der Magnet koppelt auf der Stahlscheibe, Referenz ist der Endschalter oben.
5. Becher durchs Fenster einstellen, Farbe wählen, dosieren, Becher entnehmen, umrühren.
