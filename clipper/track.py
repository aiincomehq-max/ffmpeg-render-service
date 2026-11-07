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
