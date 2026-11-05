// Host-Test der Rechenfunktionen aus include/dosing.h, ohne Arduino.
//   g++ -std=c++17 firmware/test/test_dosing.cpp -Ifirmware/include -o /tmp/test_dosing && /tmp/test_dosing
#include <assert.h>
#include <initializer_list>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "dosing.h"

using namespace dosing;

static bool near(float a, float b, float eps) { return fabsf(a - b) <= eps; }

static void testStationPositions() {
  const int expect[7] = {0, 457, 914, 1371, 1829, 2286, 2743};
  for (int p = 0; p < 7; p++) {
    assert(stationPosition(p) == expect[p]);
    assert(stationPosition(p) == (int)llround(p * 3200.0 / 7.0));  // q = round(p*3200/7)
    assert(placeAtQ(stationPosition(p)) == p);
  }
  assert(stationPosition(7) == 0);   // wrap
  assert(stationPosition(-1) == stationPosition(6));
  assert(placeAtQ(100) == -1);
  assert(normalizeQ(-1) == 3199);
  assert(normalizeQ(6400) == 0);
}

static void testShortestPath() {
  assert(shortestPlaces(0, 0) == 0);
  assert(shortestPlaces(0, 3) == 3);
  assert(shortestPlaces(0, 4) == -3);  // 4 vorwärts = 3 rückwärts
  assert(shortestPlaces(6, 0) == 1);
  assert(shortestPlaces(0, 6) == -1);
  assert(shortestPlaces(1, 6) == -2);
  assert(shortestPlaces(5, 1) == 3);
  for (int a = 0; a < 7; a++)
    for (int b = 0; b < 7; b++) {
      int d = shortestPlaces(a, b);
      assert(d >= -3 && d <= 3);
      assert(wrapPlace(a + d) == b);
    }
  // Schritte: Ziel wird exakt getroffen, nie mehr als 3 Plätze
  assert(carouselDeltaSteps(0, 0) == 0);
  assert(carouselDeltaSteps(0, 4) == -1371);  // 3 Plätze rückwärts
  assert(carouselDeltaSteps(0, 3) == 1371);
  assert(carouselDeltaSteps(stationPosition(6), 0) == 457);
  for (int a = 0; a < 7; a++)
    for (int b = 0; b < 7; b++) {
      int d = carouselDeltaSteps(stationPosition(a), b);
      assert(normalizeQ(stationPosition(a) + d) == stationPosition(b));
      assert(abs(d) <= 1372);               // höchstens 3 Plätze
      assert((d > 0) == (shortestPlaces(a, b) > 0) || d == 0);
    }
}

static void testMlMm() {
  const float mlPerMm = (float)(M_PI * 13.35 * 13.35 / 1000.0);  // Innen-Ø 26,7 mm
  assert(near(mlPerMm, 0.5599f, 0.0002f));
  assert(near(1.0f / mlPerMm, 1.786f, 0.002f));                    // mm je ml
  assert(near(50.0f / mlPerMm, 89.3f, 0.1f));                      // Nutzhub
  assert(mmToSteps(1.0f) == 1600);
  assert(mmToSteps(89.3f) == 142880);
  assert(near(stepsToMm(3200), 2.0f, 1e-6f));                      // eine Umdrehung = 2 mm
  assert(near(stepsPerMl(0.56f), 2857.14f, 0.01f));
  assert(mlToSteps(1.0f, 0.56f) == 2857);
  assert(mlToSteps(2.0f, 0.5599f) == lroundf(2.0f * 1600.0f / 0.5599f));
  assert(near(stepsToMl(mlToSteps(7.3f, 0.5599f), 0.5599f), 7.3f, 0.001f));
  assert(near(flowGps(2857.14f, 0.56f, 1.3f), 1.3f, 0.001f));      // 1 ml/s bei 2857 sps
}

static void testRamp() {
  assert(near(rampSps(0, 10000, 400, 500, 3000), 500, 1e-3f));
  assert(near(rampSps(200, 10000, 400, 500, 3000), 1750, 1e-3f));
  assert(near(rampSps(5000, 5000, 400, 500, 3000), 3000, 1e-3f));
  assert(near(rampSps(9900, 100, 400, 500, 3000), 1125, 1e-3f));   // Abbremsen am Ende
  assert(near(rampSps(0, 0, 400, 500, 3000), 500, 1e-3f));
  assert(near(rampSps(10, 10, 400, 500, 300), 300, 1e-3f));        // max unter Start
}

static void testRemaining() {
  assert(near(remainingMl(50.0f, 13.0f, 1.3f), 40.0f, 1e-4f));
  assert(remainingMl(5.0f, 100.0f, 1.3f) == 0.0f);
  assert(canDose(50.0f, 10.0f, 1.3f, 1.0f));
  assert(!canDose(5.0f, 10.0f, 1.3f, 1.0f));                       // 5 - 1 = 4 ml = 5,2 g
  assert(canDose(8.7f, 10.0f, 1.3f, 1.0f));                        // 7,7 ml >= 7,69 ml
}

