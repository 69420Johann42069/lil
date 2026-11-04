// ============================================================================
// Farbmischer Stand 6: parametrisches OpenSCAD nach hardware/farbmischer_parameter.md
// Ein schwarzer Flakon mit Goldlinien, Körper Ø 196, Fuß und Krone Ø 204, 406,8 hoch. Sechs 60-ml-Spritzen im
// Karussell, ein fester Stößel in der Mitte, Wägezelle unter dem Becher, zwei Motoren.
// Stand 6: kein Licht mehr (keine LEDs), alles aus PETG gedruckt, keine Nachbearbeitung mit Füller, Lack oder
// Anreibewachs. Gold sind eigene gedruckte Teile aus Gold-PETG, Portalscheibe und Fensterscheiben sind gedruckt,
// der Ausleger mit Stempel ist gedruckt statt Winkelstahl.
//
// Benutzung: Variable "teil" setzen (Liste unten) oder "montage" für die Gesamtansicht.
// Alle Druckteile stehen in Druckorientierung auf Z = 0, Mitte bei X = 0, Y = 0.
// Koordinaten der Montage: Ursprung Gerätemitte auf der Tischplatte, +X nach vorne
// (Portal), +Y von vorne gesehen nach rechts, +Z nach oben, Winkel theta gegen den
// Uhrzeigersinn von oben, 0 Grad vorne.
//
// Alle Maße in mm. Mit [MESSEN] gekennzeichnete Maße müssen am echten Kaufteil
// nachgemessen werden. Die Prüfungen am Ende (assert) brechen die Berechnung ab,
// die Zeilen "warnung" geben nur eine Meldung in der Konsole aus.
//
// Vereinfachungen gegenüber dem Blatt (Details siehe Antwort):
//  - Rastzungen, Namensschrift und GT2-Zähne sind angenähert, Kantenradien 1 mm fehlen.
//  - Falz der Hüllenteile 3 x 0,7 (Zapfen und Muffe), die Körperhälften zusätzlich mit Klebering.
//  - Spritzenablage: runde Taschen statt Fächer mit Farbmarken.
//  - Kaufteile (Montage) sind Platzhalterkörper, keine Konstruktionsmodelle.
//  - Portalrahmen: in der Montage als Haut über der Hülle, als Druckteil flach in der Abwicklung (Bogenlänge statt Sehne),
//    wird beim Aufkleben gebogen. Der Ausleger mit Stempel liegt beim Druck auf der Seite (Y nach oben).
//  - Portalscheibe in zwei Hälften (Bett 220), Überlappung Z 215 bis 219 mit halber Dicke.
// ============================================================================

// ---------- 0 Steuerung ----------
teil = "montage";
// Druckteile: sockel koerper_unten koerper_oben krone grundplatte lagerbock
//   rinne rinnendeckel saeule abstreifhalter laufring karussell rollenbock schlitten ausleger
//   bruecke gt2_rad schublade front podest waegebock anschlag
//   motor2_winkel hallhalter platinenhalter kabelclip fugenhalter schiene zunge ablage
//   klebering namensschild
// Gold-PETG: goldring goldband kronenring rahmen_unten rahmen_seite rahmen_oben lippe buchsenring
// Scheiben (Rauch- oder Klar-PETG): portalscheibe_unten portalscheibe_oben fensterscheibe
// Ansicht: montage
budget = 1;              // 1 = Stand 7 Budget: ohne Feuchtrinne mit Zubehör, Kabelclips, Ballast, Reed, Magnete an den Scheiben (Scheiben und Goldteile werden geklebt)
scheiben = 1;            // 1 = gedruckte Portal- und Fensterscheiben, Goldrahmen, Goldlippe, Buchsenring (Druckteile, kein Kaufteil, von außen schön)
schnitt = 0;             // 1 = Montage in der XZ-Ebene aufgeschnitten (Y > 0 entfernt)
kaufteile_zeigen = 1;    // 1 = Kaufteile als Platzhalter in der Montage
stempel_dosieren = 0;    // 0 = Park (oben), 1 = ganz unten (S_min)
phi = 0;                 // Karussellwinkel in Grad (0 = Park, Platz 0 vorne)
name_gravur = "NAME";    // Spitzname der Künstlerin, steht mit "Atelier" auf dem Namensschild in der Krone
widmung = "Hamburg 2026";// Datum und Widmung unter der Grundplatte

$fn = 64;

// ---------- 1 Allgemein ----------
eps = 0.01;
sp = 0.2;                // Spiel je Seite an Steckstellen
wand = 1.6;              // Wand aller Schalen (4 Perimeter)
bett_x = 220; bett_y = 220; bett_z = 250;     // Anycubic Kobra 2 Pro
teil_xy_blatt = 204; teil_z_blatt = 200;      // Druckgrenze etwa 200, größte Teile (Sockel, Krone) Ø 204
m3_d = 3.4; m3_pilot = 2.7; m3_kopf_d = 6.4; m3_kopf_t = 2.6;
m4_d = 4.4; m5_d = 5.5;
magnet_d = 6.2; magnet_t = 2.2;               // Tasche für Neodym 6 x 2

// ---------- 2 Plätze, Winkel ----------
n_plaetze = 7;
teilung = 360 / n_plaetze;                    // 51,4286 Grad
st_r = 57;                                    // Stationsradius (Spritzenachse)
fenster_winkel = [1, 2, 3, 4, 5, 6];          // Platz 1 bis 6 haben Spritze und Fenster
stationsbuchstabe = ["W", "Y", "M", "C", "K", "W"];   // Platz 1 Weiß 1, 2 Gelb, 3 Magenta, 4 Cyan, 5 Schwarz, 6 Weiß 2

// ---------- 3 Kaufteile, Maße [MESSEN] ----------
sp_ro = 15;                    // [MESSEN] Zylinder außen Ø 30
sp_ri = 13.35;                 // [MESSEN] Zylinder innen Ø 26,7
sp_len = 125;                  // [MESSEN] Flanschoberkante bis Zylinderende
sp_konus_len = 20;             // [MESSEN] Katheterkonus
sp_konus_d1 = 8;              // Konus außen am Zylinder
sp_konus_d2 = 6;              // Konus außen an der Spitze
sp_fl_l = 45;                  // [MESSEN] Flansch radial (lange Seite)
sp_fl_b = 32;                  // [MESSEN] Flansch tangential
sp_fl_t = 3;                   // [MESSEN] Flansch Dicke
sp_fl_r = 4;                   // [MESSEN] Eckradius Flansch
sp_kp_d = 38;                  // [MESSEN] Kolbenplatte Ø (ungünstigster Fall)
sp_kp_t = 3;                   // Kolbenplatte Dicke
sp_stange = 12;                // Kolbenstange Kreuz 12 x 12
vent_d = 9;                    // [MESSEN] Entenschnabelventil Außen-Ø
vent_l = 10;                   // [MESSEN] Ventil Länge
becher_do = 62;                // [MESSEN] Becher oben
becher_du = 47;                // [MESSEN] Becher unten
becher_h = 33;                 // [MESSEN] Becher Höhe
becher_max_d = 63;             // Hüllmaß für Ersatzbecher
zelle_l = 80; zelle_b = 12.7; zelle_h = 12.7;   // [MESSEN] Wägezelle 500 g, Lochabstand M4 prüfen
nema_b = 42.3;                 // [MESSEN] NEMA 17 Kantenlänge
nema_l1 = 34;                  // NEMA 17 Stößel, 34 mm
nema_l2 = 23;                  // NEMA 17 Pancake Karussell
pancake_welle = 20;            // [MESSEN] Wellenlänge Pancake
lager608_d = 22; lager608_t = 7; lager608_i = 8;
lm10_d = 19; lm10_l = 55;      // LM10LUU
gt2_h_gekauft = 16;            // [MESSEN] GT2-Scheibe 20 Z Gesamthöhe mit Nabe (Nabe oben)
pass_t = 0.5;                  // Passscheibe 8 x 14 x 0,5 unter der Scheibe
gt2_h_nutz = 8;                // Zahnkranz mit Bund in der Riemenebene
mutter_fl_d = 22; mutter_fl_t = 3.5; mutter_d = 10.2; mutter_l = 15;   // [MESSEN] Messingmutter T8
stellring_d = 16; stellring_h = 8;
schalter_l = 20; schalter_b = 10; schalter_h = 6;      // [MESSEN] Mikroschalter

// ---------- 4 Höhenkette (Z) ----------
z_tisch = 0;
fuss_h = 3;                    // Silikonfüße Ø 12 x 3
z_gp0 = 3; gp_t = 4; z_gp1 = z_gp0 + gp_t;           // Grundplatte 3 bis 7
gp_rippe_h = 8;                // Rippen bis Z 15
z_rippe1 = z_gp1 + gp_rippe_h;
z_zelle0 = 7.5; z_zelle1 = z_zelle0 + zelle_h;       // 20,2
z_podest0 = 24.4; podest_t = 1.6; z_podest1 = z_podest0 + podest_t;   // 24,4 bis 26 (Stiel Ø 14 steht frei, der Platz des LED-Rings ist leer)
z_schub0 = 26; schub_boden = 1.5; z_becher0 = z_schub0 + schub_boden;   // 27,5
z_becher1 = z_becher0 + becher_h;                    // 60,5
// Spritze
z_platte0 = 211; platte_t = 12; z_platte1 = z_platte0 + platte_t;      // 223
tasche_t = 3.5;
z_fl_o = 222.5;                // [MESSEN] Flanschoberkante, 0,5 unter Plattenoberkante
z_zyl_u = z_fl_o - sp_len;     // 97,5
z_konus_spitze = z_zyl_u - sp_konus_len;      // 77,5
z_vent_spitze = z_konus_spitze - vent_l;      // 67,5
vent_ueber = z_vent_spitze - z_becher1;       // 7,0 über dem Becherrand
kp_leer_ueber_fl = 9;          // [MESSEN] Kolbenplatte Oberkante bei leerer Spritze über Flanschoberkante
z_kp_leer = z_fl_o + kp_leer_ueber_fl;        // 231,5
mm_je_ml = 1000 / (PI * sp_ri * sp_ri);       // 1,786
fuellung_ml = 50; rest_ml = 2;
hub_nutz = fuellung_ml * mm_je_ml;            // 89,3
z_kp_min = z_kp_leer + rest_ml * mm_je_ml;    // 235,1 (tiefster Stempel S_min)
z_kp_voll = z_kp_leer + hub_nutz;             // 320,8
res_park = 10;
s_min = z_kp_min;
s_park = z_kp_voll + res_park;                // 330,8
s_weg = s_park - s_min;                       // 95,7
s_pos = s_park - stempel_dosieren * s_weg;    // Stellung für Montage und Druckpose
// Schlitten (Z relativ zu S)
schl_r = 34; schl_u = 10; schl_o = 48; schl_h = schl_u + schl_o;   // 58
schl_tasche_d = 23; schl_tasche_t = 12.5;
schl_bohr_d = 19.2;            // Ø 19 H7 für LM10LUU, gedruckt mit Zuschlag
mutter_oben = 35.5;            // Mutter Körper endet bei S + 35,5
// Stand 6: Ausleger mit Stempel aus einem Stück PETG (liegend auf der Seite gedruckt, L-Profil in jeder Schicht)
arm_x0 = 28; arm_x1 = 68; arm_b = 25; arm_z0 = 8;     // Ausleger: X 28 bis 68, Y +-12,5, Unterkante S + 8
arm_t = 8;                     // waagrechter Arm 8 dick (Z S + 8 bis S + 16)
platte_dick = 8;               // senkrechte Platte X 28 bis 36 an der Schlittenfläche
winkel_h = 40;                 // senkrechte Platte Z S + 8 bis S + 48
rippe_b = 3; rippe_h = 20; rippe_l = 22;               // zwei Stützrippen je 3 dick bei |Y| 9,5 bis 12,5
winkel_schraube_z = [24, 40];  // 2 x M4 in Gewindeeinsätzen, Z relativ zu S (Hebel 32 zur Kippkante)
einsatz_m4_d = 5.6; einsatz_m4_t = 8;
stempel_d = 25; stempel_t = 6; gummi_t = 2; stempel_x = 53;      // Stempel Ø 25 am Ausleger, 4 mm innen von der Spritzenachse (Flanschauflage)
kraft_max = 250;               // N, Haltekraft des Motors 1 am T8 (0,26 Nm, Wirkungsgrad 0,3), StallGuard schaltet früher ab
// Brücke und Krone
z_m1_0 = 346.8; m1_l = nema_l1; z_br0 = z_m1_0 + m1_l;   // 380,8
br_t = 7; z_br1 = z_br0 + br_t;                          // 387,8
z_riemen0 = 388.3; z_riemen1 = z_riemen0 + gt2_h_nutz;   // 396.3
z_gt2_oben = z_br1 + pass_t + gt2_h_gekauft;             // 404,3
kr_deckel = 2; z_deckel_u = z_gt2_oben + 0.5; z_hoehe = z_deckel_u + kr_deckel;   // 404,8 und 406,8
z_kr0 = 341;
z_stellring0 = z_br0 - stellring_h;                      // 372,8
// Hülle
d_sock_u = 204; d_sock_o = 196; ring_d = 202; koerper_d = 196; krone_d = 204;
koerper_ro = koerper_d / 2; koerper_ri = koerper_ro - wand;    // 98 und 96,4
z_sock0 = 3; z_ring0 = 97; z_ring1 = 101; z_kor0 = 101;
z_kor_teil = 235; z_kor1 = 338; z_fuge1 = 341;
falz_h = 3;                    // Höhe der Steckfalze
falz_t = (wand - sp) / 2;      // 0,7: Zapfen und Muffe je eine halbe Wand, 0,2 Spiel dazwischen
// Fenster und Portal
portal_b = 72; portal_z0 = 16; portal_z1 = 330; portal_ro = 24; portal_ru = 8;
rahmen_b = 4; rahmen_h = 1.5;
scheibe_b = 78; scheibe_z0 = 99; scheibe_z1 = 333; scheibe_ro = 26; scheibe_ru = 3;
scheibe_t = 2; scheibe_x = 90.5; falz_b = 3;
pad_b = 3;                     // Hinterlegung des Scheibenfalzes innen (Breite über den Falz hinaus)
fenster_b = 22; fenster_z0 = 108; fenster_z1 = 180; fenster_zm = fenster_z1 - fenster_b / 2;   // Bogenmitte 169, ganz unter dem Laufring
fenster_streifen_b = 26; fenster_streifen_h = 76; fenster_fuge = 1; fenster_fuge_t = 1;
fenster_pad_b = 32; fenster_pad_h = 78; fenster_pad_x = 93.8;  // Rahmen für die gedruckte Fensterscheibe (Scheibe liegt bei X 94,0 bis 95,6)
griff_b = 24; griff_z0 = 20; griff_z1 = 80; griff_t = 8; griff_r = 4;
buchse_z = 30; buchse_d = 8.2; buchsenring_d = 16;
krone_fase = 6;
// Zuganker
zug_r = 90.5; zug_winkel = [32, -32, 2.5 * teilung, -2.5 * teilung]; zug_d = 5; zug_loch = 5.5;   // hinten mittig zwischen zwei Fenstern
mutter_m5_af = 8; mutter_m5_h = 4;        // DIN 934 in Sechskanttaschen, Schlüsselfläche radial außen, keine Karosseriescheiben
lasche_r1 = 94.5;                          // Ende der Laufringlaschen
// Gold (Gold-PETG): Goldring, Goldband, Kronenring, Portalrahmen, Lippe
goldring_r1 = 101; goldring_gap = 39;         // Goldring Ø 202, am Portal offen (|Y| < 39)
kr_ring_dr = 2;                // Kronenring, waagrechte Dicke der Fase (1,4 senkrecht gemessen)
rahmen_t = 1.5; rahmen_bb = 3; rahmen_n = 12;  // Portalrahmen: 1,5 erhaben, 3 breit
rahmen_naht_unten = 97;        // Bühnenrahmen endet am Goldring
rahmen_hw_scheibe = 39.4;      // Fensterrahmen beginnt 0,4 außerhalb der Falzkante (Scheibe 78 + 2 x 0,2 Spiel)
scheibe_zt = 217; scheibe_ov = 4;             // Portalscheibe in zwei Teilen, Überlappung 4 mm vor der Karussellplatte
fenster_streifen_t = 1.6;      // Fensterscheibe, Klar-PETG
// Krone innen
lug_winkel_magnet = [0, 90, 180, 270];
lug_winkel_stift = [45, 225];
lug_r0 = 90; lug_halb_winkel = 7;

