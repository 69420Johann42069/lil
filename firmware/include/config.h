// Pinbelegung und Standardwerte des Farbmischers (Stand 8).
// Sechs Spritzen in einem Karussell mit 7 Plätzen (Platz 0 = Park), ein Stößel
// drückt von oben auf den Kolben, eine Wägezelle (HX711) wiegt den Becher.
#pragma once

// ---------------------------------------------------------------- Stationen
// Platz p = 1..6 gehört zur Spritze mit Index p-1: W1, Y, M, C, K, W2.
// Die Web-App kennt nur C, M, Y, W, K; "W" wählt die Firmware aus W1/W2.
#define N_SYRINGES 6
static const char* const SYRINGE_IDS[N_SYRINGES] = {"W1", "Y", "M", "C", "K", "W2"};
#define IDX_W1 0
#define IDX_W2 5

// ---------------------------------------------------------------- Pins (ESP32 DevKit 30 Pin)
#define PIN_PLUNGER_STEP 13
#define PIN_PLUNGER_DIR 14
#define PIN_CAROUSEL_STEP 27
#define PIN_CAROUSEL_DIR 26
#define PIN_ENABLE 23        // ENABLE beider A4988, LOW = aktiv
#define PIN_SWITCH_TOP 18    // Mikroschalter Stößel oben, Schließer gegen GND, INPUT_PULLUP, LOW = oben
#define PIN_HALL_PARK 19     // Hall-Sensor A3144 (Open-Collector), INPUT_PULLUP, LOW = Magnet = Platz 0
#define PIN_HX711_DOUT 32
#define PIN_HX711_SCK 33

// Drehrichtung umkehren, falls ein Motor falsch herum läuft.
// Stößel: vorwärts = nach unten (auf den Kolben), Karussell: vorwärts = Platznummer steigt.
#define PLUNGER_DIR_INVERT false
#define CAROUSEL_DIR_INVERT false

// ---------------------------------------------------------------- Mechanik
// Stößel 1600 Mikroschritte je mm, Karussell 3200 je Umdrehung: siehe dosing.h.
// 60-ml-Spritze, Innendurchmesser 26,7 mm -> 0,5599 ml pro mm Kolbenweg (Nutzhub 89,3 mm = 50 ml).
#define DEFAULT_ML_PER_MM 0.5599f
// Dichte Acrylfarbe, wird je Station per /config durch Auswiegen ersetzt.
#define DEFAULT_G_PER_ML 1.3f
#define SYRINGE_FULL_ML 50.0f

// Stößelweg ab Mikroschalter (Position 0 = Park).
#define PLUNGER_MAX_TRAVEL_MM 150.0f      // harte Grenze nach unten
#define PLUNGER_UP_MARGIN_MM 10.0f        // Zugabe beim Hochfahren über die bekannte Position
#define SWITCH_CLEAR_MM 2.0f              // ab hier muss der Mikroschalter offen sein
// Abstand Park -> Kolben bei voller Spritze (am Gerät ausmessen).
#define PLUNGER_FULL_CONTACT_MM 25.0f
#define APPROACH_MARGIN_MM 6.0f           // schnelle Anfahrt endet so weit vor dem erwarteten Kontakt
#define CONTACT_SEARCH_MM 20.0f           // langsame Kontaktsuche, danach Fehler

// Hall-Sensor Platz 0: Magnetfenster bei der Referenzfahrt.
#define CAR_HALL_MAX_WIDTH_STEPS 800      // breiter darf das Fenster nicht sein
#define HALL_OFFSET_STEPS 0               // Platz 0 gegenüber der Fenstermitte (vorwärts positiv)

// ---------------------------------------------------------------- Geschwindigkeiten (Schritte/s)
#define PLUNGER_START_SPS 500
#define PLUNGER_RAMP_STEPS 400
#define SPEED_PLUNGER_FAST_SPS 5000       // hoch fahren, Referenzfahrt
#define SPEED_APPROACH_SPS 3000           // Anfahrt zum Kolben
#define SPEED_CONTACT_SPS 500             // Kontaktsuche (0,3 mm/s)
#define SPEED_DOSE_COARSE_SPS 3000
#define SPEED_DOSE_FINE_SPS 700
#define SPEED_RETRACT_SPS 1000

#define CAROUSEL_START_SPS 300
#define CAROUSEL_RAMP_STEPS 300
#define SPEED_CAROUSEL_SPS 1500
#define SPEED_CAROUSEL_HOMING_SPS 400

// ---------------------------------------------------------------- Dosieren nach Gewicht
#define MIN_DOSE_G 0.1f                   // kleinste Menge je Farbe, zugleich Toleranz
#define DOSE_STOP_MARGIN_G 0.05f          // fertig, wenn der Rest darunter liegt
#define DOSE_COARSE_CHUNK_G 3.0f          // größter Schritt vor dem Bremspunkt
#define DOSE_FINE_CHUNK_G 0.3f            // größter Schritt nach dem Bremspunkt
#define DOSE_MIN_CHUNK_G 0.03f
#define BRAKE_LATENCY_S 0.6f              // Verzögerung der Waage für den Bremspunkt
#define BRAKE_MIN_MARGIN_G 0.5f
#define CONTACT_RISE_G 0.06f              // Gewichtsanstieg = Kolbenkontakt
#define RETRACT_ML 0.05f                  // Rückzug gegen Nachtropfen
#define DRIP_WAIT_MS 500
#define EMPTY_RESERVE_ML 1.0f             // bleibt in der Spritze, sonst gilt sie als leer
#define EMPTY_TOLERANCE_ML 0.5f
#define DOSE_TIMEOUT_MS 240000UL          // je Farbe
#define STALL_MIN_EXPECT_G 0.15f          // ab diesem Sollzuwachs wird auf Stillstand geprüft
#define STALL_COUNT 3

// ---------------------------------------------------------------- Waage (HX711)
#define SCALE_DEFAULT_FACTOR 420.0f       // Zählwerte je Gramm, per /scale kalibrieren
#define SCALE_AVG_SAMPLES 3               // gleitender Mittelwert
#define SCALE_SETTLE_SAMPLES 3            // verworfene Werte nach einer Bewegung
#define SCALE_TIMEOUT_MS 3000UL           // keine neuen Werte -> Fehler
#define TARE_SAMPLES 10
#define TARE_SKIP_SAMPLES 2
#define TARE_TIMEOUT_MS 8000UL

#define MDNS_NAME "farbmixer"
