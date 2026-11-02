# Revolver: Parameterblatt für Rendering und Druckteile

Zwei Schrittmotoren, fünf Spritzen. Die Spritzen stecken in einem Karussell, das ein Motor im Sockel über eine Welle und einen Innenzahnkranz dreht. Der Stößel sitzt fest über der vorderen Station. Die Nutzerin wählt nur die Farbe in der App, das Gerät dreht jede Station nach vorne und dosiert; am Ende nimmt sie den Becher heraus und rührt um. Optik: schlanke Säule Ø 170 mm, 48 cm hoch, mit einem messingfarbenen Drehring in der Mitte und einem Fenster unten vorne.

Druckbett: Anycubic Kobra 2 Pro, 220 x 220 x 250 mm. Alle Teile passen liegend.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (Fenster, aktive Station). Stationen im Karussell bei 0°, 72°, 144°, 216°, 288°. Die Spritzen stehen senkrecht, keine Neigung.

Stand 3: Karussell wird motorisch gedreht (zweiter NEMA 17 im Sockel bei 180°, Welle Ø 8 nach oben, Ritzel 16 Zähne auf Innenzahnkranz 140 Zähne, Modul 1, unter der Karussellplatte). Rändelschlitz, Rastung, fünf Stationsmagnete und Sperrklinke entfallen, ein Referenzmagnet plus Hall-Sensor bleibt zum Referenzieren.

Stand 2: Stationsradius 50 statt 42 (gedrehte Flansche kollidierten bei 42), Säule Ø 170, Stößelfuß als 15 mm hoher Stempel unter dem Schlitten (Führungen enden über der Flanschplatte), Kupplung über dem Schlitten eingeplant, Brückenaussparungen nur an den hinteren drei Stationen, Führungen tangential ±20.

## Höhen

| Z | Was |
|---|---|
| 0 bis 25 | Standfuß Ø 185, Elektronikfach 80 x 80 x 20 (ESP32 und ein Treiber), Buchse 12 V hinten |
| 25 bis 120 | Sockelschale Ø 170, Wand 2,4 (Innenradius 82,6). Becherraum Ø 64 unter der aktiven Station (Mitte bei Radius 50, Winkel 0°, Außenkante Radius 82), Boden bei Z 30, Fenster vorne 70 breit, 80 hoch, Unterkante Z 28, oben halbrund, Rahmen 4 mm als eigenes Teil. Unter den vier anderen Stationen eine herausnehmbare Abtropfschale (Ring, 4 mm tief) in der Sockeloberseite |
| 30 bis 90 | Mischbecher Ø 60, Höhe 60 (Kaufteil, Glas oder Becher) |
| 105 | Düsenspitzen, 15 über dem Becherrand |
| 120 bis 245 | Mittelschale Ø 170, Wand 2,4, innen bei Z 238 ein Laufring für das Karussell |
| 245 bis 259 | Karussellplatte (Halterplatte) Ø 160 x 14, glatter Rand, kein Schlitz in der Schale mehr. Fünf Flanschtaschen von oben auf Radius 50, Zylinderdurchlass Ø 31. Unter der Platte ein Zahnkranz-Skirt (siehe Karussellantrieb) |
| 259 bis 418 | Oberschale Ø 170 (Mittel- und Oberschale dürfen ein Teil Z 120 bis 300 und ein Teil Z 300 bis 418 sein), trägt oben die Brücke |
| 344 | Kolbenplatte oben bei voller Spritze (s 239 ab Düse) |
| 346 bis 361 | Stößelfuß (Stempel Ø 26, 15 hoch, mit Taster) in oberster Stellung, in unterster Stellung Z 254 bis 269 |
| 361 bis 391 | Stößelschlitten (Block 30 hoch) in oberster Stellung, in unterster Stellung Z 269 bis 299; Führungen reichen von Z 262 bis 418 |
| 393 bis 418 | Kupplung 5 auf 8 unter der Brücke, über dem Schlitten |
| 418 bis 426 | Brücke (Platte Ø 165 mit Aussparungen 48 x 36 (tangential x radial, Ecken R 6) nur über den hinteren drei Stationen 144°, 216°, 288° zum Einsetzen der Spritzen von oben, der Flansch 45 x 32 passt hindurch; über 72° sitzt der Motor), trägt Motor, Spindel, Führungswelle, Endschalter |
| 426 bis 466 | NEMA 17 auf der Brücke, Welle nach unten, 608-Lager in der Brücke |
| 466 bis 480 | Kappe Ø 170 als Haube über Motor und Brücke (Z 426 bis 480, 54 hoch), abnehmbar, darunter LED-Ring Ø 50 |

