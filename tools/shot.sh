#!/bin/sh
# Renders an SVG or HTML file to PNG with headless Chrome, for a quick look.
#   tools/shot.sh assets/hero-dark.svg 1200 420
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$(cd "$(dirname "$0")" && pwd)/.preview"
mkdir -p "$OUT"
SRC="$1"; W="${2:-1200}"; H="${3:-420}"
NAME="$(basename "$SRC" | sed 's/\.[a-z]*$//')"
PNG="$OUT/$NAME.png"
rm -f "$PNG"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --user-data-dir="$OUT/.chrome-$$" --virtual-time-budget=6000 \
  --window-size="$W,$H" --screenshot="$PNG" \
  "file://$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")" >/dev/null 2>&1 &
PID=$!
# Chrome sometimes keeps running after the screenshot is written, so stop it ourselves.
i=0
while [ $i -lt 60 ] && [ ! -s "$PNG" ]; do sleep 0.5; i=$((i + 1)); done
sleep 0.5
kill $PID 2>/dev/null
wait $PID 2>/dev/null
rm -rf "$OUT/.chrome-$$"
echo "$PNG"