// ---------- 5 Bauteile ----------
// Grundplatte
gp_r = 100;                    // Grundplatte Ø 200
gp_rippe_r0 = 96; gp_rippe_r1 = 98;
fuss_r = 92; fuss_d = 12; fuss_tasche_d = 12.5;
laschen_winkel = [45, -45, 135, -135]; laschen_r = 96;
ballast_pos = [[72, 69], [72.5, -71], [66.5, 120], [66.5, -120]];   // [r, theta], je 7 x DIN 125 M20 (Ø 37 x 3)
ballast_tasche_d = 38; ballast_n = 7; ballast_s = 3; ballast_d = 37;
// Lagerbock, Karussellwelle, Riementrieb unten
lb_d = 40; lb_z0 = 7; lb_z1 = 40;
welle2_d = 8; welle2_z0 = 9; welle2_z1 = 221;
gt2_70_z0 = 43; gt2_70_z1 = 51; gt2_70_nabe_z0 = 41; gt2_70_teilkreis = 44.6; gt2_70_aussen = 47;
gt2_20_d = 16;
m2_x = -57.8; m2_z0 = 17; m2_z1 = m2_z0 + nema_l2;       // Körper 17 bis 40
hall_r = 15;
// Wägezelle, Podest
zelle_x = 57; zelle_y0 = -70; zelle_y1 = 10;
zelle_fest_y1 = -50; zelle_last_y0 = -10;
ues_luft = 0.8; ues_tasche_t = 1.5;
podest_stiel_d = 14; podest_d = 60;
// Schublade
schub_b = 70; schub_wand = 2; schub_x0 = 22; schub_x1 = 110; schub_z1 = 45;   // Vorderkante folgt der Front (siehe t_schublade)
sitz_du = 48; sitz_do = 52; sitz_h = 3; sitz_da = 56;   // Bechersitz konisch
front_b = 68; front_z0 = 17; front_z1 = 45; front_t = 8; lippe_b = 3; lippe_h = 1.5;
auszug = 50;
schiene_y0 = 32; schiene_y1 = 35;   // KORRIGIERT: Blatt nennt 35 bis 39, dort liegt nichts unter der Schublade (Wand 33 bis 35)
kufe_l = 3;                         // Kufen der Schublade nur hinten (X 22 bis 25), liegen auf der abgesenkten Rampe
kufe_freigang = 1;                  // Schublade sonst 1 mm über Schienenoberkante 26,5 angehoben (Unterkante 27,0)
schiene_x0 = 20; schiene_x1 = 98; schiene_z1 = 26.5; schiene_balken_t = 4;
schiene_rampe_l = 5; schiene_rampe_h = 1;
schiene_pfosten_l = 8;
// Feuchtrinne
rinne_r0 = 45; rinne_r1 = 69; z_rinne0 = 54; z_rinne1 = 64; rinne_boden = 2;
rinne_offen = 38; saeule_d = 8; saeule_winkel = [95, -95, 145, -145];
schwamm_o = 65.5;
rdeckel_t = 1.2; z_rdeckel1 = z_rinne1 + rdeckel_t; rdeckel_loch = 14;   // Rinnendeckel mit sechs Löchern
lippe_winkel = 40; lippe_z1 = 68.5; lippe_t = 1.5; lippe_r0 = 50; lippe_r1 = 64;
// Karussell
platte_r = 85.5; nabe_d = 30; nabe_z0 = 205; welle_flach = 3.5;
tasche_r0 = 34; tasche_b = 33; tasche_ecke = 5; schlitz_b = 32; schlitz_r0 = 41;
rast_t = 1.5; rast_nase = 1.0; rast_r0 = 66; rast_r1 = 84; rast_schlitz = 0.8;
bock_r0 = 74.5; bock_r1 = 85.5; bock_halb = 12; bock_z0 = 193.5; bock_achse_r = 80; bock_achse_z = 199.5;
laufring_r0 = 74.5; laufring_r1 = 86.5; z_lr0 = 182.5; z_lr1 = 188.5; lr_offen = 15;
lr_rampe_l = 10; lr_rampe_h = 1.5;
rolle_z0 = 188.5;
// Stößel, Brücke
spindel_z0 = 250; spindel_z1 = 403; spindel_d = 8;
welle_d = 10; welle_y = 22; welle_z0 = s_min - schl_u;
welle_einsp = 14.3;            // Einspannlänge in Brücke (7) und Klemmnabe, Welle 170 lang
klemm_d = 20; klemm_h = 10;
br_r = 98;
br_rippe_t = 2; br_rippe_h = 12; br_rippe_winkel = [15, 75, 135, 195, 255, 315];
motor1_r = 59;
riemen1_achs = 59;
schalter_x = -26;
// Platine, Kabel
platine_y = -81; platine_z0 = 30; platine_z1 = 100;
// Wartung
zunge_l = 160; zunge_b = 16; zunge_t = 0.8;
ablage_l = 190; ablage_b = 70; ablage_h = 45;

// ---------- 6 abgeleitete Maße ----------
function sock_r(z) = d_sock_u / 2 - (d_sock_u - d_sock_o) / 2 * (z - z_sock0) / (z_ring0 - z_sock0);
function sock_ri(z) = sock_r(z) - wand;
function dist2(x1, y1, x2, y2) = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
function fits(v) = v[0] <= bett_x && v[1] <= bett_y && v[2] <= bett_z;
function fits_blatt(v) = v[0] <= teil_xy_blatt && v[1] <= teil_xy_blatt && v[2] <= teil_z_blatt;
function fits_z(v) = v[2] <= teil_z_blatt;

schritte_umdr_kar = 200 * 16 * 70 / 20;       // 11 200
schritte_platz = schritte_umdr_kar / n_plaetze;   // 1600
schritte_mm = 200 * 16 / 2;                   // T8 x 2: 1600
schritte_ml = mm_je_ml * schritte_mm;         // 2857
ul_je_schritt = 1000 / schritte_ml;           // 0,35

// Karussell: Steg zwischen zwei Flanschtaschen (Innenecken mit Radius)
tasche_mr = tasche_r0 + tasche_ecke;          // Mitte der Eckkreise radial
tasche_mv = tasche_b / 2 - tasche_ecke;       // Mitte der Eckkreise tangential
tasche_nx = tasche_mr * cos(teilung) + tasche_mv * sin(teilung);
tasche_ny = tasche_mr * sin(teilung) - tasche_mv * cos(teilung);
tasche_steg = dist2(tasche_mr, tasche_mv, tasche_nx, tasche_ny) - 2 * tasche_ecke;   // 3,1
// Höhenabstände
spiel_schl_platte = (s_min - schl_u) - z_platte1;           // 2,07
spiel_welle_platte = welle_z0 - z_platte1;                  // 2,07
stempel_ueber_kp = s_park - z_kp_voll;                      // 10,0
spiel_schl_bruecke = z_br0 - (s_park + schl_o);             // 2,0
spiel_motor1_kp = z_m1_0 - z_kp_voll;                       // 20
laufring_zyl = laufring_r0 - (st_r + sp_ro);                // 2,5
schwamm_vent = z_vent_spitze - schwamm_o;                   // 2,0
lippe_ueber = lippe_z1 - z_vent_spitze;                     // 1,0
stellring_eintauch = (s_park + schl_o) - z_stellring0;      // 6,0
stellring_luft = z_stellring0 - ((s_park + schl_o) - schl_tasche_t + mutter_fl_t);   // 3,0
zug_innen = koerper_ri - (zug_r + zug_d / 2);               // 3,4 Stange bis Körperwand
mutter_r_ecke = mutter_m5_af / cos(30) / 2;                 // 4,62
mutter_wand = koerper_ri - (zug_r + mutter_m5_af / 2);      // 1,9 Schlüsselfläche außen bis Körperwand
lasche_wand = koerper_ri - lasche_r1;                       // 1,9
zug_platte = zug_r - zug_d / 2 - platte_r;                  // 2,5 Zuganker gegen Karussellplatte
zug_bock = zug_r - zug_d / 2 - bock_r1;                     // 2,5 Zuganker gegen Rollenbock (Außenbogen)
// seitlicher Abstand Zuganker zum Fensterstreifen (nächstes Fenster: vorne 19,4 Grad, hinten 25,7 Grad)
zug_fenster_quer = min(zug_r * sin(teilung - 32), zug_r * sin(0.5 * teilung));
zug_streifen = zug_fenster_quer - zug_d / 2 - fenster_streifen_b / 2;   // 14,6
fenster_laufring = z_lr0 - fenster_z1;                      // 2,5 Fenster endet unter dem Laufring
rippe_frei = z_deckel_u - z_br1;                            // 17 Platz unter dem Kronendeckel
riemen_frei = z_deckel_u - z_riemen1;                       // 8,5
gt2_ueberstand = z_gt2_oben - z_deckel_u;                   // -0,5: Scheibe in voller Höhe unter dem Kronendeckel
rdeckel_ventil = z_vent_spitze - z_rdeckel1;                // 2,3
stempel_versatz = st_r - stempel_x;                         // 4: Kraft innerhalb der Flanschauflage
// Ausleger aus PETG: Biegespannung an der Wurzel (Arm 25 x 8, ohne die Rippen gerechnet) und Zug im oberen Schraubenpaar
ausleger_hebel = stempel_x - (arm_x0 + platte_dick);        // 17 vom Plattenrand zur Stempelmitte
ausleger_sigma = kraft_max * ausleger_hebel / (arm_b * arm_t * arm_t / 6);   // 15,9 MPa bei 250 N
schraube_zug = kraft_max * (stempel_x - arm_x0) / (winkel_schraube_z[1] - arm_z0);   // 195 N am oberen Einsatz
ausleger_fuss_unten = arm_z0 - stempel_t;                   // Stempel Z S + 2 (mit Gummi 2 mm bis S)
stempel_kp = sp_kp_d / 2 - (abs(stempel_x - st_r) + stempel_d / 2);   // 2,5: Stempel liegt innerhalb der Kolbenplatte Ø 38 (Rest zum Plattenrand)
tasche_rinne_becher = st_r * sin(rinne_offen);              // Rinnenende gegen Becherrand seitlich
becher_rinne_luft = tasche_rinne_becher - becher_do / 2;    // 4,1
rinne_ventil_luft = (rinne_r1 - wand) - (st_r + vent_d / 2);   // Ventil gegen Außenwand der Rinne
spindel_unten_rest = (s_min + 20.5) - spindel_z0;
welle_len = (z_br0 + welle_einsp) - welle_z0;               // 170 Führungswelle
rolle_oben = bock_achse_z + lager608_d / 2;                 // Rolle Oberkante 210,5
schiene_balken_u = schiene_z1 - schiene_balken_t;           // 22,5
schiene_zelle = schiene_balken_u - z_zelle1;                // 2,3
platine_ecke = sqrt(45 * 45 + (abs(platine_y) + 1) * (abs(platine_y) + 1));
platine_luft = koerper_ri - platine_ecke;                   // 2,9 (Hülle Z 97 bis 100 innen mindestens r 96,4)
// Hüllmaße der Druckteile (Breite, Tiefe, Höhe in Druckorientierung)
hm_sockel = [d_sock_u, d_sock_u, (z_ring1 + falz_h) - z_sock0];
hm_koerper_unten = [koerper_d + 2 * rahmen_h, koerper_d + 2 * rahmen_h, (z_kor_teil + falz_h) - z_kor0];
hm_koerper_oben = [koerper_d + 2 * rahmen_h, koerper_d + 2 * rahmen_h, z_kor1 - z_kor_teil];
hm_krone = [krone_d, krone_d, z_hoehe - z_kr0];
hm_goldband = [koerper_d, koerper_d, 7];
hm_goldring = [2 * goldring_r1, 2 * goldring_r1, z_ring1 - z_ring0];
hm_kronenring = [krone_d, krone_d, krone_fase];
hm_grundplatte = [2 * gp_r, 2 * gp_r, z_rippe1 - z_gp0];
hm_rinnendeckel = [2 * rinne_r1, rinne_r1 + rinne_r0, rdeckel_t];
hm_klebering = [koerper_d, koerper_d, 8];
hm_namensschild = [90, 16, 1.2];
hm_lagerbock = [lb_d, lb_d, lb_z1 - lb_z0];
hm_rinne = [2 * rinne_r1, 2 * rinne_r1, z_rinne1 - z_rinne0];
hm_saeule = [saeule_d, saeule_d, z_rinne0 - z_gp1];
hm_halter = [20, 16, 10];
hm_laufring = [2 * lasche_r1, 2 * lasche_r1, z_lr1 - z_lr0];
hm_karussell = [2 * platte_r, 2 * platte_r, z_platte1 - nabe_z0];
hm_rollenbock = [2 * bock_halb, bock_r1 - bock_r0, z_platte0 - bock_z0];
hm_schlitten = [2 * schl_r, 2 * schl_r, schl_h];
hm_ausleger = [arm_x1 - arm_x0, arm_b, (arm_z0 + winkel_h) - gummi_t];   // liegt auf der Seite (Y nach oben): X 40, Y 25, Höhe 25
hm_portalscheibe = [(scheibe_z1 - scheibe_z0) / 2 + scheibe_ov, scheibe_b, scheibe_t];
hm_fensterscheibe = [fenster_streifen_b, fenster_streifen_h, fenster_streifen_t];
hm_lippe = [front_b, 11, lippe_b];
hm_bruecke = [2 * br_r, 2 * br_r, (z_br1 + br_rippe_h) - z_br0];
hm_gt2 = [gt2_70_aussen, gt2_70_aussen, gt2_70_z1 - gt2_70_nabe_z0];
hm_schublade = [schub_b, (sock_r(z_schub0) - front_t) - schub_x0, schub_z1 - z_schub0];
front_x_min = sqrt(pow(sock_r(front_z1) - front_t, 2) - pow(front_b / 2, 2));
hm_front = [front_b, sock_r(front_z0) + lippe_h - front_x_min, front_z1 + lippe_b - front_z0];
hm_podest = [podest_d, podest_d, z_podest1 - z_zelle1];
hm_waegebock = [24, 20, 0.5];
hm_anschlag = [20, 14, (z_zelle0 - ues_luft) - (z_gp1 - ues_tasche_t)];
hm_motor2_winkel = [48, 66, m2_z1 + 2.5 - z_gp1];
hm_hallhalter = [lb_d / 2 + 2 - (hall_r - 2.5), 8, 3];
hm_platinenhalter = [4, 4, 60 - z_gp1];
hm_kabelclip = [16, 9, 8];
hm_fugenhalter = [12, 10, 4];
hm_schiene = [schiene_x1 - schiene_x0, schiene_z1 - z_gp1, schiene_y1 - schiene_y0];   // liegt auf der Seite
hm_zunge = [zunge_l, zunge_b, 6];
hm_ablage = [ablage_l, ablage_b, ablage_h];
hm_buchsenring = [buchsenring_d, buchsenring_d, 3];

