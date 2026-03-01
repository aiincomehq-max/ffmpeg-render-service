import os
import uuid
import subprocess
import shutil
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

WORKDIR = "/tmp/render"
os.makedirs(WORKDIR, exist_ok=True)


class Overlay(BaseModel):
    text: str
    start_s: float
    end_s: float


class RenderRequest(BaseModel):
    clips: List[str]
    overlays: List[Overlay]
    voiceover_url: Optional[str] = None


def download_file(url: str, output_path: str):
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


def run_ffmpeg(cmd: List[str]):
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if process.returncode != 0:
        raise RuntimeError(process.stderr)
    return process.stdout


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/render")
def render_video(req: RenderRequest):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(WORKDIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    try:
        # Download clips
        local_clips = []
        for i, clip_url in enumerate(req.clips):
            local_path = os.path.join(job_dir, f"clip_{i}.mp4")
            download_file(clip_url, local_path)
            local_clips.append(local_path)

        # Normalize each clip to 1.5 seconds, 1080x1920 vertical
        normalized_clips = []
        for i, clip_path in enumerate(local_clips):
            output_path = os.path.join(job_dir, f"norm_{i}.mp4")
            run_ffmpeg([
                "ffmpeg",
                "-y",
                "-i", clip_path,
                "-t", "1.5",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                "-an",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                output_path
            ])
            normalized_clips.append(output_path)

        # Create concat list file
        concat_file = os.path.join(job_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for clip in normalized_clips:
                f.write(f"file '{clip}'\n")

        concatenated_path = os.path.join(job_dir, "base.mp4")
        run_ffmpeg([
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            concatenated_path
        ])

        # Build text overlay filters
        draw_filters = []
        for overlay in req.overlays:
            safe_text = overlay.text.replace(":", "\\:").replace("'", "\\'")
            draw_filters.append(
                "drawtext="
                f"text='{safe_text}':"
                "x=(w-text_w)/2:"
                "y=h*0.18:"
                "fontsize=64:"
                "fontcolor=white:"
                "borderw=6:"
                "bordercolor=black@0.7:"
                f"enable='between(t,{overlay.start_s},{overlay.end_s})'"
            )

        filter_chain = ",".join(draw_filters) if draw_filters else "null"

        text_overlay_path = os.path.join(job_dir, "with_text.mp4")
        run_ffmpeg([
            "ffmpeg",
            "-y",
            "-i", concatenated_path,
            "-vf", filter_chain,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            text_overlay_path
        ])

        final_path = os.path.join(job_dir, "final.mp4")

        # Add voiceover if provided
        if req.voiceover_url:
            voice_path = os.path.join(job_dir, "voice.mp3")
            download_file(req.voiceover_url, voice_path)
            run_ffmpeg([
                "ffmpeg",
                "-y",
                "-i", text_overlay_path,
                "-i", voice_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                final_path
            ])
        else:
            shutil.copy(text_overlay_path, final_path)

        return {
            "ok": True,
            "job_id": job_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
