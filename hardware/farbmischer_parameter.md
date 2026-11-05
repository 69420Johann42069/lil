# Farbmischer Stand 8 (Grundlage Stand 6): maßgebliches Parameterblatt

Dieses Blatt ist ab Stand 5 (hier Stand 6) die einzige Vorlage für Rendering, OpenSCAD-Druckteile, Stückliste, Verdrahtung und Firmware. Es ersetzt `hardware/revolver_parameter.md` (Stand 4). Rendering und Prüfskript (`hardware/render_farbmischer.py`, Aufruf mit `--pruefung`) und `hardware/farbmischer.scad` folgen diesem Blatt. Die README ist auf Stand 6 nachgezogen, die Netzliste (`electronics/`) gehört noch zum Fünf-Motor-Entwurf und ist für dieses Gerät nicht maßgeblich. Die Ordner `web/` und `firmware/` gehören einer anderen Sitzung, Abschnitt 14 ist nur ein Hinweis an sie.

**Kurz:** Ein schwarzer Flakon mit Goldlinien, Körper Ø 196 mm, Fuß und Krone Ø 204, 407 mm hoch. Innen stehen sechs 60-ml-Spritzen senkrecht in einem Karussell (Cyan, Magenta, Gelb, zweimal Titanweiß, Schwarz). Ein fester Stößel in der Gerätemitte drückt über einen Ausleger die Spritze, die vorne steht. Eine Wägezelle unter dem Becher misst in Gramm. Sie wählt die Farbe im Handy-Browser, das Gerät dosiert alles allein, sie zieht die Schublade auf und nimmt den Becher. Zwei Motoren, sechs Fenster, ein Goldband, ihr Name in der Krone. **Stand 6: ohne Licht und fast vollständig aus PETG gedruckt.** Kaufteile sind nur noch Motoren, Elektronik, Wellen, Spindel, Lager, Riemen, Gewindestangen, Schrauben, Magnete, Silikonteile und das Spritzenzubehör.

Alle Maße in mm, Winkel in Grad, Massen in g, Preise in Euro (Stand Herbst 2026). Höhenkette und alle Kollisionen rechnet `python3 hardware/render_farbmischer.py --pruefung` (Exit-Code 1 bei einem Fehler). Die Werte in Abschnitt 15 sind dessen Ausgabe. Die Druckteile in `hardware/farbmischer.scad` haben eigene `assert`-Prüfungen (Höhenkette, Passungen, Druckbett, Ausleger-Spannung); alle Teile und die Montage rechnen fehlerfrei durch (OpenSCAD 2021.01). Die Kraft- und Massenrechnungen in Abschnitt 16 sind für Stand 6 nachgerechnet, wo sich Maße geändert haben.

## 0. Änderungen in Stand 6 (druckbar aus PETG, ohne Licht)

Wunsch: die Funktion bleibt, das Gerät bleibt schön, aber fast alles soll sich 3D-drucken lassen, die LEDs entfallen, gedruckt wird mit PETG. Höhe, Durchmesser, Karussell, Stößel, Waage, Schublade und alle Kollisionsmaße bleiben unverändert, nur Teile und Oberflächen ändern sich.

| Was | Stand 5.1 | Stand 6 | Folge |
|---|---|---|---|
| Licht | 99 WS2812 (Bühnenring, Vitrinen-LEDs, Lichtfuge), 74AHCT125, 1000 µF, 5-A-Wandler | **entfällt komplett**, auch LED-Träger, LED-Ringhalter, Laufring-Nut, Opalfenster, GPIO 25 | 15 Euro weniger Elektronik, drei Druckteile weniger. Fortschritt und „Fertig“ zeigt nur die App (optional ein Piezo-Summer) |
| Lichtfuge (Z 338 bis 341) | Opalring, leuchtet | **Goldband**, Gold-PETG | Die waagrechte Goldlinie am Hals bleibt, sie leuchtet nicht |
| Hülle | PLA, Füller, Schliff, Lack hochglanz und seidenmatt | **PETG direkt gedruckt**, nichts gespachtelt, nichts lackiert | Sockel und Front glänzen vom Filament, Körper und Krone matt (Matt-PETG oder 0,2 mm). PETG lässt sich kaum schleifen, deshalb ist die Oberfläche das Druckbild |
| Körperteilung Z 235 | verklebt, gespachtelt, überlackiert, unsichtbar | **gewollte Schattenfuge** 1,0 breit, 0,5 tief (zwei Fasen 0,5 x 45 Grad) | die einzige Stelle, wo man die Teilung sieht, als saubere Linie |
| Gold | Anreibewachs und Lackmarker auf erhabenen Linien | **gedruckte Gold-PETG-Teile**: Goldring, Goldband, Kronenring (Fase), Portalrahmen in drei Leistenarten, Goldlippe, Buchsenring, Namensschild-Schrift | kein Wachs, keine Maske. Rahmenleisten werden flach in der Abwicklung gedruckt und um die Hülle gebogen aufgeklebt |
| Portalscheibe | Rauchacryl 2 mm, 78 x 234 | **Rauch-PETG 2 mm**, zwei Hälften mit Überlappung hinter der Karussellplatte (Bett 220 x 220 erlaubt 234 am Stück nicht) | eine Haarlinie bei Z 215 vor der schwarzen Platte |
| Fensterscheiben | Rauchacryl 2 mm | **Klar-PETG 1,6 mm** | ohne Licht gibt es keinen Grund mehr, abzudunkeln. Bleibt das Druckbild zu trüb, die Scheiben weglassen (Fenster 22 breit, Spritzen sind dann offen) |
| Ausleger | Winkelstahl 40 x 40 x 4 mit Stempelscheibe | **ein PETG-Teil**: Platte 8, Arm 8 dick, Stempelfuß Ø 25, zwei Rippen, liegend gedruckt | Spannung 16 MPa bei 250 N (Grenze 20), Zug am oberen M4-Einsatz 195 N. Entfällt: Winkelstahl, Stempelschraube |
| Podest | opal | schwarz | |
| Schublade | PETG natur mit Opalfenster | **PETG weiß**, ohne Fenster | der Becher steht auf Weiß, die Farbe lässt sich ohne Licht beurteilen |
| Stationskennung | Lackmarker-Ring in Stationsfarbe | **Buchstabe C, M, Y, W, K, W** 0,6 tief neben jeder Tasche | |
| Kosten | Gerät 210 Euro | **Gerät etwa 160 Euro** (Abschnitt 13) | |

Was dabei bewusst schwächer wird: Ohne Licht sind die Farben in den sechs Fenstern nur bei Tageslicht oder Raumlicht zu sehen. Dafür sind die Fenster klar statt rauchgrau. Die Bühne ist nicht mehr beleuchtet, der Becher ist weiß hinterlegt. Der Körper hat jetzt sichtbare Schichtlinien (0,16 mm), die matt-schwarze Hülle verbirgt sie weitgehend.

## 0a. Stand 7 Budget und Stand 8 (aktueller Standard in `farbmischer.scad`, `budget = 1`)

**Stand 8, Karussell direkt am Motor:** Motor 2 (NEMA 17, 34 mm, derselbe wie der Stößel) steht mit der Welle nach oben mittig in einem gedruckten Kasten, dem Motorturm (außen 50,4 x 50,4, Wand 3, Z 7 bis 202, Tisch 2,5 mit Zentrierbund Ø 22,5 und vier M3 von oben, Kabelfenster unten in der -Y-Wand, Aufnahmerahmen in der Grundplatte, Turm wird aufgeklebt). Die Welle (Ø 5, D-Fläche, 22 mm angenommen) steckt in der Nabe der Karussellplatte (Sackloch, Madenschraube M3). Die Platte läuft unverändert mit den sieben Rollenböcken auf dem Laufring, die Welle trägt kein Gewicht. Hall-Sensor: Pfosten auf dem Tisch bei r 14, Magnet 5 x 2 in der Nabenunterseite. Entfallen sind Lagerbock, Karussellwelle Ø 8 x 212, 70-Z-Rad, Motor-2-Winkel, Hallhalter, Riemen 210 mm, eine Riemenscheibe, zwei Stellringe, drei 608-Lager und der Pancake-Motor. Offene Punkte: Wellenlänge und D-Fläche des gekauften Motors messen, Drehmoment 0,28 Nm statt 0,45 Nm am Rad (Test), Firmware mit Übersetzung 1 statt 3,5 (3200 Schritte je Umdrehung bei 1/16 Schritt), Kollisionsprüfung der Montage und Abschnitt 15 sind für Stand 8 nicht neu gerechnet. Die Beschreibung von Riemen, Lagerbock und 70-Z-Rad in den späteren Abschnitten gilt nur für Stand 6 und 7.

Wunsch: so billig wie möglich, viele Teile weglassen. Von außen bleibt Stand 6 unverändert: Portalscheiben, Fensterscheiben, Goldrahmen, Goldlippe und Buchsenring sind gedruckt und kosten nur Filament (Schalter `scheiben = 1`); die Scheiben werden geklebt statt über vier Magnete gehalten (`budget = 1` lässt die Magnettaschen weg). Stand 7 druckt außerdem die Linearlager (Gleitzonen im Schlitten, kein LM10LUU) und nimmt M4-Kernlöcher ohne Gewindeeinsätze; die Ballastbecher werden gratis mit Schrauben und Muttern aus dem Arbeitsvorrat gefüllt (Ø 38, 7 x 3 mm je Becher, etwa 0,4 kg). Gegenüber Stand 6 entfallen Feuchtrinne mit Deckel, Säulen und Abstreifhalter (und mit ihnen Silikonlippen und Schwamm), Spritzenablage, Einführzunge, Kabelclips, der Reed-Kontakt und der Ballast. Treiber wahlweise A4988 statt TMC2209. Druckteile 30 statt 33 Zeilen, Filament zählt nicht mit (netto etwa 1,45 kg), Gerät etwa 83 Euro, mit Startpaket und Farbe etwa 164 Euro, ohne Filament (Standard-Schrauben, Muttern, Scheiben und Kleber kommen aus dem Arbeitsvorrat bzw. gratis) (Details, Quellen und Schätzungen in `hardware/einkaufsliste.md`). `budget = 0` stellt Stand 6 her. Die Abschnitte 1 bis 20 dieses Blattes sind auf Stand 8 nachgezogen, wo Stand 6 abweicht, steht „Stand 6:" daneben. Rendering und Prüfskript (`render_farbmischer.py`, 56 Prüfungen) laufen auf Stand 8, die Tabelle in Abschnitt 15 zeigt noch die 50 Prüfungen von Stand 6.

**Folgen:** Portal und Fenster sind mit gedruckten Scheiben geschlossen. Ohne Feuchtrinne trocknen die Düsen an: Ventiltest (17.2) ist Pflicht, vor jeder Session Düsen wischen. Der Ballast (0,4 statt 0,48 kg Schrauben und Muttern aus dem Arbeitsvorrat) hält die Kippkraft nahe 7 N (Schwerpunkt etwa Z 195, Schätzung). Mit A4988 entfallen UART und StallGuard: Strom per Poti (Stößel 0,5 A), kein Überlastschutz.

## 0b. Änderungen in Stand 5.1 (Abnahme durch die vier Rollen, zur Information)

| Befund | Änderung |
|---|---|
| Zuganker r 92: Karosseriescheibe Ø 20 reicht bis r 102, Mutter bis r 96,6, Körperwand innen r 96,4 (alle vier Rollen) | Zuganker auf r 90,5, Muttern M5 in Sechskanttaschen mit Schlüsselfläche außen (r 94,5), Scheiben Ø 20 und Kontermuttern entfallen, Schraubensicherung. Rollenböcke außen als Bogen r 85,5, Karussellplatte Ø 171. Prüfungen 45 bis 47 neu |
| Zuganker bei ± 148 stehen 6 Grad neben Fenster 3 und 4 und wären im Fenster sichtbar (Künstlerin, SCAD) | Zuganker hinten auf ± 128,6, genau zwischen zwei Fenstern. Ballast neu verteilt (Prüfung 48 und 49) |
| Sockelschale Ø 214 und Grundplatte Ø 210 über der Druckgrenze von etwa 200, Verzugsgefahr am Bettrand (Designerin, Ingenieur) | Fuß Ø 204, Kegel auf Ø 196 (2,4 Grad), Grundplatte Ø 200, Füße auf r 92. Größtes Teil jetzt Ø 204 mit 8 mm Rand |
| Lichtfuge: 36 LED aus 600 mm Streifen passen nicht auf 546 mm Umfang, Punkte statt Band (Designerin, Ingenieur) | 75 LED aus einem Streifen 144/m auf r 83,5, 11,3 mm vor einem 1,2 mm Opalring mit matter Innenseite, Verhältnis Abstand zu Teilung 1,6. Musterstück vor dem Hüllendruck |
| Oberes Ende der Höhenkette: Rippen durchdringen den Deckel, GT2-Scheibe 16 hoch ragt 7 mm über die Krone, Führungswellen hängen nicht in der Brücke (Ingenieur) | Kronendeckel bei 404,8 bis 406,8 (Höhe 406,8 statt 399,3), GT2-Scheiben in voller Kaufhöhe, Rippen 12 hoch, Führungswellen 170 lang, 14,3 eingespannt in Brücke und Klemmnabe |
| Ausleger greift nur 4 bis 6 mm in die Schlittennut (Ingenieur) | Winkelstahl 40 x 40 x 4, senkrechter Schenkel mit 2 x M4 bei 34 mm Hebel auf eine ebene Schlittenfläche geschraubt, Nachweis in Abschnitt 16 |
| Flansch 32 breit über Schlitz 32 breit trägt nur innen (Umsetzung) | Stempel 4 mm innen von der Spritzenachse (X 53), die Kraft liegt innerhalb der Auflage (Prüfung 51) |
| Zylinderschlitz-Steg 6,75 im Blatt, Skript 17,46 (Künstlerin, Controllerin) | 17,5 ist richtig (Halbkreisende R 16), 6,75 galt für ein eckiges Ende. Abschnitt 15 jetzt direkt aus dem Skript |
| Laufring liegt als schwarzes Band im Fenster, Farben hinter Rauchglas zu dunkel (Umsetzung, Künstlerin) | Fenster Z 108 bis 180 ganz unter dem Laufring, zwei Vitrinen-LEDs je Fenster unter dem Laufring |
| LED-Ring 3 dick, HX711 an 5 V, Kontaktschwelle 0,05 g, Spindelspiel, Wägeluft ohne Einstellmaß, Bechersitz zu weit, Pflege alle 7 Tage, Gold als Lackmarker, Hochglanzkrone, Gravur im ersten Layer (Kleinigkeiten) | Podest 1,6 dick (0,7 Luft), HX711 an 3,3 V, Schwelle 0,2 g mit Zeitkriterium, Rückhub 1,3 und Anfahrt von oben, Kufenluft 0,5 ± 0,2 mit Beilagen, konischer Sitz, Rinnendeckel (Ziel 4 Wochen), Gold-Anreibewachs, Krone seidenmatt, Namensschild als Einlage |
| Kosten: Spritzen 1,30 zu optimistisch, Sparpfad-Summe falsch, Druckzeit zu knapp, Verschleiß fehlt (Controllerin) | Spritzen 2,00, Summen neu, Druckzeit 90 bis 130 h, Verschleißsatz 15 Euro in den laufenden Kosten |

## 1. Grundlage und Entscheidungen

**Basis.** Bewertung der vier Rollen nachgezählt: Flakon 6 (Konzept 1) 8 + 8 + 7 + 7 = 30, Farbspieluhr (Konzept 2) 7 + 6,5 + 5 + 8 = 26,5, Atelier-Flakon (Konzept 3) 5 + 7,5 + 4,5 + 5 = 22. Die automatische Zählung stimmt. Basis ist Konzept 1, ergänzt um die besten Ideen aus 2 und 3 und mit allen Punkten unter „Ändern“ eingearbeitet.

**Fehler in Konzept 1, die hier behoben sind:**

| Fehler in Konzept 1 | Folge | Lösung Stand 5 und 5.1 |
|---|---|---|
| Hub 90 mm zwischen leer und voll ist nur 50 ml, nicht 60 ml (1 ml = 1,786 mm bei Innen-Ø 26,7) | Höhenkette falsch oder Spritze nicht voll | Nutzfüllung ehrlich 50 ml, Füllmarke auf jeder Spritze, Hub 89,3 mm plus 10 mm Reserve |
| Drei feste Rollen laufen unter einer Platte mit sechs radialen Schlitzen 32 breit | Rollen fallen beim Drehen in die Schlitze, Platte kippt | Sieben Rollen sitzen an der Platte zwischen den Schlitzen und laufen auf einem festen Laufring, der nur vorne (± 15 Grad) für die Entnahme offen ist |
| T8 mit 4 mm Steigung als selbsthemmend angegeben | Steigungswinkel 10,3 Grad über dem Reibwinkel 8,8 Grad, Schlitten kann bei stromlosem Motor absinken | T8 mit 2 mm Steigung, 5,2 Grad, selbsthemmend |
| Zwei LM8UU je Welle mit 40 Abstand passen nicht in einen 50 hohen Schlitten | Maße widersprechen sich | Je Welle ein LM10LUU (55 lang) auf Wellen Ø 10, Schlitten 58 hoch (ab Stand 7 statt der LM10LUU zwei gedruckte Gleitzonen von je 14 im Schlitten, Bohrung Ø 10,4 auf der Welle Ø 10, der Schlitten bleibt 58 hoch) |
| Stationen in Ruhe stehen über dem Becher, keine feuchte Parkstellung | Düse über dem Becher trocknet und tropft | Sieben Plätze, Platz 0 bleibt leer und steht in Ruhe über dem Becher, die sechs Düsen parken über einer feuchten Rinne |
| Flanschtaschen 46 x 33 tangential nur 0,57 Steg | Platte bricht an den Taschen | Taschen radial lang, Innenecken R 5, Steg 3,1, Schlitzsteg 17,5 |

**Zielkonflikte und Entscheidungen:**

| Konflikt | Entscheidung | Grund |
|---|---|---|
| Ventil allein (Konzept 1) oder Feuchtparken (Ingenieur, Konzept 3) | beides: Entenschnabelventil auf jeder Düse und Parken über einer Feuchtrinne mit Schwammstreifen | Der Ingenieur verlangt, dass die Rückfallebene gleich mitgeplant wird. Ein siebter, leerer Platz im Karussell macht die Parkstellung ohne Zusatzmotor möglich. Ein Deckel mit sechs Löchern über der Rinne senkt die offene Schwammfläche auf ein Sechstel, Ziel 4 Wochen je Wasserfüllung (am Prototyp prüfen) |
| Rücksaugen mit Magnet oder Gabel (Ingenieur, Konzept 2 und 3) gegen einfache Mechanik | kein Rücksaugen, nur Druckentlastung durch 1 mm Rückhub | Magnet reißt den Kolben mit oder rutscht ab (Kolbenreibung 5 bis 15 N gegen Haftkraft 20 bis 30 N), die Gabel braucht exakte Buchführung der Halshöhen und quetscht bei Fehlern. Das Ventil schließt bei Druckabfall von selbst |
| Höhe deutlich unter 400 (Künstlerin) gegen 50 ml Vorrat, Waage und 10 mm Reserve (Ingenieur) | 406,8 | Weniger geht nur mit 30-ml-Spritzen (doppelt so oft tauschen), ohne Waage oder mit abgedrehten GT2-Naben. Die 7,5 mm über Stand 5 kommen von der GT2-Scheibe, die als Kaufteil 16 hoch ist (Stand 5 hatte nur den Zahnkranz gerechnet). Gegenüber Stand 4 sind es 73 mm weniger, Höhe zu Durchmesser 2,0 statt 2,8 |
| Drei Rollen (Kosten) gegen Kugelring oder 6808 (Ingenieur) | sieben 608 als Laufrollen an der Platte, fester Laufring mit Höhenbeilagen | Drei Rollen fallen in die Entnahmelücke. Sieben kosten 2,80 Euro. 6808 auf einer Hülse bleibt die Rückfallebene |
| Wellen Ø 8 (Konzept 1) gegen Ø 10 (Ingenieur) | Ø 10 mit LM10LUU (ab Stand 7 ohne Linearlager, Gleitzonen im Schlitten) | Stempel senkt sich 0,24 statt 0,58 mm, Mehrkosten etwa 4 Euro |
| Kosten 175 bis 185 (Controllerin) gegen Waage, Feuchtrinne (Stand 6: ohne Lack und Licht) | Stand 6: Gerät, Startpaket und Farbe in Abschnitt 13 ehrlich ausgewiesen | Mit Stand 6 entfallen Lack, Füller, Licht und Rauchacryl, das Gerät wird billiger als gefordert. Gespart wird bei Platine, Kupplungen, Reservespritzen |
| Schlüssellochfenster (Konzept 1) gegen einheitliches Motiv (Designerin) | ein Portal vorne als Rechteck mit großen oberen Radien, sechs schmale Rundbogenfenster | Die Entnahme braucht eine durchgehende Öffnung von der Bühne bis zur Kolbenplatte. Ohne 45-Grad-Schräge lässt sie sich spachteln und lackieren |
| Schublade (Konzept 1 und 3) gegen direkter Griff (Konzept 2, Ingenieur) | Schublade, die geschlossen lose auf dem Wägepodest liegt | Die Künstlerin will kein Fischen im Loch. Der Ingenieur verlangt, dass die Führung nicht auf der Waage liegt: Die Laufschienen senken sich auf den letzten 5 mm um 1 mm ab, die geschlossene Schublade ruht nur auf dem Podest |
| Gold: Anreibewachs (Stand 5.1) gegen gedruckt (Stand 6) | Gold-PETG als eigene Teile: Ringe flach, Rahmenleisten flach in der Abwicklung, danach geklebt | PETG nimmt Füller, Schliff und Lack schlecht an, Anreibewachs braucht eine geschliffene Fläche. Gedruckte Goldteile sind sauber kantig, brauchen keine Maske und kein Nacharbeiten. Seidige Gold-PETG-Sorte nehmen (Silk), die Teile sind klein. Messingband 4 mm bleibt Rückfallebene für den Rahmen |
| Becher 60 ml (Kosten) gegen 50 bis 100 ml Mischungen (Künstlerin) | Portionsbecher 60 ml mit Deckel im 100er-Pack, Mischmenge bis 50 g, für mehr „Nochmal“ in der App | Ein höherer Becher kostet Gerätehöhe, ein breiterer passt nicht in die Schublade. 50 g Farbe sind etwa 38 ml und füllen den Becher zu zwei Dritteln, Rühren mit Pinsel geht. 100 ml sind zwei gleiche Läufe |
| Gleiche Motoren (Konzept 2) gegen Pancake (Kosten) | **Stand 8: zwei gleiche NEMA 17 (34 mm), Karussell direkt am Motor 2** (Stand 5 bis 7: Karussell Pancake 23 mm mit 1 : 3,5, Stößel NEMA 17 34 mm) | Mit 1 : 3,5 braucht das Karussell 0,018 Nm am Motor. Der Pancake liefert bei 0,4 A etwa 0,05 Nm, Reserve etwa 2,8-fach, bei 0,6 A etwa 4-fach. Der kurze Stößelmotor reicht für 150 N. Stand 8: ohne Getriebe braucht die Platte 0,062 Nm direkt am Motor, der 34-mm-Motor hat etwa 0,28 Nm Haltemoment (Reserve 4,5-fach gegen das Haltemoment, Abschnitt 16), ein zweiter gleicher Motor spart Riemen, 70-Z-Rad, Lagerbock und Welle |

