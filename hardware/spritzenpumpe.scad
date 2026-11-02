// ============================================================
// Spritzenpumpe als senkrechter Turm, 5 Stationen in einer Reihe, OpenSCAD
// Alle Maße in mm. Düse nach unten, flache Mischschale wird von vorne
// in einen Schacht unter die Düsen geschoben.
//
// Koordinaten (Montage): X mittig, Y = 0 hinten, Y+ nach vorne, Z = 0 Tisch.
// Teile werden lokal um die Spindelachse der Station modelliert (X = 0, Y = 0
// auf der Spindel, Linearwelle bei X = wellen_abstand) und für den Druck
// flach auf das Bett gelegt. Alle fünf Stationen sind gleich.
//
// Aufbau je Station:
//   Motor NEMA 17 hängt unter der Sockelplatte, Welle nach oben
//   Kupplung, T8-Spindel senkrecht, EINE 8-mm-Welle 22 mm neben der Spindel
//   Spritzenhalter (auf der Welle geklemmt, von vorne offen, Rastnase)
//   Schlitten (zwei LM8UU übereinander auf der Welle, Flanschmutter auf der
//     Spindel, Arm nach vorne mit U-Aufnahme für die Kolbenplatte)
//   Kopf (Wellenende, Lager 608 am Spindelende, Endschalter)
//
// Spindel hinten, Spritzenachse davor über der Schale. Die Welle steht neben
// der Spindel (X+). Welle und Spindel zusammen halten den Schlitten gegen
// Verdrehen, zwei LM8UU übereinander gegen Kippen des Arms.
//
// Platz: Die Motoren (42,3 mm) hängen an der Rückseite unter der Platte. Die
// Platte steht so hoch, dass die Schale (37,5 mm hoch) unter den Motoren
// durchgeschoben werden kann. Dadurch liegen Motorreihe und Schale in der
// gleichen Tiefe und der Sockel bleibt etwa 115 mm tief. Die Spritzen stehen
// vor der Motorplatte über der Schale.
// ============================================================

// ---------- Steuerung ----------
teil = "alle";          // "sockel", "bodenplatte", "schlitten", "spritzenhalter", "kopf", "montage", "alle"
stationen = 5;          // Anzahl Stationen
$fn = 64;               // Rundungsqualität

// ---------- Allgemein ----------
spiel = 0.3;            // Spiel für Steckverbindungen
m3_d = 3.4;             // M3 Durchgangsloch
m3_kopf_d = 6.4;        // Senkung für M3 Zylinderkopf
m3_kopf_t = 4;          // Tiefe der Kopfsenkung
m3_mutter_sw = 5.5;     // M3 Mutter Schlüsselweite
m3_mutter_h = 2.4;      // M3 Mutter Dicke
m3_pilot = 2.7;         // Kernloch für selbstschneidende M3 in PETG
m2_pilot = 1.7;         // Kernloch für selbstschneidende M2 in PETG

// ---------- Spritze 60 ml Luer-Lock ----------
syr_zyl_d = 30;         // Außendurchmesser Zylinder
syr_flansch_b = 45;     // Flanschbreite (lange Achse, liegt in Y)
syr_flansch_t = 3;      // Flanschdicke
syr_flansch_h = 32;     // Flanschbreite quer (kurze Achse, liegt in X, Annahme, nachmessen)
syr_stange_b = 12;      // Breite der Kolbenstange (Annahme, nachmessen)
syr_l = 90;             // Länge ab Flansch bis Spitze (Annahme, nachmessen)
kolben_d = 30;          // Kolbenplatte Durchmesser
kolben_t = 4;           // Kolbenplatte Dicke

// ---------- NEMA 17 ----------
nema_flansch = 42.3;    // Flanschmaß
nema_loch = 31;         // Lochabstand
nema_m3 = 3.4;          // Lochdurchmesser M3
nema_bund_d = 22;       // Zentrierbund Durchmesser
nema_l = 40;            // Baulänge des Motorkörpers (Annahme, nachmessen)
nema_welle_l = 24;      // Wellenlänge über dem Flansch (Annahme, nachmessen)

// ---------- Trapezspindel T8 mit Flanschmutter ----------
sp_d = 8;               // Spindeldurchmesser
mutter_flansch_d = 22;  // Flanschdurchmesser der Mutter
mutter_flansch_t = 3.5; // Flanschdicke (Annahme, nachmessen)
mutter_loch_kreis = 16; // Lochkreis der 4 M3-Löcher
mutter_koerper_d = 10.2;// Mutterkörper Durchmesser
mutter_laenge = 15;     // Mutterkörper Länge
spindel_frei_d = 9.2;   // Durchlass für die Spindel im Spritzenhalter (hält den Halter auch gegen Verdrehen)

