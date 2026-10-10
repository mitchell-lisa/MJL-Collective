#!/usr/bin/env python3
"""Builds every page from one template so the bar, the footer and the head
stay identical. Run from the repo root: python3 tools/build.py
Privacy and Terms bodies live in tools/content/ and are inserted verbatim."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "tools" / "content"
SITE = "https://mjlcollective.com"
V = "20261009r5"  # bump when site.css or site.js changes

NAV = [("/work", "Work"), ("/partners", "Partners"), ("/services", "Services"), ("/about", "About"), ("/contact", "Contact")]

# Clients, newest first (order from commit fea8c67).
CLIENTS = [
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
          "address": {"@type": "PostalAddress", "addressLocality": "Moorestown", "addressRegion": "NJ", "addressCountry": "US"},
          "knowsAbout": ["web design", "brand identity", "logo design", "website maintenance", "email and SMS marketing"]}) + "</script>\n  "
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#2b2825">
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
  <link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  {ld}<link rel="preload" href="/assets/fonts/InstrumentSans-latin.woff2" as="font" type="font/woff2" crossorigin>
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
    <div class="wrap">
      <a class="home" href="/" aria-label="MJL Collective, home"><img src="/assets/lockup-plaster.svg" alt="MJL Collective" width="552" height="143"></a>
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
    <nav class="drawer" id="drawer" aria-label="Menu">
      <ul>
        {drawer}
        <li><a href="/clients">Client login</a></li>
      </ul>
      <p class="mail">Or email me at <a href="mailto:mitchell@mjlcollective.com">mitchell@mjlcollective.com</a></p>
    </nav>
  </header>
'''

def foot(cur, ask=True):
    items = "\n          ".join(navlinks(cur))
    askblock = '''<div class="ask">
        <h2>Tell me about the business.</h2>
        <div>
          <p>I&rsquo;ll tell you what it needs and what it costs, before anyone signs anything.</p>
          <a class="btn solid" href="/contact">Write to me</a>
          <a class="mail" href="mailto:mitchell@mjlcollective.com">mitchell@mjlcollective.com</a>
        </div>
      </div>''' if ask else ""
    return f'''
  <footer class="foot">
    <div class="wrap">
      {askblock}
      <div class="mark-wall"><img class="big-mark" src="/assets/lockup-plaster.svg" alt="MJL Collective" width="552" height="143" loading="lazy"></div>
      <div class="rows">
        <ul>
          {items}
          <li><a href="/clients">Client login</a></li>
        </ul>
        <div class="legal">
          <span>MJL Collective LLC, Moorestown, New Jersey</span>
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
SIZES = {"lead": "(min-width: 1100px) min(60vw, 860px), 100vw", "project": "(min-width: 900px) min(72vw, 1040px), 100vw",
         "wide": "(min-width: 900px) min(82vw, 1160px), 100vw", "pair": "(min-width: 900px) min(56vw, 800px), 100vw",
         "phone": "(min-width: 900px) min(16vw, 230px), 28vw"}

def pic(shot, alt, sizes, eager=False):
    kind = shot.rsplit("-", 1)[1]
    ws = SHOT_W[kind]
    w, h = (1440, 900) if kind == "d" else (390, 844)
    src = lambda ext: ", ".join(f"/assets/shots/{shot}-{x}.{ext} {x}w" for x in ws)
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{src("avif")}" sizes="{sizes}">'
            f'<img src="/assets/shots/{shot}-{ws[1]}.webp" srcset="{src("webp")}" sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {lz}></picture>')

def browser(url, shot, alt, eager=False, sizes="pair"):
    return f'<a class="browser" href="{url}" target="_blank" rel="noopener"><span class="addr">{host(url)}</span>{pic(shot, alt, SIZES[sizes], eager)}</a>'

def phone(url, shot, alt, eager=False):
    return f'<a class="phone" href="{url}" target="_blank" rel="noopener" tabindex="-1">{pic(shot, alt, SIZES["phone"], eager)}</a>'

def stage(url, d, dalt, p, palt, flip=False, eager=False, sizes="project"):
    return f'<div class="stage{" flip" if flip else ""}">{browser(url, d, dalt, eager, sizes)}{phone(url, p, palt, eager)}</div>'

# Brand panels: only brand work MJL actually did, shown next to the site it belongs to.
def bimg(src, alt, w, h, cls=""):
    return f'<img{" class=" + chr(34) + cls + chr(34) if cls else ""} src="/assets/brand-work/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'

def swatches(items):
    lis = "".join(f'<li><i style="background:{c}"></i>{n}</li>' for n, c in items)
    return f'<ul class="swatches">{lis}</ul>'

def brand(marks, note, extra=""):
    return f'<div class="brand-panel"><div class="marks">{marks}</div>{extra}<p>{note}</p></div>'

def then(before, after):
    return f'<span class="was">{before}</span><span class="to" aria-hidden="true">&rarr;</span>{after}'

BRAND = {
  "arden": brand(bimg("arden-seal.svg", "The Arden Collective oval seal", 120, 145, "tall") + bimg("arden-icon.svg", "The Arden favicon: the oak sprig on an oak green tile", 48, 48, "icon"),
                 "I drew the seal and the leaf mark, chose the four colors and the two typefaces, Libre Caslon Display and Albert Sans, and built the site from them.",
                 swatches([("Blush", "#F8F3F2"), ("Rose", "#DAA1AA"), ("Sage", "#62766D"), ("Brown", "#3B2E27")])),
  "lewiston": brand(bimg("lewiston-badge.webp", "The Lewiston lion badge", 160, 160, "tall") + bimg("lewiston-icon-180.png", "The Lewiston app icon", 60, 60, "icon") + bimg("lewiston-fav-32.png", "The Lewiston favicon at 32 pixels", 32, 32, "px") + bimg("lewiston-fav-16.png", "The Lewiston favicon at 16 pixels", 16, 16, "px"),
                    "The lion badge is theirs. I cut it down into the favicon and app icon, so it still reads at 16 pixels in a browser tab."),
  "simos": brand(bimg("simos-wordmark.webp", "The Simo&rsquo;s Barbering wordmark", 600, 334, "wide") + bimg("simos-pole-256.png", "The barber pole favicon", 48, 48, "icon"),
                 "John&rsquo;s wordmark, cut out clean for the header, and the barber pole as the favicon. The wallpaper pattern on the site is redrawn from a photograph of the real one in the shop."),
  "tiger": brand(then(bimg("tiger-before.webp", "The old Tiger Digital mark", 126, 174, "tall"), bimg("tiger-seal.webp", "The new Tiger Digital seal", 160, 160, "tall")),
                 "The old mark, and the seal that replaced it."),
  "bluethreadz": brand(then(bimg("bluethreadz-before.webp", "The old BlueThreadz logo", 760, 250, "wide"), bimg("bluethreadz-wordmark.webp", "The redrawn BlueThreadz wordmark", 600, 80, "wide")),
                       "The logo before and after I redrew it."),
  "dorothy": brand(bimg("dorothy-sign.webp", "The Dorothy&rsquo;s Flower Shop mark, taken from the old shop sign", 160, 160, "tall"),
                   "The old shop sign, made into the mark."),
}

def about_it(name, url, text, tag="h3", panel=""):
    return f'<div class="about-it"><{tag}>{name}</{tag}><p>{text}</p><a class="link" href="{url}" target="_blank" rel="noopener">Visit {host(url)}</a>{panel}</div>'

def project(cls, name, url, text, d, dalt, p, palt, flip=False, panel=""):
    return f'''<article class="project {cls}">
          {stage(url, d, dalt, p, palt, flip, sizes="wide" if "wide" in cls else "project")}
          {about_it(name, url, text, panel=panel)}
        </article>'''

def pair_item(name, url, text, d=None, dalt="", p=None, palt="", flip=False, panel=""):
    if d and p: art = stage(url, d, dalt, p, palt, flip, sizes="pair")
    elif d: art = browser(url, d, dalt)
    else: art = f'<div class="solo-phone">{phone(url, p, palt)}</div>'
    return f'<article class="item">{art}{about_it(name, url, text, panel=panel)}</article>'

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
          <h2 id="clients-h">The businesses I work with, newest first.</h2>
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
home = f'''    <section class="opening">
      <div class="wrap hero">
        <h1>Websites and brands for local businesses. I build them, then I keep them current.</h1>
        <div class="words">
          <p class="lede">I&rsquo;m Mitchell Lisa, and MJL Collective is my studio in Moorestown, New Jersey. Everything on this page is a site I built. Open any of them and click around.</p>
          <div class="actions">
            <a class="btn solid" href="/contact">Tell me about your business</a>
            <a class="link" href="/work">See all the work</a>
          </div>
        </div>
        <div class="lead">
          {stage(L, "lewiston-finishes-d", "The Lewiston finishes page on a laptop: a stone house above the facade, paint, door and roof choices", "lewiston-top-p", "The Lewiston home page on a phone: Custom homes in Middle Tennessee", eager=True, sizes="lead")}
        </div>
      </div>
    </section>
    <div class="wrap hero-after">
      <p class="credit"><span><strong>Lewiston Design &amp; Build.</strong> Custom homes in Middle Tennessee. Every project has its plans to download, and buyers can try out finishes on the house before they call.</span> <a class="link" href="{L}" target="_blank" rel="noopener">Visit lewistondesignbuild.com</a></p>
    </div>

    {carousel()}

    <section class="projects" aria-labelledby="recent-h" style="padding-top:clamp(40px,5vw,72px)">
      <div class="wrap">
        <div class="section-head">
          <h2 id="recent-h">The newest sites.</h2>
        </div>
        {project("", "Arden Collective", "https://arden-collective.vercel.app", "Talent management for social media creators. I drew the oval seal and built the site around it. The site is in preview.", "arden-home-d", "The Arden Collective home page, with the oval seal: Boutique talent management for social media creators", "arden-business-p", "The Arden Collective business services on a phone, down to Creators and brands, say hello")}
        {project("right", "Loftus Construction", "https://loftus-construction.vercel.app", "A heavy civil contractor in Cinnaminson, New Jersey, building bridges since 1994. The new site is written for the people who hire them, like PennDOT and NJDOT, and is in preview.", "loftus-build-d", "What Loftus builds: bridges, culverts and retaining walls, each with a photo of finished work", "loftus-top-p", "The Loftus home page on a phone: the wordmark and the train, Design-build, preconstruction, construction", flip=True)}
        <div class="pair">
          {pair_item("George Gravenstine Agency", "https://georgeinsurance.agency/quote", "An independent insurance agency on North Church Street, here in Moorestown. Auto and home quotes run on the site, through the agency&rsquo;s own quoting system.", d="george-quote-d", dalt="The George Gravenstine quote page: Start a quote")}
          {pair_item("Simo&rsquo;s Barbering", "https://www.simosbarbering.com", "A traditional barbershop on Lancaster Ave in Wayne. The shop&rsquo;s first website, live one week after I met John.", d="simos-menu-d", dalt="The Simo&rsquo;s Barbering price board on the website")}
        </div>
        <div class="after-projects">
          <p>Tiger Digital, BlueThreadz, Dorothy&rsquo;s and the rest are on the Work page.</p>
          <a class="link" href="/work">See all the work</a>
        </div>
      </div>
    </section>

    <section class="band cement on-light" aria-labelledby="me-h">
      <div class="wrap two">
        <h2 id="me-h">When you reach out, you&rsquo;re talking to me.</h2>
        <div>
          <p>MJL Collective is one person, not an agency. I design the brand, build the site and keep running it after launch.</p>
          <p>Text me a change and it ships. Hosting, fixes, menus, team pages and catalogs stay current without you chasing anyone. When something needs a specialist, like deep search work, I bring in people I trust and tell you up front.</p>
          <div class="actions">
            <a class="link" href="/services">What I do</a>
            <a class="link" href="/about">About me</a>
          </div>
        </div>
      </div>
    </section>'''
page("index.html", "/", "MJL Collective | Websites and brands for local businesses",
     "Mitchell Lisa builds websites and brands for local businesses, then keeps them current. MJL Collective, Moorestown, New Jersey.", home)

# ------------------------------------------------------------------ work
work = f'''    <section class="dark page-head">
      <div class="wrap">
        <h1>Client sites, newest first.</h1>
        <p class="lede">Every project opens the live site, so you can click around. Try them on your phone too.</p>
      </div>
    </section>
    <section class="projects">
      <div class="wrap">
        {project("wide", "Arden Collective", "https://arden-collective.vercel.app", "Talent management for social media creators. The brand is an oval seal I drew for them, and the site is built from the same type and colors. In preview.", "arden-creative-d", "The Arden Collective services: Creative and Business on either side of a Full service oval", "arden-contact-p", "The Arden Collective contact page on a phone, with the email inside a pink oval", panel=BRAND["arden"])}
        {project("right", "Loftus Construction", "https://loftus-construction.vercel.app", "Bridges, culverts, retaining walls, foundations and dams, laid out by type so an engineer can find the work they care about. In preview.", "loftus-record-d", "The Loftus selected record: a table of finished public projects with owner and contract value", "loftus-careers-p", "Loftus careers on a phone: the Bench Strength Program", flip=True)}
        {project("", "Lewiston Design &amp; Build", L, "Custom homes in Middle Tennessee, drawn and built by the same firm. Each house has its drawings to download, and on the finishes page a buyer picks a facade, paint, door and roof and watches the house change.", "lewiston-projects-d", "The Lewiston projects page: three houses, each with its plans", "lewiston-process-p", "The Lewiston process on a phone: discovery, site and feasibility, architectural design", panel=BRAND["lewiston"])}
        <div class="pair mirror">
          {pair_item("Simo&rsquo;s Barbering", "https://www.simosbarbering.com", "The shop&rsquo;s first website, live one week after I met John. The price board, booking, and the hours and directions for 240 Lancaster Ave.", "simos-door-d", "The Simo&rsquo;s shop section: His name on the door, with John at work", "simos-book-p", "The end of the Simo&rsquo;s price board on a phone, and Book a chair", panel=BRAND["simos"])}
          {pair_item("George Gravenstine Agency", "https://georgeinsurance.agency", "An independent agency in Moorestown that quotes across several companies. Auto and home quotes run right on the site, in three to five minutes, through the agency&rsquo;s own quoting system.", "george-home-d", "The George Gravenstine home page: Independent auto, home and business insurance in Moorestown", "george-auto-p", "The George Gravenstine auto insurance page on a phone", flip=True)}
        </div>
        {project("wide", "Tiger Digital", "https://www.tigerdigital.marketing", "A marketing agency for people who just bought a business. New brand and a new site in two days.", "tiger-results-d", "Tiger Digital results: Numbers we can back up", "tiger-top-p", "The Tiger Digital home page on a phone: Real growth. No fluff.", panel=BRAND["tiger"])}
        <div class="pair">
          {pair_item("BlueThreadz", "https://www.bluethreadz.com", "Custom embroidery and printing. I redrew the logo and rebuilt the catalog so every garment leads straight to a quote.", "bluethreadz-ordering-d", "BlueThreadz: What people are ordering right now, a row of jackets, hoodies and polos", "bluethreadz-methods-p", "BlueThreadz on a phone: Five ways to put your name on it", panel=BRAND["bluethreadz"])}
          {pair_item("Dorothy&rsquo;s Flower Shop", "https://www.dorothysflower.shop", "The old shop sign became the mark, then a line of hats and the store that sells them.", "dorothy-home-d", "The Dorothy&rsquo;s Flower Shop home page, with lilacs", "dorothy-shop-p", "The Dorothy&rsquo;s hat shop on a phone", flip=True, panel=BRAND["dorothy"])}
        </div>
      </div>
    </section>'''
page("work.html", "/work", "Work | MJL Collective",
     "Client sites by MJL Collective, newest first: Arden Collective, Loftus Construction, Lewiston Design & Build, Simo's Barbering, George Gravenstine Agency, Tiger Digital, BlueThreadz and Dorothy's Flower Shop.", work)

# ------------------------------------------------------------------ partners
tiles = "\n          ".join(
    f'<li><a href="{u}" target="_blank" rel="noopener"><img class="mark-{k}" src="{s}" width="{w}" height="{h}" alt="{n}" loading="lazy"><span class="nm" aria-hidden="true">{n.replace(" Insurance Agency", "")}</span></a></li>'
    for n, u, s, w, h, k in CLIENTS)
partners = f'''    <section class="dark page-head">
      <div class="wrap">
        <h1>Partners.</h1>
        <p class="lede">The businesses I work with, newest first. Each logo opens the live site.</p>
      </div>
    </section>
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
    return f'<figure>{browser(url, shot, alt)}<figcaption><strong>{name}.</strong> {cap}</figcaption></figure>'

def sheet():
    srcs = lambda ext: ", ".join(f"/assets/brand-work/arden-sheet-{w}.{ext} {w}w" for w in (800, 1600))
    sz = "(min-width: 900px) min(56vw, 800px), 100vw"
    return (f'<figure class="sheet"><picture><source type="image/avif" srcset="{srcs("avif")}" sizes="{sz}">'
            f'<img src="/assets/brand-work/arden-sheet-1600.webp" srcset="{srcs("webp")}" sizes="{sz}" width="1600" height="1352" loading="lazy" decoding="async" '
            f'alt="The Arden Collective brand sheet: the oval seal in brown and in blush, the leaf mark, avatars and favicon, six colors, and the two typefaces"></picture>'
            f'<figcaption><strong>Arden Collective.</strong> The brand sheet I made for Rachael: the seal, the leaf mark and favicon, the colors and the type the site is built from.</figcaption></figure>')

services = f'''    <section class="dark page-head">
      <div class="wrap">
        <h1>The site is where it starts.</h1>
        <p class="lede">Then I keep it current, and help with the channels that usually go stale.</p>
      </div>
    </section>
    <div class="wrap">
      <section class="service" aria-labelledby="s1">
        <div class="words">
          <h2 id="s1">Website and brand</h2>
          <p>The mark, the site, mobile, and clear calls to action. Live in days.</p>
          <p>Tiger Digital went from a new brand to a new site in two days. Simo&rsquo;s had its first website a week after I met the owner.</p>
        </div>
        <div class="shot">{sheet()}</div>
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
about = '''    <section class="dark founder-head">
      <div class="wrap founder">
        <div class="portrait"><img src="/assets/mitchell.webp" alt="Mitchell Lisa in an MJL Collective cap" width="1122" height="1402" fetchpriority="high"></div>
        <div class="intro">
          <h1>Mitchell Lisa</h1>
          <p class="first">MJL Collective is one person, not an agency. I design and build the site, then run what keeps the presence current.</p>
          <p>When you reach out, you are talking to me.</p>
        </div>
      </div>
    </section>
    <section class="founder-body">
      <div class="wrap founder">
        <div class="text">
          <p>I started the company in 2023, and it&rsquo;s still based in Moorestown, New Jersey.</p>
          <p>Some of my clients are right here in town, like the insurance agency on Church Street. Others are a barbershop in Wayne, Pennsylvania, and a homebuilder in Middle Tennessee.</p>
          <p>Most of them started with a site that was out of date, or no site at all. I start with the brand, build the site, and stay on after launch so it doesn&rsquo;t go stale again.</p>
          <div class="actions">
            <a class="btn solid dark" href="/contact">Tell me about your business</a>
            <a class="link" href="/work">See the work</a>
          </div>
        </div>
        <figure class="glass-photo"><img src="/assets/glass-stairs.webp" alt="A stairway seen through a wall of fluted glass" width="1920" height="800" loading="lazy"></figure>
      </div>
    </section>'''
page("about.html", "/about", "About Mitchell Lisa | MJL Collective",
     "Mitchell Lisa runs MJL Collective, a one-person studio in Moorestown, New Jersey that builds websites and brands for local businesses.", about)

# ------------------------------------------------------------------ contact
contact = '''    <section class="dark page-head">
      <div class="wrap">
        <h1>Tell me about the business.</h1>
        <p class="lede">Say what the business does and where it&rsquo;s stuck. I&rsquo;ll tell you what it needs and what it costs, before anyone signs anything.</p>
      </div>
    </section>
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
            <button class="btn solid dark" type="submit">Send message</button>
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
    body = f'''    <section class="dark page-head legal-head">
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
lost = '''    <section class="dark page-head lost">
      <div class="wrap">
        <h1>That page isn&rsquo;t here.</h1>
        <p class="lede">It may have moved when the site changed. The work is a good place to start.</p>
        <div class="actions" style="margin-top:30px">
          <a class="btn solid" href="/work">See the work</a>
          <a class="link" href="/">Home</a>
        </div>
      </div>
    </section>'''
page("404.html", "/404", "Page not found | MJL Collective", "This page could not be found.", lost)
print("built")