## 2. Koordinatensystem und Konventionen

| Begriff | Festlegung |
|---|---|
| Ursprung | Gerätemitte auf der Tischplatte, Z = 0 ist die Tischfläche |
| +X | nach vorne, zur Nutzerin (Mitte des Portals und der Schublade) |
| +Y | von vorne gesehen nach rechts |
| +Z | nach oben |
| Winkel θ | in der Draufsicht von +X aus gegen den Uhrzeigersinn (von oben gesehen), also von vorne gesehen zur rechten Seite hin positiv. 0 Grad vorne, 90 Grad rechts, 180 Grad hinten |
| Platzteilung | 360 / 7 = 51,4286 Grad. Plätze p = 0 bis 6 im Karussell, Platz 0 ist leer |
| Karussellwinkel φ | Drehung des Karussells gegen die Ruhelage. In Ruhe (Park) ist φ = 0, Platz p steht dann bei θ = p · 51,43 |
| Aktive Station | die Station bei θ = 0 unter dem Stempel und über dem Becher |
| Stationsradius | 57,0 (Spritzenachse) |
| Stempelhöhe S | Z der Stempelunterkante |
| Toleranz | Maße ohne Angabe ± 0,3, Passungen siehe Bauteil. Druckteile mit 0,2 Spiel je Seite an Steckstellen |

## 3. Hauptmaße und Höhenkette

**Außenmaße:** Fußkante Ø 204, größter Durchmesser 204 (Fuß und Krone), Goldring Ø 202, Körper Ø 196, Höhe 406,8. Kein Druckteil ist größer als Ø 204. Masse Stand 6 etwa 3,8 kg mit 0,48 kg Ballast, Schwerpunkt etwa Z 190. Stand 8: etwa 3,7 kg mit etwa 0,4 kg Ballast, Schwerpunkt höher, etwa Z 195 (Motor 2 sitzt bei Z 165,5 bis 199,5; beides Schätzung, nicht gewogen, Abschnitt 16).

| Z | Element |
|---|---|
| 0 bis 3 | sechs Silikonfüße Ø 12 x 3 auf Radius 92 bei θ = 30 + 60 k, Unterkante Sockelschale schwebt 3 mm über dem Tisch (Schattenfuge) |
| 3 bis 7 | Grundplatte Ø 200 x 4 (Rippen nach oben bis Z 15), trägt alles im Sockel und die vier Zuganker |
| 7 bis 28 | Ballast, vier Stapel in den Bechern Ø 38 der Grundplatte: Stand 8 etwa 0,4 kg Schrauben, Muttern und Scheiben aus dem Arbeitsvorrat (gratis, je Becher bis Z 28 gefüllt), Stand 6 sieben Scheiben M20 je Stapel |
| 7 bis 205,5 | Motorturm (Stand 8): Kasten 50,4 x 50,4, Wand 3, auf den Aufnahmerahmen der Grundplatte geklebt, Tisch Z 199,5 bis 202 (2,5 dick), Hallpfosten bei r 14 bis Z 205,5 |
| 7,5 bis 20,2 | Wägezelle 500 g, 80 x 12,7 x 12,7, liegt entlang Y bei X 57 |
| 20,2 bis 24,4 | Podeststiel Ø 14 (die 3 mm Platz des früheren LED-Rings bleiben frei) |
| 24,4 bis 26,0 | Podestscheibe Ø 60 x 1,6 aus PETG schwarz auf Stiel Ø 14 |
| 26,0 bis 27,5 | Schubladenboden aus PETG weiß (liegt geschlossen auf der Podestscheibe) |
| 27,5 | Becherboden |
| 60,5 | Becherrand (Portionsbecher 60 ml, oben Ø 62, unten Ø 47, 33 hoch) |
| 54 bis 65,2 | Feuchtrinne mit Deckel (Z 64 bis 65,2, sechs Löcher Ø 14), Schwamm nass in den Löchern bis 65,5 (entfällt ab Stand 7) |
| 60 bis 68,5 | Abstreiflippen bei θ ± 40 (entfallen ab Stand 7) |
| 67,5 | Ventilspitze, 7,0 über dem Becherrand |
| 77,5 | Spritzenspitze (Ende Katheterkonus) |
| 97,5 bis 219,5 | Spritzenzylinder Ø 30 |
| 97 bis 101 | Goldring außen (Gold-PETG, eigenes Teil auf dem Sockel) |
| 108 bis 180 | Seitenfenster (ganz unter dem Laufring), Klar-PETG 1,6 dahinter |
| 165,5 bis 199,5 | Motor 2 (NEMA 17, 34 mm, Stand 8) im Motorturm, Flansch bündig unter dem Tisch bei Z 199,5, Welle nach oben |
| 182,5 bis 188,5 | Laufring (fest) |
| 188,5 bis 210,5 | Laufrollen 608 (drehen mit dem Karussell), Achse Z 199,5 |
| 199,5 bis 221,5 | Motorwelle Ø 5 x 22 (Modell, messen), steckt im D-Sackloch der Karussellnabe, Wellenende 1,5 unter der Plattenoberseite, trägt nur Drehmoment |
| 207 bis 211 | Nabe Ø 36 der Karussellplatte, Magnet 5 x 2 in der Unterseite bei r 14, 1,5 über dem Hall-Sensor (Pfostenoberseite Z 205,5) |
| 211,0 bis 223,0 | Karussellplatte Ø 171 x 12 |
| 219,5 bis 222,5 | Spritzenflansch in der Tasche (Tasche 3,5 tief) |
| 231,5 | Oberkante Kolbenplatte bei leerer Spritze (Kolben ganz unten) |
| 235,1 | Oberkante Kolbenplatte bei 2 ml Rest (tiefster Stempel S_min) |
| 320,8 | Oberkante Kolbenplatte bei 50 ml (Nutzfüllung) |
| 330,8 | Stempelunterkante S_park (höchste Stellung), 10,0 über der 50-ml-Platte |
| 320,8 bis 378,8 | Schlitten in Parkstellung (S - 10 bis S + 48), Ausleger mit Stempel Z S + 2 bis S + 48 |
| 330 | Oberkante Portalöffnung |
| 338 bis 341 | Goldband (Gold-PETG) |
| 346,8 bis 380,8 | Motor 1 (NEMA 17, 34 mm) hängt unter der Brücke bei θ 180, Radius 59 (ohne LED-Träger wäre darunter Platz, die Höhe ändert das nicht: sie wird von Stößelweg und Brücke bestimmt) |
| 341 bis 406,8 | Krone (Fase Z 400,8 bis 406,8 als Kronenring aus Gold-PETG) |
| 372,8 bis 380,8 | Stellring auf der Spindel unter der Brücke (taucht in eine Tasche des Schlittens) |
| 380,8 bis 387,8 | Brücke mit 608 für die Spindel |
| 387,8 bis 388,3 | Passscheibe 8 x 14 x 0,5 auf dem Lagerinnenring |
| 387,8 bis 399,8 | Brückenrippen 2 x 12, Klemmnaben der Führungswellen bis 397,8 (Wellen bis 395,1) |
| 388,3 bis 396,3 | Riemenebene GT2 20 : 20 (Zahnkranz der Scheiben) |
| 396,3 bis 404,3 | Naben der GT2-Scheiben (Kaufteil 16 hoch), Motorwelle auf 23 gekürzt bis 403,8 |
| 404,8 bis 406,8 | Kronendeckel (2 mm), 0,5 über den Naben, oben 6 mm Fase |

Stempelweg S_min bis S_park 95,7 mm.

## 4. Form und Hülle

### 4.1 Silhouette in drei Zonen

| Zone | Z | Durchmesser | Oberfläche |
|---|---|---|---|
| Sockel (Schulter) | 3 bis 97 | Kegel von Ø 204 (unten) auf Ø 196 (oben), Neigung 2,4 Grad | PETG schwarz glänzend (Filament, 0,12 bis 0,16 mm) |
| Goldring | 97 bis 101 | Ø 202, steht 3 mm über Körper und Sockeloberkante, unten 0,8 x 45 Grad Fase als Schattenfuge, eigenes Teil auf dem Sockel | Gold-PETG |
| Körper | 101 bis 338 | Ø 196 zylindrisch, Wand 1,6, Teilungsfuge bei Z 235 | PETG schwarz matt |
| Goldband | 338 bis 341 | Ø 196, Ring mit Steckern in Körper und Krone | Gold-PETG |
| Krone | 341 bis 406,8 | Ø 204 (4 mm Überstand je Seite wie eine Lippenstiftkappe), oben 6 mm Fase 45 Grad als Kronenring, Namensschild im Deckel | PETG schwarz matt (sie wird beim Abheben angefasst), Fase Gold-PETG |

Proportion Sockel : Körper : Krone = 98 : 237 : 66, also etwa 1 : 2,4 : 0,7. Eine steilere Schulter bräuchte unten mehr als Ø 204 und verletzt die Druckgrenze von etwa 200 mm. 2,4 Grad sind flach, die Taille entsteht durch Goldring (Ø 202) und Krone (Ø 204) über dem Körper Ø 196. Ob die Krone mit 66 mm zu mächtig wirkt, entscheidet die Pappattrappe (17.5). Kürzer geht sie nur mit abgedrehten GT2-Naben (Abschnitt 18).

Waagrechte Linien: Fußschatten, Goldring, Teilungsfuge (Z 235, nur 1 mm breit und dunkel), Goldband, Kronenkante. Das sind fünf statt vier, die Fuge ist aber ein Schatten und keine Farblinie. Die Druckteilung des Körpers wird nicht mehr gespachtelt: die Ränder bekommen 0,5 mm Fasen und sind gewollt sichtbar. Alle sichtbaren Kanten 1 mm Radius, außer den Fasen. Z-Naht aller Schalen hinten bei θ 180. Keine sichtbare Schraube: Sockel von unten verschraubt, Krone mit Magneten.

### 4.2 Öffnungen

**Portal vorne (θ 0):** Rechteck 72 breit (Y ± 36, als Sehne gemessen) von Z 16 bis Z 330, obere Ecken R 24, untere Ecken R 8. Es geht durch Sockel, Goldring und Körper. Ein Goldrahmen 3 breit und 1,5 erhaben läuft ringsum (drei Leistenarten, siehe unten), der Goldring endet links und rechts an der Rahmenkante (bei |Y| 39). Unten (Z 16 bis 97) ist die Bühne mit der Schublade, darüber (Z 101 bis 330) sitzt eine plane Scheibe aus Rauch-PETG.

**Portalscheibe (gedruckt):** Rauch-PETG (transparent, grau oder schwarz getönt) 2 mm, eben, 78 x 234 (Y ± 39, Z 99 bis 333, oben 3 mm Auflage über der Öffnung), Ecken passend R 26 oben und R 3 unten. 234 am Stück passt nicht aufs 220er-Bett, deshalb **zwei Hälften**: unten Z 99 bis 219, oben Z 215 bis 333, im Überlappbereich Z 215 bis 219 jeweils nur die halbe Dicke (unten innen, oben außen). Die Außenfläche bleibt bündig, außen ist eine Haarlinie bei Z 215, innen bei Z 219, beide vor der schwarzen Karussellplatte (Z 211 bis 223). Jede Hälfte wird flach gedruckt (Außenseite auf dem Bett, 0,2 mm, 100 Prozent Füllung). Sie liegt außen in einem Falz 3 breit und 2,2 tief am Portalrand, ihre Außenfläche liegt in der Ebene X 90,5 (Mitte 7,5 hinter der Zylinderfläche, an den Kanten bündig). Wo der Falzboden hinter der Wandinnenfläche liegt, trägt eine innen angesetzte Hinterlegung (3 breit). Falz und Laibung bleiben matt schwarz: von schräg vorne ist die Stufe zwischen Scheibe und Hülle als Schattenkante sichtbar, das ist gewollt. Stand 6: gehalten von 4 Magneten 6 x 2 in den Falzecken (Gegenstück: 4 Stahlscheiben 8 x 0,5 auf die Scheibe geklebt, je zwei auf jede Hälfte, bei Z 111 und Z 303). Stand 7 und 8 (`budget = 1`): ohne Magnete und Stahlscheiben, die Scheibe wird mit Klebepunkten (Heißkleber oder 2K-Epoxid) in den Falz geklebt, die Falzecken haben keine Magnettaschen. Eine Fingerkerbe entfällt: die Unterkante der Scheibe (Z 99) ist von der Bühne aus frei greifbar.

**Portalrahmen (Gold-PETG, drei Leistenarten, 3 breit, 1,5 dick):** Er ist ein eigenes Teil und liegt nicht mehr in der Hülle. Die Leisten werden **flach in der Abwicklung der Hülle** gedruckt (Bogenlänge s = r · arcsin(Y / r) statt Sehne, `dev_s` in `farbmischer.scad`) und beim Aufkleben um die Hülle gebogen: 1,5 mm PETG biegt sich über r 98 ohne Mühe (0,8 Prozent Randdehnung), die senkrechten Leisten laufen auf einer Mantellinie und biegen sich gar nicht. Bühnenrahmen (`rahmen_unten`, 80 x 84): Boden und beide Seiten von Z 13 bis 97, Innenkante = Portalkante (|Y| 36). Fensterrahmen: zwei gerade Seitenleisten (`rahmen_seite`, 3,3 x 206, Z 101 bis 307, gleich links und rechts) und ein oberes Stück (`rahmen_oben`, 88 x 29) mit beiden Bögen R 26,4 innen und dem oberen Balken bis Z 336,4. Die Innenkante des Fensterrahmens liegt bei |Y| 39,4, also 0,4 außerhalb der Falzkante, damit die Leiste nicht über die Scheibe läuft. Die Nähte bei Z 97/101 (unter dem Goldring) und Z 307 bleiben Stoßfugen in Gold. Kleben mit Sekundenkleber (Gel) oder dünnem 2K-Epoxid, zuerst ohne Kleber anlegen und mit Malerkrepp fixieren.

**Sechs Seitenfenster:** bei θ = p · 51,43 (p = 1 bis 6), je 22 breit (als Sehne), Z 108 bis 180, oben Rundbogen R 11 (Mittelpunkt Z 169), also ganz unter dem Laufring (Z 182,5): kein schwarzes Band im Fenster. Sichtbar ist der Farbstand von etwa 6 bis 46 ml. Kein Goldrahmen, ringsum 1 mm breite, 1 mm tiefe Schattenfuge (Wand darunter 0,6). Innen eine Fensterscheibe aus Klar-PETG 1,6 mm, 26 x 76, flach gedruckt, eingeklebt in einen innen aufgesetzten Rahmen 32 x 78 (ein Falz in der 1,6-mm-Wand ginge nicht), sie sitzt flach bei X 94,0 bis 95,6 und hat in der Mitte 0,8 Luft zur Wand. In Ruhe steht hinter jedem Fenster genau eine Spritze, im Tageslicht oder Raumlicht zu sehen. Das gedruckte Klar-PETG ist milchig-klar, die Farbe schimmert durch. Ist es zu trüb, wird die Scheibe weggelassen (Fenster 22 breit). Die Zuganker stehen mittig zwischen den Fenstern und sind in keinem Fenster zu sehen.

**Griffmulde:** hinten (θ 180) im Sockel, 24 breit, 60 hoch (Z 20 bis 80), 8 tief, Kanten R 4. Eine zweite Griffkante bildet der Kronenüberstand.

**Hinten:** Hohlsteckerbuchse 5,5/2,1 bei θ 180, Z 30, unterhalb der Griffmulde, mit gedrucktem Buchsenring Ø 16 aus Gold-PETG.

**Krone:** Namensschild als Einlage im Deckel: ihr Spitzname plus „Atelier“, Schrift Didot oder ähnliche Antiqua, Versalhöhe 9, mittig, Leserichtung von vorne. Das Schild (etwa 90 x 16 x 1,2, Schrift 0,6 erhaben, 0,12 mm Schicht) wird separat flach gedruckt, **zweifarbig durch einen Filamentwechsel**: Basis 0,6 in Schwarz, bei Schichthöhe 0,6 im Slicer pausieren (Farbwechsel), Schrift in Gold. Es wird in eine 1,2 tiefe Tasche im Deckel geklebt. Der Spitzname fehlt noch, Johann trägt ihn in `farbmischer.scad` (`name_gravur`) ein. Unter der Grundplatte Datum und Widmung, 0,6 tief graviert (ungefärbt).

### 4.3 Farben, Materialien, Oberflächen (CMF, Hex-Werte für das Rendering)

Alles ist PETG. Keine Nachbearbeitung außer Entgraten, Kleben und dem Einsetzen der Magnete. PETG lässt sich nur schlecht schleifen (schmiert), also wird auf Druckbild und Filamentwahl gesetzt.

| Element | Material, Verfahren | Hex | Rendering |
|---|---|---|---|
| Sockel, Schubladenfront | PETG schwarz glänzend, 0,12 bis 0,16 mm, Außenwand langsam (30 bis 40 mm/s) | #0A0A0C | Rauheit 0,15, Schichtlinien nur andeuten |
| Körper, Krone | PETG schwarz matt (Matt-PETG) oder normales Schwarz mit 0,2 mm und 50 Prozent Lüfter, damit es matt bleibt | #141417 | Rauheit 0,5 |
| Gold (Goldring, Goldband, Kronenring, Portalrahmen, Goldlippe, Buchsenring, Schildschrift) | Gold-PETG (Silk oder metallic), flach oder stehend nach 12, Kanten gratfrei | #C9A44C, Licht #E8CB7A, Schatten #8A6A22 | Metall 1,0, Rauheit 0,25 |
| Portalscheibe | Rauch-PETG transparent (grau getönt), 2 mm, zwei Hälften, etwa 40 bis 50 Prozent Transmission | #2E2E33, Deckkraft 0,45 | glänzend, Brechung 1,49 |
| Fensterscheiben | Klar-PETG 1,6 mm, milchig-klar | #E9ECEE, Deckkraft 0,25 | |
| Schublade (Korpus) | PETG weiß | #F4F2EE | Rauheit 0,5 |
| Innenteile (Karussell, Rollenböcke, Schlitten, Ausleger, Rinne, Brücke, Podest, Grundplatte) | PETG schwarz (beliebige Sorte) | #1C1C1E | Rauheit 0,7 |
| Spritzen | PP klar | #E9ECEE, Deckkraft 0,25 | Skala zur Mitte gedreht, Aufdruck unsichtbar |
| Ventile, Lippen, Gummiauflage | Silikon transluzent, Gummi | #DAD6CC, Deckkraft 0,6 | |
| Stahl (Wellen, Spindel, Zuganker) | blank, verzinkt | #8C8D91 | Metall 1,0, Rauheit 0,35 |
| Messingmutter | Messing | #B08D57 | |
| Füße | Silikon | #1A1A1A | |
| Becher | PP transluzent | #EEEEEE, Deckkraft 0,55 | |
| Farbe Cyan | Studienacryl Primärcyan | #0093D3 | |
| Farbe Magenta | Primärmagenta | #D4007A | |
| Farbe Gelb | Primärgelb | #FFD200 | |
| Farbe Titanweiß | | #F6F4EE | |
| Farbe Schwarz | Mars- oder Elfenbeinschwarz | #1B1A19 | |

