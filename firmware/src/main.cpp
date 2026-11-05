// Farbmischer Firmware Stand 8: sechs 60-ml-Spritzen (Platz 1..6) in einem Karussell
// mit 7 Plätzen (Platz 0 = Park), ein Stößel drückt von oben auf den Kolben, eine
// Wägezelle (HX711) wiegt den Becher. Bedienung über die Web-App aus ../web, die vom
// LittleFS ausgeliefert wird.
//
// Platz -> Spritze: 1 = W1 (Weiß 1), 2 = Y, 3 = M, 4 = C, 5 = K, 6 = W2 (Weiß 2).
// Die Web-App kennt nur C, M, Y, W, K. Bei "W" wählt die Firmware die Weiß-Spritze mit
// mehr Restmenge und wechselt bei Bedarf auf die andere.
//
// HTTP-Schnittstelle (alle Antworten JSON, CORS an):
//   GET  /status    {"state":"idle|homing|moving|dosing|error","homed":bool,
//                    "carousel_pos":int,"station":int|null,"plunger_mm":float,
//                    "weight_g":float,"fill_ml":{"W1":..,"Y":..,"M":..,"C":..,"K":..,"W2":..},
//                    "job":{"active":bool,"id":"C","target_g":float,"done_g":float,
//                           "step":int,"steps":int},"error":""}
//   POST /home      Referenzfahrt (Stößel hoch bis Mikroschalter, dann Karussell auf
//                   Hall-Park). Antwort {"ok":true}
//   POST /tare      Waage nullen (Becher steht)
//   POST /scale     {"known_g":100.0} Waage mit bekanntem Gewicht kalibrieren,
//                   Faktor in Preferences
//   POST /dispense  {"grams":{"C":1.1,"Y":4.2,"W":10.0}} Rezept dosieren (Reihenfolge:
//                   hell nach dunkel, K zuletzt). Antwort sofort {"ok":true,"job":...},
//                   die Bewegung läuft in loop(). Fehler 409, wenn nicht referenziert,
//                   Waage nicht tariert oder Spritze zu leer
//   POST /prime     {"id":"C","ml":2.0} Düse vorfüllen (ml, negativ = zurück)
//   POST /refill    {"id":"C"} setzt die Restmenge der Spritze auf voll (50 ml),
//                   nach dem Nachfüllen
//   POST /park      Karussell auf Platz 0, Stößel oben
//   POST /stop      bricht ab
//   GET  /config, POST /config  {"C":{"g_per_ml":1.32,"ml_per_mm":0.56},...} je Station
//                   (Schlüssel W1, Y, M, C, K, W2), Kalibrierung in Preferences
//   /, /farbmath.js, /mixbox.js  Web-App vom LittleFS
//
// Die Bewegungen laufen als Zustandsautomat in loop(), der Webserver blockiert nie:
// /status und /stop antworten auch während einer Bewegung. Preferences halten
// Waagenfaktor, g_per_ml und ml_per_mm je Station sowie die Restmenge je Spritze.

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <HX711.h>

#include "config.h"
#include "dosing.h"
#include "secrets.h"

// ---------------------------------------------------------------- Zustand

static Preferences prefs;
static WebServer server(80);
static HX711 scale;

struct Syringe {
  float gPerMl;
  float mlPerMm;
  float fillMl;        // Restmenge
  float contactMm;     // zuletzt bekannte Kolbenposition (mm unter Park)
  bool contactKnown;
};
static Syringe syr[N_SYRINGES];

enum State { ST_IDLE, ST_HOMING, ST_MOVING, ST_DOSING, ST_ERROR };
enum Phase {
  PH_NONE,
  PH_HOME_PL, PH_HOME_LEAVE, PH_HOME_SEEK, PH_HOME_WIDTH, PH_HOME_CENTER,
  PH_PARK_PL, PH_PARK_CAR,
  PH_PL_UP, PH_CAR, PH_SETTLE0, PH_APPROACH, PH_CONTACT, PH_SETTLE, PH_CHUNK,
  PH_PRIME_MOVE, PH_RETRACT, PH_DRIP, PH_RAISE,
  PH_ABORT_RAISE
};
static State state = ST_IDLE;
static Phase phase = PH_NONE;
static unsigned long phaseMs = 0;
static unsigned long stepStartMs = 0;
static String lastError;
static bool stopRequested = false;
static State abortTarget = ST_IDLE;  // Zustand nach PH_ABORT_RAISE

static bool plungerHomed = false;
static bool carouselHomed = false;
static bool homed() { return plungerHomed && carouselHomed; }

// ---------------------------------------------------------------- Achsen

enum Fault { FAULT_NONE, FAULT_SWITCH, FAULT_LIMIT };

struct Axis {
  Axis(int sp, int dp, bool inv, long ramp, float start)
      : stepPin(sp), dirPin(dp), invert(inv), rampLen(ramp), startSps(start) {}
  int stepPin, dirPin;
  bool invert;
  long rampLen;
  float startSps;
  long pos = 0;           // Mikroschritte (Stößel: ab Park, nach unten positiv)
  bool active = false;
  bool fwd = true;
  long remaining = 0;
  long done = 0;
  float maxSps = 0;
  unsigned long nextUs = 0;
  bool stopOnSwitch = false;  // Stößel hoch: stoppt am Mikroschalter
  bool watchSwitch = false;   // Stößel runter: Mikroschalter muss offen bleiben
  long maxPos = 0;            // 0 = keine Grenze
  bool hitSwitch = false;
  Fault fault = FAULT_NONE;
};
static Axis plunger(PIN_PLUNGER_STEP, PIN_PLUNGER_DIR, PLUNGER_DIR_INVERT,
                    PLUNGER_RAMP_STEPS, (float)PLUNGER_START_SPS);
