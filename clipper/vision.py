"""Visual QA gate: Claude looks at frames from a candidate moment before we spend a render on it.

Rejects moments that only work as audio (nothing to see, streamer off-screen, black/loading screens)
and corrects payoff_t to the frame where the payoff is actually visible.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import tempfile
from pathlib import Path

import anthropic

from .moments import MODEL

N_FRAMES = 8

SCHEMA = {
    "type": "object",
    "properties": {
        "keep": {"type": "boolean"},
        "payoff_frame": {"type": "integer"},
        "visual_score": {"type": "integer"},
        "reason": {"type": "string"},
        "burned_captions": {"type": "boolean"},
    },
    "required": ["keep", "payoff_frame", "visual_score", "reason", "burned_captions"],
    "additionalProperties": False,
}


def _frames(src: str, times: list[float]) -> list[bytes]:
    out = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(times):
            f = Path(td) / f"{i}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                            "-vf", "scale=640:-2", "-q:v", "4", str(f)], check=True)
            out.append(f.read_bytes())
    return out


STREAMER_RULE = ("keep=false if the moment would be boring to WATCH: streamer not visible in most frames, static/black/"
                 "loading/menu screens, the payoff happens off-camera, or the streamer is only a small corner facecam over a "
                 "still image / game / screen-share (the 9:16 crop will lose them). ")
# game channels (Roblox etc.): the GAME is the show, a facecam is optional
GAMEPLAY_RULE = ("keep=false if the moment would be boring to WATCH: static/black/loading/menu screens, nothing happening "
                 "on screen, or the payoff happens off-screen. Gameplay with no facecam is FINE if the action in the "
                 "centre of the frame shows the payoff (the 9:16 crop keeps the centre). ")


def check(m: dict, ch: dict, client: anthropic.Anthropic | None = None) -> dict:
    """Returns {"keep", "payoff_t", "visual_score", "reason"}. Fails open (keep) on any error."""
    try:
        client = client or anthropic.Anthropic()
        span = m["end"] - m["start"]
        times = [m["start"] + span * (i + 0.5) / N_FRAMES for i in range(N_FRAMES)]
        # make sure the claimed payoff is one of the frames
        j = min(range(N_FRAMES), key=lambda i: abs(times[i] - m["payoff_t"]))
        times[j] = m["payoff_t"]
        content = []
        for i, (t, img) in enumerate(zip(times, _frames(m["src"], times))):
            content.append({"type": "text", "text": f"Frame {i} (t={t - m['start']:.1f}s)"})
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                        "data": base64.standard_b64encode(img).decode()}})
        content.append({"type": "text", "text": (
            f"These are {N_FRAMES} frames from a candidate {ch['streamer']} Short (cropped to 9:16 later).\n"
            f"Planned hook: {m.get('hook_tag')}. Why it was picked: {m.get('why')}.\n"
            f"Transcript-estimated payoff is frame {j}.\n"
            + (GAMEPLAY_RULE if ch.get("gameplay_ok") else STREAMER_RULE) +
            "payoff_frame = the frame where the payoff is "
            "most visible. visual_score 1-10 for how watchable it is on a phone. burned_captions=true if the footage "
            "already shows its own subtitles of the speech (stream caption overlay or a previous edit's captions).")})
        kwargs = dict(model=MODEL, max_tokens=4000, messages=[{"role": "user", "content": content}],
                      output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
        if os.environ.get("CLIPPER_FALLBACKS", "1") == "1":
            resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
        else:
            resp = client.messages.create(**kwargs)
        from . import library, log_usage
        log_usage(resp, "vision", library.CHANNEL)
        if resp.stop_reason == "refusal":
            return {"keep": True, "payoff_t": m["payoff_t"], "visual_score": None, "reason": "vision refused"}
        r = json.loads(next(b.text for b in resp.content if b.type == "text"))
        pf = max(0, min(N_FRAMES - 1, r["payoff_frame"]))
        return {"keep": r["keep"], "payoff_t": times[pf], "visual_score": r["visual_score"], "reason": r["reason"],
                "burned_captions": bool(r.get("burned_captions"))}
    except Exception as e:  # never block the pipeline on QA
        return {"keep": True, "payoff_t": m.get("payoff_t"), "visual_score": None, "reason": f"vision check skipped: {e}"}