Nie sichtbar: unbehandeltes Beige oder Grau an der Hülle, mehr als eine Metallfarbe, Gold als Fläche. Fingerabdrücke und Staub zeigen sich auf Glanz-Schwarz deutlich, deshalb sind Körper und Krone, die sie anfasst, matt.

Standardansicht für das Rendering: Gerät auf einem hellen Holzschreibtisch, Kamera 30 Grad von vorne rechts, 15 Grad von oben, Raumlicht (Softboxen, Decke), kein Eigenlicht. Bühne mit Becher in der Zielfarbe auf weißem Schubladenboden, durch die Seitenfenster bei 51 und 103 Grad sind Weiß 1 und Gelb zu sehen. Dazu ein Schnitt in der XZ-Ebene.

## 5. Bauteile

### 5.1 Grundplatte und Sockelinneres (Stand 6: LED-Ring und LED-Ringhalter entfallen)

| Element | Lage und Maße |
|---|---|
| Grundplatte | Ø 200 x 4, Z 3 bis 7, Randrippe r 96 bis 98 und Radialrippen 2 x 8 nach oben. Sechs Fußtaschen Ø 12,5 x 1 unten auf r 92 bei θ 30 + 60 k. Vier Bohrungen Ø 5,5 für die Zuganker auf r 90,5 bei θ ± 32 und ± 128,6, unten je eine Sechskanttasche für die Mutter M5 (Schlüsselfläche radial außen). Vier Bohrungen M3 auf r 96 bei θ ± 45 und ± 135 zum Verschrauben der Sockelschale von unten (Senkung, unsichtbar) |
| Ballast | Stand 8: etwa 0,4 kg Schrauben, Muttern und Unterlegscheiben aus dem Arbeitsvorrat (gratis), je Becher bis Z 28 gefüllt (Ø 38, 7 x 3 mm), mit Heißkleber oder Epoxid vergossen. Stand 6: 0,48 kg Stahlscheiben, 28 x DIN 125 M20 (Ø 37 x 3, je 17 g), vier Stapel zu je sieben Scheiben. Becher der Grundplatte bei (r 72, θ +69), (r 72,5, θ -71), (r 66,5, θ +120) und (r 66,5, θ -120), Z 7 bis 28, mit Filz abgedeckt. Kleinster Abstand zu Wägezelle, Schienen, Lagerbock, Motor 2 mit Winkel, Rinnensäulen und Zugankern 5,2 (Prüfung 49, Stand 6, für Stand 8 nicht neu gerechnet; zum Motorturm mindestens 14,9, Handrechnung Stapel Ø 37 gegen Turm 50,4 x 50,4). Die alten Plätze bei ± 115 lagen unter den neuen Zugankern |
| Motorturm (Stand 8) | gedruckter vierwandiger Kasten, außen 50,4 x 50,4 (Motor 42,3 plus 1 Luft je Seite plus Wand 3), Z 7 bis 202, innen 44,4 x 44,4 bis Z 199,5. Tisch Z 199,5 bis 202 (2,5 dick) mit Zentrierbund-Loch Ø 22,5 und vier M3 von oben (Lochkreis 31 x 31), Kabelfenster 18 breit x 18 hoch unten in der -Y-Wand (zur Platine), Hallpfosten 6 x 9 auf dem Tisch bei r 14 bis Z 205,5. Der Turm wird mit dem eingebauten Motor und dem Kabel auf die Grundplatte geklebt (quadratischer Aufnahmerahmen 2 hoch, Spiel 0,2). Abstand zum Spritzenzylinder beim Drehen mindestens 6,4 (Handrechnung: Turmecke r 35,6 gegen Zylinder Ø 30 bei r 57, nicht aus dem Prüfskript). Entfallen sind der Lagerbock Karussellwelle (Rohr Ø 40 x 33 mit zwei 608) und der Hallhalter |
| Motorwelle (Stand 8) | Welle des Motors 2: Ø 5 mit D-Fläche (Fläche 2,0 von der Achse), 22 ab Flansch angenommen [MESSEN], Z 199,5 bis 221,5. Sie steckt im D-Sackloch der Nabe (Madenschraube M3 auf die D-Fläche) und trägt kein Gewicht, die Platte läuft auf den Rollen. Entfallen sind die Karussellwelle Stahl Ø 8 h6 x 212 und zwei Stellringe |
| GT2-Rad 70 Z (entfällt) | Stand 8: kein Riemen am Karussell. Die Magnettasche Ø 5,2 x 2,2 für die Hall-Referenz liegt jetzt in der Nabenunterseite der Karussellplatte (r 14) |
| Motor 2 | NEMA 17, 34 mm (derselbe Motor wie der Stößel, etwa 0,28 Nm), 42,3 x 42,3, Achse in der Gerätemitte (X 0, Y 0), Körper Z 165,5 bis 199,5, Welle nach oben, Flansch von oben mit vier M3 am Tisch des Motorturms angeschraubt, Zentrierbund Ø 22 im Tischloch. Entfallen sind der Pancake 23 mm bei θ 180 und r 57,8, der Motor-2-Winkel mit Langlöchern und Silikondämpfern und die GT2-Scheibe 20 Z |
| Hall-Sensor | A3144 liegt flach (Fläche nach oben) in der Tasche 4,4 x 5,4 des Hallpfostens auf dem Tisch des Motorturms bei θ 0 und r 14, die Beinchen gehen durch den Schlitz 3 x 4 in den Turm. Gegenüber sitzt der Magnet Neodym 5 x 2 in der Nabenunterseite der Karussellplatte (Tasche Ø 5,2 x 2,2), Luft 1,5. Entfallen ist der Hallhalter am Lagerbock |
| Wägezelle | 500 g, 80 x 12,7 x 12,7, entlang Y bei X 50,65 bis 63,35, Y -70 bis +10, Z 7,5 bis 20,2. Festes Ende Y -70 bis -50 auf einem Bock 0,5 hoch (2 x M4), Lastende Y -10 bis +10 genau unter der Bechermitte (X 57, Y 0). Unter dem Lastende ein fester Überlastanschlag mit 0,8 Luft. Auf Silikonscheiben 1 mm entkoppelt |
| Podest | Stiel Ø 14, Z 20,2 bis 24,4 auf dem Lastende (2 x M4), Scheibe Ø 60 x 1,6 PETG schwarz Z 24,4 bis 26 |
| Schubladenschienen | zwei L-Schienen bei \|Y\| 32 bis 35 (genau unter den Schubladenwänden Y 33 bis 35), X 20 bis 98, Oberkante Z 26,5, als Balken Z 22,5 bis 26,5 über die Wägezelle geführt (2,3 Luft), auf je zwei Pfosten. Auf den hinteren 5 mm (X 20 bis 25) um 1 mm abgesenkt (Rampe 1 : 5). Höhe je Pfosten mit Beilagen 0,1 bis 0,5 justierbar. **Einstellmaß:** Kufenluft über der Schiene bei geschlossener Schublade 0,5 ± 0,2, mit Fühlerlehre prüfen. Stand 6: Reed-Kontakt in der rechten Schiene bei X 30 (ab Stand 7 entfällt er, die Waage erkennt die Schublade) |
| Platine | Lochraster 70 x 90 senkrecht in der Ebene Y -81, X -45 bis +45, Z 30 bis 100 (über den Ballaststapeln), Bauteile nach innen: unter Z 52 bis Y -66, darüber höchstens bis Y -70 (Feuchtrinne r 69). ESP32 unten einsetzen. Ecke r 93,5, 2,9 zur Hülle |
| Kabelkanal | Kabelbinder am Zuganker θ -128,6 (Stand 6: gedruckte Clips) von Z 15 bis zur Brücke, alle festen Leitungen nach oben (Motor 1 und Endschalter, vier plus zwei Adern) |

### 5.2 Bühne und Schublade

| Element | Lage und Maße |
|---|---|
| Schublade | PETG weiß, außen 70 breit (Y ± 35), X 27,2 bis zur Front (Stand 8, vorher X 22: der Motorturm reicht bis X 25,2), Seitenwände 2 dick bis Z 45, Boden 1,5 dick (Z 26 bis 27,5), ohne Fenster. Bechersitz konisch: innen Ø 48 unten auf Ø 52 in 3 mm Höhe, zentriert den Becherboden Ø 47 auf etwa 0,5 genau unter dem Ventil. Hinten offen. Kufen nur hinten (X 22 bis 25), sonst 1 mm Freistich über den Schienen |
| Front | PETG schwarz glänzend, folgt der Sockelkontur (Kegel), 68 breit, Z 17 bis 45, mit der Schublade verschraubt. Oben aufgeklebt die Goldlippe (Gold-PETG, 3 hoch, 1,5 über der Front, 4,5 tief für die Klebefläche) als Daumenauflage |
| Wägeprinzip | Geschlossen fällt die Schublade über die Schienenrampe 1 mm ab und liegt nur noch auf der Podestscheibe (Kufen 0,5 über den Schienen). Gewogen werden Schublade, Becher und Farbe, die Waage tariert. Beim Herausziehen hebt die Rampe die Schublade 0,5 über das Podest. Die Firmware prüft vor jeder Dosierung das Tara-Fenster (leere Schublade plus 2 bis 15 g) und ob der Wert ruhig steht, sonst Meldung „Schublade ganz schließen“ (Druck auf die Front oder ein schief stehender Becher würde die Schublade auf die Schienen drücken) |
| Rastung | Magnet 6 x 2 in der Front gegen Stahlscheibe im Sockel, horizontal, Klick beim Schließen |
| Auszug | 50, dann steht die Bechermitte bei X 107, also vor dem Sockel, und der Becher ist von beiden Seiten greifbar. Ganz herausnehmbar zum Spülen |
| Becher | Portionsbecher PP 60 ml mit Deckel: oben Ø 62, unten Ø 47, Höhe 33 (Hüllmaß für Ersatzbecher: unten Ø 46 bis 47,5, oben höchstens Ø 63, höchstens 33 hoch). Bechermitte X 57, Y 0 |

### 5.3 Feuchtrinne und Abstreifer

*Stand 7 und 8: Feuchtrinne, Deckel, Säulen, Abstreifhalter, Silikonlippen, Schwamm und Einführzunge entfallen (`budget = 1`). Der Abschnitt beschreibt Stand 6.*

| Element | Lage und Maße |
|---|---|
| Feuchtrinne | fester C-Ring r 45 bis 69, Z 54 bis 64, Boden 2 dick, offen vorne zwischen θ -38 und +38. Getragen von vier Säulen Ø 8 bei θ ± 95 (r 57) und ± 145 (r 57) von der Grundplatte. Innen zwei Kammern (links, rechts, Trennsteg bei 180) |
| Rinnendeckel | zwei Hälften PETG 1,2 (je Kammer eine), Z 64 bis 65,2, auf Stiften gesteckt. Sechs Löcher Ø 14 genau unter den Parkstellungen der Düsen (θ = p · 51,43), dazwischen geschlossen. Die offene Schwammfläche sinkt von etwa 5800 auf 920 mm², die Verdunstung etwa auf ein Sechstel. Ventil beim Drehen 2,3 über dem Deckel |
| Schwammstreifen | je Kammer ein Streifen Zellulose-Schwammtuch 20 x 145, zwei Lagen, unter dem Deckel, nass in den Löchern bis Z 65,5, 2,0 unter den Ventilspitzen. Wasservorrat je Kammer etwa 30 ml. Ziel: 4 Wochen je Füllung, am Prototyp durch Wiegen der Rinne prüfen |
| Abstreiflippen | zwei Lippen aus Silikon 1,5 dick (aus Backmatte geschnitten, einziges nicht gedrucktes Teil der Rinne; Rückfallebene gedruckte PETG-Lippe 0,6 dick, wischt aber härter) bei θ ± 40, radial r 50 bis 64, Oberkante Z 68,5 (1,0 über der Ventilspitze), in gedruckten Haltern auf den Rinnenenden. Jede Düse wird gewischt, bevor sie über den Becher fährt, der Abrieb fällt in die Rinne |
| Wechsel der Streifen | Schublade ziehen, Portalscheibe ab, Karussell in Parkstellung. Streifen am vorderen Ende unter dem Deckel greifen und herausziehen. Den neuen Streifen mit der gedruckten Einführzunge (PETG 0,8 x 16 x 160, vorne Haken) einschieben |

### 5.4 Spritze (Kaufteil, Maße nachmessen)

| Größe | Wert (Annahme) |
|---|---|
| Typ | 60-ml-Einmalspritze mit Katheteransatz (Blasenspritze), z. B. Omnifix 50/60 ml oder BD Plastipak 60 ml Catheter Tip. Luer-Lock passt in dieselbe Tasche als Ausweichteil (langsamer) |
| Zylinder | außen Ø 30, innen Ø 26,7, Länge Flanschoberkante bis Zylinderende 125 |
| Konus | 20 lang, außen Ø 8 bis 6, Öffnung Ø 3,5 |
| Flansch | 45 x 32 x 3, Ecken mindestens R 4 (sonst Taschenecken freilegen) |
| Kolbenplatte | Ø 38 (ungünstigster Fall), 3 dick |
| Kolbenstange | Kreuz 12 x 12 |
| Lage im Gerät | Flanschoberkante Z 222,5, lange Flanschseite radial |
| Füllung | Nutzfüllung 50 ml, Füllmarke (Aufkleber gold) bei 50 ml. Kolbenplatte leer Z 231,5, 50 ml Z 320,8. Eine überfüllte Spritze passt nicht unter den geparkten Stempel und lässt sich nicht einsetzen (eingebaute Lehre) |
| Ventil | Silikon-Entenschnabelventil, Außen-Ø 8 bis 9, 10 lang, auf einem 6 mm langen Silikonschlauch 4 x 6 über dem Konus, Spitze Z 67,5 |

### 5.5 Karussell (dreht, Motor 2)

| Element | Lage und Maße |
|---|---|
| Karussellplatte | PETG schwarz, Ø 171 x 12, Z 211 bis 223. Nabe Ø 36 unten bis Z 207 (Stand 6: Nabe Ø 30 bis Z 205 mit D-Bohrung 8, axial frei auf der Welle). Stand 8: D-Sackloch Ø 5,3 mit Fläche bei 2,15 von der Achse für die Motorwelle Ø 5, von unten bis 1,5 unter die Plattenoberseite (Z 221,5), Madenschraube M3 (Kernloch 2,7) von +X auf die D-Fläche bei Z 210,6, Magnettasche Ø 5,2 x 2,2 in der Nabenunterseite bei r 14 (Hall-Referenz). Die Platte läuft unverändert mit den sieben Rollenböcken auf dem Laufring, die Welle trägt kein Gewicht |
| Plätze | p = 0 bis 6 bei θ = p · 51,43 + φ. Platz 0 ohne Spritze (geschlossene Platte), Plätze 1 bis 6 mit Station |
| Flanschtasche je Station | 33 tangential, 3,5 tief, radial ab r 34 bis zum Plattenrand r 85,5 offen (Einschub von außen), Innenecken R 5. Steg zwischen Nachbartaschen 3,1 |
| Zylinderschlitz | 32 breit, von r 41 (Mitte r 57, Halbkreis R 16) radial nach außen durchgehend, Einlaufschrägen 1 x 45 Grad. Steg zwischen Nachbarschlitzen 17,5 (kürzester Abstand der Halbkreise) |
| Flanschauflage | Der Flansch (32 breit) liegt über dem 32 breiten Schlitz nur innen auf, auf dem Halbmond zwischen r 34,5 und dem Halbkreis R 16, der an den Seiten bis r 57 reicht. Damit die Dosierkraft sicher innerhalb dieser Auflage liegt, drückt der Stempel 4 mm innen von der Spritzenachse (X 53, Prüfung 51). Bei der Funktionsprobe beobachten, dass die Spritze unter 100 N nicht kippt |
| Rastzunge | je Station eine gedruckte Federzunge 1,5 dick in der Taschenwand außen, Rastnase 1,0, hält den Flansch radial, klickt beim Einschieben |
| Stationsbuchstabe | je Station ein Buchstabe (W, Y, M, C, K, W für Platz 1 bis 6), Größe 8, 0,6 tief eingraviert, bei r 76, 24,7 seitlich der Stationsachse (auf dem Steg neben der Tasche), lesbar von vorne, sichtbar durchs Portal. Statt eines Lackfarbrings (er braucht kein Farbfilament) |
| Rollenböcke | sieben gedruckte Gabeln unter der Platte bei θ = (j + 0,5) · 51,43 + φ (j = 0 bis 6), radial r 74,5 bis 85,5, Außenfläche als Bogen r 85,5 (keine Ecke darüber, 2,5 zu den Zugankern), tangential ± 12, Z 193,5 bis 211, je 2 x M3 von oben verschraubt (Ohren tangential außen). Wangen 2 dick, Raum für die 608 7,0. Achse M8 radial bei r 80, Z 199,5 |
| Laufrollen | sieben Kugellager 608 (22 x 8 x 7), Achse radial, Lauffläche r 76,5 bis 83,5, Unterkante Z 188,5 |
| Laufring | fest, PETG, r 74,5 bis 86,5, Z 182,5 bis 188,5, Lauffläche oben eben, offen vorne zwischen θ -15 und +15, Enden mit Rampe 1,5 auf 10 mm. Vier Laschen bis zu den Zugankern (r 90,5) bei ± 32 und ± 128,6, Laschenende r 94,5 (1,9 zur Körperwand) mit außen offenen Sechskanttaschen, Muttern M5 oben und unten, Höhe über Passscheiben 5 x 10 (0,1 bis 0,5) unter der Lasche justierbar. Die Unterseite ist glatt (keine Nut, keine LEDs mehr) |
| Mittelstift oben | Die Plattenmitte (r unter 30) ist oben eben, darüber hängt der Stößel. Nichts ragt über Z 223 |

### 5.6 Stößel (fest in der Mitte, Motor 1)

