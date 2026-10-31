// ============================================================
// Spritzenpumpe (Dosierstation) für das Acrylfarben-Mischgerät
// Parametrisch, OpenSCAD. Alle Maße in mm.
//
// Aufbau einer Station (Blick von oben, Y = Spindelachse):
//   Motor | Motorhalter | Kupplung | Kolbenschlitten | Spritzenhalter | Spritze
// Der Kolbenschlitten läuft auf zwei 8-mm-Wellen (LM8UU) und wird von der
// T8-Spindel verfahren. Die Kolbenplatte der Spritze steckt von oben in einem
// Schlitz des Schlittens (ziehen und drücken). Die Spritze liegt mit dem Flansch
// im Spritzenhalter. Die Spindel liegt auf Wellenhöhe, die Spritzenachse
// liegt syr_dz darüber.
// Koordinaten der Teile: X mittig, Y = 0 an der Rückseite, Z = 0 unten.
// ============================================================

// ---------- Steuerung ----------
teil = "alle";          // "motorhalter", "kolbenschlitten", "spritzenhalter", "grundplatte", "alle"
stationen = 5;          // Anzahl Stationen der Grundplatte
becher_modus = "aussparung";  // "aussparung" (Ausschnitt) oder "markierung" (eingravierter Ring)
$fn = 64;               // Rundungsqualität

// ---------- Allgemein ----------
wand = 4;               // Wandstärke
spiel = 0.3;            // Spiel für Steckverbindungen
m3_d = 3.4;             // M3 Durchgangsloch
m3_kopf_d = 6.4;        // Senkung für M3 Zylinderkopf (Kopf 5,5)
m3_kopf_t = 4;          // Tiefe der Kopfsenkung
m3_mutter_sw = 5.5;     // M3 Mutter Schlüsselweite
m3_mutter_h = 2.4;      // M3 Mutter Dicke

// ---------- Spritze 60 ml Luer-Lock ----------
syr_zyl_d = 30;         // Außendurchmesser Zylinder
syr_flansch_b = 45;     // Flanschbreite
syr_flansch_t = 3;      // Flanschdicke
syr_flansch_h = 32;     // Flanschhöhe quer zur Breite (Annahme, nachmessen)
syr_stange_b = 12;      // Breite der Kolbenstange (Annahme, nachmessen)
syr_l = 90;             // Länge ab Flansch bis Spitze (Annahme, nachmessen)
kolben_d = 30;          // Kolbenplatte Durchmesser
kolben_t = 4;           // Kolbenplatte Dicke

// ---------- NEMA 17 ----------
nema_flansch = 42.3;    // Flanschmaß
nema_loch = 31;         // Lochabstand
nema_m3 = 3.4;          // Lochdurchmesser M3
nema_bund_d = 22;       // Zentrierbund Durchmesser
motor_freiraum = 3;     // Abstand Motorunterseite zur Grundplatte

// ---------- Trapezspindel T8 mit Flanschmutter ----------
sp_d = 8;               // Spindeldurchmesser
mutter_flansch_d = 22;  // Flanschdurchmesser der Mutter
mutter_flansch_t = 3.5; // Flanschdicke (Annahme, nachmessen)
mutter_loch_kreis = 16; // Lochkreis der 4 M3-Löcher
mutter_koerper_d = 10.2;// Mutterkörper Durchmesser
mutter_laenge = 15;     // Mutterkörper Länge (Annahme, nur für Spindelabschätzung)
spindel_frei_d = 10;    // Durchlass für das freie Spindelende im Spritzenhalter

// ---------- Linearwellen und Lager ----------
welle_d = 8;            // Wellendurchmesser
welle_pass = 7.8;       // Bohrung für Presspassung der Welle
wellen_tiefe = 10;      // Einstecktiefe der Wellen in Motorhalter und Spritzenhalter
wellen_abstand = 35;    // Abstand der beiden Wellen (Mitte zu Mitte)
lm_d = 15;              // LM8UU Außendurchmesser
lm_l = 24;              // LM8UU Länge
lm_spiel = 0.2;         // Zugabe für den Lagersitz

// ---------- Kupplung ----------
kupp_d = 19;            // Durchmesser
kupp_l = 25;            // Länge

// ---------- Mikro-Endschalter ----------
es_l = 20;              // Länge
es_b = 10;              // Breite
es_t = 6.5;             // Dicke
es_loch = 9.5;          // Lochabstand
es_loch_d = 2.2;        // Loch für M2
es_langloch = 4;        // Verstellweg der Langlöcher in Y
es_y0 = 3;              // Abstand Schalterkörper zur Vorderseite des Motorhalters
es_z_ueber = 27;        // Höhe der Schaltermitte über der Spindelachse
nase_b = 5;             // Breite der Schaltnase

