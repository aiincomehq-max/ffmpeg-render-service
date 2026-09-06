#!/usr/bin/env python3
"""Sum the receipts that only the Mac holds: hours, sessions, tokens.

Run on the Mac:   python3 mac_receipts.py
Writes:           ~/CodexProjects/claude-sessions/RECEIPTS.md and RECEIPTS.json
Reads only. Never prints or copies a credential.

Sources
  1. Terminal recordings  ~/CodexProjects/claude-sessions/terminal-logs/claude_session_*.log
     Start time is in the filename (written by the `script` wrapper); end time is the file's
     last-modified time. Duration = end - start.
  2. Claude Code transcripts  ~/.claude/projects/**/*.jsonl
     One line per event. Assistant events carry message.usage with token counts, so the
     total tokens across every session on this machine can be summed exactly.
  3. n8n (optional)  if ~/.claude/fdh_n8n.key exists, counts workflows and executions
     through the public API. The key value is read into memory and never printed.
"""
import glob, json, os, re, sys, datetime as dt, collections, urllib.request

HOME = os.path.expanduser("~")
TERM_DIR = os.path.join(HOME, "CodexProjects", "claude-sessions", "terminal-logs")
CLAUDE_DIR = os.path.join(HOME, ".claude", "projects")
OUT_DIR = os.path.join(HOME, "CodexProjects", "claude-sessions")
N8N_KEYFILE = os.path.join(HOME, ".claude", "fdh_n8n.key")
N8N_BASE = "https://n8n.humanupgradehq.com/api/v1"

out = {"generated_at": dt.datetime.now().isoformat(timespec="seconds")}

# ---------------------------------------------------------------- 1. terminal recordings
sessions = []
for path in sorted(glob.glob(os.path.join(TERM_DIR, "claude_session_*.log"))):
    m = re.search(r"claude_session_(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})", os.path.basename(path))
    if not m:
        continue
    start = dt.datetime.strptime(f"{m.group(1)} {m.group(2)}:{m.group(3)}:{m.group(4)}", "%Y-%m-%d %H:%M:%S")
    end = dt.datetime.fromtimestamp(os.path.getmtime(path))
    hours = max(0.0, (end - start).total_seconds() / 3600)
    sessions.append({"file": os.path.basename(path), "start": start.isoformat(), "end": end.isoformat(),
                     "hours": round(hours, 2), "bytes": os.path.getsize(path)})

if sessions:
    by_day = collections.defaultdict(float)
    for s in sessions:
        by_day[s["start"][:10]] += s["hours"]
    days = sorted(by_day)
    span_days = (dt.date.fromisoformat(days[-1]) - dt.date.fromisoformat(days[0])).days + 1
    plausible = [s for s in sessions if s["hours"] <= 20]  # a recording left open overnight is not work
    out["terminal"] = {
        "recordings": len(sessions),
        "first_day": days[0], "last_day": days[-1], "calendar_days_spanned": span_days,
        "days_with_a_session": len(days),
        "hours_recorded_total": round(sum(s["hours"] for s in sessions), 1),
        "hours_recorded_excluding_sessions_over_20h": round(sum(s["hours"] for s in plausible), 1),
        "sessions_over_20h_excluded": len(sessions) - len(plausible),
        "average_hours_per_active_day": round(sum(s["hours"] for s in plausible) / max(1, len(days)), 2),
        "longest_session_hours": round(max(s["hours"] for s in sessions), 2),
        "sessions_per_active_day": round(len(sessions) / max(1, len(days)), 2),
        "total_recording_bytes": sum(s["bytes"] for s in sessions),
        "busiest_days": sorted(((round(h, 1), d) for d, h in by_day.items()), reverse=True)[:10],
        "hours_by_month": {k: round(v, 1) for k, v in sorted(
            collections.Counter({m: 0 for m in set(d[:7] for d in days)}).items())},
    }
    for d, h in by_day.items():
        out["terminal"]["hours_by_month"][d[:7]] = round(out["terminal"]["hours_by_month"].get(d[:7], 0) + h, 1)
else:
    out["terminal"] = {"error": f"no recordings found in {TERM_DIR}"}