| Element | Lage und Maße |
|---|---|
| Spindel | T8, Steigung 2 (eingängig), Achse X 0, Y 0, Z 250 bis 403, Länge 153 (Kaufmaß 200, gekürzt). Die Mutter sitzt im Schlitten bei S + 20,5 bis S + 35,5, bei S_min also ab Z 255,6, die Spindel reicht dort noch 5,6 tiefer. Hängt im 608 der Brücke. Ein Stellring Ø 8 (16 x 8) unter dem Lager, Z 372,8 bis 380,8, nimmt die Dosierkraft nach oben auf. Oben auf dem Lagerinnenring liegt eine Passscheibe 8 x 14 x 0,5, darauf die GT2-Scheibe 20 Z (Bohrung 8, Kaufteil 16 hoch, Zahnkranz unten, Nabe oben) mit Madenschraube auf einer angeschliffenen Fläche der Spindel, sie hält das Eigengewicht. Keine Kupplung, die Motorwelle trägt nur Riemenzug |
| Führungswellen | zwei Stahlwellen Ø 10 h6, bei X 0, Y ± 22, Z 225,1 bis 395,1 (Länge 170, Kaufmaß 200), oben 14,3 tief eingespannt in Brücke (7) und geschlitzter Klemmnabe Ø 20 x 10 auf der Brückenoberseite (M3), unten frei |
| Schlitten | PETG, zylindrisch r 34 mit einer ebenen Fläche bei X 28 (vorne, volle Höhe) für den Winkel, 58 hoch, Z S - 10 bis S + 48. Stand 7: zwei Gleitbohrungen Ø 10,4 bei Y ± 22 direkt auf den Wellen Ø 10, als zwei Gleitzonen von je 14 mm unten und oben, dazwischen Ø 12 frei (kein Linearlager gekauft, Wellen leicht einfetten, klemmt der Schlitten, Bohrung auf 10,5 aufweiten). Stand 6: Bohrungen Ø 19 H7 für je ein LM10LUU (19 x 55), eingeklebt und mit Madenschraube gesichert. Mittig von oben eine Stufenbohrung: Ø 23 x 12,5 tief, darin unten der Flansch der Messingmutter (Ø 22 x 3,5, 4 x M3), oben 9 mm freier Raum für den Stellring. Spindeldurchgang Ø 12 |
| Ausleger mit Stempel | **ein Teil aus PETG schwarz** (ersetzt Winkelstahl und Stempelscheibe). Senkrechte Platte X 28 bis 36, Y ± 12,5, Z S + 8 bis S + 48, an der ebenen Schlittenfläche X 28 mit 2 x M4 (Zylinderkopf, Senkung Ø 7,6 x 4) in zwei waagrechten Kernlöchern Ø 3,7 x 12 tief im Schlitten bei S + 24 und S + 40 (32 mm Hebel zur Kippkante; Stand 7: die Schrauben schneiden das Gewinde selbst in das PETG, Auszugtest Pflicht; Stand 6: Gewindeeinsätze M4). Waagrechter Arm X 28 bis 68, Z S + 8 bis S + 16 (8 dick). Stempelfuß Ø 25 x 6 unter dem Arm bei X 53 (Z S + 2 bis S + 8), 4 mm innen von der Spritzenachse, liegt ganz auf der Kolbenplatte Ø 38 (Rand 2,5). Zwei Stützrippen 3 dick bei \|Y\| 9,5 bis 12,5, Dreieck 22 x 20 zwischen Platte und Arm. Darunter klebt eine 2 mm Gummi- oder Silikonauflage Ø 25 (Unterkante S). **Druck liegend auf der Seite (Y nach oben):** das L-Profil steht dann in jeder Schicht, die Last liegt in der Schichtebene, nicht quer dazu. 4 Perimeter, 100 Prozent Füllung. Nachweis Abschnitt 16 |
| Endschalter oben | Mikroschalter in einer Tasche der Brückenunterseite bei X -26, Y 0 (zwischen Schlitten in Park und Brücke sind nur 2 mm), die Schlittenoberkante löst bei S = S_park + 0,5 aus |
| Motor 1 | NEMA 17, 34 lang (etwa 0,26 Nm), 42,3 x 42,3, hängt unter der Brücke bei θ 180, r 59 (X -59), Körper Z 346,8 bis 380,8, Welle nach oben durch ein Langloch ± 3 (Riemenspannung), auf 23 gekürzt, auf 4 Silikonscheiben 1 mm |
| Riementrieb | GT2 20 : 20, geschlossener Riemen 158, 6 breit, Achsabstand 59, Riemenebene Z 388,3 bis 396,3, beide Scheiben mit Nabe oben (bis 404,3) |
| Kein Sensor am Schlitten | Den Kontakt zur Kolbenplatte erkennt die Waage, es gibt keine bewegte Leitung |

### 5.7 Brücke, Goldband, Krone

| Element | Lage und Maße |
|---|---|
| Brücke | PETG, Ø 196 x 7, Z 380,8 bis 387,8, sechs Radialrippen 2 x 12 nach oben bis Z 399,8 (5 unter dem Kronendeckel, am Riemen ausgespart), Lagersitz 608 mittig, zwei Klemmnaben Ø 20 x 10, Langloch für Motor 1, Tasche für den Mikroschalter unten, vier Bohrungen für die Zuganker: oben Mutter in 4,5 tiefer Sechskanttasche (Stange endet bündig bei 387,8), unten eine Mutter, beide mit Schraubensicherung mittelfest |
| Goldband | Gold-PETG (ersetzt die Lichtfuge), außen Ø 196, Wand 1,6, sichtbar Z 338 bis 341, oben und unten je 2 mm Stecker (Wand 1,2) in Körper und Krone. Es leuchtet nicht. Die offene Körperoberkante ist damit zu (kein Licht, kein Staub von oben) |
| Krone | PETG schwarz matt, Ø 204, Z 341 bis 406,8, Wand 2,4 bis Z 400,8, Deckel 2 (Z 404,8 bis 406,8). Die Fase 6 x 45 Grad oben außen ist ein eigener **Kronenring** (Gold-PETG, Parallelogramm 2 mm waagrecht dick, r 102 bei Z 400,8 bis r 96 bei Z 406,8), der auf die um 2 mm zurückgesetzte Fase des Kronenkörpers geklebt wird (Außenmaß bleibt Ø 204). Der Kronenkörper hat dazu einen Absatz bei Z 400,8 und eine Schale entlang der Fase (2,4 waagrecht) mit Innenkragen Z 397,8 bis 400,8. Tasche für das Namensschild im Deckel. Innen vier Magnete 6 x 2 gegen vier Magnete in der Brücke, zwei Zentrierstifte. Abnehmbar nur für die Wartung, nicht für das Nachfüllen. Gedruckt kopfüber (Deckel auf dem Bett), Fase und Absatz sind 45 Grad und 2 mm Brücke |
| Körperbefestigung | Körper steckt unten mit 3 mm Falz (Zapfen und Muffe je 0,7) auf dem Sockel, der Goldring liegt dazwischen (der Sockelfalz geht durch den Ring), und wird oben vom Goldband gehalten, auf dem vier Haltewinkel an den Zugankern (Z 333 bis 336, 3,0 hoch) aufliegen. Die zwei Körperhälften (Teilung Z 235) werden über einen innen liegenden Klebering PETG 8 hoch x 1,2 (je 4 mm in beide Hälften) verklebt (2K-Epoxid), außen sitzt der Stoß 3 x 0,7 mit der Schattenfuge (0,5 x 45 Grad Fasen) |

### 5.8 Kraftpfad

Stempel, Kolbenplatte, Kolben, Farbe und Zylinder, Flansch, Karussellplatte, Rollenbock, vordere Rollen (θ ± 25,7), Laufring, vier Zuganker M5 (verzinkt, r 90,5, θ ± 32 und ± 128,6), Brücke, 608, Stellring, Spindel, Messingmutter, Schlitten, Ausleger mit Stempel. Die Schalen liegen nicht im Kraftfluss. Die Muttern M5 (DIN 934) sitzen in Sechskanttaschen der PETG-Teile, Schlüsselfläche radial außen (r 94,5, 1,9 zur Körperwand). Die Karosseriescheiben Ø 20 aus Stand 5 passen nicht in die Hülle und entfallen: die Auflage einer Mutter (etwa 33 mm²) trägt höchstens 50 N, das sind 1,5 MPa, für PETG unkritisch. Gegen Lösen Schraubensicherung mittelfest statt Kontermutter. Spannung im Zuganker 1,8 MPa bei 100 N. Stand 8: Die Motorwelle des Karussells gehört nicht zum Kraftpfad, sie überträgt nur das Drehmoment der Platte (Bedarf 0,062 Nm, Haltemoment 0,28 Nm), das Gewicht der Platte und die Dosierkraft laufen über die Rollenböcke auf den Laufring. Der Schlitten läuft ab Stand 7 mit Gleitzonen direkt auf den Führungswellen.

### 5.9 Licht (entfällt in Stand 6)

Es gibt kein Licht mehr: keine LEDs, keinen Pegelwandler, keinen 1000-µF-Kondensator, keine Datenleitung. Der Fortschritt einer Dosierung und die Meldung „Fertig“ erscheinen nur in der App. Wer ein Signal am Gerät will, steckt einen aktiven Piezo-Summer 5 V (etwa 1 Euro) an einen freien Pin (GPIO 25 ist durch den Wegfall der LED-Daten frei) und lässt ihn bei „Fertig“ kurz piepen. Das ist optional und nicht in der Stückliste.

## 6. Kaufteile mit Maßen (für Rendering und Konstruktion)

| Teil | Maße |
|---|---|
| NEMA 17, 34 mm (Stößel und Karussell, zwei gleiche) | 42,3 x 42,3 x 34, etwa 0,26 bis 0,28 Nm Haltemoment, 0,4 A (Einkaufsliste), Zentrierbund Ø 22 x 2, Welle Ø 5 mit Abflachung, Länge ab Flansch 24 (Stößel, auf 23 kürzen), Karussell im Modell 22 [MESSEN], Lochkreis 31 x 31 M3 |
| NEMA 17 Pancake 23 mm | entfällt ab Stand 8 (Karussell direkt am Motor 2 mit dem 34-mm-Motor). Stand 5 bis 7: 42,3 x 42,3 x 23, Welle Ø 5 x 20, Lochkreis 31 x 31 M3, etwa 0,12 Nm bei Nennstrom (etwa 1 A), bei 0,4 A etwa 0,05 Nm |
| Kugellager 608, 10er-Pack (8 verbaut: 7 Rollen, 1 Brücke, 2 Reserve; Stand 8 ohne Lagerbock) | Ø 22 x Ø 8 x 7 |
| T8-Spindel, Steigung 2 | Ø 8, Messing-Flanschmutter Flansch Ø 22 x 3,5, Körper Ø 10,2 x 15, 4 x Ø 3,5 auf Lochkreis 16 |
| Linearwelle | Ø 10 h6 x 200, gekürzt auf 170 |
| LM10LUU | entfällt ab Stand 7 (Gleitzonen im Schlitten). Stand 6: Ø 19 x 55, Bohrung 10 |
| Karussellwelle | entfällt ab Stand 8 (Direktantrieb). Stand 6 und 7: Ø 8 h6, gekürzt auf 212 |
| Stellring | Ø 8, außen Ø 16, 8 breit, M4-Madenschraube (Stand 8: 1 Stück, auf der Spindel unter der Brücke; Stand 6: 3 Stück) |
| GT2-Scheibe 20 Z | Teilkreis Ø 12,7, außen Ø 16, Bund Ø 16, Höhe 16 (Zahnkranz mit Bund 8, Nabe 8), Stand 8: 2 Stück, Bohrung 5 (Motor 1) und 8 (Spindel), Stand 6: Bohrung 5 (2 x) und 8 (1 x), dazu Passscheibe 8 x 14 x 0,5 (DIN 988) |
| GT2-Riemen | geschlossen 158 (Stößel), 6 breit. Der Riemen 210 (Karussell) entfällt ab Stand 8 |
| Gewindestange M5 | 4 x 385 (Z 3 bis 387,8), 28 Muttern M5 DIN 934, Passscheiben 5 x 10, Schraubensicherung mittelfest |
| Wägezelle 500 g | Aluminiumbalken 80 x 12,7 x 12,7, je Ende 2 x M4 (bei manchen Typen M5), Typ YZC-133 oder ähnlich, mit HX711-Modul 21 x 34 |
| Hall-Sensor | A3144 im TO-92, Magnet Neodym Ø 5 x 2 (Stand 8: Sensor auf dem Motorturm, Magnet in der Nabenunterseite) |
| Reed-Kontakt | entfällt ab Stand 7 (die Waage erkennt die Schublade). Stand 6: Glas 2 x 14 mit Magnet 6 x 2 |
| Mikroschalter | 20 x 10 x 6 mit Rollenhebel |
| Spritze | siehe 5.4 |
| Entenschnabelventil | Silikon, Ø 8 bis 9, 10 lang |
| Becher | PP 60 ml, oben Ø 62, unten Ø 47, 33 hoch, mit Deckel |
| Silikonfüße | Ø 12 x 3, selbstklebend |
| Gummiauflage | Ø 25 x 2, selbstklebend, unter dem Stempel (Gummi oder Silikon, Rest einer Backmatte genügt) |
| Gewindeeinsätze M4 | entfallen ab Stand 7: Kernloch Ø 3,7 x 12 im Schlitten, die M4-Schrauben aus dem Arbeitsvorrat schneiden das Gewinde selbst. Stand 6: 2 Stück, Messing, zum Einschmelzen oder Einkleben in den Schlitten (Ausleger) |
| Magnete | Neodym Ø 6 x 2, 10er-Pack (Stand 7 und 8: 4 Krone, 4 Brücke, 1 Schublade, 1 Reserve), dazu 1 Magnet Ø 5 x 2 für den Hall-Sensor (Nabe). Die 4 Magnete und 4 Stahlscheiben 8 x 0,5 an den Portalscheiben entfallen (Scheiben geklebt, Stand 6: 4 Portal) |
| Netzteil | 12 V 3 A Steckernetzteil, Hohlstecker 5,5/2,1, Einbaubuchse M8 |
| Step-down | MP1584 oder Mini-360, 12 V auf 5 V, 1 A (5 V brauchen nur noch den ESP32 an VIN, rund 0,3 A; Hall-Sensor und HX711 hängen an 3,3 V) |
| Ballast | Stand 8: etwa 0,4 kg Schrauben, Muttern und Unterlegscheiben aus dem Arbeitsvorrat (gratis). Stand 6: 28 Unterlegscheiben M20 (DIN 125, Ø 37 x 3), zusammen etwa 0,48 kg |

## 7. Kinematik und Schrittzahlen

### 7.1 Karussell

| Größe | Wert |
|---|---|
| Übersetzung | Stand 8: keine, Karussell direkt am Motor 2 (1 : 1). Stand 6 und 7: GT2 20 : 70 = 1 : 3,5 |
| Schritte | 200 Vollschritte x 16 = 3200 Mikroschritte je Umdrehung (1/16 über MS1, MS2, MS3 fest an 3,3 V), 0,1125 Grad je Mikroschritt. Stand 6 und 7: 700 Vollschritte, 11 200 Mikroschritte je Umdrehung |
| Je Platz (51,43 Grad) | 3200 / 7 = 457,142857 Mikroschritte (28,5714 Vollschritte), **nicht ganzzahlig** (Stand 6 und 7: 1600, ganzzahlig). Die Firmware rechnet jede Station absolut aus p, q = round(p · 3200 / 7), oder hält die Position als Bruch bzw. auf 22 400 Schritte (7 Umdrehungen = 49 Plätze), damit sich nichts aufsummiert. Größter Rundungsfehler 0,43 Mikroschritt = 0,048 Grad = 0,05 mm auf r 57 |
| Positionen | Karussellposition q in Mikroschritten, q = 0 ist Park (Platz 0 vorne). Station p vorne bei q = -round(p · 3200 / 7) modulo 3200, also p = 1: 2743, p = 2: 2286, p = 3: 1829, p = 4: 1371, p = 5: 914, p = 6: 457. Der Vertrag mit der Firmware nennt q = round(p · 3200 / 7), das Vorzeichen folgt der DIR-Konvention der Firmware und ist bei der Inbetriebnahme zu prüfen. Stand 6 und 7: q = -p · 1600 modulo 11 200 |
| Drehrichtung | positive Schritte drehen gegen den Uhrzeigersinn (von oben). Bei der Inbetriebnahme prüfen und DIR in der Firmware invertieren, falls nötig |
| Weg | immer der kürzere Weg, höchstens 3 Plätze (1371 Mikroschritte; Stand 7: 5600) |
| Fahrprofil | 60 Grad/s, Rampe 0,3 s, ein Platz in etwa 1,2 s; Schrittfrequenz 533 Hz bei 60 Grad/s (Stand 7: 1867 Hz) |
| Drehmoment | 0,28 Nm Haltemoment direkt an der Platte, Bedarf 0,062 Nm (Beschleunigen 0,031 plus Reibung 0,031), Reserve 4,5-fach gegen das Haltemoment (im Lauf weniger, Test am Prototyp, Abschnitt 16 und 17.3). Stand 6 und 7: Pancake, Bedarf 0,018 Nm am Motor nach 1 : 3,5 |
| Referenz | Hall-Sensor (A3144 auf dem Pfosten des Motorturms bei r 14, aktiv LOW) sieht den Magneten in der Nabenunterseite der Karussellplatte bei q = 0. Fahrt langsam (10 Grad/s, 89 Mikroschritte/s) in positive Richtung bis Flanke, dann zurück und erneut langsam anfahren, Mitte der Flanke ist q = 0 |
| Bedingung | Drehen nur, wenn S = S_park (Endschalter oben geschlossen) |

### 7.2 Stationsbelegung (Platz p, Winkel in Ruhe)

| p | θ in Ruhe | Farbe | Lage von vorne gesehen |
|---|---|---|---|
| 0 | 0 | leer (Park über dem Becher) | vorne |
| 1 | 51,4 | Titanweiß W1 | vorne rechts |
| 2 | 102,9 | Gelb Y | rechts |
| 3 | 154,3 | Magenta M | hinten rechts |
| 4 | 205,7 | Cyan C | hinten links |
| 5 | 257,1 | Schwarz K | links |
| 6 | 308,6 | Titanweiß W2 | vorne links |

Die zwei Weißspritzen rahmen das Portal, Gelb und Schwarz stehen seitlich, Magenta und Cyan hinten. Auf der Karussellplatte steht neben jeder Tasche der Buchstabe der Station (W, Y, M, C, K, W).

### 7.3 Stößel

| Größe | Wert |
|---|---|
| Spindel | T8 x 2, direkt über Riemen 1 : 1 |
| Schritte | 200 x 16 = 3200 Mikroschritte je Umdrehung, 1600 je mm, 0,625 µm je Mikroschritt |
| Volumen | Kolbenfläche 560 mm² (Innen-Ø 26,7 angenommen), 1 ml = 1,786 mm = 2858 Mikroschritte, 1 Mikroschritt = 0,35 µl. Die Waage kalibriert das, der Wert ist nur Startwert |
| S_park | 330,8, Endschalter oben. Weg bis S_min (235,1) 95,7 mm |
| Geschwindigkeiten | Eilgang 8 mm/s (4 U/s, 12 s für den ganzen Weg), Anfahrt der Kolbenplatte 1 mm/s, Dosieren 0,2 bis 2 mm/s (geregelt) |
| Kraft | Motor 34 mm mit 0,8 A etwa 0,16 Nm, Wirkungsgrad T8 x 2 0,36: etwa 180 N. Benötigt bis 100 N (0,087 Nm). Strom so begrenzen, dass höchstens 150 N entstehen (etwa 0,65 A). Stand 7: mit dem A4988 stellt das Poti den Strom ein (Stößel 0,5 A), es gibt keinen StallGuard |
| Spindelspiel | Messingmutter 0,1 bis 0,2. Die Dosierstellung wird immer von oben angefahren (Spiel liegt einseitig an), der Rückhub nach dem Stopp ist 1,3 mm (1 mm Entlastung plus Spiel), damit das Ventil sicher schließt |
| Selbsthemmung | ja (Steigungswinkel 5,2 Grad, Reibwinkel 8,8 Grad), der Schlitten sinkt stromlos nicht ab |

## 8. Sensoren

| Sensor | Ort | Aufgabe |
|---|---|---|
| Wägezelle 500 g mit HX711 (80 Hz) | unter Podest und Schublade | Dosieren nach Gramm, Becher und Schublade erkennen, Kolbenkontakt erkennen (erstes Gramm), Fließende erkennen, g je ml lernen |
| Hall A3144 | Pfosten auf dem Tisch des Motorturms (r 14), Magnet in der Nabenunterseite der Karussellplatte | Referenz Karussell (q = 0) |
| Mikroschalter | Brückenunterseite | Referenz Stößel oben (S_park), Freigabe zum Drehen |
| Reed-Kontakt | rechte Schublade-Schiene | Schublade geschlossen (Stand 6; ab Stand 7 entfallen, die Waage erkennt die Schublade) |
| TMC2209 StallGuard (über UART) | Treiber Stößel | Schutz bei verstopfter Düse oder fehlender Spritze (Stand 6; ab Stand 7 mit dem A4988 entfallen, kein UART, kein Überlastschutz) |

Ein Sensor je Aufgabe, keiner bewegt sich mit, kein Kabel am Schlitten oder am Karussell.

## 9. Verdrahtung (ESP32 DevKit 30 Pin)

Verfügbare GPIOs auf diesem Board: 0, 2, 4, 5, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33 sowie die reinen Eingänge 34, 35, 36 (VP), 39 (VN). GPIO 15 ist nicht herausgeführt. Die Eingänge 34 bis 39 haben keinen internen Pullup. Die Strapping-Pins 0, 2, 5 und 12 bleiben frei. STEP, DIR, ENABLE, Endschalter und Hall bleiben wie im README von Stand 4, damit die Firmware wenig ändern muss. Stand 6 hat keine LEDs mehr, GPIO 25 ist frei.

**Stand 8 (gilt, Vertrag mit Firmware und Web-App):** zwei A4988, kein UART, Mikroschritt 1/16 fest über MS1, MS2, MS3 an 3,3 V.

