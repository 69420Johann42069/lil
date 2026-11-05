> **Hinweis:** Die alte Trägerplatine (Fünf-Motor-Variante: `NETZLISTE.md`, `generate_pcb.py`, `farbmixer_traeger.kicad_pcb`) gilt für Stand 8 nicht mehr. Stand 8 wird auf Lochraster mit Dupont-Leitungen verdrahtet, genau nach diesem Plan.

# Verdrahtungsplan Farbmischer Stand 8 (Lochraster / Dupont)

Grundlage ist der Vertrag Stand 8 (Pinbelegung und Versorgung sind verbindlich, Firmware und Web-App rechnen mit denselben Pins). Zwei NEMA 17 mit A4988, Mikroschritt 1/16, kein LED-Ring, keine Pumpen. Keine Zugangsdaten in dieser Datei.

## 1. Bauteilliste (Kaufteile)

| Menge | Bauteil | Bemerkung |
|---|---|---|
| 1 | ESP32 DevKit, 30 Pin | Beschriftung D13, D14 usw. = GPIO13, GPIO14 |
| 2 | A4988 Treibermodul | übliche rote Module, Kühlkörper bei 0,35 A nicht nötig |
| 2 | NEMA 17, 34 mm, Nennstrom 0,4 A | Stößel und Karussell (derselbe Typ) |
| 1 | Wägezelle 500 g mit HX711-Modul | |
| 1 | Mini-360 (Step-down) | 12 V auf 5,0 V, vor dem Anschluss einstellen |
| 1 | Hohlsteckerbuchse 5,5 x 2,1 | für das 12-V-Netzteil |
| 1 | Mikroschalter mit Rollenhebel | Stößel oben |
| 1 | Hall-Sensor A3144 (TO-92) | Karussell Park, dazu der Magnet 5 x 2 aus der Stückliste |
| 2 | Elko 100 µF 25 V | je einer an VMOT eines Treibers |
| 1 | Kondensator 100 nF | am A3144 |

Vorausgesetzt, aber nicht in dieser Liste: Netzteil 12 V (3 A) mit Hohlstecker 5,5 x 2,1, Lochraster, Dupont-Leitungen, Litze 0,5 mm² für 12 V und Motoren, Schrumpfschlauch.

Optional (nur falls vorhanden): 10 kΩ von GPIO23 nach 3,3 V (siehe Hinweise).

## 2. Verbindungen

Alle Pins sind GPIOs des ESP32 (30-Pin-DevKit). Pinbelegung wie im Vertrag. Spalte „Leitung": D = Dupont, L = Litze 0,5 mm².

### 2.1 Stromversorgung

| Von | Zu | Leitung |
|---|---|---|
| Netzteil 12 V, Stecker | Hohlsteckerbuchse | Stecker in Buchse |
| Buchse Plus (Mittelstift) | +12-V-Schiene (Lochraster) | L rot |
| Buchse Minus (Hülse) | Sternpunkt GND (Lochraster) | L schwarz |
| +12-V-Schiene | Treiber 1 VMOT | L rot |
| +12-V-Schiene | Treiber 2 VMOT | L rot |
| +12-V-Schiene | Mini-360 IN+ | L rot |
| Sternpunkt GND | Treiber 1 GND (Motorseite, neben VMOT) | L schwarz, eigene Leitung |
| Sternpunkt GND | Treiber 2 GND (Motorseite, neben VMOT) | L schwarz, eigene Leitung |
| Sternpunkt GND | Mini-360 IN− | L schwarz, eigene Leitung |
| Elko 100 µF Plus | Treiber 1 VMOT | Beinchen direkt am Pin |
| Elko 100 µF Minus | Treiber 1 GND (Motorseite) | Beinchen direkt am Pin |
| Elko 100 µF Plus | Treiber 2 VMOT | Beinchen direkt am Pin |
| Elko 100 µF Minus | Treiber 2 GND (Motorseite) | Beinchen direkt am Pin |
| Mini-360 OUT+ (5,0 V) | ESP32 VIN | D oder L rot |
| Mini-360 OUT− | ESP32 GND (neben VIN) | D oder L schwarz |
| ESP32 3V3 | 3,3-V-Schiene (Lochraster) | D |
| ESP32 GND | Logik-GND-Schiene (Lochraster) | D |

