// ============================================================
// Farbmischer-Revolver, parametrisch, OpenSCAD (Stand 2 des Parameterblatts)
// Ein Schrittmotor, fünf Spritzen in einem drehbaren Karussell.
// Alle Maße in mm. Z nach oben, Z = 0 Tischplatte.
// Winkel 0 Grad zeigt nach vorne (+X), positive Winkel gegen den Uhrzeigersinn.
// Stationen bei 0, 72, 144, 216, 288 Grad auf Radius 50.
// Stößel lokal: X radial nach außen, Y tangential. Spindel bei Y +20, Welle bei Y -20.
//
// Lösung für das Drehen: Das Karussell (Ø 160) liegt innen auf einem 45-Grad-Kegelring
// der Mittelschale (stützenfrei druckbar). Es ragt nicht heraus. Durch den Schlitz
// 60 x 20 bei -60 Grad ist der geränderte Rand mit dem Daumen drehbar.
// Mittelschale (Z 120 bis 300) und Oberschale (Z 300 bis 418) sind Steckteile.
// ============================================================

// ---------- Steuerung ----------
teil = "alle";   // "fuss", "sockelschale", "fensterrahmen", "abtropfschale", "schale_mitte",
                 // "karussell", "schale_oben", "bruecke", "schlitten", "stoesselfuss",
                 // "sperrklinke", "kappe", "montage", "alle"
$fn = 64;        // Rundungsqualität

// ---------- Allgemein ----------
spiel = 0.3;           // Spiel für Steckverbindungen
m3_d = 3.4;            // M3 Durchgangsloch
m3_kopf_d = 6.4;       // Senkung M3 Zylinderkopf
m3_kopf_t = 2.6;       // Tiefe der Senkung
m3_pilot = 2.7;        // Kernloch selbstschneidende M3 in PETG
m2_pilot = 1.7;        // Kernloch selbstschneidende M2 in PETG
stationen = 5;         // Anzahl Stationen
st_r = 50;             // Stationsradius
schale_d = 170;        // Außendurchmesser aller Schalen
wand = 2.4;            // Wandstärke der Schalen
feder_b = 1.2;         // Nut und Feder: Feder Breite
feder_h = 2;           // Feder Höhe
nut_spiel = 0.4;       // Nut Spiel (Breite und Tiefe)

// ---------- Fuß ----------
fuss_d = 185;          // Fuß Durchmesser
fuss_h = 25;           // Fuß Höhe
fach_b = 80;           // Elektronikfach Breite
fach_t = 80;           // Elektronikfach Tiefe
fach_h = 20;           // Elektronikfach Höhe
fach_x = -20;          // Fach nach hinten versetzt (X-Mitte)
fach_fase = 6;         // 45-Grad-Fase der Fachdecke (stützenfrei)
buchse_d = 11;         // Bohrung Buchse 12 V hinten
kabel_d = 12;          // Kabelloch vom Fach nach oben
kabel_x = -50;         // Lage Kabelloch (X)

// ---------- Sockelschale ----------
sk_z0 = 25;            // Unterkante
sk_z1 = 120;           // Oberkante
boden_z = 30;          // Boden Becherraum (Oberkante)
becher_d = 64;         // Becherraum Durchmesser (Mitte Radius 50, 0 Grad)
becher_h = 60;         // Mischbecher Höhe (Kaufteil Ø 60)
duese_z = 105;         // Düsenspitzen
fenster_b = 70;        // Fenster Breite
fenster_h = 80;        // Fenster Höhe, oben halbrund
fenster_z0 = 28;       // Fenster Unterkante
rahmen_b = 5;          // Rahmenbreite seitlich und oben
rahmen_unten = 3;      // Rahmenbreite unten (sitzt auf dem Fuß)
rahmen_t = 4;          // Rahmen Dicke (radial außen)

// ---------- Abtropfschale ----------
trop_z0 = 96;          // Unterkante
trop_t = 4;            // Tiefe (Randhöhe)
trop_boden = 1.2;      // Bodenstärke
trop_rand = 1.6;       // Randstärke
trop_ra = 80;          // Außenradius
trop_ri = 25;          // Innenradius
trop_frei_d = 44;      // Aussparung unter der aktiven Station
auf_b = 6;             // Breite der 45-Grad-Auflage in der Sockelschale

// ---------- Mittelschale ----------
sm_z0 = 120;           // Unterkante
sm_z1 = 300;           // Oberkante
lr_z0 = 238;           // Laufring: Unterkante der senkrechten Innenfläche
lr_z1 = 245;           // Laufring: Oberkante (Gleitfläche)
lr_ri = 65;            // Laufring Innenradius (Innen-Ø 130)
zunge_winkel = 36;     // Lage der Federzunge (Kerben liegen bei 36 + n * 72)
zunge_t = 1.2;         // Federzunge Dicke
zunge_l = 20;          // Federzunge Länge (tangential)
zunge_r0 = 67;         // Zungenhohlraum Innenradius
zunge_r1 = 77;         // Zungenhohlraum Außenradius
zunge_bump_d = 5;      // Rastnase Durchmesser
zunge_bump_h = 1.2;    // Rastnase Höhe
fz_z0 = 240;           // Fensterschlitz Unterkante
fz_h = 20;             // Fensterschlitz Höhe
fz_b = 60;             // Fensterschlitz Breite
fz_winkel = -60;       // Fensterschlitz Winkel
fz_r0 = 80;            // Fensterschlitz beginnt bei diesem Radius (Rand des Karussells)
hall_r1 = 76;          // Hall-Sensor Radius (Stationsmagnet), bei 0 Grad
hall_r2 = 69;          // Hall-Sensor Radius (Referenzmagnet), bei 0 Grad (Blatt 68, 1 mm weiter außen: Tasche ragt sonst 0,1 in den Durchlass)
hall_b = 4;            // Sensor tangential
hall_t = 3;            // Sensor radial
hall_h = 1.5;          // Sensor Dicke
hall_tief = 2;         // Taschentiefe (0,5 Luft nach unten)
hall_bein = 6;         // Länge Beinschlitz (nach -Y)

// ---------- Oberschale ----------
so_z0 = 300;           // Unterkante
ao_b = 5;              // Breite der 45-Grad-Auflage der Brücke

