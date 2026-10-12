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
# Reference block: ~19 lines spanning 16%-44% of frame height, so roughly a
# 28px line gap, breaking at ~6-7 words. Tight leading and a narrow column are
# what make it read as typed-on-a-photo rather than as a quote card.
TITLE_SIZE = 29
BODY_SIZE = 26
LINE_H = 31
PARA_GAP = 16
TEXT_W = 430
TOP = 300
INK = (26, 24, 22)

POSTS = [
    {
        "slug": "1-gone-quiet",
        "title": "Soulmate Connection",
        "body": """There is someone who stopped replying
the way they used to. You have read
it as losing interest. It is not that.

He is aware of how much he feels, and
he has decided that wanting it this
badly makes him careless. So he has
gone quiet to feel in control of
something. He is not with anyone else.
He checks. He drafts things he does
not send.

You know this is true because you have
done exactly the same thing and called
it dignity.

Something in the next two weeks forces
it. A message at the wrong hour, or you
see him somewhere you did not expect.
He will not be able to pretend.""",
    },
    {
        "slug": "2-keeps-coming-back",
        "title": "The One Who Keeps Returning",
        "body": """He has left and come back more than
once, and you have stopped telling
your friends about it.

He does not come back because he is
bored. He comes back because every
attempt to replace you is a comparison,
and he keeps losing it.

But he has never once been the person
who stayed, in any part of his life,
and he does not believe he can start
with you. He is waiting to be told he
is already enough as he is. Nobody has
ever told him that.

The next time he reaches out it will
not be an apology. It will be a small,
pointless question. That is what it
looks like when he is frightened.""",
    },
    {
        "slug": "3-what-hes-not-saying",
        "title": "What He Is Not Saying",
        "body": """You are reading his silence as
indifference, and you are wrong
about it.

He is an overthinker. He rehearses
conversations with you that he never
has. There is an entire version of this
he has never said out loud, because
saying it makes it real, and real
things can be lost.

You are more alike than either of you
has admitted. You both go quiet and
call it being reasonable.

One of you has to stop first. It will
not be him this week. It will be you,
and you will do it badly, at a stupid
hour, and it will work anyway.""",
    },
    {
        "slug": "4-not-met-yet",
        "title": "Someone You Have Not Met",
        "body": """This one is not about anybody from
your past.

There is a face your mind cannot build.
You have tried. You get a height, a
shape, a feeling in your chest, and no
face -- because your mind cannot
construct one it has never seen.

That is not a failure of imagination.
It is the only honest thing about it.

You are being prepared for someone, and
the preparation does not look like
progress. It looks like losing interest
in things that used to hold you. People
you wanted a year ago. A job that fits.

You are not falling apart. You are
being cleared out.""",
    },
    {
        "slug": "5-her",
        "title": "She Has Stopped Asking",
        "body": """She was the one making it easy. You
let her. Now she has stopped, and you
are reading it as her cooling off.

It is not that. She has spent months
being the only one who starts things,
and she has made a decision she has
not announced.

She is not angry. Angry would be
easier. She is tired in a way that
does not argue.

There is a specific thing she has been
waiting for you to notice without being
told, and you have walked past it more
than once.

You get a short window. It closes
quietly, and nobody informs you.""",
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


def frame(post, seed):
    from PIL import Image, ImageDraw, ImageFont

    img = wall(seed)
    d = ImageDraw.Draw(img)
    title_f = ImageFont.truetype(f"{FONTS}/InstrumentSans-Bold.ttf", TITLE_SIZE)
    body_f = ImageFont.truetype(f"{FONTS}/InstrumentSans-Regular.ttf", BODY_SIZE)

    paras = [" ".join(p.split())
             for p in post["body"].strip().split("\n\n") if p.strip()]

    y = TOP
    tw = d.textlength(post["title"], font=title_f)
    d.text(((W - tw) / 2, y), post["title"], font=title_f, fill=INK)
    y += int(TITLE_SIZE * 2.0)

    for para in paras:
        line, words = "", para.split()
        out = []
        for word in words:
            trial = (line + " " + word).strip()
            if d.textlength(trial, font=body_f) <= TEXT_W or not line:
                line = trial
            else:
                out.append(line)
                line = word
        out.append(line)
        for ln in out:
            lw = d.textlength(ln, font=body_f)
            d.text(((W - lw) / 2, y), ln, font=body_f, fill=INK)
            y += LINE_H
        y += PARA_GAP

    assert y < H * 0.60, f"{post['slug']}: text block too tall ({y/H:.0%} of frame)"
    return img


def build(post, seed):
    os.makedirs(OUT, exist_ok=True)
    still = os.path.join(OUT, f"{post['slug']}.png")
    frame(post, seed).save(still)

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
    for i, post in enumerate(POSTS):
        build(post, seed=i * 17 + 3)