static Axis carousel(PIN_CAROUSEL_STEP, PIN_CAROUSEL_DIR, CAROUSEL_DIR_INVERT,
                     CAROUSEL_RAMP_STEPS, (float)CAROUSEL_START_SPS);

static bool switchPressed() { return digitalRead(PIN_SWITCH_TOP) == LOW; }
static bool hallActive() { return digitalRead(PIN_HALL_PARK) == LOW; }
static void driversEnable(bool on) { digitalWrite(PIN_ENABLE, on ? LOW : HIGH); }
static bool axesActive() { return plunger.active || carousel.active; }
static int carQ() { return dosing::normalizeQ(carousel.pos); }

static void axisStart(Axis& a, long steps, bool fwd, float sps) {
  driversEnable(true);  // bleibt aktiv, damit das Karussell seine Position hält
  a.fwd = fwd;
  a.remaining = steps;
  a.done = 0;
  a.maxSps = sps;
  a.hitSwitch = false;
  a.fault = FAULT_NONE;
  digitalWrite(a.dirPin, (fwd != a.invert) ? HIGH : LOW);
  a.nextUs = micros() + 20;
  a.active = steps > 0;
}

static void axisStop(Axis& a) {
  a.active = false;
  a.remaining = 0;
}

// Ein Schritt, falls fällig. Aufruf so oft wie möglich.
static void axisService(Axis& a, bool isPlunger) {
  if (!a.active) return;
  unsigned long now = micros();
  if ((long)(now - a.nextUs) < 0) return;
  if (isPlunger) {
    if (a.stopOnSwitch && switchPressed()) {
      a.active = false;
      a.hitSwitch = true;
      a.pos = 0;
      return;
    }
    if (a.fwd) {
      if (a.watchSwitch && a.pos > dosing::mmToSteps(SWITCH_CLEAR_MM) && switchPressed()) {
        a.active = false;
        a.fault = FAULT_SWITCH;
        return;
      }
      if (a.maxPos > 0 && a.pos >= a.maxPos) {
        a.active = false;
        a.fault = FAULT_LIMIT;
        return;
      }
    }
  }
  digitalWrite(a.stepPin, HIGH);
  delayMicroseconds(3);
  digitalWrite(a.stepPin, LOW);
  a.pos += a.fwd ? 1 : -1;
  a.done++;
  a.remaining--;
  float sps = dosing::rampSps(a.done, a.remaining, a.rampLen, a.startSps, a.maxSps);
  unsigned long interval = (unsigned long)(1000000.0f / sps);
  a.nextUs += interval;
  if ((long)(now - a.nextUs) > (long)interval) a.nextUs = now + interval;  // aufgeholt
  if (a.remaining <= 0) a.active = false;
}

static void startPlungerUp() {
  long steps = dosing::mmToSteps(PLUNGER_UP_MARGIN_MM);
  if (plungerHomed) steps += (plunger.pos > 0 ? plunger.pos : 0);
  else steps += dosing::mmToSteps(PLUNGER_MAX_TRAVEL_MM);
  plunger.stopOnSwitch = true;
  plunger.watchSwitch = false;
  plunger.maxPos = 0;
  axisStart(plunger, steps, false, SPEED_PLUNGER_FAST_SPS);
}

static void startPlungerDown(long steps, float sps) {
  plunger.stopOnSwitch = false;
  plunger.watchSwitch = true;
  plunger.maxPos = dosing::mmToSteps(PLUNGER_MAX_TRAVEL_MM);
  axisStart(plunger, steps, true, sps);
}

static void startPlungerBack(long steps, float sps) {
  plunger.stopOnSwitch = false;
  plunger.watchSwitch = false;
  plunger.maxPos = 0;
  axisStart(plunger, steps, false, sps);
}

// ---------------------------------------------------------------- Waage

static const int RING = 8;
static long rawRing[RING];
static int ringCount = 0;       // gültige Werte im Ring
static int ringHead = 0;
static unsigned long sampleSeq = 0;
static unsigned long lastSampleMs = 0;
static float scaleFactor = SCALE_DEFAULT_FACTOR;
static double tareOffset = 0;
static bool tared = false;

enum TareMode { TARE_NONE, TARE_ZERO, TARE_CAL };
static TareMode tareMode = TARE_NONE;
static int tareCount = 0;
static int tareSkip = 0;
static double tareSum = 0;
static float calKnownG = 0;
static unsigned long tareStartMs = 0;

static unsigned long freshTarget = 0;
static void scaleWaitFresh() { freshTarget = sampleSeq + SCALE_SETTLE_SAMPLES + SCALE_AVG_SAMPLES; }
static bool scaleFresh() { return sampleSeq >= freshTarget; }

static double avgRaw() {
  int n = ringCount < SCALE_AVG_SAMPLES ? ringCount : SCALE_AVG_SAMPLES;
  if (n == 0) return 0;
  double s = 0;
  for (int i = 1; i <= n; i++) s += rawRing[(ringHead - i + RING) % RING];
  return s / n;
}

// Gewicht relativ zur Tara (ohne Prüfung, ob tariert wurde).
static float weightRel() { return (float)((avgRaw() - tareOffset) / scaleFactor); }
static float weightG() { return (tared && ringCount > 0) ? weightRel() : 0.0f; }

static void saveScale() {
  prefs.begin("farbmixer", false);
  prefs.putFloat("sf", scaleFactor);
  prefs.end();
}

