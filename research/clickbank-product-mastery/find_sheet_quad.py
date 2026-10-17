import sys
import numpy as np
from PIL import Image

# Side edges are near-vertical, so fit them as x = a*y + b.
# Top and bottom edges are near-horizontal, so fit them as y = c*x + d.
# Mixing the two parameterisations keeps both fits well conditioned.


def fit_x_of_y(pts):
    y = np.array([p[0] for p in pts], float)
    x = np.array([p[1] for p in pts], float)
    return np.polyfit(y, x, 1)


def fit_y_of_x(pts):
    x = np.array([p[0] for p in pts], float)
    y = np.array([p[1] for p in pts], float)
    return np.polyfit(x, y, 1)


def meet(side, edge):
    """side: x = a*y + b   edge: y = c*x + d"""
    a, b = side
    c, d = edge
    y = (c * b + d) / (1 - c * a)
    return a * y + b, y


def find(path, verbose=False):
    a = np.asarray(Image.open(path).convert('RGB'), float)
    H, W, _ = a.shape
    lum, sat = a.mean(2), a.max(2) - a.min(2)
    m = (lum > 200) & (sat < 42)
    m[:int(H * 0.55)] = False

    runs = {}
    for y in range(H):
        xs = np.nonzero(m[y])[0]
        if len(xs) < 20:
            continue
        br = np.split(xs, np.where(np.diff(xs) != 1)[0] + 1)
        r = max(br, key=len)
        if len(r) > 30:
            runs[y] = (int(r[0]), int(r[-1]), len(r))

    peak = max(v[2] for v in runs.values())
    ys = sorted(runs)
    wide = [y for y in ys if runs[y][2] > 0.85 * peak]
    lo, hi = wide[0], wide[-1]
    core = [y for y in ys if lo + 8 <= y <= hi - 8]

    left = fit_x_of_y([(y, runs[y][0]) for y in core])
    right = fit_x_of_y([(y, runs[y][1]) for y in core])
    # above `lo` the run's LEFT end traces the top edge; below `hi` its RIGHT end traces the bottom
    top = fit_y_of_x([(runs[y][0], y) for y in ys if y < lo])
    bot = fit_y_of_x([(runs[y][1], y) for y in ys if y > hi])

    q = [meet(left, top), meet(right, top), meet(right, bot), meet(left, bot)]
    print(path, ';'.join('%d,%d' % (x, y) for x, y in q),
          '  w=%d h=%d' % (q[1][0] - q[0][0], q[3][1] - q[0][1]))
    return q


for p in sys.argv[1:]:
    find(p)
