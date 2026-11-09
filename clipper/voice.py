"""Voiceover: our own commentary on every Short (YouTube's reused-content rule wants original commentary, not just
re-posted clips). Claude writes the lines; local Kokoro speaks them (free, on this Mac). CLIPPER_VOICE=0 turns it off.

Lines are written from the moment's transcript/why, so they react to what actually happens on screen.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import wave
from pathlib import Path

from . import ROOT

MODEL = os.environ.get("CLIPPER_VOICE_MODEL", "claude-haiku-5-5")
MLX_PY = Path(os.environ.get("CLIPPER_MLX_PY", Path.home() / ".local/share/uv/tools/mlx-audio/bin/python"))
VOICE = os.environ.get("CLIPPER_VOICE_NAME", "am_puck")
WORKER = ROOT / "tools" / "tts_kokoro.py"

GENDERED = re.compile(r"\b(he|she|his|her|him|hers|himself|herself)\b", re.I)
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["lines"],
          "properties": {"lines": {"type": "array", "items": {"type": "string"}}}}


def enabled() -> bool:
    return os.environ.get("CLIPPER_VOICE", "1") == "1" and MLX_PY.exists()


def _ask(prompt: str, n: int, channel: str) -> list[str]:
    import anthropic

    from . import log_usage
    client = anthropic.Anthropic()
    resp = client.messages.create(model=MODEL, max_tokens=3000, messages=[{"role": "user", "content": prompt}],
                                  output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
    log_usage(resp, "voice", channel)
    lines = [l.strip() for l in json.loads(next(b.text for b in resp.content if b.type == "text"))["lines"]][:n]
    if GENDERED.search(" ".join(lines)) and "Rewrite" not in prompt:
        return _ask(prompt + "\nRewrite: you used he/she/his/her/him. Use the name, 'bro' or 'they' instead.", n, channel)
    return lines


STYLE = ("You are the voice of a gaming/streamer clips Shorts channel: a hype, funny narrator reacting to the clip like "
         "a friend watching with you. Plain spoken English, no emojis, no hashtags, no swearing, never say 'subscribe'. "
         "Each line must be about what really happens in the clip (use the details given), never generic. "
         "Never guess anyone's gender: use their name, 'bro', or 'they', never he/she/his/her.")


def ranking_lines(group: list[dict], game: str, channel: str, opener: str = "Number {n}.") -> list[str]:
    """One line per clip, spoken over its first ~2 s. group is ordered #5 -> #1. The rank opener is added here,
    not by the model (9 Nov: the model counted 1,2,3,4 up instead of 5..1)."""
    items = "\n".join(f"#{len(group) - i}: {m.get('hook_tag', '')} | {m.get('why', '')[:200]}" for i, m in enumerate(group))
    bodies = _ask(f"{STYLE}\nThis Short ranks the funniest {game} moments, counting down.\n{items}\n\n"
                  f"Write exactly {len(group)} lines, one per clip in this order. Each line is at most 7 words setting up "
                  "the clip without spoiling the payoff. Do NOT include the rank number.", len(group), channel)
    return [f"{opener.format(n=len(group) - i)} {b}" for i, b in enumerate(bodies)]


ORDINAL = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh"}


def countdown_calls(count: int, look: dict) -> list[str]:
    """Rank calls only, no model call: e.g. 'Coming in at number 5.' ... 'And number one.'
    look: vo_opener ('{n}' / '{ord}'), optional vo_first (top rank) and vo_last (rank 1)."""
    import random

    def pool(key, fallback):
        v = look.get(key + "s") or look.get(key) or fallback  # list ("vo_openers") or single string ("vo_opener")
        return list(v) if isinstance(v, list) else [v]
    mids = pool("vo_opener", "Number {n}.")
    random.shuffle(mids)  # 9 Nov: never the same phrase on every rank, nor the same order every day
    first = random.choice(pool("vo_first", "")) if look.get("vo_firsts", look.get("vo_first")) else None
    if first:  # don't echo the opening's wording later ("At number five" ... "At number 2")
        def lead(s):
            return s.lower().split("{")[0].split("number")[0].split("place")[0].strip(" ,.")
        mids = [t for t in mids if lead(t) != lead(first)] or mids
    out = []
    for i in range(count):
        n = count - i
        if n == count and first:
            tpl = first
        elif n == 1:
            tpl = random.choice(pool("vo_last", "And number one."))
        else:
            tpl = mids[i % len(mids)]
        out.append(tpl.format(n=n, ord=ORDINAL.get(n, str(n))))
    return out


def context_line(m: dict, channel: str) -> str:
    """9 Nov: no-VO channels (Speed/Kai) explain the moment in on-screen text instead: one plain line at the top."""
    p = (f"{STYLE}\nClip: {m.get('hook_tag', '')} | {m.get('why', '')[:300]}\n\n"
         "Write exactly 1 line of at most 7 words and at most 40 characters that tells a viewer what is going on "
         "in this clip (the situation, not the payoff). Use the streamer's name, e.g. 'Speed meets a kid who wants a 1v1'.")
    line = _ask(p, 1, channel)[0].strip().rstrip(".")
    if len(line) > 44:  # 9 Nov: a 52-char line was cut mid-sentence on screen ("...THEN A YOUNG")
        line = _ask(p + f"\nToo long ({len(line)} characters). Max 40.", 1, channel)[0].strip().rstrip(".")
    return line


def single_lines(m: dict, channel: str) -> list[str]:
    """[intro over the first ~2.5 s, reaction just after the payoff]."""
    return _ask(f"{STYLE}\nClip: {m.get('hook_tag', '')} | {m.get('why', '')[:300]}\n\n"
                "Write exactly 2 lines: 1) an intro hook of at most 9 words that makes people stay to see what happens "
                "(no spoiler); 2) a reaction of at most 5 words said right after the payoff.", 2, channel)


EL_MODEL = os.environ.get("CLIPPER_EL_MODEL", "eleven_multilingual_v2")


def _el_speak(text: str, voice_id: str, out: Path) -> None:
    """One ElevenLabs TTS call -> 24 kHz mono WAV. Authorised by the chairman 9 Nov 2026 (guardrail v8 standing
    approval 'voice-turboclipz-'); run the pipeline with RENDER_OBJECTIVE=voice-turboclipz-... on the command."""
    import urllib.request
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=pcm_24000",
        data=json.dumps({"text": text, "model_id": EL_MODEL,
                         "voice_settings": {"stability": 0.4, "similarity_boost": 0.75, "style": 0.35}}).encode(),
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    pcm = urllib.request.urlopen(req, timeout=60).read()
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    with open(ROOT / "data" / "elevenlabs_usage.jsonl", "a") as f:
        f.write(json.dumps({"voice": voice_id, "chars": len(text), "model": EL_MODEL}) + "\n")


def speak(lines: list[str], workdir: Path | None = None, voice: str | None = None, speed: float | None = None,
          el_voice: str | None = None) -> list[tuple[str, float]]:
    """-> [(wav path, seconds)]. ElevenLabs when the channel has an el_voice and ELEVENLABS_API_KEY is set; else (or on
    any ElevenLabs error) the local Kokoro worker (separate python: mlx-audio lives in its own uv tool env)."""
    d = Path(workdir or tempfile.mkdtemp(prefix="vo_"))
    d.mkdir(parents=True, exist_ok=True)
    outs = [d / f"vo{i}.wav" for i in range(len(lines))]
    done = False
    if el_voice and os.environ.get("ELEVENLABS_API_KEY"):
        try:
            for t, o in zip(lines, outs):
                _el_speak(t, el_voice, o)
            done = True
        except Exception as e:
            print(f"  elevenlabs failed ({type(e).__name__}: {str(e)[:80]}) -> kokoro")
    if not done:
        jobs = [{"text": t, "out": str(o), "voice": voice or VOICE, "speed": speed or 1.1} for t, o in zip(lines, outs)]
        jf = d / "jobs.json"
        jf.write_text(json.dumps(jobs))
        subprocess.run([str(MLX_PY), str(WORKER), str(jf)], check=True, capture_output=True)
    out = []
    for o in outs:
        with wave.open(str(o)) as w:
            out.append((str(o), w.getnframes() / w.getframerate()))
    return out