static void finishTare() {
  double avg = tareSum / tareCount;
  if (tareMode == TARE_ZERO) {
    tareOffset = avg;
    tared = true;
  } else if (tareMode == TARE_CAL) {
    float f = (float)((avg - tareOffset) / calKnownG);
    if (fabsf(f) < 1.0f) {
      lastError = "Waagenkalibrierung fehlgeschlagen: kein Gewichtsunterschied";
    } else {
      scaleFactor = f;
      saveScale();
    }
  }
  tareMode = TARE_NONE;
}

static void beginTare(TareMode m) {
  tareMode = m;
  tareCount = 0;
  tareSkip = TARE_SKIP_SAMPLES;
  tareSum = 0;
  tareStartMs = millis();
}

// Neue Werte vom HX711 holen, nur wenn einer bereitsteht (blockiert nicht).
static void scaleService() {
  if (scale.is_ready()) {
    long raw = scale.read();
    rawRing[ringHead] = raw;
    ringHead = (ringHead + 1) % RING;
    if (ringCount < RING) ringCount++;
    sampleSeq++;
    lastSampleMs = millis();
    if (tareMode != TARE_NONE) {
      if (tareSkip > 0) tareSkip--;
      else {
        tareSum += raw;
        if (++tareCount >= TARE_SAMPLES) finishTare();
      }
    }
  }
  if (tareMode != TARE_NONE && millis() - tareStartMs > TARE_TIMEOUT_MS) {
    tareMode = TARE_NONE;
    lastError = "Waage antwortet nicht (HX711)";
  }
}

// ---------------------------------------------------------------- Kalibrierung / Restmenge

static void loadConfig() {
  prefs.begin("farbmixer", true);
  scaleFactor = prefs.getFloat("sf", SCALE_DEFAULT_FACTOR);
  for (int i = 0; i < N_SYRINGES; i++) {
    syr[i].gPerMl = prefs.getFloat((String("g") + i).c_str(), DEFAULT_G_PER_ML);
    syr[i].mlPerMm = prefs.getFloat((String("m") + i).c_str(), DEFAULT_ML_PER_MM);
    // Unbekannte Restmenge gilt als leer, bis /refill aufgerufen wurde.
    syr[i].fillMl = prefs.getFloat((String("f") + i).c_str(), 0.0f);
    syr[i].contactKnown = false;
    syr[i].contactMm = 0;
  }
  prefs.end();
}

static void saveCalibration() {
  prefs.begin("farbmixer", false);
  for (int i = 0; i < N_SYRINGES; i++) {
    prefs.putFloat((String("g") + i).c_str(), syr[i].gPerMl);
    prefs.putFloat((String("m") + i).c_str(), syr[i].mlPerMm);
  }
  prefs.end();
}

static void saveFill() {
  prefs.begin("farbmixer", false);
  for (int i = 0; i < N_SYRINGES; i++) prefs.putFloat((String("f") + i).c_str(), syr[i].fillMl);
  prefs.end();
}

static int syringeIndex(const char* id) {
  if (!id) return -1;
  for (int i = 0; i < N_SYRINGES; i++)
    if (strcmp(SYRINGE_IDS[i], id) == 0) return i;
  return -1;
}

// ---------------------------------------------------------------- Auftrag

enum JobType { JOB_NONE, JOB_DISPENSE, JOB_PRIME };
struct JobStep {
  int idx;       // Spritze
  float grams;
};
static const int MAX_STEPS = 8;
struct Job {
  JobType type = JOB_NONE;
  bool active = false;
  JobStep steps[MAX_STEPS];
  int n = 0;
  int cur = 0;
  int idx = 0;           // aktuelle Spritze
  float targetG = 0;
  float doneG = 0;
  float primeMl = 0;
};
static Job job;

// Dosierschritt (Werte des aktuellen Schritts)
static float baseG = 0;        // Gewicht vor dem Schritt
static float prevDoneG = 0;
static float expectG = 0;
static int stallCount = 0;
static float fillAtStart = 0;
static long pistonSteps = 0;   // tiefste Stößelposition (Kolbenlage)
static bool contacted = false;

static char colorOf(int idx) { return SYRINGE_IDS[idx][0]; }

static const char* stateName() {
  switch (state) {
    case ST_HOMING: return "homing";
    case ST_MOVING: return "moving";
    case ST_DOSING: return "dosing";
    case ST_ERROR: return "error";
    default: return "idle";
  }
}
static bool busy() { return state == ST_HOMING || state == ST_MOVING || state == ST_DOSING; }

// ---------------------------------------------------------------- Zustandsautomat

static void enter(Phase p);

// Rückzug gegen Nachtropfen. Vorher die Kolbenlage merken (für die nächste Kontaktschätzung).
static void beginRetract() {
  pistonSteps = plunger.pos;
  long steps = dosing::mlToSteps(RETRACT_ML, syr[job.idx].mlPerMm);
  startPlungerBack(steps > 0 ? steps : 1, SPEED_RETRACT_SPS);
}

// Restmenge nach abgebrochenem/fehlerhaftem Dosieren fortschreiben.
static void commitPartial() {
  if (job.active && job.type == JOB_DISPENSE && contacted) {
    Syringe& s = syr[job.idx];
    s.fillMl = dosing::remainingMl(fillAtStart, job.doneG > 0 ? job.doneG : 0, s.gPerMl);
    s.contactKnown = false;
    saveFill();
  }
  contacted = false;
}

