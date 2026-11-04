#!/bin/sh
# Kopiert die Web-App nach data/, damit `pio run -t uploadfs` sie auf das
# LittleFS des ESP32 schreibt. mixbox.js muss vorher in ../web liegen.
set -e
cd "$(dirname "$0")"
mkdir -p data
cp ../web/index.html ../web/farbmath.js ../web/icon.png ../web/hamster.js data/
if [ -f ../web/mixbox.js ]; then
  cp ../web/mixbox.js data/
else
  echo "Warnung: ../web/mixbox.js fehlt, siehe README" >&2
fi
ls -la data
