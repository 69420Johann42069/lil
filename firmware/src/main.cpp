// Farbmischer Firmware: fünf Spritzenpumpen am ESP32, Bedienung über die
// Web-App aus ../web, die vom LittleFS ausgeliefert wird.
//
// HTTP-Schnittstelle (alle Antworten JSON):
//   GET  /status                     Zustand, Position, Fehler
//   POST /dispense  {"grams":{"C":1.1,"Y":4.2,...}}   Rezept dosieren
//   POST /home      {"id":"C"} oder leer für alle    Referenzfahrt
//   POST /prime     {"id":"C","ml":2.0}               Vorfüllen (ml, negativ = zurück)
//   GET  /config                     Kalibrierung pro Station
//   POST /config    {"C":{"g_per_ml":1.32,"ml_per_mm":0.56},...}
//   POST /stop                       laufenden Auftrag abbrechen
//
// Die Bewegungen laufen in loop(), damit der Webserver nicht blockiert.

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <LittleFS.h>
#include <Preferences.h>
#include <ArduinoJson.h>

#include "config.h"
#include "secrets.h"

// ---------------------------------------------------------------- Stationen

struct Station {
  char id;
  int stepPin, dirPin, endPin;
  bool invert;
  float gPerMl;
  float mlPerMm;
  long posSteps;        // 0 = am Endschalter (Kolben aufgezogen)
  long retractedSteps;  // zuletzt zurückgezogen, beim nächsten Hub vorgefahren
  bool homed;
};

static Station stations[N_STATIONS];
static Preferences prefs;
static WebServer server(80);

static volatile bool stopRequested = false;
static String lastError;

static int stationIndex(char id) {
  for (int i = 0; i < N_STATIONS; i++) if (stations[i].id == id) return i;
  return -1;
}

static float stepsPerMl(const Station& s) { return STEPS_PER_MM / s.mlPerMm; }
static long maxTravelSteps() { return (long)(MAX_TRAVEL_MM * STEPS_PER_MM); }

static void loadConfig() {
  prefs.begin("farbmixer", true);
  for (int i = 0; i < N_STATIONS; i++) {
    String k = String("g") + i;
    stations[i].gPerMl = prefs.getFloat(k.c_str(), DEFAULT_G_PER_ML);
    k = String("m") + i;
    stations[i].mlPerMm = prefs.getFloat(k.c_str(), DEFAULT_ML_PER_MM);
  }
  prefs.end();
}

static void saveConfig() {
  prefs.begin("farbmixer", false);
  for (int i = 0; i < N_STATIONS; i++) {
    String k = String("g") + i;
    prefs.putFloat(k.c_str(), stations[i].gPerMl);
    k = String("m") + i;
    prefs.putFloat(k.c_str(), stations[i].mlPerMm);
  }
  prefs.end();
}

// ---------------------------------------------------------------- Motorik

static void driversEnable(bool on) { digitalWrite(PIN_ENABLE, on ? LOW : HIGH); }

static bool endstopPressed(const Station& s) { return digitalRead(s.endPin) == LOW; }

// Blockierende Bewegung mit linearer Rampe. forward = Kolben drücken.
// Gibt die tatsächlich gefahrenen Schritte zurück (weniger bei Stop oder
// Endschalter in Rückwärtsrichtung).
static long moveSteps(Station& s, long steps, bool forward) {
  if (steps <= 0) return 0;
  digitalWrite(s.dirPin, (forward != s.invert) ? HIGH : LOW);
  delayMicroseconds(5);
  long done = 0;
  for (long i = 0; i < steps; i++) {
    if (stopRequested) break;
    if (!forward && endstopPressed(s)) break;
    long rampLen = min((long)ACCEL_STEPS, steps / 2);
    float sps;
    if (i < rampLen)
      sps = SPEED_START_SPS + (SPEED_MAX_SPS - SPEED_START_SPS) * (float)i / rampLen;
    else if (steps - i < rampLen)
      sps = SPEED_START_SPS + (SPEED_MAX_SPS - SPEED_START_SPS) * (float)(steps - i) / rampLen;
    else
      sps = SPEED_MAX_SPS;
    unsigned long interval = (unsigned long)(1000000.0f / sps);
    digitalWrite(s.stepPin, HIGH);
    delayMicroseconds(3);
    digitalWrite(s.stepPin, LOW);
    delayMicroseconds(interval > 3 ? interval - 3 : 1);
    done++;
    // Webserver zwischendurch bedienen, damit /stop und /status erreichbar
    // bleiben. Die kurze Pause alle 256 Schritte stört die Dosierung nicht.
    if ((i & 0xff) == 0) server.handleClient();
  }
  s.posSteps += forward ? done : -done;
  return done;
}

