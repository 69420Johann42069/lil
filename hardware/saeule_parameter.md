# Säule: Parameterblatt für Rendering und Druckteile

Rundes Design nach Vorbild YSL Rouge Sur Mesure: eine schlanke Säule mit drehbarer Hülse. Die Hülse hat eine Öffnung; man dreht sie vor die gewünschte Station und schiebt die Spritze seitlich ein. Der Mischbecher sitzt unten in der Mitte hinter einem Fenster. Die Motoren sitzen oben unter der Haube, damit unten Platz für die zusammenlaufenden Düsen und den Becher bleibt.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (zum Fenster). Stationen bei 36°, 108°, 180°, 252°, 324°, vorne liegt keine Station, sondern das Fenster.

Stand 5: Spritzen werden radial von außen eingeschoben (nicht mehr von oben, weil dort der Motor sitzt). Drehbare Hülse mit einer Öffnung statt fester Mittelschale. Halterplatte als Stern mit radial offenen Schlitzen. Düsenradius 32, Außendurchmesser 208. Tragstruktur aus drei Säulen. Behebt alle Kollisionen der Zahlenprüfung von Stand 4.

## Stationsachse

Jede Station ist um `neigung` = 4° gekippt: unten (Düse) innen, oben (Motor) außen. Der Weg entlang der Achse heißt s, s = 0 an der Düsenspitze, s wächst nach oben. Radius der Achse: r(s) = 32 + s * sin(4°). Weltkoordinaten: z(s) = 105 + s * cos(4°). Lokales System der Station: lokal Z = s, lokal X tangential, lokal Y radial nach außen.

| Element | s (lokal Z) | Lage quer (X, Y) | Werte |
|---|---|---|---|
| Düse Luer | 0 bis 15 | Achse | Ø 4 außen |
| Spritzenzylinder 60 ml | 15 bis 140 | Achse | Ø 30, Flansch 45 x 32 x 3 bei s = 137 bis 140, lange Flanschseite tangential |
| Kolbenplatte | 145 bis 149 (ganz gedrückt) bis 235 bis 239 (ganz gezogen) | Achse | Ø 30 x 4, Stahlscheibe M10 (Ø 20 x 2) oben aufgeklebt, Kolbenstange 12 x 12 Kreuzprofil |
| Halterplatte (ein Stern für alle fünf) | 128 bis 142 (an jeder Station) | Scheibe mit radialen Schlitzen | Scheibe Ø 198 x 14 bei Welt-Z 233 bis 247, Mittelloch Ø 40. Je Station ein radialer Schlitz 31 breit von der Stationsachse bis zum Außenrand (Zylinder wird von außen eingeschoben, Schlitz um 4° geneigt wie die Achse). Flanschtasche 32,6 breit (tangential 45,6) und 3,6 tief, Taschenboden bei s = 136,8, nach außen offen, innen Anschlag, Rastlasche 1,2 dick am äußeren Ende hält den Flansch. Benachbarte Taschen dürfen ineinander übergehen, kein Steg nötig. Drei Bohrungen Ø 4,2 für die Tragsäulen bei 0°, 144°, 216° auf Radius 90 |
| Kolbenschlitten | Unterkante 151 (gedrückt) bis 241 (gezogen), Höhe 30 | an Welle und Spindel | ein LM8UU (Ø 15, Länge 24) auf der Welle, Flanschmutter T8 (Ø 22, 4 x M3 Lochkreis 16) auf der Spindel, Arm nach innen über die Achse mit Magnet Ø 10 x 3 in der Unterseite bei s = 151, Armdicke 8, Schlitten tangential höchstens 42 breit (rechnerisch 40,5, X von -27,5 bis +13) |
| Linearwelle 8 mm | 149 bis 306 | X = -18, Y = +21 | Länge 157 (Kaufmaß 160 oder 200 gekürzt), oben Sackloch 7,8 in der Motorplatte, unten frei |
| Spindel T8, 2 mm | 149 bis 285 | X = 0, Y = +21 | Länge 136 (Kaufmaß 150), unten frei, oben in der Kupplung |
| Kupplung 5 auf 8 | 275 bis 300 | auf der Spindel | Ø 19, Länge 25, unter der Motorplatte |
| Lager 608 | in der Motorplatte | auf der Spindelachse | Sitz Ø 22,2 x 7 |
| Endschalter | Nase am Schlitten löst bei s = 271 | neben dem Schlitten, X +12 bis +22, Y +8 bis +28 | Mikroschalter 20 x 10 x 6,5 an der Unterseite der Motorplatte |
| Motorplatte | 300 bis 308 | Ring | Innendurchmesser 90, Außendurchmesser 196, Dicke 8, je Station ein keilförmiger Aufsatz, dessen Oberseite senkrecht zur Stationsachse steht, an der niedrigen Seite mindestens 6 hoch (der geneigte Motorflansch taucht sonst 2,7 in die Platte), mit NEMA-Lochbild, Bundloch 22,6, Lagersitz 608 auf der Spindelachse, Wellensackloch. Drei Bohrungen Ø 4,2 für die Tragsäulen auf Radius 90 |
| Motor NEMA 17 | 308 bis 348 | Achse = Spindelachse (X 0, Y +21) | Flansch 42,3, Länge 40, Welle nach unten |

