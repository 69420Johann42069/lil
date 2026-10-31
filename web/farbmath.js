// Farbmathematik für den Farbmischer (Stufe 0 und Stufe 1).
// Läuft im Browser (window.farbmath) und in Node (module.exports) zum Testen.
// Benötigt mixbox.js (Secret Weapons, CC BY-NC 4.0) als globales `mixbox`
// bzw. per require. Siehe README für den Download.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory(require(process.env.MIXBOX_PATH || './mixbox.js'));
  } else {
    root.farbmath = factory(root.mixbox);
  }
})(typeof self !== 'undefined' ? self : this, function (mixbox) {
  'use strict';

  // Standard-Primärfarben. RGB = ungefährer Masston der Tube auf Weiß.
  // Diese Werte sind Startwerte und sollen per Kalibrierung ersetzt werden.
  var DEFAULT_PRIMARIES = [
    { id: 'C', name: 'Primär-Cyan',    rgb: [0, 118, 182] },
    { id: 'M', name: 'Primär-Magenta', rgb: [196, 18, 112] },
    { id: 'Y', name: 'Primär-Gelb',    rgb: [255, 222, 0] },
    { id: 'W', name: 'Titanweiß',      rgb: [250, 250, 247] },
    { id: 'K', name: 'Schwarz',        rgb: [22, 22, 24] }
  ];

  // ---------- sRGB -> CIE Lab ----------
  function srgbToLinear(c) {
    c /= 255;
    return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  }
  function rgbToLab(rgb) {
    var r = srgbToLinear(rgb[0]), g = srgbToLinear(rgb[1]), b = srgbToLinear(rgb[2]);
    var x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
    var y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.0;
    var z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;
    var f = function (t) { return t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116; };
    var fx = f(x), fy = f(y), fz = f(z);
    return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
  }
  function deltaE(lab1, lab2) {
    var dl = lab1[0] - lab2[0], da = lab1[1] - lab2[1], db = lab1[2] - lab2[2];
    return Math.sqrt(dl * dl + da * da + db * db);
  }

  // ---------- Mischen ----------
  // Float-Varianten verwenden: latentToRgb rundet auf Ganzzahlen, dann wäre
  // der numerische Gradient im Optimierer null.
  function latents(primaries) {
    return primaries.map(function (p) { return mixbox.floatRgbToLatent(p.rgb[0] / 255, p.rgb[1] / 255, p.rgb[2] / 255); });
  }
  function mixLatents(zs, w) {
    var z = new Array(mixbox.LATENT_SIZE);
    for (var i = 0; i < z.length; i++) {
      var s = 0;
      for (var j = 0; j < zs.length; j++) s += w[j] * zs[j][i];
      z[i] = s;
    }
    return mixbox.latentToFloatRgb(z).map(function (c) { return Math.min(255, Math.max(0, c * 255)); });
  }
  function predict(primaries, weights) {
    return mixLatents(latents(primaries), weights);
  }

  // Projektion auf den Simplex: w >= 0, sum(w) = 1
  function projectSimplex(v) {
    var n = v.length;
    var u = v.slice().sort(function (a, b) { return b - a; });
    var css = 0, theta = 0;
    for (var i = 0; i < n; i++) {
      css += u[i];
      if (u[i] - (css - 1) / (i + 1) > 0) theta = (css - 1) / (i + 1);
    }
    return v.map(function (x) { return Math.max(x - theta, 0); });
  }

  // Findet Gewichte w (Anteile 0..1, Summe 1), sodass predict(w) der
  // Zielfarbe in Lab möglichst nahe kommt. Projizierter Gradientenabstieg
  // mit numerischem Gradienten und mehreren Startpunkten.
  function solve(targetRgb, primaries, opts) {
    opts = opts || {};
    primaries = primaries || DEFAULT_PRIMARIES;
    var zs = latents(primaries);
    var n = primaries.length;
    var targetLab = rgbToLab(targetRgb);
    var cost = function (w) { return deltaE(rgbToLab(mixLatents(zs, w)), targetLab); };

    var starts = [];
    starts.push(new Array(n).fill(1 / n));
    for (var i = 0; i < n; i++) { var e = new Array(n).fill(0.02); e[i] = 1 - 0.02 * (n - 1); starts.push(e); }
    var seed = 12345;
    var rnd = function () { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
    var randomStarts = opts.randomStarts == null ? 12 : opts.randomStarts;
    for (var r = 0; r < randomStarts; r++) {
      var v = [], s = 0;
      for (var k = 0; k < n; k++) { var x = -Math.log(rnd() + 1e-9); v.push(x); s += x; }
      starts.push(v.map(function (x) { return x / s; }));
    }

    var best = null, bestCost = Infinity;
    var iters = opts.iters || 150, h = 1e-4;
    starts.forEach(function (w0) {
      var w = w0.slice(), c = cost(w), step = 0.05;
      for (var it = 0; it < iters; it++) {
        var grad = new Array(n);
        for (var j = 0; j < n; j++) {
          var wp = w.slice(); wp[j] += h;
          grad[j] = (cost(projectSimplex(wp)) - c) / h;
        }
        var gn = 0; for (j = 0; j < n; j++) gn += grad[j] * grad[j];
        gn = Math.sqrt(gn) || 1;
        var improved = false;
        for (var tries = 0; tries < 6; tries++) {
          var wn = projectSimplex(w.map(function (x, j) { return x - step * grad[j] / gn; }));
          var cn = cost(wn);
          if (cn < c) { w = wn; c = cn; improved = true; step *= 1.2; break; }
          step *= 0.5;
        }
        if (!improved && step < 1e-5) break;
      }
      if (c < bestCost) { bestCost = c; best = w; }
    });

    var predicted = mixLatents(zs, best);
    return { weights: best, predictedRgb: predicted, deltaE: bestCost };
  }

  // Gewichte -> Rezept in Gramm. Anteile unter `minGrams` werden auf 0
  // gesetzt und der Rest neu normiert, damit die Summe stimmt.
  function recipe(weights, primaries, totalGrams, minGrams) {
    minGrams = minGrams == null ? 0.1 : minGrams;
    var w = weights.map(function (x) { return x * totalGrams >= minGrams ? x : 0; });
    var s = w.reduce(function (a, b) { return a + b; }, 0) || 1;
    w = w.map(function (x) { return x / s; });
    var rows = [];
    primaries.forEach(function (p, i) {
      var g = Math.round(w[i] * totalGrams * 10) / 10;
      rows.push({ id: p.id, name: p.name, rgb: p.rgb, grams: g, percent: Math.round(w[i] * 1000) / 10 });
    });
    return { rows: rows, totalGrams: totalGrams, predictedRgb: predict(primaries, w), weights: w };
  }

  function rating(dE) {
    if (dE < 2) return 'sehr nah, mit bloßem Auge kaum zu unterscheiden';
    if (dE < 5) return 'gut, kleine Korrektur mit einem Klecks reicht';
    if (dE < 10) return 'grob, die Richtung stimmt, Nachmischen nötig';
    return 'mit diesen Primärfarben nicht erreichbar, zu leuchtend oder außerhalb des Farbraums';
  }

  function hexToRgb(hex) {
    var m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex.trim());
    return m ? [parseInt(m[1], 16), parseInt(m[2], 16), parseInt(m[3], 16)] : null;
  }
  function rgbToHex(rgb) {
    return '#' + rgb.map(function (c) { return ('0' + Math.round(c).toString(16)).slice(-2); }).join('');
  }

  return {
    DEFAULT_PRIMARIES: DEFAULT_PRIMARIES,
    solve: solve, recipe: recipe, predict: predict, rating: rating,
    rgbToLab: rgbToLab, deltaE: deltaE, hexToRgb: hexToRgb, rgbToHex: rgbToHex
  };
});