// ---------- Station ----------
station_abstand = 60;   // Abstand der Stationen
hub = 80;               // Kolbenweg
puffer = 4;             // Abstand Schlittenvorderseite zu Spritzenhalter bei vollem Hub
syr_dz = 26;            // Höhe der Spritzenachse über der Spindelachse

// ---------- Füße ----------
fuss_b = 14;            // Breite der Fußlasche
fuss_l = 12;            // Länge der Fußlasche
fuss_t = 4;             // Dicke der Fußlasche

// ---------- Grundplatte ----------
gp_t = 6;               // Plattendicke
gp_rand = 8;            // seitlicher Rand
gp_hinten = 10;         // Plattenüberstand hinter der Motorplatte
becher_d = 90;          // Außendurchmesser Mischbecher (Annahme, nachmessen)

// ============================================================
// Abgeleitete Maße (nicht ändern)
// ============================================================
lm_bohr = lm_d + lm_spiel;                  // Lagersitz
bl_b = wellen_abstand + lm_bohr + 2 * wand; // Blockbreite aller Teile
achse_h = nema_flansch / 2 + motor_freiraum;// Höhe Spindel und Wellen über der Grundplatte
fuss_x = bl_b / 2 - fuss_b / 2;             // X-Lage der Fußlöcher

// Motorhalter
mp_t = 12;                                  // Plattendicke Motorhalter
mp_h = achse_h + nema_flansch / 2 + wand;   // Plattenhöhe
es_kons_b = es_b + 6;                       // Breite der Schalterkonsole
es_kons_l = es_y0 + es_l + 2;               // Länge der Schalterkonsole
es_kons_z = achse_h + es_z_ueber - es_t / 2 - wand;  // Unterkante der Konsole

// Kolbenschlitten
sl_boden = 2.5;                             // Wand unter dem Lagersitz
sl_ca = lm_bohr / 2 + sl_boden;             // Achshöhe im Schlitten (Z=0 unten)
sl_zk = sl_ca + syr_dz;                     // Höhe der Kolbenplattenmitte
sl_h = sl_zk + kolben_d / 2 + wand;         // Gesamthöhe
sl_l = lm_l + 2;                            // Länge
sl_haut = 3;                                // Außenhaut hinter der Flanschmutter
sl_rw = sl_haut + (m3_mutter_h + spiel) + 2.5;  // Hinterwand bis zum Kolbenschlitz
sl_anschlag = 1;                            // Lageranschlag hinten
hom_abstand = kupp_l + mutter_flansch_t + 5;// Abstand Schlittenrückseite zu Motorhalter in Referenzstellung
nase_h = 3;                                 // Höhe der Nasenfläche
nase_l = hom_abstand - es_y0 - es_l - 0.5;  // Länge der Nase
sl_nut_z0 = max(0.6, sl_ca - mutter_loch_kreis / 2 * sin(45) - 3.5);  // Unterkante Mutterschlitze

// Spritzenhalter
sh_l = 20;                                  // Länge
sh_wb = 7;                                  // Hinterwand vor dem Flanschschlitz
sh_zs = achse_h + syr_dz;                   // Höhe der Spritzenachse
sh_h = sh_zs + syr_zyl_d / 2 + wand;        // Gesamthöhe

// Lage der Stationsteile in Y (Motorhalter Rückseite = 0)
y_halter = mp_t + hom_abstand + sl_l + hub + puffer;  // Rückseite Spritzenhalter
y_flansch = y_halter + sh_wb + (syr_flansch_t + spiel) / 2;
y_spitze = y_flansch + syr_l;               // Spritzenspitze

// Grundplatte
gp_vorn = max(y_halter + sh_l + fuss_l + becher_d / 2 + 5, y_spitze);  // Vorderkante

function gp_breite(n) = n * station_abstand + 2 * gp_rand;

// Fußlöcher einer Station (X, Y)
function fuss_loecher() = [
    [-fuss_x, mp_t + fuss_l / 2],
    [ fuss_x, mp_t + fuss_l / 2],
    [-fuss_x, y_halter - fuss_l / 2],
    [ fuss_x, y_halter - fuss_l / 2],
    [-fuss_x, y_halter + sh_l + fuss_l / 2],
    [ fuss_x, y_halter + sh_l + fuss_l / 2]
];

assert(bl_b <= station_abstand, "Blockbreite ist größer als der Stationsabstand");

