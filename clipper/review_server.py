"""Local approve-and-post page: http://localhost:8765

Each Short: watch it, pick (or edit) a title, tick platforms, Approve -> scheduled into the next
free slot via Blotato. Skip hides it. Runs only on your Mac (127.0.0.1).
"""
from __future__ import annotations

import html
import json
import re
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import blotato, publish

PAGE_CSS = """body{font-family:system-ui;background:#111;color:#eee;margin:16px}.g{display:flex;flex-wrap:wrap;gap:16px}
.c{width:320px;background:#1c1c1c;border-radius:12px;overflow:hidden}.c.done{opacity:.55}
video{width:320px;aspect-ratio:9/16;background:#000;display:block}.m{padding:10px;font-size:14px}
label{display:block;margin:4px 0;cursor:pointer}input[type=text]{width:100%;box-sizing:border-box;padding:6px;
background:#222;color:#eee;border:1px solid #444;border-radius:6px}.btns{display:flex;gap:6px;margin-top:8px}
button{flex:1;padding:9px;border:0;border-radius:8px;font-weight:700;cursor:pointer}.ok{background:#22c55e;color:#000}
.now{background:#3b82f6;color:#fff}.no{background:#444;color:#eee}.badge{display:inline-block;padding:2px 8px;
border-radius:99px;background:#333;font-size:12px}.warn{background:#7c2d12;padding:10px;border-radius:8px;margin-bottom:12px}
.plat{display:flex;gap:10px;flex-wrap:wrap}.sched{font-size:13px;color:#aaa}"""


def latest_day(ch_out: Path) -> Path | None:
    days = sorted([d for d in ch_out.glob("*") if d.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}$", d.name)])
    return days[-1] if days else None


def render_page(ch: dict, day: Path) -> str:
    posts = json.loads((day / "posts.json").read_text()) if (day / "posts.json").exists() else []
    st = publish.load_state(ch)
    ids = ch.get("blotato", {})
    cards = []
    for i, p in enumerate(posts):
        key = f"{day.name}/{p['file']}"
        s = st.get(key, {})
        titles = p.get("titles") or [""]
        radios = "".join(
            f'<label><input type=radio name=t{i} value="{html.escape(t)}" {"checked" if j == 0 else ""}> {html.escape(t)}</label>'
            for j, t in enumerate(titles))
        plats = "".join(
            f'<label><input type=checkbox name=p{i} value={pl} {"checked" if ids.get(pl) or blotato.dry_run() else "disabled"}> '
            f'{pl}{"" if ids.get(pl) else " <small>(no account id)</small>"}</label>' for pl in publish.PLATFORMS)
        badge = ""
        if s:
            when = f" {s['slot'][5:16].replace('T', ' ')}" if s.get("slot") else ""
            badge = f'<span class=badge>{s["status"]}{when}{" (dry run)" if s.get("dry_run") else ""}</span>'
        cards.append(f"""<div class="c{' done' if s else ''}" id=c{i}>
<video src="/media/{html.escape(p['file'])}" controls preload=metadata playsinline></video><div class=m>
<b>{publish.batch_label(p)}</b> · <b>{html.escape(p.get('format', ''))}</b> · score {p.get('virality', '-')} {badge}<br><small>{html.escape(p.get('why') or '')}</small>
<div style=margin-top:8px>{radios}<label><input type=radio name=t{i} value=__custom> custom:</label>
<input type=text id=custom{i} placeholder="your own title"></div>
<div class=plat style=margin-top:6px>{plats}</div>
<div class=btns><button class=ok onclick="act({i},'approve','slot')">Approve</button>
<button class=now onclick="act({i},'approve','now')">Post now</button><button class=no onclick="act({i},'skip')">Skip</button></div>
<div id=r{i} class=sched></div></div></div>""")
    sched = sorted([(v["slot"], k, v.get("title", "")) for k, v in st.items() if v.get("status") == "scheduled" and v.get("slot")])
    sched_html = "".join(f"<li>{s[:16].replace('T', ' ')}: {html.escape(t)}</li>" for s, _, t in sched[-12:])
    warn = ('<div class=warn>DRY RUN: nothing is sent. Add BLOTATO_API_KEY to .env and the account ids to '
            'channels.json ("blotato") to post for real.</div>') if blotato.dry_run() else ""
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Approve · {ch['key']}</title><style>{PAGE_CSS}</style>
<h2>{ch['key']} · {day.name} · {len(posts)} Shorts</h2>{warn}
<details><summary>Scheduled ({len(sched)})</summary><ul>{sched_html}</ul></details><div class=g>{''.join(cards)}</div>
<script>
async function act(i, action, when){{
  const r=document.getElementById('r'+i); r.textContent='working...';
  let t=(document.querySelector('input[name=t'+i+']:checked')||{{}}).value||'';
  if(t==='__custom') t=document.getElementById('custom'+i).value.trim();
  const plats=[...document.querySelectorAll('input[name=p'+i+']:checked')].map(x=>x.value);
  if(action==='approve' && (!t || !plats.length)){{ r.textContent='pick a title and at least one platform'; return; }}
  const res=await fetch('/'+action,{{method:'POST',headers:{{'Content-Type':'application/json'}},
    body:JSON.stringify({{index:i,title:t,platforms:plats,when:when}})}});
  const j=await res.json(); r.textContent=j.error?('ERROR: '+j.error):(j.status+(j.slot?' for '+j.slot.slice(0,16).replace('T',' '):'')
    +(j.dry_run?' (dry run)':''));
  if(!j.error) document.getElementById('c'+i).classList.add('done');
}}
</script>"""


def make_handler(ch: dict, day: Path):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, code: int, obj: dict):
            b = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                b = render_page(ch, day).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)
                return
            if self.path.startswith("/media/"):
                f = day / Path(self.path[7:]).name
                if not f.exists():
                    self.send_error(404)
                    return
                size = f.stat().st_size
                rng = self.headers.get("Range")
                start, end = 0, size - 1
                if rng and rng.startswith("bytes="):  # Safari needs range requests for <video>
                    a, _, b = rng[6:].partition("-")
                    start = int(a) if a else 0
                    end = int(b) if b else size - 1
                    self.send_response(206)
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                else:
                    self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(end - start + 1))
                self.end_headers()
                with open(f, "rb") as fh:
                    fh.seek(start)
                    remaining = end - start + 1
                    while remaining > 0:
                        chunk = fh.read(min(1 << 20, remaining))
                        if not chunk:
                            break
                        try:
                            self.wfile.write(chunk)
                        except (BrokenPipeError, ConnectionResetError):
                            return
                        remaining -= len(chunk)
                return
            self.send_error(404)

        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                posts = json.loads((day / "posts.json").read_text())
                post = posts[int(body["index"])]
                if self.path == "/approve":
                    res = publish.approve(ch, day, post, body["title"], body["platforms"], body.get("when", "slot"))
                elif self.path == "/skip":
                    res = publish.skip(ch, day, post)
                else:
                    self.send_error(404)
                    return
                self._json(200, res)
            except Exception as e:
                self._json(200, {"error": str(e)})
    return H


def serve(ch: dict, day: Path, port: int = 8765, open_browser: bool = True, timeout_h: float = 0) -> None:
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(ch, day))
    url = f"http://localhost:{port}"
    print(f"Approve page: {url}   (Ctrl+C to stop)")
    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    if timeout_h:
        threading.Timer(timeout_h * 3600, srv.shutdown).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