// ---------- 7 Prüfungen ----------

assert(spiel_schl_platte >= 2.0 - 0.01, "Schlitten tiefste Stellung gegen Karussellplatte unter 2 mm");
assert(spiel_welle_platte >= 2.0 - 0.01, "Wellenende Ø 10 gegen Karussellplatte unter 2 mm");
assert(stempel_ueber_kp >= 10 - 0.001, "Stempel in Park weniger als 10 mm über voller Kolbenplatte");
assert(spiel_schl_bruecke >= 2.0 - 0.01, "Schlitten in Park gegen Brückenunterseite unter 2 mm");
assert(spiel_motor1_kp >= 10, "Motor 1 Unterkante gegen Kolbenplatte 50 ml unter 10 mm");
assert(vent_ueber >= 5, "Ventil gegen Becherrand unter 5 mm");
assert(laufring_zyl >= 2.0, "Laufring gegen Spritzenzylinder beim Drehen unter 2 mm");
assert(schwamm_vent >= 1.5 - 0.001, "nasser Schwamm gegen Ventilspitze unter 1,5 mm");
assert(lippe_ueber > 0, "Abstreiflippe nicht über der Ventilspitze");
assert(stellring_luft >= 2.0 - 0.01, "Stellring gegen Mutterflansch unter 2 mm");
assert(stellring_eintauch > 0 && stellring_eintauch < schl_tasche_t - mutter_fl_t, "Stellring taucht nicht in die Schlittentasche");
assert(tasche_steg >= 3.0, "Steg zwischen zwei Flanschtaschen unter 3 mm");
assert(rinne_ventil_luft >= 2.0, "Ventil gegen Rinnenwand unter 2 mm");
assert(becher_rinne_luft >= 2.0, "Rinnenende gegen Becher unter 2 mm");
assert(becher_du <= sitz_du - 0.5 && becher_du + (becher_do - becher_du) * sitz_h / becher_h <= sitz_do, "Becher passt nicht in den konischen Sitz");
assert(schiene_zelle >= 2.0, "Schienenbalken gegen Wägezelle unter 2 mm");
assert(spindel_unten_rest > 0, "Spindel endet über der Mutter bei S_min");
assert(falz_t > 0 && falz_t * 2 + sp <= wand + 0.001, "Falz passt nicht in die Wand");
assert(wand - fenster_fuge_t >= 0.6, "Wand unter der Schattenfuge unter 0,6 mm");
assert(rolle_oben < z_platte0 + 0.6, "Laufrolle stößt oben an die Karussellplatte");
assert(abs(schritte_platz - round(schritte_platz)) < 1e-9, "Schritte je Platz nicht ganzzahlig");
assert(abs(schritte_umdr_kar - 11200) < 1e-9, "Schritte je Umdrehung Karussell nicht 11200");
assert(abs(s_weg - 95.7) < 0.1, "Stempelweg weicht vom Blatt ab");
assert(abs(z_hoehe - 406.8) < 1e-6 && abs(z_hoehe - (z_kr0 + 65.8)) < 1e-6, "Gesamthöhe passt nicht zur Kronenhöhe 65,8");
assert(gt2_ueberstand <= -0.5 + 1e-6, "GT2-Scheibe in voller Höhe stößt an den Kronendeckel");
assert(abs(welle_len - 170) < 0.1, "Führungswelle nicht 170 lang");
assert(z_riemen1 + 0.5 <= z_deckel_u, "Riemenebene stößt an den Kronendeckel");
assert(br_rippe_h <= rippe_frei - 0.3, "Brückenrippen stoßen an den Kronendeckel");
assert(zug_innen >= 1.5, "Zugankerrohr zu nah an der Körperwand");
assert(mutter_wand >= 1.5, "Mutter M5 (Fläche außen) zu nah an der Körperwand");
assert(lasche_wand >= 1.5, "Laufringlasche zu nah an der Körperwand");
assert(zug_platte >= 2.0, "Zuganker gegen Karussellplatte unter 2 mm");
assert(zug_bock >= 2.0, "Zuganker gegen Rollenbock unter 2 mm");
assert(zug_streifen >= 5.0, "Zuganker steht im Fensterbereich");
assert(fenster_laufring >= 2.0, "Seitenfenster reicht an den Laufring");
assert(rdeckel_ventil >= 2.0, "Rinnendeckel gegen Ventil beim Drehen unter 2 mm");
assert(stempel_versatz >= 2.0, "Stempel liegt nicht innerhalb der Flanschauflage");
assert(ausleger_sigma <= 20, "Ausleger aus PETG: Biegespannung über 20 MPa (Reserve zu etwa 45 MPa XY und 30 MPa quer zu den Schichten)");
assert(schraube_zug <= 250, "Ausleger: Zug am oberen M4-Einsatz über 250 N");
assert(stempel_kp >= 1.5, "Stempel Ø 25 liegt nicht ganz auf der Kolbenplatte Ø 38");
assert(rahmen_hw_scheibe >= scheibe_b / 2 + sp, "Fensterrahmen steht im Scheibenfalz");
assert(platine_luft >= 2.0, "Platinenecke gegen Hülle unter 2 mm");
assert(z_vent_spitze > z_rinne1, "Rinne höher als die Ventilspitze");
assert(s_pos <= s_park + eps && s_pos >= s_min - eps, "Stempelstellung außerhalb des Weges");
// Hüllmaße gegen das Druckbett 220 x 220 x 250 und gegen die Blattgrenze Z 200
assert(fits(hm_sockel), "Sockelschale passt nicht aufs Bett");
assert(fits(hm_koerper_unten), "Körper unten passt nicht aufs Bett");
assert(fits(hm_koerper_oben), "Körper oben passt nicht aufs Bett");
assert(fits(hm_krone), "Krone passt nicht aufs Bett");
assert(fits(hm_goldband), "Goldband passt nicht aufs Bett");
assert(fits(hm_goldring), "Goldring passt nicht aufs Bett");
assert(fits(hm_kronenring), "Kronenring passt nicht aufs Bett");
assert(fits(hm_portalscheibe), "Portalscheibe (Hälfte) passt nicht aufs Bett");
assert(fits(hm_fensterscheibe), "Fensterscheibe passt nicht aufs Bett");
assert(fits(hm_lippe), "Goldlippe passt nicht aufs Bett");
assert(fits(hm_grundplatte), "Grundplatte passt nicht aufs Bett");
assert(fits(hm_lagerbock), "Lagerbock passt nicht aufs Bett");
assert(fits(hm_rinne), "Feuchtrinne passt nicht aufs Bett");
assert(fits(hm_saeule), "Rinnensäule passt nicht aufs Bett");
assert(fits(hm_halter), "Abstreifhalter passt nicht aufs Bett");
assert(fits(hm_laufring), "Laufring passt nicht aufs Bett");
assert(fits(hm_karussell), "Karussellplatte passt nicht aufs Bett");
assert(fits(hm_rollenbock), "Rollenbock passt nicht aufs Bett");
assert(fits(hm_schlitten), "Schlitten passt nicht aufs Bett");
assert(fits(hm_ausleger), "Ausleger mit Stempel passt nicht aufs Bett");
assert(fits(hm_bruecke), "Brücke passt nicht aufs Bett");
assert(fits(hm_gt2), "GT2-Rad passt nicht aufs Bett");
assert(fits(hm_schublade), "Schublade passt nicht aufs Bett");
assert(fits(hm_front), "Schubladenfront passt nicht aufs Bett");
assert(fits(hm_podest), "Podest passt nicht aufs Bett");
assert(fits(hm_waegebock), "Wägezellenbock passt nicht aufs Bett");
assert(fits(hm_anschlag), "Überlastanschlag passt nicht aufs Bett");
assert(fits(hm_motor2_winkel), "Motor-2-Winkel passt nicht aufs Bett");
assert(fits(hm_hallhalter), "Hallhalter passt nicht aufs Bett");
assert(fits(hm_platinenhalter), "Platinenhalter passt nicht aufs Bett");
assert(fits(hm_kabelclip), "Kabelclip passt nicht aufs Bett");
assert(fits(hm_fugenhalter), "Fugenhalter passt nicht aufs Bett");
assert(fits(hm_schiene), "Schiene passt nicht aufs Bett");
assert(fits(hm_zunge), "Einführzunge passt nicht aufs Bett");
assert(fits(hm_ablage), "Spritzenablage passt nicht aufs Bett");
assert(fits(hm_buchsenring), "Buchsenring passt nicht aufs Bett");
assert(fits(hm_rinnendeckel), "Rinnendeckel passt nicht aufs Bett");
assert(fits(hm_klebering), "Klebering passt nicht aufs Bett");
assert(fits(hm_namensschild), "Namensschild passt nicht aufs Bett");
assert(fits_z(hm_sockel) && fits_z(hm_koerper_unten) && fits_z(hm_koerper_oben),
       "ein Teil ist höher als 200 mm");
assert(fits_blatt(hm_sockel) && fits_blatt(hm_krone) && fits_blatt(hm_grundplatte) && fits_blatt(hm_karussell) && fits_blatt(hm_bruecke)
       && fits_blatt(hm_koerper_unten) && fits_blatt(hm_koerper_oben) && fits_blatt(hm_laufring),
       "ein Teil überschreitet Ø 204 x 200 aus dem Blatt");
// Stand 5.1: alle Widersprüche aus Stand 5 sind im Blatt gelöst und oben als assert geprüft.

// Schrittzahlen, Rückgabe in der Konsole
echo(str("Schritte Karussell je Umdrehung (1/16): ", schritte_umdr_kar, ", je Platz: ", schritte_platz));
echo(str("Station p vorne bei q = -p * ", schritte_platz, " (mod ", schritte_umdr_kar, ")"));
echo(str("Stößel: ", schritte_mm, " Mikroschritte je mm, ", schritte_ml, " je ml, ", ul_je_schritt, " ul je Mikroschritt"));
echo(str("Kolbenplatte leer ", z_kp_leer, ", 2 ml Rest ", z_kp_min, ", 50 ml ", z_kp_voll, ", S_park ", s_park, ", Weg ", s_weg));
echo(str("Ventil über Becherrand: ", vent_ueber, ", Schlitten tief gegen Platte: ", spiel_schl_platte));
echo(str("Steg Flanschtaschen: ", tasche_steg, ", Laufring gegen Zylinder: ", laufring_zyl));
echo(str("Zuganker: Mutter bis Körperwand ", mutter_wand, ", gegen Platte ", zug_platte, ", seitlich zum Fensterstreifen ", zug_streifen));
echo(str("Höhe ", z_hoehe, ", Führungswelle ", welle_len, " lang, Ausleger Spannung ", ausleger_sigma, " MPa, Schraubenzug ", schraube_zug, " N"));

// ---------- 8 Hilfsmodule ----------
function arc_pts(r, a0, a1, n) = [for (i = [0:n]) [r * cos(a0 + (a1 - a0) * i / n), r * sin(a0 + (a1 - a0) * i / n)]];

module sektor(r0, r1, a0, a1) {
    n = max(2, ceil(abs(a1 - a0) / 4));
    polygon(concat(arc_pts(r1, a0, a1, n), arc_pts(r0, a1, a0, n)));
}