| Funktion | GPIO | Beschaltung |
|---|---|---|
| Stößel STEP | 13 | direkt |
| Stößel DIR | 14 | direkt |
| Karussell STEP | 27 | direkt |
| Karussell DIR | 26 | direkt |
| ENABLE beider A4988 (LOW = aktiv) | 23 | Pullup 10 kΩ nach 3,3 V wie Stand 6, Treiber beim Booten aus |
| Mikroschalter Stößel oben | 18 | Schließer gegen GND, INPUT_PULLUP, 100 nF |
| Hall A3144 (Park Karussell) | 19 | Open-Collector, INPUT_PULLUP, aktiv LOW bei Magnet, Sensor an 3,3 V |
| HX711 DOUT | 32 | HX711 an 3,3 V |
| HX711 SCK | 33 | direkt |

Keine weiteren Pins belegt (Reed, UART und LED entfallen).

**Stand 6 (TMC2209, Reed, nicht mehr gültig, nur zur Information):**

| Signal | GPIO | Beschaltung |
|---|---|---|
| STEP Stößel (Treiber 1) | 13 | direkt |
| DIR Stößel | 33 | direkt |
| STEP Karussell (Treiber 2) | 14 | direkt (GPIO 14 gibt beim Booten Pulse aus, Treiber sind dann über ENABLE aus) |
| DIR Karussell | 32 | direkt |
| ENABLE beide Treiber | 23 | 10 kΩ Pullup nach 3,3 V, Treiber beim Booten aus (aktiv low) |
| TMC2209 UART TX | 17 | über 1 kΩ auf die gemeinsame PDN_UART-Leitung beider Treiber |
| TMC2209 UART RX | 16 | direkt an die gemeinsame PDN_UART-Leitung. Adressen: Treiber 1 MS1 = GND, MS2 = GND (Adresse 0), Treiber 2 MS1 = 3,3 V, MS2 = GND (Adresse 1) |
| HX711 DOUT | 34 | Eingang ohne Pullup, HX711 treibt aktiv. HX711 an 3,3 V, damit DOUT höchstens 3,3 V führt (GPIO 34 verträgt höchstens 3,6 V) |
| HX711 SCK | 4 | direkt |
| Hall A3144 | 21 | offener Kollektor: 4,7 kΩ nach 3,3 V und 100 nF nach GND an der Platine, interner Pullup zusätzlich an. Sensor an 5 V |
| Endschalter Stößel oben | 18 | Schließer gegen GND, interner Pullup, 100 nF |
| Reed Schublade | 19 | Schließer gegen GND, interner Pullup, 100 nF |
| frei | 22, 25, 26, 27, 35, 36, 39 | Reserve (z. B. aktiver Summer auf 25 für „Fertig“, Farbsensor später auf 26/27; I2C 21/22 entfällt, da 21 belegt) |

**Versorgung (Stand 8):** Netzteil 12 V 3 A an VMOT beider A4988 (je 100 µF direkt am Treiber), kleiner Step-down (Mini-360 oder MP1584) von 12 V auf 5 V an ESP32 VIN. HX711 und Hall-Sensor A3144 hängen an 3,3 V vom ESP32. Strombedarf wie in Stand 6: Motoren je etwa 0,4 bis 0,5 A bei 12 V, aus 12 V gesamt unter 1,2 A von 3 A.

**Versorgung (Stand 6):** Netzteil 12 V 3 A an VMOT beider TMC2209 (je 100 µF direkt am Treiber) und an einen kleinen Step-down 12 V auf 5 V (MP1584, 1 A reicht). 5 V an ESP32 VIN und Hall-Sensor. HX711 (VCC und VDD) an 3,3 V vom ESP32, nicht an 5 V. Strombedarf: Motoren beim Fahren und Dosieren etwa 0,5 bis 0,65 A je Motor bei 12 V (Ströme siehe unten), ESP32 und Sensoren etwa 0,3 A bei 5 V, aus 12 V gesamt unter 1,2 A von 3 A. Ohne die 99 LEDs (bisher 1,8 A bei 5 V) entfallen der 5-A-Wandler, der 74AHCT125, der 330-Ω-Widerstand und der 1000-µF-Kondensator.

**Treiber (Stand 8):** A4988 StepStick, Mikroschritt 1/16 über MS1, MS2, MS3 fest an 3,3 V, Strom per Poti: Vref = I · 8 · R_sense (bei R_sense 0,068 Ω etwa 0,27 V für 0,5 A am Stößel und 0,22 V für 0,4 A am Karussell, den Widerstand des Boards nachlesen). Kein UART, kein StealthChop, kein StallGuard, der A4988 ist hörbar lauter. Wer leise sein will oder einen Überlastschutz braucht, nimmt zwei TMC2209 (12 bis 16 Euro mehr, Pins wie unten für Stand 6).

**Treiber (Stand 6):** TMC2209 StepStick, MS1/MS2 als UART-Adresse, Mikroschritt 1/16 über UART gesetzt, StealthChop. Ströme (Effektivwert): Stößel 0,5 A fahren, bis 0,65 A dosieren (Grenze 150 N), 0,3 A halten. Karussell 0,4 A fahren (bis 0,6 A, falls die Reibungsmessung es verlangt), 0,2 A halten.

**Leitungen (Stand 8):** Motor 1 (4) und Endschalter (2) laufen fest am Zuganker θ -128,6 nach oben (Kabelbinder). Motor 2 und der Hall-Sensor liegen im Motorturm, ihre Leitungen gehen durch das Kabelfenster unten in der -Y-Wand zur Platine, der Hall-Sensor liegt auf dem Tisch des Turms bei r 14 (Beinchen durch den Schlitz). HX711 bleibt im Sockel. Motorleitungen paarweise verdrillt, HX711-Leitungen kurz (unter 15 cm) und getrennt von den Motorleitungen.

**Leitungen (Stand 6):** Motor 1 (4) und Endschalter (2) laufen fest im Kabelkanal am Zuganker θ -128,6 nach oben. Motor 2, Hall, Reed und HX711 bleiben im Sockel. Motorleitungen paarweise verdrillt, HX711-Leitungen kurz (unter 15 cm) und getrennt von den Motorleitungen.

## 10. Ablauf einer Dosierung

1. **Browser:** Farbe wählen, Menge in Gramm (10 bis 50 g), Start. Die App schickt das Rezept in Gramm je Farbe. „Nochmal“ wiederholt die letzte Mischung (für 100 ml zwei Becher).
2. **Prüfen:** Schublade zu und Becher da (Stand 7 und 8 ohne Reed: die Waage zeigt gegenüber leerer Schublade 2 bis 15 g mehr und steht ruhig, sonst „Schublade ganz schließen“), Vorrat jeder Station reicht laut Buchführung. Sonst Meldung in der App, nichts wird dosiert.
3. **Vorbereiten:** Referenzfahrt Stößel (hoch bis Endschalter), Referenzfahrt Karussell (Hall). Die App zeigt den Fortschritt 0 und die Zielfarbe.
4. **Je Farbe**, sortiert hell nach dunkel (W, Y, C, M, K, nur die benötigten). Bei Weiß zuerst W1 bis 2 ml Rest, dann W2.
   1. Stößel steht auf S_park. Karussell fährt die Station auf kürzestem Weg nach vorne. Dabei wischt die Lippe bei θ ± 40 die Düse ab (nur Stand 6, ab Stand 7 gibt es keine Lippen).
   2. Waage beruhigen (0,5 s), tarieren.
   3. Stempel im Eilgang bis 2 mm über die gespeicherte Kolbenplatte (unbekannt nach einem Tausch: bis S = 322,8, also 2 über der 50-ml-Platte), dann mit 1 mm/s weiter, immer von oben kommend.
   4. Kontakt: Steigt das Gewicht in drei aufeinanderfolgenden Mittelwerten (etwa 0,3 s) um mehr als 0,2 g, liegt der Stempel an und Farbe fließt. Zweite Bedingung: die Stempelstellung liegt nicht mehr als 3 mm unter der gespeicherten Kolbenplatte. Ein einzelner Tropfen oder Rauschen (0,05 bis 0,2 g bei laufendem Motor) löst nicht aus. Stempelstellung speichern.
   5. Geregelt drücken (0,2 bis 2 mm/s) bis Zielmasse minus gelernter Nachlauf dieser Farbe (Startwert 0,3 g).
   6. Stopp, Stempel 1,3 mm zurück (1 mm Entlastung plus Spindelspiel, Druck fällt ab, das Ventil schließt).
   7. Warten auf Fließende: weniger als 0,01 g/s über 1 s, höchstens 20 s.
   8. Fehlt mehr als 0,1 g: Nachstoß 0,1 ml, Schritte 6 und 7 wiederholen. Nachlauf aus Ist minus Stopp-Wert lernen.
   9. Stempel auf S_park, Kolbenplattenhöhe und Rest-ml der Station speichern.
5. **Fertig:** Karussell fährt auf Park (q = 0, Platz 0 vorne), keine Düse über dem Becher (Stand 6: alle Düsen über der Feuchtrinne). Die App meldet „Fertig“ (optional ein kurzer Piepton) und zeigt Ist-Gramm je Farbe und Abweichung.
6. **Becher nehmen:** Schublade 50 mm aufziehen (Magnetklick), Becher greifen, Deckel drauf oder umrühren. Die Waage meldet den Becher weg (Stand 6: Reed meldet offen).

Kleinste sinnvolle Teilmenge 0,1 g. Dauer je Farbe etwa 10 bis 40 s je nach Zähigkeit, ein Rezept mit vier Farben 2 bis 4 Minuten, mit sehr zäher Farbe (100 Pa·s) bis 6 Minuten.

**Fehler:** Kein Gewichtsanstieg nach 3 mm hinter der erwarteten Kolbenplatte (Stand 6 zusätzlich: StallGuard meldet Last ohne Gewicht): Düse verstopft, Abbruch, Station in der App markieren. Gewicht springt (Becher berührt): Pause, Meldung. Stationsvorrat unter 2 ml: Station sperren, Tausch anzeigen.

## 11. Handhabung

**Spritze tauschen (vorne, auf Tischhöhe):**
1. App: „Wechseln“ und Farbe wählen. Stößel fährt auf S_park, das Karussell dreht diese Station nach vorne, die App zeigt ihre Farbe.
2. Schublade ganz herausziehen und beiseitestellen (Tropfen fielen sonst auf Schublade und Becher), ein gefaltetes Küchentuch auf die Bühne legen. Portalscheibe an der Fingerkerbe abnehmen (Stand 6: Magnete; Stand 7 und 8: die Klebepunkte aus Heißkleber lösen und beim Aufsetzen neu setzen).
3. Spritze am Zylinder fassen und waagrecht nach vorne ziehen, die Rastzunge gibt nach.
4. Gefüllte Reservespritze mit Ventil waagrecht einschieben, bis es klickt. Die Einlaufschrägen führen Flansch und Zylinder, nichts wird blind eingefädelt. Eine überfüllte Spritze (über 50 ml) stößt am Stempel an und muss etwas ausgedrückt werden.
5. Tuch weg, Schublade einschieben, Scheibe aufsetzen, in der App Füllmenge bestätigen (Vorgabe 50 ml). Das Gerät parkt. Der nächste Lauf tastet diese Station langsam an.

**Spritze füllen (am Tisch, an der Spüle):** Ventil abziehen. Katheterkonus in die offene 500-ml-Flasche tauchen, Kolben langsam bis 50 ml aufziehen (etwa 1 Minute, zähe Farbe vorher mit höchstens 5 Prozent Wasser verrühren). Spitze nach oben, klopfen, Luft ausdrücken bis Farbe kommt. Ventil aufstecken, abwischen. Gefüllte Reserven stehen mit der Spitze nach oben und mit Ventil verschlossen bereit (Stand 6: in der gedruckten Spritzenablage mit sechs Fächern und Farbmarken; ab Stand 7 gibt es keine Ablage, ein Becher oder Glas genügt). Eine 500-ml-Flasche füllt zehn Spritzen.

**Reichweite:** Weiß 96 ml nutzbar in zwei Stationen. Bei 30-g-Mischungen mit 40 Prozent Weiß (etwa 9 ml) reicht das für 10 Mischungen, bunte Farben für 20 und mehr. Die App warnt „Weiß wird knapp“, sobald W1 und W2 zusammen unter 20 ml liegen.

**Becher:** Portionsbecher 60 ml mit Deckel, 100er-Pack. Gemischte Farbe mit Deckel aufheben. Ersatzbecher: unten Ø 46 bis 47,5 (konischer Sitz), oben höchstens Ø 63, höchstens 33 hoch.

**Pflege:**

| Wann | Was |
|---|---|
| vor jeder Session | Stand 7 und 8: Düsen mit dem Wischtuch abwischen (ohne Feuchtrinne trocknen sie an, nur das Ventil schützt sie). Stand 6: nach jeder Session nichts, die Düsen parken über der feuchten Rinne, die Ventile sind zu |
| alle 4 Wochen (Ziel, am Prototyp prüfen; die App erinnert) | Stand 6, ab Stand 7 entfällt: Portalscheibe ab, je Rinnenkammer 25 ml Wasser mit einer Spritze durch ein Deckelloch auf den Schwamm geben |
| nach 15 Dosierungen (App erinnert) | Stand 6, ab Stand 7 entfällt: Portalscheibe ab, die zwei Abstreiflippen mit dem feuchten Tuch abwischen (1 Minute), bevor die Farbe antrocknet |
| nach mehr als 3 Tagen Pause | App bietet „Düsen spülen“ an: leerer Becher, je Station 0,3 g |
| alle 2 bis 3 Monate oder bei Geruch | Schwammstreifen tauschen (nur Stand 6, 5.3, Ersatz im Startpaket), Schublade herausnehmen und spülen |
| bei verklebtem Ventil | Ventil abziehen, in warmem Wasser auswaschen oder ersetzen (0,25 Euro) |
| Wartung | Krone abheben (Magnete), Spindel mit PTFE-Fett nachfetten (jährlich). Stand 7 und 8 zusätzlich: Führungswellen Ø 10 leicht einfetten (Gleitzonen im Schlitten) und prüfen, ob der Schlitten leicht läuft (jährlich oder bei Quietschen); Madenschraube der Karussellnabe auf der D-Fläche nach den ersten Betriebsstunden und dann jährlich nachsehen, nicht zu fest anziehen (reißt die PETG-Nabe) |

Ein Düsen-Wischtuch (Mikrofaser) liegt dem Gerät bei. Es gibt keine Kappen, die sie aufsetzen muss.

**Tragen:** an der Griffmulde hinten im Sockel und unter dem Kronenüberstand, 3,8 kg (Stand 8 etwa 3,7 kg, Schätzung).

**Leise:** StealthChop (nur mit TMC2209, der A4988 aus Stand 7 ist hörbar lauter), kleine Ströme, Motor 1 auf Silikondämpfern (Stand 6: auch Motor 2; Stand 8 sitzt Motor 2 im Motorturm, Dämpfer dort noch nicht vorgesehen), kein Riemen am Karussell (Direktantrieb), Riemen statt Zahnrad am Stößel, Rollen statt Gleitlager an der Platte (die Gleitzonen im Schlitten laufen gefettet), gefettete Spindel, Ballast und Filz im Sockel, Silikonfüße. Ziel unter 40 dB(A) in 1 m während der Dosierung. Gemessen ist noch nichts: beim Funktionstest mit einer Handy-App messen (17.3).

## 12. Druckteile (Anycubic Kobra 2 Pro, 220 x 220 x 250, alle Teile höchstens Ø 204 in X/Y und 200 in Z)

Alle Teile aus PETG. Die Spalte „Material, Einstellung“ steht unten als Gruppe, die Tabelle hat Hüllmaß, Lage, Stützen und Masse. Das Skript `hardware/farbmischer.scad` rechnet jedes Teil in Druckorientierung (Variable `teil`), alle haben Z = 0 auf dem Bett und die Hüllmaße der Tabelle (geprüft mit OpenSCAD 2021.01).

| Nr | Teil | Hüllmaß | Lage beim Druck | Stützen | ca. g |
|---|---|---|---|---|---|
| 1 | Sockelschale mit Griffmulde und Buchsenloch (ohne Rahmen und Ring) | Ø 204 x 101 | stehend, Fuß unten. Portal oben offen, Griffmulde mit 45-Grad-Oberkante | keine | 150 |
| 2 | Körper unten (Z 101 bis 235), Portalschlitz, sechs Fenster mit Innenrahmen | Ø 196 x 137 | stehend. Fensterbögen R 11 drucken sich als Bogen | keine | 160 |
| 3 | Körper oben (Z 235 bis 338), Portaloberteil | Ø 196 x 103 | kopfüber (Portalecken R 24 werden zur Unterseite) | keine | 125 |
| 4 | Krone mit Absatz für den Kronenring und Schildtasche | Ø 204 x 65,8 | kopfüber, Deckel auf dem Bett. Fase und Absatz sind 45 Grad und 2 mm Brücke | keine | 210 |
| 5 | Goldband (ersetzt die Lichtfuge) | Ø 196 x 7 | stehend | keine | 7 |
| 6 | Goldring (am Portal offen) | Ø 202 x 4 | flach, Fase unten | keine | 10 |
| 7 | Kronenring (Fase) | Ø 204 x 6 | stehend, Wände 45 Grad | keine | 9 |
| 8 | Portalrahmen: rahmen_unten, rahmen_seite (2 x), rahmen_oben | 80 x 84 / 3,3 x 206 / 88 x 29, alle 1,5 dick | flach in der Abwicklung | keine | 5 |
| 9 | Goldlippe | 68 x 11 x 3 | flach | keine | 1 |
| 10 | Buchsenring | Ø 16 x 3 | flach | keine | 1 |
| 11 | Namensschild zweifarbig | 90 x 16 x 1,2 | flach, Schrift oben | keine | 2 |
| 12 | Portalscheibe unten (Z 99 bis 219) | 120 x 78 x 2 | flach, Außenseite unten | keine | 23 |
| 13 | Portalscheibe oben (Z 215 bis 333) | 118 x 78 x 2 | flach, Außenseite unten | keine | 23 |
| 14 | Fensterscheiben (6 Stück) | 26 x 76 x 1,6 | flach | keine | 24 |
| 15 | Grundplatte mit Fußtaschen, Ballastbechern und Aufnahmerahmen für den Motorturm | Ø 200 x 12 | Platte unten, Rippen oben | keine | 95 |
| 16 | Motorturm (Stand 8, ersetzt den Lagerbock Karussellwelle): Kasten mit Tisch, Kabelfenster und Hallpfosten | 50,4 x 50,4 x 198,5 | stehend, Tisch oben, Kabelfenster unten | Tischunterseite ist eine 44-mm-Brücke: Stütze nur dort oder Brückenprofil, am Probedruck klären | 145 |
| 17 | entfällt ab Stand 7: Feuchtrinne (C-Ring, zwei Kammern) und Deckel (zwei Hälften, 1,2), nur bei `budget = 0` | Ø 138 x 10 | Boden unten, Deckel flach | keine | 0 (Stand 6: 42) |
| 18 | Fugenhalter (4), Platinenhalter, Schienen (2), Klebering (Stand 6 zusätzlich Rinnensäulen, Kabelclips, Hallhalter, Motor-2-Winkel, die ab Stand 7 und 8 entfallen) | Klebering 192 x 180 x 8, Platinenhalter 98 x 4 x 53, Schiene 78 x 19,5 x 3, Fugenhalter 13 x 10 x 3 | je flach oder stehend | keine | 13 (Stand 6: 58) |
| 19 | entfällt ab Stand 7: Abstreifhalter (2) | 20 x 16 x 10 | flach | keine | 0 (Stand 6: 8) |
| 20 | Laufring mit vier Laschen | Ø 189 x 6 | flach | keine | 45 |
| 21 | Karussellplatte mit Nabe Ø 36, D-Sackloch, Madenschraubenloch, Magnettasche, Taschen, Schlitzen, Rastzungen, Stationsbuchstaben | Ø 171 x 16 (mit Nabe, Stand 6: x 18) | Oberseite unten auf dem Bett (Taschen zum Bett offen, Nabe oben), die Buchstaben liegen auf dem Bett | keine | 100 |
| 22 | Rollenböcke (7) | 25 x 11 x 18 | Gabel offen nach oben | keine | 28 |
| 23 | Schlitten mit Fläche X 28, zwei Gleitzonen Ø 10,4 und zwei M4-Kernlöchern Ø 3,7 (Stand 6: LM10LUU-Bohrungen und M4-Einsätze) | Ø 68 x 58 | stehend, Mutternstufe oben | keine | 85 (Stand 6: 75) |
| 24 | Ausleger mit Stempel (ersetzt Winkelstahl und Stempelscheibe) | 40 x 46 x 25 | **liegend auf der Seite (Y oben)**, L-Profil in jeder Schicht | keine | 23 |
| 25 | Brücke mit Rippen, Lagersitz, Klemmnaben | Ø 196 x 19 | Platte unten, Rippen oben | keine | 90 |
| 26 | entfällt ab Stand 8: GT2-Rad 70 Z mit Magnettasche (Direktantrieb, die Magnettasche sitzt jetzt in der Karussellplatte) | Ø 47 x 10 | Nabe oben | keine | 0 (Stand 6: 18) |
| 27 | Schublade (Korpus) mit konischem Bechersitz | 70 x 71 x 19 | Boden unten | keine | 40 |
| 28 | Schubladenfront | 68 x 16 x 28 | aufrecht wie eingebaut | keine | 20 |
| 29 | Podest (Stiel und Scheibe Ø 60 x 1,6) | Ø 60 x 5,8 | Scheibe unten | keine | 8 |
| 30 | Wägezellenbock, Überlastanschlag | je unter 24 x 20 x 2 | flach | keine | 12 |
| 31 | entfällt ab Stand 7: Einführzunge für Schwammstreifen | 160 x 16 x 0,8 | flach | keine | 0 (Stand 6: 6) |
| 32 | entfällt ab Stand 7: Spritzenablage für den Tisch, sechs Fächer | 190 x 70 x 45 | flach | keine | 0 (Stand 6: 45) |