// ---------- Karussell ----------
ka_d = 160;            // Durchmesser
ka_z0 = 245;           // Unterkante
ka_t = 14;             // Dicke
ka_tasche_t = 45.6;    // Flanschtasche tangential (lange Seite)
ka_tasche_r = 32.6;    // Flanschtasche radial
ka_tasche_h = 3.6;     // Flanschtasche Tiefe
ka_durchlass = 31;     // Zylinderdurchlass
ka_mittel = 40;        // Mittelloch
raendel_n = 60;        // Anzahl Rillen
raendel_b = 1;         // Rille Breite
raendel_t = 1;         // Rille Tiefe
mag_d = 5.2;           // Magnettasche Durchmesser
mag_h = 2.2;           // Magnettasche Tiefe
mag_r1 = 76;           // Magnete je Station
mag_r2 = 69;           // Referenzmagnet bei Station 1 (Blatt 68, siehe hall_r2)
relief_h = 1;          // Freistellung innerhalb und außerhalb des Laufstegs
lauf_ri = 65;          // Laufsteg Innenradius (Innen-Ø 130)
lauf_ra = 79;          // Laufsteg Außenradius (Außen-Ø 158)
kerbe_r = 72;          // Rastkerben Radius
kerbe_d = 6;           // Rastkerbe Durchmesser oben
kerbe_t = 1.5;         // Rastkerbe Tiefe

// ---------- Spritze 60 ml ----------
syr_zyl_d = 30;        // Zylinder
syr_flansch_l = 45;    // Flansch lang (tangential)
syr_flansch_q = 32;    // Flansch quer (radial)
kolben_d = 30;         // Kolbenplatte
kolben_t = 4;          // Kolbenplatte Dicke

// ---------- NEMA 17, Spindel, Welle, Lager ----------
tang = 20;             // Spindel (+) und Welle (-) tangential neben der Spritzenachse
nema_flansch = 42.3;   // Flanschmaß
nema_loch = 31;        // Lochabstand
nema_l = 40;           // Baulänge
nema_welle_l = 24;     // Wellenlänge über dem Flansch
mutter_flansch_d = 22; // T8 Flanschmutter, Flansch
mutter_flansch_t = 3.5;// Flanschdicke
mutter_loch_kreis = 16;// Lochkreis 4 x M3
mutter_laenge = 15;    // Mutterkörper Länge
welle_pass = 7.8;      // Sackloch für 8-mm-Welle
welle_sack = 6;        // Tiefe Wellensackloch in der Brücke
lm_d = 15;             // LM8UU außen
lm_l = 24;             // LM8UU Länge
lm_spiel = 0.2;        // Zugabe Lagersitz
sl_wand = 2;           // Wand um den Lagersitz
kupp_l = 25;           // Kupplung 5 auf 8 Länge
kupp_d = 19;           // Kupplung Durchmesser
lager_sitz_d = 22.2;   // Sitz Lager 608
lager_t = 7;           // Tiefe Sitz 608
fuehrung_z0 = 262;     // Unterende von Spindel und Welle

// ---------- Schalter ----------
ms_l = 12.8;           // Mikroschalter im Stößelfuß
ms_b = 6.5;
ms_h = 5.8;
knopf_d = 8;           // federnder Tasterknopf
es_l = 20;             // Endschalter an der Brückenunterseite
es_b = 10;
es_t = 6.5;
es_loch = 9.5;         // Lochabstand (in X)
es_x = 8;              // Lage Endschalter und Schaltnase (lokal X)
es_y = -8;             // Lage Endschalter und Schaltnase (lokal Y)
nase_b = 5;            // Schaltnase Querschnitt

// ---------- Stößel ----------
z_oben = 346;          // Stempelunterkante oben
z_unten = 254;         // Stempelunterkante unten
stempel_d = 26;        // Stößelfuß als Stempel
stempel_h = 15;        // Stempelhöhe
blk_h = 30;            // Schlittenblock Höhe
blk_x = 15;            // Block halbe Breite radial
blk_b = 56;            // Block Breite tangential (höchstens 56)
fahne_x1 = 28;         // Fahne für die Sperrklinke bis X
fahne_y0 = 4;          // Fahne Y von
fahne_y1 = 20;         // Fahne Y bis
klinke_x = 22;         // Sperrklinke Lage (lokal X)
klinke_y = 12;         // Sperrklinke Lage (lokal Y)
klinke_d = 7;          // Sperrklinke Durchmesser
klinke_tief = 22;      // Einstecktiefe der Klinke in die Fahne
stempel_schr = 9;      // Stempelschrauben bei X +-9

// ---------- Brücke, Haube ----------
br_z0 = 418;           // Brücke Unterkante (= Oberkante Oberschale)
br_t = 8;              // Brücke Dicke
br_d = 165;            // Brücke Durchmesser
aus_t = 48;            // Aussparung tangential
aus_r = 36;            // Aussparung radial
aus_ecke = 6;          // Eckenradius
aus_winkel = [144, 216, 288];  // über 72 Grad sitzt der Motor, über 0 Grad der Stößel
aus_min = 2;           // Mindestwand Aussparung zu Bohrungen
motor_rand_min = 0.2;  // Mindestabstand Motorecke zum Brückenrand
haube_z1 = 480;        // Oberkante Haube
led_d = 50;            // LED-Ring
led_t = 5;             // Tiefe LED-Aufnahme