Die 3,3-V-Schiene versorgt Treiber-VDD, MS1 bis MS3 und HX711. Der A3144 braucht laut Datenblatt mindestens 4,5 V und hängt deshalb an der 5-V-Leitung (VIN-Seite des Mini-360); sein Ausgang ist offener Kollektor, der nur nach GND zieht, der interne Pullup von GPIO19 liegt auf 3,3 V, der Pin sieht also nie mehr als 3,3 V. Die Logik-GND-Schiene führt nur Signalmasse (Treiber-Logik-GND, HX711, A3144).

### 2.2 Treiber 1 (Stößel)

| Von | Zu | Leitung |
|---|---|---|
| ESP32 GPIO13 | Treiber 1 STEP | D |
| ESP32 GPIO14 | Treiber 1 DIR | D |
| ESP32 GPIO23 | Treiber 1 ENABLE (LOW = aktiv) | D, gemeinsame Leitung mit Treiber 2 |
| 3,3-V-Schiene | Treiber 1 MS1, MS2, MS3 | D (1/16 Schritt) |
| Treiber 1 RESET | Treiber 1 SLEEP | Brücke (Draht oder Dupont) |
| 3,3-V-Schiene | Treiber 1 VDD | D |
| Logik-GND-Schiene | Treiber 1 GND (Logikseite, neben VDD) | D |
| Motor 1, Spule A (ein Adernpaar) | Treiber 1 1A und 1B | verdrilltes Paar |
| Motor 1, Spule B (anderes Adernpaar) | Treiber 1 2A und 2B | verdrilltes Paar |

### 2.3 Treiber 2 (Karussell)

| Von | Zu | Leitung |
|---|---|---|
| ESP32 GPIO27 | Treiber 2 STEP | D |
| ESP32 GPIO26 | Treiber 2 DIR | D |
| ESP32 GPIO23 | Treiber 2 ENABLE (LOW = aktiv) | D, gemeinsame Leitung mit Treiber 1 |
| 3,3-V-Schiene | Treiber 2 MS1, MS2, MS3 | D (1/16 Schritt) |
| Treiber 2 RESET | Treiber 2 SLEEP | Brücke |
| 3,3-V-Schiene | Treiber 2 VDD | D |
| Logik-GND-Schiene | Treiber 2 GND (Logikseite, neben VDD) | D |
| Motor 2, Spule A | Treiber 2 1A und 1B | verdrilltes Paar |
| Motor 2, Spule B | Treiber 2 2A und 2B | verdrilltes Paar |

Die zwei Spulen eines Motors findest du mit dem Durchgangsprüfer: zwei Adern mit etwa 1 bis 4 Ω gehören zusammen, zwischen den Paaren kein Durchgang. Aderfarben nicht blind glauben.

### 2.4 Mikroschalter (Stößel oben)

Mikroschalter als Schließer: Anschlüsse C (Common) und NO benutzen, NC bleibt frei.

| Von | Zu | Leitung |
|---|---|---|
| Mikroschalter C | Logik-GND-Schiene | D oder Litze dünn |
| Mikroschalter NO | ESP32 GPIO18 (INPUT_PULLUP) | D oder Litze dünn |

Gedrückt = GPIO18 LOW = Stößel oben (Park).

### 2.5 Hall-Sensor A3144 (Karussell Park)

A3144 von der beschrifteten Flachseite gesehen, Beinchen nach unten: links Pin 1 (VCC), Mitte Pin 2 (GND), rechts Pin 3 (OUT, offener Kollektor).

| Von | Zu | Leitung |
|---|---|---|
| A3144 Pin 1 (VCC) | 5-V-Leitung (Mini-360 Ausgang, gleiche Leitung wie ESP32 VIN) | D oder Litze dünn |
| A3144 Pin 2 (GND) | Logik-GND-Schiene | D oder Litze dünn |
| A3144 Pin 3 (OUT) | ESP32 GPIO19 (INPUT_PULLUP) | D oder Litze dünn |
| 100 nF | zwischen A3144 Pin 1 und Pin 2, direkt am Sensor | Beinchen |

Aktiv LOW, wenn der Magnet in der Karussellnabe darüber steht. Außer dem internen Pullup gibt es keinen Widerstand.

### 2.6 HX711 und Wägezelle

