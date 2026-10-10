// The glass. Mitchell's glass block wall sits clear at the top of the page.
// On the home page it frosts over as you scroll, then the blocks clear one at
// a time and a client site is behind them. Only opacity and transform change
// on scroll; the frosted glass is drawn ahead of time. Nothing moves for
// people who ask for reduced motion.
(function () {
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia && matchMedia("(hover: hover) and (pointer: fine)").matches;
  var clamp = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var ease = function (a, b, x) { var t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  // Frosted panes: line the frosted copy of the photograph up behind each
  // pane so it reads as part of the same wall in every browser.
  function frostFor(el) {
    var tall = innerWidth <= 700;
    if (el.classList.contains("enter")) return tall ? ["tall", "/assets/glass/soft-tall.webp"] : ["wall", "/assets/glass/soft-wall.webp"];
    return tall ? ["tall", "/assets/glass/soft-tall.webp"] : ["band", "/assets/glass/soft-band.webp"];
  }
  var ASPECT = { wall: 5423 / 3389, band: 5423 / 2358, tall: 1947 / 4214 };
  function align() {
    $$(".glass-head, .enter").forEach(function (host) {
      var pane = host.querySelector(".pane"); if (!pane) return;
      var f = frostFor(host), box;
      var wallEl = host.querySelector(f[0] === "tall" ? ".wall-tall" : ".wall-wall");
      if (host.classList.contains("enter") && wallEl) box = wallEl.getBoundingClientRect();
      else {
        var g = host.querySelector(".gp"); if (!g) return;
        var r = g.getBoundingClientRect(), a = ASPECT[f[0]], w = r.width, h = r.height;
        if (w / h > a) { h = w / a; } else { w = h * a; }
        box = { left: r.left + (r.width - w) / 2, top: r.top + (r.height - h) / 2, width: w, height: h };
      }
      var p = pane.getBoundingClientRect(), s = pane.style;
      s.setProperty("--fi", "url(" + f[1] + ")");
      s.setProperty("--fx", (box.left - p.left).toFixed(1) + "px");
      s.setProperty("--fy", (box.top - p.top).toFixed(1) + "px");
      s.setProperty("--fw", box.width.toFixed(1) + "px");
      s.setProperty("--fh", box.height.toFixed(1) + "px");
      pane.classList.add("aligned");
    });
  }

  var enter = document.querySelector(".enter");
  var head = document.querySelector(".glass-head");
  var plates = $$(".plate.focus");
  var rooms = $$(".room");
  if (enter && !still) enter.classList.add("live");
  // Lens: a soft circle around the pointer where the frost lifts. Desktop only.
  var lenses = [];
  if (fine && !still) {
    var hosts = [];
    if (enter) $$(".wall", enter).forEach(function (w) { hosts.push({ box: w, src: w.querySelector(".clear"), after: w.querySelector(".frosted"), host: enter }); });
    if (head) hosts.push({ box: head, src: head.querySelector(".gp"), after: head.querySelector(".frost"), host: head });
    hosts.forEach(function (h) {
      if (!h.src || !h.after) return;
      var l = document.createElement("div"); l.className = "lens"; l.setAttribute("aria-hidden", "true");
      var c = h.src.cloneNode(true); c.removeAttribute("class");
      $$("img", c).forEach(function (i) { i.removeAttribute("fetchpriority"); i.setAttribute("alt", ""); i.setAttribute("loading", "lazy"); });
      l.appendChild(c);
      h.after.parentNode.insertBefore(l, h.after.nextSibling);
      lenses.push({ el: l, box: h.box, host: h.host, last: "" });
    });
    var mx = -999, my = -999, lq = false, lensOn = false;
    function moveLens() {
      lq = false;
      lenses.forEach(function (L) {
        var r = L.box.getBoundingClientRect();
        L.el.style.setProperty("--mx", (mx - r.left).toFixed(0) + "px");
        L.el.style.setProperty("--my", (my - r.top).toFixed(0) + "px");
      });
    }
    addEventListener("pointermove", function (e) { mx = e.clientX; my = e.clientY; if (!lensOn) { lensOn = true; lenses.forEach(function (L) { L.el.classList.add("on"); }); } if (!lq) { lq = true; requestAnimationFrame(moveLens); } }, { passive: true });
    document.addEventListener("pointerleave", function () { mx = my = -999; moveLens(); });
  }

  // Everything below runs once per frame at most and reads nothing from the
  // layout while scrolling: positions are measured on load and resize, and
  // each frame only does arithmetic on scrollY and writes opacity/transform.
  var barGlass = $$(".bar-glass i");
  var barFrost = document.querySelector(".bar-glass .f");
  var G = { vh: innerHeight, enterTop: 0, enterH: 1, headTop: 0, headH: 1, roomTops: [], roomsOn: false };
  function measure() {
    var sy = scrollY;
    G.vh = innerHeight;
    if (enter) { var r = enter.getBoundingClientRect(); G.enterTop = r.top + sy; G.enterH = r.height; }
    // the bar's pre-blurred copy of the wall, placed where the wall sits once
    // the entrance stage is pinned to the top of the screen
    if (enter && barGlass.length) {
      var wl = enter.querySelector(innerWidth <= 700 ? ".wall-tall" : ".wall-wall"), st = enter.querySelector(".enter-stage");
      if (wl && st) {
        var wr = wl.getBoundingClientRect(), sr = st.getBoundingClientRect();
        barGlass.forEach(function (i) {
          i.style.left = wr.left.toFixed(1) + "px"; i.style.top = (wr.top - sr.top).toFixed(1) + "px";
          i.style.width = wr.width.toFixed(1) + "px"; i.style.height = wr.height.toFixed(1) + "px";
        });
      }
    }
    if (head) { var h = head.getBoundingClientRect(); G.headTop = h.top + sy; G.headH = h.height; }
    G.roomsOn = rooms.length > 0 && !still && innerWidth > 900 && G.vh >= 620;
    if (rooms.length) {
      var box = rooms[0].parentNode.getBoundingClientRect().top + sy, acc = 0;
      G.roomTops = rooms.map(function (el) { var t = box + acc; acc += el.offsetHeight; return t; });
    }
  }
  var last = new Map();
  // write real properties on the element that moves, not inherited custom
  // properties on a parent, so a scroll frame never restyles a whole subtree
  function put(el, name, val) {
    if (!el) return;
    var k = last.get(el) || {}; if (k[name] === val) return;
    k[name] = val; last.set(el, k); el.style[name] = val;
  }
  var E = enter ? { words: enter.querySelector(".enter-words"), print: enter.querySelector(".print"), frost: $$(".wall .frosted", enter) } : null;
  var headFrost = head ? head.querySelector(".frost") : null;
  function flag(el, cls, on) { if (el.classList.contains(cls) !== on) el.classList.toggle(cls, on); }

  var seen = new Set();
  if ("IntersectionObserver" in window && !still) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      tick();
    }, { rootMargin: "10% 0px" });
    plates.forEach(function (el) { var pc = el.querySelector("picture"); if (pc) { pc.style.opacity = ".4"; pc.style.transform = "translate3d(0,18px,0)"; } io.observe(el); });
  }
  // decode pictures a screen or two before they arrive, so no frame waits on it
  if ("IntersectionObserver" in window) {
    var pre = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var img = e.target; pre.unobserve(img);
        var go = function () { if (img.decode) img.decode().catch(function () {}); };
        if (img.complete) go(); else img.addEventListener("load", go, { once: true });
      });
    }, { rootMargin: "200% 0px" });
    $$(".room img, .plate img, .print img, .ba img, .lens img").forEach(function (i) { pre.observe(i); });
  }

  var queued = false;
  function frame() {
    queued = false;
    var sy = scrollY, vh = G.vh;
    if (enter) flag(document.documentElement, "over-enter", sy < G.enterTop + G.enterH - 40);
    if (enter && !still) {
      var p = clamp((sy - G.enterTop) / Math.max(1, G.enterH - vh));
      var w = ease(0, .18, p), f = ease(.04, .34, p), c = ease(.36, .66, p);
      put(E.words, "opacity", (1 - w).toFixed(3));
      put(E.words, "transform", "translate3d(0," + (-36 * w).toFixed(1) + "px,0)");
      // never fully 0: the frost layer stays rastered and decoded from load, so
      // the first scroll frame does not wait on it
      E.frost.forEach(function (el) { put(el, "opacity", Math.max(f, .002).toFixed(3)); });
      put(barFrost, "opacity", f.toFixed(3));
      put(E.print, "opacity", c.toFixed(3));
      put(E.print, "transform", "translate3d(-50%,calc(-50% + " + ((1 - c) * 28).toFixed(1) + "px),0)");
      flag(enter, "frosted", f > .995);
      flag(enter, "past-words", w > .995);
      flag(enter, "showing", p > .2);
      flag(enter, "at-end", c > .6);
      lenses.forEach(function (L) { if (L.host === enter) put(L.el, "opacity", (f * (1 - c)).toFixed(3)); });
    }
    if (head && !still) {
      var hf = ease(0, .9, (sy - G.headTop) / Math.max(1, G.headH));
      put(headFrost, "opacity", hf.toFixed(3));
      lenses.forEach(function (L) { if (L.host === head) put(L.el, "opacity", hf.toFixed(3)); });
    }
    if (seen.size) {
      var reads = [];
      seen.forEach(function (el) { reads.push([el, el.getBoundingClientRect()]); });
      reads.forEach(function (rb) {
        var b = rb[1], cc = (b.top + Math.min(b.height, vh) * .35) / vh, ff = ease(.62, .98, cc);
        var pic = rb[0].querySelector("picture");
        put(pic, "opacity", (1 - ff * .6).toFixed(3));
        put(pic, "transform", "translate3d(0," + (ff * 18).toFixed(1) + "px,0)");
        flag(rb[0], "clear", ff === 0);
      });
    }
    // the exhibition: the next room comes up over this one, which settles back
    if (G.roomsOn) {
      for (var k = 0; k < rooms.length; k++) {
        var top = G.roomTops[k] - sy;
        var nxt = k + 1 < rooms.length ? G.roomTops[k + 1] - sy : vh * 2;
        var near = top < vh * 1.2 && nxt > -vh * .2;
        flag(rooms[k], "near", near);
        // a room the next one has fully covered stays stuck underneath; stop painting it
        flag(rooms[k], "covered", nxt <= 0);
        if (!near) continue;
        var come = ease(0, 1, 1 - Math.max(0, top) / vh);
        var go = ease(0, 1, 1 - nxt / vh);
        var rin = rooms[k].firstElementChild;
        put(rin, "opacity", ((.4 + .6 * come) * (1 - .88 * go)).toFixed(3));
        put(rin, "transform", "translate3d(0," + ((1 - come) * 48).toFixed(1) + "px,0)");
      }
    }
  }
  function tick() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  addEventListener("scroll", tick, { passive: true });
  var rq = false;
  addEventListener("resize", function () { if (rq) return; rq = true; requestAnimationFrame(function () { rq = false; measure(); align(); frame(); }); }, { passive: true });
  addEventListener("load", function () { measure(); align(); frame(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measure(); align(); frame(); });
  measure();
  align();
  frame();
})();

