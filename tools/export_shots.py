#!/usr/bin/env python3
"""Export the high-DPI client captures to responsive AVIF and WebP.
Raw captures (desktop 1440x900 at 2x, phone 390x844 at 3x) live outside the repo
in /workspace/mjl-redesign/hd/. usage: python3 tools/export_shots.py [slug ...]"""
import sys, pathlib
from PIL import Image
RAW = pathlib.Path('/workspace/mjl-redesign/hd')
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'shots'
WIDTHS = {'d': (1200, 1800, 2880), 'p': (360, 720, 1080)}
only = set(sys.argv[1:])
OUT.mkdir(exist_ok=True)
for f in sorted(RAW.glob('*.png')):
    slug = f.stem
    if only and slug not in only: continue
    kind = slug.rsplit('-', 1)[1]
    im = Image.open(f).convert('RGB')
    for w in WIDTHS[kind]:
        r = im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f'{slug}-{w}.avif', quality=62, speed=4)
        r.save(OUT / f'{slug}-{w}.webp', quality=82, method=6)
    print(slug, im.size)
