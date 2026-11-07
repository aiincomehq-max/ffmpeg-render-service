#!/usr/bin/env bash
# One-command Mac setup for the clipper.
#   bash tools/setup_mac.sh
# Installs ffmpeg + Python, creates .venv, installs packages, saves your API key to .env (git-ignored),
# sets your channel handle, generates audio assets and runs the offline demo.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v brew >/dev/null; then
  echo "Homebrew is missing. Install it first (one line, from https://brew.sh), then re-run this script."
  exit 1
fi

echo "==> Installing ffmpeg-full + Python 3.12 (Homebrew)"
brew install ffmpeg-full python@3.12 deno >/dev/null   # ffmpeg-full = libass (captions); plain ffmpeg 9.x lacks it
PY="$(brew --prefix python@3.12)/bin/python3.12"

echo "==> Python environment"
[ -d .venv ] || "$PY" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements-clipper.txt

touch .env
if ! grep -q '^ANTHROPIC_API_KEY=' .env; then
  read -rsp "Anthropic API key (sk-ant-..., from console.anthropic.com): " KEY; echo
  [ -n "$KEY" ] && echo "ANTHROPIC_API_KEY=$KEY" >> .env
fi

if ! grep -q '^BLOTATO_API_KEY=' .env; then
  read -rsp "Blotato API key for auto-posting (Blotato > Settings > API; Enter to skip = dry run): " BKEY; echo
  [ -n "$BKEY" ] && echo "BLOTATO_API_KEY=$BKEY" >> .env
fi

read -rp "Channel key to set up [speed]: " CHKEY; CHKEY=${CHKEY:-speed}
read -rp "Its YouTube @handle (Enter to skip): " HANDLE
if [ -n "$HANDLE" ]; then
  python - "$CHKEY" "$HANDLE" <<'EOF'
import json, sys
key, handle = sys.argv[1], sys.argv[2]
handle = handle if handle.startswith("@") else "@" + handle
c = json.load(open("channels.json"))
c[key]["handle"] = handle
json.dump(c, open("channels.json", "w"), indent=2, ensure_ascii=False)
open("channels.json", "a").write("\n")
print(f"   {key} watermark set to {handle}")
EOF
fi

echo "==> Generating sound effects + placeholder music"
python tools/make_audio_assets.py >/dev/null

echo "==> Offline demo render (about 1-2 min)"
python -m clipper demo
open out/demo/*/review.html 2>/dev/null || true

cat <<EOF

Setup done.
  Daily run:      source .venv/bin/activate && python -m clipper --channel $CHKEY auto
  Approve+post:   python -m clipper --channel $CHKEY review   (http://localhost:8765)
  Blotato ids:    python -m clipper --channel $CHKEY accounts (copy ids into channels.json → blotato)
  Autopilot:      bash tools/schedule.sh $CHKEY 10:00     (runs daily, notifies you, approve page stays up 12h)
  Twitch channels also: bash tools/schedule.sh kai 01:00 night   (1am: auto-posts the strongest fresh Short)
EOF
