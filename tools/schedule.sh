#!/usr/bin/env bash
# Daily autopilot on macOS (launchd). The Mac must be awake (or set to wake) at that time.
#   bash tools/schedule.sh speed 11:00      # run `clipper --channel speed auto` every day at 11:00
#   bash tools/schedule.sh speed off        # remove it
# Output: out/<channel>/<date>/review.html + a macOS notification. Log: data/<channel>/auto.log
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"
CH="${1:?usage: schedule.sh <channel> <HH:MM|off>}"
WHEN="${2:?usage: schedule.sh <channel> <HH:MM|off>}"
LABEL="com.clipper.$CH"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
if [ "$WHEN" = "off" ]; then
  rm -f "$PLIST"; echo "Removed daily run for $CH"; exit 0
fi
HOUR=$((10#${WHEN%%:*})); MIN=$((10#${WHEN##*:}))
mkdir -p "$HOME/Library/LaunchAgents" "data/$CH"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array>
    <string>/bin/bash</string><string>-lc</string>
    <string>cd "$REPO" &amp;&amp; source .venv/bin/activate &amp;&amp; git pull -q || true; python -m clipper --channel $CH auto</string>
  </array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>$HOUR</integer><key>Minute</key><integer>$MIN</integer></dict>
  <key>StandardOutPath</key><string>$REPO/data/$CH/auto.log</string>
  <key>StandardErrorPath</key><string>$REPO/data/$CH/auto.log</string>
</dict></plist>
EOF
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Scheduled: '$CH' runs daily at $WHEN. Log: data/$CH/auto.log"
echo "Tip: System Settings > Battery > Options: allow wake for network access, or keep the Mac awake at that time."