// Bewegung beenden und Stößel (falls nicht oben) hochfahren, danach Zustand `after`.
static void abortAndRaise(State after) {
  axisStop(plunger);
  axisStop(carousel);
  commitPartial();
  job.active = false;
  job.type = JOB_NONE;
  if (!switchPressed() && phase != PH_HOME_PL) {
    abortTarget = after;
    state = ST_MOVING;
    phase = PH_ABORT_RAISE;
    phaseMs = millis();
    startPlungerUp();
  } else {
    state = after;
    phase = PH_NONE;
  }
}

static void fail(const String& msg, bool raise) {
  lastError = msg;
  if (raise) {
    abortAndRaise(ST_ERROR);
  } else {
    axisStop(plunger);
    axisStop(carousel);
    commitPartial();
    job.active = false;
    job.type = JOB_NONE;
    state = ST_ERROR;
    phase = PH_NONE;
  }
}

static void startStep() {
  stepStartMs = millis();
  job.idx = job.steps[job.cur].idx;
  job.targetG = job.steps[job.cur].grams;
  job.doneG = 0;
  prevDoneG = 0;
  expectG = 0;
  stallCount = 0;
  contacted = false;
  fillAtStart = syr[job.idx].fillMl;
  enter(PH_CAR);
}

static void jobFinished() {
  job.active = false;
  job.type = JOB_NONE;
  state = ST_IDLE;
  phase = PH_NONE;
}

static void finishStep() {
  Syringe& s = syr[job.idx];
  if (job.type == JOB_DISPENSE) {
    s.fillMl = dosing::remainingMl(fillAtStart, job.doneG, s.gPerMl);
    s.contactMm = dosing::stepsToMm(pistonSteps);
    s.contactKnown = true;
  } else {
    float f = fillAtStart - job.primeMl;
    s.fillMl = f < 0 ? 0 : (f > SYRINGE_FULL_ML ? SYRINGE_FULL_ML : f);
    if (job.primeMl > 0) {
      s.contactMm = dosing::stepsToMm(pistonSteps);
      s.contactKnown = true;
    } else {
      s.contactKnown = false;
    }
  }
  contacted = false;
  saveFill();
  job.cur++;
  if (job.type == JOB_DISPENSE && job.cur < job.n) startStep();
  else jobFinished();
}

static float estimateContactMm(int idx) {
  const Syringe& s = syr[idx];
  if (s.contactKnown) return s.contactMm;
  return PLUNGER_FULL_CONTACT_MM + (SYRINGE_FULL_ML - s.fillMl) / s.mlPerMm;
}

// Karussell auf Platz, nur bei oben stehendem Stößel. Gibt false bei Fehler zurück.
static bool startCarouselTo(int place) {
  if (!switchPressed()) {
    fail("Stößel-Mikroschalter unerwartet offen, Karussell gesperrt", true);
    return false;
  }
  int d = dosing::carouselDeltaSteps(carQ(), place);
  if (d != 0) axisStart(carousel, d > 0 ? d : -d, d > 0, SPEED_CAROUSEL_SPS);
  return true;
}

static void enter(Phase p) {
  phase = p;
  phaseMs = millis();
  switch (p) {
    case PH_HOME_PL:
    case PH_RAISE:
      startPlungerUp();
      break;
    case PH_HOME_LEAVE:
      if (hallActive()) axisStart(carousel, CAR_HALL_MAX_WIDTH_STEPS, true, SPEED_CAROUSEL_HOMING_SPS);
      else enter(PH_HOME_SEEK);
      break;
    case PH_HOME_SEEK:
      axisStart(carousel, dosing::CAROUSEL_STEPS_PER_REV + CAR_HALL_MAX_WIDTH_STEPS, true,
                SPEED_CAROUSEL_HOMING_SPS);
      break;
    case PH_HOME_WIDTH:
      axisStart(carousel, CAR_HALL_MAX_WIDTH_STEPS, true, SPEED_CAROUSEL_HOMING_SPS);
      break;
    case PH_HOME_CENTER: {
      long back = carousel.done / 2 - HALL_OFFSET_STEPS;
      if (back > 0) axisStart(carousel, back, false, SPEED_CAROUSEL_HOMING_SPS);
      else if (back < 0) axisStart(carousel, -back, true, SPEED_CAROUSEL_HOMING_SPS);
      break;
    }
    case PH_PARK_PL:
      if (switchPressed()) enter(PH_PARK_CAR);
      else startPlungerUp();
      break;
    case PH_PARK_CAR:
      startCarouselTo(0);
      break;
    case PH_PL_UP:
      if (switchPressed()) {
        plunger.pos = 0;
        startStep();
      } else {
        startPlungerUp();
      }
      break;
    case PH_CAR:
      if (startCarouselTo(job.idx + 1) && !carousel.active) enter(PH_SETTLE0);
      break;
    case PH_SETTLE0:
    case PH_SETTLE:
      scaleWaitFresh();
      break;
    case PH_APPROACH:
    case PH_CONTACT:
    case PH_CHUNK:
    case PH_RETRACT:
      beginRetract();
      break;
    case PH_PRIME_MOVE:
    case PH_DRIP:
    case PH_ABORT_RAISE:
    case PH_NONE:
      break;
  }
}

static void onContact() {
  contacted = true;
  scaleWaitFresh();
  enter(PH_SETTLE);
}

static void doStop() {
  if (state == ST_IDLE) return;
  if (state == ST_ERROR) {
    state = ST_IDLE;
    lastError = "";
    return;
  }
  if (phase == PH_ABORT_RAISE) return;  // Hochfahren ist sicher, weiterlaufen lassen
  if (state == ST_HOMING) {
    plungerHomed = plungerHomed && switchPressed();
    carouselHomed = false;
  }
  lastError = "abgebrochen";
  abortAndRaise(ST_IDLE);
}