static bool homeStation(Station& s) {
  driversEnable(true);
  // Zurückfahren bis Endschalter, maximal etwas mehr als der Gesamtweg.
  digitalWrite(s.dirPin, (false != s.invert) ? HIGH : LOW);
  unsigned long interval = 1000000UL / HOMING_SPS;
  long limit = maxTravelSteps() + (long)(5 * STEPS_PER_MM);
  long i = 0;
  while (!endstopPressed(s) && i < limit && !stopRequested) {
    digitalWrite(s.stepPin, HIGH);
    delayMicroseconds(3);
    digitalWrite(s.stepPin, LOW);
    delayMicroseconds(interval - 3);
    i++;
    if ((i & 0xff) == 0) server.handleClient();
  }
  if (!endstopPressed(s)) {
    s.homed = false;
    lastError = String("Endschalter ") + s.id + " nicht erreicht";
    return false;
  }
  s.posSteps = 0;
  s.retractedSteps = 0;
  // Ein Stück vorfahren, damit der Schalter frei ist.
  moveSteps(s, (long)(1.0f * STEPS_PER_MM), true);
  s.homed = true;
  return true;
}

// Dosiert `grams` aus Station s. Vorher wird der letzte Rückzug kompensiert,
// danach wieder ein Stück zurückgezogen.
static bool dispenseGrams(Station& s, float grams) {
  if (!s.homed) { lastError = String("Station ") + s.id + " nicht referenziert"; return false; }
  long steps = lroundf(grams / s.gPerMl * stepsPerMl(s));
  long retract = lroundf(RETRACT_ML * stepsPerMl(s));
  long total = steps + s.retractedSteps;
  if (s.posSteps + total > maxTravelSteps()) {
    lastError = String("Spritze ") + s.id + " leer, bitte nachfüllen";
    return false;
  }
  driversEnable(true);
  long done = moveSteps(s, total, true);
  s.retractedSteps = 0;
  if (done < total) { lastError = "abgebrochen"; return false; }
  delay(150);  // Nachlauf abwarten
  moveSteps(s, retract, false);
  s.retractedSteps = retract;
  return true;
}

// ---------------------------------------------------------------- Aufträge

enum JobType { JOB_NONE, JOB_DISPENSE, JOB_HOME, JOB_PRIME };
struct Job {
  JobType type = JOB_NONE;
  float grams[N_STATIONS] = {0};
  int stationMask = 0;  // für HOME: Bitmaske, für PRIME: Index in primeIdx
  int primeIdx = -1;
  float primeMl = 0;
};
static Job job;
static bool busy = false;
static char currentStation = '-';

// Helle Farben zuerst, dunkle zuletzt: W, Y, C, M, K.
static const char DISPENSE_ORDER[N_STATIONS] = {'W', 'Y', 'C', 'M', 'K'};