module box(x0, x1, y0, y1, z0, z1) {
    translate([x0, y0, z0]) cube([x1 - x0, y1 - y0, z1 - z0]);
}

module zyl(r, z0, z1) {
    translate([0, 0, z0]) cylinder(r = r, h = z1 - z0);
}

module rohr(ra, ri, z0, z1) {
    difference() {
        zyl(ra, z0, z1);
        zyl(ri, z0 - eps, z1 + eps);
    }
}

module rrect2d(b, h, r) {
    hull() {
        for (sx = [-1, 1]) for (sy = [-1, 1])
            translate([sx * (b / 2 - r), sy * (h / 2 - r)]) circle(r = r);
    }
}

// 2D-Profil in (Y, Z): oben und unten verschiedene Eckradien
module portal2d(b, z0, z1, ro, ru) {
    hull() {
        for (s = [-1, 1]) {
            translate([s * (b / 2 - ru), z0 + ru]) circle(r = ru);
            translate([s * (b / 2 - ro), z1 - ro]) circle(r = ro);
        }
    }
}

// Extrusion entlang +X: 2D x wird Y, 2D y wird Z
module quer_extrusion(x0, x1) {
    translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(height = x1 - x0) children();
}

module fenster2d() {
    translate([-fenster_b / 2, fenster_z0]) square([fenster_b, fenster_zm - fenster_z0]);
    translate([0, fenster_zm]) circle(r = fenster_b / 2);
}

// Aussenkontur der Hülle (r, z), o = Aufmaß (Rahmenhaut)
function env_pts(o) = [[0, z_sock0], [d_sock_u / 2 + o, z_sock0], [d_sock_o / 2 + o, z_ring0],
                       [ring_d / 2, z_ring0], [ring_d / 2, z_ring1], [koerper_ro + o, z_ring1],
                       [koerper_ro + o, z_kor1], [0, z_kor1]];

module env_solid(o) {
    rotate_extrude() polygon(env_pts(o));
}

module zbereich(z0, z1) {
    intersection() {
        children();
        box(-300, 300, -300, 300, z0, z1);
    }
}

// ---- Portal und Scheibe ----
module portal_cut() {
    quer_extrusion(40, 140) portal2d(portal_b, portal_z0, portal_z1, portal_ro, portal_ru);
}

module scheibe2d() {
    portal2d(scheibe_b, scheibe_z0, scheibe_z1, scheibe_ro, scheibe_ru);
}

module scheibe_falz_cut() {
    quer_extrusion(scheibe_x - scheibe_t, 140) offset(delta = sp) scheibe2d();
}

// ---- Portalrahmen aus Gold-PETG (Stand 6): eigene Leisten, 3 breit, 1,5 erhaben ----
// Für den Druck liegen sie flach in der Abwicklung der Hülle (Bogenlänge statt Sehne) und werden beim Aufkleben
// um die Hülle gebogen (1,5 mm PETG biegt sich über r 98 ohne Mühe). Für die Montage steht dieselbe Kontur als Haut.
function dev_s(y, r) = r * asin(y / r) * PI / 180;
function ecke(cy, cz, rad, a0, a1) = [for (i = [0:rahmen_n]) [cy + rad * cos(a0 + (a1 - a0) * i / rahmen_n), cz + rad * sin(a0 + (a1 - a0) * i / rahmen_n)]];
function rr_pts(hw, z0, z1, ro, ru) = concat(ecke(hw - ru, z0 + ru, ru, -90, 0), ecke(hw - ro, z1 - ro, ro, 0, 90),
                                             ecke(-(hw - ro), z1 - ro, ro, 90, 180), ecke(-(hw - ru), z0 + ru, ru, 180, 270));
function dev_pts(pts, r) = [for (p = pts) [dev_s(p[0], r), p[1]]];

// Bühnenrahmen (Z 13 bis 97): Innenkante = Portalkante, Außenkante 3 weiter
rb_in = rr_pts(portal_b / 2, portal_z0, portal_z1, portal_ro, portal_ru);
rb_out = rr_pts(portal_b / 2 + rahmen_bb, portal_z0 - rahmen_bb, portal_z1 + rahmen_bb, portal_ro + rahmen_bb, portal_ru + rahmen_bb);
// Fensterrahmen (Z 101 bis 336,4): Innenkante 0,4 außerhalb der Falzkante, Außenkante 3 weiter
fw_in = rr_pts(rahmen_hw_scheibe, 60, scheibe_z1 + (rahmen_hw_scheibe - scheibe_b / 2), scheibe_ro + (rahmen_hw_scheibe - scheibe_b / 2), 3);
fw_out = rr_pts(rahmen_hw_scheibe + rahmen_bb, 60 - rahmen_bb, scheibe_z1 + (rahmen_hw_scheibe - scheibe_b / 2) + rahmen_bb,
                scheibe_ro + (rahmen_hw_scheibe - scheibe_b / 2) + rahmen_bb, 3 + rahmen_bb);
rahmen_z_seite0 = 101;                                            // Seitenleiste von hier bis zum Beginn der oberen Bögen
rahmen_z_seite1 = scheibe_z1 + (rahmen_hw_scheibe - scheibe_b / 2) - (scheibe_ro + (rahmen_hw_scheibe - scheibe_b / 2));   // 307
rahmen_z_oben1 = scheibe_z1 + (rahmen_hw_scheibe - scheibe_b / 2) + rahmen_bb;                                              // 336,4
r_dev_unten = 99.8;                                               // mittlerer Radius des Sockelkegels zwischen Z 13 und 97
r_dev_koerper = koerper_ro;

module band2d(pi, po) {
    polygon(points = concat(po, pi), paths = [[for (i = [0:len(po) - 1]) i], [for (i = [0:len(pi) - 1]) len(po) + i]]);
}

module rahmen_haut(pi, po, z0, z1) {
    zbereich(z0, z1) intersection() {
        quer_extrusion(40, 140) band2d(pi, po);
        difference() {
            env_solid(rahmen_t);
            env_solid(0);
        }
    }
}

module rahmen_flach(pi, po, r, z0, z1) {
    intersection() {
        band2d(dev_pts(pi, r), dev_pts(po, r));
        translate([-300, z0]) square([600, z1 - z0]);
    }
}

module portal_pad(za, zb) {
    // Hinterlegung innen unter dem Scheibenfalz, damit der Falz nicht in der Luft hängt
    zbereich(za, zb) intersection() {
        difference() {
            quer_extrusion(scheibe_x - scheibe_t - 3, 92) offset(delta = pad_b) scheibe2d();
            quer_extrusion(scheibe_x - scheibe_t - 4, 93) portal2d(portal_b, portal_z0, portal_z1, portal_ro, portal_ru);
        }
        env_solid(0);
    }
}

module portal_magnete() {
    // vier Magnettaschen von innen, in den Falzecken (Gegenstück Stahlscheibe auf der Scheibe)
    for (sy = [-1, 1]) for (z = [scheibe_z0 + 12, scheibe_z1 - 30])
        translate([scheibe_x - scheibe_t - 2.5, sy * (portal_b / 2 + 1.5), z]) rotate([0, 90, 0])
            cylinder(d = magnet_d, h = 3.0);
}

// ---- Seitenfenster ----
module fenster_cut(th) {
    rotate([0, 0, th]) quer_extrusion(60, 140) fenster2d();
}

module fenster_fuge_cut(th) {
    rotate([0, 0, th]) intersection() {
        quer_extrusion(60, 140) difference() {
            offset(delta = fenster_fuge) fenster2d();
            fenster2d();
        }
        difference() {
            zyl(koerper_ro + 1, 100, 240);
            zyl(koerper_ro - fenster_fuge_t, 99, 241);
        }
    }
}

module fenster_pad(th) {
    // Rahmen innen für die gedruckte Fensterscheibe 26 x 76 x 1,6 (Klar-PETG), mit Aussparung für die Scheibe
    rotate([0, 0, th]) intersection() {
        difference() {
            quer_extrusion(fenster_pad_x, 98) translate([0, (fenster_z0 + fenster_z1) / 2]) rrect2d(fenster_pad_b, fenster_pad_h, 4);
            quer_extrusion(fenster_pad_x - 1, 99) translate([0, (fenster_z0 + fenster_z1) / 2]) rrect2d(fenster_streifen_b + 0.4, fenster_streifen_h + 0.4, 2);
        }
        zyl(koerper_ri + 0.6, 100, 240);
    }
}

// ============================================================================
// 9 Teile (Gerätekoordinaten, Druckpose jeweils im Block "druck_...")
// ============================================================================

// ---- 1 Sockelschale ----
// Stand 6: Der Goldring ist ein eigenes Teil (Gold-PETG) und liegt auf der Oberkante des Sockels (Z 97),
// der Sockel trägt nur die innere Falzhälfte bis Z 104 durch den Ring hindurch.
sockel_profil = [[sock_ri(z_sock0), z_sock0], [d_sock_u / 2, z_sock0], [d_sock_o / 2, z_ring0],
                 [koerper_ri + falz_t, z_ring0], [koerper_ri + falz_t, z_ring1 + falz_h],
                 [koerper_ri, z_ring1 + falz_h], [koerper_ri, z_ring0]];

// Griffmulde hinten: Boden folgt dem Kegel, oben 45-Grad-Kante, Ecken R 4 in der Ansicht.
// versatz > 0 schiebt die Form nach innen (Wand hinter der Mulde), dz und dy weiten sie auf.
module griff_form(versatz, dz, dy) {
    zi0 = griff_z0 - dz;
    zi1 = griff_z1 + dz;
    intersection() {
        rotate([90, 0, 0]) linear_extrude(height = griff_b + 2 * dy + 2, center = true)
            polygon([[-(sock_r(zi0) - griff_t) + versatz, zi0],
                     [-(sock_r(zi1 - griff_t) - griff_t) + versatz, zi1 - griff_t],
                     [-sock_r(zi1) + versatz, zi1],
                     [-130, zi1], [-130, zi0]]);
        quer_extrusion(-130, 0) translate([0, (griff_z0 + griff_z1) / 2])
            rrect2d(griff_b + 2 * dy, griff_z1 - griff_z0 + 2 * dz, griff_r);
    }
}

module t_sockel() {
    difference() {
        union() {
            rotate_extrude() polygon(sockel_profil);
            // Wand hinter der Griffmulde (Mulde ragt 8 mm in den Hohlraum)
            intersection() {
                griff_form(wand, wand, wand);
                rotate_extrude() polygon([[0, z_sock0], [d_sock_u / 2, z_sock0], [d_sock_o / 2, z_ring0], [0, z_ring0]]);
            }
            // Rippen innen 1,2 x 8, sechs Stück
            for (k = [0:5]) rotate([0, 0, 30 + 60 * k]) rotate([90, 0, 0]) linear_extrude(height = 1.2, center = true)
                polygon([[sock_ri(7) - 8, 7], [sock_ri(7) + 0.6, 7], [sock_ri(96) + 0.6, 96], [sock_ri(96) - 8, 96]]);
            // Laschenböcke für die vier M3 von unten (Grundplatte liegt Z 3 bis 7)
            for (a = laschen_winkel) rotate([0, 0, a]) difference() {
                box(laschen_r - 3.5, sock_ri(10) + 0.8, -4.5, 4.5, z_gp1, z_gp1 + 6);
                translate([laschen_r, 0, z_gp1 - eps]) cylinder(d = m3_pilot, h = 6);
            }
        }
        griff_form(0, 0, 0);
        portal_cut();
        if (budget == 0) portal_magnete();
        // Buchsenloch Ø 8,2 hinten (Einbaubuchse M8), Goldring Ø 16 außen aufgeklebt
        translate([-140, 0, buchse_z]) rotate([0, 90, 0]) cylinder(d = buchse_d, h = 60);
    }
}

// ---- 2 und 3 Körper ----
// Stand 6: Die Teilung bei Z 235 wird nicht gespachtelt, sondern ist eine gewollte Schattenfuge:
// an beiden Außenkanten 0,5 x 45 Grad Fase, zusammen eine V-Nut 1,0 breit und 0,5 tief.
fuge_fase = 0.5;
koerper_unten_profil = [[koerper_ri, z_kor0 + falz_h], [koerper_ro - falz_t, z_kor0 + falz_h], [koerper_ro - falz_t, z_kor0],
                        [koerper_ro, z_kor0], [koerper_ro, z_kor_teil - fuge_fase], [koerper_ro - fuge_fase, z_kor_teil],
                        [koerper_ri + falz_t, z_kor_teil],
                        [koerper_ri + falz_t, z_kor_teil + falz_h], [koerper_ri, z_kor_teil + falz_h]];
koerper_oben_profil = [[koerper_ri, z_kor_teil + falz_h], [koerper_ro - falz_t, z_kor_teil + falz_h], [koerper_ro - falz_t, z_kor_teil],
                       [koerper_ro - fuge_fase, z_kor_teil], [koerper_ro, z_kor_teil + fuge_fase], [koerper_ro, z_kor1], [koerper_ri, z_kor1]];

module koerper_rippen(z0, z1) {
    for (a = [77.1, 128.6, 180, 231.4, 282.9, 334.3]) rotate([0, 0, a]) box(koerper_ri - 8, koerper_ri + 0.4, -0.6, 0.6, z0, z1);
}

module t_koerper_unten() {
    difference() {
        union() {
            rotate_extrude() polygon(koerper_unten_profil);
            koerper_rippen(z_kor0 + falz_h, z_kor_teil - 5);
            if (scheiben == 1) {
                portal_pad(z_kor0 + falz_h, z_kor_teil);
                for (p = fenster_winkel) fenster_pad(p * teilung);
            }
        }
        portal_cut();
        if (scheiben == 1) scheibe_falz_cut();
        if (budget == 0) portal_magnete();
        for (p = fenster_winkel) {
            fenster_cut(p * teilung);
            fenster_fuge_cut(p * teilung);
        }
    }
}

module t_koerper_oben() {
    difference() {
        union() {
            rotate_extrude() polygon(koerper_oben_profil);
            koerper_rippen(z_kor_teil + falz_h + 5, z_kor1);
            if (scheiben == 1) portal_pad(z_kor_teil + falz_h, z_kor1);
        }
        portal_cut();
        if (scheiben == 1) scheibe_falz_cut();
        if (budget == 0) portal_magnete();
    }
}