| Von | Zu | Leitung |
|---|---|---|
| HX711 VCC | 3,3-V-Schiene | D |
| HX711 GND | Logik-GND-Schiene | D |
| HX711 DT (DOUT) | ESP32 GPIO32 | D, unter 15 cm |
| HX711 SCK | ESP32 GPIO33 | D, unter 15 cm |
| Wägezelle rot | HX711 E+ | an die Zelle gelötete Adern |
| Wägezelle schwarz | HX711 E− | |
| Wägezelle weiß | HX711 A− | |
| Wägezelle grün | HX711 A+ | |

Aderfarben der Wägezelle sind nicht normiert: Datenblatt des gekauften Teils prüfen. Zeigt die Waage beim Belasten fallende Werte, A+ und A− tauschen (oder Vorzeichen in der Firmware).

### 2.7 Belegung auf einen Blick (Vertrag)

| Funktion | GPIO |
|---|---|
| Stößel STEP / DIR | 13 / 14 |
| Karussell STEP / DIR | 27 / 26 |
| ENABLE beider A4988 | 23 |
| Mikroschalter Stößel oben | 18 |
| Hall-Sensor Park | 19 |
| HX711 DOUT / SCK | 32 / 33 |

Keine weiteren Pins belegt.

## 3. Strom je Motor einstellen (A4988)

Formel des A4988: **Vref = I × 8 × Rs** (I = gewünschter Spitzenstrom je Spule, Rs = Sense-Widerstand des Moduls).

Rechnung mit Python (Bruchrechnung, exakt), Rs = 0,068 Ω:

| Zielstrom | Vref |
|---|---|
| 0,35 A (empfohlen für das Karussell, Treiber 2) | 0,35 × 8 × 0,068 = **0,1904 V** (rund 190 mV) |
| 0,40 A (Nennstrom, Stößel, Treiber 1, nicht überschreiten) | 0,40 × 8 × 0,068 = **0,2176 V** (rund 218 mV) |
| 0,30 A (falls der Motor zu warm wird) | 0,30 × 8 × 0,068 = 0,1632 V |

Gegenprobe: 0,1904 V / (8 × 0,068) = 0,35 A genau.

**Der Sense-Widerstand des gekauften Moduls ist zu prüfen.** Auf den beiden kleinen SMD-Widerständen neben dem Chip steht R068 (0,068 Ω, die übliche rote Variante), R100 (0,1 Ω) oder R050 (0,05 Ω). Bei einem anderen Wert muss Vref neu gerechnet werden. Für 0,35 A: Rs 0,1 Ω ergibt 0,280 V, Rs 0,05 Ω ergibt 0,140 V. Mit dem falschen Rs wird der Strom um 36 Prozent zu hoch oder um 32 Prozent zu niedrig (Rs 0,1: 0,1904 V ergäbe nur 0,238 A, Rs 0,05: ergäbe 0,476 A).

Vorgehen, für jeden Treiber getrennt:

1. Alles stromlos. Motor anstecken (nie bei eingeschalteter Spannung).
2. 12 V einschalten (ESP32 ohne Firmware oder ENABLE hoch, der Motor steht).
3. Multimeter (Gleichspannung, Bereich 2 V): Minus an GND des Treibers, Plus an die Metallschraube des Potis.
4. Mit kleinem Schraubendreher (kein Metall mit Handkontakt, besser Keramik/Kunststoff) drehen: Treiber 1 (Stößel) auf 0,2176 V, Treiber 2 (Karussell) auf 0,1904 V.
5. 12 V aus.

Hinweis: Das ist der Spitzenstrom der Chopper-Regelung. Der Effektivwert liegt im Mikroschrittbetrieb bei etwa 0,707 × 0,35 A = 0,25 A. Das ist vorsichtig. Verliert der Karussell-Motor Schritte, in 0,01-V-Schritten erhöhen, aber nicht über 0,2176 V (0,4 A).

## 4. Hinweise zum Aufbau

