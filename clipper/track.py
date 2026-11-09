"""Face-tracked 9:16 crop path (YuNet face detector, OpenCV).

Behaves like a camera operator: holds still while the face stays near the centre of the
crop, then eases over when it drifts. Falls back to centre crop if no face is found.
"""
from __future__ import annotations

import cv2
import numpy as np

from . import ASSETS

MODEL = ASSETS / "models" / "face_detection_yunet_2023mar.onnx"
SAMPLE_FPS = 5
DET_W = 640
DEADZONE = 0.06      # fraction of source width the face may drift before the crop moves
EASE = 0.5           # per-sample easing toward target (0..1)

_det = None
try:
    cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
except Exception:
    pass


def _detector(w: int, h: int):
    global _det
    if _det is None:
        _det = cv2.FaceDetectorYN.create(str(MODEL), "", (w, h), 0.6, 0.3, 50)
    _det.setInputSize((w, h))
    return _det


def _faces(frame: np.ndarray) -> list[tuple[float, float, float]]:
    """Returns [(cx_norm, area_norm, score)]."""
    h, w = frame.shape[:2]
    scale = DET_W / w
    small = cv2.resize(frame, (DET_W, int(h * scale)))
    det = _detector(small.shape[1], small.shape[0])
    _, faces = det.detect(small)
    out = []
    if faces is not None:
        for f in faces:
            x, y, fw, fh, score = f[0], f[1], f[2], f[3], f[-1]
            out.append(((x + fw / 2) / small.shape[1], (fw * fh) / (small.shape[0] * small.shape[1]), float(score)))
    return out


def face_boxes_at(src: str, t: float) -> list[tuple[float, float, float, float]]:
    """Face boxes (x, y, w, h) in the source frame's pixels at time t. Empty if none/unreadable."""
    cap = cv2.VideoCapture(src)
    try:
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, t) * 1000)
        ok, frame = cap.read()
    finally:
        cap.release()
    if not ok:
        return []
    h, w = frame.shape[:2]
    k = DET_W / w
    small = cv2.resize(frame, (DET_W, int(h * k)))
    _, faces = _detector(small.shape[1], small.shape[0]).detect(small)
    return [(f[0] / k, f[1] / k, f[2] / k, f[3] / k) for f in (faces if faces is not None else [])]


def clear_x(boxes, cy: float, size: float, frame_w: float) -> float:
    """x-centre for a size*size overlay at height cy that doesn't cover a face: centre if free,
    otherwise the side away from the face (centre if that still overlaps)."""
    def hits(cx):
        return any(cx - size / 2 < x + bw and x < cx + size / 2 and cy - size / 2 < y + bh and y < cy + size / 2
                   for x, y, bw, bh in boxes)
    if not hits(frame_w / 2):
        return frame_w / 2
    fx = sum(x + bw / 2 for x, _, bw, _ in boxes) / len(boxes)
    side = frame_w * 0.8 if fx < frame_w / 2 else frame_w * 0.2
    return side if not hits(side) else frame_w / 2


def centers(src: str, start: float, end: float) -> list[tuple[float, float | None]]:
    """Sample the source between start/end; return [(t_rel, face_cx_norm or None)]."""
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        return []
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    step = max(1, int(round(fps / SAMPLE_FPS)))
    out, prev, i = [], None, 0
    t = start
    while t < end:
        ok = cap.grab()
        if not ok:
            break
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if i % step == 0 and t >= start:
            ok, frame = cap.retrieve()
            if not ok:
                break
            fs = _faces(frame)
            cx = None
            if fs:
                big = max(a for _, a, _ in fs)
                cands = [f for f in fs if f[1] >= 0.5 * big]
                if prev is not None:
                    cx = min(cands, key=lambda f: abs(f[0] - prev))[0]
                else:
                    cx = max(cands, key=lambda f: f[1] * f[2])[0]
                prev = cx
            out.append((t - start, cx))
        i += 1
    cap.release()
    return out


def smooth_path(samples: list[tuple[float, float | None]]) -> list[tuple[float, float]] | None:
    """Camera-operator smoothing. Returns [(t_rel, cx_norm)] or None if no faces at all."""
    if not samples or all(c is None for _, c in samples):
        return None
    xs = [c for _, c in samples]
    # fill gaps with nearest known value
    known = [i for i, c in enumerate(xs) if c is not None]
    for i, c in enumerate(xs):
        if c is None:
            j = min(known, key=lambda k: abs(k - i))
            xs[i] = xs[j]
    # median filter (kills single-frame false detections)
    k = 2
    med = [float(np.median(xs[max(0, i - k): i + k + 1])) for i in range(len(xs))]
    # deadzone + easing
    cur = med[0]
    path = []
    for (t, _), target in zip(samples, med):
        if abs(target - cur) > DEADZONE:
            cur += (target - cur) * EASE
        path.append((t, cur))
    return path


