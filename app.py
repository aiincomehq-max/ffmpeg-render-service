import os
import re
import uuid
import shutil
import textwrap
import subprocess
from typing import List, Optional, Dict, Any

import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

FFMPEG = os.environ.get("FFMPEG_BIN", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE_BIN", "ffprobe")

# drawtext needs an explicit font file. Relying on fontconfig's "Sans" default
# fails on slim base images that ship no fonts at all.
FONT_BOLD = os.environ.get(
    "FONT_BOLD", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
)

WORKDIR = os.environ.get("WORKDIR", "/tmp/render")
OUTDIR = os.environ.get("OUTDIR", "/tmp/outputs")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")

WIDTH, HEIGHT = 1080, 1920
FPS = 30
SIDE_MARGIN = 60

os.makedirs(WORKDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)

app = FastAPI(title="ffmpeg-render-service")
app.mount("/outputs", StaticFiles(directory=OUTDIR), name="outputs")

JOBS: Dict[str, Dict[str, Any]] = {}


# --------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------


class Clip(BaseModel):
    url: str
    # Per-clip duration. When omitted the renderer applies the beat pattern:
    # a long opening beat, then shorter ones.
    duration_s: Optional[float] = None


class Caption(BaseModel):
    """A three-part caption block: small line, big emphasis, small line.

    This mirrors the hook structure that reads at thumbnail size:
    "THEY PULLED" / "3X" / "MORE SHARES THAN LIKES".
    Any part may be empty.
    """

    pre: str = ""
    emphasis: str = ""
    post: str = ""
    start_s: float
    end_s: float
    # Vertical anchor as a fraction of frame height; the block is centred on it.
    y: float = 0.30


class RenderRequest(BaseModel):
    clips: List[Clip]
    captions: List[Caption] = Field(default_factory=list)
    voiceover_url: Optional[str] = None
    music_url: Optional[str] = None
    music_gain_db: float = -18.0
    # Beat pattern. The opening beat is deliberately longer: a hook needs time
    # to land, and a uniform cut cadence is what reads as machine-generated.
    first_beat_s: float = 2.6
    beat_s: float = 1.3
    body_size: int = 62
    emphasis_size: int = 150
    uppercase: bool = True
    # Stretch clip durations so the cut sequence matches the voiceover length.
    fit_to_voiceover: bool = False


class BatchRequest(BaseModel):
    jobs: List[RenderRequest]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def download_file(url: str, output_path: str) -> str:
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    return output_path


def run(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-25:])
        raise RuntimeError(tail)
    return proc.stdout


