FROM python:3.11-slim

# ffmpeg's drawtext filter needs a real font file on disk. The slim base ships
# none, so text rendering fails unless fonts are installed explicitly.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

ENV PORT=8080 \
    WORKDIR=/tmp/render \
    OUTDIR=/tmp/outputs \
    FONT_BOLD=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

RUN mkdir -p /tmp/render /tmp/outputs

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