// ---------- Linearwelle und Lager ----------
welle_d = 8;            // Wellendurchmesser
welle_pass = 7.8;       // Bohrung für Presspassung der Welle
wellen_tiefe = 10;      // Einstecktiefe der Welle im Sockel
wellen_abstand = 22;    // Abstand Spindel zu Welle (Mitte zu Mitte), Welle liegt bei X+
lm_d = 15;              // LM8UU Außendurchmesser
lm_l = 24;              // LM8UU Länge
lm_spiel = 0.2;         // Zugabe für den Lagersitz

// ---------- Kupplung ----------
kupp_d = 19;            // Durchmesser
kupp_l = 25;            // Länge
kupp_einschub = 12;     // Einstecktiefe der Spindel in die Kupplung

// ---------- Mikro-Endschalter ----------
es_l = 20;              // Länge
es_b = 10;              // Breite
es_t = 6.5;             // Dicke
es_loch = 9.5;          // Lochabstand (liegt in X)
es_y = 19;              // Y-Lage von Schalter und Nase vor der Spindelachse
es_hub = 1;             // Stößelweg bis zum Schalten
es_sitz = 2;            // Sitztiefe des Schalters im Kopf
nase_b = 5;             // Breite und Tiefe der Schaltnase
nase_h = 8;             // Höhe der Schaltnase

// ---------- Station ----------
station_abstand = 44;   // Abstand der Stationen (Spritzenachsen), alle in einer Reihe
hub = 80;               // Kolbenweg

// ---------- Mischschale ----------
schale_b = 200;         // Schale Breite (X)
schale_t = 90;          // Schale Tiefe (Y)
schale_h = 35;          // Schale Höhe
schale_spiel = 2;       // Spiel im Schacht, je Seite
duese_luft = 10;        // Düsenspitze über Schalenoberkante
bp_t = 4;               // Dicke der losen Bodenplatte im Schacht
mulde_t = 1.5;          // Tiefe der Mulde (hinterer Anschlag der Schale)
mulde_spiel = 0.5;      // Spiel der Schale in der Mulde, je Seite
schale_motor_luft = 2.5;// Luft zwischen Schalenoberkante und Motorunterseite
syr_abstand_platte = 3; // Luft zwischen Spritzenzylinder und Vorderkante der Motorplatte

// ---------- Sockel ----------
sk_pl = 12;             // Dicke der Motorplatte
sk_wand = 3;            // Wand von Rückwand und Seitenwänden
kabel_b = 14;           // Breite des Kabelkanals
kabel_h = 10;           // Höhe des Kabelkanals

// ---------- Schlitten ----------
sl_wand = 2;            // Wand um den Lagersitz
sl_links = 8.4;         // Schlittenkörper links der Spindelachse
lm_sitz_boden = 2;      // Anschlag unter dem unteren Lager
ar_boden = 3;           // Boden der U-Aufnahme (zieht den Kolben nach oben)
ar_decke = 3;           // Decke der U-Aufnahme (drückt den Kolben)
ar_wand = 3;            // Wand um die U-Aufnahme
ar_vorn = 10;           // Aufnahmeblock reicht so weit vor die Kolbenachse
ar_rippe_b = 18;        // Breite der Armrippe

// ---------- Spritzenhalter ----------
sh_boden = 5;           // Boden unter dem Flansch
sh_decke = 3;           // Decke über dem Flansch
sh_hinten = 4;          // Rückwand der Flanschtasche
sh_vorn = 20;           // Block reicht so weit vor die Spritzenachse
sh_steg_b = 16;         // Breite des Stegs zur Wellenklemme
sh_rippe_b = 10;        // Breite der Tragrippe
sh_rippe_h = 40;        // Höhe der Tragrippe nach unten
sh_klemm_wand = 6;      // Wand der Wellenklemme außen
raste = 1;              // Überstand der Rastnasen pro Seite
raste_d = 3;            // Durchmesser der Rastnasen
raste_y = 13;           // Lage der Rastnasen vor der Spritzenachse

// ---------- Kopf ----------
kp_t = 10;              // Plattendicke
kp_rand = 3;            // Rand um die Welle und das Lager
lager_d = 22;           // Lager 608 Außendurchmesser
lager_t = 7;            // Lager 608 Dicke

// ============================================================
// Abgeleitete Maße (nicht ändern)
// ============================================================
lm_bohr = lm_d + lm_spiel;
wa = wellen_abstand;

