"""Worker: speak lines with local Kokoro (free, on this Mac). Runs under the mlx-audio uv tool python.
usage: <mlx-audio python> tools/tts_kokoro.py <jobs.json>   jobs = [{"text": "...", "out": "x.wav", "voice": "am_puck"}]"""
import json, sys, wave
import numpy as np
from mlx_audio.tts.utils import load_model

SR = 24000
jobs = json.load(open(sys.argv[1]))
model = load_model("mlx-community/Kokoro-82M-bf16")
for j in jobs:
    a = np.concatenate([np.array(o.audio, dtype=np.float32).ravel()
                        for o in model.generate(text=j["text"], voice=j.get("voice", "am_puck"), speed=j.get("speed", 1.1), lang_code=j.get("voice", "am_puck")[0])])  # lang a=US, b=UK voices
    pcm = (np.clip(a, -1, 1) * 32767).astype(np.int16)
    with wave.open(j["out"], "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(j["out"], round(len(pcm) / SR, 2))
