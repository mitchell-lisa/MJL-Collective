# Bake the mortar grid into the frost so the home crossfade is one plain bitmap layer.
# usage: python3 tools/bake_frost.py (after build.py has written mortar-*.svg)
from playwright.sync_api import sync_playwright
from PIL import Image
import pathlib
G=pathlib.Path(__file__).resolve().parent.parent/'assets'/'glass'
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,w,h in [('wall',2880,1800),('tall',1170,2532)]:
    pg=b.new_page(viewport={'width':w,'height':h})
    html=f"<html><body style='margin:0'><div style='width:{w}px;height:{h}px;background:url(file://{G}/mortar-{n}.svg) 0 0/100% 100% no-repeat, url(file://{G}/frost-{n}.webp) 0 0/100% 100% no-repeat'></div></body></html>"
    pathlib.Path('/tmp/bake.html').write_text(html); pg.goto('file:///tmp/bake.html'); pg.wait_for_timeout(500)
    pg.screenshot(path=f'/tmp/bake-{n}.png')
    Image.open(f'/tmp/bake-{n}.png').convert('RGB').save(G/f'frost-{n}-m.webp', quality=80, method=6)
  b.close()