// ---- 4 Krone ----
module lug(th, mit_magnet) {
    rotate([0, 0, th]) difference() {
        intersection() {
            // Außenkante 0,5 unter der Fasenfläche des Kronenkörpers (r = 100 - (z - 400,8))
            rotate_extrude() polygon([[lug_r0, z_riemen0], [99.0, z_riemen0], [99.0, z_fase0 + 0.7],
                                      [krone_d / 2 - kr_ring_dr - 0.5 - (z_deckel_u - z_fase0), z_deckel_u + eps], [lug_r0, z_riemen0 + 3]]);
            rotate([0, 0, -lug_halb_winkel]) linear_extrude(height = 500)
                polygon([[0, 0], [200, 0], [200 * cos(2 * lug_halb_winkel), 200 * sin(2 * lug_halb_winkel)]]);
        }
        if (mit_magnet == 1)
            translate([94.5, 0, z_riemen0 - eps]) cylinder(d = magnet_d, h = magnet_t);
        else
            translate([94.5, 0, z_riemen0 - eps]) cylinder(d = 3.4, h = 4);
    }
}

// Stand 6: Die Fase ist ein eigenes Teil (Kronenring, Gold-PETG, 2 mm waagrecht dick). Der schwarze Kronenkörper
// trägt die Fase um diese Dicke zurückgesetzt, die Außenmaße bleiben Ø 204 und 6 x 45 Grad.
z_fase0 = z_hoehe - krone_fase;                                      // 400,8
module t_krone() {
    difference() {
        union() {
            // Wand r 99,6 bis 102 bis Z 400,8 (Absatz 2 mm für den Kronenring), darüber eine Schale entlang der Fase
            // (2,4 waagrecht dick) mit Innenkragen Z 397,8 bis 400,8 als Übergang, Deckel 2 dick
            rotate_extrude() polygon([[krone_d / 2 - 2.4, z_kr0], [krone_d / 2, z_kr0], [krone_d / 2, z_fase0],
                                      [krone_d / 2 - kr_ring_dr, z_fase0],
                                      [krone_d / 2 - kr_ring_dr - krone_fase, z_hoehe], [0, z_hoehe],
                                      [0, z_deckel_u],
                                      [krone_d / 2 - kr_ring_dr - 2.4 - (z_deckel_u - z_fase0), z_deckel_u],
                                      [krone_d / 2 - kr_ring_dr - 2.4, z_fase0],
                                      [krone_d / 2 - kr_ring_dr - 2.4, z_fase0 - 3],
                                      [krone_d / 2 - 2.4, z_fase0 - 3]]);
            for (a = lug_winkel_magnet) lug(a, 1);
            for (a = lug_winkel_stift) lug(a, 0);
        }
        // Tasche 92 x 18 x 1,2 für das Namensschild, Leserichtung von vorne (lange Seite entlang Y)
        translate([0, 0, z_hoehe - 1.2]) linear_extrude(height = 2) rotate([0, 0, 90]) rrect2d(92, 18, 2);
    }
}

module t_kronenring() {
    // Gold-PETG, Parallelogramm in (r, z): bildet die Fase 6 x 45 Grad, liegt auf der Fase des Kronenkörpers
    rotate_extrude() polygon([[krone_d / 2, z_fase0], [krone_d / 2 - krone_fase, z_hoehe],
                              [krone_d / 2 - krone_fase - kr_ring_dr, z_hoehe], [krone_d / 2 - kr_ring_dr, z_fase0]]);
}

// ---- 5 Goldband (ersetzt die Lichtfuge) und Goldring (Sockel/Körper) ----
module t_goldband() {
    zk = z_kor1;
    // sichtbarer Ring 338 bis 341, Wand 1,6, Stecker 2 mm in Körper und Krone (Wand 1,2)
    rohr(koerper_ro, koerper_ro - 1.6, zk, zk + 3);
    rohr(koerper_ri - sp, koerper_ri - sp - 1.2, zk - 2, zk + eps);
    rohr(koerper_ri - sp, koerper_ri - sp - 1.2, zk + 3 - eps, zk + 3 + 2);
}

module t_goldring() {
    // Ø 202 x 4, liegt auf dem Sockel (Z 97), Körper steht darauf (Z 101). Innen r 97,3 (Sockelfalz geht hindurch),
    // unten außen 0,8 x 45 Grad Fase als Schattenfuge, am Portal offen (|Y| < 39)
    difference() {
        rotate_extrude() polygon([[koerper_ri + falz_t + sp, z_ring0], [goldring_r1 - 0.8, z_ring0], [goldring_r1, z_ring0 + 0.8],
                                  [goldring_r1, z_ring1], [koerper_ri + falz_t + sp, z_ring1]]);
        box(0, 200, -goldring_gap, goldring_gap, z_ring0 - 1, z_ring1 + 1);
    }
}

// ---- Portalrahmen: drei Leistenarten in Gold-PETG ----
module t_rahmen_unten() {   // Bühnenrahmen: Boden und beide Seiten bis Z 97, flach in der Abwicklung
    linear_extrude(height = rahmen_t) translate([0, -(portal_z0 - rahmen_bb)])
        rahmen_flach(rb_in, rb_out, r_dev_unten, portal_z0 - rahmen_bb, rahmen_naht_unten);
}
module t_rahmen_seite() {   // eine gerade Seitenleiste Z 101 bis 307 (zwei Stück, rechts und links gleich)
    linear_extrude(height = rahmen_t) translate([-dev_s(rahmen_hw_scheibe, r_dev_koerper), -rahmen_z_seite0])
        intersection() {
            rahmen_flach(fw_in, fw_out, r_dev_koerper, rahmen_z_seite0, rahmen_z_seite1);
            translate([0, 0]) square([300, 600]);
        }
}
module t_rahmen_oben() {    // beide Bögen und der obere Balken, Z 307 bis 336,4
    linear_extrude(height = rahmen_t) translate([0, -rahmen_z_seite1])
        rahmen_flach(fw_in, fw_out, r_dev_koerper, rahmen_z_seite1, rahmen_z_oben1);
}

// ---- 6 Grundplatte ----
module t_grundplatte() {
    difference() {
        union() {
            zyl(gp_r, z_gp0, z_gp1);
            // Rippen 2 x 8: Ringrippe am Rand mit Lücken an Laschen und Zugankern, dazu sechs kurze Radialrippen
            difference() {
                rohr(gp_rippe_r1, gp_rippe_r0, z_gp1, z_rippe1);
                for (a = concat(laschen_winkel, zug_winkel)) rotate([0, 0, a]) box(88, 110, -7, 7, z_gp1 - 1, z_rippe1 + 1);
            }
            for (a = [90, 120, 150, 210, 240, 270]) rotate([0, 0, a]) box(21, 36, -1, 1, z_gp1, z_rippe1);
            // Ballastbecher Ø 38 mit Wand, Stapel 7 x 3 mm ragt bis Z 28 (Filz darüber)
            for (b = ballast_pos) rotate([0, 0, b[1]]) translate([b[0], 0, 0]) rohr(ballast_tasche_d / 2 + wand, ballast_tasche_d / 2, z_gp1, z_rippe1);
            // Aufnahmering für den Lagerbock
            rohr(lb_d / 2 + 1.4, lb_d / 2 + 0.2, z_gp1, z_gp1 + 2);
        }
        // Fußtaschen Ø 12,5 x 1 unten
        for (k = [0:5]) rotate([0, 0, 30 + 60 * k]) translate([fuss_r, 0, z_gp0 - eps]) cylinder(d = fuss_tasche_d, h = 1 + eps);
        // Zuganker Ø 5,5 mit Sechskanttasche unten für Mutter
        for (a = zug_winkel) rotate([0, 0, a]) translate([zug_r, 0, 0]) {
            translate([0, 0, z_gp0 - 1]) cylinder(d = zug_loch, h = gp_t + 2);
            translate([0, 0, z_gp0 - eps]) rotate([0, 0, 30]) cylinder(d = 2 * mutter_r_ecke + 0.4, h = 2.2, $fn = 6);   // Schlüsselfläche radial außen
        }
        // Laschenlöcher M3 mit Senkung (Sockelschale von unten)
        for (a = laschen_winkel) rotate([0, 0, a]) translate([laschen_r, 0, 0]) {
            translate([0, 0, z_gp0 - 1]) cylinder(d = m3_d, h = gp_t + 2);
            translate([0, 0, z_gp0 - eps]) cylinder(d1 = m3_kopf_d, d2 = m3_d, h = m3_kopf_t);
        }
        // Säulen der Rinne: M3 von unten
        for (a = saeule_winkel) rotate([0, 0, a]) translate([st_r, 0, z_gp0 - 1]) cylinder(d = m3_d, h = gp_t + 2);
        // Wägezellenbock: zwei Löcher M4 am festen Ende
        for (dx = [-5, 5]) translate([zelle_x + dx, zelle_y0 + 10, z_gp0 - 1]) cylinder(d = m4_d, h = gp_t + 2);
        // Tasche für den Überlastanschlag unter dem Lastende
        translate([zelle_x - 11, -8, z_gp1 - ues_tasche_t]) cube([22, 16, ues_tasche_t + 1]);
        // Datum und Widmung unten, gespiegelt, damit sie von unten gelesen richtig stehen
        translate([0, -45, z_gp0 - 0.1]) mirror([1, 0, 0]) linear_extrude(height = 0.7) text(widmung, size = 6, halign = "center");
    }
}

// ---- 7 Lagerbock ----
module t_lagerbock() {
    difference() {
        zyl(lb_d / 2, lb_z0, lb_z1);
        // zwei Lagersitze 608 (Ø 22 H7 x 7), dazwischen Durchgang Ø 12
        translate([0, 0, lb_z0 + 3]) cylinder(d = lager608_d + 0.1, h = lager608_t + 0.01);
        translate([0, 0, lb_z1 - lager608_t]) cylinder(d = lager608_d + 0.1, h = lager608_t + 1);
        translate([0, 0, lb_z0 - 1]) cylinder(d = 12, h = lb_z1 - lb_z0 + 2);
        // Halterungen für den Hallhalter, M3
        translate([lb_d / 2 - 4, 0, lb_z1 - 12]) rotate([0, 90, 0]) cylinder(d = m3_pilot, h = 6);
    }
}

// ---- 8 Feuchtrinne ----
module t_rinne() {
    a0 = rinne_offen; a1 = 360 - rinne_offen;
    difference() {
        union() {
            translate([0, 0, z_rinne0]) linear_extrude(height = rinne_boden) sektor(rinne_r0, rinne_r1, a0, a1);
            translate([0, 0, z_rinne0]) linear_extrude(height = z_rinne1 - z_rinne0) {
                sektor(rinne_r0, rinne_r0 + wand, a0, a1);
                sektor(rinne_r1 - wand, rinne_r1, a0, a1);
                sektor(rinne_r0, rinne_r1, a0, a0 + 1.6 / rinne_r1 * 57.3);
                sektor(rinne_r0, rinne_r1, a1 - 1.6 / rinne_r1 * 57.3, a1);
                sektor(rinne_r0, rinne_r1, 180 - 0.8 / 57 * 57.3, 180 + 0.8 / 57 * 57.3);
            }
        }
        // M3 Senkungen für die vier Säulen
        for (a = saeule_winkel) rotate([0, 0, a]) translate([st_r, 0, z_rinne0 - 1]) {
            cylinder(d = m3_d, h = rinne_boden + 2);
            translate([0, 0, rinne_boden + 1 - m3_kopf_t]) cylinder(d1 = m3_d, d2 = m3_kopf_d, h = m3_kopf_t + eps);
        }
    }
}

// ---- 8b Rinnendeckel (zwei Hälften, je Kammer eine) ----
module t_rinnendeckel(seite) {
    a0 = seite > 0 ? rinne_offen : 180 + 0.3;
    a1 = seite > 0 ? 180 - 0.3 : 360 - rinne_offen;
    difference() {
        translate([0, 0, z_rinne1]) linear_extrude(height = rdeckel_t) sektor(rinne_r0 + sp, rinne_r1 - sp, a0, a1);
        // Löcher Ø 14 unter den Parkstellungen der Düsen
        for (p = fenster_winkel) rotate([0, 0, p * teilung]) translate([st_r, 0, z_rinne1 - 1]) cylinder(d = rdeckel_loch, h = rdeckel_t + 2);
    }
}

// ---- 9 Rinnensäule (lokal, Fuß bei Z = z_gp1) ----
module t_saeule() {
    difference() {
        zyl(saeule_d / 2, z_gp1, z_rinne0);
        translate([0, 0, z_gp1 - eps]) cylinder(d = m3_pilot, h = 8);
        translate([0, 0, z_rinne0 - 8 + eps]) cylinder(d = m3_pilot, h = 8);
    }
}

// ---- 10 Abstreifhalter (am Rinnenende), lokal um den Ursprung (Mitte Block) ----
module t_abstreifhalter_lokal() {
    difference() {
        box(-8, 8, -10, 10, 0, 10);
        translate([-7.1, -lippe_t / 2 - 0.1, 4]) cube([14.2, lippe_t + 0.2, 7]);
        translate([0, 0, -1]) cylinder(d = m3_d, h = 12);
    }
}

module t_abstreifhalter(vz) {
    // Gerätelage: radial r 49 bis 65 bei theta = vz * lippe_winkel, Z 54 bis 64
    rotate([0, 0, vz * lippe_winkel]) translate([57, 0, z_rinne0]) rotate([0, 0, 0]) t_abstreifhalter_lokal();
}

