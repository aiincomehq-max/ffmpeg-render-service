"""Render a job file locally without running the web server.

    python render_job.py jobs/block-lore.json            -> out/block-lore.mp4

Clip/music/voice paths in the job file can be local (relative to the repo root) or http(s) URLs.
Any shot file that doesn't exist yet is listed before rendering so you can see what's missing.
"""
import json
import os
import shutil
import sys

os.environ.setdefault("ALLOW_LOCAL_FILES", "1")
import app  # noqa: E402

job_path = sys.argv[1]
job = json.load(open(job_path))

missing = []
for c in job["clips"]:
    url = c if isinstance(c, str) else c["url"]
    if not url.startswith("http") and not os.path.exists(url):
        missing.append(url)
for key in ("music_url", "voiceover_url"):
    if job.get(key) and not job[key].startswith("http") and not os.path.exists(job[key]):
        missing.append(job[key])
for v in job.get("voice_lines", []):
    if not v["url"].startswith("http") and not os.path.exists(v["url"]):
        missing.append(v["url"])
if missing:
    print("Missing files (generate these first):")
    for m in missing:
        print("  -", m)
    sys.exit(1)

result = app.render_video(app.RenderRequest(**job))
os.makedirs("out", exist_ok=True)
out = os.path.join("out", os.path.splitext(os.path.basename(job_path))[0] + ".mp4")
shutil.copy(app.final_path(result["job_id"]), out)
print("Rendered:", out)