// ============================================================
// Abgeleitete Maße (nicht ändern)
// ============================================================
R_aus = schale_d / 2;
R_in = R_aus - wand;                       // 82,6
st_w = 360 / stationen;
sehne = 2 * st_r * sin(st_w / 2);          // Abstand benachbarter Stationen
feder_r = R_aus - wand / 2;
hub = z_oben - z_unten;
blk_z0_oben = z_oben + stempel_h;          // Blockunterkante oben (361)
blk_z1_oben = blk_z0_oben + blk_h;         // Blockoberkante oben (391)
kupp_z0 = br_z0 - kupp_l;                  // 393
br_z1 = br_z0 + br_t;
motor_z1 = br_z1 + nema_l;
ka_z1 = ka_z0 + ka_t;
sp_z1 = br_z1 - nema_welle_l - 2;          // Spindel oben, 2 Luft zur Motorwelle
sp_l = sp_z1 - fuehrung_z0;
w_z1 = br_z0 + welle_sack;
w_l = w_z1 - fuehrung_z0;
kupp_ein = sp_z1 - kupp_z0;                // Spindel in der Kupplung
nase_z = br_z0 - es_t - blk_z0_oben;       // Nasenspitze lokal (über Blockunterkante)
klinke_laenge = blk_z0_oben - (ka_z1 + 1); // Klinke unter dem Block
boss_d = lm_d + lm_spiel + 2 * sl_wand;    // Säule um das LM8UU
sperr_d = klinke_d + 1.6;                  // Sperrnut in Karussell und Laufring
fz_rahmen_z0 = fenster_z0 - rahmen_unten;
fz_rahmen_h = fenster_h + rahmen_unten + rahmen_b;

// ---------- Funktionen ----------
function rot(a, p) = [p[0] * cos(a) - p[1] * sin(a), p[0] * sin(a) + p[1] * cos(a)];
function flansch_eck(i, l, q) = [for (s = [[1, 1], [1, -1], [-1, -1], [-1, 1]])
    rot(i * st_w, [st_r + s[0] * q / 2, s[1] * l / 2])];
function psd(p, a, b) = let(d = b - a, t = max(0, min(1, ((p - a) * d) / (d * d)))) norm(p - (a + t * d));
function pds(p, poly) = min([for (i = [0 : 3]) psd(p, poly[i], poly[(i + 1) % 4])]);
function innen(p, poly) = let(c = [for (i = [0 : 3]) cross(poly[(i + 1) % 4] - poly[i], p - poly[i])]) (min(c) >= 0 || max(c) <= 0);
function polyd(p1, p2) = min(min([for (p = p1) pds(p, p2) * (innen(p, p2) ? -1 : 1)]),
                             min([for (p = p2) pds(p, p1) * (innen(p, p1) ? -1 : 1)]));
function rp(p, c, h) = norm([max(abs(p[0] - c[0]) - h[0], 0), max(abs(p[1] - c[1]) - h[1], 0)]);
function aus_abst(a, b) = let(q = rot(-a, [b[0] - st_r * cos(a), b[1] - st_r * sin(a)]))
    rp(q, [0, 0], [aus_r / 2, aus_t / 2]) - b[2];

// Bohrungen in der Brücke: [x, y, Radius]
bohr = concat(
    [[st_r, tang, lager_sitz_d / 2], [st_r, -tang, welle_pass / 2]],
    [for (a = [-1, 1], b = [-1, 1]) [st_r + a * nema_loch / 2, tang + b * nema_loch / 2, m3_kopf_d / 2]],
    [for (a = [-1, 1]) [st_r + es_x + a * es_loch / 2, es_y, m2_pilot / 2]]);

fl_luft = polyd(flansch_eck(0, syr_flansch_l, syr_flansch_q), flansch_eck(1, syr_flansch_l, syr_flansch_q));
ta_luft = polyd(flansch_eck(0, ka_tasche_t, ka_tasche_r), flansch_eck(1, ka_tasche_t, ka_tasche_r));
aus_ist = min([for (a = aus_winkel, b = bohr) aus_abst(a, b)]);
motor_eck_r = norm([st_r + nema_flansch / 2, tang + nema_flansch / 2]);
fuss_luft = sehne - stempel_d / 2 - syr_zyl_d / 2;
blk_c = [st_r, (blk_b / 2 - (tang + boss_d / 2)) / 2];       // Mitte des Blocks inkl. Säule
blk_h2 = [blk_x, (blk_b / 2 + tang + boss_d / 2) / 2];
blk_luft = min(rp([st_r * cos(st_w), st_r * sin(st_w)], blk_c, blk_h2),
               rp([st_r * cos(st_w), -st_r * sin(st_w)], blk_c, blk_h2)) - kolben_d / 2;
fahne_r = norm([st_r + fahne_x1, fahne_y1]);
hoehen = [fuss_h + feder_h, sk_z1 - sk_z0 + feder_h, sm_z1 - sm_z0 + feder_h, br_z0 - so_z0 + feder_h,
          ka_t, br_t, trop_t, haube_z1 - br_z0, fz_rahmen_h, nase_z + 0, stempel_h, klinke_laenge + klinke_tief];
durchm = [fuss_d, schale_d, ka_d, br_d, 2 * trop_ra, 2 * R_aus + 2 * rahmen_t];

// ---------- Prüfungen ----------
assert(max(hoehen) <= 200, "Ein Teil ist höher als 200 mm");
assert(max(durchm) <= 220, "Ein Teil ist breiter als 220 mm");
assert(sehne - syr_flansch_l > 2, "Sehne minus Flansch 45 nicht größer 2");
assert(fl_luft > 2, "gedrehte Flansche 45 x 32 haben weniger als 2 mm Luft");
assert(st_r + becher_d / 2 <= R_in, "Becher Ø 64 liegt nicht innerhalb des Innenradius");
assert(motor_eck_r <= br_d / 2 - motor_rand_min, "Motor ragt über die Brücke hinaus");
assert(aus_ist >= aus_min, "Brückenaussparung zu nah an Motor-, Lager- oder Schalterbohrung");
assert(fuss_luft >= 2, "Stößelfuß Ø 26 näher als 2 mm an den Nachbarzylindern");
assert(blk_b <= 56, "Schlittenblock breiter als 56");
assert(blk_luft >= 2, "Schlittenblock näher als 2 mm an den Nachbarkolben");
assert(fuehrung_z0 >= ka_z1 + 2, "Führungsunterkante nicht 2 über der Karussell-Oberkante");
assert(blk_z1_oben + 2 <= kupp_z0, "Kupplung kollidiert mit dem Schlitten in oberster Stellung");
assert(ka_d / 2 <= R_in - 0.3, "Karussell zu groß für die Mittelschale");
assert(br_d / 2 < R_in, "Brücke passt nicht in die Oberschale");
assert(fahne_r <= R_in - 1.5, "Fahne der Sperrklinke zu nah an der Schale");
assert(st_r + klinke_x + sperr_d / 2 + 2 <= ka_d / 2, "Sperrnut zu nah am Karussell-Rand");
assert(stempel_d / 2 + welle_pass / 2 + 0.5 <= tang, "Stempel stößt an Spindel oder Welle");
assert(kupp_ein >= 5, "Spindel steckt zu kurz in der Kupplung");
assert(sp_z1 < br_z1 - nema_welle_l, "Spindel stößt an die Motorwelle");

