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

SYSTEM = """You are the clip editor for a YouTube Shorts channel that posts {streamer} livestream edits.
You read a timestamped transcript window and pick the moments that would go viral as 15-58 second Shorts.

What wins on the top streamer-edit channels (deagzzzshorts, Nexxo Recaps, Ironaldox, OnShortz, core_fx, Drayzshorts):
- a clear payoff near the END (a reveal, reaction, success/fail, punchline) the viewer waits for
- wholesome fan / family / kindness moments (the biggest category, 190M-338M views)
- {short} attempting a physical skill or challenge (backflips, races, strength, reflexes) - success or fail
- interactions with famous people, athletes, or the regular crew ({people})
- scares, chaos, ragebait, chat moments, money/numbers

Rules:
- start: a second or two before the setup; end: right after the payoff (hard cut). Length 15-58s.
- payoff_t: the exact second the payoff happens (reaction peak / punchline / landing).
- impact_ts: other strong beats (landings, scares, hits) inside the moment; can be empty.
- hook_tag: the BIG headline on the first frame (0-2.5s) - it decides whether people swipe. ALL CAPS, 3-6 words,
  max 32 characters, letters/numbers/basic punctuation only (NO emoji). Use one of the two proven patterns:
  (a) open loop that makes them wait, WITHOUT revealing the payoff: "WAIT FOR HIS FIRST CUSTOMER",
      "NO WAY HE DID THIS AT THE END", "THE ENDING IS CRAZY", "HE DID NOT SEE THIS COMING";
  (b) name + verb + specific detail (numbers/money/famous people win): "{SHORT} BENCHED 225 COLD",
      "JAMAL ORDERED 12 BUCKETS", "KEVIN HART COOKED {SHORT}".
  It MUST contain one concrete detail - a number, money, a place, a famous name or a specific act - like the
  winners' titles do ("$12,000 RESTAURANT BILL"). Setting up the situation is fine; just don't state the final reaction.
  BANNED: empty teasers with no detail ("WAIT FOR HIS REACTION", "WAIT FOR WHAT HE SAID", "WATCH TILL THE END") and
  flat scene descriptions ("{SHORT} WORKS THE DRIVE-THRU", "{SHORT} MEETS A FAN"). Must be true to the clip.
  Good: "A KID ASKED {SHORT} ONE QUESTION", "{SHORT} JUST GAVE A FAN $10,000", "DELE ALLI DESTROYED HIS CONTROLLER".
- action_tags: 0-3 narrator tags in the middle, e.g. "WAIT FOR IT", "{SHORT} FREAKS OUT", "PASSED", "FAILS".
- skill: pick from the given skill list when {short} attempts a physical/reflex/skill thing, else "none".
- outcome: "success" or "fail" for skill attempts, else "na".
- titles: 3 options using these formulas:
  "No way he [did X] at the end 😳 {tag}" | "[Name] [verb] [specific detail] 😭💀" |
  "{streamer_first} [kind act] ❤️‍🩹❤️‍🩹" | "The ENDING is crazy 💀🔥" | "Bro [did X] 🤯 {tag}"
- virality: 1-10, be harsh; only 7+ is worth posting.

REAL top-performing titles from the leading channels (views), so match this voice, length and emoji use:
338M "iShowSpeed Finally Fought Back in 2026 💪🔥" | 287M "He even got it cleaned, mad respect ❤️‍🩹 ❤️‍🩹"
238M "Old Speed Would Not Hesitate 💀🤣 #ishowspeed #speed #edit" | 232M "We made the right person famous 💖💖"
210M "The ENDING is crazy 💀🔥" | 208M "IShowSpeed free KFC code 😂❤️" | 193M "iShowSpeed Never Forgets His True Fans ❤️‍🩹❤️‍🩹"
149M "Bro got ragebaited at the end 😂😂" | 134M "Bro pulled it off exactly like the real one 😳 #ishowspeed"
108M "Speed has slow reflexes 💀🐌🔥" | 94M "Rakai Accidentally Woke Up Rayquan 😭💀 #shorts"
54M "Bro humbled an Olympic pro🤯 #ishowspeed #edit" | 12M "Lacy Got Hit With A $12,000 Restaurant Bill 😭💸"
Patterns: under ~60 characters; 1-2 emojis repeated at the end (😭💀 ❤️‍🩹❤️‍🩹 😳 🤯 💀🔥); a curiosity gap ("at the end",
"the ENDING", "did NOT see that coming"); specific numbers and money; "Bro ..." voice; name the famous person when one is in it.
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


def _system(ch: dict) -> str:
    base = SYSTEM.format(streamer=ch["streamer"], short=ch["short"], SHORT=ch["short"].upper(),
                         people=", ".join(ch.get("people", [])), tag=ch.get("title_tag", ""),
                         streamer_first=ch["streamer"].split(",")[0])
    from .performance import load_learnings
    own = load_learnings(ch) if ch.get("key") else ""
    return base + ("\n\n" + own if own else "")


def _call(client: anthropic.Anthropic, text: str, skills: list[str], context: str, ch: dict) -> list[dict]:
    kwargs = dict(
        model=ch.get("moments_model", MODEL),  # game channels: Sonnet (half the price; Opus was 90% of spend)
        max_tokens=16000,
        # 10 Nov: prompt caching. The system prompt + output schema (~2.85k of ~3.3k input tokens) is identical for every
        # transcript window of a stream, and windows run back to back, so calls after the first read it at 0.05-0.1x price.
        system=[{"type": "text", "text": _system(ch), "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": f"Stream: {context}\nSkill list: {', '.join(skills)}\n\nTranscript window (seconds):\n{text}"}],
        output_config={"format": {"type": "json_schema", "schema": _schema(skills)}},
    )
    if os.environ.get("CLIPPER_FALLBACKS", "1") == "1":
        resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    else:
        resp = client.messages.create(**kwargs)
    from . import library, log_usage
    log_usage(resp, "moments", library.CHANNEL)
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


def find_moments(transcript: dict, context: str, ch: dict) -> list[dict]:
    skills = load()["formats"]["subversion_comp"]["skills_backlog"]
    client = anthropic.Anthropic()
    found = []
    wins = _windows(transcript["segments"])
    for i, w in enumerate(wins, 1):
        print(f"  moments: window {i}/{len(wins)}", flush=True)
        for m in _call(client, _fmt(w), skills, context, ch):
            if 8 <= m["end"] - m["start"] <= 70 and m["start"] <= m["payoff_t"] <= m["end"]:
                found.append(m)
    found = _dedupe(found)
    words = transcript["words"]
    for m in found:
        m["words"] = [x for x in words if m["start"] <= x["s"] < m["end"]]
        m["success"] = m["outcome"] == "success"
    return found