Radien in Welt: Düse 32, Zylinderunterkante (s 15) 33, Zylinderoberkante (s 140) 41,8, Achse an der Motorplatte 53,5, Spindel und Motorachse 74,5, Motorecke am Flansch 97,9, Motorecke oben (s 348) 100,7.

Sehnen: Zylinder unten 38,8 (Luft 8,8), Flansch bei s 140 Sehne 49,1 (Flanschecken der Nachbarn etwa 6 auseinander), Schlittenzone r 46 Sehne 54 (Schlitten 40,5), Motoren auf r 74,5 Sehne 87,6 (Luft 45).

Welthöhen: Düsenspitze z = 105, Flansch z = 245, Halterplatte z = 233 bis 247, Motorplatte Oberkante z = 412, Motoroberkante z = 452.

## Tragstruktur

Drei Säulen Ø 10 (gedruckt, mit M4-Gewindestange innen, oder M4-Gewindestange mit Distanzhülsen) bei 0°, 144°, 216° auf Radius 90, von der Sockeloberseite (Z 120) über die Halterplatte (Z 233 bis 247) bis zur Motorplatte (Z 404 bis 412). Die Hülse berührt die Struktur nicht. Säulen bei 0° liegt hinter dem Fenster über dem Sockel, nicht im Fenster.

## Sockel (Z 0 bis 120)

| Größe | Wert |
|---|---|
| Standfuß | Ø 218, Höhe 25, Elektronikfach innen 110 x 110 x 20 für die Trägerplatine, Kabeldurchlass nach oben, Buchse 12 V hinten bei 180° |
| Sockelschale | Zylinder Ø 208, Z 25 bis 120, Wand 2,4, oben ein Laufring (Lippe 3 breit) für die Hülse |
| Becherraum | Zylinder Ø 84, Boden bei Z = 30 |
| Mischbecher (Kaufteil) | Ø 75, Höhe 60, Rand bei Z = 90 |
| Fenster vorne (0°) | Breite 90, Höhe 80, Unterkante Z = 28, oben halbrund, Rahmen 4 mm breit als eigenes Druckteil (im Rendering messingfarben) |
| Düsen | enden bei Z = 105, also 15 mm über dem Becherrand, auf Radius 32, Becherradius 37,5 |

## Hülse und Gehäuse

| Teil | Wert |
|---|---|
| Außendurchmesser | 208, Wand 2,4, Innenradius 101,6 (Motorecke 100,7 liegt oberhalb der Hülse in der Oberschale, dort Luft 0,9, bei Kollision Oberschale auf 210) |
| Drehhülse | Zylinder Ø 208, Z 120 bis 300, 180 hoch, am Stück druckbar, läuft unten auf dem Laufring des Sockels und oben unter einer Lippe der Oberschale. Eine Öffnung 60 breit, Z 200 bis 290 (vor der Halterplatte und dem Zylinder bis zur Oberkante der Kolbenstange reicht sie nicht, muss sie nicht: eingeschoben wird in Höhe der Halterplatte, die Öffnung reicht von Z 150 bis 290). Griffmulde außen neben der Öffnung. Rastnasen innen, die bei jeder Station einrasten (5 Raststellungen, Kugel-Feder-Rast oder gedruckte Federzunge). |
| Oberschale | Zylinder Ø 208 (bei Bedarf 210), Z 300 bis 420, fest, unten Lippe für die Hülse, trägt die Motorplatte bei Z 404 bis 412 (Auflagering innen), Lüftungsschlitze hinten |
| Haube (Krone) | Z 420 bis 470, abnehmbar nur für Wartung, Steckverbindung Nut und Feder 2 mm, innen frei bis Z 455, LED-Ring WS2812 Ø 50 in der Haubenmitte nach unten leuchtend |
| Gesamt | Ø 208 (Fuß 218), Höhe 470 mit Haube |
| Farbgebung Rendering | Schalen cremeweiß, Hülse cremeweiß mit Öffnung, Haube und Fuß dunkelgrau, Fensterrahmen messing |

Varianten: Mit 30-ml-Spritzen (Zylinder 105, Hub 75) wird die Säule 35 mm niedriger, 435 mm.

## Handhabung

1. Hülse drehen, bis die Öffnung vor der gewünschten Station einrastet. Die App zeigt, welche Station leer ist, und fährt deren Schlitten nach oben.
2. Spritze am Flansch fassen und radial nach außen herausziehen, der Magnet löst sich von der Stahlscheibe, die Rastlasche gibt nach.
3. Gefüllte Spritze mit der Düse nach unten in den Schlitz schieben, bis der Flansch innen anschlägt und die Rastlasche einrastet.
4. Schlitten per App herunterfahren, der Magnet koppelt auf der Stahlscheibe, Referenz ist der Endschalter oben.
5. Hülse zurückdrehen (Öffnung nach hinten), Becher durchs Fenster einstellen, Farbe wählen, dosieren, Becher entnehmen, umrühren.
