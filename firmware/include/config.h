// Pinbelegung und Standardwerte des Farbmischers.
// Reihenfolge der Stationen: C, M, Y, W, K (wie in der Web-App).
#pragma once

#define N_STATIONS 5
static const char STATION_IDS[N_STATIONS] = {'C', 'M', 'Y', 'W', 'K'};

// Schrittmotortreiber (TMC2208 / A4988), ein gemeinsamer Enable-Pin.
static const int PIN_STEP[N_STATIONS] = {13, 14, 27, 26, 25};
static const int PIN_DIR[N_STATIONS]  = {33, 32, 4, 16, 17};
static const int PIN_ENABLE = 23;  // LOW = Treiber aktiv

// Endschalter, Schließer gegen GND, interner Pullup.
// Gedrückt = Kolbenschlitten ganz oben (Spritze voll aufgezogen).
// GPIO 34 ist nur Eingang ohne internen Pullup, auf der Trägerplatine
// sitzt dafür ein 10-kOhm-Pullup nach 3,3 V. (GPIO 15 fehlt auf dem
// 30-poligen DevKit V1.)
static const int PIN_ENDSTOP[N_STATIONS] = {18, 19, 21, 22, 34};

// Drehrichtung pro Station umkehren, falls der Motor falsch herum läuft.
static const bool DIR_INVERT[N_STATIONS] = {false, false, false, false, false};

// Mechanik: T8-Spindel mit 2 mm Steigung, 200 Vollschritte, 1/16 Mikroschritt.
#define STEPS_PER_MM 1600.0f
// 60-ml-Spritze, Innendurchmesser 26,7 mm -> 0,56 ml pro mm Kolbenweg.
#define DEFAULT_ML_PER_MM 0.56f
// Dichte Acrylfarbe, wird pro Station per /config durch Auswiegen ersetzt.
#define DEFAULT_G_PER_ML 1.3f
// Maximaler Kolbenweg ab Endschalter.
#define MAX_TRAVEL_MM 105.0f
// Rückzug nach jeder Dosierung gegen Nachtropfen, wird beim nächsten Hub
// wieder vorgefahren.
#define RETRACT_ML 0.05f

// Geschwindigkeit in Schritten pro Sekunde. Acryl ist zäh, lieber langsam.
#define SPEED_MAX_SPS 2500
#define SPEED_START_SPS 600
#define ACCEL_STEPS 400   // Rampe in Schritten
#define HOMING_SPS 1500

// Kleinste dosierbare Menge in Gramm.
#define MIN_DOSE_G 0.1f

// LED-Ring WS2812 unter der Haube, zeigt die Zielfarbe beim Dosieren.
#define PIN_LED_RING 5
#define LED_COUNT 12
#define LED_BRIGHTNESS 80  // 0 bis 255

#define MDNS_NAME "farbmixer"
