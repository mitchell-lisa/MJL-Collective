// Scroll behavior for the work rooms and the client plates. Nothing moves
// for people who ask for reduced motion.
(function () {
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var clamp = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var ease = function (a, b, x) { var t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  var plates = $$(".plate.focus");
  var rooms = $$(".rooms:not(.flow) .room");
  var G = { vh: innerHeight, roomTops: [], roomsOn: false };
  function measure() {
    var sy = scrollY;
    G.vh = innerHeight;
    G.roomsOn = rooms.length > 0 && !still && innerWidth > 900 && G.vh >= 620;
    if (rooms.length) {
      var box = rooms[0].parentNode.getBoundingClientRect().top + sy, acc = 0;
      G.roomTops = rooms.map(function (el) { var t = box + acc; acc += el.offsetHeight; return t; });
    }
  }
  var last = new Map();
  function put(el, name, val) {
    if (!el) return;
    var k = last.get(el) || {}; if (k[name] === val) return;
    k[name] = val; last.set(el, k); el.style[name] = val;
  }
  function flag(el, cls, on) { if (el.classList.contains(cls) !== on) el.classList.toggle(cls, on); }

  var seen = new Set();
  if ("IntersectionObserver" in window && !still) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      tick();
    }, { rootMargin: "10% 0px" });
    plates.forEach(function (el) {
      var device = el.classList.contains("d") || el.classList.contains("p");
      var target = device ? el : el.querySelector("picture");
      if (target) { target.style.opacity = ".4"; target.style.transform = "translate3d(0,18px,0)"; }
      io.observe(el);
    });
  }
  if ("IntersectionObserver" in window) {
    var pre = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var img = e.target; pre.unobserve(img);
        var go = function () { if (img.decode) img.decode().catch(function () {}); };
        if (img.complete) go(); else img.addEventListener("load", go, { once: true });
      });
    }, { rootMargin: "200% 0px" });
    $$(".room img, .plate img, .ba img").forEach(function (i) { pre.observe(i); });
  }

  var loops = $$("video.loop");
  if (loops.length && "IntersectionObserver" in window && !still) {
    var warm = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.preload = "auto"; warm.unobserve(e.target); } });
    }, { rootMargin: "100% 0px" });
    var want = new Set(), idle = 0;
    function start() {
      want.forEach(function (v) {
        v.muted = true; v.defaultMuted = true;
        if (v.paused) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
      });
    }
    addEventListener("scroll", function () { clearTimeout(idle); idle = setTimeout(start, 200); }, { passive: true });
    var show = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) want.add(v);
        else { want.delete(v); if (!v.paused) v.pause(); }
      });
      clearTimeout(idle); idle = setTimeout(start, 200);
    }, { threshold: 0.25 });
    loops.forEach(function (v) {
      v.muted = true;
      v.addEventListener("playing", function () { v.classList.add("on"); }, { once: true });
      warm.observe(v); show.observe(v);
    });
  } else loops.forEach(function (v) { v.remove(); });

  var queued = false;
  function frame() {
    queued = false;
    var sy = scrollY, vh = G.vh;
    if (seen.size) {
      var reads = [];
      seen.forEach(function (el) { reads.push([el, el.getBoundingClientRect()]); });
      reads.forEach(function (rb) {
        var b = rb[1], cc = (b.top + Math.min(b.height, vh) * .35) / vh, ff = ease(.62, .98, cc);
        var device = rb[0].classList.contains("d") || rb[0].classList.contains("p");
        var pic = device ? rb[0] : rb[0].querySelector("picture");
        put(pic, "opacity", (1 - ff * .6).toFixed(3));
        put(pic, "transform", "translate3d(0," + (ff * 18).toFixed(1) + "px,0)");
        flag(rb[0], "clear", ff === 0);
      });
    }
    if (G.roomsOn) {
      for (var k = 0; k < rooms.length; k++) {
        var top = G.roomTops[k] - sy;
        var nxt = k + 1 < rooms.length ? G.roomTops[k + 1] - sy : vh * 2;
        var near = top < vh * 1.2 && nxt > -vh * .2;
        flag(rooms[k], "near", near);
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
  addEventListener("resize", function () { if (rq) return; rq = true; requestAnimationFrame(function () { rq = false; measure(); frame(); }); }, { passive: true });
  addEventListener("load", function () { measure(); frame(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measure(); frame(); });
  measure();
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
// a body-level overlay. While it is open the page
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

// Work sub-pages: a dropdown on the desktop bar, and an expandable group
// in the phone menu. The Work link itself still goes to the Work page.
(function () {
  function bind(item, isDrawer) {
    var btn = item.querySelector(".sub-toggle");
    var sub = item.querySelector(":scope > .sub");
    if (!btn || !sub) return;
    function setOpen(on) {
      item.classList.toggle("open", on);
      btn.setAttribute("aria-expanded", on ? "true" : "false");
      if (isDrawer) {
        if (on) sub.removeAttribute("hidden");
        else sub.setAttribute("hidden", "");
      }
    }
    if (isDrawer && item.classList.contains("open")) setOpen(true);
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });
    if (!isDrawer) {
      item.addEventListener("mouseenter", function () { setOpen(true); });
      item.addEventListener("mouseleave", function () { setOpen(false); });
      item.addEventListener("focusin", function () { setOpen(true); });
      item.addEventListener("focusout", function (e) {
        if (!item.contains(e.relatedTarget)) setOpen(false);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") setOpen(false);
      });
    }
  }
  [].slice.call(document.querySelectorAll(".nav .has-sub")).forEach(function (el) { bind(el, false); });
  [].slice.call(document.querySelectorAll(".drawer .has-sub")).forEach(function (el) { bind(el, true); });
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

// Preview request on the division pages. Same endpoint as the contact form.
(function () {
  var form = document.querySelector(".preview-form");
  if (!form) return;
  var button = form.querySelector("button");
  var note = form.querySelector(".cf-note");
  var sent = form.querySelector(".cf-sent");
  var grid = form.querySelector(".cf-grid");
  var foot = form.querySelector(".cf-foot");
  var label = button.textContent;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var payload = {};
    new FormData(form).forEach(function (v, k) { payload[k] = v; });
    button.disabled = true;
    button.textContent = "Sending";
    note.hidden = true;
    fetch("/api/contact", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { if (!r.ok) throw new Error("send failed"); grid.hidden = true; foot.hidden = true; sent.hidden = false; })
      .catch(function () { note.hidden = false; button.disabled = false; button.textContent = label; });
  });
})();
