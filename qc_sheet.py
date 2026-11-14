"""Quality-check sheet: one frame per second of every clip, one row per clip.

    python qc_sheet.py assets/bemz-dnd            -> assets/bemz-dnd/qc.jpg

Look at every row before rendering. Check each one for:
  - location continuity: underground stays underground, night stays night, same vehicle type
  - physics: vehicles never reverse, doors open the right way, people don't morph
  - text/numbers: logos and numbers stay readable and never mirror or warp
  - faces: the artist's stand-in never shows their face
"""
import glob
import os
import subprocess
import sys

folder = sys.argv[1]
clips = sorted(glob.glob(os.path.join(folder, "[0-9][0-9].mp4")))
if not clips:
    sys.exit(f"No clips like 01.mp4 in {folder}")

font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
rows = []
for clip in clips:
    label = os.path.splitext(os.path.basename(clip))[0]
    row = os.path.join(folder, f".qc_{label}.jpg")
    vf = (f"fps=1,scale=160:284:force_original_aspect_ratio=increase,crop=160:284,"
          f"drawtext=fontfile={font}:text='{label} %{{pts\\:hms}}':fontsize=14:fontcolor=red:x=4:y=4,"
          f"tile=5x1:padding=2")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-vf", vf,
                    "-frames:v", "1", row], check=True)
    rows.append(row)

out = os.path.join(folder, "qc.jpg")
args = sum([["-i", r] for r in rows], [])
filt = f"vstack=inputs={len(rows)}" if len(rows) > 1 else "null"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args, "-filter_complex", filt, out], check=True)
for r in rows:
    os.remove(r)
print(out)
