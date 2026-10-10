#!/usr/bin/env python3
"""MJL glass block, drawn as SVG. Run from the repo root: python3 tools/glass.py

A 2x2 tile of real-looking glass block: thin mortar joints, a translucent face
that lets whatever sits behind it show through, wavy refraction running down
each block, a soft inner bevel, light catching the top and left edges, and a
small specular highlight. The four blocks differ slightly in phase, the way
pressed glass does.

Colors: the six MJL colors plus one cool glass tint (--glass, #cfdad8), which
is cement pushed a little cool. Most fills are partly transparent on purpose.

  glass-dark.svg   for the poured bands: clear glass in front of a dark room
  glass-light.svg  for plaster grounds: glass with daylight behind it
"""
import math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
POURED, INK, PLASTER, CEMENT, MORTAR, INK2 = "#2b2825", "#1c1a17", "#f4f0e9", "#ebe6dc", "#d5cec2", "#565047"
GLASS = "#cfdad8"
B, J = 100, 1.6          # block size, half mortar joint (thin joints)

V = {
  "glass-dark": dict(joint=INK2, joint_op=.85, face=GLASS, face_op=.05, center=GLASS, center_op=.10,
                     wave=GLASS, wave_op=.13, wave_dark=INK, wave_dark_op=.32,
                     hi=PLASTER, hi_op=.30, edge=PLASTER, edge_op=.26, shade=INK, shade_op=.45, spec=PLASTER, spec_op=.22),
  "glass-light": dict(joint=MORTAR, joint_op=1, face=GLASS, face_op=.30, center=PLASTER, center_op=.55,
                      wave=PLASTER, wave_op=.8, wave_dark=GLASS, wave_dark_op=.75,
                      hi=PLASTER, hi_op=.95, edge=PLASTER, edge_op=1, shade=INK2, shade_op=.16, spec=PLASTER, spec_op=1),
}

def wave_path(x, phase, amp=3.4, step=23):
    y0, y1 = -14, B + 14
    d = f"M{x + amp * math.sin(phase):.2f} {y0}"
    y = y0
    while y < y1:
        ny = min(y + step, y1)
        a1 = x + amp * math.sin(phase + (y - y0 + step / 3) / step * math.pi)
        a2 = x + amp * math.sin(phase + (y - y0 + 2 * step / 3) / step * math.pi)
        a3 = x + amp * math.sin(phase + (ny - y0) / step * math.pi)
        d += f" C{a1:.2f} {y + step / 3:.2f} {a2:.2f} {y + 2 * step / 3:.2f} {a3:.2f} {ny:.2f}"
        y = ny
    return d

def block(v, i, ox, oy):
    ph = [0, 1.7, 3.1, 4.6][i]
    f0, f1 = J, B - J
    w = f1 - f0
    o = [f'<g transform="translate({ox} {oy})">']
    o.append(f'<rect x="{f0}" y="{f0}" width="{w}" height="{w}" rx="2.2" fill="{v["face"]}" fill-opacity="{v["face_op"]}"/>')
    o.append(f'<rect x="{f0}" y="{f0}" width="{w}" height="{w}" rx="2.2" fill="url(#c{i})"/>')
    # wavy refraction: broad soft ripples, a bright line with a darker twin beside it.
    # One ripple is drawn per block and reused across the face with <use>.
    o.append(f'<g clip-path="url(#face)" filter="url(#ripple)" fill="none" stroke-linecap="round">')
    for k in range(5):
        x = (k - 2) * (w - 12) / 4.0
        dy = (k * 7 + i * 5) % 23 - 11
        o.append(f'<use href="#w{i % 2}" x="{x:.1f}" y="{dy}"/>')
    o.append('</g>')
    # soft inner bevel: light from the top left, shade to the bottom right
    o.append(f'<rect x="{f0 + 3}" y="{f0 + 3}" width="{w - 6}" height="{w - 6}" rx="1.6" fill="none" stroke="url(#bev)" stroke-width="6" filter="url(#soft)"/>')
    # light catching the edges
    o.append(f'<path d="M{f0 + .8} {f1 - 6}V{f0 + 2.4}Q{f0 + .8} {f0 + .8} {f0 + 2.4} {f0 + .8}H{f1 - 6}" fill="none" stroke="{v["edge"]}" stroke-opacity="{v["edge_op"]}" stroke-width=".9"/>')
    # specular highlight
    sx, sy = [(24, 20), (70, 26), (30, 64), (66, 70)][i]
    o.append(f'<ellipse cx="{sx}" cy="{sy}" rx="15" ry="6" transform="rotate(-35 {sx} {sy})" fill="url(#sp)"/>')
    o.append('</g>')
    return "".join(o)