// ---------- Funktionen ----------
function sk_breite(n) = sk_xl + (n - 1) * station_abstand + sk_xr;
function sx(i, n) = -sk_breite(n) / 2 + sk_xl + i * station_abstand;   // X der Spindel und Spritzenachse
function xn(n) = (sx(0, n) + sx(n - 1, n)) / 2;                       // Mitte der Düsenreihe
function kp_breite(n) = (n - 1) * station_abstand + kp_links + kp_rechts;

// Schale und Schacht
schacht_b = schale_b + 2 * schale_spiel;
schacht_t = schale_t + 2 * schale_spiel;
schale_z0 = bp_t - mulde_t;                           // Schalenunterseite (in der Mulde)
schale_ok = schale_z0 + schale_h;                     // Schalenoberkante
duese_z = schale_ok + duese_luft;                     // Düsenspitze

// Sockel
sk_luft = schale_ok + schale_motor_luft;              // Motorunterseite über dem Tisch
sk_h = sk_pl + nema_l + sk_luft;                      // Oberkante Platte
sk_fuehr_h = sk_luft - 1;                             // Höhe der Führungswände neben der Schale
sk_xl = nema_flansch / 2 + sk_wand + 0.5;             // Rand links der ersten Spindel
sk_xr = max(sk_xl, wa + welle_pass / 2 + sk_wand);    // Rand rechts der letzten Spindel (Welle)
y_a = nema_flansch / 2 + sk_wand + 0.5;               // Spindelachse (Motormitte) in Y
sk_pt = y_a + nema_flansch / 2 + sk_wand;             // Tiefe der Motorplatte
y_syr = sk_pt + syr_zyl_d / 2 + spiel + syr_abstand_platte; // Spritzenachse, liegt in der Schalenmitte
dy = y_syr - y_a;                                     // Abstand Spindelachse zu Spritzenachse
y_sch0 = y_syr - schacht_t / 2;                       // Hinterkante des Schachts für die Schale
sk_t = y_syr + schacht_t / 2;                         // Tiefe des Sockels (Schachtvorderkante)

// Schlitten
sl_rechts = wa + lm_bohr / 2 + sl_wand;
sl_b = sl_links + sl_rechts;                          // Breite des Schlittenkörpers
sl_huell = max(sl_links, mutter_flansch_d / 2) + sl_rechts; // Breite mit überstehender Flanschmutter
sl_t = max(lm_bohr + 2 * sl_wand, mutter_flansch_d + 2);
sl_h = 2 * lm_l + lm_sitz_boden + 1;                  // zwei LM8UU übereinander
ar_b = kolben_d + 2 * spiel + 2 * ar_wand;
ar_h = ar_boden + kolben_t + 2 * spiel + ar_decke;

// Spritzenhalter
sh_h = sh_boden + syr_flansch_t + spiel + sh_decke;
sh_b = station_abstand - 4;
kl_x0 = -(spindel_frei_d / 2 + 4);                    // linke Kante des Klemmkörpers
kl_x1 = wa + welle_d / 2 + sh_klemm_wand;             // rechte Kante des Klemmkörpers
kl_y = welle_d / 2 + 4;
sh_schr_x = wa + welle_d / 2 + sh_klemm_wand / 2;
sh_y_block = dy - syr_flansch_b / 2 - spiel - sh_hinten; // Hinterkante des Flanschblocks (lokal)

// Kopf
kp_links = lager_d / 2 + 3;
kp_rechts = wa + welle_pass / 2 + kp_rand;
kp_wtiefe = kp_t - 2;                                 // Wellensackloch im Kopf (nicht durchgehend)
ky0 = y_a - (lager_d / 2 + 4);
ky1 = y_a + es_y + es_b / 2 + 4;

// Höhen (Z)
fl_z = duese_z + syr_l;                               // Flanschunterseite
sh_z0 = fl_z - sh_boden;                              // Unterkante Spritzenhalter
hc_z = sh_z0 + sh_h;                                  // Oberkante Spritzenhalter
sl_z_min = hc_z + 1;                                  // Schlittenunterkante ganz unten
sl_z_max = sl_z_min + hub;                            // Schlittenunterkante ganz oben
nase_oben = sl_z_max + sl_h + nase_h;                 // Nasenspitze oben
kp_z0 = nase_oben + es_hub + es_t - es_sitz;          // Unterkante Kopf
turm_h = kp_z0 + kp_t;                                // Gesamthöhe

// Kupplung, Spindel, Welle (Motorflansch liegt an der Plattenunterseite)
kupp_z0 = sk_h - sk_pl + nema_welle_l - kupp_l / 2;
sp_z0 = kupp_z0 + kupp_l - kupp_einschub;
sp_z1 = kp_z0 + lager_t - 1;
sp_laenge = sp_z1 - sp_z0;
w_z0 = sk_h - wellen_tiefe;
w_z1 = kp_z0 + kp_wtiefe;
w_laenge = w_z1 - w_z0;
totweg = (sl_z_min + ar_boden) - (fl_z + syr_flansch_t);  // Kolben kann nicht ganz bis zum Flansch

