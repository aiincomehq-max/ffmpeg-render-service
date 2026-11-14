"""ffmpeg render service.

POST /render           -> assembles clips into a 1080x1920 vertical video
GET  /render/{job_id}  -> downloads the finished final.mp4
GET  /health

Backwards compatible: the original payload ({"clips": [url, ...], "overlays": [...],
"voiceover_url": ...}) still renders 1.5s clips exactly as before.
"""
import os
import uuid
import shutil
import subprocess
from typing import List, Optional, Union, Literal

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI()

WORKDIR = os.environ.get("RENDER_WORKDIR", "/tmp/render")
os.makedirs(WORKDIR, exist_ok=True)

# Local file paths are only accepted when explicitly enabled (e.g. on your own Mac),
# so a publicly deployed service can't be asked to read arbitrary files from disk.
ALLOW_LOCAL_FILES = os.environ.get("ALLOW_LOCAL_FILES") == "1"

FONT_FILE = os.environ.get("FONT_FILE", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
MONO_FONT_FILE = os.environ.get("MONO_FONT_FILE", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

W, H, FPS = 1080, 1920, 30


# ---------- request models ----------

class Clip(BaseModel):
    url: str
    duration_s: Optional[float] = None       # falls back to bpm/beats_per_shot, then default_duration_s
    trim_start_s: float = 0.0                # where in the source clip to start
    look: Literal["none", "cctv", "camcorder"] = "none"
    look_text: Optional[str] = None          # CCTV timestamp / camcorder date text


class Overlay(BaseModel):
    text: str
    start_s: float
    end_s: float
    y: float = 0.18                          # fraction of height
    fontsize: int = 64
    color: str = "white"


class VoiceLine(BaseModel):
    url: str
    start_s: float = 0.0
    volume: float = 1.0


class EndCard(BaseModel):
    text: str = "DREAMREACH."
    subtext: Optional[str] = None
    duration_s: float = 2.0
    color: str = "white"
    background: str = "black"
    fontsize: int = 110


class RenderRequest(BaseModel):
    clips: List[Union[str, Clip]]
    overlays: List[Overlay] = Field(default_factory=list)
    voiceover_url: Optional[str] = None      # legacy: one voice track from 0s
    voice_lines: List[VoiceLine] = Field(default_factory=list)
    music_url: Optional[str] = None
    music_start_s: float = 0.0               # offset into the music file (start on the hook)
    music_volume: float = 0.9
    duck_music: bool = True                  # lower music under voice lines
    bpm: Optional[float] = None
    beats_per_shot: int = 4
    default_duration_s: float = 1.5
    grain: bool = False
    vignette: bool = False
    end_card: Optional[EndCard] = None


# ---------- helpers ----------

def fetch(src: str, output_path: str):
    if src.startswith(("http://", "https://")):
        r = requests.get(src, stream=True, timeout=120)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        return
    if not ALLOW_LOCAL_FILES:
        raise ValueError(f"Only http(s) URLs are allowed (set ALLOW_LOCAL_FILES=1 for local paths): {src}")
    path = src[len("file://"):] if src.startswith("file://") else src
    shutil.copy(path, output_path)


def run_ffmpeg(cmd: List[str]):
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        raise RuntimeError(process.stderr[-3000:])
    return process.stdout


def is_image(path: str) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name",
         "-of", "csv=p=0", path],
        stdout=subprocess.PIPE, text=True,
    ).stdout.strip()
    return out in {"png", "mjpeg", "webp", "bmp", "tiff"}


def text_file(job_dir: str, text: str) -> str:
    """drawtext reads from a file so we never have to escape quotes/colons."""
    path = os.path.join(job_dir, f"txt_{uuid.uuid4().hex}.txt")
    with open(path, "w") as f:
        f.write(text)
    return path


def drawtext(textfile: str, font: str, size: int, color: str, x: str, y: str,
             extra: str = "") -> str:
    f = (f"drawtext=fontfile={font}:textfile={textfile}:fontsize={size}:fontcolor={color}:"
         f"x={x}:y={y}:borderw=4:bordercolor=black@0.6")
    return f + (":" + extra if extra else "")