- **Mikroschritt:** MS1, MS2 und MS3 jedes Treibers fest auf 3,3 V (1/16). Nie auf 5 V.
- **RESET mit SLEEP verbinden** (beide Treiber), sonst bleibt der Treiber aus. Reagiert ein Modul trotzdem nicht, die verbundene Brücke zusätzlich auf 3,3 V legen.
- **Elko nah an VMOT:** 100 µF 25 V mit kürzesten Beinchen zwischen VMOT und GND-Pin des Treibers (Motorseite), Plus (langes Beinchen, Streifen = Minus) an VMOT. Falsche Polung zerstört den Elko.
- **Nie einen Motor im Betrieb abstecken.** Beim Abziehen unter Spannung entstehen Spannungsspitzen, die den Treiber zerstören. Erst 12 V aus, dann Stecker.
- **Mini-360 vor dem Anschluss auf 5,0 V einstellen:** Mini-360 allein an 12 V hängen, Ausgang ohne Last mit dem Multimeter messen, am Poti auf 5,0 V drehen (das Poti hat mehrere Umdrehungen), dann erst an VIN. Werkseinstellung kann weit über 5 V liegen und den ESP32 zerstören.
- **Masse sternförmig:** Netzteil-Minus (Hohlsteckerbuchse) ist der Sternpunkt. Von dort je eine eigene Leitung zu Treiber 1 (Motorseite), Treiber 2 (Motorseite) und Mini-360 IN−. Nicht von Treiber zu Treiber durchschleifen. Das Treibermodul verbindet seine beiden GND-Pins intern, eine kleine Schleife über die Logik-Masse ist deshalb nicht ganz vermeidbar und bei 0,35 A unkritisch.
- **Motorkabel und Turm:** Motorleitungen des Karussellmotors laufen durch den Motorturm und treten durch das Kabelfenster unten in der -Y-Wand aus. Motorleitungen paarweise verdrillen und getrennt von den HX711-Leitungen führen, die kurz bleiben (unter 15 cm).
- **Stößelmotor und Mikroschalter:** Leitungen im Kabelkanal am Zuganker nach oben führen (Parameterblatt Abschnitt 9, Zuganker θ -128,6, mit Kabelbindern festlegen), Zugentlastung am Motor.
- **Hall-Sensor:** liegt flach in der Tasche auf dem Turm, die Beschriftungsseite zum Magneten in der Nabe gewandt, die Beinchen gehen durch den Schlitz nach unten in den Turm und raus durch das Kabelfenster. Beinchen vorher auf Länge kürzen und mit Schrumpfschlauch einzeln isolieren (kein Kurzschluss untereinander oder zum Motor). Der A3144 schaltet nur auf eine Magnetpol-Seite: reagiert er nicht, den Magneten in der Nabe umdrehen (vor dem Einkleben mit dem Sensor prüfen).
- **Versorgung im Test:** Viele DevKits haben keine Trenndiode zwischen USB-5-V und VIN. Solange USB steckt, die 5-V-Leitung vom Mini-360 zum VIN abziehen. Treiber-VDD kommt aus 3V3, deshalb laufen alle Tests auch mit USB-Versorgung und 12 V nur an VMOT. Im Endbetrieb ohne USB versorgt der Mini-360 den ESP32 über VIN.
- **ENABLE beim Booten (optional):** GPIO14 gibt beim Booten kurz Pulse aus, GPIO23 ist dann hochohmig. Mit 10 kΩ von GPIO23 nach 3,3 V bleiben die Treiber sicher aus, bis die Firmware startet. Ohne diesen Widerstand kann der Stößel beim Einschalten kurz zucken.
- **Leitungen:** 12 V und Motoren mit Litze 0,5 mm², Signale mit Dupont. Dupont-Stecker an Motorleitungen nur mit Schrumpfschlauch oder Kabelbinder gegen Abrutschen sichern.

## 5. Inbetriebnahme mit Prüfpunkten

Vor jedem Schritt Spannung aus, Verdrahtung gegen Abschnitt 2 prüfen. Der Reihe nach, nicht überspringen.

1. **Sichtprüfung und Durchgang (alles stromlos, Motoren noch nicht angesteckt).** Kein Durchgang zwischen +12 V und GND, 3V3 und GND, VIN und GND. Elko-Polung richtig. Spulenpaare der Motoren gefunden (Abschnitt 2.3).
2. **Mini-360 einstellen** (Abschnitt 4): nur Mini-360 an 12 V, Ausgang 5,0 V (±0,1 V). Die 5-V-Leitung bleibt danach vom VIN abgezogen, solange USB steckt (Abschnitt 4, Versorgung im Test).
3. **Spannungen.** Netzteil an, Motoren noch nicht angesteckt: +12 V an VMOT beider Treiber (rund 12 V), 3V3 am ESP32 (3,3 V ±0,1 V), 3,3 V an VDD beider Treiber und am HX711-VCC, 5,0 V an VIN und am A3144 Pin 1. Abweichung: sofort abschalten, Fehler suchen.
4. **Vref einstellen** (Abschnitt 3): Motoren stromlos anstecken, 12 V ein, Treiber 1 (Stößel) 0,218 V, Treiber 2 (Karussell) 0,190 V, 12 V aus.
5. **Mikroschalter im Serial-Monitor** (115200 Baud, USB, VIN abgezogen). Kleiner Test-Sketch, nur zum Prüfen:

   ```cpp
   void setup() { Serial.begin(115200); pinMode(18, INPUT_PULLUP); pinMode(19, INPUT_PULLUP); }
   void loop()  { Serial.printf("Schalter=%d Hall=%d\n", digitalRead(18), digitalRead(19)); delay(200); }
   ```

   Erwartet: Schalter offen = 1, Schalter gedrückt (Rollenhebel) = 0. Hall ohne Magnet = 1.
