# ffmpeg-render-service

A vertical short-form video renderer. Takes clip URLs plus caption copy and
returns a finished 1080x1920 MP4. Built for volume: one HTTP call per video,
or a batch call for many.

## Why it is shaped this way

Three rendering decisions carry most of the output quality.

**Variable beats.** A uniform cut cadence is the clearest signal of machine
generated video. The opening beat defaults to 2.6 seconds so a hook has time
to land; later beats default to 1.3. Any clip can override its own duration.

**Three part captions.** A caption is `pre` / `emphasis` / `post`, rendered as
small line, large line, small line. This is the structure that stays legible at
thumbnail size: "THEY PULLED" / "3X" / "MORE SHARES THAN LIKES". Lines are
wrapped to the frame width and each line is centred independently.

**Exact duration.** Audio is padded or trimmed to precisely the length of the
cut sequence rather than relying on `-shortest`, so output length is always
deterministic.

## API

`GET /health` reports whether the configured font file exists. Text rendering
fails without one, so check this after any image change.

`POST /render` renders synchronously and returns a URL.

```json
{
  "clips": [
    {"url": "https://example.com/a.mp4"},
    {"url": "https://example.com/b.mp4", "duration_s": 0.9}
  ],
  "captions": [
    {"pre": "This video cost", "emphasis": "$0.00", "post": "and took 9 seconds",
     "start_s": 0.0, "end_s": 2.6, "y": 0.30}
  ],
  "voiceover_url": "https://example.com/vo.mp3",
  "music_url": "https://example.com/bed.mp3",
  "music_gain_db": -18.0,
  "fit_to_voiceover": false
}
```

Response:

```json
{"ok": true, "job_id": "...", "url": "/outputs/....mp4",
 "duration_s": 5.2, "clip_durations": [2.6, 1.3, 1.3]}
```

`POST /render/batch` takes `{"jobs": [<render request>, ...]}` and queues them
in the background, returning job ids immediately.

`GET /jobs/{job_id}` returns `queued`, `running`, `done` or `error`.

Rendered files are served from `/outputs`.

## Configuration

| Variable | Purpose |
|---|---|
| `PORT` | Listen port, default 8080 |
| `FONT_BOLD` | Absolute path to the caption font file |
| `OUTDIR` | Where finished renders are written and served from |
| `WORKDIR` | Scratch space for downloads, cleared after each job |
| `PUBLIC_BASE_URL` | Prefix so responses carry absolute URLs |
| `FFMPEG_BIN`, `FFPROBE_BIN` | Binary overrides |

## Notes for anyone changing the render path

Caption text is written to a file and passed via `textfile=` with
`expansion=none`. Both parts matter. Inline `text=` breaks on quotes and
colons, and leaving expansion on makes any caption containing a percent sign
render as nothing at all.

`OUTDIR` grows without bound. Add a retention sweep before running this
anywhere long lived.

Clip and audio URLs are fetched server side with no allowlist, so do not expose
this endpoint to untrusted callers without adding one.

## Rendering a sheet of hooks

`batch.py` turns a CSV into finished videos. One row is one caption; rows
sharing an `id` become a single video, so a three caption video is three rows.
Clip and audio columns are read from the first row of each group, and `clips`
is a pipe separated list of URLs.

```csv
id,pre,emphasis,post,start_s,end_s,clips,music_url
v1,They pulled,3X,more shares than likes,0,2.6,https://x/a.mp4|https://x/b.mp4,https://x/bed.mp3
v1,,No face. No editor.,,2.6,3.9,,
v2,This reel cost,$0.00,to make. 100% automated.,,,https://x/c.mp4|https://x/d.mp4,
```

```
python batch.py hooks.csv --service http://localhost:8080 --out results.csv
```

Timing columns may be left blank, in which case captions are laid out
consecutively using the beat pattern. Rows without clips are skipped with a
warning rather than failing the run. `results.csv` carries the status and
finished URL for every row.
