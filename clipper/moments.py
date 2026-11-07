"""Find clip-worthy moments in a transcript with the Claude API (structured JSON output)."""
from __future__ import annotations

import json
import os

import anthropic

from .style import load

MODEL = os.environ.get("CLIPPER_MODEL", "claude-opus-5-5")
WINDOW_S = 8 * 60
OVERLAP_S = 60
EMOJIS = ["💀", "🤯", "😭", "😂", "🥶", "❤️‍🩹", "💖", "🔥", "😳"]

SYSTEM = """You are the clip editor for a YouTube Shorts channel that posts iShowSpeed livestream edits.
You read a timestamped transcript window and pick the moments that would go viral as 15-58 second Shorts.

What wins on the top Speed edit channels (deagzzzshorts, Nexxo Recaps, Ironaldox, wklerClips, Drayzshorts):
- a clear payoff near the END (a reveal, reaction, success/fail, punchline) the viewer waits for
- wholesome fan / family / kindness moments (the biggest category, 190M-338M views)
- Speed attempting a physical skill or challenge (backflips, races, strength, reflexes) - success or fail
- celebrity/athlete interactions (Ronaldo, MrBeast, Kai Cenat, KSI, athletes)
- scares, chaos, ragebait, chat moments, money/numbers

Rules:
- start: a second or two before the setup; end: right after the payoff (hard cut). Length 15-58s.
- payoff_t: the exact second the payoff happens (reaction peak / punchline / landing).
- impact_ts: other strong beats (landings, scares, hits) inside the moment; can be empty.
- hook_tag: 2-6 word narrator caption shown at 0-2s, ALL CAPS, e.g. "SPEED MEETS HIS BIGGEST FAN".
- action_tags: 0-3 narrator tags in the middle, e.g. "WAIT FOR IT", "SPEED FREAKS OUT", "PASSED", "FAILS".
- skill: pick from the given skill list when Speed attempts a physical/reflex/skill thing, else "none".
- outcome: "success" or "fail" for skill attempts, else "na".
- titles: 3 options using these formulas:
  "No way he [did X] at the end 😳 #ishowspeed" | "[Name] [verb] [specific detail] 😭💀" |
  "iShowSpeed [kind act] ❤️‍🩹❤️‍🩹" | "The ENDING is crazy 💀🔥" | "Bro [did X] 🤯 #ishowspeed #edit"
- virality: 1-10, be harsh; only 7+ is worth posting.
- Use only timestamps that exist in the transcript window. Return an empty list if nothing is good."""


def _schema(skills: list[str]) -> dict:
    moment = {
        "type": "object",
        "properties": {
            "start": {"type": "number"}, "end": {"type": "number"}, "payoff_t": {"type": "number"},
            "impact_ts": {"type": "array", "items": {"type": "number"}},
            "type": {"type": "string", "enum": ["wholesome", "skill", "funny", "scary", "celebrity", "drama", "chaos", "other"]},
            "skill": {"type": "string", "enum": skills + ["none"]},
            "outcome": {"type": "string", "enum": ["success", "fail", "na"]},
            "people": {"type": "array", "items": {"type": "string"}},
            "hook_tag": {"type": "string"},
            "action_tags": {"type": "array", "items": {
                "type": "object", "properties": {"t": {"type": "number"}, "text": {"type": "string"}},
                "required": ["t", "text"], "additionalProperties": False}},
            "emoji": {"type": "string", "enum": EMOJIS},
            "comedic": {"type": "boolean"},
            "virality": {"type": "integer"},
            "titles": {"type": "array", "items": {"type": "string"}},
            "why": {"type": "string"},
        },
        "required": ["start", "end", "payoff_t", "impact_ts", "type", "skill", "outcome", "people", "hook_tag",
                     "action_tags", "emoji", "comedic", "virality", "titles", "why"],
        "additionalProperties": False,
    }
    return {"type": "object", "properties": {"moments": {"type": "array", "items": moment}},
            "required": ["moments"], "additionalProperties": False}


def _windows(segments: list[dict]) -> list[list[dict]]:
    if not segments:
        return []
    end = segments[-1]["e"]
    out, t = [], segments[0]["s"]
    while t < end:
        w = [s for s in segments if s["s"] >= t and s["s"] < t + WINDOW_S]
        if w:
            out.append(w)
        t += WINDOW_S - OVERLAP_S
    return out


def _fmt(segs: list[dict]) -> str:
    return "\n".join(f"[{s['s']:.1f}-{s['e']:.1f}] {s['text']}" for s in segs)


def _call(client: anthropic.Anthropic, text: str, skills: list[str], context: str) -> list[dict]:
    kwargs = dict(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Stream: {context}\nSkill list: {', '.join(skills)}\n\nTranscript window (seconds):\n{text}"}],
        output_config={"format": {"type": "json_schema", "schema": _schema(skills)}},
    )
    if os.environ.get("CLIPPER_FALLBACKS", "1") == "1":
        resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    else:
        resp = client.messages.create(**kwargs)
    if resp.stop_reason == "refusal":
        return []
    txt = next((b.text for b in resp.content if b.type == "text"), "")
    try:
        return json.loads(txt).get("moments", [])
    except json.JSONDecodeError:
        return []


def _dedupe(ms: list[dict]) -> list[dict]:
    ms = sorted(ms, key=lambda m: -m["virality"])
    kept = []
    for m in ms:
        overlap = any(min(m["end"], k["end"]) - max(m["start"], k["start"]) > 0.5 * (m["end"] - m["start"]) for k in kept)
        if not overlap:
            kept.append(m)
    return sorted(kept, key=lambda m: m["start"])


def find_moments(transcript: dict, context: str) -> list[dict]:
    skills = load()["formats"]["subversion_comp"]["skills_backlog"]
    client = anthropic.Anthropic()
    found = []
    wins = _windows(transcript["segments"])
    for i, w in enumerate(wins, 1):
        print(f"  moments: window {i}/{len(wins)}", flush=True)
        for m in _call(client, _fmt(w), skills, context):
            if 8 <= m["end"] - m["start"] <= 70 and m["start"] <= m["payoff_t"] <= m["end"]:
                found.append(m)
    found = _dedupe(found)
    words = transcript["words"]
    for m in found:
        m["words"] = [x for x in words if m["start"] <= x["s"] < m["end"]]
        m["success"] = m["outcome"] == "success"
    return found