static bool plungerUpPhase() {
  return phase == PH_HOME_PL || phase == PH_PARK_PL || phase == PH_PL_UP ||
         phase == PH_RAISE || phase == PH_ABORT_RAISE;
}

static void stateService() {
  if (stopRequested) {
    stopRequested = false;
    doStop();
  }
  if (state == ST_IDLE || state == ST_ERROR) return;

  // Fehler der Stößelachse (Mikroschalter unerwartet, Endlage)
  if (!plunger.active && plunger.fault != FAULT_NONE) {
    Fault f = plunger.fault;
    plunger.fault = FAULT_NONE;
    if (f == FAULT_SWITCH) {
      plungerHomed = false;  // Position stimmt nicht mehr
      fail("Stößel-Mikroschalter unerwartet geschlossen, bitte neu referenzieren", false);
    } else {
      fail("Stößel am Ende des Verfahrwegs", true);
    }
    return;
  }

  if (state == ST_DOSING && phase != PH_ABORT_RAISE && millis() - stepStartMs > DOSE_TIMEOUT_MS) {
    fail("Timeout beim Dosieren", true);
    return;
  }

  // Alle "Stößel hoch"-Phasen
  if (plungerUpPhase()) {
    if (plunger.active) return;
    if (!plunger.hitSwitch) {
      plungerHomed = false;
      if (phase == PH_ABORT_RAISE) {
        lastError += " (Stößel-Mikroschalter nicht erreicht)";
        state = ST_ERROR;
        phase = PH_NONE;
      } else {
        fail("Stößel-Mikroschalter nicht erreicht", false);
      }
      return;
    }
    plungerHomed = true;
    plunger.pos = 0;
    switch (phase) {
      case PH_HOME_PL: enter(PH_HOME_LEAVE); break;
      case PH_PARK_PL: enter(PH_PARK_CAR); break;
      case PH_PL_UP: startStep(); break;
      case PH_RAISE: finishStep(); break;
      case PH_ABORT_RAISE:
        state = abortTarget;
        phase = PH_NONE;
        break;
      default: break;
    }
    return;
  }

  switch (phase) {
    case PH_HOME_LEAVE:
      if (!hallActive()) {
        axisStop(carousel);
        enter(PH_HOME_SEEK);
      } else if (!carousel.active) {
        fail("Hall-Sensor bleibt aktiv, Magnet oder Verdrahtung prüfen", false);
      }
      break;
    case PH_HOME_SEEK:
      if (hallActive()) {
        axisStop(carousel);
        enter(PH_HOME_WIDTH);
      } else if (!carousel.active) {
        fail("Hall-Sensor Park nicht gefunden, Magnet oder Verdrahtung prüfen", false);
      }
      break;
    case PH_HOME_WIDTH:
      if (!hallActive()) {
        axisStop(carousel);
        enter(PH_HOME_CENTER);  // carousel.done = Breite des Magnetfensters
      } else if (!carousel.active) {
        fail("Hall-Fenster zu breit", false);
      }
      break;
    case PH_HOME_CENTER:
      if (!carousel.active) {
        carousel.pos = 0;
        carouselHomed = true;
        state = ST_IDLE;
        phase = PH_NONE;
      }
      break;
    case PH_PARK_CAR:
      if (!carousel.active) {
        carousel.pos = carQ();
        state = ST_IDLE;
        phase = PH_NONE;
      }
      break;
    case PH_CAR:
      if (!carousel.active) {
        carousel.pos = carQ();
        enter(PH_SETTLE0);
      }
      break;
    case PH_SETTLE0: {
      if (!scaleFresh()) {
        if (millis() - phaseMs > SCALE_TIMEOUT_MS) fail("Waage antwortet nicht (HX711)", true);
        break;
      }
      baseG = weightRel();
      float apprMm = estimateContactMm(job.idx) - APPROACH_MARGIN_MM;
      if (apprMm > PLUNGER_MAX_TRAVEL_MM) apprMm = PLUNGER_MAX_TRAVEL_MM;
      if (apprMm > 1.0f) {
        startPlungerDown(dosing::mmToSteps(apprMm), SPEED_APPROACH_SPS);
        enter(PH_APPROACH);
      } else {
        startPlungerDown(dosing::mmToSteps(CONTACT_SEARCH_MM), SPEED_CONTACT_SPS);
        enter(PH_CONTACT);
      }
      break;
    }
    case PH_APPROACH:
      if (weightRel() - baseG >= CONTACT_RISE_G) {
        axisStop(plunger);
        onContact();
      } else if (!plunger.active) {
        startPlungerDown(dosing::mmToSteps(CONTACT_SEARCH_MM), SPEED_CONTACT_SPS);
        enter(PH_CONTACT);
      }
      break;
    case PH_CONTACT:
      if (weightRel() - baseG >= CONTACT_RISE_G) {
        axisStop(plunger);
        onContact();
      } else if (!plunger.active) {
        fail(String("Kein Kolbenkontakt, Spritze ") + SYRINGE_IDS[job.idx] +
                 " leer oder Restmenge falsch (/refill)",
             true);
      }
      break;
    case PH_CHUNK:
      if (!plunger.active) {
        scaleWaitFresh();
        enter(PH_SETTLE);
      }
      break;
    case PH_SETTLE: {
      if (!scaleFresh()) {
        if (millis() - phaseMs > SCALE_TIMEOUT_MS) fail("Waage antwortet nicht (HX711)", true);
        break;
      }
      if (job.type == JOB_PRIME) {
        long steps = dosing::mlToSteps(fabsf(job.primeMl), syr[job.idx].mlPerMm);
        if (job.primeMl > 0) startPlungerDown(steps, SPEED_DOSE_FINE_SPS);
        else startPlungerBack(steps, SPEED_DOSE_FINE_SPS);
        enter(PH_PRIME_MOVE);
        break;
      }
      Syringe& s = syr[job.idx];
      float done = weightRel() - baseG;
      job.doneG = done;
      if (expectG > STALL_MIN_EXPECT_G) {
        if (done - prevDoneG < 0.25f * expectG) stallCount++;
        else stallCount = 0;
        if (stallCount >= STALL_COUNT) {
          fail(String("Keine Gewichtszunahme, Spritze ") + SYRINGE_IDS[job.idx] +
                   " leer oder Düse verstopft",
               true);
          break;
        }
      }
      prevDoneG = done;
      float coarseFlow = dosing::flowGps(SPEED_DOSE_COARSE_SPS, s.mlPerMm, s.gPerMl);
      float brake = dosing::brakePointG(job.targetG, coarseFlow, BRAKE_LATENCY_S, BRAKE_MIN_MARGIN_G);
      dosing::Chunk c = dosing::nextChunk(done, job.targetG, s.gPerMl, brake, DOSE_COARSE_CHUNK_G,
                                          DOSE_FINE_CHUNK_G, DOSE_MIN_CHUNK_G, DOSE_STOP_MARGIN_G);
      if (c.ml <= 0) {
        enter(PH_RETRACT);
        break;
      }
      float fillNow = fillAtStart - done / s.gPerMl;
      if (fillNow - c.ml < -EMPTY_TOLERANCE_ML) {
        fail(String("Spritze ") + SYRINGE_IDS[job.idx] + " leer, bitte nachfüllen", true);
        break;
      }
      expectG = c.ml * s.gPerMl;
      long steps = dosing::mlToSteps(c.ml, s.mlPerMm);
      if (steps < 1) steps = 1;
      startPlungerDown(steps, c.fine ? SPEED_DOSE_FINE_SPS : SPEED_DOSE_COARSE_SPS);
      enter(PH_CHUNK);
      break;
    }
    case PH_PRIME_MOVE:
      if (!plunger.active) {
        pistonSteps = plunger.pos;
        enter(PH_RAISE);
      }
      break;
    case PH_RETRACT:
      if (!plunger.active) {
        scaleWaitFresh();
        enter(PH_DRIP);
      }
      break;
    case PH_DRIP:
      if (millis() - phaseMs >= DRIP_WAIT_MS && scaleFresh()) {
        job.doneG = weightRel() - baseG;
        enter(PH_RAISE);
      } else if (millis() - phaseMs > SCALE_TIMEOUT_MS + DRIP_WAIT_MS) {
        fail("Waage antwortet nicht (HX711)", true);
      }
      break;
    default:
      break;
  }
}

