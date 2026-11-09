"""EDL -> finished 1080x1920 Short via ffmpeg.

EDL shape (all times in OUTPUT seconds except piece src ranges):
{
  "pieces":  [{"src": path, "start": s, "end": e, "speed": 1.0, "zoom": 1.0, "shake": false}],
  "words":   [{"w": "hello", "s": 0.1, "e": 0.4}],          # captions (output timeline), optional
  "caption_active": "#00FF44",
  "texts":   [{"text": "*WAIT FOR IT*", "start": 1.0, "end": 2.5, "kind": "tag|header", "color": "#FFD700", "y_pct": 50}],
  "impacts": [{"t": 3.2, "flash": "white|red|green|null", "sfx": "bass_thud|null", "emoji": "💀|null", "emoji_y_pct": 62}],
  "music":   {"file": path, "drop_t": 3.0} | null,
  "handle":  "@yourhandle",
  "end_sfx": {"t": 20.0, "sfx": "vine_boom"} | null
}
"""
from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
from pathlib import Path

from . import ASSETS
from . import ass as A
from .style import color, emoji_name

W, H, FPS, SR = 1080, 1920, 30, 44100


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(cmd[:6])}...\n{p.stderr[-3000:]}")
    return p.stdout


def has_audio(path: str) -> bool:
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", path])
    return bool(out.strip())


def probe_duration(path: str) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())


def atempo_chain(speed: float) -> str:
    parts, s = [], speed
    while s < 0.5:
        parts.append("atempo=0.5")
        s /= 0.5
    while s > 2.0:
        parts.append("atempo=2.0")
        s /= 2.0
    parts.append(f"atempo={s:.4f}")
    return ",".join(parts)


def db(x: float) -> float:
    return 10 ** (x / 20)


def piece_duration(p: dict) -> float:
    return (p["end"] - p["start"]) / p.get("speed", 1.0)


def probe_dims(path: str) -> tuple[int, int]:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path])
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def _interp(kf: list[tuple[float, int]], hz: float = 15) -> list[tuple[float, int]]:
    if len(kf) < 2:
        return kf
    out = []
    for (t0, x0), (t1, x1) in zip(kf, kf[1:]):
        n = max(1, int((t1 - t0) * hz))
        for i in range(n):
            out.append((t0 + (t1 - t0) * i / n, int(round(x0 + (x1 - x0) * i / n))))
    out.append(kf[-1])
    return out