echo(str("Gesamthöhe ", haube_z1, " mm, Durchmesser Schale ", schale_d, ", Fuß ", fuss_d, ", größtes Teil ", max(durchm)));
echo(str("Spindel T8 ", sp_l, " mm (Z ", fuehrung_z0, " bis ", sp_z1, "), Welle 8 mm ", w_l, " mm (Z ", fuehrung_z0, " bis ", w_z1, ")"));
echo(str("Hub ", hub, " mm, Stempelunterkante Z ", z_unten, " bis ", z_oben, ", Block oben Z ", blk_z0_oben, " bis ", blk_z1_oben));
echo(str("Luft gedrehte Flansche 45 x 32: ", fl_luft, " mm, Taschen 45,6 x 32,6: ", ta_luft, " mm, Sehne ", sehne));
echo(str("Luft Stößelfuß zu Nachbarzylindern ", fuss_luft, " mm, Block zu Nachbarkolben ", blk_luft, " mm"));
echo(str("Brückenaussparungen: kleinste Wand zu Bohrungen ", aus_ist, " mm, Motorecke bei r ", motor_eck_r, " von ", br_d / 2));
echo(str("Kupplung Z ", kupp_z0, " bis ", br_z0, ", Luft zum Schlitten oben ", kupp_z0 - blk_z1_oben, " mm, Spindel in Kupplung ", kupp_ein, " mm"));
echo(str("Sperrklinke ", klinke_laenge, " mm unter dem Block, Länge Stift ", klinke_laenge + klinke_tief, " mm"));

// ============================================================
// Hilfsmodule
// ============================================================

// Rohr von Radius ri bis ra, Höhe h
module ring(ra, ri, h) {
    difference() {
        cylinder(r = ra, h = h, $fn = 160);
        translate([0, 0, -0.1]) cylinder(r = ri, h = h + 0.2, $fn = 160);
    }
}

// Feder (oben auf einer Schale) und Nut (unten in der nächsten Schale)
module feder_ring(z0) {
    translate([0, 0, z0 - 0.01]) ring(feder_r + feder_b / 2, feder_r - feder_b / 2, feder_h + 0.01);
}
module nut_ring(z0) {
    translate([0, 0, z0 - 0.1])
        ring(feder_r + (feder_b + nut_spiel) / 2, feder_r - (feder_b + nut_spiel) / 2, feder_h + 0.3);
}

// 45-Grad-Auflage an der Innenwand: oben eben von r_in bis r_out, Unterseite schräg
module auflage(r_out, r_in, z0, h) {
    rotate_extrude($fn = 160) polygon([[r_in, z0 + h], [r_out + 0.01, z0 + h], [r_out + 0.01, z0]]);
}

// Fensterprofil (Y tangential, Z hoch), unten gerade, oben halbrund
module fenster_profil(b, z0, h) {
    hull() {
        translate([-b / 2, z0]) square([b, 0.01]);
        translate([0, z0 + h - b / 2]) circle(d = b);
    }
}
// Profil radial ausgezogen ab Radius r0, Länge l (Winkel 0 Grad)
module fenster_prisma(b, z0, h, r0, l) {
    translate([r0, 0, 0]) rotate([90, 0, 90]) linear_extrude(height = l) fenster_profil(b, z0, h);
}

// Fensterschlitz der Mittelschale (Ellipse 60 x 20, oben flach gewölbt)
module fz_loch() {
    rotate([0, 0, fz_winkel]) translate([fz_r0, 0, fz_z0 + fz_h / 2]) rotate([0, 90, 0])
        linear_extrude(height = 12) scale([fz_h / 2, fz_b / 2]) circle(r = 1);
}

// ============================================================
// 1. Fuß (Z 0 bis 25), Feder oben
// Druck: wie modelliert, Fachöffnung unten, Fachdecke mit 45-Grad-Fase
// ============================================================
module fuss() {
    difference() {
        union() {
            cylinder(d = fuss_d, h = fuss_h, $fn = 160);
            feder_ring(fuss_h);
        }
        // Elektronikfach von unten mit Fase
        hull() {
            translate([fach_x - fach_b / 2, -fach_t / 2, -0.1]) cube([fach_b, fach_t, fach_h - fach_fase + 0.1]);
            translate([fach_x - fach_b / 2 + fach_fase, -fach_t / 2 + fach_fase, -0.1])
                cube([fach_b - 2 * fach_fase, fach_t - 2 * fach_fase, fach_h + 0.1]);
        }
        // Buchse 12 V hinten, vom Rand bis ins Fach
        translate([-fuss_d / 2 - 1, 0, 11]) rotate([0, 90, 0])
            cylinder(d = buchse_d, h = fuss_d / 2 + 2 + fach_x - fach_b / 2);
        // Kabelloch nach oben
        translate([kabel_x, 0, fach_h - 1]) cylinder(d = kabel_d, h = fuss_h - fach_h + 2);
    }
}

// ============================================================
// 2. Sockelschale (Z 25 bis 120): Becherraum, Fenster vorne, Auflage Abtropfschale
// Druck: stehend, Nut unten, Feder oben, Fenster oben halbrund
// ============================================================
module sockelschale() {
    difference() {
        union() {
            translate([0, 0, sk_z0]) ring(R_aus, R_in, sk_z1 - sk_z0);
            translate([0, 0, sk_z0]) cylinder(r = R_in + 0.01, h = boden_z - sk_z0, $fn = 160);
            feder_ring(sk_z1);
            auflage(R_in, R_in - auf_b, trop_z0 - auf_b, auf_b);
        }
        nut_ring(sk_z0);
        translate([kabel_x, 0, sk_z0 - 1]) cylinder(d = kabel_d, h = boden_z - sk_z0 + 2);
        // Fenster durch die Wand
        fenster_prisma(fenster_b, fenster_z0, fenster_h, R_in - 0.5, 15);
        // Auflage im Fensterbereich freischneiden (Becher geht nach vorne heraus)
        intersection() {
            fenster_prisma(fenster_b, fenster_z0, fenster_h, 70, 15);
            translate([60, -60, trop_z0 - auf_b - 1]) cube([40, 120, 40]);
        }
    }
}