// ---------------------------------------------------------------- HTTP

static void sendJson(int code, JsonDocument& doc) {
  String out;
  serializeJson(doc, out);
  server.send(code, "application/json", out);
}

static void sendError(int code, const String& msg) {
  JsonDocument doc;
  doc["error"] = msg;
  sendJson(code, doc);
}

static void sendOk() {
  JsonDocument doc;
  doc["ok"] = true;
  sendJson(200, doc);
}

static float r2(float v) { return roundf(v * 100.0f) / 100.0f; }

static void fillJobJson(JsonObject o) {
  o["active"] = job.active;
  int show = job.cur < job.n ? job.cur : job.n - 1;
  o["id"] = show >= 0 ? String(colorOf(job.steps[show].idx)) : String("");
  o["target_g"] = r2(job.targetG);
  o["done_g"] = r2(job.doneG);
  o["step"] = job.active ? job.cur + 1 : job.cur;
  o["steps"] = job.n;
}

static void handleStatus() {
  JsonDocument doc;
  doc["state"] = stateName();
  doc["homed"] = homed();
  doc["carousel_pos"] = carQ();
  int place = (carouselHomed && !carousel.active) ? dosing::placeAtQ(carQ()) : -1;
  if (place >= 0) doc["station"] = place;
  else doc["station"] = nullptr;
  doc["plunger_mm"] = r2(dosing::stepsToMm(plunger.pos));
  doc["weight_g"] = r2(weightG());
  JsonObject fill = doc["fill_ml"].to<JsonObject>();
  for (int i = 0; i < N_SYRINGES; i++) fill[SYRINGE_IDS[i]] = r2(syr[i].fillMl);
  fillJobJson(doc["job"].to<JsonObject>());
  doc["error"] = lastError;
  sendJson(200, doc);
}

static bool parseBody(JsonDocument& doc) {
  if (!server.hasArg("plain")) return true;  // leerer Body ist erlaubt
  DeserializationError err = deserializeJson(doc, server.arg("plain"));
  if (err) {
    sendError(400, String("JSON ungültig: ") + err.c_str());
    return false;
  }
  return true;
}

// Fehlerzustand wird mit dem nächsten Befehl quittiert.
static void clearErrorForNewCommand() {
  if (state == ST_ERROR) state = ST_IDLE;
  lastError = "";
}

static bool rejectIfBusy() {
  if (busy()) { sendError(409, "Gerät ist beschäftigt"); return true; }
  if (tareMode != TARE_NONE) { sendError(409, "Waage arbeitet noch (Tara oder Kalibrierung)"); return true; }
  return false;
}

static void handleHome() {
  if (rejectIfBusy()) return;
  clearErrorForNewCommand();
  plungerHomed = false;
  carouselHomed = false;
  state = ST_HOMING;
  enter(PH_HOME_PL);
  sendOk();
}