def render_piece(p: dict, out: Path) -> None:
    speed = p.get("speed", 1.0)
    zoom = max(p.get("zoom", 1.0), 1.06 if p.get("shake") else 1.0)
    src_dur = p["end"] - p["start"]
    shake = "+14*sin(t*55)" if p.get("shake") else ""
    shake_y = "+10*cos(t*47)" if p.get("shake") else ""
    kf = None
    if p.get("layout") == "stack" and p.get("rects"):
        # 9 Nov: webcam panel on top (y 460-1060), gameplay below (1060-1880), blurred frame behind, text bands free.
        from .track import CAM_PANEL, GAME_PANEL
        cx, cy, cw, ch = p["rects"]["cam"]
        gx, gy, gw, gh = p["rects"]["game"]
        if zoom > 1.0:  # payoff punch-in on the gameplay
            nw, nh = int(gw / zoom) // 2 * 2, int(gh / zoom) // 2 * 2
            gx, gy, gw, gh = gx + (gw - nw) // 2, gy + (gh - nh) // 2, nw, nh
        vf = (
            f"setpts=(PTS-STARTPTS)/{speed},split=3[bg][c][g];"
            f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:2,eq=brightness=-0.15[bgb];"
            f"[c]crop={cw}:{ch}:{cx}:{cy},scale={CAM_PANEL[0]}:{CAM_PANEL[1]}[cs];"
            f"[g]crop={gw}:{gh}:x='{gx}{shake}':y='{gy}{shake_y}',scale={GAME_PANEL[0]}:{GAME_PANEL[1]}[gs];"
            f"[bgb][cs]overlay=0:460[t];[t][gs]overlay=0:1060,setsar=1,fps={FPS},format=yuv420p"
        )
        return _encode_piece(p, vf, speed, src_dur, out)
    if p.get("layout") == "game":
        # 9 Nov: a face-tracked 9:16 slice of a game stream showed walls/sky, the character was cut off.
        # Game layout = the middle of the screen (64% of the width, full height) big in the centre,
        # a blurred, darkened copy of the same frame filling the top and bottom.
        fw = f"trunc(iw*0.64/{zoom}/2)*2"
        fh = f"trunc(ih/{zoom}/2)*2"
        vf = (
            f"setpts=(PTS-STARTPTS)/{speed},split[bg][fg];"
            f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:2,eq=brightness=-0.12[bgb];"
            f"[fg]crop={fw}:{fh}:x='(iw-ow)/2{shake}':y='(ih-oh)/2{shake_y}',scale={W}:-2[fgs];"
            f"[bgb][fgs]overlay=(W-w)/2:(H-h)/2,setsar=1,fps={FPS},format=yuv420p"
        )
        return _encode_piece(p, vf, speed, src_dur, out)
    if p.get("track", True) and os.environ.get("CLIPPER_TRACK", "1") == "1":
        try:
            from .track import crop_keyframes
            sw, sh = probe_dims(p["src"])
            kf = crop_keyframes(p["src"], p["start"], p["end"], sw, sh, W, H, zoom, speed)
        except Exception as e:  # tracking is best-effort; never block a render
            print(f"  (tracking skipped: {e})")
            kf = None
    if kf:
        if p.get("shake"):
            mid = kf[len(kf) // 2][1]
            xexpr, cmd = f"{mid}{shake}", ""
        else:
            cmdfile = out.with_suffix(".cmd")
            cmdfile.write_text("".join(f"{t:.3f} crop@c x {x};\n" for t, x in _interp(kf)))
            xexpr, cmd = str(kf[0][1]), f"sendcmd=f='{ff_escape_path(cmdfile)}',"
        crop = f"{cmd}crop@c={W}:{H}:x='{xexpr}':y='(in_h-{H})/2{shake_y}'"
    else:
        crop = f"crop={W}:{H}:x='(in_w-{W})/2{shake}':y='(in_h-{H})/2{shake_y}'"
    vf = (
        f"setpts=(PTS-STARTPTS)/{speed},"
        f"scale=w={int(W * zoom)}:h={int(H * zoom)}:force_original_aspect_ratio=increase,"
        f"{crop},setsar=1,fps={FPS},format=yuv420p"
    )
    _encode_piece(p, vf, speed, src_dur, out)


def _encode_piece(p: dict, vf: str, speed: float, src_dur: float, out: Path) -> None:
    cmd = ["ffmpeg", "-y", "-ss", f"{p['start']:.3f}", "-t", f"{src_dur:.3f}", "-i", p["src"]]
    if has_audio(p["src"]):
        af = f"asetpts=PTS-STARTPTS,{atempo_chain(speed)},aformat=sample_rates={SR}:channel_layouts=stereo"
        cmd += ["-filter_complex", f"[0:v]{vf}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{src_dur / speed:.3f}", "-i", f"anullsrc=r={SR}:cl=stereo",
                "-filter_complex", f"[0:v]{vf}[v]", "-map", "[v]", "-map", "1:a"]
    cmd += ["-t", f"{src_dur / speed:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2", str(out)]
    run(cmd)


def concat(pieces: list[Path], out: Path) -> None:
    n = len(pieces)
    cmd = ["ffmpeg", "-y"]
    for p in pieces:
        cmd += ["-i", str(p)]
    streams = "".join(f"[{i}:v][{i}:a]" for i in range(n))
    cmd += ["-filter_complex", f"{streams}concat=n={n}:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(out)]
    run(cmd)


def build_ass(edl: dict, style: dict, duration: float, path: Path) -> None:
    g = style["global"]
    lines = [A.header(style)]
    words = edl.get("words") or []
    if words:
        lines += A.caption_events(words, style, edl.get("caption_active", color(style, "green")), y_pct=g["action_tag"]["y_pct"] + 8)
    for t in edl.get("texts", []):
        kind = t.get("kind", "tag")
        sname = {"header": "Header", "hook": "Hook"}.get(kind, "Tag")
        y = t.get("y_pct", 8 if kind == "header" else g["action_tag"]["y_pct"])
        hexc = color(style, t["color"]) if t.get("color") else None
        lines.append(A.text_event(t["text"], t["start"], t["end"], sname, y, hexc))
    if edl.get("handle"):
        lines.append(A.watermark_event(edl["handle"], duration, g["watermark"]["y_pct"]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ff_escape_path(p: Path) -> str:
    return str(p).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def emoji_x(base: str, t: float, y: int, size: int = 400) -> int:
    """Keep emoji pops off the streamer's face (e.g. lying on a bench at the payoff). Best-effort."""
    if os.environ.get("CLIPPER_TRACK", "1") != "1":
        return W // 2
    try:
        from .track import clear_x, face_boxes_at
        boxes = face_boxes_at(base, t) + face_boxes_at(base, t + 0.5)
        return int(clear_x(boxes, y, size, W))
    except Exception:
        return W // 2


def finalize(base: Path, edl: dict, style: dict, ass_path: Path, out: Path) -> None:
    duration = probe_duration(str(base))
    inputs = ["-i", str(base)]
    idx = 1
    vf_chain = []
    # Flashes (drawbox full-frame, ~3 frames)
    for imp in edl.get("impacts", []):
        if imp.get("flash"):
            c = color(style, imp["flash"]).lstrip("#")
            a, b = imp["t"], imp["t"] + 0.1
            vf_chain.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=0x{c}@0.55:t=fill:enable='between(t,{a:.3f},{b:.3f})'")
    fonts_dir = ff_escape_path(ASSETS / "fonts")
    vf_chain.append(f"ass='{ff_escape_path(ass_path)}':fontsdir='{fonts_dir}'")
    graph = [f"[0:v]{','.join(vf_chain)}[vbase]"]
    last_v = "vbase"

    # Emoji pops
    for k, imp in enumerate([i for i in edl.get("impacts", []) if i.get("emoji")]):
        png = ASSETS / "emoji" / f"{emoji_name(imp['emoji'])}.png"
        if not png.exists():
            continue
        inputs += ["-loop", "1", "-t", f"{duration:.3f}", "-i", str(png)]
        t0, t1 = imp["t"], min(duration, imp["t"] + imp.get("emoji_dur", 0.9))
        y = int(H * imp.get("emoji_y_pct", 62) / 100)
        cx = emoji_x(str(base), t0, y)
        graph.append(f"[{idx}:v]split=2[e{k}a][e{k}b]")
        graph.append(f"[e{k}a]scale=400:400[e{k}big]")
        graph.append(f"[e{k}b]scale=320:320[e{k}sm]")
        graph.append(f"[{last_v}][e{k}big]overlay=x={cx}-w/2:y={y}-h/2:enable='between(t,{t0:.3f},{t0 + 0.09:.3f})'[v{k}a]")
        graph.append(f"[v{k}a][e{k}sm]overlay=x={cx}-w/2:y={y}-h/2:enable='between(t,{t0 + 0.09:.3f},{t1:.3f})'[v{k}]")
        last_v = f"v{k}"
        idx += 1

    # Audio: source + music (muffled before drop, ducked under speech) + sfx
    a_labels = ["src"]
    vo = [v for v in edl.get("voice") or [] if Path(v["file"]).exists() and v["t"] < duration]
    if vo:
        # our commentary on top: the clip's own audio ducks under it (sidechain), VO a touch hot so it reads on a phone
        graph.append("[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[src0][sc]")
        for k, v in enumerate(vo):
            inputs += ["-i", v["file"]]
            ms = max(0, int(v["t"] * 1000))
            graph.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={ms}|{ms},volume=1.6[vo{k}]")
            idx += 1
        graph.append("".join(f"[vo{k}]" for k in range(len(vo))) +
                     f"amix=inputs={len(vo)}:normalize=0:duration=longest,apad,atrim=0:{duration:.3f},asplit=2[vo][vosc]")
        graph.append("[src0][vosc]sidechaincompress=threshold=0.02:ratio=8:attack=10:release=250[src]")
        a_labels.append("vo")
    else:
        graph.append("[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[src][sc]")
    mus = edl.get("music")
    if mus and Path(mus["file"]).exists():
        g = style["global"]["audio"]["music"]
        drop = mus.get("drop_t", 0)
        pre, post = db(g["bed_gain_db"] - 6), db(g["bed_gain_db"] + 4)
        skip = [] if Path(mus["file"]).name.startswith("placeholder") else ["-ss", "12"]  # real tracks: skip the intro
        inputs += ["-stream_loop", "-1", *skip, "-i", mus["file"]]
        graph.append(
            f"[{idx}:a]atrim=0:{duration:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,"
            f"lowpass=f=500:enable='lt(t,{drop:.3f})',volume='if(lt(t,{drop:.3f}),{pre:.4f},{post:.4f})':eval=frame[mraw]"
        )
        graph.append("[mraw][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=350[mus]")
        a_labels.append("mus")
        idx += 1
    else:
        graph.append("[sc]anullsink")
    sfx_events = [(i["t"], i["sfx"]) for i in edl.get("impacts", []) if i.get("sfx")]
    if edl.get("end_sfx"):
        sfx_events.append((edl["end_sfx"]["t"], edl["end_sfx"]["sfx"]))
    for k, (t, name) in enumerate(sfx_events):
        f = ASSETS / "sfx" / f"{name}.wav"
        if not f.exists():
            continue
        inputs += ["-i", str(f)]
        ms = max(0, int(t * 1000))
        graph.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo,adelay={ms}|{ms},volume=0.8[sfx{k}]")
        a_labels.append(f"sfx{k}")
        idx += 1
    graph.append("".join(f"[{l}]" for l in a_labels) + f"amix=inputs={len(a_labels)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,alimiter=limit=0.89[aout]")

    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(graph), "-map", f"[{last_v}]", "-map", "[aout]",
           "-t", f"{duration:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    run(cmd)


def render(edl: dict, style: dict, out: Path, workdir: Path | None = None, keep: bool = False) -> Path:
    out = Path(out)
    work = Path(workdir or out.with_suffix(".work"))
    work.mkdir(parents=True, exist_ok=True)
    piece_files = []
    for i, p in enumerate(edl["pieces"]):
        f = work / f"piece_{i:03d}.mp4"
        render_piece(p, f)
        piece_files.append(f)
    base = work / "base.mp4"
    if len(piece_files) == 1:
        shutil.copy(piece_files[0], base)
    else:
        concat(piece_files, base)
    duration = probe_duration(str(base))
    ass_path = work / "overlay.ass"
    build_ass(edl, style, duration, ass_path)
    (work / "edl.json").write_text(json.dumps(edl, indent=2, ensure_ascii=False))
    finalize(base, edl, style, ass_path, out)
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    return out