// ---------- Prüfungen ----------
assert(sl_b <= 40.01, "Schlitten breiter als 40 mm");
assert(sl_b + 2 < station_abstand, "Schlittenbreite plus 2 mm Spiel nicht kleiner als der Stationsabstand");
assert(nema_flansch < station_abstand, "Motorbreite nicht kleiner als der Stationsabstand");
assert(sl_huell + 0.5 <= station_abstand, "Flanschmutter stößt an den Schlitten der Nachbarstation");
assert(sl_links >= mutter_koerper_d / 2 + spiel + 2, "Schlitten links zu schmal für den Mutterkörper");
assert(ar_b + 1 <= station_abstand, "Armblock kollidiert mit dem Nachbararm");
assert(sh_b >= syr_flansch_h + 2 * spiel + 4, "Halterblock zu schmal für den Flansch");
assert(ar_b <= sh_b, "Armblock breiter als Halterblock");
assert(kl_x1 + 2 <= station_abstand + kl_x0, "Wellenklemme stößt an den Steg der Nachbarstation");
assert(kl_y + 1 <= sh_y_block, "Wellenklemme kollidiert mit dem Flanschblock der Nachbarstation");
assert(y_syr - syr_zyl_d / 2 - spiel >= sk_pt, "Spritzenzylinder steht auf der Motorplatte");
assert(y_sch0 >= sk_wand, "Schacht ragt in die Rückwand");
assert((stationen - 1) * station_abstand / 2 + 10 <= schale_b / 2, "Düsen der äußeren Stationen liegen nicht über der Schale");
assert(sl_z_min > kupp_z0 + kupp_l, "Schlitten stößt unten an die Kupplung");
assert(turm_h <= 350, "Turm höher als 350 mm");

echo(str("Turmhöhe gesamt ", turm_h, " mm"));
echo(str("Stellfläche Sockel ", sk_breite(stationen), " x ", sk_t, " mm (Breite x Tiefe), Sockelhöhe ", sk_h, " mm"));
echo(str("Tiefe: Motorplatte ", sk_pt, " mm, Spritzenachse bei y = ", y_syr, " mm, Schacht von y = ", y_sch0, " bis ", sk_t, " mm"));
echo(str("Schlittenbreite ", sl_b, " mm, mit überstehender Flanschmutter ", sl_huell, " mm, Stationsabstand ", station_abstand, " mm"));
echo(str("Kopf ", kp_breite(stationen), " mm breit"));
echo(str("Linearwelle je Stück ", w_laenge, " mm (1 pro Station, ", stationen, " Stück)"));
echo(str("Spindel T8 mindestens ", sp_laenge, " mm (1 pro Station, ", stationen, " Stück)"));
echo(str("Totweg am unteren Hubende ", totweg, " mm (Kolben erreicht den Flansch nicht ganz)"));
echo(str("Düsenhöhe über dem Tisch ", duese_z, " mm, Flanschhöhe ", fl_z, " mm, Schalenoberkante ", schale_ok, " mm"));

// ============================================================
// Hilfsmodule
// ============================================================

// Langloch in Y: Kreis d bei y=0 bis y=l, Höhe h ab z0 (zur Front offene Aussparung)
module langloch_y(d, l, z0, h) {
    translate([0, 0, z0]) linear_extrude(height = h)
        hull() {
            circle(d = d);
            translate([0, l]) circle(d = d);
        }
}