static void handlePark() {
  if (rejectIfBusy()) return;
  if (!homed()) { sendError(409, "Nicht referenziert, zuerst /home"); return; }
  clearErrorForNewCommand();
  state = ST_MOVING;
  enter(PH_PARK_PL);
  sendOk();
}

static void handleStop() {
  stopRequested = true;
  sendOk();
}

static void handleTare() {
  if (rejectIfBusy()) return;
  clearErrorForNewCommand();
  beginTare(TARE_ZERO);
  sendOk();
}

static void handleScale() {
  if (rejectIfBusy()) return;
  JsonDocument doc;
  if (!parseBody(doc)) return;
  float known = doc["known_g"] | 0.0f;
  if (known < 1.0f || known > 5000.0f) { sendError(400, "known_g fehlt oder außerhalb 1 bis 5000"); return; }
  if (!tared) { sendError(409, "Waage nicht tariert, zuerst /tare (leer), dann Gewicht auflegen"); return; }
  clearErrorForNewCommand();
  calKnownG = known;
  beginTare(TARE_CAL);
  sendOk();
}

static void handleDispense() {
  if (rejectIfBusy()) return;
  JsonDocument doc;
  if (!parseBody(doc)) return;
  JsonObject grams = doc["grams"].as<JsonObject>();
  if (grams.isNull()) { sendError(400, "Feld grams fehlt"); return; }

  // Hell nach dunkel, K zuletzt.
  static const char* const ORDER[5] = {"W", "Y", "C", "M", "K"};
  float want[5] = {0, 0, 0, 0, 0};
  for (JsonPair kv : grams) {
    const char* key = kv.key().c_str();
    int o = -1;
    for (int k = 0; k < 5; k++) if (strcmp(ORDER[k], key) == 0) o = k;
    if (o < 0) { sendError(400, String("Unbekannte Farbe ") + key + " (erlaubt: C, M, Y, W, K)"); return; }
    float g = kv.value().as<float>();
    if (g < 0 || g > 200) { sendError(400, "Menge außerhalb 0 bis 200 g"); return; }
    want[o] = g;
  }

  if (!homed()) { sendError(409, "Nicht referenziert, zuerst /home"); return; }
  if (!tared) { sendError(409, "Waage nicht tariert, zuerst /tare"); return; }

  Job j;
  j.type = JOB_DISPENSE;
  for (int o = 0; o < 5; o++) {
    float g = want[o];
    if (g < MIN_DOSE_G) continue;
    if (o == 0) {  // Weiß: Spritze mit mehr Rest, bei Bedarf Aufteilung auf beide
      dosing::WhitePlan wp = dosing::planWhite(g, syr[IDX_W1].fillMl, syr[IDX_W1].gPerMl,
                                               syr[IDX_W2].fillMl, syr[IDX_W2].gPerMl,
                                               EMPTY_RESERVE_ML, MIN_DOSE_G);
      if (wp.n == 0) { sendError(409, "Weiß-Spritzen zu leer, bitte nachfüllen (/refill)"); return; }
      for (int k = 0; k < wp.n; k++) {
        j.steps[j.n].idx = wp.idx[k] == 0 ? IDX_W1 : IDX_W2;
        j.steps[j.n].grams = wp.grams[k];
        j.n++;
      }
    } else {
      int idx = syringeIndex(ORDER[o]);
      if (!dosing::canDose(syr[idx].fillMl, g, syr[idx].gPerMl, EMPTY_RESERVE_ML)) {
        sendError(409, String("Spritze ") + ORDER[o] + " zu leer, bitte nachfüllen (/refill)");
        return;
      }
      j.steps[j.n].idx = idx;
      j.steps[j.n].grams = g;
      j.n++;
    }
  }
  if (j.n == 0) { sendError(400, "Rezept ist leer"); return; }

  clearErrorForNewCommand();
  j.active = true;
  j.cur = 0;
  job = j;
  state = ST_DOSING;
  enter(PH_PL_UP);

  JsonDocument out;
  out["ok"] = true;
  fillJobJson(out["job"].to<JsonObject>());
  sendJson(200, out);
}

static void handlePrime() {
  if (rejectIfBusy()) return;
  JsonDocument doc;
  if (!parseBody(doc)) return;
  const char* id = doc["id"] | "";
  int idx = syringeIndex(id);
  if (idx < 0) { sendError(400, "Feld id fehlt oder unbekannt (W1, Y, M, C, K, W2)"); return; }
  float ml = doc["ml"] | 1.0f;
  if (fabsf(ml) > 30 || fabsf(ml) < 0.01f) { sendError(400, "ml zwischen 0,01 und 30 (negativ = zurück)"); return; }
  if (!homed()) { sendError(409, "Nicht referenziert, zuerst /home"); return; }
  if (ml > 0 && syr[idx].fillMl - EMPTY_RESERVE_ML < ml) {
    sendError(409, String("Spritze ") + id + " zu leer, bitte nachfüllen (/refill)");
    return;
  }
  if (ml < 0 && syr[idx].fillMl - ml > SYRINGE_FULL_ML) { sendError(409, "Spritze ist voll"); return; }
  clearErrorForNewCommand();
  Job j;
  j.type = JOB_PRIME;
  j.active = true;
  j.n = 1;
  j.steps[0].idx = idx;
  j.steps[0].grams = 0;
  j.primeMl = ml;
  job = j;
  state = ST_DOSING;
  // Kontaktsuche läuft über die Gewichtsänderung, Tara ist dafür nicht nötig.
  enter(PH_PL_UP);
  sendOk();
}