**Material und Einstellung je Teil:**

| Nr | Material und Einstellung |
|---|---|
| 1 | PETG schwarz glänzend, 0,16 mm (0,12 für eine glattere Fläche), 4 Perimeter (1,6), 0 Prozent Infill, 6 Innenrippen 1,2 x 8 |
| 2 | PETG schwarz matt, 0,16 mm, 4 Perimeter, 6 Rippen |
| 3 | PETG schwarz matt, 0,16 mm, 4 Perimeter, 6 Rippen |
| 4 | PETG schwarz matt, 0,16 mm, Wand 2,4, Deckel 2 |
| 5 | Gold-PETG, Wand 1,6 und 1,2 |
| 6 | Gold-PETG, 3 Perimeter, 3 mm Brim |
| 7 | Gold-PETG |
| 8 | Gold-PETG, 0,12 mm, 100 Prozent, 3 mm Brim, die zwei Seitenleisten zusammen auf einem Bett |
| 9 | Gold-PETG |
| 10 | Gold-PETG |
| 11 | 0,12 mm, Basis 0,6 schwarz, ab 0,6 Gold (Filamentwechsel), Schrift 0,6 erhaben |
| 12 | Rauch-PETG, 0,2 mm, 100 Prozent, 245 Grad, Lüfter höchstens 30 Prozent, Außenseite auf glattem Bett |
| 13 | wie unten |
| 14 | Klar-PETG, 0,16 mm, 100 Prozent |
| 15 | PETG schwarz, 15 Prozent Gyroid |
| 16 | PETG schwarz, Wand 3 (7 Perimeter), Tisch 100 Prozent, Brim 5 (hoher schlanker Kasten, Vorschlag, am Probedruck prüfen) |
| 17 | entfällt ab Stand 7 |
| 18 | PETG, 40 Prozent |
| 19 | entfällt ab Stand 7 |
| 20 | PETG schwarz, 30 Prozent |
| 21 | PETG schwarz matt, 25 Prozent, Brim 5 |
| 22 | PETG, 40 Prozent |
| 23 | PETG, 40 Prozent |
| 24 | PETG schwarz, 4 Perimeter, 100 Prozent, 0,16 mm |
| 25 | PETG schwarz, 30 Prozent |
| 26 | entfällt ab Stand 8 |
| 27 | PETG weiß |
| 28 | PETG schwarz glänzend |
| 29 | PETG schwarz |
| 30 | PETG |
| 31 | entfällt ab Stand 7 |
| 32 | entfällt ab Stand 7 |

**Summe Stand 8 etwa 1454 g netto** (PETG schwarz 1309, davon glänzend 170 und matt 495, Rest Innenteile in beliebigem Schwarz; Gold 35; Rauch 46; Klar 24; weiß 40; mit 20 Prozent Zuschlag 1,74 kg; 27 Teilezeilen statt 32, Filament zählt nicht zu den Kosten, Abschnitt 13). Zum Vergleich Stand 6: **Summe etwa 1488 g netto** (PETG schwarz 1343, davon glänzend 170 und matt 495, Rest Innenteile in beliebigem Schwarz; Gold 35; Rauch 46; Klar 24; weiß 40), mit 20 Prozent Zuschlag für Fehldrucke und Probestücke 1.79 kg. Druckzeit realistisch 90 bis 130 Stunden (Hülle 0,16 mm). Größte Teile Sockelschale und Krone Ø 204 (8 mm Rand auf dem 220er-Bett, 3 mm Brim möglich), höchstes Teil Körper unten mit 137. Stand 8: höchstes Teil ist der Motorturm mit 198,5 (Blattgrenze 200, Bett 250), die Druckzeit ist nicht neu geschätzt (Rinne, Ablage, Zunge, Rad und Lagerbock entfallen, der 198 hohe Motorturm kommt dazu).

**PETG, was anders ist als bei PLA (Richtwerte, mit einem Testwürfel prüfen):**

- Düse 235 bis 245 Grad, Bett 75 bis 85 Grad, Lüfter 30 bis 50 Prozent, nur bei Überhängen und Brücken mehr. Außenwände langsam (30 bis 40 mm/s), das gibt die glatte Fläche.
- PETG klebt auf glattem PEI **zu gut**: Klebestift oder Trennmittel auf das Blech, sonst reißt beim Lösen Material aus der Platte. Auf Textur-PEI wird die Unterseite rau, das stört nur bei Scheiben und Gold (dort glattes Blech nehmen).
- Fadenziehen und Tropfen: Düse sauber, Temperatur nicht höher als nötig, Filament trocken (4 bis 6 Stunden bei 65 Grad). Die Hülle zeigt jeden Faden. Sichtflächen nie mit Stützen drucken (die Hülle braucht keine).
- Brücken und Überhänge hängen bei PETG früher durch: längere freie Brücken als 20 mm vermeiden. Im Entwurf kommen nur kurze vor (Fensterbögen R 11, Absatz an der Krone 2 mm).
- Schwinden etwa 0,3 bis 0,5 Prozent: Passungen (Lagersitze 608, Gleitzonen Ø 10,4 im Schlitten (Stand 6: Ø 19,2 für die LM10LUU), M4-Kernloch Ø 3,7, D-Sackloch der Karussellnabe, Stationstaschen) nach dem ersten Probestück mit der Schieblehre prüfen und in `farbmischer.scad` nachziehen.
- Kleben: 2K-Epoxid oder Sekundenkleber (Gel, bei Spalten mit Aktivator). Kein Lösungsmittelkleber, der greift PETG nicht an. Zuerst trocken anlegen und markieren.
- Weißes und transparentes PETG nie mit schwarzen Resten in derselben Düse drucken: Düse vorher mit dem neuen Filament spülen.

**Nachbearbeitung Hülle (Stand 6, ohne Füller, Schliff und Lack):** Körper unten und oben über den innen liegenden Klebering und den Stoß 3 x 0,7 verkleben (2K-Epoxid), die Teilungsfuge bleibt als V-Nut sichtbar. Grate und Fäden mit dem Cutter oder einer Feile entfernen, mit Isopropanol entfetten. Dann die Goldteile aufkleben: Goldring auf den Sockel, Portalrahmen in drei Leistenarten, Kronenring auf die Kronenfase, Goldlippe oben auf die Front, Buchsenring um die Buchse, Namensschild in die Krone. Zuerst zwei Probestücke (Ring 60 x 30 mit einer Goldleiste, 3 breit) komplett aufbauen.

**Druckreihenfolge:** erst die Funktionsteile, Prototyp Stand 8: 24 (der Ausleger zuerst: er ist das einzige tragende Teil, das gedruckt statt aus Stahl ist), 21, 22, 20, 23, 25, 16 (Motorturm) und 15, das sind 8 Zeilen mit etwa 611 g Filament (Stand 6: 21, 22, 20, 23, 24, 25, 26, 16, 15, 17; Druckzeit für Stand 8 nicht neu geschätzt, Stand 7: 35 bis 45 Stunden für 10 Teile), und Funktionsprobe mit echten Spritzen und Wasser, dann Waage und Schublade, dann die Gold- und Scheiben-Probestücke, erst danach die Hüllen (1 bis 4). Pflicht vor dem ersten Hüllendruck: Pappattrappe (17.5), Ventiltest (17.2), Probestücke Gold und Rauchscheibe (17.6, 17.7). Vor dem Großeinkauf drei billige Tests: (1) ein Motor mit A4988 unter Last (Strom per Poti), (2) drei Ventile mit verdünnter Farbe 48 Stunden offen stehen lassen, dann drücken, (3) eine Riemenscheibe und einen Riemen bestellen und mit der Schieblehre prüfen (Breite 6, Bohrung 5 oder 8).

## 13. Stückliste mit Preisen

**Stand 8 (aktueller Standard, `budget = 1`), Preise aus `hardware/einkaufsliste.md` (Stand 2026-11-04).** Filament ist nicht eingerechnet (Filament zählt nicht mit). Umrechnung AliExpress: 1 US-Dollar = 0,92 Euro (Annahme). Von 164,03 Euro sind 134,24 Euro belegt (Suchtreffer, keine Seite im Warenkorb geprüft) und 29,79 Euro geschätzt, Versand ist nirgends enthalten. Standard-Schrauben, Muttern und Unterlegscheiben (M3, M4, M5, Passscheiben 5 x 10 und 8 x 14), Schraubensicherung, Ballast, Füße und Gummiauflage unter dem Stempel (Möbelgleiter, Silikonmatte) und Kleber (2K-Epoxid, Sekundenkleber) kommen gratis aus dem Arbeitsvorrat oder dem Haushalt.

| Gruppe | Teil | Menge | Einzel | Summe in Euro | Status |
|---|---|---|---|---|---|
| Elektronik | ESP32 DevKit 30 Pin (Set mit 2 Boards, 1 Reserve) | 1 | 12,99 | 12,99 | belegt |
| Elektronik | A4988 Treiber (5er-Pack, 2 genutzt), ohne UART und StallGuard | 1 | 4,59 USD | 4,22 | belegt |
| Elektronik | NEMA 17 34 mm 0,4 A (zwei gleiche: Stößel und Karussell direkt) | 2 | 6,49 | 12,98 | belegt |
| Elektronik | Wägezelle 1 kg mit HX711 (Blatt rechnet mit 500 g, Abgleich offen) | 1 | 7,96 | 7,96 | belegt |
| Elektronik | Netzteil 12 V 3 A, 5,5 x 2,1 | 1 | 15,99 | 15,99 | belegt |
| Elektronik | Einbaubuchse 5,5 x 2,1 | 1 | 1,15 | 1,15 | belegt |
| Elektronik | Step-down Mini-360 oder MP1584 | 1 | 1,00 | 1,00 | Schätzung |
| Elektronik | Mikroschalter mit Rollenhebel (10er-Pack, 1 genutzt) | 1 | 1,75 | 1,75 | belegt |
| Elektronik | Hall A3144 (Pack) | 1 | 1,17 | 1,17 | belegt |
| Elektronik | Dupont-Kabel und Stiftleisten statt Lochraster | 1 | 3,00 | 3,00 | Schätzung |
| Elektronik | 2 x 100 µF, Widerstände, 100 nF | 1 | 1,00 | 1,00 | Schätzung |
| Mechanik | T8-Spindel 200 mm, Steigung 2, Messingmutter (2er-Pack) | 1 | 9,99 | 9,99 | belegt |
| Mechanik | Linearwelle Ø 10 x 200 | 2 | 1,09 USD | 2,01 | belegt |
| Mechanik | Kugellager 608ZZ (10er: 7 Rollen, 1 Brücke, 2 Reserve) | 1 | 0,33 USD | 0,30 | belegt |
| Mechanik | Stellring Ø 8 mit Madenschraube (Spindel unter der Brücke) | 1 | 1,00 | 1,00 | belegt |
| Mechanik | GT2-Riemenscheibe 20 Z (Bohrung 5 für Motor 1, Bohrung 8 für die Spindel) | 2 | 1,09 USD | 2,01 | belegt |
| Mechanik | GT2-Riemen geschlossen 158 mm (10er-Mix) | 1 | 0,99 USD | 0,91 | belegt |
| Mechanik | Gewindestange M5 1 m verzinkt | 2 | 1,00 | 2,00 | belegt |
| Mechanik | Magnete 6 x 2 (10er: 4 Krone, 4 Brücke, 1 Schublade, 1 Reserve) | 1 | 0,99 USD | 0,91 | belegt |
| Mechanik | Magnet 5 x 2 für den Hall-Sensor | 1 | 1,00 | 1,00 | Schätzung |
| Startpaket | Wund- und Blasenspritze 50/60 ml Luer (6 im Gerät) | 6 | 0,94 | 5,64 | belegt |
| Startpaket | Silikon-Entenschnabelventile (Pack) | 1 | 5,00 | 5,00 | Schätzung |
| Startpaket | Portionsbecher 60 ml mit Deckel, 100er | 1 | 6,00 | 6,00 | Schätzung |
| Farbe | Marabu 500 ml Cyan | 1 | 12,79 | 12,79 | belegt |
| Farbe | Marabu 500 ml Magenta | 1 | 12,79 | 12,79 | belegt |
| Farbe | Marabu 500 ml Gelb | 1 | 13,49 | 13,49 | belegt |
| Farbe | Marabu Artist Titanweiß 500 ml | 1 | 12,19 | 12,19 | belegt |
| Farbe | Schwarz 500 ml (Marabu, wie Cyan angenommen) | 1 | 12,79 | 12,79 | Schätzung |

**Summen Stand 8 (Filament nicht gerechnet):** Elektronik 63,21, Mechanik 20,13, **Gerät 83,34 Euro**. Mit Startpaket (16,64) **99,98 Euro**, mit der ersten Farbe (64,05) **164,03 Euro**, mit 10 Prozent Puffer für Fehlkäufe rund 180 Euro. Stand 6 zum Vergleich (mit Filament 36,26 und Kleber 7,00): Gerät 159,76 Euro (Stand 5.1: 210,20), mit Startpaket 195,76, mit erster Farbe 245,76, mit Puffer rund 270 Euro. Wer Filament kaufen muss, braucht nach Stand 6 zwei Spulen PETG schwarz 1 kg (40 Euro) und je 250 g Gold (10), Rauch (9), Klar (8) und weiß (8), zusammen 75 Euro, das steht nicht in den Summen oben. Matt-PETG für Körper und Krone ist die zweite schwarze Spule (Körper und Krone brauchen etwa 0,49 kg), wer nur eine Sorte hat, druckt alles glänzend. Eine zweite Flasche Titanweiß (10 Euro) lohnt sich, weil Weiß doppelt so schnell verbraucht wird.

**Was gegenüber Stand 5.1 weg ist (Gerät, Stand 6):** LED-Ring 3,00, LED-Streifen 9,00, 74AHCT125 mit Zubehör 1,50 (Rest 0,50 bleibt), Step-down XL4015 3,00 (jetzt MP1584 1,00), Winkelstahl 4,00, Rauchacryl 8,00, Füllgrund 8,00, Lack hochglanz 8,00, Lack seidenmatt 8,00, Schleifpapier 4,00, Anreibewachs 8,00. **Neu:** Gold-, Rauch-, Klar- und Weiß-PETG, Kleber 7,00, Gummiauflage und Gewindeeinsätze im Sammelposten.

**Was Stand 7 und 8 gegenüber Stand 6 weglassen (Kaufteile):** vier Magnete und Stahlscheiben an den Portalscheiben (Scheiben geklebt), Feuchtrinne mit Deckel, Säulen, Abstreifhalter, Silikonlippen und Schwamm (Risiko: Düsen trocknen an, Ventiltest 17.2 ist Pflicht), Spritzenablage, Einführzunge und Kabelclips (Kabelbinder), Reed-Kontakt, Ballast aus gekauften Scheiben M20 (jetzt gratis aus dem Arbeitsvorrat), TMC2209 gegen A4988, zwei LM10LUU (Gleitzonen im Schlitten, Risiko: etwas mehr Spiel und Reibung, Leichtgängigkeitstest), Gewindeeinsätze M4 (Kernloch Ø 3,7, Risiko: Auszugtest), Gummi- und Filzfüße (Haushalt). Stand 8 zusätzlich: Karussellwelle Ø 8, Riemen 210, eine Riemenscheibe, zwei Stellringe, drei 608-Lager (Lagerbock), Pancake-Motor (jetzt zwei gleiche NEMA 17 34 mm). Nicht belegt sind Wellenlänge und D-Fläche des gekauften Motors, das Drehmoment am Karussell, die Hall-Tasche und die Auszugkraft im PETG.

**Optionen und Sparpfad (Auswahlliste für Johann, Stand 8, aus `hardware/einkaufsliste.md`):**

| Option | Ersparnis | Voraussetzung |
|---|---|---|
| Handy-Ladegerät mit 12 V per PD plus PD-Trigger-Modul statt Netzteil und Einbaubuchse | etwa 13 Euro (Trigger etwa 3 Euro, unbelegt) | Ladegerät liefert 12 V per PD (Aufdruck prüfen), mindestens 36 W. Laptop-Netzteile liefern meist 19 V und gehen nicht |
| Altteile ausbauen (NEMA 17, T8-Spindel, Wägezelle, 608-Lager, GT2-Riemen) | etwa 30 bis 37 Euro (Schätzung) | Typenschild prüfen, Maße passen zum Blatt (die Welle Ø 8 braucht Stand 8 nicht mehr) |
| Hall-Sensor am Karussell weglassen | etwa 2 Euro | Park per App bestätigen, nach Schrittverlust falsche Farbe möglich |
| Fensterscheiben (Klar-PETG) weglassen | nur Filament, kein Geld | Fenster offen, Staub auf den Spritzen, Farben besser sichtbar |
| 30-ml-Spritzen, Gerät 35 mm kürzer | wenig | Spritzen doppelt so oft tauschen, Höhenkette neu rechnen |
| Zwei TMC2209 statt A4988 | kostet 12 bis 16 Euro mehr | leise, UART, StallGuard |

Der Sparpfad von Stand 6 (Summe 18,50, Gerät 154,26, mit Startpaket zusammen 177,26) ist durch Stand 7 und 8 überholt.

Nicht sparen an Wägezelle (Dosierkern) und Lagern. Der Kleber kommt gratis, ist aber Pflicht (2K-Epoxid).

**Laufende Kosten:** Farbe 0,016 bis 0,028 Euro je ml (8 bis 14 Euro je 500 ml), Becher 0,06 Euro, Ventile 0,25 Euro (einige im Jahr), Spritzen 5 bis 8 im Jahr aus der Apotheke, etwa 10 bis 20 Euro, Schwammtuch 0,15 Euro im Monat (nur Stand 6). Verschleißsatz alle 1 bis 2 Jahre: Messingmutter T8 (die zweite liegt im 2er-Pack bei), 10 Ventile (2,50 Euro), den Schlitten neu drucken, wenn die Gleitzonen ausgeschlagen sind (Stand 6: zwei LM10LUU und Schwammtücher, etwa 15 Euro). Die Silikonlippen der Kolben verschleißen mit der Spritze und werden mit ihr getauscht. Strom: Standby und Dosieren unter 15 W, ohne Licht kaum messbar.

**Ehrliche Einordnung:** Gegen Bastelacryl rechnet sich das Gerät nie. Gegen fertig gemischte Farbtöpfchen (0,05 bis 0,15 Euro je ml) erst nach 0,7 bis 4,5 Litern Mischfarbe (Stand 8: 99,98 Euro für Gerät und Startpaket, ohne Filament, geteilt durch die Ersparnis je ml gegenüber 0,016 bis 0,028 Euro je ml eigener Farbe; Stand 6 mit 195,76 Euro: 1,5 bis 6,5 Litern). Es ist ein Geschenk mit Farbtreffer, Wiederholbarkeit und Ritual, kein Sparprojekt.

**Einkauf und Nachschub:** Elektronik und Mechanik in einer Sammelbestellung (AliExpress, etwa drei Wochen) oder teurer bei Amazon. Spritzen, Ventile und Becher immer aus mindestens zwei Quellen: Spritzen aus Apotheke oder Sanitätshaus (Katheterspritze 60 ml über Nacht bestellbar), Entenschnabelventile bei Amazon und Ali, Becher im Supermarkt oder Gastrobedarf. Farbe: Studienacryl 500 ml (Boesner Studio, Gerstaecker Studio oder ähnlich), keine Markenfarbe als Pflicht.

## 14. Was die Firmware wissen muss (Hinweis an die Software-Sitzung)