6. **Hall mit Magnet.** Magnet (5 x 2) an die Beschriftungsseite des A3144 halten: Hall = 0, Magnet weg = 1. Bleibt er bei 1, Magnet umdrehen. Bleibt er bei 0, Verdrahtung und Pin 3 prüfen.
7. **HX711 Rohwert** (HX711-Bibliothek, `read()` oder `read_average(10)`): Wägezelle unbelastet liest einen ruhigen Wert (Schwankung nur wenige Zählpunkte). Mit der Hand leicht auf das Lastende drücken oder ein bekanntes Gewicht (z. B. 100 g) auflegen: der Wert ändert sich deutlich und gleichmäßig (grobe Größenordnung einige 10^5 Zählpunkte je 100 g, je nach Zelle). Springt er, fehlt Kontakt an E+/E−/A+/A−. Fällt er statt zu steigen, A+ und A− tauschen oder in der Firmware umkehren.
8. **Motoren trocken.** Zuerst ohne Last: Stößel ohne Spritze, Karussell ohne Spritzen. 12 V ein, ENABLE LOW, Treiber 1 langsam eine Umdrehung (3200 Mikroschritte), dann Treiber 2. Prüfen: Motor dreht sanft, ohne Brummen oder Ruckeln, wird nur handwarm. Richtung falsch: bei stromlosem Zustand ein Spulenpaar (Spule A) am Treiber vertauschen oder DIR in der Firmware drehen. Kein Zittern auf der Stelle (dann ein Kabelpaar falsch gepaart).
9. **Referenzfahrt (`POST /home`).** Stößel fährt hoch bis der Mikroschalter auslöst (Schalter = 0, Motor stoppt), danach dreht das Karussell bis der Hall-Sensor auslöst (Platz 0). Im Notfall `POST /stop`. Dann mit kleinen Beträgen Dosierfahrten ohne Becher prüfen.

## 6. Offene Punkte

- **Sense-Widerstand des gekauften Moduls** ist unbekannt: R068 prüfen, sonst Vref neu rechnen (Abschnitt 3).
- **Stößelkraft:** Der Stößel läuft mit dem Nennstrom 0,4 A (Vref 0,2176 V). Rechnung (Näherung, Wirkungsgrad Trapezspindel mit Messingmutter etwa 0,3 angenommen): 0,28 Nm × 2π × 0,3 / 0,002 m etwa 264 N, das Modell rechnet mit höchstens 250 N. Das Parameterblatt nennt an anderer Stelle bis 0,65 A, das überschreitet Motor und A4988 (0,4 A Nennstrom, 0,5 A Modulgrenze ohne Kühlkörper). Am Gerät die Kraft messen.
- **A3144 an 5 V (geändert):** Das Datenblatt verlangt mindestens 4,5 V, deshalb liegt Pin 1 an der 5-V-Leitung. Der Ausgang ist offener Kollektor, GPIO19 hat den Pullup auf 3,3 V, das ist für den Pin unkritisch. Vertrag und Firmware ändern sich dadurch nicht.
- **Einbau des Hall-Sensors:** Das Parameterblatt (Abschnitt 0a) beschreibt noch einen Pfosten auf dem Tisch bei r 14, dieser Plan folgt der Vorgabe (flach in der Tasche auf dem Turm, Beinchen durch den Schlitz nach unten). Abstimmen mit dem OpenSCAD-Modell.
- **HX711-Abtastrate:** Das Parameterblatt rechnet mit 80 Hz. Viele Module sind ab Werk auf 10 Hz eingestellt (Pad RATE). Prüfen.
- **Aderfarben der Wägezelle** und Polarität des Netzteils (Plus innen) am gekauften Teil prüfen.
