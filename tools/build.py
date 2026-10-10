#!/usr/bin/env python3
"""Builds every page from one template so the bar, the footer and the head
stay identical. Run from the repo root: python3 tools/build.py
Privacy and Terms bodies live in tools/content/ and are inserted verbatim."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "tools" / "content"
SITE = "https://mjlcollective.com"
V = "20261010m1"  # bump when site.css or site.js changes

NAV = [("/work", "Work"), ("/partners", "Partners"), ("/services", "Services"), ("/about", "About"), ("/contact", "Contact")]

# Clients, newest first (order from commit fea8c67, with ABC Styling added on top).
CLIENTS = [
  ("ABC Styling", "https://annie-culbertson-concept.vercel.app", "/assets/logos/abc-styling.svg", 1003, 166, "wide"),
  ("Arden Collective", "https://arden-collective.vercel.app", "/assets/logos/arden-seal-small.svg", 827, 985, "stack"),
  ("Loftus Construction", "https://loftus-construction.vercel.app", "/assets/logos/loftus.webp?v=20261009", 1191, 277, "wide"),
  ("Lewiston Design &amp; Build", "https://lewistondesignbuild.com", "/assets/logos/lewiston.webp", 508, 508, "stack"),
  ("Simo&rsquo;s Barbering", "https://www.simosbarbering.com", "/assets/logos/simos.webp?v=20261002", 1022, 556, "wide"),
  ("George Gravenstine Insurance Agency", "https://georgeinsurance.agency", "/assets/logos/george.webp", 781, 391, "wide"),
  ("Tiger Digital", "https://www.tigerdigital.marketing", "/assets/logos/tiger.webp", 560, 560, "stack"),
  ("BlueThreadz", "https://www.bluethreadz.com", "/assets/logos/bluethreadz.webp", 1000, 132, "wide"),
  ("Dorothy&rsquo;s Flower Shop", "https://www.dorothysflower.shop", "/assets/logos/dorothy.webp", 700, 1337, "stack"),
]

def host(url):
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")

def head(path, title, desc, extra=""):
    url = SITE + path
    ld = ""
    if path == "/":
        ld = '<script type="application/ld+json">' + json.dumps({
          "@context": "https://schema.org", "@type": "ProfessionalService", "name": "MJL Collective LLC",
          "alternateName": "MJL Collective", "url": SITE, "email": "mitchell@mjlcollective.com", "image": SITE + "/assets/og.png",
          "description": desc, "founder": {"@type": "Person", "name": "Mitchell Lisa"},
          "knowsAbout": ["web design", "brand identity", "logo design", "website maintenance", "email and SMS marketing"]}) + "</script>\n  "
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#f4f0e9">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MJL Collective">
  <meta property="og:image" content="{SITE}/assets/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="The MJL Collective mark">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/assets/monogram-small.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">

  {ld}<link rel="preload" href="/assets/fonts/InstrumentSerif-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/InstrumentSans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/SourceSerif4-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/site.css?v={V}">{extra}
</head>'''

def navlinks(cur, cls=""):
    out = []
    for href, label in NAV:
        a = ' aria-current="page"' if href == cur else ""
        out.append(f'<li><a href="{href}"{a}>{label}</a></li>')
    return out

def bar(cur):
    items = "\n          ".join(navlinks(cur))
    drawer = "\n        ".join(navlinks(cur))
    return f'''<body>
  <a class="skip" href="#main">Skip to the content</a>
  <header class="bar" id="top">
    <div class="bar-glass" aria-hidden="true"><i class="g"></i><i class="f"></i></div>
    <div class="wrap">
      <a class="home" href="/" aria-label="MJL Collective, home"><img src="/assets/lockup-ink.svg" alt="MJL Collective" width="552" height="143"></a>
      <nav class="nav" aria-label="Main">
        <ul>
          {items}
          <li class="sep"><a href="/clients">Client login</a></li>
        </ul>
      </nav>
      <div class="tools">
        <a class="login" href="/clients">Client login</a>
        <button class="menu-btn" type="button" aria-expanded="false" aria-controls="drawer">Menu</button>
      </div>
    </div>
  </header>
  <nav class="drawer" id="drawer" aria-label="Menu">
    <ul>
      {drawer}
      <li><a href="/clients">Client login</a></li>
    </ul>
    <p class="mail">Or email me at <a href="mailto:mitchell@mjlcollective.com">mitchell@mjlcollective.com</a></p>
  </nav>
'''

def foot(cur, ask=True):
    items = "\n          ".join(navlinks(cur))
    askblock = '''<div class="ask">
        <h2>Tell me about the business.</h2>
        <div>
          <p>I&rsquo;ll tell you what it needs and what it costs.</p>
          <a class="btn" href="/contact">Write to me</a>
          <a class="mail" href="mailto:mitchell@mjlcollective.com">mitchell@mjlcollective.com</a>
        </div>
      </div>''' if ask else ""
    return f'''
  <footer class="foot{"" if ask else " slim"}">
    <div class="wrap">
      {askblock}
      <a class="sign" href="/" aria-label="MJL Collective, home"><img src="/assets/lockup-ink.svg" alt="MJL Collective" width="552" height="143" loading="lazy"></a>
      <div class="rows">
        <ul>
          {items}
          <li><a href="/clients">Client login</a></li>
        </ul>
        <div class="legal">
          <span>MJL Collective LLC</span>
          <span><a href="/privacy"{' aria-current="page"' if cur=="/privacy" else ""}>Privacy</a></span>
          <span><a href="/terms"{' aria-current="page"' if cur=="/terms" else ""}>Terms</a></span>
        </div>
      </div>
    </div>
  </footer>

  <script src="/assets/site.js?v={V}"></script>
</body>
</html>
'''

def img(src, alt, w, h, eager=False):
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{src}" alt="{alt}" width="{w}" height="{h}" {lz}>'

# Client captures: desktop 1440x900 at 2x, phone 390x844 at 3x (tools/export_shots.py),
# served as AVIF with a WebP fallback, at three widths each.
SHOT_W = {"d": (1200, 1800, 2880), "p": (360, 720, 1080)}
SIZES = {"lead": "(min-width: 900px) min(62vw, 940px), 88vw", "look": "(min-width: 900px) min(78vw, 1120px), 100vw",
         "half": "(min-width: 900px) min(56vw, 800px), 100vw", "phone": "(min-width: 900px) 220px, 52vw",
         "lead-phone": "(min-width: 900px) 170px, 26vw"}

def pic(shot, alt, sizes, eager=False):
    kind = shot.rsplit("-", 1)[1]
    ws = SHOT_W[kind]
    w, h = (1440, 900) if kind == "d" else (390, 844)
    src = lambda ext: ", ".join(f"/assets/shots/{shot}-{x}.{ext} {x}w" for x in ws)
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{src("avif")}" sizes="{sizes}">'
            f'<img src="/assets/shots/{shot}-{ws[1]}.webp" srcset="{src("webp")}" sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {lz}></picture>')

def plate(url, shot, alt, sizes="look", eager=False, focus=True):
    kind = "d" if shot.endswith("-d") else "p"
    t = ' tabindex="-1"' if kind == "p" else ""
    f = " focus" if focus else ""
    return f'<a class="plate {kind}{f}" href="{url}" target="_blank" rel="noopener"{t}>{pic(shot, alt, SIZES[sizes], eager)}</a>'

# The glass block: Mitchell's photograph of a real glass block wall, squared up
# so the blocks sit on a true grid (tools/glass-grid.json). Three crops: the
# wall (16:10) for the home entrance, the band for page heads, the tall crop
# for phones. Each has a frosted twin, diffused ahead of time.
GRID = json.loads((ROOT / "tools" / "glass-grid.json").read_text())
GW = {"wall": (960, 1440, 1920, 2880), "band": (960, 1440, 1920, 2880), "tall": (780, 1170, 1560)}

def gsrc(crop, ext):
    return ", ".join(f"/assets/glass/glass-{crop}-{w}.{ext} {w}w" for w in GW[crop])

def glass_pic(wide="band", eager=False, cls="gp"):
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    g = GRID[wide]
    return (f'<picture class="{cls}">'
            f'<source media="(max-width: 700px)" type="image/avif" srcset="{gsrc("tall", "avif")}" sizes="100vw">'
            f'<source media="(max-width: 700px)" type="image/webp" srcset="{gsrc("tall", "webp")}" sizes="100vw">'
            f'<source type="image/avif" srcset="{gsrc(wide, "avif")}" sizes="100vw">'
            f'<img src="/assets/glass/glass-{wide}-1920.webp" srcset="{gsrc(wide, "webp")}" sizes="100vw" alt="" width="{g["w"]}" height="{g["h"]}" {lz}></picture>')

def glass_head(inner, cls=""):
    return f'''    <section class="glass-head{(" " + cls) if cls else ""}" data-glass="band">
      {glass_pic("band", eager=True)}
      <div class="frost" aria-hidden="true"></div>
      <div class="wrap">
        <div class="pane">
          {inner}
        </div>
      </div>
    </section>'''

def mortar_svg(crop):
    """The mortar between the blocks, drawn on the photograph's own grid, with a
    thin bevel of light on each block. A few kilobytes, sharp at any size."""
    g = GRID[crop]; W, H = g["w"], g["h"]
    xs = [x * W / 100 for x in g["xs"]]; ys = [y * H / 100 for y in g["ys"]]
    m = 24  # half the joint, in photo pixels (the pitch is about 431)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">',
           '<g fill="#f3efe8">']
    for x in xs[1:-1]: out.append(f'<rect x="{x - m:.0f}" y="0" width="{2 * m}" height="{H}"/>')
    for y in ys[1:-1]: out.append(f'<rect x="0" y="{y - m:.0f}" width="{W}" height="{2 * m}"/>')
    out.append('</g><g fill="none" stroke-width="7">')
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x0, x1, y0, y1 = xs[i] + m, xs[i + 1] - m, ys[j] + m, ys[j + 1] - m
            if x1 - x0 < 60 or y1 - y0 < 60: continue
            out.append(f'<path d="M{x0 + 8:.0f} {y1 - 8:.0f}V{y0 + 8:.0f}H{x1 - 8:.0f}" stroke="#fff" stroke-opacity=".7"/>'
                       f'<path d="M{x1 - 8:.0f} {y0 + 8:.0f}V{y1 - 8:.0f}H{x0 + 8:.0f}" stroke="#1c1a17" stroke-opacity=".12"/>')
    out.append('</g></svg>')
    (ROOT / "assets" / "glass" / f"mortar-{crop}.svg").write_text("".join(out))

def wall(crop, eager):
    g = GRID[crop]
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    sizes = "max(100vw, 160svh)" if crop == "wall" else "max(100vw, 46svh)"
    # each crop only ever downloads at the screen sizes that show it
    skip = "(max-width: 700px)" if crop == "wall" else "(min-width: 701px)"
    return f'''<div class="wall wall-{crop}" style="--a:{g["w"] / g["h"]:.4f}" aria-hidden="true">
          <picture class="clear"><source media="{skip}" srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><source type="image/avif" srcset="{gsrc(crop, "avif")}" sizes="{sizes}"><img src="/assets/glass/glass-{crop}-{GW[crop][1]}.webp" srcset="{gsrc(crop, "webp")}" sizes="{sizes}" alt="" width="{g["w"]}" height="{g["h"]}" {lz}></picture>
          <div class="frosted"></div>
        </div>'''

for _c in ("wall", "tall", "band"): mortar_svg(_c)

# Before and after: only where MJL really replaced something, and only with a
# real before (the old file from the repo history, or the Wayback Machine).
def ba(name, before, after, bcap, acap, kind="site"):
    st = ""
    return f'''<figure class="ba ba-{kind}">
            <div class="ba-frame" style="--x:50%{st}">
              <div class="ba-after">{after}</div>
              <div class="ba-before">{before}</div>
              <span class="ba-tag b" aria-hidden="true">Before</span><span class="ba-tag a" aria-hidden="true">After</span>
              <div class="ba-line" aria-hidden="true"><span></span></div>
              <input class="ba-range" type="range" min="0" max="100" value="50" step="1" aria-label="{name}: before and after. Left shows before, right shows after.">
            </div>
            <figcaption><span>Before: {bcap}</span><span>After: {acap}</span></figcaption>
          </figure>'''

def shotpic(shot, alt, sizes, folder="shots"):
    kind = shot.rsplit("-", 1)[1]; ws = SHOT_W[kind]
    w, h = (1440, 900) if kind == "d" else (390, 844)
    src = lambda ext: ", ".join(f"/assets/{folder}/{shot}-{x}.{ext} {x}w" for x in ws)
    return (f'<picture><source type="image/avif" srcset="{src("avif")}" sizes="{sizes}">'
            f'<img src="/assets/{folder}/{shot}-{ws[1]}.webp" srcset="{src("webp")}" sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></picture>')

def mark(src, alt, w, h, cls=""):
    return f'<img class="mk{(" " + cls) if cls else ""}" src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

ROOM_SIZES = "(min-width: 901px) min(60vw, 1000px), 100vw"
def room(name, url, line, d, dalt, p=None, palt="", art=None, side="", tag="h2", flip=False, link=None, rid=""):
    art = art or (plate(url, d, dalt, "look", focus=False).replace(SIZES["look"], ROOM_SIZES)
                  + (plate(url, p, palt, "phone", focus=False) if p else ""))
    link = link or f"Visit {host(url)}"
    idattr = f' id="{rid}"' if rid else ""
    return f'''<article class="room{" flip" if flip else ""}"{idattr}>
        <div class="room-in">
          <div class="room-art{" has-p" if p else ""}">{art}</div>
          <div class="room-words">
            <{tag}>{name}</{tag}>
            <p>{line}</p>
            {side}
            <a class="link" href="{url}" target="_blank" rel="noopener">{link}</a>
          </div>
        </div>
      </article>'''

def carousel():
    def li(c, hidden):
        name, url, src, w, h, kind = c
        t = ' tabindex="-1"' if hidden else ""
        return f'<li><a href="{url}" target="_blank" rel="noopener"{t}><img class="mark-{kind}" src="{src}" width="{w}" height="{h}" alt="{"" if hidden else name}" loading="lazy"></a></li>'
    a = "\n              ".join(li(c, False) for c in CLIENTS)
    b = "\n              ".join(li(c, True) for c in CLIENTS)
    return f'''<section class="clients" aria-labelledby="clients-h">
      <div class="wrap">
        <div class="clients-head">
          <h2 id="clients-h">The businesses I work with.</h2>
          <a class="link" href="/partners">Every logo, with a link to the site</a>
        </div>
        <div class="trusted-row">
          <div class="trusted-view">
            <div class="trusted-track">
              <ul>
              {a}
              </ul>
              <ul aria-hidden="true">
              {b}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>'''

def page(name, path, title, desc, body, ask=True, extra=""):
    html = head(path, title, desc, extra) + "\n" + bar(path) + '\n  <main id="main">\n' + body + "\n  </main>\n" + foot(path, ask)
    (ROOT / name).write_text(html)

# ------------------------------------------------------------------ home
L = "https://lewistondesignbuild.com"
# Behind the glass: the top of the site for Annie Culbertson's styling
# studio. She is the newest client: first in the logos and on Partners.
ANNIE = "https://annie-culbertson-concept.vercel.app"
print_ = (f'<picture><source media="(max-width: 700px)" type="image/avif" srcset="/assets/shots/annie-top-p-360.avif 360w, /assets/shots/annie-top-p-720.avif 720w, /assets/shots/annie-top-p-1080.avif 1080w" sizes="70vw">'
          f'<source media="(max-width: 700px)" type="image/webp" srcset="/assets/shots/annie-top-p-360.webp 360w, /assets/shots/annie-top-p-720.webp 720w, /assets/shots/annie-top-p-1080.webp 1080w" sizes="70vw">'
          f'<source type="image/avif" srcset="/assets/shots/annie-top-d-1200.avif 1200w, /assets/shots/annie-top-d-1800.avif 1800w, /assets/shots/annie-top-d-2880.avif 2880w" sizes="(min-width: 701px) min(64vw, 1180px), 70vw">'
          f'<img src="/assets/shots/annie-top-d-1800.webp" srcset="/assets/shots/annie-top-d-1200.webp 1200w, /assets/shots/annie-top-d-1800.webp 1800w, /assets/shots/annie-top-d-2880.webp 2880w" sizes="(min-width: 701px) min(64vw, 1180px), 70vw" '
          f'alt="The top of the ABC Styling site: Annie in a black cape beside the ABC Styling wordmark on oxblood, under the site&rsquo;s menu" width="1440" height="900" loading="lazy" decoding="async" fetchpriority="low"></picture>')
home = f'''    <section class="enter" aria-labelledby="hello">
      <div class="enter-stage">
        <div class="wall-box">
        {wall("wall", True)}
        {wall("tall", True)}
        </div>
        <div class="wrap enter-words">
          <div class="pane">
            <h1 id="hello">Websites and brands for local businesses.</h1>
            <p class="lede">I build them, then I keep them current.</p>
            <div class="actions">
              <a class="btn" href="/contact">Tell me about your business</a>
              <a class="link" href="/work">See the work</a>
            </div>
          </div>
        </div>
        <figure class="print">
          <a class="print-frame" href="{ANNIE}" target="_blank" rel="noopener">{print_}</a>
          <figcaption><strong>ABC Styling.</strong> A site for Annie Culbertson, a stylist in New York. <a href="{ANNIE}" target="_blank" rel="noopener">See the site</a></figcaption>
        </figure>
      </div>
    </section>

    {carousel()}

    <section class="rooms" aria-label="The newest sites">
      {room("Arden Collective", "https://arden-collective.vercel.app", "I drew the oval seal, then built the site from it.", "arden-home-d", "The Arden Collective home page, with the oval seal: Boutique talent management for social media creators", "arden-contact-p", "The Arden Collective contact page on a phone, with the pink seal", tag="h2", link="See the preview")}
      {room("Loftus Construction", "https://loftus-construction.vercel.app", "Bridges since 1994, laid out for the engineers who hire them.", "loftus-home-d", "The Loftus home page: a steam train on a bridge under Design-build, preconstruction, construction", "loftus-build-p", "What Loftus builds on a phone: a stone-faced bridge with a black steel railing, and the kinds of bridges they build", tag="h2", flip=True, link="See the preview")}
    </section>
    <div class="more-work wrap"><a class="link" href="/work">See all the work</a></div>
    <section class="portal-feature" aria-labelledby="portal-h">
      <div class="wrap portal-in">
        <div class="room-words">
          <h2 id="portal-h">Your own client portal.</h2>
          <p>Every client gets a login. You send me an edit there in a sentence or two, and my reply shows up in the same thread.</p>
          <p>It can email you or text you when I answer, so you don&rsquo;t have to keep checking.</p>
          <a class="link" href="/clients">Client login</a>
        </div>
        <div class="room-art has-p">{plate("/clients", "portal-thread-d", "An edit thread in the client portal: a request to change Saturday hours, and my reply that it&rsquo;s done", "look", focus=False).replace(SIZES["look"], ROOM_SIZES).replace(' target="_blank" rel="noopener"', '')}{plate("/clients", "portal-alerts-p", "Alert settings in the client portal on a phone: email me and text me when MJL replies", "phone", focus=False).replace(' target="_blank" rel="noopener"', '')}</div>
      </div>
    </section>

    </section>'''
page("index.html", "/", "MJL Collective | Websites and brands for local businesses",
     "Mitchell Lisa builds websites and brands for local businesses, then keeps them current.", home)

# ------------------------------------------------------------------ work
loftus_ba = ba("Loftus Construction",
    shotpic("loftus-old-d", "The Loftus Construction website before: a dark header with the wordmark, a train photo in a slider, and three columns of text", ROOM_SIZES),
    shotpic("loftus-home-d", "The new Loftus Construction website: the same train, full width, under Design-build, preconstruction, construction", ROOM_SIZES),
    'loftusconstruction.com, from the <a href="https://web.archive.org/web/20260513061451/http://loftusconstruction.com/" target="_blank" rel="noopener">Wayback Machine, May 2026</a>', "the preview I built")
tiger_ba = ba("Tiger Digital mark",
    mark("/assets/brand-work/tiger-before.webp", "The old Tiger Digital mark", 126, 174),
    mark("/assets/brand-work/tiger-seal.webp", "The Tiger Digital seal I drew", 160, 160),
    "the old mark", "the seal I drew", "mark")
blue_ba = ba("BlueThreadz logo",
    mark("/assets/brand-work/bluethreadz-before.webp", "The old BlueThreadz logo", 760, 250),
    mark("/assets/brand-work/bluethreadz-wordmark.webp", "The BlueThreadz wordmark I redrew", 600, 80),
    "the old logo", "the one I redrew", "mark wide")
work = glass_head('''<h1>The work.</h1>
          <p class="lede">Every site opens live. Try them on your phone too.</p>''') + f'''
    <section class="rooms" aria-label="Client sites, newest first">
      {room("Arden Collective", "https://arden-collective.vercel.app", "An oval seal I drew, and a site built from its type and color.", "arden-contact-d", "The Arden Collective contact page, with the email address inside the pink oval seal", "arden-top-p", "The Arden Collective home page on a phone", side='<div class="marks">' + mark("/assets/brand-work/arden-seal.svg", "The Arden Collective oval seal", 120, 145, "tall") + mark("/assets/brand-work/arden-icon.svg", "The Arden favicon: the seal on an oak green tile", 64, 64, "icon") + '</div>', link="See the preview", rid="arden")}
      {room("Loftus Construction", "https://loftus-construction.vercel.app", "The site they have now, and the one I built for the engineers who hire them.", None, "", art=loftus_ba, flip=True, link="See the preview")}
      {room("Lewiston Design &amp; Build", L, "Every house has its plans, and buyers try the finishes before they call.", "lewiston-projects-d", "The Lewiston projects page: three houses, each with its plans", "lewiston-top-p", "The Lewiston home page on a phone: Custom homes in Middle Tennessee", side='<div class="marks">' + mark("/assets/brand-work/lewiston-badge.webp", "The Lewiston lion badge, which I cut down into the favicon", 160, 160, "tall") + mark("/assets/brand-work/lewiston-fav-32.png", "The Lewiston favicon at 32 pixels", 32, 32, "px") + '</div>')}
      {room("Simo&rsquo;s Barbering", "https://www.simosbarbering.com", "The shop&rsquo;s first website, live a week after I met John.", "simos-top-d", "The top of the Simo&rsquo;s site: the price board under the Simo&rsquo;s wordmark", "simos-door-p", "Further down the Simo&rsquo;s site on a phone: His name on the door, with John at work", flip=True, side='<div class="marks">' + mark("/assets/brand-work/simos-wordmark.webp", "The Simo&rsquo;s Barbering wordmark, cut out clean for the header", 600, 334, "wide") + '</div>')}
      {room("George Gravenstine Agency", "https://georgeinsurance.agency", "Auto and home quotes right on the site, in three to five minutes.", "george-home-d", "The George Gravenstine home page: Independent auto, home and business insurance", "george-auto-p", "The George Gravenstine auto insurance page on a phone")}
      {room("Tiger Digital", "https://www.tigerdigital.marketing", "Joe&rsquo;s agency got a new seal and a new site in two days.", "tiger-home-d", "The Tiger Digital home page: Real growth. No fluff. Under the new seal", "tiger-team-p", "The Tiger Digital team page on a phone, with Joe", flip=True, side=tiger_ba, rid="tiger")}
      {room("BlueThreadz", "https://www.bluethreadz.com", "I redrew the logo and rebuilt the catalog so every garment leads to a quote.", "bluethreadz-home-d", "The BlueThreadz home page: Build your brand in style", "bluethreadz-quote-p", "The BlueThreadz quote form on a phone: Tell us about your order", side=blue_ba)}
      {room("Dorothy&rsquo;s Flower Shop", "https://www.dorothysflower.shop", "The old shop sign became the mark, then a line of hats.", "dorothy-home-d", "The Dorothy&rsquo;s Flower Shop home page, a full screen of lilacs", "dorothy-shop-p", "The Dorothy&rsquo;s hat shop on a phone", flip=True, side='<div class="marks">' + mark("/assets/brand-work/dorothy-sign.webp", "The Dorothy&rsquo;s Flower Shop mark, taken from the old shop sign", 160, 160, "tall") + '</div>')}
    </section>'''
page("work.html", "/work", "Work | MJL Collective",
     "Client sites by MJL Collective, newest first: Arden Collective, Loftus Construction, Lewiston Design & Build, Simo's Barbering, George Gravenstine Agency, Tiger Digital, BlueThreadz and Dorothy's Flower Shop.", work)

# ------------------------------------------------------------------ partners
tiles = "\n          ".join(
    f'<li><a href="{u}" target="_blank" rel="noopener"><img class="mark-{k}" src="{s}" width="{w}" height="{h}" alt="{n}" loading="lazy"><span class="nm" aria-hidden="true">{n.replace(" Insurance Agency", "")}</span></a></li>'
    for n, u, s, w, h, k in CLIENTS)
partners = glass_head('''<h1>Partners.</h1>
          <p class="lede">Newest first. Each logo opens the site.</p>''') + f'''
    <section class="partners">
      <div class="wrap">
        <ul class="logo-grid">
          {tiles}
        </ul>
      </div>
    </section>'''
page("partners.html", "/partners", "Partners | MJL Collective", "The businesses MJL Collective works with, newest first. Each logo links to the live site.", partners)

# ------------------------------------------------------------------ services
def fig(url, shot, alt, name, cap):
    return f'<figure>{plate(url, shot, alt, "half")}<figcaption><strong>{name}.</strong> {cap}</figcaption></figure>'

services = glass_head('''<h1>The site is where it starts.</h1>
          <p class="lede">Then I keep it current.</p>''') + f'''
    <div class="wrap">
      <section class="service" aria-labelledby="s1">
        <div class="words">
          <h2 id="s1">Website and brand</h2>
          <p>The mark, the site, and a clear next step for the customer. Live in days.</p>
          <a class="link" href="/work#tiger">The Tiger Digital before and after</a>
        </div>
        <div class="shot">{fig("https://www.tigerdigital.marketing", "tiger-services-d", "The Tiger Digital services page: Smarter coverage. Better spend. Real local results.", "Tiger Digital", "A new seal and a new site in two days.")}</div>
      </section>
      <section class="service flip" aria-labelledby="s2">
        <div class="words">
          <h2 id="s2">Keep it current</h2>
          <p>Text a change and it ships. Hosting, fixes, and catalog, listing or team updates, without the owner chasing anyone.</p>
          <p>Clients send requests through the client portal and get my reply there, with a text when I answer if they want one.</p>
        </div>
        <div class="shot">{fig("https://georgeinsurance.agency/team", "george-team-d", "The George Gravenstine team page", "George Gravenstine Agency", "The team page. When someone joins the office, they show up here.")}</div>
      </section>
      <section class="service" aria-labelledby="s3">
        <div class="words">
          <h2 id="s3">Show up where it matters</h2>
          <p>Company LinkedIn or other channels. Listings, catalogs and simple presence systems. Light automation so what is true offline stays true online.</p>
        </div>
        <div class="shot">{fig("https://www.bluethreadz.com/products", "bluethreadz-catalog-d", "The BlueThreadz catalog: Pick the garment. We&rsquo;ll put your name on it.", "BlueThreadz", "The catalog. Every brand and garment they carry, each one a step away from a quote.")}</div>
      </section>
      <section class="service text-only" aria-labelledby="s4">
        <div class="words">
          <h2 id="s4">Bring people back</h2>
        </div>
        <div class="more">
          <p>Email and SMS once the base is solid. When search needs a specialist, I bring in search specialists I trust.</p>
          <a class="link" href="/contact">Ask me what your business needs</a>
        </div>
      </section>
    </div>'''
page("services.html", "/services", "Services | MJL Collective",
     "The website and brand first, then keeping it current: hosting, fixes, listings, catalogs, and email and SMS once the base is solid.", services)

# ------------------------------------------------------------------ about
about = glass_head('''<h1>Mitchell Lisa</h1>
          <p class="lede">One person, not an agency. When you reach out, you&rsquo;re talking to me.</p>''') + '''
    <section class="founder-body">
      <div class="wrap founder">
        <div class="portrait"><img src="/assets/mitchell.webp" alt="Mitchell Lisa in an MJL Collective cap" width="1122" height="1402" loading="lazy" decoding="async"></div>
        <div class="text">
          <p>I build every site myself, and usually the brand it sits on too: the logo, the type and the colors.</p>
          <p>Once it&rsquo;s live, I keep it current. When your hours change, a price goes up or you add a service, you send me a note and I make the change.</p>
          <p>There&rsquo;s nobody in the middle. You email or text me, and I&rsquo;m the one who answers and the one who does the work.</p>
          <p>My clients include an insurance agency, a barbershop and a homebuilder. Most of them came to me with a site that was out of date, or no site at all.</p>
          <div class="actions">
            <a class="btn" href="/contact">Tell me about your business</a>
            <a class="link" href="/work">See the work</a>
          </div>
        </div>
      </div>
    </section>'''
page("about.html", "/about", "About Mitchell Lisa | MJL Collective",
     "Mitchell Lisa runs MJL Collective, a one-person studio that builds websites and brands for local businesses and keeps them current.", about)

# ------------------------------------------------------------------ contact
contact = glass_head('''<h1>Tell me about the business.</h1>
          <p class="lede">Say what it does and where it&rsquo;s stuck. I&rsquo;ll tell you what it needs and what it costs.</p>''') + '''
    <section class="meet on-light">
      <div class="wrap grid">
        <form class="cf" id="cf" novalidate>
          <input type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
          <div class="cf-grid">
            <label><span>Name</span><input name="name" required maxlength="200" autocomplete="name"></label>
            <label><span>Business</span><input name="business" maxlength="200" autocomplete="organization"></label>
            <label><span>Email</span><input name="email" type="email" required maxlength="200" autocomplete="email"></label>
            <label><span>Phone <em>(optional)</em></span><input name="phone" type="tel" maxlength="60" autocomplete="tel"></label>
            <label class="full"><span>What do you need help with?</span><textarea name="message" required rows="6" maxlength="4000" placeholder="New site, a rebuild, updates, or email and SMS. Tell me a little about the business."></textarea></label>
          </div>
          <div class="cf-foot">
            <button class="btn" type="submit">Send message</button>
            <p class="cf-note" hidden>Something went wrong. <a href="mailto:mitchell@mjlcollective.com?subject=MJL%20Collective%20meeting%20request">Email me directly instead</a>.</p>
          </div>
          <div class="cf-sent" hidden>
            <p class="big">Got it.</p>
            <p>Your message is in my inbox. I will be in touch soon.</p>
          </div>
        </form>
        <aside>
          <div class="block">
            <h2>Email</h2>
            <p>Your message goes to my inbox, and you&rsquo;ll hear back from me, not a team. You can also write to me directly.</p>
            <a class="link" href="mailto:mitchell@mjlcollective.com">mitchell@mjlcollective.com</a>
          </div>
          <div class="block">
            <h2>Already a client?</h2>
            <p>Send changes and questions through the client portal.</p>
            <a class="link" href="/clients">Client login</a>
          </div>
        </aside>
      </div>
    </section>'''
page("contact.html", "/contact", "Contact | MJL Collective",
     "Tell Mitchell about the business. He will say what it needs and what it costs, before anyone signs anything.", contact, ask=False)

# ------------------------------------------------------------------ privacy and terms
for slug, title, desc in [
    ("privacy", "Privacy Policy | MJL Collective", "How MJL Collective LLC collects, uses, stores, shares, and deletes information, including Plaid financial connections for internal bookkeeping."),
    ("terms", "Terms | MJL Collective", "Text message terms for MJL Collective client portal alerts: program, frequency, cost, STOP and HELP, carriers and privacy.")]:
    hd = (C / f"{slug}.head.html").read_text().strip()
    doc = (C / f"{slug}.doc.html").read_text()
    body = f'''    <section class="legal-head">
      <div class="wrap">
        {hd}
      </div>
    </section>
    <article class="policy">
      <div class="wrap">
        <div class="doc">
{doc}        </div>
      </div>
    </article>'''
    page(f"{slug}.html", "/" + slug, title, desc, body)

# ------------------------------------------------------------------ 404
lost = glass_head('''<h1>That page isn&rsquo;t here.</h1>
          <p class="lede">It may have moved. The work is a good place to start.</p>
          <div class="actions">
            <a class="btn" href="/work">See the work</a>
            <a class="link" href="/">Home</a>
          </div>''', "lost")
page("404.html", "/404", "Page not found | MJL Collective", "This page could not be found.", lost)
print("built")
