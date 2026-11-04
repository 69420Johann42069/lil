#!/bin/sh
# Kopiert die Web-App nach data/, damit `pio run -t uploadfs` sie auf das
# LittleFS des ESP32 schreibt. mixbox.js muss vorher in ../web liegen:
# `sh ../web/paket.sh` lädt sie bei Bedarf, siehe README.
set -e
cd "$(dirname "$0")"
if [ ! -s ../web/mixbox.js ]; then
  echo "FEHLER: ../web/mixbox.js fehlt, die Seite würde auf dem Gerät nur einen Hinweis zeigen." >&2
  echo "        Mit 'sh ../web/paket.sh' laden oder von Hand nach web/ legen, siehe README." >&2
  exit 1
fi
rm -rf data
mkdir -p data
cp ../web/index.html ../web/farbmath.js ../web/mixbox.js ../web/hamster.js ../web/icon.png data/
ls -la data
