#!/usr/bin/env python3
"""The MJL monogram in a glass block. The letters are the strokes from the
lockup (assets/lockup-ink.svg), untouched: only placed and scaled.
Writes assets/monogram.svg (the full block) and assets/monogram-small.svg
(the same block, simplified so it stays crisp at 16 and 32 pixels)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
# the lockup's own letter strokes, viewBox units
MJ = 'M7,110 V10 L54,80 L101,10 V118 A28,28 0 0 1 73,146 H54'
L_ = 'M131,10 V103 H191'
# letters span x 0..198, y 3..153 (with the 14 stroke); center them in a 512 block
S = 1.36
LW, LH = 198 * S, 150 * S
TX, TY = (512 - LW) / 2, (512 - LH) / 2 - 3 * S + 4
letters = (f'<g transform="translate({TX:.1f} {TY:.1f}) scale({S})" fill="none" stroke="#1c1a17" stroke-width="14" stroke-linejoin="miter" stroke-miterlimit="6">'
           f'<path d="{MJ}"/><path d="{L_}"/></g>')
full = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="MJL Collective">
<defs>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fdfcfa"/><stop offset=".5" stop-color="#ebe6dc"/><stop offset="1" stop-color="#d5cec2"/></linearGradient>
<linearGradient id="face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3ddd2"/><stop offset=".45" stop-color="#f4f0e9"/><stop offset="1" stop-color="#fbf9f5"/></linearGradient>
<linearGradient id="bevel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b9b0a2"/><stop offset=".5" stop-color="#d5cec2" stop-opacity=".4"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="spec" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="in"><rect x="70" y="70" width="372" height="372" rx="26"/></clipPath>
</defs>
<rect x="12" y="12" width="488" height="488" rx="46" fill="url(#rim)"/>
<rect x="13.5" y="13.5" width="485" height="485" rx="44.5" fill="none" stroke="#d5cec2" stroke-width="3"/>
<rect x="70" y="70" width="372" height="372" rx="26" fill="url(#face)"/>
<g clip-path="url(#in)" fill="none" stroke="#fff" stroke-linecap="round">
<path d="M40 150 C 110 120, 170 190, 250 150 S 400 120, 480 160" stroke-width="10" stroke-opacity=".55"/>
<path d="M40 300 C 120 270, 190 340, 270 300 S 410 270, 480 310" stroke-width="8" stroke-opacity=".4"/>
<path d="M40 400 C 120 380, 200 430, 280 395 S 420 380, 480 410" stroke-width="6" stroke-opacity=".35"/>
</g>
{letters}
<rect x="70" y="70" width="372" height="372" rx="26" fill="none" stroke="url(#bevel)" stroke-width="6"/>
<path d="M60 40 H 300" stroke="url(#spec)" stroke-width="5" stroke-linecap="round"/>
<path d="M40 64 V 260" stroke="url(#spec)" stroke-width="4" stroke-linecap="round"/>
</svg>
'''
small = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs><linearGradient id="face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9e3d8"/><stop offset="1" stop-color="#fbf9f5"/></linearGradient></defs>
<rect x="6" y="6" width="500" height="500" rx="64" fill="url(#face)" stroke="#b9b0a2" stroke-width="12"/>
<rect x="34" y="34" width="444" height="444" rx="40" fill="none" stroke="#fff" stroke-width="10"/>
{letters.replace('stroke-width="14"', 'stroke-width="21"').replace(f'scale({S})', 'scale(1.88)').replace(f'translate({TX:.1f} {TY:.1f})', f'translate({(512-198*1.88)/2:.1f} {(512-150*1.88)/2 - 4:.1f})')}
</svg>
'''
(ROOT / "assets" / "monogram.svg").write_text(full)
(ROOT / "assets" / "monogram-small.svg").write_text(small)
print("monogram written")
