# Farbmischer

Ein Geschenk: Tischgerät plus Web-App. Sie wählt eine Farbe am Handy (Farbwähler oder Foto antippen), das Gerät dosiert die passenden Mengen aus fünf günstigen Acryl-Grundfarben in einen Becher, sie rührt um. Gemerkte Farben lassen sich später exakt nachmischen.

## Entscheidungen

- Acrylfarbe aus fünf 60-ml-Spritzen: Primär-Cyan, Primär-Magenta, Primär-Gelb, Titanweiß, Schwarz
- Günstige Studienacryl in 500-ml-Flaschen als Vorrat, nachgefüllt wird direkt in die Spritze
- Bauform Revolver: runde Säule Ø 170 mm, 48 cm hoch, ein Schrittmotor, Spritzen im handgedrehten Karussell
- Bedienung nur im Browser, der ESP32 liefert die Seite selbst im WLAN aus
- Gerät dosiert nur, kein Rührwerk
- Elektronik auf Lochraster (ein Treiber), Druckteile aus dem eigenen Drucker (Anycubic Kobra 2 Pro)

## Aufbau des Repos

| Pfad | Inhalt |
|---|---|
| `web/` | Web-App: Farbwahl, Foto, Rezept, gemerkte Farben, Kalibrierung, Gerätesteuerung |
| `firmware/` | PlatformIO-Projekt für den ESP32 |
| `hardware/` | Parameterblätter, OpenSCAD-Druckteile und Renderings (aktuell: Revolver) |
| `electronics/` | Generator für die KiCad-Trägerplatine (Fünf-Motor-Variante, beim Revolver nicht nötig) |

## Stufen

| Stufe | Was | Status |
|---|---|---|
| 0 | Web-App: Farbe wählen, Rezept in Gramm, mit Küchenwaage abwiegen | fertig, getestet |
| 1 | Revolver mit einem Motor und Karussell | Konzept, Druckteile und Rendering entworfen, Firmware noch auf fünf Motoren, nichts auf Hardware getestet |
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

## Stufe 1: Revolver (aktuelles Konzept)

Zwei Schrittmotoren, fünf Spritzen in einem Karussell. Der Stößel sitzt fest über der vorderen Station, ein zweiter Motor zentral im Sockel dreht das Karussell direkt über eine Welle in der Mitte. Die Nutzerin wählt die Farbe, das Gerät dreht und dosiert alle Stationen nacheinander, am Ende nimmt sie den Becher heraus und rührt um. Säule Ø 170 mm, 48 cm hoch, Fenster unten vorne für den Becher, Rändelrand des Karussells durch einen Schlitz drehbar. Parameterblatt: `hardware/revolver_parameter.md`, Druckteile: `hardware/revolver.scad`, Rendering: `hardware/rendering_revolver.png`.