// ============================================================
// 3. Fensterrahmen (eigenes Teil, außen auf die Sockelschale geklebt)
// Druck: stehend, Fuß des Rahmens unten
// ============================================================
module fensterrahmen() {
    difference() {
        intersection() {
            translate([0, 0, fz_rahmen_z0]) ring(R_aus + rahmen_t, R_aus, fz_rahmen_h);
            fenster_prisma(fenster_b + 2 * rahmen_b, fz_rahmen_z0, fz_rahmen_h, R_aus - 5, 20);
        }
        fenster_prisma(fenster_b, fenster_z0, fenster_h, R_aus - 6, 20);
    }
}

// ============================================================
// 4. Abtropfschale (Ring 4 tief, herausnehmbar, liegt auf der Auflage)
// Druck: flach
// ============================================================
module abtropfschale() {
    translate([0, 0, trop_z0]) union() {
        difference() {
            ring(trop_ra, trop_ri, trop_boden);
            translate([st_r, 0, -1]) cylinder(d = trop_frei_d, h = trop_boden + 2);
        }
        ring(trop_ra, trop_ra - trop_rand, trop_t);
        ring(trop_ri + trop_rand, trop_ri, trop_t);
        difference() {
            translate([st_r, 0, 0]) cylinder(d = trop_frei_d + 2 * trop_rand, h = trop_t);
            translate([st_r, 0, -1]) cylinder(d = trop_frei_d, h = trop_t + 2);
        }
    }
}

// ============================================================
// 5. Mittelschale (Z 120 bis 300): Fensterschlitz, Kegel-Laufring, Federzunge, Hall-Taschen
// Der Laufring ist ein 45-Grad-Kegel an der Wand (stützenfrei), keine Stege nötig.
// Druck: stehend, Nut unten, Feder oben
// ============================================================
module schale_mitte() {
    difference() {
        union() {
            translate([0, 0, sm_z0]) ring(R_aus, R_in, sm_z1 - sm_z0);
            feder_ring(sm_z1);
            // Laufring: senkrechte Innenfläche Z 238 bis 245, darunter 45 Grad zur Wand
            rotate_extrude($fn = 160)
                polygon([[lr_ri, lr_z1], [R_in + 0.01, lr_z1], [R_in + 0.01, lr_z0 - (R_in - lr_ri)], [lr_ri, lr_z0]]);
            // Rastnase der Federzunge
            rotate([0, 0, zunge_winkel]) translate([kerbe_r, 0, lr_z1 - 0.01])
                cylinder(d1 = zunge_bump_d, d2 = zunge_bump_d - 2, h = zunge_bump_h + 0.01);
        }
        nut_ring(sm_z0);
        fz_loch();
        // Federzunge freischneiden: Hohlraum unter einer Haut von 1,2, Schlitz an einem Ende
        rotate([0, 0, zunge_winkel]) {
            translate([zunge_r0, -zunge_l / 2, lr_z0 - 20])
                cube([zunge_r1 - zunge_r0, zunge_l, (lr_z1 - zunge_t) - (lr_z0 - 20)]);
            translate([zunge_r0, -zunge_l / 2, lr_z0 - 20])
                cube([zunge_r1 - zunge_r0, 1, lr_z1 - lr_z0 + 21]);
        }
        // Durchlass für die Sperrklinke (Station vorne)
        translate([st_r + klinke_x, klinke_y, lr_z0 - 30]) cylinder(d = sperr_d, h = lr_z1 - lr_z0 + 31);
        // Hall-Sensor-Taschen bei 0 Grad, Beine nach -Y
        for (r = [hall_r1, hall_r2])
            translate([r, 0, lr_z1 - hall_tief]) {
                translate([-hall_t / 2, -hall_b / 2, 0]) cube([hall_t, hall_b, hall_tief + 0.1]);
                translate([-hall_t / 2, -hall_b / 2 - hall_bein, hall_tief - hall_h + 0.6])
                    cube([hall_t, hall_bein + 0.1, hall_h]);
            }
    }
}

// ============================================================
// 6. Karussell (Z 245 bis 259), Ø 160
// Druck: Unterseite auf dem Bett (Laufsteg unten), Taschen oben offen
// ============================================================
module karussell() {
    difference() {
        translate([0, 0, ka_z0]) cylinder(d = ka_d, h = ka_t, $fn = 200);
        translate([0, 0, ka_z0 - 1]) cylinder(d = ka_mittel, h = ka_t + 2);
        // Laufsteg Ø 130 bis Ø 158: innen und außen 1 mm freigestellt
        translate([0, 0, ka_z0 - 0.01]) cylinder(r = lauf_ri, h = relief_h + 0.01, $fn = 160);
        translate([0, 0, ka_z0 - 0.01]) ring(ka_d / 2 + 1, lauf_ra, relief_h + 0.01);
        for (i = [0 : stationen - 1]) rotate([0, 0, i * st_w]) {
            translate([st_r, 0, 0]) {
                // Zylinderdurchlass und Flanschtasche (lange Seite tangential)
                translate([0, 0, ka_z0 - 1]) cylinder(d = ka_durchlass, h = ka_t + 2);
                translate([-ka_tasche_r / 2, -ka_tasche_t / 2, ka_z1 - ka_tasche_h])
                    cube([ka_tasche_r, ka_tasche_t, ka_tasche_h + 1]);
            }
            // Sperrnut für die Klinke (durchgehend)
            translate([st_r + klinke_x, klinke_y, ka_z0 - 1]) cylinder(d = sperr_d, h = ka_t + 2);
            // Magnettasche von unten
            translate([mag_r1, 0, ka_z0 - 0.01]) cylinder(d = mag_d, h = mag_h + 0.01);
            // Rastkerbe zwischen den Stationen
            rotate([0, 0, st_w / 2]) translate([kerbe_r, 0, ka_z0 - 0.01])
                cylinder(d1 = kerbe_d, d2 = 1.5, h = kerbe_t + 0.01);
        }
        // Referenzmagnet bei Station 1
        translate([mag_r2, 0, ka_z0 - 0.01]) cylinder(d = mag_d, h = mag_h + 0.01);
        // Rändel
        for (k = [0 : raendel_n - 1]) rotate([0, 0, k * 360 / raendel_n])
            translate([ka_d / 2 - raendel_t, -raendel_b / 2, ka_z0 - 1]) cube([raendel_t + 1, raendel_b, ka_t + 2]);
    }
}

