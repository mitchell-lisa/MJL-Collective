"""Rebuild the clipped right edge of the Simo's wordmark.

Every copy of the colour mark (including the one on simosbarbering.com) is cut
flat at the right edge: the outer dark halo of the final s is sliced on its two
bulges, and the rule after OF WAYNE, PA runs off the edge. The copper ring
inside the halo is intact, and the halo is a band of near-constant width around
it, so the missing halo is redrawn as that same offset of the copper/white
artwork, onto a canvas padded on the right. Nothing else is touched.
usage: repair_simos_right.py IN OUT [PAD]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, dst = sys.argv[1], sys.argv[2]
PAD = int(sys.argv[3]) if len(sys.argv) > 3 else 22
a = np.array(Image.open(src).convert('RGBA')).astype(float)
H, W = a.shape[:2]
A = a[..., 3]; R, G, B = a[..., 0], a[..., 1], a[..., 2]
luma = .299 * R + .587 * G + .114 * B
bright = (A > 200) & (luma > 70)          # copper ring, white letter, copper rule

# halo width, measured on intact outer edges in the right-hand part of the mark
dist = ndi.distance_transform_edt(~bright)
edge = (A > 128) & ~ndi.binary_erosion(A > 128)
zone = np.zeros_like(edge); zone[:, int(W * .78):W - 8] = True
samples = dist[edge & zone]
samples = samples[(samples > 1) & (samples < 25)]
d = float(np.median(samples))
print('halo width', round(d, 2), 'from', samples.size, 'edge pixels')

# canvas padded on the right, bright mask extended so its distance field is right
NW = W + PAD
out = np.zeros((H, NW, 4)); out[:, :W] = a
br = np.zeros((H, NW), bool); br[:, :W] = bright
dist2 = ndi.distance_transform_edt(~br)
halo_a = np.clip((d + 1.25 - dist2) / 2.5, 0, 1) * 255  # soft 2.5px edge, like the original
col = np.array([15, 10, 0], float)                       # the halo's own colour
xx = np.arange(NW)[None, :].repeat(H, 0)
fix = (xx >= W - 3) & (halo_a > out[..., 3])              # only the cut strip and the pad
# composite: halo under whatever original pixels exist there
oa = out[..., 3] / 255.0; ha = halo_a / 255.0
na = oa + ha * (1 - oa)
rgb = (out[..., :3] * oa[..., None] + col * (ha * (1 - oa))[..., None]) / np.maximum(na, 1e-6)[..., None]
out[fix, :3] = rgb[fix]; out[fix, 3] = na[fix] * 255
o = np.clip(np.round(out), 0, 255).astype(np.uint8)
im = Image.fromarray(o, 'RGBA')
bb = im.getbbox(); print('size', im.size, 'bbox', bb, 'right margin', NW - bb[2])
if dst.endswith('.webp'): im.save(dst, quality=92, method=6)
else: im.save(dst)