// ---- 11 Laufring ----
module t_laufring() {
    h = z_lr1 - z_lr0;
    n_r = 7;
    da = (lr_rampe_l / 80 * 57.3) / n_r;      // Rampe 10 mm lang auf r 80, in sieben Stufen
    a_r = n_r * da;
    translate([0, 0, z_lr0]) difference() {
        union() {
            linear_extrude(height = h) sektor(laufring_r0, laufring_r1, lr_offen + a_r, 360 - lr_offen - a_r);
            // Rampen: Oberkante fällt zur Lücke um 1,5 mm ab
            for (i = [0:n_r - 1]) {
                hh = h - lr_rampe_h + lr_rampe_h * (i + 0.5) / n_r;
                linear_extrude(height = hh) sektor(laufring_r0, laufring_r1, lr_offen + i * da, lr_offen + (i + 1) * da + 0.01);
                linear_extrude(height = hh) sektor(laufring_r0, laufring_r1, 360 - lr_offen - (i + 1) * da - 0.01, 360 - lr_offen - i * da);
            }
            // vier Laschen bis zu den Zugankern
            for (a = zug_winkel) rotate([0, 0, a]) hull() {
                translate([laufring_r1 - 1, 0, 0]) cylinder(r = 3, h = h);
                translate([zug_r, 0, 0]) cylinder(r = lasche_r1 - zug_r, h = h);
            }
        }
        for (a = zug_winkel) rotate([0, 0, a]) translate([zug_r, 0, 0]) {
            translate([0, 0, -1]) cylinder(d = zug_loch, h = h + 2);
            // Sechskanttaschen oben und unten, 1,5 tief, Schlüsselfläche außen (außen offen)
            for (zz = [-eps, h - 1.5]) translate([0, 0, zz]) rotate([0, 0, 30]) cylinder(d = 2 * mutter_r_ecke + 0.4, h = 1.5 + eps, $fn = 6);
        }
    }
}

// ---- 12 Karussellplatte (Gerätelage, Park) ----
module flansch_tasche2d() {
    // radial 46 lang ab r 34, 33 breit, Innenecken R 5, nach außen offen bis über den Rand
    hull() {
        for (sy = [-1, 1]) translate([tasche_r0 + tasche_ecke, sy * tasche_mv]) circle(r = tasche_ecke);
        translate([platte_r + 8, -tasche_b / 2]) square([1, tasche_b]);
    }
}

module zylinder_schlitz2d() {
    // Halbkreis R 16 bei r 57, dann radial nach außen offen
    translate([st_r, 0]) circle(r = schlitz_b / 2);
    translate([st_r, -schlitz_b / 2]) square([platte_r + 8 - st_r, schlitz_b]);
}

module t_karussell() {
    difference() {
        union() {
            zyl(platte_r, z_platte0, z_platte1);
            zyl(nabe_d / 2, nabe_z0, z_platte0 + eps);
            // Federzungen sind Teil der Platte, Nasen stehen in den Taschen
        }
        // D-Bohrung 8 in der Nabe
        translate([0, 0, nabe_z0 - 1]) intersection() {
            cylinder(d = welle2_d + 0.3, h = z_platte1 - nabe_z0 + 2);
            translate([-10, -10, 0]) cube([10 + welle_flach, 20, z_platte1 - nabe_z0 + 2]);
        }
        for (p = fenster_winkel) rotate([0, 0, p * teilung]) {
            // Tasche 3,5 tief
            translate([0, 0, z_platte1 - tasche_t]) linear_extrude(height = tasche_t + 1) flansch_tasche2d();
            // Zylinderschlitz durch, oben mit Einlaufschräge 1 x 45 Grad
            translate([0, 0, z_platte0 - 1]) linear_extrude(height = platte_t + 2) zylinder_schlitz2d();
            hull() {
                translate([0, 0, z_platte1 - 1]) linear_extrude(height = eps) zylinder_schlitz2d();
                translate([0, 0, z_platte1]) linear_extrude(height = eps) offset(delta = 1) zylinder_schlitz2d();
            }
            // Rastzungen: Zunge 1,5 dick neben der Tasche, außen und innen frei geschlitzt, nur am Wurzelende (r 66) fest
            for (s = [-1, 1]) {
                translate([rast_r0, s > 0 ? tasche_b / 2 + rast_t : -(tasche_b / 2 + rast_t + rast_schlitz), z_platte0 - 1])
                    cube([rast_r1 - rast_r0 + 2, rast_schlitz, platte_t + 2]);
                translate([rast_r0, s > 0 ? tasche_b / 2 - rast_schlitz : -tasche_b / 2, z_platte0 - 1])
                    cube([rast_r1 - rast_r0 + 2, rast_schlitz, platte_t - tasche_t + 1.01]);
            }
            // Stationsbuchstabe 0,6 tief neben der Tasche (Stand 6: statt Farbring), lesbar von vorne
            translate([76, tasche_b / 2 + 8.2, z_platte1 - 0.6]) rotate([0, 0, 90]) linear_extrude(height = 1)
                text(stationsbuchstabe[p - 1], size = 8, halign = "center", valign = "center");
        }
        // Rollenböcke: sieben Paare M3 von oben
        for (j = [0:6]) rotate([0, 0, (j + 0.5) * teilung]) for (s = [-1, 1])
            translate([bock_achse_r, s * 10, z_platte0 - 1]) cylinder(d = m3_d, h = platte_t + 2);
    }
    // Nasen der Federzungen
    for (p = fenster_winkel) rotate([0, 0, p * teilung]) for (s = [-1, 1])
        translate([rast_r1 - 3, s > 0 ? tasche_b / 2 - rast_nase : -tasche_b / 2, z_platte1 - tasche_t])
            cube([2.5, rast_nase, tasche_t]);
}

// ---- 13 Rollenbock (Gabel offen nach oben, Gerätelage bei theta = 0, Achse radial) ----
module t_rollenbock() {
    difference() {
        intersection() { union() {
            // zwei Wangen 2 dick
            box(bock_r0, bock_r0 + 2, -bock_halb, bock_halb, bock_z0, z_platte0);
            box(bock_r1 - 2, bock_r1, -bock_halb, bock_halb, bock_z0, z_platte0);
            // Ohren oben außerhalb der Rolle (y 8 bis 12), tragen die M3
            for (s = [-1, 1]) box(bock_r0, bock_r1, s > 0 ? 8 : -12, s > 0 ? 12 : -8, z_platte0 - 3.5, z_platte0);
        }
        zyl(bock_r1, bock_z0 - 1, z_platte0 + 1); }   // Außenfläche als Bogen r 85,5
        // Achse M8 radial bei r 80, Z 199,5
        translate([bock_r0 - 1, 0, bock_achse_z]) rotate([0, 90, 0]) cylinder(d = 8.2, h = bock_r1 - bock_r0 + 2);
        // Rolle (608, Ø 22) Freiraum
        translate([bock_achse_r - lager608_t / 2 - 0.1, 0, bock_achse_z]) rotate([0, 90, 0]) cylinder(d = lager608_d + 1, h = lager608_t + 0.2);
        for (s = [-1, 1]) translate([bock_achse_r, s * 10, z_platte0 - 4]) cylinder(d = 2.5, h = 4.5);
    }
}

// ---- 14 Schlitten (Gerätelage bei S = s_pos) ----
module t_schlitten() {
    zb = s_pos - schl_u;
    translate([0, 0, zb]) difference() {
        cylinder(r = schl_r, h = schl_h);
        // zwei Bohrungen für LM10LUU bei Y +-22, Madenschraube radial
        for (s = [-1, 1]) {
            translate([0, s * welle_y, -1]) cylinder(d = schl_bohr_d, h = schl_h + 2);
            translate([0, s * welle_y, schl_h / 2]) rotate([0, -90, 0]) cylinder(d = m3_pilot, h = schl_r);
        }
        // Stufenbohrung von oben: Ø 23 x 12,5 tief, unten Mutternflansch Ø 22 x 3,5, vier M3
        translate([0, 0, schl_h - schl_tasche_t]) cylinder(d = schl_tasche_d, h = schl_tasche_t + 1);
        translate([0, 0, -1]) cylinder(d = 12, h = schl_h + 2);
        for (a = [45, 135, 225, 315]) rotate([0, 0, a]) translate([8, 0, schl_h - schl_tasche_t - 8]) cylinder(d = m3_pilot, h = 8.1);
        // ebene Fläche bei X 28 über die volle Höhe für den senkrechten Schenkel des Winkels
        translate([arm_x0, -schl_r - 1, -1]) cube([schl_r, 2 * schl_r + 2, schl_h + 2]);
        // zwei Gewindeeinsätze M4 waagrecht, bei S + 16 und S + 42
        for (zz = winkel_schraube_z) translate([arm_x0 - einsatz_m4_t, 0, schl_u + zz]) rotate([0, 90, 0]) cylinder(d = einsatz_m4_d, h = einsatz_m4_t + 1);
    }
}

// ---- 15 Ausleger mit Stempel (ein Stück PETG, ersetzt Winkelstahl und Stempelscheibe) ----
// Platte X 28 bis 36 an der Schlittenfläche, Arm X 28 bis 68 (Z S + 8 bis S + 16), Stempelfuß Ø 25 bei X 53 (Z S + 2 bis S + 8),
// zwei Stützrippen. Gedruckt liegt er auf der Seite (Y nach oben): das L-Profil steht dann in jeder Schicht.
// Unter dem Stempel klebt eine 2 mm Gummiauflage (Gummi oder Silikon, Kaufteil).
module t_ausleger() {
    zb = s_pos + arm_z0;
    difference() {
        union() {
            box(arm_x0, arm_x0 + platte_dick, -arm_b / 2, arm_b / 2, zb, zb + winkel_h);
            box(arm_x0, arm_x1, -arm_b / 2, arm_b / 2, zb, zb + arm_t);
            translate([stempel_x, 0, s_pos + gummi_t]) cylinder(d = stempel_d, h = stempel_t + eps);
            for (y0 = [arm_b / 2, -arm_b / 2 + rippe_b]) translate([0, y0, 0]) rotate([90, 0, 0]) linear_extrude(height = rippe_b)
                polygon([[arm_x0 + platte_dick - eps, zb + arm_t - eps], [arm_x0 + platte_dick + rippe_l, zb + arm_t - eps],
                         [arm_x0 + platte_dick - eps, zb + arm_t + rippe_h]]);
        }
        for (zz = winkel_schraube_z) {
            translate([arm_x0 - 1, 0, s_pos + zz]) rotate([0, 90, 0]) cylinder(d = m4_d, h = platte_dick + 2);
            translate([arm_x0 + platte_dick - 4, 0, s_pos + zz]) rotate([0, 90, 0]) cylinder(d = 7.6, h = 5);   // Senkung für M4-Zylinderkopf
        }
    }
}

// ---- 16 Brücke ----
module t_bruecke() {
    difference() {
        union() {
            zyl(br_r, z_br0, z_br1);
            // Rippen 2 x 9, zwischen Riemen und Kronendeckel ausgespart (Rippe bei 195 Grad erst ab r 70)
            for (a = br_rippe_winkel) rotate([0, 0, a]) box(a == 195 ? 70 : 22, br_r - 2, -br_rippe_t / 2, br_rippe_t / 2, z_br1, z_br1 + br_rippe_h);
            // Klemmnaben für die Führungswellen
            for (s = [-1, 1]) translate([0, s * welle_y, 0]) zyl(klemm_d / 2, z_br1, z_br1 + klemm_h);
            // Stifte für die Krone
            for (a = lug_winkel_stift) rotate([0, 0, a]) translate([94.5, 0, z_br1 - eps]) cylinder(d = 3, h = 3.5);
        }
        // Lagersitz 608 mittig
        translate([0, 0, z_br0 - 1]) cylinder(d = lager608_d + 0.1, h = br_t + 2);
        // Führungswellen, in der Nabe eingeklemmt, Klemmschlitz und M3
        for (s = [-1, 1]) translate([0, s * welle_y, z_br0 - 1]) cylinder(d = welle_d + 0.2, h = welle_einsp + 1);
        for (s = [-1, 1]) translate([klemm_d / 2 - 2, s * welle_y, z_br1 + klemm_h / 2]) rotate([0, 90, 0]) cylinder(d = m3_d, h = 5);
        // Zuganker mit Sechskanttasche oben (Mutter versenkt)
        for (a = zug_winkel) rotate([0, 0, a]) translate([zug_r, 0, 0]) {
            translate([0, 0, z_br0 - 1]) cylinder(d = zug_loch, h = br_t + 2);
            translate([0, 0, z_br1 - 4.5]) rotate([0, 0, 30]) cylinder(d = 2 * mutter_r_ecke + 0.4, h = 5, $fn = 6);   // Stange endet bündig bei z_br1
        }
        // Langloch für Motor 1 bei theta 180, r 59, +-3
        hull() for (dy = [-3, 3]) translate([-motor1_r, dy, z_br0 - 1]) cylinder(d = 5.4, h = br_t + 2);
        // Montage Motor 1: vier M3 in den Langlochbereich
        // Magnettaschen für die Krone
        for (a = lug_winkel_magnet) rotate([0, 0, a]) translate([94.5, 0, z_br1 - magnet_t + eps]) cylinder(d = magnet_d, h = magnet_t);
        // Schalter-Tasche in der Unterseite bei X -26
        translate([schalter_x - schalter_l / 2, -schalter_b / 2 - 0.2, z_br0 - 1]) cube([schalter_l + 0.4, schalter_b + 0.4, 5]);
        // Kabeldurchführung am Zuganker -128,6
        rotate([0, 0, -2.5 * teilung]) translate([zug_r - 10, 0, z_br0 - 1]) cylinder(d = 6, h = br_t + 2);
    }
}

// ---- 18 GT2-Rad 70 Z (Gerätelage) ----
module t_gt2_rad() {
    z = 70;
    r_tip = gt2_70_teilkreis / 2 - 0.38;
    difference() {
        union() {
            zyl(r_tip, gt2_70_z0 + 1, gt2_70_z1 - 1);
            zyl(gt2_70_aussen / 2, gt2_70_z0, gt2_70_z0 + 1);
            zyl(gt2_70_aussen / 2, gt2_70_z1 - 1, gt2_70_z1);
            zyl(10, gt2_70_nabe_z0, gt2_70_z0 + eps);
        }
        // Zahnlücken GT2
        for (i = [0:z - 1]) rotate([0, 0, i * 360 / z]) translate([r_tip, 0, gt2_70_z0 + 1 - eps]) cylinder(d = 1.5, h = gt2_70_z1 - gt2_70_z0 - 2 + 2 * eps, $fn = 12);
        // D-Bohrung 8
        translate([0, 0, gt2_70_nabe_z0 - 1]) intersection() {
            cylinder(d = welle2_d + 0.2, h = 12);
            translate([-10, -10, 0]) cube([10 + 3.5, 20, 12]);
        }
        translate([0, 0, gt2_70_nabe_z0 + 1]) rotate([0, 90, 0]) cylinder(d = m3_pilot, h = 12);
        // Magnettasche Ø 5,2 x 2,2 unten auf r 15
        translate([hall_r, 0, gt2_70_z0 - eps]) cylinder(d = 5.2, h = 2.2);
    }
}

