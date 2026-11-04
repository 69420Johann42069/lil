#!/bin/sh
# Baut ein fertiges Web-Paket des Farbmischers.
#   1. lädt mixbox.js, falls es neben diesem Skript fehlt
#   2. baut hamster.js aus hamster.png neu
#   3. packt index.html, farbmath.js, mixbox.js, hamster.js, icon.png
#      in einen Ordner farbmischer-web/ und legt ../farbmischer-web.zip an
# Braucht nur sh, curl, zip und python3 (Standardbibliothek).
# Aufruf aus einem beliebigen Ordner:  sh web/paket.sh
# mixbox.js: Lizenz CC BY-NC 4.0, nur für privaten, nicht kommerziellen Gebrauch.
set -eu
cd "$(dirname "$0")"

URL="https://raw.githubusercontent.com/scrtwpns/mixbox/master/javascript/mixbox.js"
SHA256="7827560f74061e187acf5ce0e54abb7b2f81eac1515fc974f93efaaa1480eed9"
OUT="../farbmischer-web.zip"

for tool in zip python3; do
  command -v "$tool" >/dev/null 2>&1 || { echo "Fehler: $tool nicht gefunden" >&2; exit 1; }
done

# Eine vorhandene mixbox.js muss plausibel sein, sonst wird sie neu geladen.
if [ -s mixbox.js ] && { [ "$(wc -c < mixbox.js)" -lt 100000 ] || ! grep -q "MIXBOX" mixbox.js; }; then
  echo "mixbox.js ist unvollständig, lade neu ..."
  rm -f mixbox.js
fi

if [ ! -s mixbox.js ]; then
  command -v curl >/dev/null 2>&1 || { echo "Fehler: curl nicht gefunden, mixbox.js von Hand nach web/ legen" >&2; exit 1; }
  echo "mixbox.js fehlt, lade herunter ..."
  tmp="mixbox.js.tmp.$$"
  trap 'rm -f "$tmp"' EXIT
  curl -fsSL --retry 2 --max-time 60 -o "$tmp" "$URL" \
    || { echo "Fehler: Download von $URL fehlgeschlagen. Datei von Hand nach web/ legen." >&2; exit 1; }
  # Plausibilität: nicht leer, keine HTML-Fehlerseite, Mixbox-Kopf vorhanden
  [ "$(wc -c < "$tmp")" -gt 100000 ] && grep -q "MIXBOX" "$tmp" \
    || { echo "Fehler: heruntergeladene mixbox.js sieht nicht richtig aus" >&2; exit 1; }
  mv "$tmp" mixbox.js
  trap - EXIT
fi

# Prüfsumme nur als Warnung: Upstream darf sich ändern, die Seite soll trotzdem gebaut werden.
sum=$(python3 -I -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' mixbox.js)
[ "$sum" = "$SHA256" ] || echo "Hinweis: mixbox.js weicht vom getesteten Stand ab (sha256 $sum). Seite danach im Browser prüfen." >&2

python3 -I build_hamster.py

stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
mkdir "$stage/farbmischer-web"
cp index.html farbmath.js mixbox.js hamster.js icon.png "$stage/farbmischer-web/"
rm -f "$OUT"
(cd "$stage" && zip -q -r -X "$(cd - >/dev/null && pwd)/$OUT" farbmischer-web)
echo "Fertig: $(cd .. && pwd)/$(basename "$OUT")"
python3 -I -c 'import sys,zipfile;[print("  ",i.file_size,i.filename) for i in zipfile.ZipFile(sys.argv[1]).infolist()]' "$OUT"
