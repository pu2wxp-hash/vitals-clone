#!/usr/bin/env python3
"""Generate the RaioX Mac app icon as a crisp 1024px PNG using Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
SCALE = 3
N = SIZE * SCALE
OUT = Path(__file__).resolve().parents[1] / "Assets" / "RaioXMac-1024.png"


def q(value):
    return int(round(value * SCALE))


def blend(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for py in range(q(y0), q(y1) + 1):
        t = (py / SCALE - y0) / max(1, (y1 - y0))
        draw.line((q(x0), py, q(x1), py), fill=blend(top, bottom, t))


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(q(v) for v in box), radius=q(radius), fill=fill,
                           outline=outline, width=q(width) if outline else 1)


def line(draw, points, fill, width):
    draw.line([(q(x), q(y)) for x, y in points], fill=fill, width=q(width), joint="curve")


def circle(draw, cx, cy, r, fill, outline=None, width=1):
    box = (q(cx-r), q(cy-r), q(cx+r), q(cy+r))
    draw.ellipse(box, fill=fill, outline=outline, width=q(width) if outline else 1)


# Midnight-blue full-bleed background.
base = Image.new("RGBA", (N, N), (5, 12, 25, 255))
bg = ImageDraw.Draw(base)
for py in range(N):
    t = py / (N - 1)
    bg.line((0, py, N, py), fill=(*blend((13, 29, 52), (4, 9, 20), t), 255))

# Soft cyan illumination behind the chip, kept subtle at small sizes.
glow = Image.new("RGBA", (N, N), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((q(170), q(145), q(854), q(845)), fill=(20, 150, 190, 92))
glow = glow.filter(ImageFilter.GaussianBlur(q(110)))
base = Image.alpha_composite(base, glow)

# Chip shadow and four clean pins on each side.
shadow = Image.new("RGBA", (N, N), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
rounded(sd, (236, 254, 788, 806), 88, (0, 0, 0, 150))
shadow = shadow.filter(ImageFilter.GaussianBlur(q(24)))
base = Image.alpha_composite(base, shadow)
d = ImageDraw.Draw(base)
pin_centres = (410, 614)
for c in pin_centres:
    rounded(d, (c-15, 170, c+15, 252), 14, (43, 142, 171, 255), (112, 218, 233, 255), 5)
    rounded(d, (c-15, 772, c+15, 854), 14, (43, 142, 171, 255), (112, 218, 233, 255), 5)
    rounded(d, (170, c-15, 252, c+15), 14, (43, 142, 171, 255), (112, 218, 233, 255), 5)
    rounded(d, (772, c-15, 854, c+15), 14, (43, 142, 171, 255), (112, 218, 233, 255), 5)

# The chip case clips two halves: opaque silicon above, x-ray cutaway below the scan.
x0, y0, x1, y1, mid = 236, 236, 788, 788, 512
mask = Image.new("L", (N, N), 0)
md = ImageDraw.Draw(mask)
rounded(md, (x0, y0, x1, y1), 88, 255)
inside = Image.new("RGBA", (N, N), (0, 0, 0, 0))
idraw = ImageDraw.Draw(inside)
gradient(idraw, (x0, y0, x1, mid), (30, 126, 156, 255), (18, 76, 104, 255))
gradient(idraw, (x0, mid, x1, y1), (10, 30, 52, 255), (7, 19, 36, 255))
base.paste(inside, (0, 0), mask)
d = ImageDraw.Draw(base)

# Top side is the opaque chip surface; the lower half reveals three bold traces.
trace = (105, 222, 239, 255)
node = (217, 250, 252, 255)
line(d, [(326, 590), (450, 590), (450, 620), (574, 620), (574, 590), (698, 590)], trace, 18)
line(d, [(326, 684), (698, 684)], trace, 18)
line(d, [(512, 548), (512, 736)], trace, 18)
for cx, cy in ((326, 590), (698, 590), (326, 684), (698, 684), (512, 620), (512, 684)):
    circle(d, cx, cy, 12, node)
# Horizontal scan beam: one beam, not an X/cancel symbol.
beam = Image.new("RGBA", (N, N), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.line((q(110), q(512), q(914), q(512)), fill=(91, 230, 245, 210), width=q(34))
beam = beam.filter(ImageFilter.GaussianBlur(q(20)))
base = Image.alpha_composite(base, beam)
d = ImageDraw.Draw(base)
line(d, [(124, 512), (900, 512)], (145, 248, 252, 255), 14)
# Small ice-blue focus point at the scan crossing; no warning/error color.
circle(d, 512, 512, 24, (8, 25, 43, 255), (190, 247, 250, 255), 6)
circle(d, 512, 512, 8, (245, 255, 255, 255))

# Crisp case outline sits above all internal artwork.
d = ImageDraw.Draw(base)
rounded(d, (x0, y0, x1, y1), 88, None, (120, 225, 239, 255), 14)

# Reduce once with high-quality antialiasing and write the master asset.
icon = base.convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
OUT.parent.mkdir(parents=True, exist_ok=True)
icon.save(OUT, format="PNG", optimize=True)
print(f"Wrote {OUT} ({icon.size[0]}x{icon.size[1]})")