Gesamt: Ø 170 (Fuß 185), Höhe 480. Mit 30-ml-Spritzen 35 niedriger (445).

## Karussell

| Größe | Wert |
|---|---|
| Stationsradius | 50 (Sehne 58,8, Zylinder Ø 30 hat 29 Luft, gedrehte Flansche 45 x 32 haben 2,9 Luft, Taschen 2,2) |
| Flanschtasche | 45,6 x 32,6, 3,6 tief, von oben offen, Zylinderdurchlass Ø 31, keine Rastlasche nötig (Spritze hängt im Flansch, der Stößel drückt nur) |
| Lagerung | Platte liegt mit ihrem Außenrand auf dem Laufring der Mittelschale (Ring Innen-Ø 152, Außen-Ø 160 bei Z 238 bis 245, Gleitlagerung PETG auf PETG, Rille mit 6-mm-Stahlkugeln als Option, 24 Stück). Innen davon hängt der Zahnkranz-Skirt |
| Rastung | entfällt, der Motor hält die Position |
| Positionserkennung | ein Referenzmagnet Ø 5 x 2 in der Plattenunterseite auf Radius 76 bei Station 1, ein Hall-Sensor fest in der Mittelschale bei 0°. Firmware referenziert beim Start (drehen bis Magnet) und zählt danach Schritte |
| Mittelloch | Ø 40 für Kabel und Blick in den Becherraum |

## Karussellantrieb

| Element | Wert |
|---|---|
| Zahnkranz | Innenverzahnung, Modul 1, 140 Zähne, Teilkreis Ø 140, Fußkreis r 71,25, als Skirt unter der Karussellplatte: Ring r 66 bis 74, Z 228 bis 245, Zähne innen. Die Spritzenzylinder (bis r 65) laufen innen frei vorbei |
| Ritzel | Modul 1, 16 Zähne, Teilkreis Ø 16, 12 breit, auf der Antriebswelle, Mitte bei Radius 62, Winkel 180°, Z 230 bis 242. Übersetzung 8,75, 72° Karussell = 350 Vollschritte, Luft zum nächsten Zylinder 21 |
| Antriebswelle | Stahl Ø 8, Länge 170, Z 72 bis 242, oben Ritzel (Madenschraube auf Abflachung), 608-Lager in der Sockeloberseite (Z 113 bis 120) und Gleitbuchse Ø 8,3 in einem Haltearm der Mittelschale bei Z 215 bis 225, unten Kupplung 5 auf 8 zum Motor |
| Motor 2 | NEMA 17, 40 lang, steht im Sockel bei 180° auf Radius 62, Welle nach oben, Flansch bei Z 72, Motorkörper Z 32 bis 72, Kupplung Z 72 bis 97. Der Becherraum liegt bei 0°, keine Kollision; das Elektronikfach bleibt im Fuß |
| Durchlässe | Bohrung Ø 12 in der Abtropfschale bei 180° r 62 für die Welle |
| Drehmoment | 0,4 Nm am Motor ergibt 3,5 Nm am Karussell, Reibung des Karussells grob 0,25 Nm |

## Stößel (eine Station, vorne)

