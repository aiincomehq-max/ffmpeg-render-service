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
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True)
    return wav


def load_wav(wav: Path):
    """16 kHz mono 16-bit WAV -> float32 array in [-1, 1]. We decode it ourselves because faster-whisper's
    own decoder (PyAV) breaks on new PyAV releases (`open() got an unexpected keyword 'metadata_errors'`)."""
    import wave

    import numpy as np

    with wave.open(str(wav), "rb") as f:
        assert f.getframerate() == 16000 and f.getnchannels() == 1 and f.getsampwidth() == 2, "expected 16k mono s16"
        pcm = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2")
    return pcm.astype(np.float32) / 32768.0


def transcribe(video: Path, key: str, model_name: str | None = None, words: bool = True) -> dict:
    """Returns {"segments": [{"s","e","text"}], "words": [{"w","s","e"}]} in source seconds."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / f"{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    from faster_whisper import WhisperModel  # heavy import, only when needed

    model_name = model_name or os.environ.get("CLIPPER_WHISPER", "small.en")
    model = WhisperModel(model_name, device="auto", compute_type="int8")
    wav = extract_audio(video)
    segs, _ = model.transcribe(load_wav(wav), word_timestamps=words, vad_filter=True, language="en")
    out = {"segments": [], "words": []}
    for s in segs:
        out["segments"].append({"s": round(s.start, 2), "e": round(s.end, 2), "text": s.text.strip()})
        for w in s.words or []:
            out["words"].append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
        print(f"\r  transcribed {s.end / 60:6.1f} min", end="", flush=True)
    print()
    cache.write_text(json.dumps(out))
    return out
