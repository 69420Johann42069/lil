# Farbmischer

Ein Geschenk: Gerät plus Web-App, das aus fünf Acryl-Grundfarben ein Rezept für eine Wunschfarbe berechnet und die Mengen selbst dosiert. Gemischt wird von Hand.

## Entscheidungen

- Acrylfarbe, fünf Kartuschen: Primär-Cyan, Primär-Magenta, Primär-Gelb, Titanweiß, Schwarz
- Bedienung nur im Browser, keine native App. Der ESP32 liefert die Seite selbst im WLAN aus.
- Gerät dosiert nur, kein Rührwerk
- 3D-Drucker vorhanden, Halter und Gehäuse werden gedruckt

## Aufbau des Repos

| Pfad | Inhalt |
|---|---|
| `web/` | Web-App: Farbwahl, Rezept, Kalibrierung, Gerätesteuerung |
| `firmware/` | PlatformIO-Projekt für den ESP32 |
| `hardware/` | OpenSCAD-Druckteile der Spritzenpumpe |

## Stufen

| Stufe | Was | Status |
|---|---|---|
| 0 | Web-App: Farbe wählen, Rezept in Gramm, mit Küchenwaage abwiegen | fertig, getestet |
| 1 | Fünf Spritzenpumpen am ESP32, Web-App dosiert per HTTP | Code geschrieben, noch nicht auf Hardware getestet |
| 2 | Kalibrierung mit Farbsensor, automatische Korrektur der Primärfarben | optional |

## Stufe 0: Web-App

1. `mixbox.js` herunterladen und nach `web/` legen. Quelle: Repository `scrtwpns/mixbox` auf GitHub, Datei `javascript/mixbox.js`. Lizenz CC BY-NC 4.0, für ein privates Geschenk in Ordnung, nicht für Verkauf. Die Datei steht in `.gitignore`.
2. `web/index.html` im Browser öffnen. Für das Handy im gleichen WLAN:

```
cd web
python3 -m http.server 8000
```

Dann am Handy `http://<IP des Rechners>:8000` aufrufen.

Die Farbmathematik liegt in `web/farbmath.js`: Mixbox mischt die Primärfarben im Latentraum, ein projizierter Gradientenabstieg sucht die Anteile mit kleinster Lab-Abweichung zur Zielfarbe. Die Primärfarben sind im Aufklappmenü kalibrierbar und werden im Browser gespeichert.

### Primärfarben kalibrieren

Jede Grundfarbe satt auf weißes Papier streichen, trocknen lassen, bei Tageslicht fotografieren, Farbwert mit einer Pipette ablesen und in der App eintragen. Das verbessert die Rezepte deutlich, weil die Standardwerte nur grobe Schätzungen sind.

## Stufe 1: Hardware

### Stückliste

| Teil | Menge | Hinweis |
|---|---|---|
| ESP32 DevKit | 1 | WLAN und Bluetooth eingebaut |
| NEMA 17 Schrittmotor | 5 | 40 mm Länge reicht |
| Schrittmotortreiber TMC2208 oder A4988 | 5 | TMC2208 ist leise, Mikroschritt 1/16 einstellen |
| Trapezgewindespindel T8, 2 mm Steigung, 150 mm, mit Flanschmutter | 5 | 2 mm Steigung statt 8 mm für feine Dosierung |
| Spritze 60 ml Luer-Lock | 5 | Standard-Einwegspritze |
| Linearwelle 8 mm, 150 mm, plus LM8UU Lager | 10 | Führung des Kolbenschlittens |
| Kupplung 5 mm auf 8 mm | 5 | Motor auf Spindel |
| Netzteil 12 V, 3 A | 1 | |
| Step-Down 12 V auf 5 V | 1 | für den ESP32 |
| Mikro-Endschalter | 5 | Referenzfahrt am Anschlag |
| Luer-Lock-Verschlusskappen | 10 | gegen Eintrocknen |
| Schrauben M3, Elko 100 µF für die Treiber-Versorgung | | |

Grob 120 bis 180 Euro.

### Druckteile

`hardware/spritzenpumpe.scad`, parametrisch. Variable `teil` am Dateianfang auf `motorhalter`, `kolbenschlitten`, `spritzenhalter`, `grundplatte` oder `alle` setzen und als STL exportieren. Pro Station je ein Motorhalter, Kolbenschlitten und Spritzenhalter, dazu eine Grundplatte. Die Maße der Spritze und der Flanschmutter vor dem Druck an den echten Teilen nachmessen, die Datei ist ungerendert entstanden. Die Liste der nachzumessenden Maße steht im Kommentarblock am Dateiende.

Die Grundplatte für fünf Stationen ist etwa 316 x 264 mm groß und passt auf die meisten Druckbetten nicht. Empfehlung: Lochbild als Vorlage nehmen und die Platte aus Holz oder Acryl zuschneiden, oder stationsweise drucken mit `grundplatte(anzahl=1, becher=false)`.

### Dosierung

Spritze 60 ml, Innendurchmesser etwa 26,7 mm, ergibt rund 0,56 ml pro mm Kolbenweg. Mit 2 mm Spindelsteigung, 200 Vollschritten und 1/16 Mikroschritt sind das 1600 Schritte pro mm, also etwa 2860 Schritte pro ml. Die kleinste Dosis von 0,1 g entspricht rund 220 Schritten, Auflösung ist also kein Problem. Dichte von Acrylfarbe etwa 1,2 bis 1,5 g/ml, der Faktor wird pro Station einmal durch Auswiegen bestimmt (siehe Kalibrierung).

### Verdrahtung

| Signal | GPIO | Hinweis |
|---|---|---|
| STEP C, M, Y, W, K | 13, 14, 27, 26, 25 | |
| DIR C, M, Y, W, K | 33, 32, 4, 16, 17 | |
| ENABLE (alle Treiber) | 23 | LOW = aktiv |
| Endschalter C, M, Y, W, K | 18, 19, 21, 22, 15 | Schließer gegen GND, interner Pullup |

Endschalter sitzt am Motorhalter und wird vom Kolbenschlitten in der hinteren Stellung (Spritze voll aufgezogen) gedrückt. Läuft ein Motor falsch herum, in `firmware/include/config.h` den Eintrag `DIR_INVERT` für die Station auf `true` setzen.

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

Pro Station: Becher auf die Waage, tarieren, `/prime` mit 5 ml, Gewicht ablesen. Gewicht geteilt durch 5 ist `g_per_ml`, per `/config` setzen. Weicht die Menge auch volumetrisch ab (Spritze hat anderen Innendurchmesser), `ml_per_mm` anpassen.

### Bekannte Hürde

Acryl härtet an der Düse in Minuten. Düsen nach jeder Session abwischen und mit Luer-Kappen verschließen. Die Spritzen bleiben geschlossen, nur zum Dosieren öffnen.

## Offene Punkte

- Firmware auf echter Hardware testen, besonders Richtung, Endschalter und Geschwindigkeit bei zäher Farbe
- Druckteile an echten Spritzen und Muttern nachmessen
- Stufe 2 (Farbsensor) nur, wenn die Rezepte ohne Kalibrierung zu weit daneben liegen
