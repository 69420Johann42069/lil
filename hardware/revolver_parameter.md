# Revolver: Parameterblatt für Rendering und Druckteile

Ein Schrittmotor, fünf Spritzen. Die Spritzen stecken in einem drehbaren Karussell, der Stößel sitzt fest über der vorderen Station. Zum Farbwechsel wird der Drehring von Hand weitergedreht, bis die gewünschte Spritze vorne einrastet. Die App weiß über einen Hall-Sensor, welche Station vorne steht, und drückt dann die Menge aus. Optik: schlanke Säule Ø 156 mm, 44 cm hoch, mit einem messingfarbenen Drehring in der Mitte und einem Fenster unten vorne.

Druckbett: Anycubic Kobra 2 Pro, 220 x 220 x 250 mm. Alle Teile passen liegend.

Alle Maße in mm. Z nach oben, Z = 0 ist die Tischplatte. Winkel 0° zeigt nach vorne (Fenster, aktive Station). Stationen im Karussell bei 0°, 72°, 144°, 216°, 288°. Die Spritzen stehen senkrecht, keine Neigung.

## Höhen

| Z | Was |
|---|---|
| 0 bis 25 | Standfuß Ø 170, Elektronikfach 80 x 80 x 20 (ESP32 und ein Treiber), Buchse 12 V hinten |
| 25 bis 120 | Sockelschale Ø 156, Wand 2,4. Becherraum Ø 64 unter der aktiven Station (Mitte bei Radius 42, Winkel 0°), Boden bei Z 30, Fenster vorne 70 breit, 80 hoch, Unterkante Z 28, oben halbrund, Rahmen 4 mm als eigenes Teil. Unter den vier anderen Stationen eine herausnehmbare Abtropfschale (Ring, 4 mm tief) in der Sockeloberseite |
| 30 bis 90 | Mischbecher Ø 60, Höhe 60 (Kaufteil, Glas oder Becher) |
| 105 | Düsenspitzen, 15 über dem Becherrand |
| 120 bis 245 | Mittelschale Ø 156, Wand 2,4, innen bei Z 238 ein Laufring für das Karussell |
| 245 bis 259 | Karussellplatte (Halterplatte) Ø 162 x 14, ragt 3 mm über die Schale hinaus als Drehring, Außenkante gerändelt, messingfarben. Fünf Flanschtaschen von oben, Zylinderdurchlass Ø 31 |
| 259 bis 380 | Oberschale Ø 156, Z 259 bis 380, unten Schlitz 15 hoch für den Drehring, trägt oben die Brücke |
| 344 | Kolbenplatte oben bei voller Spritze (s 239 ab Düse) |
| 350 bis 380 | Stößelschlitten in oberster Stellung |
| 380 bis 388 | Brücke (Platte Ø 150 mit Aussparungen über den vier inaktiven Stationen zum Einsetzen der Spritzen von oben), trägt Motor, Spindel, Führungswelle, Endschalter |
| 388 bis 428 | NEMA 17 auf der Brücke, Welle nach unten |
| 428 bis 440 | Kappe Ø 156, abnehmbar, darunter LED-Ring Ø 50 |

Gesamt: Ø 156 (Fuß 170, Drehring 162), Höhe 440. Mit 30-ml-Spritzen 35 niedriger (405).

## Karussell