// ============================================================
// 7. Oberschale (Z 300 bis 418), Auflage für die Brücke
// Druck: stehend, Nut unten, Feder oben
// ============================================================
module schale_oben() {
    difference() {
        union() {
            translate([0, 0, so_z0]) ring(R_aus, R_in, br_z0 - so_z0);
            feder_ring(br_z0);
            auflage(R_in, R_in - ao_b, br_z0 - ao_b, ao_b);
        }
        nut_ring(so_z0);
    }
}

// ============================================================
// 8. Brücke (Z 418 bis 426), Ø 165
// Aussparungen 48 x 36, Ecken R 6, über 144, 216, 288 Grad. Motoraufnahme über der
// Spindel (Y +20), Sitz Lager 608 und Schalter unten, Wellensackloch bei Y -20.
// Druck: flach, Unterseite auf dem Bett
// ============================================================
module bruecke() {
    difference() {
        translate([0, 0, br_z0]) cylinder(d = br_d, h = br_t, $fn = 200);
        for (a = aus_winkel) rotate([0, 0, a]) translate([st_r, 0, br_z0 - 1])
            linear_extrude(height = br_t + 2)
                offset(r = aus_ecke) square([aus_r - 2 * aus_ecke, aus_t - 2 * aus_ecke], center = true);
        // NEMA 17: Wellendurchgang, Lochbild mit Kopfsenkung von unten, Lagersitz 608 von unten
        translate([st_r, tang, br_z0 - 1]) {
            cylinder(d = 10, h = br_t + 2);
            for (a = [-1, 1], b = [-1, 1]) translate([a * nema_loch / 2, b * nema_loch / 2, 0]) {
                cylinder(d = m3_d, h = br_t + 2);
                cylinder(d = m3_kopf_d, h = 1 + m3_kopf_t + 0.1);
            }
        }
        translate([st_r, tang, br_z0 - 0.1]) cylinder(d = lager_sitz_d, h = lager_t + 0.1);
        // Wellensackloch
        translate([st_r, -tang, br_z0 - 0.1]) cylinder(d = welle_pass, h = welle_sack + 0.1);
        // Endschalter an der Unterseite (Kernlöcher M2)
        for (s = [-1, 1]) translate([st_r + es_x + s * es_loch / 2, es_y, br_z0 - 0.1])
            cylinder(d = m2_pilot, h = 5);
    }
}

// ============================================================
// 9. Schlitten (lokal: Spritzenachse, X radial, Y tangential, Z 0 = Blockunterkante)
// Block 30 hoch. LM8UU auf der Welle (Y -20), Flanschmutter auf der Spindel (Y +20),
// Mutterflansch bündig in der Unterseite versenkt, Schaltnase oben, Fahne für die Klinke.
// Der Stößelfuß (Stempel) hängt mittig darunter (2 x M3x40 von oben).
// Druck: Blockunterseite auf dem Bett, keine Stützen
// ============================================================
module schlitten() {
    difference() {
        union() {
            translate([-blk_x, -blk_b / 2, 0]) cube([2 * blk_x, blk_b, blk_h]);
            translate([0, -tang, 0]) cylinder(d = boss_d, h = blk_h);
            translate([blk_x - 2, fahne_y0, 0]) cube([fahne_x1 - blk_x + 2, fahne_y1 - fahne_y0, blk_h]);
            // Schaltnase
            translate([es_x - nase_b / 2, es_y - nase_b / 2, blk_h - 0.01]) cube([nase_b, nase_b, nase_z - blk_h + 0.01]);
        }
        // LM8UU von unten, oben eine Lippe
        translate([0, -tang, -0.1]) cylinder(d = lm_d + lm_spiel, h = lm_l + 0.6);
        translate([0, -tang, -0.1]) cylinder(d = 12, h = blk_h + 0.2);
        // Spindeldurchgang, Flansch von unten versenkt, vier M3-Kernlöcher
        translate([0, tang, -0.1]) cylinder(d = 10.6, h = blk_h + 0.2);
        translate([0, tang, -0.1]) cylinder(d = mutter_flansch_d + 0.4, h = mutter_flansch_t + 0.1);
        for (k = [0 : 3]) translate([mutter_loch_kreis / 2 * cos(45 + 90 * k), tang + mutter_loch_kreis / 2 * sin(45 + 90 * k), mutter_flansch_t - 0.1])
            cylinder(d = m3_pilot, h = 9.1);
        // Schrauben zum Stößelfuß, Kopf von oben versenkt
        for (s = [-1, 1]) translate([s * stempel_schr, 0, -0.1]) {
            cylinder(d = m3_d, h = blk_h + 0.2);
            translate([0, 0, blk_h + 0.1 - m3_kopf_t]) cylinder(d = m3_kopf_d, h = m3_kopf_t + 0.1);
        }
        // Sackloch für die Sperrklinke von unten
        translate([klinke_x, klinke_y, -0.1]) cylinder(d = klinke_d + 0.2, h = klinke_tief + 0.1);
    }
}

