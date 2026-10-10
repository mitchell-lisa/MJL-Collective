#!/usr/bin/env python3
"""Draws MJL's glass block tile as SVG, in two palette variants.
One 200x200 tile holds four blocks. Each block has vertical flutes (the
reeded glass in the old hero photograph), a bevel that catches light on the
top left and falls into shade on the bottom right, and a soft pillow of
light that sits in a slightly different place in each block, the way real
glass block refracts. The grout between blocks is 8 units.
Only MJL palette colors are used, some at reduced opacity.
Run from the repo root: python3 tools/glass.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = dict(poured="#2b2825", ink="#1c1a17", plaster="#f4f0e9", cement="#ebe6dc", mortar="#d5cec2", ink2="#565047")

VARIANTS = {
    # on poured bands: everything stays dark so light text keeps its contrast
    "glass-dark": dict(grout=P["ink"], body=P["poured"], flute=P["ink2"], flute_op=.26, shade=P["ink"], shade_op=.45,
                       hi=P["mortar"], hi_op=.06, pillow=P["ink2"], pillow_op=.34),
    # on plaster: cement blocks, mortar grout, plaster light
    "glass-light": dict(grout=P["mortar"], body=P["cement"], flute=P["plaster"], flute_op=.8, shade=P["mortar"], shade_op=.55,
                        hi=P["plaster"], hi_op=.9, pillow=P["plaster"], pillow_op=.75),
}
PILLOWS = [(.34, .30), (.62, .36), (.40, .64), (.66, .58)]

def tile(v):
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">')
    o.append('<defs>')
    o.append(f'<linearGradient id="f" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="11.5" y2="0" spreadMethod="repeat">'
             f'<stop offset="0" stop-color="{v["body"]}"/>'
             f'<stop offset=".38" stop-color="{v["flute"]}" stop-opacity="{v["flute_op"]}"/>'
             f'<stop offset=".5" stop-color="{v["body"]}"/>'
             f'<stop offset=".9" stop-color="{v["shade"]}" stop-opacity="{v["shade_op"]}"/>'
             f'<stop offset="1" stop-color="{v["body"]}"/></linearGradient>')
    o.append(f'<linearGradient id="b" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{v["hi"]}" stop-opacity="{min(1, v["hi_op"] * 2.2):.2f}"/>'
             f'<stop offset=".48" stop-color="{v["hi"]}" stop-opacity="0"/>'
             f'<stop offset=".52" stop-color="{v["shade"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{v["shade"]}" stop-opacity="{v["shade_op"]}"/></linearGradient>')
    for i, (cx, cy) in enumerate(PILLOWS):
        o.append(f'<radialGradient id="p{i}" cx="{cx}" cy="{cy}" r=".55">'
                 f'<stop offset="0" stop-color="{v["pillow"]}" stop-opacity="{v["pillow_op"]}"/>'
                 f'<stop offset="1" stop-color="{v["pillow"]}" stop-opacity="0"/></radialGradient>')
    o.append('</defs>')
    o.append(f'<rect width="200" height="200" fill="{v["grout"]}"/>')
    for i, (x, y) in enumerate([(0, 0), (100, 0), (0, 100), (100, 100)]):
        o.append(f'<g transform="translate({x} {y})">'
                 f'<rect x="4" y="4" width="92" height="92" rx="3" fill="url(#f)"/>'
                 f'<rect x="4" y="4" width="92" height="92" rx="3" fill="url(#p{i})"/>'
                 f'<rect x="6.5" y="6.5" width="87" height="87" rx="2" fill="none" stroke="url(#b)" stroke-width="5"/>'
                 f'<path d="M8 8H92" stroke="{v["hi"]}" stroke-opacity="{v["hi_op"]}" stroke-width="1"/></g>')
    o.append('</svg>')
    return "".join(o)

for name, v in VARIANTS.items():
    (ROOT / "assets" / f"{name}.svg").write_text(tile(v) + "\n")
    print(name, len(tile(v)), "bytes")
