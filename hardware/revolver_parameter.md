# Revolver: Parameterblatt für Rendering und Druckteile

Ein Schrittmotor, fünf Spritzen. Die Spritzen stecken in einem drehbaren Karussell, der Stößel sitzt fest über der vorderen Station. Zum Farbwechsel wird der Drehring von Hand weitergedreht, bis die gewünschte Spritze vorne einrastet. Die App weiß über einen Hall-Sensor, welche Station vorne steht, und drückt dann die Menge aus. Optik: schlanke Säule Ø 170 mm, 48 cm hoch, mit einem messingfarbenen Drehring in der Mitte und einem Fenster unten vorne.

Druckbett: Anycubic Kobra 2 Pro, 220 x 220 x 250 mm. Alle Teile passen liegend.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (Fenster, aktive Station). Stationen im Karussell bei 0°, 72°, 144°, 216°, 288°. Die Spritzen stehen senkrecht, keine Neigung.

Stand 2: Stationsradius 50 statt 42 (gedrehte Flansche kollidierten bei 42), Säule Ø 170, Stößelfuß als 15 mm hoher Stempel unter dem Schlitten (Führungen enden über der Flanschplatte), Kupplung über dem Schlitten eingeplant, Brückenaussparungen nur an den hinteren drei Stationen, Führungen tangential ±20.

## Höhen

| Z | Was |
|---|---|
| 0 bis 25 | Standfuß Ø 185, Elektronikfach 80 x 80 x 20 (ESP32 und ein Treiber), Buchse 12 V hinten |
| 25 bis 120 | Sockelschale Ø 170, Wand 2,4 (Innenradius 82,6). Becherraum Ø 64 unter der aktiven Station (Mitte bei Radius 50, Winkel 0°, Außenkante Radius 82), Boden bei Z 30, Fenster vorne 70 breit, 80 hoch, Unterkante Z 28, oben halbrund, Rahmen 4 mm als eigenes Teil. Unter den vier anderen Stationen eine herausnehmbare Abtropfschale (Ring, 4 mm tief) in der Sockeloberseite |
| 30 bis 90 | Mischbecher Ø 60, Höhe 60 (Kaufteil, Glas oder Becher) |
| 105 | Düsenspitzen, 15 über dem Becherrand |
| 120 bis 245 | Mittelschale Ø 170, Wand 2,4, innen bei Z 238 ein Laufring für das Karussell |
| 245 bis 259 | Karussellplatte (Halterplatte) Ø 160 x 14, Außenkante gerändelt, messingfarben, durch einen Schlitz in der Schale (20 hoch, 60 breit, bei -60°) mit dem Daumen drehbar. Fünf Flanschtaschen von oben auf Radius 50, Zylinderdurchlass Ø 31 |
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
| Lagerung | Platte liegt auf dem Laufring der Mittelschale (Ring Innen-Ø 130, Außen-Ø 158, Gleitlagerung PETG auf PETG, Rille mit 6-mm-Stahlkugeln als Option, 24 Stück) |
| Rastung | fünf Kerben an der Plattenunterseite auf Radius 72, Federzunge 1,2 dick in der Mittelschale rastet ein |
| Positionserkennung | fünf Magnete Ø 5 x 2 in der Plattenunterseite auf Radius 76 (eine je Station), ein Hall-Sensor fest in der Mittelschale bei 0°; Station 1 hat einen zweiten Magneten auf Radius 68, zweiter Hall-Sensor darüber als Referenz. Firmware zählt Rastschritte ab Referenz |
| Mittelloch | Ø 40 für Kabel und Blick in den Becherraum |

## Stößel (eine Station, vorne)

| Element | Wert |
|---|---|
| Spindel T8, 2 mm Steigung | senkrecht bei Radius 50, Winkel 0°, tangential +20 neben der Spritzenachse, von Z 262 bis 400, Kaufmaß 200 gekürzt auf 150, oben Kupplung 5 auf 8 an der Motorwelle (Kupplung Z 393 bis 418, unter der Brücke, über dem Schlitten), 608-Lager in der Brücke |
| Führungswelle 8 mm | tangential -20 neben der Spritzenachse, von Z 262 bis 424 (Sackloch 6 in der Brücke), Länge 162, Kaufmaß 200 gekürzt, unten frei. Beide Führungen enden 3 über der Karussellplatte, die Flansche drehen frei darunter durch |
| Schlitten | Block 30 hoch, tangential höchstens 56 breit (Welle bei -20, Spindel bei +20), LM8UU auf der Welle, Flanschmutter auf der Spindel, mittig darunter der Stempel Ø 26, 15 hoch, mit federndem Taster (Mikroschalter) in der Stirnfläche, erkennt den Kontakt mit der Kolbenplatte. Stempelunterkante oben Z 346, unten Z 254 (Kolben ganz gedrückt, Platte bei Z 250 bis 254). Hub 92 |
| Endschalter oben | an der Brückenunterseite, Nase am Schlitten, Referenz |
| Motor | NEMA 17, 40 lang, auf der Brücke über der Spindel |

Der Stößel drückt nur. Vor dem Drehen des Karussells fährt er ganz nach oben (App und Firmware prüfen den Endschalter, die Rastung lässt sich sonst nicht drehen: eine Sperrklinke am Schlitten blockiert den Drehring, solange der Schlitten nicht oben ist).

## Ablauf

1. App: Farbe wählen, Rezept berechnen. Die App zeigt die Reihenfolge der Stationen an.
2. Drehring drehen, bis die angezeigte Station vorne einrastet. Die App bestätigt per Hall-Sensor.
3. Stößel fährt herunter, bis der Taster die Kolbenplatte berührt, dann die berechnete Strecke weiter, dann 2 mm hoch. Nächste Station, zurück zu Schritt 2.
4. Becher durchs Fenster entnehmen, umrühren.

Spritze wechseln: Haube abnehmen, Karussell so drehen, dass die leere Station hinten unter einer der drei Brückenaussparungen (144°, 216°, 288°) steht, Spritze nach oben herausziehen, volle einsetzen. Über 0° sitzt der Stößel, über 72° der Motor, dort geht es nicht.

## Elektronik

ESP32 DevKit, ein TMC2209, zwei Hall-Sensoren (z. B. SS49E oder A3144), Mikroschalter im Stößelfuß, Endschalter oben, LED-Ring, Netzteil 12 V 2 A. Keine Trägerplatine nötig, ein Lochrasterstück oder ein fertiges ESP32-Stepper-Shield reicht.

## Was die Firmware wissen muss (für die Software-Sitzung)

- Ein Motor, Dosierung über Strecke nach Kontakt: Kontakt-Taster schließt, dann Schritte = Gramm / g_per_ml * Schritte pro ml, danach 2 mm Rückzug des Stößels (nicht des Kolbens).
- Station = Zählwert der Hall-Impulse ab Referenzmagnet, Drehrichtung egal, Rastung sichert die Position.
- Vor jedem Drehen: Stößel am oberen Endschalter, sonst Drehring gesperrt.
- Erste Dosierung einer Session je Station: 0,1 ml Vorlauf, weil die Kolbendichtung erst anliegt.