def crop_keyframes(src: str, start: float, end: float, src_w: int, src_h: int, out_w: int, out_h: int,
                   zoom: float, speed: float) -> list[tuple[float, int]] | None:
    """[(t_out, crop_x_px)] in the scaled frame, or None for centre crop."""
    if src_w / src_h < 1.2:  # already vertical-ish: centre crop is fine
        return None
    path = smooth_path(centers(src, start, end))
    if not path:
        return None
    scaled_w = src_w * (out_h * zoom) / src_h
    kf = []
    for t, cx in path:
        x = cx * scaled_w - out_w / 2
        x = int(max(0, min(scaled_w - out_w, x)))
        kf.append((t / speed, x))
    return kf


# ---- 9 Nov: "stacked" layout for gaming streams (webcam panel on top, gameplay below) ----
CAM_PANEL = (1080, 600)    # output size of the webcam panel
GAME_PANEL = (1080, 820)   # output size of the gameplay panel


def webcam_box(src: str, start: float, end: float, n: int = 6):
    """A streamer webcam = a face that stays in the same place through the clip (IRL faces and game characters move).
    Returns (x, y, w, h, src_w, src_h) of the median face box, or None."""
    cap = cv2.VideoCapture(src)
    sw, sh = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frames = []
    try:
        for i in range(n):
            cap.set(cv2.CAP_PROP_POS_MSEC, (start + (end - start) * (i + 0.5) / n) * 1000)
            ok, fr = cap.read()
            if not ok:
                continue
            k = DET_W / fr.shape[1]
            small = cv2.resize(fr, (DET_W, int(fr.shape[0] * k)))
            _, faces = _detector(small.shape[1], small.shape[0]).detect(small)
            frames.append([(f[0] / k, f[1] / k, f[2] / k, f[3] / k) for f in (faces if faces is not None else [])])
    finally:
        cap.release()
    if not sw or len(frames) < 3:
        return None
    best = None
    for fb in frames:
        for b in fb:
            cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
            hits = []
            for other in frames:
                m = [o for o in other if abs(o[0] + o[2] / 2 - cx) < 0.04 * sw and abs(o[1] + o[3] / 2 - cy) < 0.05 * sh
                     and 0.7 < (o[2] / max(b[2], 1)) < 1.4]
                if m:
                    hits.append(m[0])
            if len(hits) >= len(frames) - 1 and (best is None or len(hits) > len(best)):
                best = hits
    if not best:
        return None
    med = [float(np.median([h[i] for h in best])) for i in range(4)]
    if med[3] > 0.22 * sh:  # a face that big is an in-game close-up (GTA RP), not a webcam overlay
        return None
    if med[3] * 2.6 * CAM_PANEL[0] / CAM_PANEL[1] < 300:  # webcam too small: blown up 4x it's just blur
        return None
    return (*med, sw, sh)


def stacked_rects(cam):
    """From webcam_box -> {'cam': [x,y,w,h], 'game': [x,y,w,h]} in source pixels.
    Game crop = the largest centred-ish GAME_PANEL-shaped window that keeps the webcam face out of it."""
    x, y, w, h, sw, sh = cam
    ar_c = CAM_PANEL[0] / CAM_PANEL[1]
    ch = min(sh, h * 2.6)
    cw = min(sw, ch * ar_c)
    ch = cw / ar_c
    cx = min(max(0, x + w / 2 - cw / 2), sw - cw)
    cy = min(max(0, y + h * 0.45 - ch / 2), sh - ch)
    ar_g = GAME_PANEL[0] / GAME_PANEL[1]
    fx0, fy0, fx1, fy1 = x - w * 0.3, y - h * 0.3, x + w * 1.3, y + h * 1.6   # face + a margin = keep out
    game = None
    for frac in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5):
        gh = sh * frac
        gw = min(sw, gh * ar_g)
        gh = gw / ar_g
        cands = []
        for gx in np.linspace(0, sw - gw, 9):
            for gy in np.linspace(0, sh - gh, 5):
                if not (gx < fx1 and fx0 < gx + gw and gy < fy1 and fy0 < gy + gh):
                    cands.append((abs(gx + gw / 2 - sw / 2) + abs(gy + gh / 2 - sh / 2), gx, gy))
        if cands:
            _, gx, gy = min(cands)
            game = [gx, gy, gw, gh]
            break
    if game is None:  # webcam sits in the middle of everything: plain centre crop
        gw = min(sw, sh * ar_g); gh = gw / ar_g
        game = [(sw - gw) / 2, (sh - gh) / 2, gw, gh]
    ev = lambda v: int(v) // 2 * 2
    return {"cam": [ev(cx), ev(cy), ev(cw), ev(ch)], "game": [ev(v) for v in game]}