// ---- 19 Schublade (Gerätelage, geschlossen) ----
// Vorderende folgt der Innenfläche der Front (Kegel, Front 8 dick), dort 2 mm Stirnwand für die Front
module front_innen_solid(z0, z1) {
    rotate_extrude() polygon([[0, z0], [sock_r(z0) - front_t, z0], [sock_r(z1) - front_t, z1], [0, z1]]);
}

module t_schublade() {
    difference() {
        intersection() {
            union() {
                box(schub_x0, schub_x1, -schub_b / 2, schub_b / 2, z_schub0, z_becher0);
                for (s = [-1, 1]) box(schub_x0, schub_x1, s > 0 ? schub_b / 2 - schub_wand : -schub_b / 2, s > 0 ? schub_b / 2 : -schub_b / 2 + schub_wand, z_schub0, schub_z1);
                // Stirnwand 2 mm hinter der Front
                intersection() {
                    box(schub_x0, schub_x1, -schub_b / 2, schub_b / 2, z_schub0, schub_z1);
                    difference() {
                        front_innen_solid(z_schub0 - 2, schub_z1 + 2);
                        rotate_extrude() polygon([[0, z_schub0 - 3], [sock_r(z_schub0 - 3) - front_t - 2, z_schub0 - 3],
                                                  [sock_r(schub_z1 + 3) - front_t - 2, schub_z1 + 3], [0, schub_z1 + 3]]);
                    }
                }
                // Bechersitz, innen konisch
                translate([zelle_x, 0, z_becher0 - eps]) cylinder(d = sitz_da, h = sitz_h);
            }
            front_innen_solid(z_schub0 - 2, schub_z1 + 2);
        }
        // Freistich unter Wänden und Boden über den Schienen, nur die Kufen hinten (X 22 bis 25) reichen bis Z 26
        for (s = [-1, 1]) translate([schub_x0 + kufe_l, s > 0 ? schiene_y0 - 0.1 : -schiene_y1 - 0.1, z_schub0 - 1])
            cube([schub_x1, schiene_y1 - schiene_y0 + 0.2, 1 + kufe_freigang - 0.5]);
        // konischer Sitz: zentriert den Becherboden Ø 47
        translate([zelle_x, 0, z_becher0 - 2 * eps]) cylinder(d1 = sitz_du, d2 = sitz_do, h = sitz_h + 4 * eps);
        // zwei M3 durch die Stirnwand in die Front
        for (s = [-1, 1]) translate([sock_r(z_schub0 + 8) - front_t - 12, s * 25, z_schub0 + 8]) rotate([0, 90, 0]) cylinder(d = m3_d, h = 14);
    }
}

// ---- 20 Schubladenfront (folgt der Sockelkontur, steht beim Druck aufrecht wie in der Montage) ----
module t_front() {
    difference() {
        union() {
            intersection() {
                difference() {
                    rotate_extrude() polygon([[0, front_z0], [sock_r(front_z0), front_z0], [sock_r(front_z1), front_z1], [0, front_z1]]);
                    front_innen_solid(front_z0 - 1, front_z1 + 1);
                }
                box(0, 200, -front_b / 2, front_b / 2, front_z0, front_z1);
            }
        }
        // Magnettasche 6 x 2 von innen, Mitte
        translate([sock_r(front_z0 + 14) - front_t - 0.1, 0, front_z0 + 4]) rotate([0, 90, 0]) cylinder(d = magnet_d, h = magnet_t + 0.1);
        // M3-Kernlöcher gegenüber der Stirnwand
        for (s = [-1, 1]) translate([sock_r(z_schub0 + 8) - front_t - 0.2, s * 25, z_schub0 + 8]) rotate([0, 90, 0]) cylinder(d = m3_pilot, h = 6);
    }
}

// ---- 20b Goldlippe (Gold-PETG): Daumenauflage 3 x 1,5 oben auf der Front, 4,5 tief für die Klebefläche ----
module t_lippe() {
    intersection() {
        rotate_extrude() polygon([[sock_r(front_z1) - 3, front_z1], [sock_r(front_z1) + lippe_h, front_z1],
                                  [sock_r(front_z1) + lippe_h, front_z1 + lippe_b], [sock_r(front_z1) - 3, front_z1 + lippe_b]]);
        box(0, 200, -front_b / 2, front_b / 2, front_z1 - 1, front_z1 + lippe_b + 1);
    }
}

// ---- 21 Podest: Scheibe Ø 60 x 1,6 (PETG schwarz) auf Stiel Ø 14, liegt um die Becherachse (X = zelle_x) ----
module t_podest() {
    translate([zelle_x, 0, 0]) difference() {
        union() {
            zyl(podest_d / 2, z_podest0, z_podest1);
            zyl(podest_stiel_d / 2, z_zelle1, z_podest0 + eps);
        }
        for (s = [-1, 1]) translate([0, s * 4, z_zelle1 - 1]) cylinder(d = 3.3, h = 4);
    }
}

// ---- 22 Wägezellenbock, Überlastanschlag ----
module t_waegebock() {
    // festes Ende der Wägezelle auf 0,5 hohem Bock (zwei Lagen), M4
    difference() {
        box(zelle_x - 12, zelle_x + 12, zelle_y0, zelle_y0 + 20, z_gp1, z_gp1 + 0.5);
        for (dx = [-5, 5]) translate([zelle_x + dx, zelle_y0 + 10, z_gp1 - 1]) cylinder(d = m4_d, h = 3);
    }
}

module t_anschlag() {
    // liegt in der Tasche der Grundplatte, Oberkante 0,8 unter der Zelle
    box(zelle_x - 10, zelle_x + 10, -7, 7, z_gp1 - ues_tasche_t, z_zelle0 - ues_luft);
}

// ---- 23 Kleinteile ----
module t_motor2_winkel() {
    // Tisch über dem Pancake-Motor (Flansch oben), zwei Wangen, Füße mit M3, Zentrierbund Ø 22,5, Langlöcher +-3
    pz = m2_z1;
    difference() {
        union() {
            box(m2_x - 24, m2_x + 24, -24, 24, pz, pz + 2.5);
            for (s = [-1, 1]) {
                box(m2_x - 24, m2_x + 24, s > 0 ? nema_b / 2 + 1 : -nema_b / 2 - 4, s > 0 ? nema_b / 2 + 4 : -nema_b / 2 - 1, z_gp1, pz + 2.5);
                box(m2_x - 24, m2_x + 24, s > 0 ? nema_b / 2 + 4 : -nema_b / 2 - 12, s > 0 ? nema_b / 2 + 12 : -nema_b / 2 - 4, z_gp1, z_gp1 + 3);
            }
        }
        translate([m2_x, 0, pz - 1]) cylinder(d = 22.5, h = 5);
        for (sx = [-1, 1]) for (sy = [-1, 1]) hull() for (dx = [-3, 3])
            translate([m2_x + sx * 15.5 + dx, sy * 15.5, pz - 1]) cylinder(d = m3_d, h = 5);
        for (sx = [-1, 1]) for (sy = [-1, 1]) translate([m2_x + sx * 15, sy * (nema_b / 2 + 8), z_gp1 - 1]) cylinder(d = m3_d, h = 5);
    }
}

module t_hallhalter() {
    // Arm vom Lagerbock zum 70er-Rad, Stirn des A3144 liegt 1,5 unter dem Rad (Z 41,5)
    difference() {
        box(hall_r - 2.5, lb_d / 2 + 2, -4, 4, lb_z1 - 2, lb_z1 + 1.0);
        translate([hall_r - 2.2, -2.7, lb_z1 - 1.5]) cube([4.4, 5.4, 4]);
    }
}

module t_platinenhalter() {
    // zwei Leisten 4 x 4 an den Enden der Lochrasterplatine 70 x 90 (Ebene Y -81), Nut 1 tief, Platine steht ab Z 30
    // (zwischen den Ballaststapeln bei -71 und -120 ist unten kein Platz für breite Füße)
    for (x = [-49, 45]) difference() {
        box(x, x + 4, platine_y - 2, platine_y + 2, z_gp1, 60);
        box(-46, 46, platine_y - 1.0, platine_y + 1.0, platine_z0, 61);
    }
}

module t_kabelclip() {
    // Schelle um den Zuganker (Ø 5) mit Schlitz, außen ein Kabelauge Ø 4 zur Fahrzeugmitte hin
    translate([zug_r, 0, 0]) difference() {
        union() {
            cylinder(d = 8.6, h = 8);
            translate([-7.5, 0, 0]) cylinder(d = 8, h = 8);
            translate([-7.5, -1.5, 0]) cube([7.5, 3, 8]);
        }
        translate([0, 0, -1]) cylinder(d = zug_d + 0.3, h = 10);
        translate([0, -0.6, -1]) cube([6, 1.2, 10]);
        translate([-7.5, 0, -1]) cylinder(d = 4, h = 10);
    }
}

module t_fugenhalter() {
    // Haltewinkel am Zuganker auf Z 333 bis 336, trägt den Goldbandring
    difference() {
        union() {
            hull() {
                translate([zug_r, 0, 333]) cylinder(r = 5, h = 3);
                translate([koerper_ri - 1, 0, 333]) cylinder(r = 3, h = 3);
            }
            translate([koerper_ri - 2, -3, 333]) cube([2.5, 6, 3.0]);
        }
        translate([zug_r, 0, 332]) cylinder(d = zug_loch, h = 6);
    }
}

module t_schiene(s) {
    // L-Schiene: Balken Z 22,5 bis 26,5 über der Wägezelle, Pfosten vorn und hinten, Rampe hinten
    y0 = s > 0 ? schiene_y0 : -schiene_y1;
    y1 = s > 0 ? schiene_y1 : -schiene_y0;
    difference() {
        union() {
            // Balken mit Rampe
            rotate([90, 0, 0]) translate([0, 0, -y1]) linear_extrude(height = y1 - y0)
                polygon([[schiene_x0, schiene_balken_u], [schiene_x1, schiene_balken_u], [schiene_x1, schiene_z1],
                         [schiene_x0 + schiene_rampe_l, schiene_z1], [schiene_x0, schiene_z1 - schiene_rampe_h]]);
            box(schiene_x0, schiene_x0 + schiene_pfosten_l, y0, y1, z_gp1, schiene_balken_u + eps);
            box(schiene_x1 - schiene_pfosten_l, schiene_x1, y0, y1, z_gp1, schiene_balken_u + eps);
        }
        // Reed-Kontakt Glas 2 x 14 in der rechten Schiene bei X 30
        if (s > 0) translate([30 - 7.2, (y0 + y1) / 2 - 1.3, schiene_balken_u - 1]) cube([14.4, 2.6, 2.6]);
        // M3 in die Grundplatte
        for (x = [schiene_x0 + 4, schiene_x1 - 4]) translate([x, (y0 + y1) / 2, z_gp1 - 1]) cylinder(d = m3_pilot, h = 6);
    }
}

// ---- 24 Einführzunge (lokal flach) ----
module t_zunge() {
    cube([zunge_l, zunge_b, zunge_t]);
    // Haken vorne
    translate([zunge_l - 3, zunge_b / 2 - 3, 0]) cube([3, 6, 6]);
}

// ---- 25 Spritzenablage (lokal) ----
module t_ablage() {
    difference() {
        box(0, ablage_l, 0, ablage_b, 0, ablage_h);
        for (i = [0:2]) for (j = [0:1])
            translate([ablage_l / 6 + i * ablage_l / 3, ablage_b / 4 + j * ablage_b / 2, 3]) cylinder(d = 32.5, h = ablage_h);
    }
}

// ---- 26 Scheiben (gedruckt) ----
// Portalscheibe in zwei Hälften mit Überlappung: unten Z 99 bis 219, oben Z 215 bis 333. In der Überlappung (4 mm, hinter der
// Karussellplatte Z 211 bis 223) hat jede Hälfte nur die halbe Dicke, außen bündig. Rauch-PETG, transparent.
module scheibe_vol(x0, x1) {
    intersection() {
        translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(height = x1 - x0) scheibe2d();
        box(0, 200, -100, 100, 0, 400);
    }
}

module t_portalscheibe(teil) {
    xi = scheibe_x - scheibe_t; xm = scheibe_x - scheibe_t / 2; xa = scheibe_x;
    za = scheibe_zt - scheibe_ov / 2; zb = scheibe_zt + scheibe_ov / 2;
    if (teil == 0) {   // unten: außen bis Z 215, innen halb bis 219
        intersection() { scheibe_vol(xi, xa); box(0, 200, -100, 100, 0, za); }
        intersection() { scheibe_vol(xi, xm + eps); box(0, 200, -100, 100, za - eps, zb); }
    } else {           // oben: außen halb ab Z 215, voll ab 219
        intersection() { scheibe_vol(xm - eps, xa); box(0, 200, -100, 100, za, zb + eps); }
        intersection() { scheibe_vol(xi, xa); box(0, 200, -100, 100, zb, 400); }
    }
}

module t_fensterscheibe() {
    linear_extrude(height = fenster_streifen_t) rrect2d(fenster_streifen_b, fenster_streifen_h, 2);
}

// Lage im Gerät bei theta = 0: flach bei X 94,0 bis 95,6 hinter dem Fenster, im Rahmen (fenster_pad) verklebt
module fensterscheibe_montage() {
    translate([94.0, 0, (fenster_z0 + fenster_z1) / 2]) rotate([90, 0, 90]) linear_extrude(height = fenster_streifen_t)
        rrect2d(fenster_streifen_b, fenster_streifen_h, 2);
}