// ============================================================
// 1. Sockel (Montageposition, Z = 0 Tisch)
// Platte mit hängenden Motoren hinten, Rückwand und Seitenwände tragen sie.
// Davor liegt der Schacht für die Schale, die unter den Motoren durch bis zum
// Anschlag der Mulde geschoben wird. Niedrige Führungswände halten die Schale.
// Druck: auf der Rückwand liegend (siehe druck_sockel), keine Stützen.
// ============================================================
module sockel() {
    sb = sk_breite(stationen);
    pxl = xn(stationen) - schacht_b / 2;                  // linke Schachtkante
    pxr = xn(stationen) + schacht_b / 2;                  // rechte Schachtkante
    difference() {
        union() {
            // Motorplatte
            translate([-sb / 2, 0, sk_h - sk_pl]) cube([sb, sk_pt, sk_pl]);
            // Rückwand über die volle Höhe
            translate([-sb / 2, 0, 0]) cube([sb, sk_wand, sk_h]);
            // Seitenwände hinter der Plattenvorderkante, volle Höhe
            translate([-sb / 2, 0, 0]) cube([sk_wand, sk_pt, sk_h]);
            translate([sb / 2 - sk_wand, 0, 0]) cube([sk_wand, sk_pt, sk_h]);
            // Führungswände neben dem Schacht, niedriger als die Motoren
            translate([-sb / 2, 0, 0]) cube([pxl + sb / 2, sk_t, sk_fuehr_h]);
            translate([pxr, 0, 0]) cube([sb / 2 - pxr, sk_t, sk_fuehr_h]);
        }
        for (i = [0 : stationen - 1]) {
            translate([sx(i, stationen), y_a, 0]) {
                // Zentrierbund und Durchgang für Welle und Kupplung
                translate([0, 0, sk_h - sk_pl - 1]) cylinder(d = nema_bund_d + 2 * spiel, h = sk_pl + 2);
                // NEMA-Lochbild mit Kopfsenkung von oben
                for (a = [-1, 1], b = [-1, 1])
                    translate([a * nema_loch / 2, b * nema_loch / 2, sk_h - sk_pl - 1]) {
                        cylinder(d = nema_m3, h = sk_pl + 2);
                        translate([0, 0, sk_pl + 1 - m3_kopf_t]) cylinder(d = m3_kopf_d, h = m3_kopf_t + 1);
                    }
                // Wellensackloch (eine Welle je Station, neben der Spindel)
                translate([wa, 0, sk_h - wellen_tiefe]) cylinder(d = welle_pass, h = wellen_tiefe + 1);
                // Kabelkanal nach hinten durch die Rückwand, in Höhe der Motorrückseite
                translate([-kabel_b / 2, -y_a - 1, sk_luft - 2]) cube([kabel_b, sk_wand + 2, kabel_h + 2]);
            }
        }
    }
}

// ============================================================
// 1b. Bodenplatte (lose, liegt im Schacht auf dem Tisch)
// Mulde nimmt die Schale auf, ihre Hinterkante ist der Anschlag, vorne offen.
// Druck: flach, Mulde oben.
// ============================================================
module bodenplatte() {
    bw = schacht_b - 2 * spiel;
    by0 = sk_wand + spiel;
    bl = sk_t - spiel - by0;
    mw = schale_b + 2 * mulde_spiel;
    difference() {
        translate([xn(stationen) - bw / 2, by0, 0]) cube([bw, bl, bp_t]);
        translate([xn(stationen) - mw / 2, y_syr - schale_t / 2 - mulde_spiel, bp_t - mulde_t])
            cube([mw, sk_t, mulde_t + 1]);
    }
}

// ============================================================
// 2. Spritzenhalter (lokal: Spindelachse, Z = 0 Unterkante Boden)
// Druck: auf den Kopf gestellt (Oberseite auf dem Bett), Rippe zeigt nach oben.
// ============================================================
module spritzenhalter() {
    d = dy;
    y_pb = d - syr_flansch_b / 2 - spiel;          // Rückwand der Flanschtasche
    y_b0 = y_pb - sh_hinten;                       // Hinterkante des Blocks
    y_b1 = d + sh_vorn;                            // Vorderkante des Blocks
    tw = syr_flansch_h / 2 + spiel;
    union() {
        difference() {
            union() {
                // Klemmkörper an der Welle, reicht links bis über die Spindel
                translate([kl_x0, -kl_y, 0]) cube([kl_x1 - kl_x0, 2 * kl_y, sh_h]);
                // Steg und Tragrippe nach vorne
                translate([-sh_steg_b / 2, 0, 0]) cube([sh_steg_b, y_b0 + 1, sh_h]);
                translate([-sh_rippe_b / 2, kl_y - 1, -sh_rippe_h]) cube([sh_rippe_b, y_b0 + 1 - (kl_y - 1), sh_rippe_h + 0.01]);
                // Block mit Flanschtasche
                translate([-sh_b / 2, y_b0, 0]) cube([sh_b, y_b1 - y_b0, sh_h]);
            }
            // Welle mit Klemmschlitz nach außen und M3-Klemmschraube quer in Y
            translate([wa, 0, -1]) cylinder(d = welle_d + 0.1, h = sh_h + 2);
            translate([wa + 5, 0, sh_h / 2]) cube([10, 1.2, sh_h + 2], center = true);
            translate([sh_schr_x, -kl_y - 1, sh_h / 2]) rotate([-90, 0, 0]) cylinder(d = m3_d, h = 2 * kl_y + 2);
            translate([sh_schr_x, -kl_y - 1, sh_h / 2]) rotate([-90, 0, 0]) rotate([0, 0, 30])
                cylinder(d = (m3_mutter_sw + spiel) / cos(30), h = m3_mutter_h + spiel + 1, $fn = 6);
            translate([sh_schr_x, kl_y - m3_kopf_t, sh_h / 2]) rotate([-90, 0, 0])
                cylinder(d = m3_kopf_d, h = m3_kopf_t + 1);
            // Durchlass für die Spindel
            translate([0, 0, -1]) cylinder(d = spindel_frei_d, h = sh_h + 2);
            // Flanschtasche, von vorne offen
            translate([-tw, y_pb, sh_boden]) cube([2 * tw, y_b1 - y_pb + 1, syr_flansch_t + spiel]);
            // Zylinderschlitz im Boden, von vorne offen
            translate([0, d, 0]) langloch_y(syr_zyl_d + 2 * spiel, 40, -1, sh_boden + 1);
            // Schlitz in der Decke für die Kolbenstange, von vorne offen
            translate([0, d, 0]) langloch_y(syr_stange_b + 2 * spiel, 40, sh_boden + syr_flansch_t, sh_h - sh_boden - syr_flansch_t + 1);
        }
        // Rastnasen am Zylinderschlitz, halten die Spritze gegen Herausrutschen
        for (s = [-1, 1])
            translate([s * (syr_zyl_d / 2 + spiel - raste + raste_d / 2), d + raste_y, 0])
                cylinder(d = raste_d, h = sh_boden);
    }
}

