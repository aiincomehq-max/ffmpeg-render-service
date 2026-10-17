import sys
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, '.')
from composite import clean_sketch, CREAM, CONTRAST

W, H = 1200, 800


def build(src, out, left_frac=0.17):
    s = clean_sketch(src)
    s = np.clip(CREAM - (CREAM - s) * CONTRAST, 0, 255)
    sk = Image.fromarray(s.astype(np.uint8))

    # the drawing carries the ad, so give it nearly the full height
    sh = int(H * 0.90)
    sw = int(round(sh * sk.width / sk.height))
    sk = sk.resize((sw, sh), Image.LANCZOS)

    # warm paper field, very slightly graded so it does not look like flat fill
    yy, xx = np.mgrid[0:H, 0:W]
    grad = 1.0 - 0.055 * (xx / W) - 0.03 * (yy / H)
    bg = np.clip(CREAM * grad[..., None] * 1.02, 0, 255)
    canvas = Image.fromarray(bg.astype(np.uint8))

    x = int(W * left_frac)
    y = (H - sh) // 2

    # a soft drop shadow so the sheet sits on the surface instead of floating
    sh_layer = Image.new('L', (W, H), 0)
    sh_layer.paste(255, (x + 10, y + 14, x + sw + 10, y + sh + 14))
    sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(18))
    dark = Image.new('RGB', (W, H), (120, 108, 92))
    canvas = Image.composite(dark, canvas, sh_layer.point(lambda v: int(v * 0.30)))

    canvas.paste(sk, (x, y))
    canvas.save(out, quality=95)
    print(out, (x, y, sw, sh))


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