| Größe | Wert |
|---|---|
| Stationsradius | 42 (Sehne 49,4, Zylinder Ø 30 hat 19 Luft, Flansch 45 x 32 tangential hat 4,4 Luft) |
| Flanschtasche | 45,6 x 32,6, 3,6 tief, von oben offen, Zylinderdurchlass Ø 31, keine Rastlasche nötig (Spritze hängt im Flansch, der Stößel drückt nur) |
| Lagerung | Platte liegt auf dem Laufring der Mittelschale (Ring Innen-Ø 120, Außen-Ø 150, Gleitlagerung PETG auf PETG, Rille mit 6-mm-Stahlkugeln als Option, 24 Stück) |
| Rastung | fünf Kerben an der Plattenunterseite auf Radius 65, Federzunge 1,2 dick in der Mittelschale rastet ein |
| Positionserkennung | fünf Magnete Ø 5 x 2 in der Plattenunterseite auf Radius 58 (eine je Station), ein Hall-Sensor fest in der Mittelschale bei 0°; Station 1 hat einen zweiten Magneten auf Radius 50, zweiter Hall-Sensor darüber als Referenz. Firmware zählt Rastschritte ab Referenz |
| Mittelloch | Ø 40 für Kabel und Blick in den Becherraum |

## Stößel (eine Station, vorne)

| Element | Wert |
|---|---|
| Spindel T8, 2 mm Steigung | senkrecht bei Radius 42, Winkel 0°, tangential +18 neben der Spritzenachse, Länge 150, oben Kupplung 5 auf 8 an der Motorwelle (Kupplung Z 355 bis 380, unter der Brücke), 608-Lager in der Brücke |
| Führungswelle 8 mm | tangential -18 neben der Spritzenachse, Länge 150, Sackloch in der Brücke, unten frei |
| Schlitten | Höhe 30, LM8UU auf der Welle, Flanschmutter auf der Spindel, dazwischen der Fuß: Teller Ø 26 mit federndem Taster (Mikroschalter) in der Mitte, erkennt den Kontakt mit der Kolbenplatte. Unterkante Fuß in oberster Stellung Z 350, in unterster Stellung Z 250 (Kolben ganz gedrückt, Platte bei Z 250 bis 254). Hub 100 |
| Endschalter oben | an der Brückenunterseite, Nase am Schlitten, Referenz |
| Motor | NEMA 17, 40 lang, auf der Brücke über der Spindel |

Der Stößel drückt nur. Vor dem Drehen des Karussells fährt er ganz nach oben (App und Firmware prüfen den Endschalter, die Rastung lässt sich sonst nicht drehen: eine Sperrklinke am Schlitten blockiert den Drehring, solange der Schlitten nicht oben ist).

## Ablauf

1. App: Farbe wählen, Rezept berechnen. Die App zeigt die Reihenfolge der Stationen an.
2. Drehring drehen, bis die angezeigte Station vorne einrastet. Die App bestätigt per Hall-Sensor.
3. Stößel fährt herunter, bis der Taster die Kolbenplatte berührt, dann die berechnete Strecke weiter, dann 2 mm hoch. Nächste Station, zurück zu Schritt 2.
4. Becher durchs Fenster entnehmen, umrühren.

Spritze wechseln: Kappe abnehmen, Karussell so drehen, dass die leere Station unter einer Brückenaussparung steht, Spritze nach oben herausziehen, volle einsetzen.

## Elektronik

ESP32 DevKit, ein TMC2209, zwei Hall-Sensoren (z. B. SS49E oder A3144), Mikroschalter im Stößelfuß, Endschalter oben, LED-Ring, Netzteil 12 V 2 A. Keine Trägerplatine nötig, ein Lochrasterstück oder ein fertiges ESP32-Stepper-Shield reicht.

## Was die Firmware wissen muss (für die Software-Sitzung)

- Ein Motor, Dosierung über Strecke nach Kontakt: Kontakt-Taster schließt, dann Schritte = Gramm / g_per_ml * Schritte pro ml, danach 2 mm Rückzug des Stößels (nicht des Kolbens).
- Station = Zählwert der Hall-Impulse ab Referenzmagnet, Drehrichtung egal, Rastung sichert die Position.
- Vor jedem Drehen: Stößel am oberen Endschalter, sonst Drehring gesperrt.
- Erste Dosierung einer Session je Station: 0,1 ml Vorlauf, weil die Kolbendichtung erst anliegt.
