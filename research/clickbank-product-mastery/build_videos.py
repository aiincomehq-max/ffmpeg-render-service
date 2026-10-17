#!/usr/bin/env python3
"""Assemble the five dreamreach.x videos from the approved stills and voiceovers.

One still + one voiceover each, a slow linear push in, a hook card in the first
few seconds and the comment instruction at the end. Nothing else -- the outlier
analysis in NICHE_ANALYSIS.md says craft is not what wins here, the hook and the
ask are.

Outputs 1080x1920 / 30fps / H.264 + AAC to build/.
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build")
CARDS = os.path.join(OUT, "cards")
VO = os.path.join(HERE, "vo")
IMG = ("/tmp/claude-0/-home-user-ffmpeg-render-service/"
       "d872ae07-1834-578d-b800-348251a266c4/images")
FONTS = "/mnt/skills/examples/canvas-design/canvas-fonts"
FFMPEG = os.path.expanduser("~/bin/ffmpeg")

W, H, FPS = 1080, 1920, 30
MARGIN = 108          # 10% side gutters -- inside every platform's safe area
TAIL = 1.4            # silence after the last word so the end card can be read
ZOOM = 0.055          # total push across the whole clip

VIDEOS = [
    {
        "slug": "1-face-test",
        "image": "48.webp",           # blank paper + pencil, top-down
        "vo": "1-face-test-takeA.mp3",
        "hook": "Try this.\nIt takes four seconds.",
        "hook_y": 150,                # above the sheet, not across its top edge
        "end": "Comment what you got.",
    },
    {
        "slug": "2-first-name",
        "image": "46.webp",           # folded scrap under a cup
        "vo": "2-first-name-v2-takeA.mp3",
        "hook": "A name just came\ninto your head.",
        "end": "Comment the first letter.",
    },
    {
        "slug": "3-if-this-is-you",
        "image": "47.webp",           # two mugs, one cold
        "vo": "3-if-this-is-you-takeA.mp3",
        "hook": "You'll know\nin ten seconds.",
        "end": "Say “landed” if it did.",
    },
    {
        "slug": "4-count-them",
        "image": "50.webp",           # four coins
        "vo": "4-count-them-takeA.mp3",
        "hook": "Count how many\nare you.",
        "end": "Comment your number.",
        # Timed off silencedetect on the voiceover, not guessed.
        "items": [
            (6.35, 11.50, "1", "The same name, from three\ndifferent people, one week"),
            (11.89, 16.30, "2", "An urge to be somewhere\nyou never go"),
            (16.63, 21.00, "3", "Losing interest in someone\nyou wanted for a year"),
            (21.17, 25.90, "4", "Feeling early.\nFor what, you can't say"),
        ],
        "hook_window": (0.40, 5.90),
        "end_lead": 2.60,
    },
    {
        "slug": "5-stop-waiting",
        "image": "45.webp",           # half-packed suitcase
        "vo": "5-stop-waiting-takeA.mp3",
        "hook": "Nobody becomes\nready.",
        "end": "Tell me I'm wrong.",
    },
]

DEFAULT_HOOK_WINDOW = (0.40, 4.20)
DEFAULT_END_LEAD = 3.20


# ---------------------------------------------------------------- text cards

def wrap(draw, text, font, max_w):
    """Honour explicit newlines, then wrap anything still too wide."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=font) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def card(path, text, size, anchor_y, align="top", number=None):
    """A transparent 1080x1920 PNG: centred lines on dark pills.

    Pills rather than a single block so the shape follows the text and the
    photograph stays visible around it.
    """
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"{FONTS}/InstrumentSans-Bold.ttf", size)
    lines = wrap(d, text, font, W - 2 * MARGIN - 70)

    pad_x, pad_y = 30, 16
    line_h = int(size * 1.30)
    gap = 10

    blocks = []
    if number is not None:
        num_font = ImageFont.truetype(f"{FONTS}/InstrumentSans-Bold.ttf", int(size * 1.9))
        blocks.append((number, num_font, int(size * 1.9 * 1.15)))
    for ln in lines:
        blocks.append((ln, font, line_h))

    total_h = sum(h for _, _, h in blocks) + gap * (len(blocks) - 1) + 2 * pad_y
    y = anchor_y if align == "top" else anchor_y - total_h
    y += pad_y

    for txt, fnt, h in blocks:
        tw = d.textlength(txt, font=fnt)
        x = (W - tw) / 2
        d.rounded_rectangle(
            [x - pad_x, y - pad_y * 0.7, x + tw + pad_x, y + h + pad_y * 0.3],
            radius=int(h * 0.26), fill=(0, 0, 0, 132),
        )
        d.text((x + 3, y + 4), txt, font=fnt, fill=(0, 0, 0, 150))   # shadow
        d.text((x, y), txt, font=fnt, fill=(255, 255, 255, 255))
        y += h + gap

    img.save(path)
    return path


