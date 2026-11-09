"""Format presets: moment(s) -> EDL for render.py.

Moment shape (source-video seconds):
{
  "src": "/path/vod.mp4", "start": 812.0, "end": 851.0, "payoff_t": 846.2,
  "impact_ts": [846.2], "hook_tag": "SPEED TRIES THE SNAKE",
  "action_tags": [{"t": 830.0, "text": "WAIT FOR IT"}], "emoji": "💀",
  "words": [{"w": "bro", "s": 812.4, "e": 812.6}, ...], "skill": "reflexes", "success": true,
  "comedic": true
}
"""
from __future__ import annotations

import random
import re

KEEP_GAP = 0.40      # remove silences longer than this
PAD = 0.12           # keep this much around speech when cutting
PROTECT = 1.5        # never cut within +-PROTECT of payoff / impacts
MAX_LEN = 58.0
MIN_LEN = 12.0  # an 8 s Short (Jason 8 Nov) is over before the hook lands
HOOK_S = 2.5        # big opening hook text on screen 0..HOOK_S


def _speech_ranges(m: dict) -> list[tuple[float, float]]:
    """Ranges of the source to keep: everything except long silences, protecting payoff/impacts."""
    s0, s1 = m["start"], m["end"]
    words = [w for w in m.get("words", []) if s0 <= w["s"] < s1]
    protect = [(t - PROTECT, t + PROTECT) for t in [m.get("payoff_t"), *m.get("impact_ts", [])] if t is not None]

    def protected(a: float, b: float) -> bool:
        return any(a < pb and b > pa for pa, pb in protect)

    cuts = []
    prev_end = s0
    for w in words + [{"s": s1, "e": s1}]:
        gap_a, gap_b = prev_end + PAD, w["s"] - PAD
        if w["s"] - prev_end > KEEP_GAP and gap_b > gap_a and not protected(gap_a, gap_b):
            cuts.append((gap_a, gap_b))
        prev_end = max(prev_end, w["e"])
    keep, cur = [], s0
    for a, b in cuts:
        if a > cur:
            keep.append((cur, a))
        cur = b
    if s1 > cur:
        keep.append((cur, s1))
    return [(a, b) for a, b in keep if b - a > 0.05]


class Timeline:
    """Maps source time -> output time through a list of pieces."""

    def __init__(self):
        self.pieces: list[dict] = []
        self.out_t = 0.0
        self._map: list[tuple[float, float, float, float]] = []  # (src_a, src_b, out_a, speed)

    def add(self, src: str, a: float, b: float, speed: float = 1.0, zoom: float = 1.0, shake: bool = False):
        if b - a <= 0.03:
            return
        self.pieces.append({"src": src, "start": round(a, 3), "end": round(b, 3), "speed": speed, "zoom": zoom, "shake": shake})
        self._map.append((a, b, self.out_t, speed))
        self.out_t += (b - a) / speed

    def to_out(self, t: float) -> float | None:
        for a, b, oa, sp in self._map:
            if a <= t <= b:
                return oa + (t - a) / sp
        return None


def hook_text(tag: str, max_chars: int = 34) -> str:
    """Frame-1 hook: the font has no emoji glyphs and 120px fits ~2 lines, so keep plain text, cut at a word."""
    t = re.sub(r"[^A-Za-z0-9 '!?$%&.,#:-]", "", tag).replace("*", "").strip().upper()
    t = re.sub(r"\s+", " ", t)
    if len(t) > max_chars:
        t = t[:max_chars].rsplit(" ", 1)[0]
        # never end on a dangling word ("...XXXTENTACION AT A")
        while t.split(" ")[-1] in DANGLING and " " in t:
            t = t.rsplit(" ", 1)[0]
    return t


DANGLING = {"A", "AN", "THE", "AT", "TO", "OF", "IN", "ON", "FOR", "AND", "WITH", "HIS", "HER", "MY", "BY", "FROM", "IS", "WAS", "BUT", "OR"}


def kept_len(m: dict) -> float:
    """Seconds of the moment left after silence cuts (before MAX_LEN trim)."""
    return sum(b - a for a, b in _speech_ranges(m))