static void runJob() {
  busy = true;
  lastError = "";
  stopRequested = false;
  bool ok = true;
  switch (job.type) {
    case JOB_DISPENSE:
      for (int o = 0; o < N_STATIONS && ok; o++) {
        int i = stationIndex(DISPENSE_ORDER[o]);
        if (i < 0 || job.grams[i] < MIN_DOSE_G) continue;
        currentStation = stations[i].id;
        ok = dispenseGrams(stations[i], job.grams[i]);
      }
      break;
    case JOB_HOME:
      for (int i = 0; i < N_STATIONS && ok; i++) {
        if (!(job.stationMask & (1 << i))) continue;
        currentStation = stations[i].id;
        ok = homeStation(stations[i]);
      }
      break;
    case JOB_PRIME: {
      Station& s = stations[job.primeIdx];
      currentStation = s.id;
      driversEnable(true);
      long steps = lroundf(fabsf(job.primeMl) * stepsPerMl(s));
      bool fwd = job.primeMl > 0;
      if (fwd && s.homed && s.posSteps + steps > maxTravelSteps()) {
        lastError = "Weg zu lang"; ok = false;
      } else {
        moveSteps(s, steps, fwd);
        s.retractedSteps = 0;
      }
      break;
    }
    default: break;
  }
  driversEnable(false);
  currentStation = '-';
  job.type = JOB_NONE;
  busy = false;
  if (!ok && lastError.length() == 0) lastError = "Fehler";
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

static void handleStatus() {
  JsonDocument doc;
  doc["busy"] = busy;
  doc["station"] = String(currentStation);
  doc["error"] = lastError;
  JsonObject st = doc["stations"].to<JsonObject>();
  for (int i = 0; i < N_STATIONS; i++) {
    JsonObject o = st[String(stations[i].id)].to<JsonObject>();
    o["homed"] = stations[i].homed;
    o["pos_mm"] = stations[i].posSteps / STEPS_PER_MM;
    o["remaining_ml"] = (maxTravelSteps() - stations[i].posSteps) / stepsPerMl(stations[i]);
    o["endstop"] = endstopPressed(stations[i]);
  }
  sendJson(200, doc);
}

static bool parseBody(JsonDocument& doc) {
  if (!server.hasArg("plain")) return true;  // leerer Body ist erlaubt
  DeserializationError err = deserializeJson(doc, server.arg("plain"));
  if (err) { sendError(400, String("JSON ungültig: ") + err.c_str()); return false; }
  return true;
}

static void handleDispense() {
  if (busy) { sendError(409, "Gerät ist beschäftigt"); return; }
  JsonDocument doc;
  if (!parseBody(doc)) return;
  JsonObject grams = doc["grams"].as<JsonObject>();
  if (grams.isNull()) { sendError(400, "Feld grams fehlt"); return; }
  Job j;
  j.type = JOB_DISPENSE;
  float sum = 0;
  for (JsonPair kv : grams) {
    const char* key = kv.key().c_str();
    int i = key[0] ? stationIndex(key[0]) : -1;
    if (i < 0 || key[1] != 0) { sendError(400, String("Unbekannte Station ") + key); return; }
    float g = kv.value().as<float>();
    if (g < 0 || g > 200) { sendError(400, "Menge außerhalb 0 bis 200 g"); return; }
    j.grams[i] = g;
    sum += g;
  }
  if (sum < MIN_DOSE_G) { sendError(400, "Rezept ist leer"); return; }
  for (int i = 0; i < N_STATIONS; i++) {
    if (j.grams[i] >= MIN_DOSE_G && !stations[i].homed) {
      sendError(409, String("Station ") + stations[i].id + " zuerst referenzieren (/home)");
      return;
    }
  }
  job = j;
  JsonDocument out;
  out["started"] = true;
  out["total_g"] = sum;
  sendJson(202, out);
}

static void handleHome() {
  if (busy) { sendError(409, "Gerät ist beschäftigt"); return; }
  JsonDocument doc;
  if (!parseBody(doc)) return;
  Job j;
  j.type = JOB_HOME;
  if (doc["id"].is<const char*>()) {
    const char* id = doc["id"];
    int i = stationIndex(id[0]);
    if (i < 0) { sendError(400, "Unbekannte Station"); return; }
    j.stationMask = 1 << i;
  } else {
    j.stationMask = (1 << N_STATIONS) - 1;
  }
  job = j;
  JsonDocument out;
  out["started"] = true;
  sendJson(202, out);
}

static void handlePrime() {
  if (busy) { sendError(409, "Gerät ist beschäftigt"); return; }
  JsonDocument doc;
  if (!parseBody(doc)) return;
  if (!doc["id"].is<const char*>()) { sendError(400, "Feld id fehlt"); return; }
  const char* id = doc["id"];
  int i = stationIndex(id[0]);
  if (i < 0) { sendError(400, "Unbekannte Station"); return; }
  float ml = doc["ml"] | 1.0f;
  if (fabsf(ml) > 30) { sendError(400, "Höchstens 30 ml pro Aufruf"); return; }
  Job j;
  j.type = JOB_PRIME;
  j.primeIdx = i;
  j.primeMl = ml;
  job = j;
  JsonDocument out;
  out["started"] = true;
  sendJson(202, out);
}

static void handleStop() {
  stopRequested = true;
  JsonDocument out;
  out["stopping"] = true;
  sendJson(200, out);
}

static void handleConfigGet() {
  JsonDocument doc;
  for (int i = 0; i < N_STATIONS; i++) {
    JsonObject o = doc[String(stations[i].id)].to<JsonObject>();
    o["g_per_ml"] = stations[i].gPerMl;
    o["ml_per_mm"] = stations[i].mlPerMm;
    o["steps_per_ml"] = stepsPerMl(stations[i]);
  }
  sendJson(200, doc);
}

static void handleConfigPost() {
  if (busy) { sendError(409, "Gerät ist beschäftigt"); return; }
  JsonDocument doc;
  if (!parseBody(doc)) return;
  for (JsonPair kv : doc.as<JsonObject>()) {
    int i = stationIndex(kv.key().c_str()[0]);
    if (i < 0) { sendError(400, String("Unbekannte Station ") + kv.key().c_str()); return; }
    JsonObject o = kv.value().as<JsonObject>();
    if (o["g_per_ml"].is<float>()) {
      float v = o["g_per_ml"];
      if (v < 0.5f || v > 3.0f) { sendError(400, "g_per_ml außerhalb 0,5 bis 3"); return; }
      stations[i].gPerMl = v;
    }
    if (o["ml_per_mm"].is<float>()) {
      float v = o["ml_per_mm"];
      if (v < 0.1f || v > 2.0f) { sendError(400, "ml_per_mm außerhalb 0,1 bis 2"); return; }
      stations[i].mlPerMm = v;
    }
  }
  saveConfig();
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

// ---------------------------------------------------------------- Setup

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENABLE, OUTPUT);
  driversEnable(false);
  for (int i = 0; i < N_STATIONS; i++) {
    Station& s = stations[i];
    s.id = STATION_IDS[i];
    s.stepPin = PIN_STEP[i];
    s.dirPin = PIN_DIR[i];
    s.endPin = PIN_ENDSTOP[i];
    s.invert = DIR_INVERT[i];
    s.posSteps = 0;
    s.retractedSteps = 0;
    s.homed = false;
    pinMode(s.stepPin, OUTPUT);
    pinMode(s.dirPin, OUTPUT);
    pinMode(s.endPin, INPUT_PULLUP);
    digitalWrite(s.stepPin, LOW);
  }
  loadConfig();

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
  server.serveStatic("/icon.png", LittleFS, "/icon.png", "max-age=86400");
  server.on("/status", HTTP_GET, handleStatus);
  server.on("/dispense", HTTP_POST, handleDispense);
  server.on("/home", HTTP_POST, handleHome);
  server.on("/prime", HTTP_POST, handlePrime);
  server.on("/stop", HTTP_POST, handleStop);
  server.on("/config", HTTP_GET, handleConfigGet);
  server.on("/config", HTTP_POST, handleConfigPost);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("Webserver läuft");
}

void loop() {
  server.handleClient();
  if (job.type != JOB_NONE && !busy) runJob();
  delay(1);
}