// ============================================================
// 3. Schlitten (lokal: Spindelachse, Z = 0 Unterkante)
// Eine Welle (zwei LM8UU übereinander) plus Spindelmutter. Welle und Spindel
// zusammen verhindern das Verdrehen. Der Körper reicht von sl_links links der
// Spindel bis über die Welle, die Flanschmutter steht links etwas über.
// Druck: wie modelliert, Unterseite auf dem Bett.
// Die U-Aufnahme ist eine Brücke von etwa 30 mm, Lüfter voll.
// ============================================================
module schlitten() {
    d = dy;
    y_p0 = d - (kolben_d / 2 + spiel + ar_wand);   // Hinterkante Aufnahmeblock
    union() {
        difference() {
            union() {
                // Körper mit Lagersitzen und Mutter
                translate([-sl_links, -sl_t / 2, 0]) cube([sl_b, sl_t, sl_h]);
                // Armrippe, hoch für Steifigkeit
                translate([-ar_rippe_b / 2, sl_t / 2 - 1, 0]) cube([ar_rippe_b, y_p0 + 1 - (sl_t / 2 - 1), sl_h]);
                // Aufnahmeblock für die Kolbenplatte
                translate([-ar_b / 2, y_p0, 0]) cube([ar_b, d + ar_vorn - y_p0, ar_h]);
            }
            // Lagersitz für zwei LM8UU übereinander, von oben eingepresst
            translate([wa, 0, 0]) {
                translate([0, 0, -1]) cylinder(d = lm_d - 2, h = sl_h + 2);
                translate([0, 0, lm_sitz_boden]) cylinder(d = lm_bohr, h = sl_h);
            }
            // Durchgang für Mutterkörper und Spindel
            translate([0, 0, -1]) cylinder(d = mutter_koerper_d + 2 * spiel, h = sl_h + 2);
            // Vier M3-Kernlöcher für die Flanschmutter (Flansch liegt oben auf)
            for (k = [0 : 3])
                translate([mutter_loch_kreis / 2 * cos(45 + 90 * k), mutter_loch_kreis / 2 * sin(45 + 90 * k), sl_h - 12])
                    cylinder(d = m3_pilot, h = 13);
            // U-Aufnahme für die Kolbenplatte, von vorne offen
            translate([0, d, 0]) langloch_y(kolben_d + 2 * spiel, 40, ar_boden, kolben_t + 2 * spiel);
            // Schlitz im Boden für die Kolbenstange
            translate([0, d, 0]) langloch_y(syr_stange_b + 2 * spiel, 40, -1, ar_boden + 1.5);
        }
        // Schaltnase auf der Armrippe
        translate([-nase_b / 2, es_y - nase_b / 2, sl_h - 0.01]) cube([nase_b, nase_b, nase_h + 0.01]);
    }
}

