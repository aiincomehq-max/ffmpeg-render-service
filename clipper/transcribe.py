"""Word-level transcription with faster-whisper (cached per VOD)."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from . import ROOT

CACHE = ROOT / "data" / "transcripts"


def extract_audio(video: Path) -> Path:
    wav = video.with_suffix(".16k.wav")
    if not wav.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    return wav


def transcribe(video: Path, key: str, model_name: str | None = None) -> dict:
    """Returns {"segments": [{"s","e","text"}], "words": [{"w","s","e"}]} in source seconds."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    from faster_whisper import WhisperModel  # heavy import, only when needed

    model_name = model_name or os.environ.get("CLIPPER_WHISPER", "small.en")
    model = WhisperModel(model_name, device="auto", compute_type="int8")
    wav = extract_audio(video)
    segs, _ = model.transcribe(str(wav), word_timestamps=True, vad_filter=True, language="en")
    out = {"segments": [], "words": []}
    for s in segs:
        out["segments"].append({"s": round(s.start, 2), "e": round(s.end, 2), "text": s.text.strip()})
        for w in s.words or []:
            out["words"].append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
        print(f"\r  transcribed {s.end / 60:6.1f} min", end="", flush=True)
    print()
    cache.write_text(json.dumps(out))
    return out