Vorbild aus der Recherche: das Hackaday-Projekt If Then Paint nutzt ein Spritzenkarussell mit fester Druckplatte (https://hackaday.io/project/166524). Zwei Lehren daraus: die Druckplatte darf nicht freitragend sein (dort hat sie sich bei 30-ml-Spritzen verbogen), und Acrylfarbe ist thixotrop, also nach dem Dosieren kurz warten, bevor der Stößel hochfährt. Einen Mechanismus, der mit einem Motor dreht und drückt (Malteserkreuz, Klinke), gibt es in der Literatur, aber kein DIY-Beispiel mit Spritzen; deshalb ein zweiter Motor für das Karussell, das ist einfacher und zuverlässiger.

Stößelkraft: NEMA 17 (0,4 Nm) an T8 mit 2 mm Steigung ergibt bei 30 % Wirkungsgrad rund 370 N, ein 60-ml-Kolben braucht bei zäher Farbe deutlich unter 100 N.

### Stückliste Revolver

| Teil | Menge | Woher |
|---|---|---|
| ESP32 DevKit V1 | 1 | Elektronikhändler |
| TMC2209 StepStick (oder A4988) | 2 | Elektronikhändler |
| NEMA 17, 40 mm | 2 | Stößel und Karussell |
| Stahlwelle Ø 8, 180 mm, mit Abflachung | 1 | 3D-Druck-Shop, Antriebswelle Karussell |
| T8-Spindel 2 mm Steigung, 150 mm, mit Flanschmutter | 1 | 3D-Druck-Shop |
| Linearwelle 8 mm, 150 mm, LM8UU | 1 plus 1 | 3D-Druck-Shop |
| Kugellager 608 | 2 | 3D-Druck-Shop |
| Kupplung 5 auf 8 mm | 2 | 3D-Druck-Shop |
| Mikro-Endschalter | 2 | einer oben, einer im Stößelfuß |
| Hall-Sensor A3144 | 1 | Referenz des Karussells |
| Magnet Ø 5 x 2 | 1 | Elektronikhändler |
| Stahlkugeln 6 mm (optional für das Karussell-Lager) | 24 | Baumarkt, Fahrradladen |
| Spritze 60 ml Luer-Lock | 5 plus Ersatz | Apotheke |
| Luer-Lock-Verschlusskappen | 10 | Apotheke |
| Netzteil 12 V 3 A mit Hohlstecker | 1 | Elektronikhändler |
| Buck-Modul 12 V auf 5 V | 1 | Elektronikhändler |
| LED-Ring WS2812 12 LEDs (optional) | 1 | Elektronikhändler |
| Lochrasterplatine, Buchsenleisten, Klemmen | | Elektronikhändler |
| Mischbecher Ø 56, Höhe 60 | 2 | Haushaltswaren |

Grob 80 bis 110 Euro. Die Trägerplatine aus `electronics/` ist für fünf Motoren ausgelegt, beim Revolver werden nur zwei Treiberplätze bestückt; Lochraster geht auch.

### Druckteile

`hardware/revolver.scad`, Variable `teil` für die einzelnen Teile, alle liegend ohne Stützen, höchstens 200 mm hoch für die Kobra 2 Pro (220 x 220 x 250). Ungerendert entstanden, `assert`-Prüfungen und nachzumessende Maße stehen in der Datei. Das ältere Konzept mit fünf Motoren (gerader Turm `spritzenpumpe.scad`, Säule `saeule_parameter.md`) bleibt als Referenz im Repo.

### Verdrahtung Revolver

| Signal | GPIO | Hinweis |
|---|---|---|
| STEP, DIR Stößel | 13, 33 | Treiber 1 |
| STEP, DIR Karussell | 14, 32 | Treiber 2 |
| ENABLE | 23 | beide Treiber |
| Endschalter oben | 18 | Schließer gegen GND, interner Pullup |
| Kontakt-Taster im Stößelfuß | 19 | Schließer gegen GND |
| Hall Referenz Karussell | 21 | digitaler Hall, Pullup |
| LED-Ring | 5 | WS2812 Daten |

### Für die Software-Sitzung

Die Firmware in `firmware/` ist noch für fünf Spritzenpumpen geschrieben. Für den Revolver ändert sich: Motor 1 Stößel, Motor 2 Karussell; Dosierung als Strecke nach Kontakt (Stößel fährt bis der Taster schließt, dann Gramm geteilt durch g_per_ml mal Schritte pro ml, danach 2 Sekunden warten, dann 2 mm hoch, dann ganz nach oben); Karussell referenziert beim Start per Hall-Sensor und fährt dann 40 Vollschritte je Station (Direktantrieb 1:1); vor jedem Drehen muss der Stößel am oberen Endschalter stehen; ein Rezept läuft vollautomatisch alle Stationen ab, am Ende Fertigmeldung und Zielfarbe auf dem LED-Ring. Details in `hardware/revolver_parameter.md`, Abschnitt „Was die Firmware wissen muss“.

### Firmware bauen und flashen

Unverändert, siehe `firmware/` (PlatformIO). Die Kalibrierung per Waage bleibt gleich: 5 ml ausdrücken, wiegen, `g_per_ml` setzen.

### Bekannte Hürde

Acryl härtet an der Düse in Minuten. Düsen nach jeder Session abwischen und mit Luer-Kappen verschließen. Die vier inaktiven Düsen tropfen in die Abtropfschale im Sockel, die sich herausnehmen und abwaschen lässt.

## Offene Punkte

- Druckteile des Revolvers in OpenSCAD rendern, eine Station probeweise drucken, Spritzenmaße nachmessen
- Firmware auf zwei Motoren (Stößel, Karussell) und Kontakt-Dosierung umstellen (Software-Sitzung)
- Karussell-Lagerung testen: Gleitlager PETG auf PETG oder Stahlkugeln in der Rille, Reibung muss unter dem Motormoment bleiben
- Erster Hardwaretest ohne Farbe: Referenzfahrten beider Motoren, Kontakt-Taster, 40 Schritte je Station prüfen