// ============================================================
// 10. Stößelfuß: Stempel Ø 26, 15 hoch (lokal Z 0 = Stempelunterkante)
// Mikroschalter 12,8 x 6,5 x 5,8 wird von der Seite (+Y) eingeschoben, darunter Bohrung
// für den federnden Tasterknopf Ø 8 (eigenes Teil, liegt daneben).
// Druck: Unterkante auf dem Bett
// ============================================================
module stoesselfuss() {
    ms_z0 = 5.2;
    difference() {
        cylinder(d = stempel_d, h = stempel_h);
        translate([-(ms_l + 0.4) / 2, -(ms_b + 0.4) / 2, ms_z0]) cube([ms_l + 0.4, stempel_d, ms_h + 0.2]);
        translate([0, 0, -0.1]) cylinder(d = knopf_d + 0.4, h = ms_z0 + 0.3);
        for (s = [-1, 1]) translate([s * stempel_schr, 0, stempel_h - 12]) cylinder(d = m3_pilot, h = 12.1);
        // Aussparungen für die Köpfe der Mutterschrauben
        for (s = [-1, 1]) translate([s * mutter_loch_kreis / 2 * cos(45), tang - mutter_loch_kreis / 2 * sin(45), stempel_h - 3])
            cylinder(d = 6.2, h = 3.1);
    }
}
module tasterknopf() {
    cylinder(d = knopf_d, h = 5.5);
    translate([0, 0, -1.5]) cylinder(d = knopf_d + 3, h = 1.5);
}

// ============================================================
// 11. Sperrklinke: Stift Ø 7, steckt in die Fahne, greift in Sperrnut und Laufring
// (lokal: Z 0 = Spitze)
// ============================================================
module sperrklinke() {
    cylinder(d = klinke_d, h = klinke_laenge + klinke_tief);
}

// ============================================================
// 12. Haube (Z 418 bis 480) über Brücke und Motor, abnehmbar, LED-Ring Ø 50 oben
// Druck: auf dem Kopf, Deckplatte auf dem Bett, Nut oben
// ============================================================
module kappe() {
    difference() {
        union() {
            translate([0, 0, br_z0]) ring(R_aus, R_in, haube_z1 - br_z0);
            translate([0, 0, motor_z1]) cylinder(r = R_aus, h = haube_z1 - motor_z1, $fn = 160);
        }
        nut_ring(br_z0);
        translate([0, 0, motor_z1 - 0.01]) cylinder(d = led_d + 0.4, h = led_t + 0.01);
    }
}

// ============================================================
// Druckpositionen (flach auf dem Bett, ohne Stützen)
// ============================================================
module druck_fuss()          { fuss(); }
module druck_sockelschale()  { translate([0, 0, -sk_z0]) sockelschale(); }
module druck_fensterrahmen() { translate([-(R_aus + rahmen_t / 2), 0, -fz_rahmen_z0]) fensterrahmen(); }
module druck_abtropfschale() { translate([0, 0, -trop_z0]) abtropfschale(); }
module druck_schale_mitte()  { translate([0, 0, -sm_z0]) schale_mitte(); }
module druck_karussell()     { translate([0, 0, -ka_z0]) karussell(); }
module druck_schale_oben()   { translate([0, 0, -so_z0]) schale_oben(); }
module druck_bruecke()       { translate([0, 0, -br_z0]) bruecke(); }
module druck_schlitten()     { schlitten(); }
module druck_stoesselfuss()  { stoesselfuss(); translate([stempel_d + 6, 0, 1.5]) tasterknopf(); }
module druck_sperrklinke()   { translate([0, 0, klinke_d / 2]) rotate([0, 90, 0]) sperrklinke(); }
module druck_kappe()         { rotate([180, 0, 0]) translate([0, 0, -haube_z1]) kappe(); }

// Übersicht aller Teile nebeneinander (nur zur Ansicht, Teile einzeln exportieren)
module alle_teile() {
    s = 200;
    druck_fuss();
    translate([s, 0, 0]) druck_sockelschale();
    translate([2 * s, 0, 0]) druck_schale_mitte();
    translate([3 * s, 0, 0]) druck_schale_oben();
    translate([4 * s, 0, 0]) druck_kappe();
    translate([0, s, 0]) druck_karussell();
    translate([s, s, 0]) druck_bruecke();
    translate([2 * s, s, 0]) druck_abtropfschale();
    translate([3 * s, s, 0]) druck_fensterrahmen();
    translate([0, 2 * s, 0]) druck_schlitten();
    translate([s, 2 * s, 0]) druck_stoesselfuss();
    translate([2 * s, 2 * s, 0]) druck_sperrklinke();
}

// ============================================================
// Montageansicht (Kontrolle, Kaufteile als Geisterkörper)
// ============================================================
module montage() {
    fuss();
    sockelschale();
    abtropfschale();
    fensterrahmen();
    schale_mitte();
    karussell();
    schale_oben();
    bruecke();
    kappe();
    // Stößel in oberster Stellung
    translate([st_r, 0, blk_z0_oben]) {
        schlitten();
        translate([klinke_x, klinke_y, -klinke_laenge]) sperrklinke();
    }
    translate([st_r, 0, z_oben]) stoesselfuss();
    // Geisterkörper
    %translate([st_r, 0, boden_z]) cylinder(d = 60, h = becher_h);
    %translate([st_r, tang, fuehrung_z0]) cylinder(d = 8, h = sp_l);
    %translate([st_r, -tang, fuehrung_z0]) cylinder(d = 8, h = w_l);
    %translate([st_r, tang, kupp_z0]) cylinder(d = kupp_d, h = kupp_l);
    %translate([st_r - nema_flansch / 2, tang - nema_flansch / 2, br_z1]) cube([nema_flansch, nema_flansch, nema_l]);
    for (i = [0 : stationen - 1]) %rotate([0, 0, i * st_w]) translate([st_r, 0, duese_z])
        cylinder(d = syr_zyl_d, h = ka_z1 - ka_tasche_h + 3 - duese_z);
}

// ============================================================
// Auswahl
// ============================================================
if (teil == "fuss") {
    druck_fuss();
} else if (teil == "sockelschale") {
    druck_sockelschale();
} else if (teil == "fensterrahmen") {
    druck_fensterrahmen();
} else if (teil == "abtropfschale") {
    druck_abtropfschale();
} else if (teil == "schale_mitte") {
    druck_schale_mitte();
} else if (teil == "karussell") {
    druck_karussell();
} else if (teil == "schale_oben") {
    druck_schale_oben();
} else if (teil == "bruecke") {
    druck_bruecke();
} else if (teil == "schlitten") {
    druck_schlitten();
} else if (teil == "stoesselfuss") {
    druck_stoesselfuss();
} else if (teil == "sperrklinke") {
    druck_sperrklinke();
} else if (teil == "kappe") {
    druck_kappe();
} else if (teil == "montage") {
    montage();
} else {
    alle_teile();
}

