#!/usr/bin/env bash
# Daily autopilot on macOS (launchd). The Mac must be awake (or set to wake) at that time.
#
#   bash tools/schedule.sh speed 10:00            # DAY run: clip, then the approve page stays up 12h
#   bash tools/schedule.sh kai 01:00 night         # NIGHT run: last 24h of Twitch clips, auto-posts the
#                                                  #   single strongest Short at once (first after the stream),
#                                                  #   the rest wait for your morning approval
#   bash tools/schedule.sh kai off night           # remove one run
#
# Recommended:  speed → day 10:00 | kai, core → day 10:00 + night 01:00
# Output: out/<channel>/<date>/ + a macOS notification. Log: data/<channel>/auto[-night].log
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"
CH="${1:?usage: schedule.sh <channel> <HH:MM|off> [day|night]}"
WHEN="${2:?usage: schedule.sh <channel> <HH:MM|off> [day|night]}"
MODE="${3:-day}"
case "$MODE" in
  day)   ARGS="auto --serve"; SUFFIX="" ;;
  night) ARGS="auto --range 24hr --count 3 --autopost 1 --autopost-min 8"; SUFFIX="-night"
         if [ "$CH" = "speed" ]; then
           echo "Note: 'speed' uses YouTube 'Most replayed' data, which only appears ~a day after a stream,"
           echo "so a night run adds little there. Recommended for Twitch channels (kai, core)."
         fi ;;
  *) echo "mode must be day or night"; exit 1 ;;
esac
LABEL="com.clipper.$CH$SUFFIX"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
if [ "$WHEN" = "off" ]; then
  rm -f "$PLIST"; echo "Removed $MODE run for $CH"; exit 0
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
    <string>cd "$REPO" &amp;&amp; source .venv/bin/activate &amp;&amp; (git pull -q || true) &amp;&amp; python -m clipper --channel $CH $ARGS</string>
  </array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>$HOUR</integer><key>Minute</key><integer>$MIN</integer></dict>
  <key>StandardOutPath</key><string>$REPO/data/$CH/auto$SUFFIX.log</string>
  <key>StandardErrorPath</key><string>$REPO/data/$CH/auto$SUFFIX.log</string>
</dict></plist>
EOF
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Scheduled: '$CH' $MODE run daily at $WHEN (Mac local time). Log: data/$CH/auto$SUFFIX.log"
echo "Tip: System Settings > Battery > Options: allow wake for network access, or keep the Mac awake at that time."
[ "$MODE" = "night" ] && echo "Night run auto-posts only Shorts scoring 8+/10 that passed the visual check; it needs BLOTATO_API_KEY (dry run otherwise)."
exit 0