// Hilfsangaben für die Beschaffung (erscheinen in der OpenSCAD-Konsole)
echo(str("Wellenlänge ca. ", y_halter - mp_t + 2 * wellen_tiefe, " mm"));
echo(str("Spindel mindestens ca. ", hom_abstand + hub + mutter_laenge, " mm"));
echo(str("Grundplatte ", gp_breite(stationen), " x ", gp_hinten + gp_vorn, " mm"));

// ============================================================
// Hilfsmodule
// ============================================================

// Zylinder entlang +Y von y=0 bis y=l
module zyl_y(d, l) {
    rotate([-90, 0, 0]) cylinder(d = d, h = l);
}

// Liegende Bohrung entlang +Y in Tropfenform (Spitze oben, 45 Grad), ohne Stützen druckbar
module tropfen_y(d, l) {
    rotate([-90, 0, 0])
        linear_extrude(height = l)
            hull() {
                circle(d = d);
                translate([0, -d / 2 * 1.4142]) circle(d = 0.01);
            }
}

// Schlitz der Dicke t in Y, Kreis d bei Höhe zc, nach oben offen bis zt
module schlitz_u(d, t, zc, zt) {
    hull() {
        translate([0, 0, zc]) zyl_y(d, t);
        translate([-d / 2, 0, zc]) cube([d, t, zt - zc + 1]);
    }
}

// Fußlasche mit M3-Loch an der Fläche yk, r = -1 nach hinten, r = 1 nach vorne
module fuss_tab(x, yk, r) {
    y_a = (r > 0) ? yk - 1 : yk - fuss_l;
    difference() {
        translate([x - fuss_b / 2, y_a, 0]) cube([fuss_b, fuss_l + 1, fuss_t]);
        translate([x, yk + r * fuss_l / 2, -0.1]) cylinder(d = m3_d, h = fuss_t + 0.2);
    }
}

// ============================================================
// 1. Motorhalter
// Druckposition: Rückseite auf dem Bett, Vorderseite oben.
// ============================================================
module motorhalter_montage() {
    difference() {
        union() {
            // Platte
            translate([-bl_b / 2, 0, 0]) cube([bl_b, mp_t, mp_h]);
            // Füße vorne (Motor hängt hinten, dort ist kein Platz für Füße)
            for (sx = [-1, 1]) fuss_tab(sx * fuss_x, mp_t, 1);
            // Konsole für den Endschalter (im Druck eine stehende Rippe)
            translate([-es_kons_b / 2, mp_t - 1, es_kons_z])
                cube([es_kons_b, es_kons_l + 1, wand]);
        }
        // NEMA-17-Lochbild mit Kopfsenkung von vorne
        for (sx = [-1, 1], sz = [-1, 1])
            translate([sx * nema_loch / 2, 0, achse_h + sz * nema_loch / 2]) {
                translate([0, -1, 0]) zyl_y(nema_m3, mp_t + 2);
                translate([0, mp_t - m3_kopf_t, 0]) zyl_y(m3_kopf_d, m3_kopf_t + 1);
            }
        // Bohrung für Zentrierbund und Kupplung
        translate([0, -1, achse_h]) zyl_y(nema_bund_d + 2 * spiel, mp_t + 2);
        // Aufnahmen der Linearwellen (Presspassung, Sackloch von vorne)
        for (sx = [-1, 1])
            translate([sx * wellen_abstand / 2, mp_t - wellen_tiefe, achse_h])
                zyl_y(welle_pass, wellen_tiefe + 1);
        // Langlöcher für den Endschalter (M2 von oben, Mutter unter der Konsole)
        for (sy = [-1, 1])
            hull()
                for (dy = [0, es_langloch])
                    translate([0, mp_t + es_y0 + es_l / 2 + sy * es_loch / 2 + dy - es_langloch / 2, es_kons_z - 1])
                        cylinder(d = es_loch_d, h = wand + 2);
    }
}

module motorhalter() {
    // flach auf die Rückseite legen, Y wird zur Druckhöhe
    translate([0, mp_h, 0]) rotate([90, 0, 0]) motorhalter_montage();
}

// ============================================================
// 2. Kolbenschlitten
// Druckposition: Unterseite auf dem Bett, Schlitz nach oben.
// ============================================================

// Schaltnase an der Rückseite, Unterseite 45 Grad (ohne Stützen)
module nase() {
    zt = sl_ca + es_z_ueber + nase_h / 2;
    rotate([90, 0, 90])
        linear_extrude(height = nase_b, center = true)
            polygon([
                [0.5, zt],
                [-nase_l, zt],
                [-nase_l, zt - nase_h],
                [0.5, zt - nase_h - nase_l - 0.5]
            ]);
}