def single_moment(m: dict, style: dict, handle: str, music: str | None) -> dict:
    tl = Timeline()
    payoff = m.get("payoff_t")
    for a, b in _speech_ranges(m):
        if payoff is not None and a <= payoff < b:
            p0, p1 = payoff - 0.05, min(b, payoff + 0.7)
            tl.add(m["src"], a, p0)
            tl.add(m["src"], p0, p1, zoom=1.15, shake=True)
            tl.add(m["src"], p1, b)
        else:
            tl.add(m["src"], a, b)
        if tl.out_t >= MAX_LEN:
            break
    # trim to MAX_LEN
    total = 0.0
    trimmed = []
    for p in tl.pieces:
        d = (p["end"] - p["start"]) / p["speed"]
        if total + d > MAX_LEN:
            p = dict(p, end=p["start"] + (MAX_LEN - total) * p["speed"])
            trimmed.append(p)
            break
        trimmed.append(p)
        total += d
    tl.pieces = trimmed
    duration = min(tl.out_t, MAX_LEN)

    words = []
    # 8 Nov: Kai's stream has its own captions burned in; a second caption track on top is unreadable
    for w in ([] if m.get("burned_captions") else m.get("words", [])):
        s, e = tl.to_out(w["s"]), tl.to_out(w["e"])
        if s is not None and s < duration:
            words.append({"w": w["w"], "s": round(s, 3), "e": round(e if e is not None else s + 0.2, 3)})

    texts = []
    if m.get("hook_tag"):
        texts.append({"text": hook_text(m["hook_tag"]), "start": 0.0, "end": HOOK_S, "kind": "hook", "color": "yellow", "y_pct": 24})
    for tag in m.get("action_tags", []):
        t = tl.to_out(tag["t"])
        if t is not None and t > HOOK_S:
            texts.append({"text": f"*{hook_text(tag['text'], 40)}*", "start": round(t, 3), "end": round(min(duration, t + 1.6), 3), "kind": "tag", "color": "yellow", "y_pct": 36})

    impacts = []
    pay_out = tl.to_out(payoff) if payoff is not None else None
    if pay_out is not None:
        impacts.append({"t": round(pay_out, 3), "flash": "white", "sfx": "bass_thud", "emoji": m.get("emoji", "😭"), "emoji_y_pct": 74, "emoji_dur": 1.4})
    for t in m.get("impact_ts", []):
        o = tl.to_out(t)
        if o is not None and (pay_out is None or abs(o - pay_out) > 0.5):
            impacts.append({"t": round(o, 3), "flash": "red", "sfx": "bass_thud", "emoji": None})
    drop = pay_out if pay_out is not None else duration * 0.35
    drop = min(drop, duration * 0.45)
    wholesome = m.get("type") == "wholesome"
    if wholesome:
        # deagzzz-style: no hard flash/thud, soft heart pop, emotional bed from the start, no comedic end sfx
        impacts = [dict(i, flash=None, sfx=None, emoji=i.get("emoji") and "❤️‍🩹") for i in impacts]
        drop = 0.0
    return {
        "format": "wholesome_fan" if wholesome else "single_moment",
        "pieces": tl.pieces,
        "words": words,
        "texts": texts,
        "impacts": impacts,
        "music": {"file": music, "drop_t": round(drop, 3)} if music else None,
        "handle": handle,
        "end_sfx": {"t": max(0.0, duration - 1.2), "sfx": "vine_boom"} if m.get("comedic") and not wholesome else None,
        "caption_active": "#FFD700" if wholesome else "#00FF44",
        "vo_slots": [0.3] + ([round(pay_out + 0.8, 3)] if pay_out is not None and pay_out + 2.5 < duration else []),
    }


def subversion_comp(claim: str, fail: dict, successes: list[dict], style: dict, handle: str, music: str | None,
                    seed: int | None = None, name: str = "Speed") -> dict:
    """Drayzshorts format: '{NAME} CANT X' -> clip1 (supports claim) -> 'ARE YOU SURE?' -> 5 clips proving the opposite."""
    rng = random.Random(seed)
    tl = Timeline()
    # clip 1: the "evidence" for the ironic claim, ~3s around its impact
    fi = fail.get("payoff_t") or (fail["start"] + fail["end"]) / 2
    tl.add(fail["src"], max(fail["start"], fi - 2.2), min(fail["end"], fi + 1.0))
    clip_starts, slow_starts = [], []
    for m in successes[:5]:
        it = (m.get("impact_ts") or [m.get("payoff_t")])[0]
        clip_starts.append(tl.out_t)
        pre_a = max(m["start"], it - 1.45)
        tl.add(m["src"], pre_a, it - 0.15)
        slow_starts.append(tl.out_t)
        tl.add(m["src"], it - 0.15, it + 0.45, speed=0.35, zoom=1.15)
        tl.add(m["src"], it + 0.45, min(m["end"], it + 0.9))
    duration = tl.out_t
    clip3 = clip_starts[1] if len(clip_starts) > 1 else clip_starts[0]
    texts = [
        {"text": f'"{name.upper()} {claim.upper()}"', "start": 0.0, "end": round(clip3, 3), "kind": "header", "color": "yellow", "y_pct": 8},
        {"text": "ARE YOU SURE?", "start": round(clip3, 3), "end": round(min(duration, clip3 + 1.7), 3), "kind": "header", "color": "white", "y_pct": 8},
    ]
    emojis = ["💀", "🤯"]
    impacts = [{"t": round(t, 3), "flash": None, "sfx": "bass_thud", "emoji": emojis[i % 2] if rng.random() > 0.15 else "💀",
                "emoji_y_pct": 72, "emoji_dur": 1.2}
               for i, t in enumerate(slow_starts)]
    return {
        "format": "subversion_comp",
        "pieces": tl.pieces,
        "words": [],
        "texts": texts,
        "impacts": impacts,
        "music": {"file": music, "drop_t": round(clip3, 3)} if music else None,
        "handle": handle,
        "end_sfx": None,
        "title": f"{name} {claim.lower()} 💀{successes[0].get('topic_emoji', '')}🔥".replace("  ", " "),
    }


