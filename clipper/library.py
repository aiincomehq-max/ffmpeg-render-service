"""SQLite moment library: every moment from every VOD, queryable by skill/outcome/type."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from . import ROOT

CHANNEL = "speed"  # set by the CLI (--channel); each channel gets its own library


def db_path() -> Path:
    return ROOT / "data" / CHANNEL / "moments.db"


def conn() -> sqlite3.Connection:
    db = db_path()
    db.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(db)
    c.execute("""CREATE TABLE IF NOT EXISTS moments (
        id INTEGER PRIMARY KEY, vod_key TEXT, src TEXT, start REAL, "end" REAL, type TEXT, skill TEXT,
        outcome TEXT, virality INTEGER, used INTEGER DEFAULT 0, data TEXT,
        UNIQUE(vod_key, start))""")
    return c


def add(vod_key: str, src: Path, moments: list[dict]) -> None:
    with conn() as c:
        for m in moments:
            m["src"] = str(src)
            c.execute("""INSERT OR REPLACE INTO moments (vod_key, src, start, "end", type, skill, outcome, virality, data)
                         VALUES (?,?,?,?,?,?,?,?,?)""",
                      (vod_key, str(src), m["start"], m["end"], m["type"], m["skill"], m["outcome"], m["virality"],
                       json.dumps(m, ensure_ascii=False)))


def _rows(sql: str, args=()) -> list[dict]:
    with conn() as c:
        out = []
        for row_id, used, data in c.execute(sql, args).fetchall():
            m = json.loads(data)
            m["_id"], m["_used"] = row_id, used
            out.append(m)
        return out


KIND = "COALESCE(json_extract(data, '$.source_kind'), 'heatmap')"


def top(vod_key: str | None = None, n: int = 3, min_virality: int = 7, kind: str | None = None) -> list[dict]:
    """kind: 'fresh' (Claude-estimated from a new stream) | 'heatmap' (YouTube 'Most replayed') | None = any."""
    q = "SELECT id, used, data FROM moments WHERE virality >= ? AND used = 0"
    args: list = [min_virality]
    if kind:
        q += f" AND {KIND} = ?"
        args.append(kind)
    if vod_key:
        q += " AND vod_key = ?"
        args.append(vod_key)
    return _rows(q + " ORDER BY virality DESC LIMIT ?", (*args, n))


def by_skill(skill: str, outcome: str) -> list[dict]:
    return _rows("SELECT id, used, data FROM moments WHERE skill = ? AND outcome = ? ORDER BY used ASC, virality DESC",
                 (skill, outcome))


def skill_counts() -> list[tuple[str, int, int]]:
    with conn() as c:
        return c.execute("""SELECT skill, SUM(outcome='fail'), SUM(outcome='success') FROM moments
                            WHERE skill != 'none' GROUP BY skill ORDER BY 3 DESC""").fetchall()


def mark_used(ids: list[int]) -> None:
    with conn() as c:
        c.executemany("UPDATE moments SET used = used + 1 WHERE id = ?", [(i,) for i in ids])


def exists_near(video_id: str, abs_start: float, tol: float = 5.0) -> bool:
    """Same real moment already in the library (from the other batch, or an overlapping section)?"""
    with conn() as c:
        return c.execute("""SELECT 1 FROM moments WHERE json_extract(data, '$.video_id') = ?
                            AND ABS(json_extract(data, '$.abs_start') - ?) <= ? LIMIT 1""",
                         (video_id, abs_start, tol)).fetchone() is not None