// ============================================================
// 4. Kopf (lokal: X und Y wie Montage, Z = 0 Unterkante)
// Druck: Oberseite auf dem Bett, Aussparungen zeigen nach oben.
// ============================================================
module kopf() {
    x0 = sx(0, stationen) - kp_links;
    x1 = sx(stationen - 1, stationen) + kp_rechts;
    difference() {
        translate([x0, ky0, 0]) cube([x1 - x0, ky1 - ky0, kp_t]);
        for (i = [0 : stationen - 1]) {
            translate([sx(i, stationen), y_a, 0]) {
                // Wellensackloch
                translate([wa, 0, -1]) cylinder(d = welle_pass, h = kp_wtiefe + 1);
                // Lagersitz 608 für das freie Spindelende
                translate([0, 0, -1]) cylinder(d = lager_d + 0.2, h = lager_t + 1.2);
                // Sitz und Kernlöcher des Endschalters
                translate([-(es_l + 2 * spiel) / 2, es_y - (es_b + 2 * spiel) / 2, -1])
                    cube([es_l + 2 * spiel, es_b + 2 * spiel, es_sitz + 1]);
                for (s = [-1, 1])
                    translate([s * es_loch / 2, es_y, es_sitz - 1]) cylinder(d = m2_pilot, h = 8);
            }
        }
    }
}

// ============================================================
// Druckpositionen (flach auf dem Bett, ohne Stützen)
// ============================================================
module druck_sockel() {
    // Rückwand liegt auf dem Bett, Platte und Wände stehen senkrecht
    translate([0, sk_h, 0]) rotate([90, 0, 0]) sockel();
}

module druck_bodenplatte() {
    translate([0, -(sk_wand + spiel), 0]) bodenplatte();
}

module druck_schlitten() {
    translate([sl_links, sl_t / 2, 0]) schlitten();
}

module druck_halter() {
    translate([sh_b / 2, dy + sh_vorn, sh_h]) rotate([180, 0, 0]) spritzenhalter();
}

module druck_kopf() {
    translate([0, ky1, kp_t]) rotate([180, 0, 0]) kopf();
}

// ============================================================
// Anordnung aller Teile in Druckposition (nur eine Übersicht, die Teile
// werden einzeln exportiert)
// ============================================================
module alle_teile() {
    sb = sk_breite(stationen);
    y1 = sk_h + 15;
    y2 = y1 + sk_t + 15;
    y3 = y2 + (ky1 - ky0) + 15;
    y4 = y3 + dy + sh_vorn + sl_t / 2 + 15;
    druck_sockel();
    translate([0, y1, 0]) druck_bodenplatte();
    translate([0, y2, 0]) druck_kopf();
    for (i = [0 : stationen - 1]) {
        translate([-sb / 2 + i * (sl_b + 6), y3, 0]) druck_schlitten();
        translate([-sb / 2 + i * (sh_b / 2 + kl_x1 + 4), y4, 0]) druck_halter();
    }
}

// ============================================================
// Montageansicht (nur zur Kontrolle, Schale als Geisterkörper)
// ============================================================
module montage() {
    sockel();
    bodenplatte();
    %translate([xn(stationen) - schale_b / 2, y_syr - schale_t / 2, schale_z0]) cube([schale_b, schale_t, schale_h]);
    for (i = [0 : stationen - 1])
        translate([sx(i, stationen), y_a, 0]) {
            translate([0, 0, sl_z_min]) schlitten();
            translate([0, 0, sh_z0]) spritzenhalter();
        }
    translate([0, 0, kp_z0]) kopf();
}

// ============================================================
// Auswahl
// ============================================================
if (teil == "sockel") {
    druck_sockel();
} else if (teil == "bodenplatte") {
    druck_bodenplatte();
} else if (teil == "schlitten") {
    druck_schlitten();
} else if (teil == "spritzenhalter") {
    druck_halter();
} else if (teil == "kopf") {
    druck_kopf();
} else if (teil == "montage") {
    montage();
} else {
    alle_teile();
}