def look_filters(clip: Clip, job_dir: str) -> List[str]:
    if clip.look == "cctv":
        tf = text_file(job_dir, clip.look_text or "CAM 03  23:73:00")
        return [
            "hue=s=0.35", "noise=alls=18:allf=t", "lenscorrection=k1=-0.18:k2=-0.02",
            drawtext(tf, MONO_FONT_FILE, 44, "white@0.85", "60", "90"),
        ]
    if clip.look == "camcorder":
        tf = text_file(job_dir, clip.look_text or "JAN 01 '73")
        rec = text_file(job_dir, "REC")
        inner_h = int(W * 3 / 4)  # 4:3 frame inside the 9:16 canvas
        return [
            f"scale={W}:{inner_h}:force_original_aspect_ratio=increase,crop={W}:{inner_h}",
            "noise=alls=12:allf=t", "eq=saturation=0.85:contrast=1.08",
            f"pad={W}:{H}:0:(oh-ih)/2:black",
            f"drawbox=x=70:y=(ih-{inner_h})/2+60:w=34:h=34:color=red@0.9:t=fill:enable='lt(mod(t,1),0.6)'",
            drawtext(rec, MONO_FONT_FILE, 44, "white", "120", f"(h-{inner_h})/2+52"),
            drawtext(tf, MONO_FONT_FILE, 40, "white", "w-tw-70", f"(h+{inner_h})/2-100"),
        ]
    return []


def clip_duration(clip: Clip, req: RenderRequest) -> float:
    if clip.duration_s:
        return clip.duration_s
    if req.bpm:
        return round(60.0 / req.bpm * req.beats_per_shot, 3)
    return req.default_duration_s