module kolbenschlitten() {
    difference() {
        union() {
            translate([-bl_b / 2, 0, 0]) cube([bl_b, sl_l, sl_h]);
            nase();
        }
        // Lagersitze LM8UU: durchgehende Bohrung und Sitz mit Anschlag hinten, vorne offen
        for (sx = [-1, 1])
            translate([sx * wellen_abstand / 2, 0, sl_ca]) {
                translate([0, -1, 0]) tropfen_y(lm_d - 2, sl_l + 2);
                translate([0, sl_anschlag, 0]) tropfen_y(lm_bohr, sl_l);
            }
        // Durchgang für Mutterkörper und Spindel
        translate([0, -1, sl_ca]) tropfen_y(mutter_koerper_d + 2 * spiel, sl_l + 2);
        // Vier M3-Löcher der Flanschmutter
        for (k = [0:3]) {
            a = 45 + 90 * k;
            translate([mutter_loch_kreis / 2 * cos(a), -1, sl_ca + mutter_loch_kreis / 2 * sin(a)])
                zyl_y(m3_d, sl_rw + 3);
        }
        // Mutterschlitze von oben (M3-Muttern einschieben)
        for (sx = [-1, 1])
            translate([sx * mutter_loch_kreis / 2 * cos(45) - (m3_mutter_sw + spiel) / 2, sl_haut, sl_nut_z0])
                cube([m3_mutter_sw + spiel, m3_mutter_h + spiel, sl_h + 1]);
        // Schlitz für die Kolbenplatte (von oben einschieben)
        translate([0, sl_rw, 0])
            schlitz_u(kolben_d + 2 * spiel, kolben_t + spiel, sl_zk, sl_h);
        // Durchlass für die Kolbenstange in der Vorderwand
        translate([0, sl_rw + kolben_t + spiel - 0.1, 0])
            schlitz_u(syr_stange_b + 2 * spiel, sl_l - sl_rw - kolben_t - spiel + 1, sl_zk, sl_h);
    }
}

// ============================================================
// 3. Spritzenhalter
// Druckposition: Unterseite auf dem Bett, Schlitze nach oben.
// ============================================================
module spritzenhalter() {
    difference() {
        union() {
            translate([-bl_b / 2, 0, 0]) cube([bl_b, sh_l, sh_h]);
            // Füße hinten und vorne
            for (sx = [-1, 1]) {
                fuss_tab(sx * fuss_x, 0, -1);
                fuss_tab(sx * fuss_x, sh_l, 1);
            }
        }
        // Aufnahmen der Wellenenden (Presspassung, Sackloch von hinten)
        for (sx = [-1, 1])
            translate([sx * wellen_abstand / 2, -1, achse_h])
                tropfen_y(welle_pass, wellen_tiefe + 1);
        // Durchlass für das freie Spindelende
        translate([0, -1, achse_h]) tropfen_y(spindel_frei_d, sh_l + 2);
        // Schlitz für den Spritzenflansch (von oben einlegen)
        translate([-(syr_flansch_b + 2 * spiel) / 2, sh_wb, sh_zs - syr_flansch_h / 2 - spiel])
            cube([syr_flansch_b + 2 * spiel, syr_flansch_t + spiel, sh_h]);
        // Hinterwand: Durchlass für die Kolbenstange (Flansch bleibt gefangen)
        translate([0, -1, 0])
            schlitz_u(syr_stange_b + 2 * spiel, sh_wb + 1.1, sh_zs, sh_h);
        // Vorderwand: Aufnahme für den Zylinder (von oben einlegen)
        translate([0, sh_wb + syr_flansch_t + spiel - 0.1, 0])
            schlitz_u(syr_zyl_d + 2 * spiel, sh_l - sh_wb - syr_flansch_t - spiel + 1, sh_zs, sh_h);
    }
}