def probe_duration(path: str) -> Optional[float]:
    """Media duration in seconds, or None when it cannot be determined."""
    try:
        out = run([
            FFPROBE, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path,
        ])
        return float(out.strip())
    except Exception:
        pass
    # Fall back to parsing ffmpeg's own report when ffprobe is unavailable.
    try:
        proc = subprocess.run(
            [FFMPEG, "-i", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", proc.stderr)
        if m:
            h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
            return h * 3600 + mi * 60 + s
    except Exception:
        pass
    return None


def wrap_lines(text: str, font_size: int, uppercase: bool) -> List[str]:
    """Split text into lines that fit the frame width.

    drawtext does not wrap, so anything wider than the frame is silently
    clipped. Width is estimated from the glyph aspect ratio of a bold sans.
    """
    text = (text or "").strip()
    if not text:
        return []
    if uppercase:
        text = text.upper()
    usable = WIDTH - (2 * SIDE_MARGIN)
    chars_per_line = max(6, int(usable / (font_size * 0.60)))
    return textwrap.wrap(text, width=chars_per_line) or []


def caption_drawtext_filters(
    cap: Caption, job_dir: str, index: int, body_size: int, emphasis_size: int, uppercase: bool
) -> List[str]:
    """Build one drawtext filter per rendered line.

    Each line is a separate drawtext so every line is independently centred;
    a single multi-line drawtext would left-align them inside its text box.
    Text is passed via textfile= with expansion disabled, so quotes, colons,
    backslashes and percent signs in the copy cannot corrupt the filtergraph
    or silently blank the line.
    """
    blocks: List[tuple] = []
    for line in wrap_lines(cap.pre, body_size, uppercase):
        blocks.append((line, body_size))
    for line in wrap_lines(cap.emphasis, emphasis_size, uppercase):
        blocks.append((line, emphasis_size))
    for line in wrap_lines(cap.post, body_size, uppercase):
        blocks.append((line, body_size))

    if not blocks:
        return []

    line_heights = [round(size * 1.16) for _, size in blocks]
    total_height = sum(line_heights)
    cursor = int(HEIGHT * cap.y) - (total_height // 2)

    filters: List[str] = []
    for line_no, ((line, size), line_h) in enumerate(zip(blocks, line_heights)):
        text_path = os.path.join(job_dir, f"cap_{index}_{line_no}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(line)

        border = max(4, round(size * 0.075))
        filters.append(
            "drawtext="
            f"fontfile={FONT_BOLD}:"
            f"textfile={text_path}:"
            # Without this, drawtext expands %{...} in the copy: a caption
            # containing a percent sign renders as nothing at all.
            "expansion=none:"
            f"fontsize={size}:"
            "fontcolor=white:"
            f"borderw={border}:"
            "bordercolor=black@0.85:"
            "x=(w-text_w)/2:"
            f"y={cursor}:"
            f"enable='between(t,{cap.start_s},{cap.end_s})'"
        )
        cursor += line_h

    return filters


def resolve_durations(req: RenderRequest, voice_path: Optional[str]) -> List[float]:
    durations: List[float] = []
    for i, clip in enumerate(req.clips):
        if clip.duration_s is not None:
            durations.append(max(0.2, clip.duration_s))
        else:
            durations.append(req.first_beat_s if i == 0 else req.beat_s)

    if req.fit_to_voiceover and voice_path:
        voice_len = probe_duration(voice_path)
        total = sum(durations)
        if voice_len and total > 0:
            scale = voice_len / total
            durations = [d * scale for d in durations]

    return durations


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------


def render(req: RenderRequest, job_id: str) -> Dict[str, Any]:
    if not req.clips:
        raise ValueError("at least one clip is required")

    job_dir = os.path.join(WORKDIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    try:
        local_clips: List[str] = []
        for i, clip in enumerate(req.clips):
            path = os.path.join(job_dir, f"clip_{i}.mp4")
            download_file(clip.url, path)
            local_clips.append(path)

        voice_path = None
        if req.voiceover_url:
            voice_path = download_file(
                req.voiceover_url, os.path.join(job_dir, "voice.mp3")
            )

        music_path = None
        if req.music_url:
            music_path = download_file(
                req.music_url, os.path.join(job_dir, "music.mp3")
            )

        durations = resolve_durations(req, voice_path)

        cmd: List[str] = [FFMPEG, "-y"]
        for path in local_clips:
            cmd += ["-i", path]
        voice_idx = music_idx = None
        if voice_path:
            voice_idx = len(local_clips)
            cmd += ["-i", voice_path]
        if music_path:
            music_idx = len(local_clips) + (1 if voice_path else 0)
            cmd += ["-i", music_path]

        # One encode for the whole video: trim, scale, crop, concat and caption
        # in a single graph rather than re-encoding at each stage.
        graph: List[str] = []
        for i, dur in enumerate(durations):
            graph.append(
                f"[{i}:v]trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
                f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
                f"crop={WIDTH}:{HEIGHT},fps={FPS},setsar=1[v{i}]"
            )
        concat_inputs = "".join(f"[v{i}]" for i in range(len(durations)))
        graph.append(f"{concat_inputs}concat=n={len(durations)}:v=1:a=0[vcat]")

        draw: List[str] = []
        for idx, cap in enumerate(req.captions):
            draw += caption_drawtext_filters(
                cap, job_dir, idx, req.body_size, req.emphasis_size, req.uppercase
            )
        if draw:
            graph.append("[vcat]" + ",".join(draw) + "[vout]")
        else:
            graph.append("[vcat]null[vout]")

        # Audio is padded or trimmed to exactly the video length. Padding to
        # infinity and relying on -shortest overflows ffmpeg's muxing queue,
        # which surfaces as a misleading "No space left on device".
        total_s = sum(durations)

        def audio_chain(stream_idx: int, gain_db: Optional[float] = None) -> str:
            parts = [f"[{stream_idx}:a]aresample=44100"]
            if gain_db is not None:
                parts.append(f"volume={gain_db}dB")
            parts.append(f"apad=whole_dur={total_s:.3f}")
            parts.append(f"atrim=0:{total_s:.3f}")
            parts.append("asetpts=PTS-STARTPTS")
            return ",".join(parts)

        audio_label = None
        if voice_path and music_path:
            graph.append(audio_chain(voice_idx) + "[avo]")
            graph.append(audio_chain(music_idx, req.music_gain_db) + "[amu]")
            graph.append("[avo][amu]amix=inputs=2:duration=first:normalize=0[aout]")
            audio_label = "[aout]"
        elif voice_path:
            graph.append(audio_chain(voice_idx) + "[aout]")
            audio_label = "[aout]"
        elif music_path:
            graph.append(audio_chain(music_idx, req.music_gain_db) + "[aout]")
            audio_label = "[aout]"

        output_path = os.path.join(OUTDIR, f"{job_id}.mp4")
        cmd += ["-filter_complex", ";".join(graph), "-map", "[vout]"]
        if audio_label:
            cmd += ["-map", audio_label, "-c:a", "aac", "-b:a", "192k"]
        else:
            cmd += ["-an"]
        cmd += ["-t", f"{total_s:.3f}"]
        cmd += [
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path,
        ]

        run(cmd)

        url = f"/outputs/{job_id}.mp4"
        if PUBLIC_BASE_URL:
            url = f"{PUBLIC_BASE_URL}{url}"

        return {
            "ok": True,
            "job_id": job_id,
            "url": url,
            "duration_s": round(sum(durations), 3),
            "clip_durations": [round(d, 3) for d in durations],
        }
    finally:
        shutil.rmtree(job_dir, ignore_errors=True)


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------


@app.get("/health")
def health():
    return {"ok": True, "font": FONT_BOLD, "font_present": os.path.exists(FONT_BOLD)}


@app.post("/render")
def render_video(req: RenderRequest):
    job_id = str(uuid.uuid4())
    try:
        return render(req, job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _run_batch_job(req: RenderRequest, job_id: str):
    JOBS[job_id] = {"status": "running"}
    try:
        JOBS[job_id] = {"status": "done", **render(req, job_id)}
    except Exception as e:
        JOBS[job_id] = {"status": "error", "job_id": job_id, "detail": str(e)}


@app.post("/render/batch")
def render_batch(batch: BatchRequest, background: BackgroundTasks):
    """Queue many renders at once. Volume is the point of the pipeline."""
    job_ids = []
    for req in batch.jobs:
        job_id = str(uuid.uuid4())
        JOBS[job_id] = {"status": "queued"}
        background.add_task(_run_batch_job, req, job_id)
        job_ids.append(job_id)
    return {"ok": True, "job_ids": job_ids}


@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="unknown job")
    return JOBS[job_id]