/*
============================================================
DRUCKHINWEISE
============================================================
Material:  PETG, Schichthöhe 0,2 mm, 4 Perimeter, Infill 30 %
Stützen:   keine nötig
Druckposition
- Sockel: auf der Rückwand liegend (Rückwand auf dem Bett, Platte und Wände
  stehen senkrecht). Footprint auf dem Bett etwa 230 x 92 mm, braucht ein Bett
  ab 235 mm Breite. Auf einem 220-mm-Bett den Sockel teilen (nicht modelliert).
  Die großen Motorbohrungen liegen dabei waagerecht, Brückenmodus an.
- Bodenplatte: flach, Mulde oben. Etwa 204 x 111 mm.
- Spritzenhalter: auf dem Kopf, Rippe zeigt nach oben. 5 gleiche Stück.
- Schlitten: Unterseite auf dem Bett. 5 gleiche Stück.
  Die U-Aufnahme ist eine Brücke von ca. 30 mm, Lüfter voll, Brückenmodus an.
- Kopf: Oberseite auf dem Bett, Aussparungen oben. Etwa 219 x 43 mm.
- Wellensitze (7,8 mm) bei Bedarf mit 8-mm-Reibahle aufweiten, Lagersitze
  (15,2 mm) sollen die LM8UU leicht klemmend aufnehmen.
- Beim Schlitten die LM8UU vor dem Einpressen leicht einfetten. Zwei Lager
  übereinander sitzen auf 2 x 24 mm, die Wand um den Sitz ist nur 2 mm dick.

Schale
- Schale 200 x 90 x 35 mm, Schacht 204 x 94 mm (2 mm Spiel je Seite). Sie wird
  von vorne unter den Motoren durch bis an die Hinterkante der Mulde geschoben.
- Die Düsen enden 10 mm über der Schalenoberkante. Die Schalenmitte liegt
  unter der Spritzenachse und in X unter der Mitte der Düsenreihe.
- Die Motoren hängen 2,5 mm über der Schalenoberkante (37,5 mm). Höhere
  Schalen passen nicht unter die Motoren.

Schrauben und Kleinteile pro Station
- 4x M3x12 Motor an Sockelplatte (Kopf in der Senkung von oben)
- 4x M3x10 Flanschmutter am Schlitten (schneiden ins Kernloch 2,7 mm)
- 1x M3x16 und 1x M3-Mutter Wellenklemme am Spritzenhalter
- 2x M2x12 Endschalter am Kopf (schneiden ins Kernloch 1,7 mm)
- 2x LM8UU, 1x Lager 608, 1x Kupplung 5 auf 8 mm, 1x Flanschmutter T8
- 1x Linearwelle 8 mm, 1x Trapezspindel T8, 1x NEMA 17, 1x Mikroschalter
Für 5 Stationen: 20x M3x12, 20x M3x10, 5x M3x16, 5x M3-Mutter,
10x M2x12, 10x LM8UU, 5x 608, 5x Kupplung, 5x Flanschmutter, 5x NEMA 17,
5x Mikroschalter, 5x Welle, 5x Spindel.
Dazu 1 Sockel, 1 Bodenplatte, 1 Kopf, 5 Schlitten, 5 Halter.

Benötigte Längen (Werte stehen bei jedem Rendern in der Konsole)
- Linearwelle: w_laenge, Sockelsack bis Kopfsack, siehe echo
- Trapezspindel: sp_laenge, Kupplung bis Lager 608, siehe echo
- Gesamthöhe turm_h, Stellfläche, Totweg am unteren Hubende, siehe echo

Bekannte Konflikte und Risiken
- Die Spritzenachse liegt vor der Motorplatte, der Halter sitzt nur auf der
  einen Welle. Gegen Verdrehen hilft nur die Spindel im 9,2-mm-Loch des
  Halters. Bei Spiel den Spindeldurchlass verkleinern oder eine Rippe zum
  Kopf ergänzen.
- Die Flanschmutter steht links 2,6 mm über den Schlitten und hat zur
  Nachbarstation nur etwa 1,4 mm Luft. Die Kernlöcher links haben nur etwa
  1,4 mm Wand.
- Zwischen den Motoren bleiben 1,7 mm Luft, die Wärme staut sich. Bei
  Dauerbetrieb Strom herunterregeln oder Lüfter ergänzen.
- Rückwand und Seitenwände (3 mm) tragen Platte und Motoren. Bei Wackeln
  Wände verdicken oder Rippen zwischen die Motoren setzen.
- Der Turm steht im hinteren Teil des Sockels. Bei vollen Spritzen Gewicht
  oder Gummifüße vorne ergänzen, sonst kippt das Gerät nach vorne.
- Die Welle ist etwa 220 mm lang und nur an den Enden gehalten. Der Arm
  vor der Welle erzeugt ein Kippmoment, die zwei LM8UU fangen es ab.
- Der Flanschsitz hat seitlich nur etwa 1 mm Auflage, wenn die Flanschbreite
  quer 32 mm beträgt. Flansch nachmessen.

Maße, die an echten Teilen nachzumessen sind
Flanschbreite lang und quer, Flanschdicke, Zylinderdurchmesser und Länge
der 60-ml-Spritze, Kolbenplattendurchmesser und dicke, Kolbenstangenbreite,
Schalenmaße (Länge, Breite, Höhe, Randform), NEMA-17 Baulänge, Wellenlänge
und Zentrierbund, Kupplungsmaße, Flanschdicke und Lochkreis der T8-Mutter,
Mutterkörperlänge, LM8UU Außendurchmesser und Länge, Lochabstand des
Endschalters und Lage seines Stößels, Lager 608 Außendurchmesser und Dicke.
*/