static void handleRefill() {
  if (rejectIfBusy()) return;
  JsonDocument doc;
  if (!parseBody(doc)) return;
  const char* id = doc["id"] | "";
  int idx = syringeIndex(id);
  if (idx < 0) { sendError(400, "Feld id fehlt oder unbekannt (W1, Y, M, C, K, W2)"); return; }
  syr[idx].fillMl = SYRINGE_FULL_ML;
  syr[idx].contactKnown = false;
  saveFill();
  sendOk();
}

static void handleConfigGet() {
  JsonDocument doc;
  for (int i = 0; i < N_SYRINGES; i++) {
    JsonObject o = doc[SYRINGE_IDS[i]].to<JsonObject>();
    o["g_per_ml"] = syr[i].gPerMl;
    o["ml_per_mm"] = syr[i].mlPerMm;
  }
  sendJson(200, doc);
}

static void handleConfigPost() {
  if (rejectIfBusy()) return;
  JsonDocument doc;
  if (!parseBody(doc)) return;
  // Erst prüfen, dann übernehmen.
  for (JsonPair kv : doc.as<JsonObject>()) {
    int i = syringeIndex(kv.key().c_str());
    if (i < 0) { sendError(400, String("Unbekannte Station ") + kv.key().c_str()); return; }
    JsonObject o = kv.value().as<JsonObject>();
    if (o["g_per_ml"].is<float>()) {
      float v = o["g_per_ml"];
      if (v < 0.5f || v > 3.0f) { sendError(400, "g_per_ml außerhalb 0,5 bis 3"); return; }
    }
    if (o["ml_per_mm"].is<float>()) {
      float v = o["ml_per_mm"];
      if (v < 0.1f || v > 2.0f) { sendError(400, "ml_per_mm außerhalb 0,1 bis 2"); return; }
    }
  }
  for (JsonPair kv : doc.as<JsonObject>()) {
    int i = syringeIndex(kv.key().c_str());
    JsonObject o = kv.value().as<JsonObject>();
    if (o["g_per_ml"].is<float>()) syr[i].gPerMl = o["g_per_ml"];
    if (o["ml_per_mm"].is<float>()) {
      syr[i].mlPerMm = o["ml_per_mm"];
      syr[i].contactKnown = false;
    }
  }
  saveCalibration();
  handleConfigGet();
}

static void handleRoot() {
  File f = LittleFS.open("/index.html", "r");
  if (!f) { server.send(500, "text/plain", "index.html fehlt, uploadfs ausführen"); return; }
  server.streamFile(f, "text/html");
  f.close();
}

static void handleNotFound() {
  if (server.method() == HTTP_OPTIONS) { server.send(204); return; }
  sendError(404, "nicht gefunden");
}

// ---------------------------------------------------------------- Setup / loop

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENABLE, OUTPUT);
  driversEnable(false);
  pinMode(PIN_PLUNGER_STEP, OUTPUT);
  pinMode(PIN_PLUNGER_DIR, OUTPUT);
  pinMode(PIN_CAROUSEL_STEP, OUTPUT);
  pinMode(PIN_CAROUSEL_DIR, OUTPUT);
  digitalWrite(PIN_PLUNGER_STEP, LOW);
  digitalWrite(PIN_CAROUSEL_STEP, LOW);
  pinMode(PIN_SWITCH_TOP, INPUT_PULLUP);
  pinMode(PIN_HALL_PARK, INPUT_PULLUP);
  loadConfig();
  scale.begin(PIN_HX711_DOUT, PIN_HX711_SCK);

  if (!LittleFS.begin(true)) Serial.println("LittleFS konnte nicht gestartet werden");

  WiFi.mode(WIFI_STA);
  WiFi.setHostname(MDNS_NAME);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("WLAN");
  for (int i = 0; i < 60 && WiFi.status() != WL_CONNECTED; i++) { delay(500); Serial.print('.'); }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("IP: "); Serial.println(WiFi.localIP());
    if (MDNS.begin(MDNS_NAME)) {
      MDNS.addService("http", "tcp", 80);
      Serial.println("Erreichbar unter http://" MDNS_NAME ".local");
    }
  } else {
    Serial.println("Kein WLAN, starte Access Point Farbmixer");
    WiFi.mode(WIFI_AP);
    WiFi.softAP("Farbmixer");
    Serial.print("IP: "); Serial.println(WiFi.softAPIP());
  }

  server.enableCORS(true);
  server.on("/", HTTP_GET, handleRoot);
  server.serveStatic("/farbmath.js", LittleFS, "/farbmath.js", "max-age=3600");
  server.serveStatic("/mixbox.js", LittleFS, "/mixbox.js", "max-age=86400");
  server.on("/status", HTTP_GET, handleStatus);
  server.on("/home", HTTP_POST, handleHome);
  server.on("/tare", HTTP_POST, handleTare);
  server.on("/scale", HTTP_POST, handleScale);
  server.on("/dispense", HTTP_POST, handleDispense);
  server.on("/prime", HTTP_POST, handlePrime);
  server.on("/refill", HTTP_POST, handleRefill);
  server.on("/park", HTTP_POST, handlePark);
  server.on("/stop", HTTP_POST, handleStop);
  server.on("/config", HTTP_GET, handleConfigGet);
  server.on("/config", HTTP_POST, handleConfigPost);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("Webserver läuft");
}

void loop() {
  // Schritte in kurzen Blöcken erzeugen, dazwischen Waage, Zustandsautomat und Webserver.
  unsigned long t0 = micros();
  do {
    axisService(plunger, true);
    axisService(carousel, false);
  } while (axesActive() && micros() - t0 < 1500);
  scaleService();
  stateService();
  server.handleClient();
  if (!axesActive()) delay(1);
}
