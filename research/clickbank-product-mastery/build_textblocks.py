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
SUBJECT_TOP = 0.575     # the plate's head starts at 59%; stay above it
TOP = 250
INK = (26, 24, 22)

POSTS = [
    {
        "slug": "1-gone-quiet",
        "title": "Soulmate Connection",
        "body": """There is someone who stopped replying
the way they used to. You read it as
losing interest. It is not that.

He decided that wanting it this badly
makes him careless, so he went quiet to
feel in control of something. He is not
with anyone else. He checks. He drafts
things he does not send.

You know this because you have done it,
and called it dignity.

Something in the next two weeks forces
it.""",
    },
    {
        "slug": "2-keeps-coming-back",
        "title": "The One Who Keeps Returning",
        "body": """He has left and come back more than
once, and you have stopped telling your
friends.

He does not come back because he is
bored. He comes back because every
attempt to replace you is a comparison,
and he keeps losing it.

But he has never been the one who
stayed, in any part of his life, and he
does not believe he can start now.

The next time he reaches out it will
not be an apology. It will be a small,
pointless question.""",
    },
    {
        "slug": "3-what-hes-not-saying",
        "title": "What He Is Not Saying",
        "body": """You are reading his silence as
indifference. You are wrong about it.

He rehearses conversations with you
that he never has. There is a version
of this he has never said out loud,
because saying it makes it real, and
real things can be lost.

You both go quiet and call it being
reasonable.

One of you has to stop first. It will
not be him this week.""",
    },
    {
        "slug": "4-not-met-yet",
        "title": "Someone You Have Not Met",
        "body": """This is not about anybody from your
past.

There is a face your mind cannot build.
You get a height, a shape, a feeling in
your chest, and no face, because your
mind cannot construct one it has never
seen.

You are being prepared for someone, and
it does not look like progress. It
looks like losing interest in things
that used to hold you.

You are not falling apart. You are
being cleared out.""",
    },
    {
        "slug": "5-her",
        "title": "She Has Stopped Asking",
        "body": """She was the one making it easy. You let
her. Now she has stopped, and you are
reading it as her cooling off.

It is not that. She has spent months
being the only one who starts things,
and she has made a decision she has not
announced.

She is not angry. Angry would be
easier.

You get a short window. It closes
quietly, and nobody tells you.""",
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

    The subject starts 59% down this plate, so the text block above it never
    collides with the head.
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
