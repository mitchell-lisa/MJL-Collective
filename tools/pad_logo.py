"""Re-cut a logo with real transparent margin on every side.
Trims to the artwork (alpha > 8), scales so the artwork's long side is LONG px,
and adds a margin of about 1.2% of the long side all round, so the edges of
the art are never sliced by the file edge, by rounding, or by object-fit.
usage: pad_logo.py IN OUT LONG"""
import sys
from PIL import Image
src, dst, long_ = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert('RGBA')
im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
s = long_ / max(im.size)
if abs(s - 1) > 1e-3: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
m = max(4, round(.012 * long_))
c = Image.new('RGBA', (im.width + 2 * m, im.height + 2 * m), (0, 0, 0, 0)); c.paste(im, (m, m))
c.save(dst, quality=92, method=6)
print(dst, c.size)