// Before and after: the range input is the control, so it works with a
// finger, a mouse and the arrow keys.
(function () {
  [].slice.call(document.querySelectorAll(".ba-range")).forEach(function (input) {
    var frame = input.parentNode;
    function set() { frame.style.setProperty("--x", input.value + "%"); input.setAttribute("aria-valuetext", input.value + "% before"); }
    input.addEventListener("input", set);
    set();
  });
})();

// Phone menu: the bar's Menu button opens the drawer of links. The drawer is
// a body-level overlay (not inside the frosted bar). While it is open the page
// underneath is pinned in place, which is the scroll lock iOS Safari honours,
// and put back exactly where it was on close.
(function () {
  var btn = document.querySelector(".menu-btn");
  var drawer = document.getElementById("drawer");
  if (!btn || !drawer) return;
  var body = document.body, root = document.documentElement, y = 0, isOpen = false;
  function others(on) {
    for (var el = body.firstElementChild; el; el = el.nextElementSibling) {
      if (el === drawer || el.tagName === "HEADER" || el.tagName === "SCRIPT") continue;
      if (on) el.setAttribute("inert", ""); else el.removeAttribute("inert");
    }
  }
  function set(open, keepFocus) {
    if (open === isOpen) return;
    isOpen = open;
    if (open) {
      y = window.scrollY || root.scrollTop || 0;
      body.style.top = -y + "px";
      body.classList.add("menu-open");
    } else {
      body.classList.remove("menu-open");
      body.style.top = "";
      var sb = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      window.scrollTo(0, y);
      root.style.scrollBehavior = sb;
    }
    drawer.classList.toggle("open", open);
    others(open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.textContent = open ? "Close" : "Menu";
    if (open) { var first = drawer.querySelector("a"); if (first) first.focus({ preventScroll: true }); }
    else if (!keepFocus) btn.focus({ preventScroll: true });
  }
  btn.addEventListener("click", function () { set(!isOpen); });
  drawer.addEventListener("click", function (e) { if (e.target.closest && e.target.closest("a")) set(false, true); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && isOpen) set(false); });
  addEventListener("resize", function () { if (innerWidth > 900) set(false, true); });
  addEventListener("pageshow", function () { if (isOpen) set(false, true); });
})();

// The contact form posts to /api/contact, which emails the submission
// straight to Mitchell's inbox and a confirmation to the visitor.
(function () {
  var form = document.getElementById("cf");
  if (!form) return;
  var button = form.querySelector("button");
  var note = form.querySelector(".cf-note");
  var sent = form.querySelector(".cf-sent");
  var grid = form.querySelector(".cf-grid");
  var foot = form.querySelector(".cf-foot");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var payload = {};
    new FormData(form).forEach(function (v, k) { payload[k] = v; });
    button.disabled = true; button.textContent = "Sending"; note.hidden = true;
    fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { if (!r.ok) throw new Error("send failed"); grid.hidden = true; foot.hidden = true; sent.hidden = false; form.reset(); })
      .catch(function () { note.hidden = false; })
      .then(function () { button.disabled = false; button.textContent = "Send message"; });
  });
})();