| Element | Wert |
|---|---|
| Spindel T8, 2 mm Steigung | senkrecht bei Radius 50, Winkel 0°, tangential +20 neben der Spritzenachse, von Z 262 bis 400, Kaufmaß 200 gekürzt auf 150, oben Kupplung 5 auf 8 an der Motorwelle (Kupplung Z 393 bis 418, unter der Brücke, über dem Schlitten), 608-Lager in der Brücke |
| Führungswelle 8 mm | tangential -20 neben der Spritzenachse, von Z 262 bis 424 (Sackloch 6 in der Brücke), Länge 162, Kaufmaß 200 gekürzt, unten frei. Beide Führungen enden 3 über der Karussellplatte, die Flansche drehen frei darunter durch |
| Schlitten | Block 30 hoch, tangential höchstens 56 breit (Welle bei -20, Spindel bei +20), LM8UU auf der Welle, Flanschmutter auf der Spindel, mittig darunter der Stempel Ø 26, 15 hoch, mit federndem Taster (Mikroschalter) in der Stirnfläche, erkennt den Kontakt mit der Kolbenplatte. Stempelunterkante oben Z 346, unten Z 254 (Kolben ganz gedrückt, Platte bei Z 250 bis 254). Hub 92 |
| Endschalter oben | an der Brückenunterseite, Nase am Schlitten, Referenz |
| Motor | NEMA 17, 40 lang, auf der Brücke über der Spindel |

Der Stößel drückt nur. Vor dem Drehen des Karussells fährt er ganz nach oben, die Firmware dreht erst, wenn der obere Endschalter geschlossen ist. Eine mechanische Sperrklinke ist nicht mehr nötig.

## Ablauf

1. App: Farbe wählen, Rezept berechnen, Start.
2. Gerät: Stößel nach oben, Karussell dreht die erste Station nach vorne, Stößel fährt herunter bis der Taster die Kolbenplatte berührt, drückt die berechnete Strecke, wartet 2 Sekunden, hebt 2 mm ab, fährt nach oben. Nächste Station, bis das Rezept fertig ist.
3. LED-Ring zeigt die Zielfarbe, dann Fertigmeldung. Becher durchs Fenster entnehmen, umrühren.

Spritze wechseln: In der App „Wechseln“ wählen, das Gerät dreht die leere Station unter eine der drei Brückenaussparungen (144°, 216°, 288°). Haube abnehmen, Spritze nach oben herausziehen, volle einsetzen. Über 0° sitzt der Stößel, über 72° der Motor, dort geht es nicht.

## Elektronik

ESP32 DevKit, zwei TMC2209 (Stößel und Karussell), ein Hall-Sensor (z. B. A3144) als Referenz, Mikroschalter im Stößelfuß, Endschalter oben, LED-Ring, Netzteil 12 V 3 A. Lochraster oder die Trägerplatine aus `electronics/` mit zwei bestückten Treiberplätzen.

## Was die Firmware wissen muss (für die Software-Sitzung)

- Ein Motor, Dosierung über Strecke nach Kontakt: Kontakt-Taster schließt, dann Schritte = Gramm / g_per_ml * Schritte pro ml, danach 2 mm Rückzug des Stößels (nicht des Kolbens).
- Karussell: zweiter Motor, Referenzfahrt beim Start (drehen bis der Hall-Sensor den Magneten sieht, dann Nullpunkt = Station 1 vorne), danach 350 Vollschritte je Station (Übersetzung 8,75 bei 200 Schritten), Mikroschritte entsprechend. Kürzester Drehweg wählen.
- Vor jedem Drehen: Stößel am oberen Endschalter, sonst nicht drehen.
- Rezeptablauf vollautomatisch: Stationen der Reihe nach, hell zuerst (W, Y, C, M, K), am Ende Fertigmeldung.
- Erste Dosierung einer Session je Station: 0,1 ml Vorlauf, weil die Kolbendichtung erst anliegt.
