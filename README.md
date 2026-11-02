# Farbmischer

Ein Geschenk: Tischgerät plus Web-App. Sie wählt eine Farbe am Handy (Farbwähler oder Foto antippen), das Gerät dosiert die passenden Mengen aus fünf günstigen Acryl-Grundfarben in einen Becher, sie rührt um. Gemerkte Farben lassen sich später exakt nachmischen.

## Entscheidungen

- Acrylfarbe aus fünf 60-ml-Spritzen: Primär-Cyan, Primär-Magenta, Primär-Gelb, Titanweiß, Schwarz
- Günstige Studienacryl in 500-ml-Flaschen als Vorrat, nachgefüllt wird direkt in die Spritze
- Bauform Turm: Spritzen senkrecht, Düse nach unten, Becher darunter, etwa 20 x 11 cm Stellfläche
- Bedienung nur im Browser, der ESP32 liefert die Seite selbst im WLAN aus
- Gerät dosiert nur, kein Rührwerk
- Elektronik auf einer Trägerplatine von JLCPCB mit gesteckten Modulen, Druckteile aus dem eigenen Drucker

## Aufbau des Repos

| Pfad | Inhalt |
|---|---|
| `web/` | Web-App: Farbwahl, Foto, Rezept, gemerkte Farben, Kalibrierung, Gerätesteuerung |
| `firmware/` | PlatformIO-Projekt für den ESP32 |
| `hardware/` | OpenSCAD-Druckteile des Turms |
| `electronics/` | Generator für die KiCad-Trägerplatine plus Netzliste |

## Stufen

| Stufe | Was | Status |
|---|---|---|
| 0 | Web-App: Farbe wählen, Rezept in Gramm, mit Küchenwaage abwiegen | fertig, getestet |
| 1 | Turm mit fünf Spritzenpumpen am ESP32 | Code, Druckteile und Platine entworfen, nichts davon auf Hardware getestet |
| 2 | Kalibrierung mit Farbsensor | optional |

## Stufe 0: Web-App

1. `mixbox.js` herunterladen und nach `web/` legen. Quelle: Repository `scrtwpns/mixbox` auf GitHub, Datei `javascript/mixbox.js`. Lizenz CC BY-NC 4.0, für ein privates Geschenk in Ordnung, nicht für Verkauf. Die Datei steht in `.gitignore`.
2. `web/index.html` im Browser öffnen. Für das Handy im gleichen WLAN:

```
cd web
python3 -m http.server 8000
```

Dann am Handy `http://<IP des Rechners>:8000` aufrufen.

Funktionen: Farbwähler oder Hex-Wert, Farbe aus einem Foto antippen (Handykamera), Gesamtmenge in Gramm, Rezept mit Vorhersage-Swatch und Abweichung, Farben mit Namen merken und wieder laden, Primärfarben kalibrieren, Gerät steuern.

Die Farbmathematik liegt in `web/farbmath.js`: Mixbox mischt die Primärfarben im Latentraum, ein projizierter Gradientenabstieg sucht die Anteile mit kleinster Lab-Abweichung zur Zielfarbe.

### Primärfarben kalibrieren

Jede Grundfarbe satt auf weißes Papier streichen, trocknen lassen, bei Tageslicht fotografieren, Farbwert mit einer Pipette ablesen und in der App eintragen. Das verbessert die Rezepte deutlich, weil die Standardwerte nur grobe Schätzungen sind.

## Farben kaufen

Fünf Flaschen reichen für alles. Gesucht wird in Studienqualität (Flasche 250 bis 500 ml, meist unter 10 Euro):

| Spritze | Farbe | Suchbegriff beim Händler |
|---|---|---|
| C | Primär-Cyan | Primary Cyan, Primärblau, Cyan |
| M | Primär-Magenta | Primary Magenta, Primärrot, Magenta |
| Y | Primär-Gelb | Primary Yellow, Primärgelb |
| W | Titanweiß | Titanium White |
| K | Schwarz | Ivory Black oder Mars Black |

Nachfüllen: Kolben aus der Spritze ziehen, Farbe aus der Flasche einfüllen, Kolben wieder einsetzen, Düse nach oben, Luft rausdrücken. Flaschenfarbe ist dünner als Tubenfarbe und pumpt sich leichter.

