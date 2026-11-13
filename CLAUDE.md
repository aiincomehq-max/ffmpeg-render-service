# Project: ffmpeg-render-service → Speed clipping pipeline

- Current mission: **SESSION_1_BUILD.md**. The clipper CLI (`clipper/`) is already built; get it running on real footage and ship.
- Strategy, data and decisions: CLIPPING_PIPELINE_IDEA.md (sections 7–8). LOCKED: one streamer per YouTube channel (channels.json: speed → kai → core) and the style in `styles/speed_v2.json`. Don't re-debate them.
- **Renders go to the Samsung T7 SSD (13 Nov 2026):** `out/` is a symlink to `/Volumes/T7/YT_RENDERS/clipz/out`. Keep writing to `out/` as before. Prefix renders with `TMPDIR=/Volumes/T7/YT_RENDERS/_tmp`. If `ls /Volumes/T7` fails, the T7 is unplugged: ask the owner to plug it in. Never replace the link with a real folder on the Mac. `data/` (17 GB) is still on the Mac.
- `app.py` is the legacy FastAPI render endpoint. Leave it unless needed.
- The owner wants speed: build, test on real footage, ship. Ask only when blocked.
- Before every commit: `python -m unittest discover -s tests` must pass (add a test when you fix a bug).