// ---- 27 Buchsenring ----
module t_klebering() {
    // innen liegender Klebering der Körperhälften, PETG 8 x 1,2, am Portal offen
    translate([0, 0, z_kor_teil - 4]) linear_extrude(height = 8) sektor(koerper_ri - sp - 1.2, koerper_ri - sp, 30, 330);
}

module t_namensschild() {
    // Schild 90 x 16 x 0,6 mit Schrift 0,6 erhaben, liegt bündig in der Kronentasche (lokal flach)
    linear_extrude(height = 0.6) rrect2d(90, 16, 2);
    translate([0, 0, 0.6]) linear_extrude(height = 0.6) text(str(name_gravur, " Atelier"), size = 9, halign = "center", valign = "center");
}

module t_buchsenring() {
    difference() {
        cylinder(d = buchsenring_d, h = 3);
        translate([0, 0, -1]) cylinder(d = buchse_d, h = 5);
    }
}

// ============================================================================
// 10 Druckposen
// ============================================================================
module druck(name) {
    if (name == "sockel") translate([0, 0, -z_sock0]) t_sockel();
    else if (name == "koerper_unten") translate([0, 0, -z_kor0]) t_koerper_unten();
    else if (name == "koerper_oben") translate([0, 0, z_kor1]) rotate([180, 0, 0]) t_koerper_oben();
    else if (name == "krone") translate([0, 0, z_hoehe]) rotate([180, 0, 0]) t_krone();
    else if (name == "goldband") translate([0, 0, -(z_kor1 - 2)]) t_goldband();
    else if (name == "goldring") translate([0, 0, -z_ring0]) t_goldring();
    else if (name == "kronenring") translate([0, 0, -z_fase0]) t_kronenring();
    else if (name == "rahmen_unten") t_rahmen_unten();
    else if (name == "rahmen_seite") t_rahmen_seite();
    else if (name == "rahmen_oben") t_rahmen_oben();
    else if (name == "lippe") translate([-(sock_r(front_z1) - 3), 0, -front_z1]) t_lippe();
    else if (name == "portalscheibe_unten") translate([-scheibe_z0, 0, scheibe_x]) rotate([0, 90, 0]) t_portalscheibe(0);
    else if (name == "portalscheibe_oben") translate([-(scheibe_zt - scheibe_ov / 2), 0, scheibe_x]) rotate([0, 90, 0]) t_portalscheibe(1);
    else if (name == "fensterscheibe") t_fensterscheibe();
    else if (name == "grundplatte") translate([0, 0, -z_gp0]) t_grundplatte();
    else if (name == "lagerbock") translate([0, 0, -lb_z0]) t_lagerbock();
    else if (name == "rinne") translate([0, 0, -z_rinne0]) t_rinne();
    else if (name == "rinnendeckel") translate([0, 0, -z_rinne1]) t_rinnendeckel(1);
    else if (name == "saeule") translate([0, 0, -z_gp1]) t_saeule();
    else if (name == "abstreifhalter") t_abstreifhalter_lokal();
    else if (name == "laufring") translate([0, 0, -z_lr0]) t_laufring();
    else if (name == "karussell") translate([0, 0, z_platte1]) rotate([180, 0, 0]) t_karussell();
    else if (name == "rollenbock") translate([-(bock_r0 + bock_r1) / 2, 0, -bock_z0]) t_rollenbock();
    else if (name == "schlitten") translate([0, 0, -(s_pos - schl_u)]) t_schlitten();
    else if (name == "ausleger") translate([-arm_x0, s_pos + arm_z0 + winkel_h, arm_b / 2]) rotate([90, 0, 0]) t_ausleger();
    else if (name == "bruecke") translate([0, 0, -z_br0]) t_bruecke();
    else if (name == "gt2_rad") translate([0, 0, gt2_70_z1]) rotate([180, 0, 0]) t_gt2_rad();
    else if (name == "schublade") translate([-schub_x0, 0, -z_schub0]) t_schublade();
    else if (name == "front") translate([-front_x_min, 0, -front_z0]) t_front();
    else if (name == "podest") translate([-zelle_x, 0, z_podest1]) rotate([180, 0, 0]) t_podest();
    else if (name == "waegebock") translate([-zelle_x, -zelle_y0 - 10, -z_gp1]) t_waegebock();
    else if (name == "anschlag") translate([-zelle_x, 0, -(z_gp1 - ues_tasche_t)]) t_anschlag();
    else if (name == "motor2_winkel") translate([-m2_x, 0, -z_gp1]) t_motor2_winkel();
    else if (name == "hallhalter") translate([-hall_r, 0, -(lb_z1 - 2)]) t_hallhalter();
    else if (name == "platinenhalter") translate([0, -platine_y, -z_gp1]) t_platinenhalter();
    else if (name == "klebering") translate([0, 0, -(z_kor_teil - 4)]) t_klebering();
    else if (name == "namensschild") t_namensschild();
    else if (name == "kabelclip") translate([-zug_r, 0, 0]) t_kabelclip();
    else if (name == "fugenhalter") translate([-zug_r, 0, -333]) t_fugenhalter();
    else if (name == "schiene") translate([-schiene_x0, schiene_z1, -schiene_y0]) rotate([90, 0, 0]) t_schiene(1);
    else if (name == "zunge") t_zunge();
    else if (name == "ablage") t_ablage();
    else if (name == "buchsenring") t_buchsenring();
    else echo(str("Unbekanntes Teil: ", name));
}

// ============================================================================
// 11 Kaufteile (nur Montage, Platzhalter)
// ============================================================================
module spritze_kauf(kp_z, farbe) {
    kp = kp_z;
    // Zylinder
    color([0.91, 0.93, 0.94, 0.25]) translate([0, 0, z_zyl_u]) difference() {
        cylinder(r = sp_ro, h = sp_len);
        translate([0, 0, -eps]) cylinder(r = sp_ri, h = sp_len + 1);
    }
    // Farbfüllung
    kolben_z = z_zyl_u + 3 + (kp - z_kp_leer);
    color(farbe) translate([0, 0, z_zyl_u + 1]) cylinder(r = sp_ri - 0.2, h = max(0.5, kolben_z - z_zyl_u - 1));
    // Konus
    color([0.91, 0.93, 0.94, 0.5]) translate([0, 0, z_konus_spitze]) cylinder(d1 = sp_konus_d2, d2 = sp_konus_d1, h = sp_konus_len);
    // Ventil
    color([0.85, 0.84, 0.8, 0.6]) translate([0, 0, z_vent_spitze]) cylinder(d1 = 2, d2 = vent_d, h = vent_l);
    // Flansch
    color([0.91, 0.93, 0.94, 0.6]) translate([-sp_fl_l / 2, -sp_fl_b / 2, z_fl_o - sp_fl_t]) cube([sp_fl_l, sp_fl_b, sp_fl_t]);
    // Kolbenstange und -platte
    color([0.9, 0.9, 0.9]) translate([-sp_stange / 2, -sp_stange / 2, kolben_z]) cube([sp_stange, sp_stange, kp - sp_kp_t - kolben_z]);
    color([0.9, 0.9, 0.9]) translate([0, 0, kp - sp_kp_t]) cylinder(d = sp_kp_d, h = sp_kp_t);
}

farben = [[0.96, 0.96, 0.93], [1.0, 0.82, 0.0], [0.83, 0.0, 0.48], [0.0, 0.58, 0.83], [0.11, 0.1, 0.1], [0.96, 0.96, 0.93]];

module kaufteile() {
    // Spritzen im Karussell
    rotate([0, 0, phi]) for (p = fenster_winkel) rotate([0, 0, p * teilung]) translate([st_r, 0, 0]) {
        spritze_kauf(z_kp_leer + 0.55 * hub_nutz, farben[p - 1]);
    }
    // Karussellwelle, Spindel, Führungswellen
    color([0.55, 0.55, 0.57]) zyl(welle2_d / 2, welle2_z0, welle2_z1);
    color([0.55, 0.55, 0.57]) zyl(spindel_d / 2, spindel_z0, spindel_z1);
    color([0.55, 0.55, 0.57]) for (s = [-1, 1]) translate([0, s * welle_y, 0]) zyl(welle_d / 2, welle_z0, z_br0 + welle_einsp);
    // LM10LUU und Mutter am Schlitten
    color([0.7, 0.7, 0.72]) for (s = [-1, 1]) translate([0, s * welle_y, s_pos - 5]) zyl(lm10_d / 2, 0, lm10_l);
    color([0.69, 0.55, 0.34]) translate([0, 0, s_pos + 20.5]) cylinder(d = mutter_d, h = mutter_l + mutter_fl_t);
    color([0.55, 0.55, 0.57]) translate([0, 0, z_stellring0]) cylinder(d = stellring_d, h = stellring_h);
    // Gummiauflage unter dem Stempel (Ausleger und Stempel sind jetzt ein gedrucktes Teil)
    color([0.2, 0.2, 0.2]) translate([stempel_x, 0, s_pos]) cylinder(d = stempel_d, h = gummi_t);
    // Motoren
    color([0.2, 0.2, 0.22]) translate([-motor1_r - nema_b / 2, -nema_b / 2, z_m1_0]) cube([nema_b, nema_b, m1_l]);
    color([0.2, 0.2, 0.22]) translate([m2_x - nema_b / 2, -nema_b / 2, m2_z0]) cube([nema_b, nema_b, nema_l2]);
    // Riemenscheiben und Riemen oben
    for (xm = [0, -motor1_r]) color([0.4, 0.4, 0.42]) translate([xm, 0, z_riemen0]) {
        cylinder(d = gt2_20_d, h = gt2_h_nutz);
        cylinder(d = 13, h = gt2_h_gekauft);   // Nabe oben
    }
    color([0.1, 0.1, 0.1]) box(-motor1_r, 0, -3, 3, z_riemen0 + 1, z_riemen0 + gt2_h_nutz - 1);
    // Zuganker
    color([0.55, 0.55, 0.57]) for (a = zug_winkel) rotate([0, 0, a]) translate([zug_r, 0, z_gp0]) cylinder(d = zug_d, h = z_br1 - z_gp0);
    // Ballast
    color([0.5, 0.5, 0.52]) for (b = ballast_pos) rotate([0, 0, b[1]]) translate([b[0], 0, z_gp1]) cylinder(d = ballast_d, h = ballast_n * ballast_s);
    // Wägezelle, Becher
    color([0.75, 0.75, 0.78]) box(zelle_x - zelle_b / 2, zelle_x + zelle_b / 2, zelle_y0, zelle_y1, z_zelle0, z_zelle1);
    color([0.93, 0.93, 0.93, 0.55]) translate([zelle_x, 0, z_becher0]) cylinder(d1 = becher_du, d2 = becher_do, h = becher_h);
}

// ============================================================================
// 12 Montage
// ============================================================================
module montage() {
    difference() {
        union() {
            color("#0A0A0C") t_sockel();
            color("#141417") t_koerper_unten();
            color("#141417") t_koerper_oben();
            color("#0A0A0C") t_krone();
            color("#C9A44C") t_goldband();
            color("#C9A44C") t_goldring();
            color("#C9A44C") t_kronenring();
            if (scheiben == 1) {
                color("#C9A44C") rahmen_haut(rb_in, rb_out, portal_z0 - rahmen_bb, rahmen_naht_unten);
                color("#C9A44C") rahmen_haut(fw_in, fw_out, rahmen_z_seite0, rahmen_z_oben1);
                color("#C9A44C") t_lippe();
                color([0.18, 0.18, 0.2, 0.55]) { t_portalscheibe(0); t_portalscheibe(1); }
                color([0.93, 0.95, 0.96, 0.4]) for (p = fenster_winkel) rotate([0, 0, p * teilung]) fensterscheibe_montage();
            }
            color("#1C1C1E") t_grundplatte();
            color("#1C1C1E") t_lagerbock();
            if (budget == 0) {
                color("#1C1C1E") t_rinne();
                color("#1C1C1E") for (sd = [-1, 1]) t_rinnendeckel(sd);
                color("#1C1C1E") for (a = saeule_winkel) rotate([0, 0, a]) translate([st_r, 0, 0]) t_saeule();
                color("#1C1C1E") for (vz = [-1, 1]) t_abstreifhalter(vz);
                color("#DAD6CC") for (vz = [-1, 1]) rotate([0, 0, vz * lippe_winkel]) translate([lippe_r0, -lippe_t / 2, 58]) cube([lippe_r1 - lippe_r0, lippe_t, lippe_z1 - 58]);
            }
            color("#1C1C1E") t_laufring();
            color("#1C1C1E") rotate([0, 0, phi]) t_karussell();
            color("#1C1C1E") rotate([0, 0, phi]) for (j = [0:6]) rotate([0, 0, (j + 0.5) * teilung]) t_rollenbock();
            color("#1C1C1E") t_schlitten();
            color("#1C1C1E") t_ausleger();
            color("#1C1C1E") t_bruecke();
            color("#1C1C1E") t_gt2_rad();
            color("#F4F2EE") t_schublade();
            color("#0A0A0C") t_front();
            color("#1C1C1E") t_podest();
            color("#1C1C1E") t_waegebock();
            color("#1C1C1E") t_anschlag();
            color("#1C1C1E") t_motor2_winkel();
            color("#1C1C1E") t_hallhalter();
            color("#1C1C1E") t_platinenhalter();
            if (budget == 0) color("#1C1C1E") rotate([0, 0, -2.5 * teilung]) for (z = [20, 100, 160, 250, 320, 370]) translate([0, 0, z]) t_kabelclip();
            color("#141417") t_klebering();
            color("#C9A44C") translate([0, 0, z_hoehe - 1.2]) rotate([0, 0, 90]) t_namensschild();
            color("#1C1C1E") for (a = zug_winkel) rotate([0, 0, a]) t_fugenhalter();
            color("#1C1C1E") for (s = [-1, 1]) t_schiene(s);
            if (scheiben == 1) color("#C9A44C") translate([-(sock_r(buchse_z) + 3), 0, buchse_z]) rotate([0, 90, 0]) t_buchsenring();
            if (kaufteile_zeigen == 1) kaufteile();
        }
        if (schnitt == 1) translate([-300, 0, -10]) cube([600, 300, 600]);
    }
}

// ============================================================================
// 13 Auswahl
// ============================================================================
if (teil == "montage") montage();
else druck(teil);
