#!/usr/bin/env python3
"""The text-block format, built to the spec taken off @chinglung._.p (1M views).

Five silent ~5.5s verticals: a static light wall, a bold title, ~130 words of
black text present from the first frame and never changing. No voiceover, no
call to action, no movement. The music is added in Instagram's own app at post
time -- baking in a commercial track gets the post muted or pulled, and in-app
audio is part of why these travel.

The video being far shorter than the text takes to read is the mechanic, not a
mistake. The viewer replays or pauses, and the loop is what moves it.
"""
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "build-text")
FONTS = "/mnt/skills/examples/canvas-design/canvas-fonts"
FFMPEG = os.path.expanduser("~/bin/ffmpeg")

W, H, FPS = 1080, 1920, 30
DURATION = 5.5          # matched to the post that did 1M on 4.7K followers
# Measured off the reference frame: body text is roughly 27px at 1080 wide with
# a 35px line gap, in a column about 58% of frame width, starting ~16% down and
# ending ~45% down. Text this small is what stops it reading as a quote graphic.
# Size is auto-fitted rather than fixed. Measuring the reference off a
# low-resolution screenshot produced a number that was too small to read on a
# phone, so the rule is now: take the largest size that still clears the
# subject's head, and let the frame decide.
SIZE_LADDER = [46, 44, 42, 40, 38, 36, 34, 32, 30]   # tried largest first
COL_RATIO = 17.0        # column width as a multiple of body size -> ~7-8 words
SUBJECT_TOP = 0.70      # this plate is clear wall down to 73%
TOP = 230
INK = (26, 24, 22)

POSTS = [
    {
        "slug": "1-cannot-build",
        "title": "The Face You Cannot Build",
        "body": """Close your eyes and picture your
mother. Every line of it is there.

Now picture someone you have not met
yet.

You get a height. A shape. A feeling in
your chest. You do not get a face.

Your mind holds thousands of faces and
cannot build one it has never seen.

Which is strange, because you are
certain you would know them.""",
    },
    {
        "slug": "2-recognise",
        "title": "You Will Recognise Them",
        "body": """You will not meet them and slowly
decide.

You will recognise them in about four
seconds, before you have their name,
and then spend weeks arguing yourself
out of it.

It happens around the eyes. People
always say the eyes.

You will not be able to explain it
without sounding ridiculous, so you
will not try.""",
    },
    {
        "slug": "3-almost-them",
        "title": "Almost Them",
        "body": """It has happened in a supermarket, or
on a train. A stranger, for half a
second, is someone.

Then they turn, and they are not.

That is not loneliness. That is your
mind running a comparison against a
face it has never been shown.

It keeps running it. That is why
strangers keep almost working.""",
    },
    {
        "slug": "4-already-know",
        "title": "What You Already Know",
        "body": """You do not know their face. You know
other things.

Something about their hands. A sense
that they are taller than you expect.
That they are late to things.

That the first thing they ever say to
you will be unremarkable, and you will
remember it for the rest of your life.

None of that is a face. All of it is a
description.""",
    },
    {
        "slug": "5-nothing-happening",
        "title": "Why Nothing Is Happening",
        "body": """Nothing is happening, and it is
exhausting.

You have lost interest in people you
wanted a year ago. Plans have stopped
appealing. You are not sad. You are
idling.

This is what the time before looks like
from the inside. It does not feel like
preparation. It feels like nothing.

You are not falling apart. You are
being cleared out.""",
    },
]


PLATE = os.path.join(HERE, "plates", "wall.png")


def wall(seed):
    """The background photograph.

    A flat phone-camera shot of a plain wall with the back of someone's head
    and shoulder cropped into the bottom-left corner, and the ceiling line in
    the upper left -- the composition the reference post uses. The earlier
    version of this function drew a gradient instead, and that is exactly what
    made the first attempt read as a designed quote card rather than a photo
    someone typed on.

    The first plate had a ceiling line running down to 35% of the frame, which
    left only a 22% band for text and clipped the title. This one is framed with
    no ceiling at all: clear wall from the top edge down to 73%, where the
    subject starts.
    """
    from PIL import Image

    img = Image.open(PLATE).convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img


def _lay_out(d, post, size):
    """Line-break the post at one body size. Returns the lines and the height."""
    from PIL import ImageFont

    title_f = ImageFont.truetype(f"{FONTS}/InstrumentSans-Bold.ttf",
                                 int(size * 1.15))
    body_f = ImageFont.truetype(f"{FONTS}/InstrumentSans-Regular.ttf", size)
    col = size * COL_RATIO
    line_h = int(size * 1.26)
    para_gap = int(size * 0.72)

    rows = [(post["title"], title_f, int(size * 1.15 * 1.8))]
    for para in (" ".join(p.split())
                 for p in post["body"].strip().split("\n\n") if p.strip()):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if d.textlength(trial, font=body_f) <= col or not line:
                line = trial
            else:
                rows.append((line, body_f, line_h))
                line = word
        rows.append((line, body_f, line_h))
        rows.append((None, None, para_gap))

    return rows, sum(h for _, _, h in rows)


def fit_size(posts):
    """One body size for the whole set: the largest that fits every post.

    Per-post sizing looked inconsistent across an account's grid, so the
    longest post decides and the rest match it.
    """
    from PIL import Image, ImageDraw

    d = ImageDraw.Draw(Image.new("RGB", (W, H)))
    budget = H * SUBJECT_TOP - TOP
    for size in SIZE_LADDER:
        if all(_lay_out(d, post, size)[1] <= budget for post in posts):
            return size
    raise RuntimeError("no size fits every post -- shorten the longest one")


def frame(post, size):
    from PIL import ImageDraw

    img = wall(0)
    d = ImageDraw.Draw(img)
    rows, _ = _lay_out(d, post, size)

    y = TOP
    for text, font, h in rows:
        if text is not None:
            tw = d.textlength(text, font=font)
            d.text(((W - tw) / 2, y), text, font=font, fill=INK)
        y += h

    print(f"  {post['slug']:22s} block {TOP/H:.0%}-{y/H:.0%}")
    return img


def build(post, size):
    os.makedirs(OUT, exist_ok=True)
    still = os.path.join(OUT, f"{post['slug']}.png")
    frame(post, size).save(still)

    out = os.path.join(OUT, f"{post['slug']}.mp4")
    # a silent audio track rather than none -- some players mishandle a bare
    # video stream, and the real track gets added in the Instagram app
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-loop", "1", "-i", still,
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
           "-t", str(DURATION),
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "96k", "-shortest", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-2000:])
    words = len(post["body"].split())
    print(f"{post['slug']:22s} {DURATION}s  {words:3d} words  "
          f"{os.path.getsize(out)/1e6:.1f} MB")


if __name__ == "__main__":
    size = fit_size(POSTS)
    print(f"body size for the whole set: {size}px")
    for post in POSTS:
        build(post, size)