- **Zwei Achsen (Stand 8, Vertrag mit Firmware und Web-App):** Stößel und Karussell mit je einem A4988 (kein UART, kein StallGuard, Strom per Poti: Stößel 0,5 A, Karussell 0,4 A), Mikroschritt 1/16 fest über MS1, MS2, MS3 an 3,3 V, ENABLE beider Treiber auf GPIO 23 (LOW = aktiv). Pins: Stößel STEP 13, DIR 14, Karussell STEP 27, DIR 26, Mikroschalter Stößel oben 18, Hall 19, HX711 DOUT 32 und SCK 33 (Abschnitt 9). Stand 6: TMC2209 über UART, StallGuard als Überlastschutz.
- **Sieben Plätze:** Karussell im Direktantrieb, 200 x 16 = 3200 Mikroschritte je Umdrehung, je Platz 3200 / 7 = 457,142857 (nicht ganzzahlig). Platz 0 ist leer und Park. Belegung 1 W1, 2 Y, 3 M, 4 C, 5 K, 6 W2 (Abschnitt 7.2). Station p bei q = round(p · 3200 / 7), die Position intern als Bruch oder auf 22 400 Schritte (49 Plätze) führen, Vorzeichen und DIR bei der Inbetriebnahme prüfen (Abschnitt 7.1). Immer der kürzere Weg, höchstens 3 Plätze. Stand 6 und 7: 1600 Schritte je Platz, 11 200 je Umdrehung, Station p bei q = -p · 1600.
- **Drehsperre:** Das Karussell dreht nur, wenn der Endschalter oben geschlossen ist. Vor jeder Drehung Stößel auf S_park.
- **Referenz:** Stößel Mikroschalter oben (Schließer gegen GND, INPUT_PULLUP, GPIO 18, gedrückt = oben = Park). Karussell Hall A3144 (GPIO 19, INPUT_PULLUP, Open-Collector, aktiv LOW bei Magnet, Magnet in der Karussellnabe) markiert Platz 0 (Park). `POST /home` fährt erst den Stößel hoch, dann das Karussell auf Hall-Park.
- **HTTP-Schnittstelle (alle Antworten JSON, CORS an, Vertrag Stand 8):** `GET /status` (state idle, homing, moving, dosing oder error, homed, carousel_pos, station, plunger_mm, weight_g, fill_ml je W1, Y, M, C, K, W2, job mit active, id, target_g, done_g, step, steps, error), `POST /home`, `POST /tare`, `POST /scale` mit known_g, `POST /dispense` mit grams je Farbe (hell nach dunkel, K zuletzt, Fehler 409 wenn nicht referenziert, Waage nicht tariert oder Spritze zu leer), `POST /prime` mit id und ml, `POST /refill` mit id (setzt auf 50 ml), `POST /park`, `POST /stop`, `GET` und `POST /config` mit g_per_ml und ml_per_mm je Station. Die Web-App liegt auf LittleFS (`/`, `/farbmath.js`, `/mixbox.js`) und kennt nur C, M, Y, W, K: bei „W“ wählt die Firmware die Weiß-Spritze mit mehr Rest.
- **Park:** Nach jedem Rezept, nach jedem Tausch und nach 30 s Leerlauf auf q = 0. Dann hängt keine Düse über dem Becher.
- **Dosieren nach Gewicht** mit HX711 (80 Hz, Mittelwert über 8 Werte), Ablauf Abschnitt 10. Messen nur, wenn das Karussell steht. Tara vor jeder Farbe. Kontakt zur Kolbenplatte: mehr als 0,2 g in drei aufeinanderfolgenden Mittelwerten und Stempel höchstens 3 mm unter der gespeicherten Platte, kein Taster.
- **Buchführung je Station:** Kolbenplattenhöhe (mm), Rest in ml, gelernter Nachlauf in g, g je mm. Persistent im Flash. Nach einem Tausch Plattenhöhe unbekannt, Startannahme 320,8 und langsame Anfahrt ab S = 322,8. Station sperren unter 2 ml Rest.
- **Weiß doppelt:** W1 zuerst bis 2 ml Rest, dann W2. Meldung „Weiß 1 tauschen“.
- **Startwerte:** 1 ml = 2858 Mikroschritte, Dichte Weiß 1,4 g/ml, Schwarz 1,1 g/ml, sonst 1,25 g/ml. Die Waage ersetzt diese Werte nach der ersten Dosierung.
- **Grenzen:** Gesamtmenge 10 bis 50 g. Kleinste Teilmenge 0,1 g, darunter weglassen und Abweichung melden.
- **Rückhub:** nach jeder Teilmenge 1,3 mm zurück (1 mm Druckentlastung plus Spindelspiel), kein Zurückziehen des Kolbens. Dosierstellung immer von oben anfahren.
- **Fließende:** Gewichtszunahme unter 0,01 g/s über 1 s, Zeitgrenze 20 s.
- **Becher- und Schubladenprüfung:** Waage im Fenster leere Schublade plus 2 bis 15 g und ruhig (Stand 6 zusätzlich Reed geschlossen, ab Stand 7 ohne Reed), sonst keine Dosierung und Meldung „Schublade ganz schließen“.
- **Kein Licht (Stand 6):** Die LEDs entfallen vollständig. GPIO 25 und die Bibliothek für WS2812 werden nicht mehr gebraucht, Helligkeitsgrenze, Lichtzustände und Farbverläufe entfallen. Fortschritt, „Fertig“, Fehler und die Erinnerungen (Wasser nach 28 Tagen als Startwert, Lippen nach 15 Dosierungen) zeigt nur die App. Optional ein aktiver Summer auf GPIO 25 für „Fertig“ und Fehler.
- **Spülen:** nach mehr als 3 Tagen ohne Dosierung „Düsen spülen“ anbieten (0,3 g je Station in einen Spülbecher).
- **Wechselmodus:** Station nach vorne, Stößel oben, Motoren halten, auf Bestätigung warten, dann Park.
- **Gerätename:** Der Name im Kronenschild (Spitzname plus „Atelier“) als Seitentitel der Webseite, daneben die aktuelle Mischfarbe (Wunsch der Künstlerin). Ohne Licht am Gerät trägt die App die ganze Rückmeldung: großer Fortschrittsring in der Zielfarbe, „Fertig“ als eigener Bildschirm.
- **Nochmal und Lieblingsmischungen:** letzte Mischung mit einem Tipp wiederholen, Mischungen mit Namen speichern.
- **Weiß knapp:** Warnung, sobald W1 und W2 zusammen unter 20 ml liegen.
- **Nicht mehr gültig aus Stand 4, 5 und 5.1:** Kontakttaster im Stempel, Dosierung nach Strecke, 40 Vollschritte je Station, fünf Stationen, LED auf GPIO 5 oder 25, alle LEDs und Lichtzustände (WS2812, `Adafruit_NeoPixel`, `LED_COUNT`, `LED_BRIGHTNESS`, `PIN_LED_RING`), g_per_ml-Kalibrierung von Hand, 48 LEDs, Kontaktschwelle 0,05 g, Rückhub 1 mm. Die Firmware in `firmware/` ist noch für fünf Spritzenpumpen mit LED-Ring geschrieben und muss auf Stand 8 umgebaut werden (Vertrag oben). Ab Stand 7 und 8 außerdem nicht mehr gültig: TMC2209 mit UART und StallGuard (GPIO 16 und 17), Reed auf GPIO 19, DIR Stößel 33, STEP Karussell 14, DIR Karussell 32, HX711 auf 34 und 4, Hall auf 21, 1600 Schritte je Platz und 11 200 je Umdrehung, Übersetzung 1 : 3,5, Riemen 210 und die Wasser- und Lippenerinnerungen der Feuchtrinne.

## 15. Kollisionsprüfungen mit Sollabstand

Geprüft mit `python3 hardware/render_farbmischer.py --pruefung`: Spritze (Ventil, Konus, Zylinder, Flansch 45 x 32 radial, Kolbenstange 12 x 12, Kolbenplatte Ø 38) an allen sechs Stationen, Karussell in 1-Grad-Schritten über 360 Grad, Kolbenplatte bei leer (231,5), 2 ml Rest (235,1), halb (276,2) und 50 ml (320,8), gegen alle festen Teile mit Stößel in Parkstellung. Dazu die mitdrehenden Rollenböcke über 360 Grad und die Entnahme einer vollen Spritze radial nach vorne über 0 bis 130 mm. Abstände sind exakt in 2D gerechnet und in 3D als Prismen kombiniert. Sollabstand: drehend gegen fest mindestens 2,0, Entnahme mindestens 3,0, Ventil gegen Becher mindestens 5,0, Stempel über voller Kolbenplatte mindestens 10,0, fest gegen fest in der Hülle mindestens 1,5. Die Tabelle ist die Ausgabe des Skripts, Stand 6: 50 von 50 bestanden (fünf LED-Prüfungen entfallen, vier neu: Ausleger gegen Brücke 11, Stempelfuß auf Kolbenplatte 12, Ausleger in S_min 13, Goldring gegen Sockelfalz 47; die Nummern sind neu fortlaufend). Dieser Abschnitt beschreibt Stand 6, das Skript `render_farbmischer.py` wird für Stand 8 gerade überarbeitet.

Messgrößen: Nr 33 ist der kürzeste Abstand zwischen den Konturen zweier Nachbarschlitze mit Halbkreisende R 16 (17,46). Der Wert 6,75 aus Stand 5 galt für ein eckiges Schlitzende und war falsch. Nr 24 misst den Zylinder gegen die Rampe am Laufringende, Nr 40 den Zuganker gegen Schubladenwand und Schiene (beide bei \|Y\| 35).

| Nr | Prüfung | Soll | Ist | ok |
|---|---|---|---|---|
| 1 | Schlitten tiefste Stellung gegen Karussellplatte oben | 2 | 2,07 | ja |
| 2 | Wellenende Ø10 gegen Karussellplatte oben | 2 | 2,07 | ja |
| 3 | Laufring (fest, innen r 74,5) gegen Spritzenzylinder beim Drehen | 2 | 2,50 | ja |
| 4 | Zuganker gegen Rollenbock beim Drehen | 2 | 2,50 | ja |
| 5 | Zuganker gegen Laufrolle beim Drehen | 2 | 3,78 | ja |
| 6 | Feuchtrinne gegen Ventil beim Drehen | 2 | 2,30 | ja |
| 7 | Schwamm nass gegen Ventil | 1,5 | 2,00 | ja |
| 8 | Schlitten (r 34) gegen Kolbenplatten beim Drehen | 2 | 4,00 | ja |
| 9 | Schlitten tief gegen Nachbar-Kolbenplatten | 2 | 4,00 | ja |
| 10 | Stempel in Park gegen Kolbenplatte 50 ml | 10 | 10,00 | ja |
| 11 | Ausleger (Arm, Platte S + 48) in Park gegen Brücke (S + 50) | 2 | 2,00 | ja |
| 12 | Stempelfuß Ø 25 (X 53) ganz auf Kolbenplatte Ø 38 (Rand) | 1,5 | 2,50 | ja |
| 13 | Ausleger in S_min gegen Karussellplatte und Laufring | 2 | 12,07 | ja |
| 14 | Führungswellen Ø10 gegen Flansch beim Drehen | 2 | 7,93 | ja |
| 15 | Zuganker gegen Flansch beim Drehen | 2 | 6,91 | ja |
| 16 | Abstreiflippe gegen Konus (nur das Ventil darf streifen) | 2 | 9,00 | ja |
| 17 | Rollenbock gegen Körperwand | 2 | 10,90 | ja |
| 18 | Arm und Stempel beim Dosieren (tief) gegen Nachbar-Kolbenplatten | 3 | 13,07 | ja |
| 19 | Motor 1 Unterkante gegen Kolbenplatte 50 ml | 10 | 26,00 | ja |
| 20 | Ventil gegen Becherrand (senkrecht) | 5 | 7,00 | ja |
| 21 | Nachbarventil beim Dosieren gegen Becherrand (waagrecht) | 5 | 13,96 | ja |
| 22 | Nächstes Ventil in Parkstellung gegen Becherrand | 5 | 13,96 | ja |
| 23 | Rolle im Stillstand gegen Rand der Laufringlücke | 2 | 3,96 | ja |
| 24 | Entnahme: Zylinder gegen Laufringende | 3 | 4,28 | ja |
| 25 | Entnahme: Zylinder gegen Rollenbock bei ± 25,7 | 3 | 6,52 | ja |
| 26 | Entnahme: Flansch gegen Rollenbock | 3 | 10,13 | ja |
| 27 | Entnahme: Kolbenplatte gegen Portalöffnung (seitlich und oben, R 24) | 3 | 7,63 | ja |
| 28 | Entnahme: Kolbenplatte gegen Stempel oben | 3 | 10,00 | ja |
| 29 | Entnahme: Kolbenplatte gegen Nachbar-Kolbenplatten | 3 | 11,46 | ja |
| 30 | Entnahme: Zylinder gegen Nachbarzylinder | 3 | 19,46 | ja |
| 31 | Entnahme: Ventil und Konus gegen Feuchtrinne | 3 | 30,68 | ja |
| 32 | Flanschtaschen untereinander (Innenecken R 5) | 2 | 3,12 | ja |
| 33 | Zylinderschlitze untereinander | 4 | 17,46 | ja |
| 34 | Rollenbock gegen Zylinderschlitz der Platte | 3 | 5,51 | ja |
| 35 | Motor 1 gegen Schlitten in Park | 2 | 3,85 | ja |
| 36 | Stellring gegen Schlittentasche (Tasche 9 tief, Eintauchen 6) | 2 | 3,00 | ja |
| 37 | GT2-Rad 70 Z gegen Becher (Z 43 bis 51) | 3 | 4,66 | ja |
| 38 | Motor 2 gegen Lagerbock | 3 | 16,65 | ja |
| 39 | Zuganker -32 gegen Wägezelle | 3 | 10,90 | ja |
| 40 | Zuganker ± 32 gegen Schublade (Wand \| Schiene) | 3 | 10,46 | ja |
| 41 | Platinenecke gegen Hülle (Z 97 bis 100) | 2 | 2,86 | ja |
| 42 | Wägezelle festes Ende gegen Sockelwand | 3 | 5,26 | ja |
| 43 | Überlastanschlag unter dem Lastende | 0,8 | 0,80 | Einstellmaß |
| 44 | Zuganker gegen Karussellplatte (Rand r 85,5) beim Drehen | 2 | 2,50 | ja |
| 45 | Mutter M5 in Tasche (Fläche außen) gegen Körperwand | 1,5 | 1,90 | ja |
| 46 | Laufringlasche (Ende r 94,5) gegen Körperwand | 1,5 | 1,90 | ja |
| 47 | Goldring innen r 97,3 gegen Sockelfalz (r 97,1) | 0,2 | 0,20 | ja |
| 48 | Zuganker seitlich gegen Fensterscheibe (26 breit) | 5 | 14,60 | ja |
| 49 | Ballaststapel gegen Nachbarteile (Grundriss) | 2 | 5,15 | ja |
| 50 | Stempelachse innerhalb der Flanschauflage (bis r 57) | 2 | 4,00 | ja |

Die Schubladenfront folgt der Sockelkontur, eine rechteckige Front 70 breit würde an den Ecken 0,2 über die Kegelfläche stehen.

Jedes neue Formdetail und jede gemessene Spritzenmarke muss diese Liste mit `--pruefung` erneut bestehen. Knapp sind: Schlitten und Wellenende gegen Platte (2,07), Laufring gegen Zylinder (2,50), Zuganker gegen Rollenbock und Platte (2,50), Rinnendeckel gegen Ventil (2,30), Ausleger gegen Brücke (2,00), Muttern und Laschen gegen Körperwand (1,90, fest gegen fest). Wenn eine Spritzenmarke einen längeren Zylinder, einen dickeren Flansch oder einen Zylinder Ø 30,5 hat, verschiebt sich die Kette. Deshalb die Spritzenmessung (17.1) vor dem Druck der Teile 11 und 12.

## 16. Rechnungen (Stand 5 aus fm5b.py und fm5d.py, geänderte Zeilen für Stand 5.1, 6, 7 und 8 nachgerechnet)

| Größe | Ergebnis |
|---|---|
| Druck bei 100 N am Kolben | 1,79 bar (Kolbenfläche 560 mm²) |
| Spindel T8 x 2 | Wirkungsgrad 0,36, 0,087 Nm für 100 N, bei 0,25 Nm 286 N, selbsthemmend (5,2 gegen 8,8 Grad). T8 x 4 wäre es nicht (10,3 Grad) |
| Führungswellen Ø 10, 150 frei | Stempel senkt sich unter 100 N auf r 53 um etwa 0,22 mm, 27 MPa (Ø 8 wären 0,54 mm). Die Waage regelt das aus |
| Moment am Schlitten | 5,3 Nm (100 N auf r 53), je LM10LUU-Ende etwa 66 N (C etwa 590 N). Stand 7 ohne LM10LUU: zwei Gleitzonen je 14 im Abstand 44, je Zone etwa 60 N (5,3 Nm / 2 Wellen / 44 mm), Flächenpressung 0,41 MPa auf 10,4 x 14 mm projiziert, für PETG auf Stahl unkritisch (Handrechnung), Reibung und Spiel bleiben am Prototyp zu prüfen (17.3) |
| Ausleger PETG (Platte 8, Arm 25 x 8, Stempelfuß Ø 25), liegend gedruckt | Auslegung auf die Haltekraft des Motors, nicht auf die Dosierkraft: 250 N (0,26 Nm, T8 x 2, Wirkungsgrad 0,3), StallGuard schaltet früher ab. Biegung am Plattenrand: 250 N · 17 mm = 4250 N·mm, W = 25 · 8² / 6 = 266.7 mm³, **15.9 MPa** (PETG in der Schichtebene etwa 45 MPa Annahme, Sicherheit 2.8; bei 150 N 9.6 MPa). Durchbiegung am Stempel bei 100 N 0.08 mm (E = 2000 MPa, ohne Rippen gerechnet). Kippmoment 250 N · 25 mm = 6250 N·mm, oberer M4-Einsatz im Abstand 32 zur Kippkante: Zug **195 N** (117 N bei 150 N), Stand 6: ein M4-Messing-Gewindeeinsatz in PETG hält mehrere 100 N. Stand 7: Kernloch Ø 3,7 x 12 ohne Einsatz, die Schraube schneidet das Gewinde selbst, eine belegte Auszugkraft in Newton gibt es nicht, deshalb Auszugtest Pflicht (Wasserkanister 20 kg, etwa 196 N), hält es nicht, Gewindeeinsatz M4 nachkaufen. Pressung an der Kippkante 250 + 195 N auf 25 x 3 mm = 5.9 MPa. Das Teil liegt beim Druck auf der Seite, damit die Last in der Schichtebene und nicht quer zu den Schichten (etwa 30 MPa) liegt. **Muss am Prototyp mit 250 N (Kofferwaage am Stempel, Hebel) bestätigt werden;** hält er nicht, Rippen höher und Arm 10 dick (Z-Spiel zum Schlitten bleibt, Prüfung 15) |
| Flanschauflage | Stempel auf r 53, die Auflage des Flansches reicht an den Seiten bis r 57: die Kraft liegt 4 mm innerhalb, kein Kippmoment aus der Auflage |
| Zuganker M5 | 1,8 MPa in der Stange, 1,5 MPa unter der Mutter in der PETG-Tasche |
| Karussell | 0,75 kg mit sechs vollen Spritzen, Trägheit 0,0031 kg m². Beschleunigen 0,031 Nm, Rollreibung plus zwei Lippen 0,031 Nm, zusammen 0,062 Nm an der Platte. **Stand 8: direkt am Motor 2 ohne Getriebe, Haltemoment 0,28 Nm, Reserve 4,5-fach gegen das Haltemoment (im Lauf weniger, Test am Prototyp, 17.3).** Stand 6 und 7: am Motor nach 1 : 3,5 0,018 Nm, Pancake bei 0,4 A etwa 0,05 Nm, Reserve etwa 2,8-fach, bei 0,6 A etwa 4-fach (Stand 5 rechnete mit dem Haltemoment bei Nennstrom und kam auf 7-fach) |
| Reibung prüfen | Kofferwaage am Plattenrand (r 85,5): Stand 8 unter 1,6 N bedeutet unter 0,14 Nm, also höchstens das halbe Haltemoment (Reserve 2); Stand 6 und 7: unter 0,58 N bedeutet unter 0,05 Nm (Muss der Controllerin, Pflicht in 17.3) |
| Rollen | vordere Rollen bei ± 25,7 tragen beim Dosieren zusammen etwa 102 N, 608 statisch 1370 N |
| Motorwelle Karussell (Stand 8) | Welle Ø 5 trägt nur Drehmoment (Haltemoment 0,28 Nm, Bedarf 0,062 Nm). Das Gewicht der Platte (0,75 kg mit Spritzen) und die Axiallast der Dosierung (bis 250 N) laufen über die Rollenböcke auf den Laufring. Datenblätter und Foren nennen für NEMA 17 nur etwa 10 bis 49 N Axiallast (Quellen in `hardware/einkaufsliste.md`, Kurzrecherche Direktantrieb). Nabe aus PETG mit Madenschraube M3 auf der D-Fläche: leichte Last, die Schraube nicht zu fest anziehen (reißt PETG) |
| Riemen | GT2 20 : 20 mit 158 mm bei Achsabstand 59 (Stößel). Karussell ab Stand 8 ohne Riemen (Stand 6 und 7: GT2 20 : 70 mit 210 mm bei Achsabstand 57,8) |
| Durchfluss, 10 ml bei 100 N (Poiseuille, 15 Prozent Ventilverlust) | Katheter 3,5 x 20: 7 s bei 20 Pa·s, 18 s bei 50, 36 s bei 100. Luer 2,0 x 12: 40, 101 und 201 s |
| Masse | etwa 3,8 kg mit 0,48 kg Ballast, Schwerpunkt etwa Z 190 (geschätzt: Krone 7,5 höher, Ballast 20 g leichter als Stand 5). Stand 8: etwa 3,7 kg mit 0,4 kg Ballast, Schwerpunkt etwa Z 195 (Schätzung, nicht gewogen: Rinne, Säulen, Lagerbock, Welle, Rad, Pancake und 0,08 kg Ballast entfallen, der Motorturm mit 145 g und der zweite 34-mm-Motor kommen dazu und sitzen hoch) |
| Kippen | sechs Füße auf r 92, ungünstigste Richtung zwischen zwei Füßen r 79,7: Kippwinkel 23 Grad, seitliche Kippkraft oben (Z 407) 7,3 N (Stand 8 bei 3,7 kg: F = m g · 79,7 / 407 = 7,1 N, Kippwinkel bei Schwerpunkt Z 195 etwa 22 Grad), Kabelzug an der Buchse (Z 30) erst ab 99 N. Ohne Ballast Schwerpunkt etwa Z 215 |
| Druck | Stand 8: Filament 1,45 kg netto, 1,74 kg mit Zuschlag (Abschnitt 12, nicht in den Kosten). Stand 6: 1,49 kg netto, 1,79 kg mit Zuschlag, 90 bis 130 Stunden. Gold-PETG nur 35 g, die Goldteile sind in Minuten gedruckt |
| Strom | Motoren 0,5 bis 0,65 A bei 12 V, ESP32 und Sensoren etwa 0,3 A bei 5 V, aus 12 V gesamt unter 1,2 A von 3 A. Ohne LEDs kein 5-A-Wandler nötig |

