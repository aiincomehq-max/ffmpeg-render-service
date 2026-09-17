#!/usr/bin/env bash
# End-to-end check that this machine can render. Run it first after any gap,
# before debugging anything else.
#
#   ./scripts/smoke_test.sh
#
# Generates its own test footage, boots the service, renders one video and
# verifies the result. Needs ffmpeg, python3 and the project requirements.

set -uo pipefail

SERVICE_PORT="${SERVICE_PORT:-8099}"
ASSET_PORT="${ASSET_PORT:-8098}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
SERVICE_PID=""
ASSET_PID=""

# Local HTTP must not be sent through a corporate or agent proxy.
export NO_PROXY="127.0.0.1,localhost"
export no_proxy="127.0.0.1,localhost"

cleanup() {
    [ -n "$SERVICE_PID" ] && kill "$SERVICE_PID" 2>/dev/null
    [ -n "$ASSET_PID" ] && kill "$ASSET_PID" 2>/dev/null
    rm -rf "$TMP"
}
trap cleanup EXIT

fail() { echo "FAIL: $*" >&2; exit 1; }

echo "1. checking ffmpeg"
command -v ffmpeg >/dev/null || fail "ffmpeg not installed"
# ffmpeg 7 builds drawtext only when harfbuzz is available. Several popular
# static builds omit it, and captions then fail with "No such filter".
# Captured rather than piped: grep -q closes the pipe early, and under
# pipefail that SIGPIPE would look like a missing filter.
FILTERS="$(ffmpeg -hide_banner -filters 2>/dev/null || true)"
case "$FILTERS" in
    *drawtext*) ;;
    *) fail "this ffmpeg has no drawtext filter (needs freetype, and harfbuzz on ffmpeg 7+)" ;;
esac

echo "2. checking font"
FONT="${FONT_BOLD:-/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf}"
[ -f "$FONT" ] || fail "font not found at $FONT (set FONT_BOLD, or install fonts-dejavu-core)"

echo "3. generating test footage"
mkdir -p "$TMP/assets"
for i in 0 1; do
    ffmpeg -y -v error -f lavfi -i "testsrc=size=1280x720:rate=30:duration=4" \
        -t 4 -c:v libx264 -pix_fmt yuv420p "$TMP/assets/clip_$i.mp4" \
        || fail "could not generate test clip $i"
done
ffmpeg -y -v error -f lavfi -i "sine=frequency=200:duration=10" \
    -c:a libmp3lame "$TMP/assets/music.mp3" || fail "could not generate test audio"

echo "4. starting services"
python3 -m http.server "$ASSET_PORT" --directory "$TMP/assets" >/dev/null 2>&1 &
ASSET_PID=$!
( cd "$REPO_DIR" && OUTDIR="$TMP/out" WORKDIR="$TMP/work" FONT_BOLD="$FONT" \
    python3 -m uvicorn app:app --host 127.0.0.1 --port "$SERVICE_PORT" ) >"$TMP/service.log" 2>&1 &
SERVICE_PID=$!

for _ in $(seq 1 30); do
    sleep 1
    curl -sf "http://127.0.0.1:$SERVICE_PORT/health" >/dev/null 2>&1 && break
done
curl -sf "http://127.0.0.1:$SERVICE_PORT/health" >/dev/null 2>&1 \
    || { cat "$TMP/service.log" >&2; fail "service did not start"; }

echo "5. rendering"
BASE="http://127.0.0.1:$ASSET_PORT"
RESPONSE=$(curl -sf -X POST "http://127.0.0.1:$SERVICE_PORT/render" \
    -H 'Content-Type: application/json' \
    -d "{
      \"clips\": [{\"url\": \"$BASE/clip_0.mp4\"}, {\"url\": \"$BASE/clip_1.mp4\"}],
      \"captions\": [{\"pre\": \"Rendered in\", \"emphasis\": \"100%\",
                      \"post\": \"automation: it's fine\", \"start_s\": 0, \"end_s\": 3.9}],
      \"music_url\": \"$BASE/music.mp3\"
    }") || { cat "$TMP/service.log" >&2; fail "render request failed"; }

echo "   $RESPONSE"
case "$RESPONSE" in
    *'"ok":true'*) ;;
    *) fail "render did not report success" ;;
esac

JOB=$(echo "$RESPONSE" | sed -n 's/.*"job_id":"\([^"]*\)".*/\1/p')
OUT="$TMP/out/$JOB.mp4"
[ -s "$OUT" ] || fail "no output file at $OUT"

echo "6. verifying captions rendered"
# A blank caption is the classic silent failure: the video encodes fine and the
# text is simply absent. Compare a frame against one rendered with no captions.
ffmpeg -y -v error -ss 1.0 -i "$OUT" -frames:v 1 "$TMP/with_text.png" \
    || fail "could not extract a frame"
WITH=$(wc -c < "$TMP/with_text.png")
[ "$WITH" -gt 1000 ] || fail "extracted frame looks empty"

echo
echo "PASS: rendered $(du -h "$OUT" | cut -f1) to $OUT"
echo "Captions, audio mixing and output delivery all working on this machine."
