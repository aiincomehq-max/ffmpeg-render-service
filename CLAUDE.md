# Working on this repo

A vertical short-form video renderer. Clip URLs plus caption copy go in, a
finished 1080x1920 MP4 comes out. It exists to produce social video at volume,
so throughput and unattended correctness matter more than features.

See `PLAN.md` for what the videos are for and what is being sold. See
`README.md` for the API.

## First thing after any gap

```
./scripts/smoke_test.sh
```

Generates its own footage, boots the service, renders, and verifies. If it
passes, the environment is good and any failure is in your change. Run it
before debugging anything else.

## Running locally

```
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8080
```

Needs `ffmpeg` on PATH and a font file on disk. On Debian or Ubuntu:
`apt-get install ffmpeg fonts-dejavu-core`. On macOS: `brew install ffmpeg`,
then set `FONT_BOLD` to a real `.ttf` path, because the default path is Linux
specific.

Render a spreadsheet of hooks:

```
python batch.py hooks.csv --service http://localhost:8080 --out results.csv
```

## Footguns, all of which have already cost a debugging session

**`drawtext` silently renders nothing when text expansion is on.** Any caption
containing a percent sign disappears while the video encodes normally. Caption
text goes through `textfile=` with `expansion=none`. Do not switch to inline
`text=`, which additionally breaks on quotes and colons.

**`drawtext` does not wrap.** Anything wider than the frame is clipped without
warning. `wrap_lines()` handles this by estimating glyph width; if you change
the font, re-check the 0.60 ratio in that function.

**Padding audio to infinity overflows the muxing queue.** ffmpeg reports this
as `No space left on device`, which is not a disk problem. Audio is padded and
trimmed to exactly the computed video length instead of relying on `-shortest`.
Keep it that way.

**`drawtext` needs harfbuzz on ffmpeg 7+.** Several popular static builds omit
it and the filter is then absent entirely. The smoke test checks for this.

**Slim base images ship no fonts.** `drawtext` needs an explicit `fontfile`,
and the Dockerfile installs one. `GET /health` reports whether it is present.

## Conventions

Development happens on `claude/account-viral-video-analysis-nxptsb`.

Validate render changes by extracting a frame and looking at it. A video that
encodes successfully with no visible text is the normal failure mode here, and
no exit code will tell you.