## Stufe 1: Turm

### Mechanik

Fünf Stationen im Abstand von 40 mm. Je Station: 60-ml-Luer-Lock-Spritze senkrecht in einem von vorne offenen Halter, dahinter eine T8-Spindel mit 2 mm Steigung und zwei 8-mm-Linearwellen, NEMA 17 unten im Sockel, Kolbenschlitten mit Arm, der die Kolbenplatte greift, Endschalter oben. Unter den Düsen ein Becherraum von 90 mm. Spritzenwechsel: Schlitten nach oben fahren, Spritze nach vorne herausziehen, neue einschieben.

Druckteile: `hardware/spritzenpumpe.scad`, Variable `teil` auf `sockel`, `schlitten`, `spritzenhalter`, `kopf` oder `alle` setzen und als STL exportieren. Die Datei ist ungerendert entstanden, die nachzumessenden Maße stehen im Kommentarblock am Dateiende. Berechnete Wellen- und Spindellängen gibt OpenSCAD in der Konsole aus.

### Stückliste

| Teil | Menge | Woher |
|---|---|---|
| ESP32 DevKit V1, 30-polig | 1 | Elektronikhändler |
| TMC2209 StepStick (oder A4988) | 5 | Elektronikhändler |
| NEMA 17, 40 mm | 5 | Elektronikhändler, 3D-Druck-Shop |
| T8-Spindel 2 mm Steigung, 200 mm, mit Flanschmutter | 5 | 3D-Druck-Shop |
| Linearwelle 8 mm, 200 mm | 10 | 3D-Druck-Shop |
| LM8UU | 10 | 3D-Druck-Shop |
| Kupplung 5 auf 8 mm | 5 | 3D-Druck-Shop |
| Mikro-Endschalter mit Hebel | 5 | Elektronikhändler |
| Spritze 60 ml Luer-Lock | 5 plus Ersatz | Apotheke |
| Luer-Lock-Verschlusskappen | 10 | Apotheke |
| Netzteil 12 V 3 A mit Hohlstecker, Adapter auf Schraubklemme | 1 | Elektronikhändler |
| Buck-Modul 12 V auf 5 V (z. B. MP1584) | 1 | Elektronikhändler |
| JST-XH-Stecker 4-polig und 2-polig mit Kabel | 5 plus 5 | Elektronikhändler |
| Elko 470 µF und 5 x 100 µF, 25 V, Polyfuse 3 A, Widerstand 10 kOhm | | Elektronikhändler |
| Buchsenleisten 2 x 15 und 10 x 8, Schraubklemmen 5,08 mm 2- und 4-polig | | Elektronikhändler |
| Trägerplatine | 5 Stück (Mindestmenge) | JLCPCB |
| Schrauben M3, Muttern | | Baumarkt |

Grob 150 bis 200 Euro, die Spindeln und Wellen sind der größte Posten. Die Längen von Spindel und Wellen vor der Bestellung aus der OpenSCAD-Konsole übernehmen.

### Bestellung bei JLCPCB

Nur die Trägerplatine. Ablauf:

1. `python3 electronics/generate_pcb.py` ausführen, erzeugt `electronics/farbmixer_traeger.kicad_pcb` (alle Bauteile und Netze, keine Leiterbahnen) und `electronics/NETZLISTE.md`.
2. Datei in KiCad 8 öffnen. Vorher nachmessen: Reihenabstand der DevKit-Pins (im Generator 25,4 mm) und Pinreihenfolge am eigenen DevKit. Beides als Variable am Anfang des Generators.
3. Leiterbahnen ziehen: Route, dann entweder von Hand (etwa 30 Minuten, nur Durchsteckbauteile) oder mit dem Freerouting-Plugin. Für die Motorbahnen und 12 V mindestens 0,8 mm Breite.
4. Design Rules Check, dann Gerber und Bohrdateien exportieren (File, Fabrication Outputs). Als Zip hochladen bei JLCPCB, 2 Lagen, 100 x 100 mm, 1,6 mm, 5 Stück, Rest Standard. Preis grob 2 Dollar plus Versand.
5. Lötjumper nach dem Löten: MS1 und MS2 bei allen fünf Treibern schließen (1/16 Mikroschritt). MS3 und RST-SLP nur bei A4988 schließen, bei TMC2209 offen lassen.