# ---------------------------------------------------------------- 2. Claude transcripts
files = glob.glob(os.path.join(CLAUDE_DIR, "**", "*.jsonl"), recursive=True)
usage = collections.Counter(); events = collections.Counter(); tools = collections.Counter()
models = collections.Counter(); per_day = collections.defaultdict(lambda: collections.Counter())
session_ids = set(); first_ts = None; last_ts = None; user_turns = 0; bad = 0
for path in files:
    try:
        with open(path, "r", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:
                    bad += 1; continue
                t = ev.get("type"); events[t] += 1
                sid = ev.get("sessionId")
                if sid: session_ids.add(sid)
                ts = ev.get("timestamp")
                if ts:
                    first_ts = ts if not first_ts or ts < first_ts else first_ts
                    last_ts = ts if not last_ts or ts > last_ts else last_ts
                msg = ev.get("message") or {}
                if t == "user" and isinstance(msg.get("content"), str):
                    user_turns += 1
                    if ts: per_day[ts[:10]]["user_turns"] += 1
                if t == "assistant":
                    u = msg.get("usage") or {}
                    for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                        usage[k] += int(u.get(k) or 0)
                    if msg.get("model"): models[msg["model"]] += 1
                    if ts: per_day[ts[:10]]["assistant_events"] += 1
                    for block in msg.get("content") or []:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            tools[block.get("name", "?")] += 1
    except Exception as exc:
        bad += 1
out["transcripts"] = {
    "jsonl_files": len(files), "distinct_session_ids": len(session_ids),
    "first_event": first_ts, "last_event": last_ts,
    "user_turns_typed": user_turns,
    "assistant_events": events.get("assistant", 0),
    "tool_calls_total": sum(tools.values()),
    "tool_calls_by_tool": dict(tools.most_common(15)),
    "tokens": dict(usage),
    "tokens_total_all_kinds": sum(usage.values()),
    "models_seen": dict(models.most_common(8)),
    "days_active": len(per_day),
    "unparseable_lines": bad,
}

# ---------------------------------------------------------------- 3. n8n (optional, read-only)
if os.path.exists(N8N_KEYFILE):
    try:
        key = open(N8N_KEYFILE).read().strip()
        def get(path):
            req = urllib.request.Request(N8N_BASE + path, headers={"X-N8N-API-KEY": key, "accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        wf_total, wf_active, cursor = 0, 0, None
        while True:
            page = get("/workflows?limit=250" + (f"&cursor={cursor}" if cursor else ""))
            data = page.get("data", []); wf_total += len(data); wf_active += sum(1 for w in data if w.get("active"))
            cursor = page.get("nextCursor")
            if not cursor: break
        ex = get("/executions?limit=1")
        out["n8n"] = {"workflows_total": wf_total, "workflows_active": wf_active,
                      "latest_execution_id": (ex.get("data") or [{}])[0].get("id")}
    except Exception as exc:
        out["n8n"] = {"error": f"{type(exc).__name__}: {exc}"}
else:
    out["n8n"] = {"skipped": "no key file at ~/.claude/fdh_n8n.key"}

# ---------------------------------------------------------------- write
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "RECEIPTS.json"), "w") as fh:
    json.dump(out, fh, indent=2, default=str)
t, tr = out["terminal"], out["transcripts"]
md = ["# Receipts from the Mac", f"Generated {out['generated_at']}", ""]
if "error" not in t:
    md += ["## Hours",
           f"- Recordings: {t['recordings']} between {t['first_day']} and {t['last_day']} ({t['calendar_days_spanned']} calendar days, {t['days_with_a_session']} with a session)",
           f"- Hours recorded: {t['hours_recorded_total']} total; {t['hours_recorded_excluding_sessions_over_20h']} excluding {t['sessions_over_20h_excluded']} recordings left open over 20h",
           f"- Average per active day: {t['average_hours_per_active_day']} h · sessions per active day: {t['sessions_per_active_day']} · longest session: {t['longest_session_hours']} h",
           f"- Hours by month: {t['hours_by_month']}", ""]
else:
    md += ["## Hours", f"- {t['error']}", ""]
md += ["## Claude Code transcripts",
       f"- Files: {tr['jsonl_files']} · distinct sessions: {tr['distinct_session_ids']} · active days: {tr['days_active']}",
       f"- Span: {tr['first_event']} to {tr['last_event']}",
       f"- Messages you typed: {tr['user_turns_typed']} · assistant events: {tr['assistant_events']} · tool calls: {tr['tool_calls_total']}",
       f"- Tokens: {tr['tokens']} (total {tr['tokens_total_all_kinds']:,})",
       f"- Top tools: {tr['tool_calls_by_tool']}", "",
       "## n8n", f"- {out['n8n']}", "",
       "Paste this file, or RECEIPTS.json, back into the session."]
open(os.path.join(OUT_DIR, "RECEIPTS.md"), "w").write("\n".join(md))
print("\n".join(md))
print(f"\nWritten to {OUT_DIR}/RECEIPTS.md and RECEIPTS.json")