/*
============================================================
DRUCKHINWEISE
============================================================
Material: PETG, Schichthöhe 0,2 mm. Schalen 3 Perimeter, 15 % Infill.
Karussell 5 Perimeter, Rest 4 Perimeter. Keine Stützen. Jedes Teil passt aufs Bett 220 x 220 x 250.
- Fuß: wie modelliert, Fach nach unten. Die Fachdecke hat 45-Grad-Fase, 68 mm flach
  überbrückt, Lüfter voll.
- Sockelschale, Mittelschale, Oberschale: stehend, Nut unten, Feder oben. Höhen 97, 182, 120.
  Die 45-Grad-Auflagen und der Kegel-Laufring drucken stützenfrei. Fenster oben halbrund.
- Fensterrahmen: stehend wie modelliert, außen auf die Sockelschale kleben.
- Abtropfschale: flach. Karussell: Laufsteg unten auf dem Bett, Taschen oben offen.
- Brücke: flach, Unterseite (Lager, Schalter, Köpfe) auf dem Bett.
- Schlitten: Blockunterseite auf dem Bett. Stößelfuß: Stempelunterkante auf dem Bett.
- Sperrklinke: liegend. Haube: auf dem Kopf (Deckplatte auf dem Bett), Nut oben.
- Fensterschlitz der Mittelschale ist eine Ellipse 60 x 20, die Decke wölbt sich, Lüfter voll.
- Lagersitz LM8UU (15,2) leicht klemmend, bei Bedarf nacharbeiten. Wellensitz 7,8 mit 8-mm-Reibahle.

Schrauben
- 4x M3x10 Motor an der Brücke (Köpfe von unten versenkt)
- 4x M3x10 T8-Flanschmutter an den Schlittenblock (Kernloch 2,7)
- 2x M3x40 Stößelfuß am Schlitten (Köpfe von oben versenkt, Kernloch im Stempel)
- 2x M2x10 Endschalter an der Brückenunterseite
- Mikroschalter im Stempel eingeschoben oder geklebt, Druckfeder unter dem Tasterknopf

Magnete und Sensoren
- 6x Magnet Ø 5 x 2 (5 an Radius 76 je Station, 1 Referenz an Radius 69 bei Station 1)
- 2x Hall-Sensor SS49E oder A3144 in den Taschen bei 0 Grad (Radius 76 und 69), Luft etwa 0,7 mm
- Polung der Magnete einheitlich, zuerst am Sensor prüfen

Kaufteile mit Längen
- NEMA 17, 40 lang, Welle 24 (nachmessen)
- Trapezspindel T8, 2 mm Steigung: 138 mm (Z 262 bis 400), aus 200 mm gekürzt
- Führungswelle 8 mm: 162 mm (Z 262 bis 424), aus 200 mm gekürzt
- 1x LM8UU, 1x T8-Flanschmutter, 1x Kupplung 5 auf 8 (25 lang), 1x Lager 608
- 1x Mikroschalter 12,8 x 6,5 x 5,8, 1x Endschalter 20 x 10 x 6,5
- 5x Spritze 60 ml Luer-Lock, 1x Mischbecher Ø 60 x 60, 1x LED-Ring Ø 50
- ESP32 DevKit, TMC2209, Buchse 12 V, Netzteil 12 V 2 A

Nachzumessen
Flansch der 60-ml-Spritze (lang, quer, Dicke), Zylinder-Ø, Kolbenplatte, NEMA-Baulänge und
Wellenlänge, Kupplungslänge und -durchmesser, Flanschmutter (Dicke, Lochkreis, Körperlänge),
LM8UU außen, Endschalter und Mikroschalter (Maße, Lage des Stößels), Hall-Sensor.

Montagereihenfolge
1. Fuß mit Elektronik bestücken, Kabel durch das Kabelloch, Sockelschale aufstecken.
2. Fensterrahmen auf die Sockelschale kleben, Abtropfschale auf die Auflage legen.
3. Mittelschale aufstecken, Hall-Sensoren in die Taschen legen, Kabel nach unten führen.
4. Magnete ins Karussell kleben, Karussell auf den Laufring legen, Rastung prüfen.
5. Oberschale aufstecken. Spritzen in die Flanschtaschen hängen.
6. Schlitten mit LM8UU, Flanschmutter und Stempel bestücken, Klinke einstecken.
7. Brücke bestücken: Motor, Lager 608, Endschalter, Kupplung, Spindel und Welle in den
   Schlitten einfädeln, Brücke auf die Oberschale legen. Kabel anschließen.
8. Haube mit LED-Ring aufstecken, Referenzfahrt, Stationen und Hall-Impulse prüfen.

Abweichungen und Risiken gegenüber dem Parameterblatt
- Laufring: durchgehender 45-Grad-Kegel statt Ring mit Stegen (stützenfrei druckbar).
- Haube reicht als Mantel von Z 418 bis 480 (Blatt: 426 bis 480), damit sie auf der Oberschale
  sitzt. Der Motor liegt oben an der Haubendecke an (Baulänge nachmessen).
- Brücke Ø 165 hat nur 0,1 mm Radialluft zur Innenwand (82,6). Bei Bedarf br_d verkleinern.
- Motorecke liegt bei r 82,2 und damit 0,3 mm vor dem Brückenrand.
- Block des Schlittens ist 56 breit, die Säule für das LM8UU steht 1,6 mm über, und der
  Mutterflansch (Ø 22) ragt auf der Spindelseite 3 mm heraus.
- Sperrklinke ist ein 123 mm langer Stift Ø 7, empfindlich. Sie greift in eine Sperrnut
  im Karussell und eine Bohrung im Laufring. Dreht das Karussell nicht auf einer Station,
  kommt der Schlitten nicht nach unten.
- Spindel 138 mm statt 150 laut Blatt (Z 262 bis 400).
- Hall-Taschen liegen im Laufring bei 0 Grad (Radius 76 und 69), Rastzunge bei 36 Grad.
*/
