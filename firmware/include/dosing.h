// Reine Rechenfunktionen für den Farbmischer (Stand 8), ohne Arduino-Abhängigkeit.
// Wird von main.cpp und vom Host-Test firmware/test/test_dosing.cpp benutzt.
#pragma once
#include <math.h>

namespace dosing {

// Stößel: 200 Vollschritte x 16 = 3200 Mikroschritte je Umdrehung, Spindel T8 mit
// 2 mm Steigung, Riemen 1:1 -> 1600 Mikroschritte je mm.
constexpr float PLUNGER_STEPS_PER_MM = 1600.0f;

// Karussell: Direktantrieb, 3200 Mikroschritte je Umdrehung, 7 Plätze (0 = Park).
constexpr int CAROUSEL_STEPS_PER_REV = 3200;
constexpr int CAROUSEL_PLACES = 7;

// ---------------------------------------------------------------- Stößel

inline float stepsPerMl(float mlPerMm) { return PLUNGER_STEPS_PER_MM / mlPerMm; }
inline long mlToSteps(float ml, float mlPerMm) { return lroundf(ml * stepsPerMl(mlPerMm)); }
inline float stepsToMl(long steps, float mlPerMm) { return (float)steps / stepsPerMl(mlPerMm); }
inline long mmToSteps(float mm) { return lroundf(mm * PLUNGER_STEPS_PER_MM); }
inline float stepsToMm(long steps) { return (float)steps / PLUNGER_STEPS_PER_MM; }

// Förderstrom in g/s bei gegebener Schrittrate.
inline float flowGps(float sps, float mlPerMm, float gPerMl) {
  return sps / stepsPerMl(mlPerMm) * gPerMl;
}

// Geschwindigkeit (Schritte/s) mit linearer Rampe am Anfang und am Ende einer Bewegung.
// done = bisher gefahrene Schritte, remaining = noch zu fahrende Schritte.
inline float rampSps(long done, long remaining, long rampLen, float startSps, float maxSps) {
  if (maxSps <= startSps) return maxSps;
  long k = done < remaining ? done : remaining;
  if (rampLen < 1) rampLen = 1;
  if (k >= rampLen) return maxSps;
  if (k < 0) k = 0;
  return startSps + (maxSps - startSps) * (float)k / (float)rampLen;
}

// ---------------------------------------------------------------- Karussell

inline int wrapPlace(int p) {
  int m = p % CAROUSEL_PLACES;
  return m < 0 ? m + CAROUSEL_PLACES : m;
}

// Position von Platz p in Mikroschritten: q = round(p * 3200 / 7), 0..3199 für p = 0..6.
// Ganzzahlig gerundet (die Brüche p*3200/7 enden nie auf genau .5).
inline int stationPosition(int p) {
  p = wrapPlace(p);
  return (p * CAROUSEL_STEPS_PER_REV + CAROUSEL_PLACES / 2) / CAROUSEL_PLACES;
}

// Kürzester Weg in Plätzen von Platz from nach Platz to: -3 .. +3 (positiv = vorwärts).
inline int shortestPlaces(int from, int to) {
  int d = wrapPlace(to - from);
  return d > CAROUSEL_PLACES / 2 ? d - CAROUSEL_PLACES : d;
}

// Vorzeichenbehaftete Schritte von der aktuellen Position fromQ (0..3199) zu Platz
// toPlace auf dem kürzeren Weg (höchstens 3 Plätze, wenn fromQ auf einem Platz liegt).
inline int carouselDeltaSteps(int fromQ, int toPlace) {
  int d = (stationPosition(toPlace) - fromQ) % CAROUSEL_STEPS_PER_REV;
  if (d < 0) d += CAROUSEL_STEPS_PER_REV;
  return d > CAROUSEL_STEPS_PER_REV / 2 ? d - CAROUSEL_STEPS_PER_REV : d;
}

inline int normalizeQ(long pos) {
  long m = pos % CAROUSEL_STEPS_PER_REV;
  return (int)(m < 0 ? m + CAROUSEL_STEPS_PER_REV : m);
}

// Platz, falls q genau auf einem Platz liegt, sonst -1.
inline int placeAtQ(int q) {
  for (int p = 0; p < CAROUSEL_PLACES; p++)
    if (stationPosition(p) == q) return p;
  return -1;
}

// ---------------------------------------------------------------- Restmenge, Weiß

inline float remainingMl(float fillMl, float gramsDosed, float gPerMl) {
  float r = fillMl - gramsDosed / gPerMl;
  return r > 0 ? r : 0;
}

// Reicht die Spritze für `grams`, wenn reserveMl übrig bleiben sollen?
inline bool canDose(float fillMl, float grams, float gPerMl, float reserveMl) {
  return fillMl - reserveMl >= grams / gPerMl;
}

// Weiß-Spritze mit mehr Restmenge: 0 = W1, 1 = W2 (bei Gleichstand W1).
inline int pickWhite(float fillW1, float fillW2) { return fillW2 > fillW1 ? 1 : 0; }

struct WhitePlan {
  int n;          // Anzahl Teilschritte (0 = reicht nicht)
  int idx[2];     // 0 = W1, 1 = W2
  float grams[2];
};

// Teilt die Weiß-Menge auf: zuerst die Spritze mit mehr Rest, reicht sie nicht, den Rest
// aus der anderen. Teilmengen unter minG entfallen.
inline WhitePlan planWhite(float grams, float fillW1, float gPerMl1, float fillW2, float gPerMl2,
                           float reserveMl, float minG) {
  WhitePlan p = {0, {0, 0}, {0, 0}};
  float fill[2] = {fillW1, fillW2};
  float gpm[2] = {gPerMl1, gPerMl2};
  int a = pickWhite(fillW1, fillW2);
  int b = 1 - a;
  float availA = fill[a] - reserveMl;
  float maxA = (availA > 0 ? availA : 0) * gpm[a];
  if (maxA >= grams) {
    p.n = 1; p.idx[0] = a; p.grams[0] = grams;
    return p;
  }
  float availB = fill[b] - reserveMl;
  float maxB = (availB > 0 ? availB : 0) * gpm[b];
  float rest = grams - maxA;
  if (maxB < rest) return p;  // reicht nicht
  if (maxA < minG) {          // Teilmenge aus A lohnt nicht
    p.n = 1; p.idx[0] = b; p.grams[0] = grams;
    if (maxB < grams) { p.n = 0; }
    return p;
  }
  p.n = 2;
  p.idx[0] = a; p.grams[0] = maxA;
  p.idx[1] = b; p.grams[1] = rest;
  if (rest < minG) { p.n = 1; }  // Rest verschwindend klein
  return p;
}

// ---------------------------------------------------------------- Dosierschritte

// Bremspunkt: ab diesem Gewicht (Gramm) wird langsam und in kleinen Schritten dosiert.
// Abstand zum Ziel = Förderstrom x Verzögerung der Waage, mindestens minMarginG.
inline float brakePointG(float targetG, float rateGps, float latencyS, float minMarginG) {
  float m = rateGps * latencyS;
  if (m < minMarginG) m = minMarginG;
  float b = targetG - m;
  return b > 0 ? b : 0;
}

struct Chunk {
  float ml;   // 0 = Ziel erreicht
  bool fine;  // true = langsam fahren
};

// Nächster Dosierschritt. Grob (groß, schnell) bis zum Bremspunkt, danach fein: jeweils
// ein Anteil der Restmenge, begrenzt auf [minG, fineG]. Fertig, wenn Rest <= stopMarginG.
inline Chunk nextChunk(float doneG, float targetG, float gPerMl, float brakeG, float coarseG,
                       float fineG, float minG, float stopMarginG) {
  Chunk c = {0.0f, true};
  float remaining = targetG - doneG;
  if (remaining <= stopMarginG) return c;
  float g;
  if (brakeG - doneG >= minG) {
    g = brakeG - doneG;
    if (g > coarseG) g = coarseG;
    c.fine = false;
  } else {
    g = remaining * 0.6f;
    if (g > fineG) g = fineG;
    if (g < minG) g = minG;
  }
  c.ml = g / gPerMl;
  return c;
}

}  // namespace dosing
