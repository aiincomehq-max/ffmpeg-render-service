"""Smoke test: synthesize a fake 16:9 'stream VOD' and render both formats.

    python tests/smoke_render.py
Outputs to out/smoke/.
"""
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from clipper import ROOT  # noqa: E402
from clipper import edl as E  # noqa: E402
from clipper.render import render  # noqa: E402
from clipper.style import load  # noqa: E402

OUT = ROOT / "out" / "smoke"
OUT.mkdir(parents=True, exist_ok=True)
SRC = OUT / "fake_vod.mp4"

if not SRC.exists():
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30:duration=120",
        "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=44100:duration=120",
        "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", str(SRC),
    ], check=True, capture_output=True)

style = load()
music = str(ROOT / "assets" / "music" / "placeholder_phonk_130.wav")

# Fake transcript: words every ~0.35s with a few long silences
rng = random.Random(1)
vocab = "bro no way chat look at this what is he doing speed is crazy watch this one".split()
words, t = [], 10.0
while t < 50:
    if rng.random() < 0.06:
        t += rng.uniform(1.0, 2.5)  # silence that should get cut
    w = rng.choice(vocab)
    words.append({"w": w, "s": round(t, 2), "e": round(t + 0.28, 2)})
    t += 0.35

moment = {
    "src": str(SRC), "start": 10.0, "end": 45.0, "payoff_t": 41.0, "impact_ts": [30.0],
    "hook_tag": "SPEED TRIES THE SNAKE", "action_tags": [{"t": 25.0, "text": "WAIT FOR IT"}],
    "emoji": "💀", "words": words, "comedic": True,
}
edl1 = E.single_moment(moment, style, "@speedclipz", music)
f1 = render(edl1, style, OUT / "single_moment.mp4")
print("rendered", f1)

fail = {"src": str(SRC), "start": 60, "end": 66, "payoff_t": 63}
succ = [{"src": str(SRC), "start": 66 + i * 8, "end": 74 + i * 8, "impact_ts": [70 + i * 8]} for i in range(5)]
edl2 = E.subversion_comp("has slow reflexes", fail, succ, style, "@speedclipz", music, seed=1)
f2 = render(edl2, style, OUT / "subversion_comp.mp4")
print("rendered", f2)