## 17. Bauplan in sicheren Schritten

1. **Spritzen messen:** drei Marken (BD, Omnifix, eine aus der Apotheke vor Ort). Flansch (Länge, Breite, Dicke, Eckradius), Kolbenplatte Ø, Zylinder außen, Länge Flansch bis Zylinderende, Konuslänge, Hub bei 50 ml. Werte in dieses Blatt, in `render_farbmischer.py` und in `farbmischer.scad` eintragen und `--pruefung` laufen lassen. Vor dem Druck der Teile 11 und 12.
2. **Ventiltest (Pflicht vor dem Hüllendruck):** fünf gefüllte Spritzen mit Ventil zwei Wochen lang senkrecht über einem feuchten Schwammstreifen lagern, jeden zweiten Tag 1 g drücken. Ventil öffnet, schließt, tropft nicht, verklebt nicht? Rückfallebene: offene Silikondüse (Schlauch 4 x 6, 6 lang), die Rinne übernimmt dann allein das Feuchthalten. Parallel die Rinne mit Deckel und nassem Schwamm zwei Wochen stehen lassen und wiegen: daraus folgt das echte Nachfüllintervall (nur Stand 6). Stand 7 und 8 haben keine Rinne: zusätzlich der Schnelltest aus der Einkaufsliste, drei Ventile mit verdünnter Farbe 48 Stunden offen stehen lassen, dann drücken.
3. **Funktionsprobe:** Karussellplatte, Rollenböcke, Laufring, Motorturm (Stand 6 und 7: Lagerbock), Grundplatte, Zuganker, Brücke, Schlitten und gedruckten Ausleger (liegend, 100 Prozent) drucken und ohne Hülle aufbauen. Den Ausleger zuerst mit Gewicht oder Kofferwaage auf 250 N belasten und die Durchbiegung messen. Mit Wasser und dann mit Farbe dosieren und wiegen, Drehreibung mit der Kofferwaage messen (Pflicht), Rundlauf der Rollen prüfen (Laufring über Beilagen justieren). Bei 100 N beobachten, ob die Spritze im Flansch kippt. Lautstärke mit einer Handy-App in 1 m messen. Stand 7 und 8 zusätzlich: den Schlitten auf die Wellen stecken und von Hand auf Leichtgängigkeit prüfen (klemmt er, Bohrung auf 10,5 aufweiten, Wellen leicht einfetten). Die M4-Kernlöcher im Schlitten mit einem Auszugtest belasten (Schraube mit Federwaage oder Wasserkanister 20 kg, rechnerisch 195 N am oberen Punkt), hält das Gewinde nicht, Gewindeeinsatz M4 nachkaufen. Am gekauften Motor 2 Wellenlänge ab Flansch und D-Fläche messen (Modell 22 mm, Fläche 2,0 von der Achse) und Nabe und Sackloch der Karussellplatte darauf anpassen. Karussell mit Motor 2 (0,4 A per Poti) ohne Schrittverlust alle sieben Plätze fahren, Reibung mit der Kofferwaage am Plattenrand unter 1,6 N. Hall-Tasche und Magnet am Probestück prüfen (Bauform des A3144, Luft 1,5).
4. **Waage und Schublade:** Podest, Schienen, Schublade, Überlastanschlag. Kufenluft 0,5 ± 0,2 mit der Fühlerlehre einstellen. Stabilität der Waage bei laufenden Motoren prüfen, Rauschen messen (Kontaktschwelle 0,2 g bestätigen), mit Druck auf die Front und schief stehendem Becher testen, ob die Warnung kommt.
5. **Pappattrappe (Pflicht vor dem ersten Hüllendruck):** Rohr Ø 196 x 407 schwarz, Kappe Ø 204 x 66, eine Woche auf ihren Schreibtisch (das Geschenk verraten Johann und eine Freundin zur Not als „Lampe in Planung“). Wirkt es zu mächtig, die Krone um bis zu 7 mm kürzen: dafür die Naben der GT2-Scheiben auf 1 mm abdrehen und die Scheiben mit Madenschraube M3 im Zahnkranz sichern (Abschnitt 18).
6. **Rauchscheibe und Klarscheibe:** eine Portalscheibe-Hälfte (120 x 78 x 2) und eine Fensterscheibe (26 x 76 x 1,6) in Rauch- und Klar-PETG drucken, vor Fenster und Lampe halten. Reicht die Durchsicht, weiter. Sonst Temperatur und Geschwindigkeit ändern, dünner drucken (1,2 mm) oder Scheiben weglassen (Fenster offen).
7. **Probestücke:** Goldring und ein Stück Portalrahmen (`rahmen_oben`) drucken, anlegen, biegen, auf ein Probestück der Hülle kleben (Ring 60 x 30 mit einer Leiste). Namensschild zweifarbig drucken (Filamentwechsel bei 0,6) und in eine Probe-Krone kleben. Dann die Hüllen drucken und die Goldteile aufkleben.
8. **Dokumente nachziehen:** README ist auf Stand 6 (Stückliste nach Abschnitt 13). Die Netzliste in `electronics/` gehört zum Fünf-Motor-Entwurf und braucht für dieses Gerät eine neue Fassung (zwei Treiber mit UART, HX711 an 3,3 V, ohne LEDs und ohne Pegelwandler), oder Lochraster nach Abschnitt 9.

## 18. Risiken

| Risiko | Gegenmittel |
|---|---|
| Ventil verklebt mit Pigment | Test in Schritt 17.2, Rinne als zweite Sicherung, Ventile kosten 0,25 Euro |
| Spritzenmaße weichen ab (längerer Konus, größere Kolbenplatte) | messen, Kette neu rechnen. Ein 5 mm längerer Konus frisst 5 der 7 mm über dem Becher. Ausweg: Becher 28 statt 33 hoch |
| Rollen rattern oder Platte verzieht sich | Laufring justierbar, Platte mit Brim und 25 Prozent Infill. Rückfallebene: zwei Lager 6808 auf einer Hülse um einen festen Mittelturm (Konzept 3) |
| Waage driftet oder sieht Motorvibration | nur im Stillstand messen, Tara vor jeder Farbe, Silikonentkopplung, HX711-Leitungen kurz |
| Schublade berührt beim Wiegen die Schienen | Rampe mit 1 mm Absenkung, Kufenluft 0,5 ± 0,2 über Beilagen eingestellt, Tara-Fenster und Ruheprüfung in der Firmware |
| Schwamm trocknet aus oder schimmelt | Deckel, Erinnerung (Start 28 Tage, nach Messung anpassen), Streifen alle 2 bis 3 Monate tauschen, ein Tropfen Essig ins Wasser |
| Rauch- oder Klar-PETG druckt trüb | Scheiben dünn drucken (1,2 mm), langsam und heiß, Außenseite auf glattem Blech; sonst Scheiben weglassen. Die Sichtbarkeit der Farben im Fenster hängt am Raumlicht |
| Gold-Leisten lösen sich oder biegen nicht sauber | zuerst Probestück (17.7), Epoxid statt Sekundenkleber, Malerkrepp als Klemme, Leisten warm (Haartrockner) biegen. Rückfallebene Messingband 4 mm |
| Teilungsfuge Z 235 wirkt unsauber | Fasen 0,5 prüfen, Epoxid nicht in die V-Nut laufen lassen (Malerkrepp). Fuge ist gewollt, ein Versatz der Hälften über 0,3 mm fällt auf, deshalb beim Kleben auf einer ebenen Platte ausrichten |
| Gedruckter Ausleger biegt oder bricht | Auslegung 16 MPa bei 250 N, liegend gedruckt, 100 Prozent Füllung. Rückfallebene: Winkelstahl 40 x 40 x 4 (Stand 5.1), Platte und Löcher sind gleich |
| PETG-Hülle fadenzieht oder zeigt Z-Naht | Filament trocknen, Retraktion prüfen, Naht hinten bei θ 180 |
| Höhe 407 wirkt zu hoch | Pappattrappe; Krone bis 7 mm kürzer nur mit abgedrehten GT2-Naben und Madenschraube im Zahnkranz (fummelig, deshalb nicht der Normalfall) |
| Spritze kippt im Flansch | Stempel auf r 53, Beobachtung in 17.3 |
| Gerät zu laut für die WG | StealthChop, Dämpfer, Messung in 17.3 |
| Kosten über dem Wunsch der Controllerin | Gerät liegt in Stand 6 deutlich unter 175 bis 185 (Abschnitt 13), Startpaket und Farbe kommen dazu |
| Motor 2 zu schwach für die Platte, oder die Welle trägt Axiallast (Stand 8) | Haltemoment 0,28 Nm gegen Bedarf 0,062 Nm (4,5-fach, im Lauf weniger), Test 17.3. Die Platte läuft auf den Rollen, die Welle trägt nur Drehmoment. Rückfallebene: Riemenantrieb 1 : 3,5 wie Stand 7 (Lagerbock, Welle, 70-Z-Rad, Riemen 210), nur in der Git-Historie (Commit e63ffb5), nicht mehr im SCAD |
| Wellenlänge oder D-Fläche des gekauften Motors weicht ab (Stand 8) | messen, bevor die Karussellplatte gedruckt wird, `schaft_l` und `schaft_flach` in `farbmischer.scad` nachziehen. Das Wellenende liegt 1,5 unter der Plattenoberseite, ein längeres Ende setzt auf: Motor tiefer setzen (`z_m2_top`) oder Welle kürzen |
| Madenschraube reißt die PETG-Nabe, oder die Nabe rutscht auf der Welle (Stand 8) | Schraube auf der D-Fläche, nicht zu fest, scharfe Kanten der D-Fläche vermeiden. Rückfallebene (nicht erprobt): zusätzlich eine dünne Schicht Epoxid |
| Gleitzonen im Schlitten klemmen oder haben zu viel Spiel (Stand 7) | Leichtgängigkeitstest vor dem Einbau, Bohrung auf 10,5 aufweiten, Wellen einfetten. Rückfallebene: LM10LUU (2 Stück, 7,26 Euro) mit Bohrung Ø 19,2 wie Stand 6 |
| M4-Kernloch im Schlitten hält den Zug nicht (Stand 7) | Auszugtest 17.3, sonst Gewindeeinsatz M4 |
| Ohne Feuchtrinne trocknen die Düsen an (Stand 7) | Ventiltest 17.2 ist Pflicht, vor jeder Session Düsen wischen, im Zweifel Luer-Kappen oder Spülen |
| Heißkleberpunkte halten die Portalscheibe nicht oder lassen sich beim Spritzentausch schlecht lösen (Stand 7) | am Probestück prüfen, sonst die Magnete und Stahlscheiben nachrüsten (`budget = 0`, Magnettaschen im Falz) |
| Die Schublade stößt am Motorturm an (Stand 8) | Handrechnung mit OpenSCAD-Schnitt: die Schublade beginnt bei X 22, der Turm reicht bis X 25,2, der Schubladenboden überlappt 3,2 x 50,4 x 1,5. **Behoben:** `schub_x0 = 27,2` (2 mm Luft zum Turm), Prüfung Nr. 44 im Skript besteht, Becher unten Ø 47 bei X 57 beginnt erst bei X 33,5 |
| Kein Teil ist bisher gebaut | Schritte 17.1 bis 17.4 vor jeder Hülle |

## 19. Wie die Kritik der vier Rollen abgedeckt ist

*Stand 6, kurz:* Die Absätze unten sind die Abnahme von Stand 5.1. Von ihnen gelten Maße, Mechanik und Kollisionen unverändert, Oberfläche, Licht und Gold sind durch Stand 6 ersetzt (Abschnitt 0). Kosten-Controllerin: Gerät unter dem Ziel, keine Spritzgussteile, keine Lacke. Produktdesignerin: Goldlinien sind jetzt Gold-PETG-Teile, die Teilungsfuge ist gewollt und sichtbar, die Hülle verliert den Lack-Hochglanz an Körper und Krone, Sockel und Front bleiben glänzend. Ingenieur: der Ausleger ist das einzige tragende Teil, das von Stahl auf PETG wechselt, mit Nachweis in Abschnitt 16 und Rückfallebene Winkelstahl. Künstlerin: der Verlust ist das Licht (Fenster und Bühne leuchten nicht mehr), dafür sieht sie die Farben klar im Tageslicht und der Becher steht auf Weiß. Das ist der Preis des Wunsches nach PETG ohne LED.


**Kosten-Controllerin:** ehrliche Rechnung in drei Stufen (210, 246, 296) plus Filament-Neukauf und Puffer, Sparpfad als Liste mit richtiger Summe, Amortisation korrigiert (1,9 bis 8,2 Liter gegen Fertigmischung, gegen Bastelacryl nie). Apothekenpreis für Spritzen, realistische Druckzeit, Verschleißsatz. Wand 4 Perimeter, 0 Prozent Infill an den Schalen, Rippen 1,2 x 8. Ballast 0,48 kg. Rollen 608 statt Kugeln, Reibung unter 0,05 Nm messbar. Nachschub nur Standardware aus mindestens zwei Quellen. Lochraster, keine Fünf-Motor-Platine, keine Kupplungen, kein Messing. Kein Teil über Ø 204.

**Produktdesignerin:** Schwarz und Gold, Füller, Schliff, Lack, Hochglanz gegen Seidenmatt. Sockel als Kegel, Krone mit 4 mm Überstand und Fase, seidenmatt als Griff. Höchstens vier waagrechte Linien, Schattenfuge bei Z 230 gestrichen, Teilung überlackiert. Ein Portal ohne Schräge, sechs gleiche Rundbogenfenster ohne Goldrahmen. Gold genau an Ring mit Portalrahmen, Kronenfase und Namensschild, als Anreibewachs statt Lackmarker. Lichtfuge als gleichmäßiges Band. Rauchacryl 2 mm statt Folie, Spritzenskala nach innen. Krone mit Magneten, Griffmulde, Füße. Pappattrappe als Pflicht und echtes Rendering vor dem Druck.

**Ingenieur:** Stößel in der Achse, Drehung in jeder Füllhöhe über 360 Grad nachgerechnet. Axiallast über Stellring und 608 in die Brücke. Zuganker M5 auf r 90,5 mit Muttern in Taschen, frei von der Hülle. Ausleger als verschraubter Winkel mit Nachweis. Höhenkette oben mit Kaufmaßen geschlossen. 10 mm Reserve, Spritzen werden gemessen. Ventil plus Feuchtparken über der Rinne plus Spülfunktion. Rollen an der Platte statt Rollen unter Schlitzen. Taschen radial mit Steg 3,1. Wellen Ø 10. Waage nur unter Podest, Schublade schwebt beim Wiegen. Dosierzeiten auch für 100 Pa·s angegeben. 5-A-Wandler und Helligkeitsgrenze. Keine bewegten Leitungen.

**Künstlerin:** schwarzer Glanz, Gold, ihr Name. Alle sechs Farben in Ruhe hinter sechs beleuchteten Fenstern ohne Stab oder Band davor, die arbeitende Spritze im Portal. Becher leuchtet in der Zielfarbe, Gold-Moment bei Fertig. Schublade mit Klick statt Loch. Zwei Weißstationen, Tauschen auf Tischhöhe, Füllen durch Ansaugen. Keine Kappen, Wasser etwa einmal im Monat (Ziel), Lippen nach 15 Dosierungen. „Nochmal“ und „Weiß wird knapp“ in der App. Leise mit Messung. Höhe 407: knapp über 400, bewusst für 50 ml je Spritze, die Waage und Standard-Riemenscheiben.

## 20. Offene Maße, die gemessen werden müssen

| Maß | Annahme | Wirkt auf |
|---|---|---|
| Spritze Innen-Ø | 26,7 | ml je mm (Startwert, die Waage korrigiert) |
| Kolbenplatte Ø | 38 | Abstände zum Schlitten (4,0) und zu Nachbarplatten |
| Flansch | 45 x 32 x 3, Ecken R 4 | Taschen, Steg 3,1 |
| Zylinderlänge, Konuslänge | 125, 20 | ganze Höhenkette |
| Becher | Ø 62 / 47 x 33 | Ventilabstand 7 |
| Wägezelle | 80 x 12,7 x 12,7, M4 | Podesthöhe |
| Ventil | Ø 9 x 10 | Ventilabstand, Lippenhöhe |
| Motor 2 (NEMA 17, 34 mm): Wellenlänge ab Flansch, Länge und Lage der D-Fläche | 22, Ø 5, Fläche 2,0 von der Achse | Z-Lage des Motors im Turm (`z_m2_top`), D-Sackloch der Nabe |
| GT2-Scheibe Höhe | 16 | Kronenhöhe |
| Mutter M5 Schlüsselweite | 8 | Abstand zur Körperwand (1,9) |
| Schwund PETG bei diesem Filament | 0,3 bis 0,5 Prozent | Lagersitze 608 (Ø 22,1), Gleitzonen Ø 10,4 im Schlitten (Stand 6: LM10LUU-Bohrung Ø 19,2), M4-Kernloch Ø 3,7, Stationstaschen |
| Biegung der Goldleisten | 1,5 dick bei r 98 | Rahmenleisten, Goldring (am Probestück prüfen) |
| Transmission Rauch- und Klar-PETG | etwa 40 bis 50 Prozent, milchig | Portalscheibe, Fensterscheiben |
| Ausleger unter 250 N | 16 MPa, 0,08 mm bei 100 N | Rippenhöhe, Armdicke |
| Auszugkraft M4 im PETG-Kernloch Ø 3,7 x 12 | nicht belegt, Richtwert 3,75 waagrecht | Ausleger (195 N am oberen Punkt), Auszugtest |
| Hall-Tasche für den A3144 | 4,4 x 5,4 (Bauform messen) | Hallpfosten, Luft 1,5 zum Magnet |
| Drehmoment und Reibung der Platte mit Motor 2 | 0,28 Nm Haltemoment, Bedarf 0,062 Nm (Annahme) | Direktantrieb, Test 17.3 |
| Nennstrom des gekauften NEMA 17 | 0,4 A laut Einkaufsliste, das Blatt rechnet den Stößel mit 0,5 bis 0,65 A | Strom per Poti, Dosierkraft |
| Schublade gegen Motorturm | Schublade ab X 22, Turm bis X 25,2 | behoben: `schub_x0 = 27,2`, Luft 2,0 (Prüfung Nr. 44) |
| Wägezelle 500 g oder 1 kg | Blatt 500 g, Einkaufsliste 1 kg | Auflösung, Bauform 80 x 12,7 x 12,7 |