# ---------------------------------------------------------------- assembly

def duration(path):
    out = subprocess.run([FFMPEG, "-hide_banner", "-i", path],
                         capture_output=True, text=True).stderr
    for token in out.split():
        pass
    for line in out.splitlines():
        if "Duration:" in line:
            hms = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = hms.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"no duration for {path}")


def build(spec):
    vo_path = os.path.join(VO, spec["vo"])
    vo_len = duration(vo_path)
    total = round(vo_len + TAIL, 3)
    frames = int(round(total * FPS))

    hook_in, hook_out = spec.get("hook_window", DEFAULT_HOOK_WINDOW)
    end_in = round(vo_len - spec.get("end_lead", DEFAULT_END_LEAD), 2)

    # cards
    os.makedirs(CARDS, exist_ok=True)
    overlays = []   # (png, fade_in_at, fade_out_at_or_None)
    overlays.append((card(f"{CARDS}/{spec['slug']}-hook.png", spec["hook"], 76, spec.get("hook_y", 330)),
                     hook_in, hook_out))
    for i, (t_in, t_out, num, txt) in enumerate(spec.get("items", [])):
        overlays.append((card(f"{CARDS}/{spec['slug']}-item{i+1}.png", txt, 54, 300,
                              number=num), t_in, t_out))
    overlays.append((card(f"{CARDS}/{spec['slug']}-end.png", spec["end"], 64, 1310,
                          align="bottom"), end_in, None))

    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-loop", "1", "-i", os.path.join(IMG, spec["image"])]
    for png, _, _ in overlays:
        cmd += ["-loop", "1", "-i", png]
    cmd += ["-i", vo_path]

    fades = 0.35
    chain = [
        # upscale first so zoompan has pixels to crop into, then push in linearly
        f"[0:v]scale=2160:-2,crop=2160:3840,setsar=1,"
        f"zoompan=z='1+{ZOOM}*on/{frames - 1}':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={W}x{H}:fps={FPS}[bg]"
    ]
    prev = "bg"
    for i, (_, t_in, t_out) in enumerate(overlays, start=1):
        f = [f"[{i}:v]format=rgba",
             f"fade=t=in:st={t_in}:d={fades}:alpha=1"]
        if t_out is not None:
            f.append(f"fade=t=out:st={round(t_out - fades, 2)}:d={fades}:alpha=1")
        chain.append(",".join(f) + f"[o{i}]")
        nxt = f"v{i}"
        window = (f":enable='between(t,{t_in},{t_out})'" if t_out is not None
                  else f":enable='gte(t,{t_in})'")
        chain.append(f"[{prev}][o{i}]overlay=0:0{window}[{nxt}]")
        prev = nxt
    chain.append(f"[{prev}]format=yuv420p[vout]")
    chain.append(f"[{len(overlays) + 1}:a]apad,atrim=0:{total},asetpts=N/SR/TB[aout]")

    out_path = os.path.join(OUT, f"{spec['slug']}.mp4")
    cmd += ["-filter_complex", ";".join(chain),
            "-map", "[vout]", "-map", "[aout]",
            "-t", str(total),
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            out_path]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{spec['slug']}:\n{r.stderr[-3000:]}")
    size = os.path.getsize(out_path) / 1e6
    print(f"{spec['slug']:20s} {total:5.1f}s  {size:5.1f} MB  "
          f"hook {hook_in}-{hook_out}  end from {end_in}")


if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    for spec in VIDEOS:
        if only and spec["slug"] not in only:
            continue
        build(spec)
