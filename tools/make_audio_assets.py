"""Synthesize original, royalty-free SFX and a placeholder phonk-style loop.

Everything here is generated from scratch with numpy, so there is no licensing
issue. Replace assets/music/*.wav with better licensed tracks whenever you like.

    python tools/make_audio_assets.py
"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent / "assets"


def write(path: Path, x: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.clip(x / (np.max(np.abs(x)) + 1e-9) * 0.95, -1, 1)
    stereo = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


def t(sec: float) -> np.ndarray:
    return np.arange(int(SR * sec)) / SR


def env(n: int, attack: float, decay: float) -> np.ndarray:
    tt = np.arange(n) / SR
    a = np.clip(tt / max(attack, 1e-4), 0, 1)
    return a * np.exp(-tt / decay)


def kick(sec=0.5, f0=150, f1=42) -> np.ndarray:
    tt = t(sec)
    f = f1 + (f0 - f1) * np.exp(-tt * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(tt), 0.002, 0.18)


def bass_thud() -> np.ndarray:
    x = kick(0.9, 120, 35) * 1.0
    x += 0.4 * np.tanh(3 * kick(0.9, 90, 30))
    return x


def vine_boom() -> np.ndarray:
    tt = t(1.4)
    f = 32 + 80 * np.exp(-tt * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.tanh(4 * np.sin(ph)) * env(len(tt), 0.003, 0.5)
    return x


def whoosh() -> np.ndarray:
    tt = t(0.6)
    noise = np.random.default_rng(1).standard_normal(len(tt))
    # moving one-pole lowpass sweep
    cut = 300 + 6000 * np.sin(np.pi * tt / tt[-1]) ** 2
    y = np.zeros_like(noise)
    a_prev = 0.0
    for i in range(len(noise)):
        a = np.exp(-2 * np.pi * cut[i] / SR)
        a_prev = (1 - a) * noise[i] + a * a_prev
        y[i] = a_prev
    return y * np.sin(np.pi * tt / tt[-1]) ** 1.5


def riser() -> np.ndarray:
    tt = t(1.2)
    f = 200 + 1800 * (tt / tt[-1]) ** 2
    ph = 2 * np.pi * np.cumsum(f) / SR
    noise = np.random.default_rng(2).standard_normal(len(tt)) * 0.3
    return (np.sin(ph) * 0.6 + noise) * (tt / tt[-1]) ** 2


def ding() -> np.ndarray:
    tt = t(0.9)
    x = np.sin(2 * np.pi * 1760 * tt) + 0.5 * np.sin(2 * np.pi * 2640 * tt) + 0.25 * np.sin(2 * np.pi * 3520 * tt)
    return x * env(len(tt), 0.002, 0.25) + 0.6 * kick(0.9, 110, 40)


def cowbell(sec=0.25) -> np.ndarray:
    tt = t(sec)
    sq = np.sign(np.sin(2 * np.pi * 540 * tt)) + np.sign(np.sin(2 * np.pi * 800 * tt))
    return sq * env(len(tt), 0.001, 0.07)


def phonk_loop(bpm=130, bars=16, seed=0) -> np.ndarray:
    """Original drift-phonk-style loop: kick, clap, hats, cowbell melody, 808."""
    rng = np.random.default_rng(seed)
    beat = 60 / bpm
    step = beat / 4  # 16th notes
    total = int(SR * beat * 4 * bars)
    out = np.zeros(total + SR)

    def place(sig, sec, gain=1.0):
        i = int(sec * SR)
        out[i:i + len(sig)] += sig[: max(0, len(out) - i)] * gain

    scale = [0, 3, 5, 7, 10]  # minor pentatonic, cowbell pitched
    melody = [rng.choice(scale) for _ in range(16)]
    root_hz = 49.0  # G1 808

    for bar in range(bars):
        for s in range(16):
            sec = (bar * 16 + s) * step
            if s in (0, 6, 10):
                place(kick(0.45), sec, 1.0)
            if s in (4, 12):
                clap = rng.standard_normal(int(0.12 * SR)) * env(int(0.12 * SR), 0.001, 0.03)
                place(clap, sec, 0.5)
            if s % 2 == 0:
                hat = rng.standard_normal(int(0.04 * SR)) * env(int(0.04 * SR), 0.0005, 0.008)
                place(np.diff(hat, prepend=0), sec, 0.25)
            if s % 2 == 0 and melody[s] is not None:
                semis = melody[(s + bar) % 16]
                tt = t(0.22)
                f = 540 * 2 ** (semis / 12)
                cb = (np.sign(np.sin(2 * np.pi * f * tt)) + np.sign(np.sin(2 * np.pi * f * 1.48 * tt))) * env(len(tt), 0.001, 0.06)
                place(cb, sec, 0.22)
        # 808 sustained per bar
        tt = t(beat * 3.5)
        semis = scale[bar % len(scale)] if bar % 4 == 3 else 0
        f = root_hz * 2 ** (semis / 12)
        bass = np.tanh(2.5 * np.sin(2 * np.pi * f * tt)) * env(len(tt), 0.005, 1.2)
        place(bass, bar * beat * 4, 0.7)
    return out[:total]


def main() -> None:
    sfx = ROOT / "sfx"
    write(sfx / "bass_thud.wav", bass_thud())
    write(sfx / "vine_boom.wav", vine_boom())
    write(sfx / "whoosh.wav", whoosh())
    write(sfx / "riser.wav", riser())
    write(sfx / "ding.wav", ding())
    write(ROOT / "music" / "placeholder_phonk_130.wav", phonk_loop(130, 16, 0))
    write(ROOT / "music" / "placeholder_phonk_140.wav", phonk_loop(140, 16, 7))
    print("ok")


if __name__ == "__main__":
    main()