RANK_PRE, RANK_POST = 5.0, 2.5  # seconds kept before/after each moment's payoff (~7.5 s a clip, 5 clips ≈ 40 s)


_IRREG = {"IS": "ARE", "WAS": "WERE", "HAS": "HAVE", "DOES": "DO", "DOESN'T": "DON'T", "ISN'T": "AREN'T", "WASN'T": "WEREN'T"}


def neutral(t: str) -> str:
    """9 Nov: game channels clip many streamers and the library doesn't know who is male or female, so
    on-screen labels never guess: HE/SHE -> THEY (verb agreed), HIS/HIM/HER -> THEIR/THEM."""
    w = t.split(" ")
    out = []
    i = 0
    while i < len(w):
        u = w[i].upper()
        core = re.sub(r"[^A-Z']", "", u)
        tail = u[len(core):] if u.startswith(core) else ""
        if core in ("HE", "SHE"):
            out.append("THEY" + tail)
            if i + 1 < len(w):
                v = w[i + 1].upper()
                if v in _IRREG:
                    v = _IRREG[v]
                elif re.fullmatch(r"[A-Z]+IES", v):
                    v = v[:-3] + "Y"
                elif re.fullmatch(r"[A-Z]+(SH|CH|X|SS|O)ES", v):
                    v = v[:-2]
                elif re.fullmatch(r"[A-Z]+[^S]S", v):
                    v = v[:-1]
                out.append(v)
                i += 2
                continue
        elif core in ("HE'S", "SHE'S"):
            out.append("THEY'RE" + tail)
        elif core in ("HIS",):
            out.append("THEIR" + tail)
        elif core in ("HIM", "HIMSELF", "HERSELF"):
            out.append(("THEMSELVES" if core.endswith("SELF") else "THEM") + tail)
        elif core == "HER":
            nxt = w[i + 1] if i + 1 < len(w) else ""
            out.append(("THEIR" if nxt and not tail else "THEM") + tail)
        else:
            out.append(w[i])
        i += 1
    return " ".join(out)


def ranking_comp(ms: list[dict], game: str, handle: str, music: str | None, look: dict | None = None) -> dict:
    """'Ranking the funniest {game} moments' (the format breaking out on tiny channels, Nov 2026 vidIQ):
    5 clips counted down #5 -> #1, strongest last, a white flash + thud on each payoff."""
    look = look or {}  # per-channel look (channels.json rank_style) so channels on one account are not one template
    ms = ms[:5]
    tl = Timeline()
    words, texts, impacts, slots = [], [], [], []
    for rank, m in zip(range(len(ms), 0, -1), ms):
        pay = m.get("payoff_t") or (m["start"] + m["end"]) / 2
        a, b = max(m["start"], pay - RANK_PRE), min(m["end"], pay + RANK_POST)
        o0 = tl.out_t
        tl.add(m["src"], a, b)
        if look.get("layout") and tl.pieces:
            tl.pieces[-1]["layout"] = look["layout"]  # "game": centre of the game screen big, blurred fill (9 Nov)
        o1 = tl.out_t
        slots.append(round(o0 + 0.1, 3))
        texts.append({"text": look.get("rank_fmt", "#{n}").format(n=rank), "start": round(o0, 3), "end": round(o1, 3), "kind": "hook",
                      "color": look.get("rank_color", "yellow"), "y_pct": look.get("rank_y", 22)})
        if m.get("hook_tag"):
            texts.append({"text": hook_text(neutral(m["hook_tag"]), 30), "start": round(o0, 3), "end": round(min(o1, o0 + 2.5), 3),
                          "kind": "tag", "color": look.get("tag_color", "white"), "y_pct": look.get("rank_y", 22) + 10})
        if not m.get("burned_captions"):
            for w in m.get("words", []):
                if a <= w["s"] < b:
                    words.append({"w": w["w"], "s": round(o0 + w["s"] - a, 3), "e": round(o0 + min(w["e"], b) - a, 3)})
        impacts.append({"t": round(o0 + pay - a, 3), "flash": "white", "sfx": "bass_thud", "emoji": m.get("emoji") or look.get("emoji", "💀"),
                        "emoji_y_pct": 74, "emoji_dur": 1.2})
    title = look.get("header", "RANKING THE FUNNIEST {GAME} MOMENTS").format(GAME=game.upper(), game=game)
    texts.insert(0, {"text": title, "start": 0.0, "end": round(tl.out_t, 3), "kind": "header", "color": look.get("header_color", "white"), "y_pct": 8})
    return {
        "format": "ranking_comp",
        "pieces": tl.pieces,
        "words": words,
        "texts": texts,
        "impacts": impacts,
        "music": {"file": music, "drop_t": 0.0} if music else None,
        "handle": handle,
        "end_sfx": None,
        "caption_active": look.get("caption_active", "#00FF44"),
        "title": (look.get("titles") or [f"Ranking the funniest {game} moments 😭💀"])[0].format(game=game),
        "vo_slots": slots,
    }
