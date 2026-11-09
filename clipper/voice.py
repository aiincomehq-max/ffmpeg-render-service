"""Voiceover: our own commentary on every Short (YouTube's reused-content rule wants original commentary, not just
re-posted clips). Claude writes the lines; local Kokoro speaks them (free, on this Mac). CLIPPER_VOICE=0 turns it off.

Lines are written from the moment's transcript/why, so they react to what actually happens on screen.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import wave
from pathlib import Path

from . import ROOT

MODEL = os.environ.get("CLIPPER_VOICE_MODEL", "claude-haiku-5-5")
MLX_PY = Path(os.environ.get("CLIPPER_MLX_PY", Path.home() / ".local/share/uv/tools/mlx-audio/bin/python"))
VOICE = os.environ.get("CLIPPER_VOICE_NAME", "am_puck")
WORKER = ROOT / "tools" / "tts_kokoro.py"

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
    lines = json.loads(next(b.text for b in resp.content if b.type == "text"))["lines"]
    return [l.strip() for l in lines][:n]


STYLE = ("You are the voice of a gaming/streamer clips Shorts channel: a hype, funny narrator reacting to the clip like "
         "a friend watching with you. Plain spoken English, no emojis, no hashtags, no swearing, never say 'subscribe'. "
         "Each line must be about what really happens in the clip (use the details given), never generic. "
         "Never guess anyone's gender: use their name, 'bro', or 'they', never he/she/his/her.")


def ranking_lines(group: list[dict], game: str, channel: str, opener: str = "Number {n}.") -> list[str]:
    """One line per clip, spoken over its first ~2 s. group is ordered #5 -> #1."""
    items = "\n".join(f"#{len(group) - i}: {m.get('hook_tag', '')} | {m.get('why', '')[:200]}" for i, m in enumerate(group))
    return _ask(f"{STYLE}\nThis Short ranks the funniest {game} moments, counting down.\n{items}\n\n"
                f"Write exactly {len(group)} lines, one per clip in this order. Each line starts with '{opener.replace("{n}", "N")}' (N = the rank number) then at "
                f"most 7 more words setting up the clip without spoiling the payoff.", len(group), channel)


def single_lines(m: dict, channel: str) -> list[str]:
    """[intro over the first ~2.5 s, reaction just after the payoff]."""
    return _ask(f"{STYLE}\nClip: {m.get('hook_tag', '')} | {m.get('why', '')[:300]}\n\n"
                "Write exactly 2 lines: 1) an intro hook of at most 9 words that makes people stay to see what happens "
                "(no spoiler); 2) a reaction of at most 5 words said right after the payoff.", 2, channel)


def speak(lines: list[str], workdir: Path | None = None, voice: str | None = None, speed: float | None = None) -> list[tuple[str, float]]:
    """-> [(wav path, seconds)] via the Kokoro worker (separate python: mlx-audio lives in its own uv tool env)."""
    d = Path(workdir or tempfile.mkdtemp(prefix="vo_"))
    d.mkdir(parents=True, exist_ok=True)
    jobs = [{"text": t, "out": str(d / f"vo{i}.wav"), "voice": voice or VOICE, "speed": speed or 1.1} for i, t in enumerate(lines)]
    jf = d / "jobs.json"
    jf.write_text(json.dumps(jobs))
    subprocess.run([str(MLX_PY), str(WORKER), str(jf)], check=True, capture_output=True)
    out = []
    for j in jobs:
        with wave.open(j["out"]) as w:
            out.append((j["out"], w.getnframes() / w.getframerate()))
    return out