// ============================================================
// 4. Grundplatte
// Druckposition: flach, Muttertaschen liegen unten auf dem Bett.
// Koordinaten: X mittig, Y = 0 an der Rückseite des Motorhalters, vorne = +Y.
// ============================================================
module grundplatte(anzahl = 5, becher = true) {
    gb = gp_breite(anzahl);
    difference() {
        translate([-gb / 2, -gp_hinten, 0]) cube([gb, gp_hinten + gp_vorn, gp_t]);
        // Lochbild: pro Station sechs Schraubenlöcher mit Muttertasche von unten
        for (i = [0 : anzahl - 1])
            for (h = fuss_loecher()) {
                sx = (i - (anzahl - 1) / 2) * station_abstand + h[0];
                translate([sx, h[1], -0.1]) {
                    cylinder(d = m3_d, h = gp_t + 0.2);
                    cylinder(d = (m3_mutter_sw + spiel) / cos(30), h = m3_mutter_h + spiel + 0.1, $fn = 6);
                }
            }
        // Mischbecher vorne in der Mitte
        if (becher) {
            if (becher_modus == "aussparung") {
                translate([0, gp_vorn, -1]) cylinder(d = becher_d + 2 * spiel, h = gp_t + 2);
            } else {
                translate([0, gp_vorn - becher_d / 2 - 5, gp_t - 0.6])
                    difference() {
                        cylinder(d = becher_d + 4, h = 1);
                        translate([0, 0, -0.1]) cylinder(d = becher_d, h = 1.2);
                    }
            }
        }
    }
}

// ============================================================
// Anordnung aller Teile in Druckposition
// ============================================================
module alle_teile() {
    dx = bl_b + 12;
    reihe2 = max(mp_h, max(sh_l + 2 * fuss_l, sl_l)) + 15;
    motorhalter();
    translate([dx, 0, 0]) kolbenschlitten();
    translate([2 * dx, fuss_l, 0]) spritzenhalter();
    translate([gp_breite(stationen) / 2 - bl_b / 2, reihe2 + gp_hinten, 0])
        grundplatte(stationen);
}

// ============================================================
// Auswahl
// ============================================================
if (teil == "motorhalter") {
    motorhalter();
} else if (teil == "kolbenschlitten") {
    kolbenschlitten();
} else if (teil == "spritzenhalter") {
    spritzenhalter();
} else if (teil == "grundplatte") {
    grundplatte(stationen);
} else {
    alle_teile();
}

/*
============================================================
DRUCKHINWEISE
============================================================
Material:  PETG
Schicht:   0,2 mm
Wände:     4 Perimeter
Infill:    30 %
Stützen:   keine nötig (liegende Bohrungen sind als Tropfen modelliert,
           die Schaltnase hat eine 45-Grad-Unterseite)

Druckposition
- Motorhalter: liegt auf der Rückseite, der Motorflansch zeigt nach unten.
  Die Schalterkonsole und die Füße stehen im Druck als Rippen nach oben.
- Kolbenschlitten und Spritzenhalter: Unterseite auf dem Bett.
- Grundplatte: flach, Muttertaschen liegen unten.
- Die Grundplatte (316 x ca. 264 mm bei 5 Stationen) passt auf die meisten
  Druckbetten nicht. Entweder aus 6 mm Acryl oder Sperrholz nach dem Lochbild
  fertigen oder mit grundplatte(anzahl=1, becher=false) stationsweise drucken
  und die Segmente auf einer Schiene verschrauben.
- Wellensitze (7,8 mm) bei Bedarf mit 8-mm-Reibahle nacharbeiten, Lagersitze
  (15,2 mm) sollen die LM8UU leicht klemmend aufnehmen.

Schrauben und Kleinteile pro Station
- 4x M3x12 (ISO 4762) Motor an Motorhalter (Kopf in der Senkung)
- 4x M3x12 und 4x M3-Mutter Flanschmutter an Kolbenschlitten
  (Muttern von oben in die Schlitze schieben)
- 2x M2x10 und 2x M2-Mutter Endschalter an der Konsole (Mutter unter der Konsole)
- 6x M3x12 und 6x M3-Mutter Füße auf Grundplatte
  (2 am Motorhalter, 4 am Spritzenhalter, Muttern in den Taschen unten)
- 2x Linearwelle 8 mm, Länge siehe OpenSCAD-Konsole (ca. 165 mm)
- 2x LM8UU Lager
- 1x Trapezspindel T8 (150 mm laut Stückliste reichen, siehe Konsole)
  mit Flanschmutter, 1x Kupplung 5 auf 8 mm
- Optional: Kabelbinder um den Spritzenhalter und die Spritze gegen Herausheben

Für 5 Stationen: 20x M3x12 Motor, 20x M3x12 Mutter, 10x M2x10, 30x M3x12 Füße,
sowie 50x M3-Mutter und 10x M2-Mutter insgesamt.

Maße, die an echten Teilen nachzumessen sind
Flanschhöhe und Kolbenstangenbreite der Spritze, Spritzenlänge, Flanschdicke der
Spindelmutter, Lochkreis der Mutter, Bauhöhe des Endschalters und Lage des
Stößels, Mischbecher-Durchmesser. Nach dem ersten Druck Referenzfahrt prüfen und
die Position des Endschalters über die Langlöcher einstellen.
*/