def tile(v):
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">', '<defs>']
    o.append('<filter id="soft" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation=".9"/></filter>')
    o.append(f'<linearGradient id="bev" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{v["hi"]}" stop-opacity="{v["hi_op"]}"/>'
             f'<stop offset=".45" stop-color="{v["hi"]}" stop-opacity="0"/><stop offset=".55" stop-color="{v["shade"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{v["shade"]}" stop-opacity="{v["shade_op"]}"/></linearGradient>')
    o.append(f'<radialGradient id="sp"><stop offset="0" stop-color="{v["spec"]}" stop-opacity="{v["spec_op"]}"/><stop offset="1" stop-color="{v["spec"]}" stop-opacity="0"/></radialGradient>')
    for i, (cx, cy) in enumerate([(.42, .38), (.58, .4), (.4, .6), (.6, .58)]):
        o.append(f'<radialGradient id="c{i}" cx="{cx}" cy="{cy}" r=".62"><stop offset="0" stop-color="{v["center"]}" stop-opacity="{v["center_op"]}"/>'
                 f'<stop offset="1" stop-color="{v["center"]}" stop-opacity="0"/></radialGradient>')
    for n, ph in enumerate((0, 2.2)):
        cx = 50
        o.append(f'<g id="w{n}"><path d="{wave_path(cx, ph)}" stroke="{v["wave"]}" stroke-opacity="{v["wave_op"]}" stroke-width="5"/>'
                 f'<path d="{wave_path(cx + 6, ph)}" stroke="{v["wave_dark"]}" stroke-opacity="{v["wave_dark_op"]}" stroke-width="3.4"/></g>')
    o.append(f'<clipPath id="face"><rect x="{J}" y="{J}" width="{B - 2 * J}" height="{B - 2 * J}" rx="2.2"/></clipPath>')
    o.append('<filter id="ripple" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.7"/></filter>')
    o.append('</defs>')
    # mortar joints: a frame around each block, so the face itself stays see-through
    jp = []
    for x in (0, B):
        for y in (0, B):
            jp.append(f"M{x} {y}h{B}v{B}h-{B}z M{x + J} {y + J}v{B - 2 * J}h{B - 2 * J}v-{B - 2 * J}z")
    o.append(f'<path fill-rule="evenodd" d="{" ".join(jp)}" fill="{v["joint"]}" fill-opacity="{v["joint_op"]}"/>')
    for i, (x, y) in enumerate([(0, 0), (B, 0), (0, B), (B, B)]):
        o.append(block(v, i, x, y))
    o.append('</svg>')
    return "".join(o)

for name, v in V.items():
    s = tile(v)
    (ROOT / "assets" / f"{name}.svg").write_text(s + "\n")
    print(name, len(s), "bytes")

# What stands behind the glass on the dark bands: a stair, rising to the right,
# in the glass tint. backdrop-filter blurs it further where supported, so it
# reads as something seen through glass block (a nod to the photograph on About).
STAIR = ('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420">'
         '<defs><filter id="b" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>'
         '<linearGradient id="g" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#cfdad8" stop-opacity="0"/>'
         '<stop offset=".5" stop-color="#cfdad8" stop-opacity=".14"/><stop offset="1" stop-color="#cfdad8" stop-opacity=".22"/></linearGradient></defs>'
         '<g filter="url(#b)"><path fill="url(#g)" d="M0 420V380H80V330H160V280H240V230H320V180H400V130H480V80H560V30H640V420Z"/>'
         '<path d="M40 330L600 -10" stroke="#f4f0e9" stroke-opacity=".10" stroke-width="7" fill="none"/></g></svg>')
(ROOT / "assets" / "glass-stair.svg").write_text(STAIR + "\n")
print("glass-stair", len(STAIR), "bytes")

# The same stair for light grounds (the portal sign-in wall): a darker figure behind daylight.
STAIR_LIGHT = STAIR.replace('stop-color="#cfdad8" stop-opacity="0"', 'stop-color="#565047" stop-opacity="0"').replace(
    'stop-color="#cfdad8" stop-opacity=".14"', 'stop-color="#565047" stop-opacity=".16"').replace(
    'stop-color="#cfdad8" stop-opacity=".22"', 'stop-color="#565047" stop-opacity=".26"').replace(
    'stroke="#f4f0e9" stroke-opacity=".10"', 'stroke="#2b2825" stroke-opacity=".16"')
(ROOT / "assets" / "glass-stair-light.svg").write_text(STAIR_LIGHT + "\n")
print("glass-stair-light", len(STAIR_LIGHT), "bytes")
