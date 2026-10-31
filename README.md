# Farbmischer

Ein Geschenk: Gerät plus Web-App, das aus fünf Acryl-Grundfarben ein Rezept für eine Wunschfarbe berechnet und die Mengen später selbst dosiert. Gemischt wird von Hand.

## Entscheidungen

- Acrylfarbe, fünf Kartuschen: Primär-Cyan, Primär-Magenta, Primär-Gelb, Titanweiß, Schwarz
- Bedienung nur im Browser, keine native App. Der ESP32 liefert die Seite später selbst im WLAN aus.
- Gerät dosiert nur, kein Rührwerk
- 3D-Drucker vorhanden, Halter und Gehäuse werden gedruckt

## Stufen

| Stufe | Was | Status |
|---|---|---|
| 0 | Web-App: Farbe wählen, Rezept in Gramm, mit Küchenwaage abwiegen | fertig, siehe `web/` |
| 1 | Fünf Spritzenpumpen am ESP32, Web-App sendet Rezept per HTTP | offen |
| 2 | Kalibrierung mit Farbsensor, automatische Korrektur der Primärfarben | optional |

## Stufe 0 starten

1. `mixbox.js` herunterladen und nach `web/` legen. Quelle: Repository `scrtwpns/mixbox` auf GitHub, Datei `javascript/mixbox.js`. Lizenz CC BY-NC 4.0, für ein privates Geschenk in Ordnung, nicht für Verkauf.
2. `web/index.html` im Browser öffnen. Für das Handy im gleichen WLAN:

```
cd web
python3 -m http.server 8000
```

Dann am Handy `http://<IP des Rechners>:8000` aufrufen.

Die Farbmathematik liegt in `web/farbmath.js`: Mixbox mischt die Primärfarben im Latentraum, ein projizierter Gradientenabstieg sucht die Anteile mit kleinster Lab-Abweichung zur Zielfarbe. Die Primärfarben sind im Aufklappmenü kalibrierbar und werden im Browser gespeichert.

### Kalibrieren

Jede Grundfarbe satt auf weißes Papier streichen, trocknen lassen, bei Tageslicht fotografieren, Farbwert mit einer Pipette ablesen und in der App eintragen. Das verbessert die Rezepte deutlich, weil die Standardwerte nur grobe Schätzungen sind.

## Stufe 1: Hardware

### Stückliste

| Teil | Menge | Hinweis |
|---|---|---|
| ESP32 DevKit | 1 | WLAN und Bluetooth eingebaut |
| NEMA 17 Schrittmotor | 5 | 40 mm Länge reicht |
| Schrittmotortreiber TMC2208 oder A4988 | 5 | TMC2208 ist leise |
| Trapezgewindespindel T8, 2 mm Steigung, 150 mm, mit Mutter | 5 | 2 mm Steigung statt 8 mm für feine Dosierung |
| Spritze 60 ml Luer-Lock | 5 | Standard-Einwegspritze |
| Linearwelle 8 mm plus LM8UU Lager | 10 | Führung des Kolbenschlittens, alternativ gedruckte Gleitführung |
| Kupplung 5 mm auf 8 mm | 5 | Motor auf Spindel |
| Netzteil 12 V, 3 A | 1 | |
| Step-Down 12 V auf 5 V | 1 | für den ESP32 |
| Endschalter | 5 | Referenzfahrt am Anschlag |
| Luer-Lock-Verschlusskappen | 10 | gegen Eintrocknen |

Grob 120 bis 180 Euro.

### Druckteile

- Spritzenhalter mit Flanschaufnahme, fünfmal
- Kolbenschlitten mit Spindelmutter, fünfmal
- Motorhalter NEMA 17 mit Endschalteraufnahme, fünfmal
- Grundplatte mit fünf Stationen nebeneinander und Becherstellplatz darunter
- Elektronikbox für ESP32 und Treiber

### Dosierung

Spritze 60 ml, Innendurchmesser etwa 26,7 mm, ergibt rund 0,56 ml pro mm Kolbenweg. Mit 2 mm Spindelsteigung und 200 Vollschritten pro Umdrehung sind das etwa 0,0056 ml pro Vollschritt, also weit unter der benötigten Auflösung von 0,1 ml. Dichte von Acrylfarbe etwa 1,2 bis 1,5 g/ml, der Faktor wird pro Kartusche einmal durch Auswiegen bestimmt.

### Firmware-Schnittstelle

Die Web-App sendet pro Rezept einen Aufruf:

```
POST /dispense
Content-Type: application/json

{ "total_g": 20, "grams": { "C": 1.1, "M": 0.0, "Y": 4.2, "W": 14.7, "K": 0.0 } }
```

Antwort: Text `ok` oder Fehlermeldung. Weitere Endpunkte für Stufe 1: `POST /home` für die Referenzfahrt, `POST /prime` zum Vorfüllen einer Station, `GET /status`.

Die Firmware rechnet Gramm über den Dichtefaktor in Schritte um, fährt die fünf Stationen nacheinander an und zieht nach jedem Hub den Kolben einen kleinen Betrag zurück, damit nichts nachtropft.

### Bekannte Hürde

Acryl härtet an der Düse in Minuten. Düsen nach jeder Session abwischen und mit Luer-Kappen verschließen. Die Spritzen bleiben geschlossen, nur zum Dosieren öffnen.

## Offene Punkte

- Zeit bis zum Geburtstag entscheidet, ob Stufe 1 rechtzeitig fertig wird. Stufe 0 ist bereits ein brauchbares Geschenk.
- Erfahrung mit ESP32 und Schrittmotoren noch unklar.
