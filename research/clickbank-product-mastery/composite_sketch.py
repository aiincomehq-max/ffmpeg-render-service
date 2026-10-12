import sys
import numpy as np
from PIL import Image, ImageFilter

CREAM = np.array([247., 240., 223.])


def clean_sketch(path):
    """Crop the vendor plate's right-hand bleed, kill the red arrow, neutralise paper."""
    a = np.asarray(Image.open(path).convert('RGB'), float)
    h, w, _ = a.shape
    cm = a.mean(axis=(0, 2))
    cut = w
    for x in range(int(w * 0.85), w):
        if cm[x] < cm[x - 3] - 60:
            cut = x
            break
    a = a[:, :max(0, cut - 8)]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > g + 45) & (r > b + 45) & (r > 120)
    m = red.copy()
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-3, -2, -1, 0, 1, 2, 3):
            m |= np.roll(np.roll(red, dy, 0), dx, 1)
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        src = x
        while src > 0 and m[y, src]:
            src -= 1
        a[y, x] = a[y, src]
    lum = a.mean(2)
    paper = a[lum > np.percentile(lum, 85)].mean(0)
    return np.clip(a * (CREAM / paper), 0, 255)


def make_page(sketch, pw, ph, frac=0.93, left=None, top=0.42):
    """Cream page pw x ph with the sketch laid in, edges feathered into the paper."""
    sw = int(round(pw * frac))
    sh = int(round(sw * sketch.shape[0] / sketch.shape[1]))
    if sh > ph * 0.93:
        sh = int(round(ph * 0.93))
        sw = int(round(sh * sketch.shape[1] / sketch.shape[0]))
    s = np.asarray(
        Image.fromarray(sketch.astype(np.uint8)).resize((sw, sh), Image.LANCZOS), float)

    # the sketch's own paper must read as the same sheet, not a pasted photo
    lum = s.mean(2)
    paper = s[lum > np.percentile(lum, 88)].mean(0)
    s = np.clip(s * (CREAM / paper), 0, 255)

    # feather the block into the page over a small border
    fx = max(4, int(sw * 0.05))
    fy = max(4, int(sh * 0.04))
    ax = np.clip(np.minimum(np.arange(sw), sw - 1 - np.arange(sw)) / fx, 0, 1)
    ay = np.clip(np.minimum(np.arange(sh), sh - 1 - np.arange(sh)) / fy, 0, 1)
    alpha = (ay[:, None] * ax[None, :])[..., None]

    pg = np.zeros((ph, pw, 3), float) + CREAM
    x = (pw - sw) // 2 if left is None else int(round(left * pw))
    y = int(round((ph - sh) * top))
    pg[y:y + sh, x:x + sw] = pg[y:y + sh, x:x + sw] * (1 - alpha) + s * alpha
    return pg


def bilerp(quad, u, v):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad   # TL TR BR BL
    tx, ty = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    bx, by = x3 + (x2 - x3) * u, y3 + (y2 - y3) * u
    return tx + (bx - tx) * v, ty + (by - ty) * v


def warp_onto(plate, page, quad, feather=2.0):
    """Inverse-map every pixel inside quad back to the page, keeping the plate's lighting."""
    P = np.asarray(plate, float)
    H, W, _ = P.shape
    ph, pw, _ = page.shape

    xs = [p[0] for p in quad]
    ys = [p[1] for p in quad]
    x0, x1 = int(min(xs)) - 2, int(max(xs)) + 3
    y0, y1 = int(min(ys)) - 2, int(max(ys)) + 3
    gx, gy = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))

    # solve for (u, v) by Newton on the bilinear map — 6 iterations is plenty
    u = np.full(gx.shape, 0.5)
    v = np.full(gx.shape, 0.5)
    q = np.array(quad, float)
    for _ in range(12):
        tx = q[0, 0] + (q[1, 0] - q[0, 0]) * u
        ty = q[0, 1] + (q[1, 1] - q[0, 1]) * u
        bx = q[3, 0] + (q[2, 0] - q[3, 0]) * u
        by = q[3, 1] + (q[2, 1] - q[3, 1]) * u
        fx = tx + (bx - tx) * v - gx
        fy = ty + (by - ty) * v - gy
        dxu = (q[1, 0] - q[0, 0]) * (1 - v) + (q[2, 0] - q[3, 0]) * v
        dyu = (q[1, 1] - q[0, 1]) * (1 - v) + (q[2, 1] - q[3, 1]) * v
        dxv = bx - tx
        dyv = by - ty
        det = dxu * dyv - dxv * dyu
        det = np.where(np.abs(det) < 1e-9, 1e-9, det)
        u -= (fx * dyv - fy * dxv) / det
        v -= (dxu * fy - dyu * fx) / det

    inside = (u > -0.02) & (u < 1.02) & (v > -0.02) & (v < 1.02)
    su = np.clip(u, 0, 1) * (pw - 1)
    sv = np.clip(v, 0, 1) * (ph - 1)
    i0 = np.clip(su.astype(int), 0, pw - 2)
    j0 = np.clip(sv.astype(int), 0, ph - 2)
    fu = (su - i0)[..., None]
    fv = (sv - j0)[..., None]
    samp = (page[j0, i0] * (1 - fu) * (1 - fv) + page[j0, i0 + 1] * fu * (1 - fv)
            + page[j0 + 1, i0] * (1 - fu) * fv + page[j0 + 1, i0 + 1] * fu * fv)

    region = P[y0:y1, x0:x1]
    # Carry the plate's lighting, but only its low frequencies: a hard shadow edge
    # reproduced over a face reads as dirt on the print, not as light in the room.
    blur = np.asarray(
        Image.fromarray(np.clip(region, 0, 255).astype(np.uint8))
        .filter(ImageFilter.GaussianBlur(radius=max(6, (x1 - x0) * 0.12))), float)
    if inside.any():
        base = np.array([np.median(blur[..., c][inside]) for c in range(3)])
    else:
        base = blur.reshape(-1, 3).mean(0)
    shade = np.clip(blur / np.maximum(base, 1e-6), 0.72, 1.28)
    lit = np.clip(samp * shade, 0, 255)

    a = inside.astype(float)
    # soften the quad edge so it does not cut like a sticker
    for _ in range(int(feather)):
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5.0
    a = (a * inside)[..., None]
    P[y0:y1, x0:x1] = region * (1 - a) + lit * a
    return Image.fromarray(np.clip(P, 0, 255).astype(np.uint8))


if __name__ == '__main__':
    plate, sketch_path, quad_s, out = sys.argv[1:5]
    opts = dict(t.split('=') for t in sys.argv[5:])
    quad = [tuple(float(t) for t in p.split(',')) for p in quad_s.split(';')]
    sk = clean_sketch(sketch_path)
    if 'page' in opts:
        w, h = (int(t) for t in opts['page'].split('x'))
    else:
        w = int(round(np.hypot(quad[1][0] - quad[0][0], quad[1][1] - quad[0][1])))
        h = int(round(np.hypot(quad[3][0] - quad[0][0], quad[3][1] - quad[0][1])))
    page = make_page(sk, w, h,
                     frac=float(opts.get('frac', 0.93)),
                     left=float(opts['left']) if 'left' in opts else None,
                     top=float(opts.get('top', 0.42)))
    img = warp_onto(Image.open(plate).convert('RGB'), page, quad)
    img.save(out, quality=95)
    print(out, img.size, 'quad', quad, 'page', page.shape)
