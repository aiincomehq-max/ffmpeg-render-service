#!/usr/bin/env python3
"""Render a spreadsheet of hooks into finished videos.

One row is one caption. Rows sharing an `id` become one video, so a video with
three captions is three rows. Clip and audio columns are read from the first
row of each group.

    python batch.py hooks.csv --service http://localhost:8080 --out results.csv

Required columns: id, emphasis
Optional columns: pre, post, start_s, end_s, y, clips, voiceover_url,
                  music_url, first_beat_s, beat_s
`clips` is a pipe separated list of URLs.
"""

import argparse
import csv
import sys
import time
from collections import OrderedDict
from typing import Any, Dict, List

import requests


def _num(row: Dict[str, str], key: str, default):
    raw = (row.get(key) or "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def load_rows(path: str) -> "OrderedDict[str, List[Dict[str, str]]]":
    groups: "OrderedDict[str, List[Dict[str, str]]]" = OrderedDict()
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SystemExit(f"{path} has no header row")
        missing = {"id", "emphasis"} - set(n.strip() for n in reader.fieldnames)
        if missing:
            raise SystemExit(f"{path} is missing required columns: {sorted(missing)}")
        for line_no, row in enumerate(reader, start=2):
            row = {(k or "").strip(): v for k, v in row.items()}
            vid = (row.get("id") or "").strip()
            if not vid:
                print(f"skipping line {line_no}: blank id", file=sys.stderr)
                continue
            groups.setdefault(vid, []).append(row)
    return groups


def build_request(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    head = rows[0]

    clip_urls = [u.strip() for u in (head.get("clips") or "").split("|") if u.strip()]
    if not clip_urls:
        raise ValueError("no clips")

    first_beat = _num(head, "first_beat_s", 2.6)
    beat = _num(head, "beat_s", 1.3)

    captions = []
    cursor = 0.0
    for i, row in enumerate(rows):
        # Captions default to consecutive, non-overlapping spans so a sheet
        # with no timing columns still produces a sensible video.
        default_end = cursor + (first_beat if i == 0 else beat)
        start = _num(row, "start_s", cursor)
        end = _num(row, "end_s", default_end)
        captions.append({
            "pre": (row.get("pre") or "").strip(),
            "emphasis": (row.get("emphasis") or "").strip(),
            "post": (row.get("post") or "").strip(),
            "start_s": start,
            "end_s": end,
            "y": _num(row, "y", 0.30),
        })
        cursor = end

    req: Dict[str, Any] = {
        "clips": [{"url": u} for u in clip_urls],
        "captions": captions,
        "first_beat_s": first_beat,
        "beat_s": beat,
    }
    for key in ("voiceover_url", "music_url"):
        val = (head.get(key) or "").strip()
        if val:
            req[key] = val
    return req


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--service", default="http://localhost:8080",
                    help="base URL of the render service")
    ap.add_argument("--out", default="results.csv")
    ap.add_argument("--timeout", type=int, default=900,
                    help="seconds to wait for the whole batch")
    args = ap.parse_args()

    base = args.service.rstrip("/")
    groups = load_rows(args.csv_path)
    if not groups:
        raise SystemExit("no rows to render")

    ids, jobs = [], []
    for vid, rows in groups.items():
        try:
            jobs.append(build_request(rows))
            ids.append(vid)
        except ValueError as e:
            print(f"skipping {vid}: {e}", file=sys.stderr)

    if not jobs:
        raise SystemExit("every row was skipped")

    print(f"submitting {len(jobs)} video(s) to {base}")
    resp = requests.post(f"{base}/render/batch", json={"jobs": jobs}, timeout=120)
    resp.raise_for_status()
    job_ids = resp.json()["job_ids"]

    pending = dict(zip(job_ids, ids))
    results: Dict[str, Dict[str, Any]] = {}
    deadline = time.time() + args.timeout

    while pending and time.time() < deadline:
        time.sleep(3)
        for job_id in list(pending):
            r = requests.get(f"{base}/jobs/{job_id}", timeout=30)
            if r.status_code != 200:
                continue
            state = r.json()
            if state.get("status") in ("done", "error"):
                vid = pending.pop(job_id)
                results[vid] = {"job_id": job_id, **state}
                mark = "ok" if state["status"] == "done" else "FAILED"
                print(f"  {vid}: {mark}")

    for job_id, vid in pending.items():
        results[vid] = {"job_id": job_id, "status": "timeout"}
        print(f"  {vid}: timed out")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "job_id", "status", "url", "duration_s", "detail"])
        for vid in ids:
            res = results.get(vid, {"status": "missing"})
            url = res.get("url", "")
            if url.startswith("/"):
                url = base + url
            w.writerow([vid, res.get("job_id", ""), res.get("status", ""),
                        url, res.get("duration_s", ""), res.get("detail", "")])

    failed = sum(1 for v in results.values() if v.get("status") != "done")
    print(f"wrote {args.out} ({len(results) - failed} rendered, {failed} failed)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