Die Platine ist generiert und nur strukturell geprüft, nicht in KiCad geöffnet. Beim Öffnen auf Fehlermeldungen achten und den Generator anpassen, er ist kurz und kommentiert.

### Verdrahtung

| Signal | GPIO | Hinweis |
|---|---|---|
| STEP C, M, Y, W, K | 13, 14, 27, 26, 25 | |
| DIR C, M, Y, W, K | 33, 32, 4, 16, 17 | |
| ENABLE (alle Treiber) | 23 | LOW = aktiv |
| Endschalter C, M, Y, W | 18, 19, 21, 22 | interner Pullup |
| Endschalter K | 34 | nur Eingang, 10 kOhm Pullup auf der Platine |

Endschalter als Schließer gegen GND. Läuft ein Motor falsch herum, in `firmware/include/config.h` den Eintrag `DIR_INVERT` für die Station auf `true` setzen oder den Motorstecker umdrehen.

### Dosierung

Spritze 60 ml, Innendurchmesser etwa 26,7 mm, ergibt rund 0,56 ml pro mm Kolbenweg. Mit 2 mm Spindelsteigung, 200 Vollschritten und 1/16 Mikroschritt sind das 1600 Schritte pro mm, also etwa 2860 Schritte pro ml. Die kleinste Dosis von 0,1 g entspricht rund 220 Schritten. Dichte von Acrylfarbe etwa 1,2 bis 1,5 g/ml, der Faktor wird pro Station einmal durch Auswiegen bestimmt.

### Firmware bauen und flashen

PlatformIO installieren (`pip install platformio`), dann:

```
cd firmware
cp include/secrets.h.example include/secrets.h   # WLAN eintragen
pio run -t upload                                 # Firmware
./sync_web.sh && pio run -t uploadfs              # Web-App ins LittleFS
pio device monitor                                # IP-Adresse ablesen
```

Danach ist das Gerät unter `http://farbmixer.local` erreichbar. Ohne WLAN-Verbindung öffnet der ESP32 einen eigenen Access Point namens `Farbmixer`.

Die Firmware ist bisher nur mit Stub-Headern auf Syntax geprüft, nicht auf einem ESP32 gelaufen. Beim ersten Start ohne Farbe testen: Referenzfahrt, dann `/prime` mit 1 ml pro Station, Richtung und Weg kontrollieren.

### HTTP-Schnittstelle

Alle Antworten sind JSON. Bewegungen starten sofort und laufen im Hintergrund, `/status` zeigt den Fortschritt.

| Aufruf | Body | Wirkung |
|---|---|---|
| `GET /status` | | `busy`, aktive Station, Fehler, pro Station Position und Restmenge |
| `POST /home` | `{"id":"C"}` oder leer | Referenzfahrt einer oder aller Stationen |
| `POST /prime` | `{"id":"C","ml":2}` | Kolben vorfahren (negativ: zurück), zum Vorfüllen |
| `POST /dispense` | `{"grams":{"C":1.1,"Y":4.2,"W":14.7}}` | Rezept dosieren, Reihenfolge W, Y, C, M, K |
| `POST /stop` | | laufende Bewegung abbrechen |
| `GET /config` | | Kalibrierwerte pro Station |
| `POST /config` | `{"C":{"g_per_ml":1.32}}` | Kalibrierwerte setzen, im Flash gespeichert |

Nach jeder Dosierung zieht der Kolben 0,05 ml zurück, damit nichts nachtropft. Der Betrag wird beim nächsten Hub wieder vorgefahren.

### Gewicht kalibrieren

Pro Station: Becher auf die Waage, tarieren, `/prime` mit 5 ml, Gewicht ablesen. Gewicht geteilt durch 5 ist `g_per_ml`, per `/config` setzen.

### Bekannte Hürde

Acryl härtet an der Düse in Minuten. Düsen nach jeder Session abwischen und mit Luer-Kappen verschließen.

## Offene Punkte

- Platine in KiCad öffnen, routen, DRC
- Druckteile rendern, Probedruck einer Station, Maße nachmessen
- Firmware auf echter Hardware testen, besonders Richtung, Endschalter und Geschwindigkeit bei zäher Farbe
