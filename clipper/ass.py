"""Generate .ass subtitle files: word-highlight captions, action tags, headers, watermark."""
from __future__ import annotations

import re

from .style import color

W, H = 1080, 1920


def ass_color(hex_rgb: str, alpha: int = 0) -> str:
    h = hex_rgb.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def ts(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int(sec % 3600 // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def clean(text: str) -> str:
    return re.sub(r"[{}\\]", "", text).strip()


def header(style: dict) -> str:
    g = style["global"]
    font = "Montserrat Black"
    stroke = g["text_stroke"]["px"]
    white = ass_color("#FFFFFF")
    black = ass_color("#000000")
    yellow = ass_color(color(style, "yellow"))
    wm = g["watermark"]
    wm_alpha = int(255 * (1 - wm["opacity"]))
    # Alignment 5 = middle-centre, 8 = top-centre, 2 = bottom-centre. MarginV used with \pos anyway.
    styles = [
        f"Style: Caption,{font},92,{white},{white},{black},{ass_color('#000000', 80)},-1,0,0,0,100,100,0,0,1,{stroke},3,5,40,40,0,1",
        f"Style: Tag,{font},78,{yellow},{yellow},{black},{ass_color('#000000', 80)},-1,0,0,0,100,100,0,0,1,{stroke},3,5,40,40,0,1",
        # Opening hook: the first frame is what decides the swipe, so it must read as a headline.
        f"Style: Hook,{font},120,{yellow},{yellow},{black},{ass_color('#000000', 60)},-1,0,0,0,100,100,0,0,1,{stroke + 4},5,5,50,50,0,1",
        f"Style: Header,{font},84,{yellow},{yellow},{black},{ass_color('#000000', 80)},-1,0,0,0,100,100,0,0,1,{stroke + 1},3,8,40,40,0,1",
        f"Style: Watermark,{font},40,{ass_color(wm['color'], wm_alpha)},{white},{ass_color('#000000', min(255, wm_alpha + 60))},{ass_color('#000000', 255)},0,0,0,0,100,100,1,0,1,2,0,2,40,40,0,1",
    ]
    return (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        + "\n".join(styles)
        + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )


def pop(scale_from: int = 125) -> str:
    """Pop-in animation tags (scale overshoot)."""
    return f"\\fscx{scale_from}\\fscy{scale_from}\\t(0,90,\\fscx100\\fscy100)"


def group_words(words: list[dict], max_words: int = 3, max_gap: float = 0.45) -> list[list[dict]]:
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["s"] - cur[-1]["e"] > max_gap or re.search(r"[.!?]$", cur[-1]["w"])):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return groups


def caption_events(words: list[dict], style: dict, active_hex: str, y_pct: float) -> list[str]:
    """Word-by-word highlight: each word gets its own event showing the group with the active word coloured."""
    y = int(H * y_pct / 100)
    act = ass_color(active_hex)
    raw = []
    for grp in group_words(sorted(words, key=lambda w: w["s"])):
        for i, w in enumerate(grp):
            start = w["s"]
            end = grp[i + 1]["s"] if i + 1 < len(grp) else max(w["e"], w["s"] + 0.25)
            parts = []
            for j, ww in enumerate(grp):
                txt = clean(ww["w"]).upper().strip(",.")
                parts.append(f"{{\\c{act}}}{txt}{{\\r}}" if j == i else txt)
            anim = pop(112) if i == 0 else ""
            raw.append([start, end, f"{{\\pos({W // 2},{y}){anim}}}" + " ".join(parts)])
    # Captions share one position: two live at once draw on top of each other ("TYOU THANK YOUK").
    # End every event no later than the next one starts.
    for k in range(len(raw) - 1):
        raw[k][1] = min(raw[k][1], raw[k + 1][0])
    return [f"Dialogue: 1,{ts(s0)},{ts(s1)},Caption,,0,0,0,,{txt}" for s0, s1, txt in raw if ts(s1) > ts(s0)]


def text_event(text: str, start: float, end: float, style_name: str, y_pct: float, hex_color: str | None = None, animate: bool = True, layer: int = 2) -> str:
    y = int(H * y_pct / 100)
    col = f"\\c{ass_color(hex_color)}" if hex_color else ""
    anim = pop() if animate else ""
    return f"Dialogue: {layer},{ts(start)},{ts(end)},{style_name},,0,0,0,,{{\\pos({W // 2},{y}){col}{anim}}}{clean(text).upper()}"


def watermark_event(handle: str, duration: float, y_pct: float) -> str:
    y = int(H * y_pct / 100)
    return f"Dialogue: 0,{ts(0)},{ts(duration)},Watermark,,0,0,0,,{{\\an5\\pos({W // 2},{y})}}{clean(handle)}"