static void testWhite() {
  assert(pickWhite(50, 20) == 0);
  assert(pickWhite(20, 50) == 1);
  assert(pickWhite(30, 30) == 0);  // Gleichstand: W1
  // reicht aus der volleren Spritze
  WhitePlan p = planWhite(10.0f, 20.0f, 1.3f, 40.0f, 1.3f, 1.0f, 0.1f);
  assert(p.n == 1 && p.idx[0] == 1 && near(p.grams[0], 10.0f, 1e-5f));
  // volle Spritze reicht nicht, Rest aus der anderen: (6-1)*1,3 = 6,5 g aus W2, 3,5 g aus W1
  p = planWhite(10.0f, 4.0f, 1.3f, 6.0f, 1.3f, 1.0f, 0.1f);
  assert(p.n == 2 && p.idx[0] == 1 && p.idx[1] == 0);
  assert(near(p.grams[0], 6.5f, 1e-4f) && near(p.grams[1], 3.5f, 1e-4f));
  assert(near(p.grams[0] + p.grams[1], 10.0f, 1e-4f));
  // beide zu leer
  p = planWhite(10.0f, 4.0f, 1.3f, 5.0f, 1.3f, 1.0f, 0.1f);       // 3,9 g + 5,2 g = 9,1 g
  assert(p.n == 0);
  // Rest der vollen Spritze kleiner als minG: komplett aus der anderen
  p = planWhite(5.0f, 1.03f, 1.3f, 0.5f, 1.3f, 1.0f, 0.1f);
  assert(p.n == 0);
  p = planWhite(1.0f, 1.0f, 1.3f, 30.0f, 1.3f, 1.0f, 0.1f);
  assert(p.n == 1 && p.idx[0] == 1);
  // leer / leer
  p = planWhite(1.0f, 0.0f, 1.3f, 0.0f, 1.3f, 1.0f, 0.1f);
  assert(p.n == 0);
}

static void testBrakeAndChunks() {
  // Bremspunkt: mindestens minMargin, sonst Förderstrom x Verzögerung
  assert(near(brakePointG(10.0f, 1.4f, 0.6f, 0.5f), 10.0f - 0.84f, 1e-4f));
  assert(near(brakePointG(10.0f, 0.1f, 0.6f, 0.5f), 9.5f, 1e-4f));
  assert(brakePointG(0.3f, 1.4f, 0.6f, 0.5f) == 0.0f);

  // Simulierte Dosierung: jeder Schritt liefert exakt (oder leicht überschießend) Gramm.
  const float gPerMl = 1.3f;
  const float tests[] = {0.1f, 0.5f, 1.1f, 4.2f, 10.0f, 37.5f};
  for (float target : tests) {
    for (float overshoot : {0.0f, 0.02f}) {
      float done = 0.1f;  // Kontakt hat schon etwas gefördert
      float brake = brakePointG(target, 1.4f, 0.6f, 0.5f);
      int n = 0;
      bool sawFine = false;
      bool coarseAfterFine = false;
      if (done >= target - 0.05f) { n = 0; }
      for (; n < 500; n++) {
        Chunk c = nextChunk(done, target, gPerMl, brake, 3.0f, 0.3f, 0.03f, 0.05f);
        if (c.ml <= 0) break;
        if (c.fine) sawFine = true;
        else if (sawFine) coarseAfterFine = true;
        float g = c.ml * gPerMl;
        if (!c.fine) assert(done + g <= brake + 1e-3f);   // grob nie über den Bremspunkt
        assert(g <= 3.0f + 1e-4f);
        done += g + overshoot * g;
      }
      assert(n < 500);
      assert(!coarseAfterFine);
      assert(done >= target - 0.1f);      // Toleranz 0,1 g
      assert(done <= target + 0.1f + 3 * 0.3f * overshoot);
      if (overshoot == 0.0f) assert(fabsf(done - target) <= 0.1f);
    }
  }
  // Fertig, wenn Rest <= Stoppmarge
  assert(nextChunk(9.96f, 10.0f, 1.3f, 9.0f, 3.0f, 0.3f, 0.03f, 0.05f).ml == 0.0f);
  // Weit vor dem Bremspunkt: grober, schneller Schritt
  Chunk c = nextChunk(0.0f, 10.0f, 1.3f, 9.0f, 3.0f, 0.3f, 0.03f, 0.05f);
  assert(!c.fine && near(c.ml, 3.0f / 1.3f, 1e-5f));
  // Hinter dem Bremspunkt: fein, höchstens 0,3 g
  c = nextChunk(9.5f, 10.0f, 1.3f, 9.0f, 3.0f, 0.3f, 0.03f, 0.05f);
  assert(c.fine && near(c.ml * 1.3f, 0.3f, 1e-4f));
}

int main() {
  testStationPositions();
  testShortestPath();
  testMlMm();
  testRamp();
  testRemaining();
  testWhite();
  testBrakeAndChunks();
  printf("test_dosing: alle Asserts bestanden\n");
  return 0;
}