def normalize_clip(src: str, out: str, clip: Clip, duration: float, job_dir: str):
    base = [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}"]
    vf = ",".join(base + look_filters(clip, job_dir) + [f"fps={FPS}", "format=yuv420p"])
    if is_image(src):
        inputs = ["-loop", "1", "-i", src]
    else:
        inputs = ["-ss", str(clip.trim_start_s), "-i", src]
    run_ffmpeg(["ffmpeg", "-y", *inputs, "-t", str(duration), "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out])


def make_end_card(card: EndCard, out: str, job_dir: str):
    main = text_file(job_dir, card.text)
    fade_out = max(card.duration_s - 0.4, 0)
    filters = [drawtext(main, FONT_FILE, card.fontsize, card.color, "(w-tw)/2", "(h-th)/2-40")]
    if card.subtext:
        sub = text_file(job_dir, card.subtext)
        filters.append(drawtext(sub, FONT_FILE, 40, f"{card.color}@0.75", "(w-tw)/2", "(h/2)+70"))
    filters += ["fade=t=in:st=0:d=0.4", f"fade=t=out:st={fade_out}:d=0.4", "format=yuv420p"]
    run_ffmpeg(["ffmpeg", "-y", "-f", "lavfi",
                "-i", f"color=c={card.background}:s={W}x{H}:r={FPS}:d={card.duration_s}",
                "-vf", ",".join(filters), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p", out])


def video_duration(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], stdout=subprocess.PIPE, text=True).stdout
    return float(out.strip())


def final_path(job_id: str) -> str:
    return os.path.join(WORKDIR, job_id, "final.mp4")


# ---------- routes ----------

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/render")
def render_video(req: RenderRequest):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(WORKDIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    try:
        clips = [Clip(url=c) if isinstance(c, str) else c for c in req.clips]

        # 1. fetch + normalise each clip to 1080x1920 @30fps for its slot length
        segments = []
        for i, clip in enumerate(clips):
            src = os.path.join(job_dir, f"src_{i}")
            fetch(clip.url, src)
            seg = os.path.join(job_dir, f"seg_{i:03d}.mp4")
            normalize_clip(src, seg, clip, clip_duration(clip, req), job_dir)
            segments.append(seg)

        if req.end_card:
            card = os.path.join(job_dir, "seg_end.mp4")
            make_end_card(req.end_card, card, job_dir)
            segments.append(card)

        # 2. concat
        concat_file = os.path.join(job_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for seg in segments:
                f.write(f"file '{seg}'\n")
        base = os.path.join(job_dir, "base.mp4")
        run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
                    "-c", "copy", base])

        # 3. global look + text overlays
        vfilters = []
        if req.grain:
            vfilters.append("noise=alls=10:allf=t")
        if req.vignette:
            vfilters.append("vignette=PI/5")
        for ov in req.overlays:
            tf = text_file(job_dir, ov.text)
            vfilters.append(drawtext(tf, FONT_FILE, ov.fontsize, ov.color, "(w-tw)/2",
                                     f"h*{ov.y}",
                                     f"enable='between(t,{ov.start_s},{ov.end_s})'"))
        styled = os.path.join(job_dir, "styled.mp4")
        if vfilters:
            run_ffmpeg(["ffmpeg", "-y", "-i", base, "-vf", ",".join(vfilters + ["format=yuv420p"]),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-an", styled])
        else:
            shutil.copy(base, styled)

        # 4. audio: music (+ optional ducking) and voice lines
        voices = list(req.voice_lines)
        if req.voiceover_url:
            voices.insert(0, VoiceLine(url=req.voiceover_url, start_s=0.0))

        out = final_path(job_id)
        audio_inputs, chains, labels = [], [], []
        idx = 1
        music_label = None
        if req.music_url:
            mpath = os.path.join(job_dir, "music")
            fetch(req.music_url, mpath)
            audio_inputs += ["-ss", str(req.music_start_s), "-i", mpath]
            chains.append(f"[{idx}:a]volume={req.music_volume}[music]")
            music_label = "[music]"
            idx += 1
        voice_labels = []
        for n, v in enumerate(voices):
            vpath = os.path.join(job_dir, f"voice_{n}")
            fetch(v.url, vpath)
            audio_inputs += ["-i", vpath]
            delay = int(v.start_s * 1000)
            chains.append(f"[{idx}:a]volume={v.volume},adelay={delay}|{delay}[v{n}]")
            voice_labels.append(f"[v{n}]")
            idx += 1

        if not audio_inputs:
            shutil.copy(styled, out)
        else:
            if voice_labels:
                if len(voice_labels) > 1:
                    chains.append("".join(voice_labels) +
                                  f"amix=inputs={len(voice_labels)}:normalize=0[voice]")
                else:
                    chains.append(f"{voice_labels[0]}anull[voice]")
                # pad so a short voice line never cuts the music/video off early
                chains.append("[voice]apad[voicep]")
            if music_label and voice_labels:
                if req.duck_music:
                    chains.append("[voicep]asplit=2[vsc][vmix]")
                    chains.append(f"{music_label}[vsc]sidechaincompress=threshold=0.03:ratio=8:"
                                  "attack=20:release=400[ducked]")
                    chains.append("[ducked][vmix]amix=inputs=2:normalize=0[aout]")
                else:
                    chains.append(f"{music_label}[voicep]amix=inputs=2:normalize=0[aout]")
            elif music_label:
                chains.append(f"{music_label}anull[aout]")
            else:
                chains.append("[voicep]anull[aout]")
            chains[-1] = chains[-1].replace("[aout]", "[amixed]")
            chains.append("[amixed]apad[aout]")
            run_ffmpeg(["ffmpeg", "-y", "-i", styled, *audio_inputs,
                        "-filter_complex", ";".join(chains),
                        "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac",
                        "-b:a", "192k", "-t", str(video_duration(styled)), out])

        return {"ok": True, "job_id": job_id, "download_url": f"/render/{job_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/render/{job_id}")
def download(job_id: str):
    try:
        uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid job_id")
    path = final_path(job_id)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="not found")
    return FileResponse(path, media_type="video/mp4", filename=f"{job_id}.mp4")
