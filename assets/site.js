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
    if (el.classList.contains("enter")) return tall ? ["tall", "/assets/glass/frost-tall.webp"] : ["wall", "/assets/glass/frost-wall.webp"];
    return tall ? ["tall", "/assets/glass/frost-tall.webp"] : ["band", "/assets/glass/frost-band.webp"];
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
  var cellsets = [];
  if (enter && !still) {
    enter.classList.add("live");
    $$(".wall", enter).forEach(function (w) {
      var list = $$(".cells i", w).map(function (el) { return { el: el, t: parseFloat(el.getAttribute("data-t")) || 0, o: -1 }; });
      cellsets.push({ wall: w, cells: list });
    });
  }
  // Lens: a soft circle around the pointer where the frost lifts. Desktop only.
  var lenses = [];
  if (fine && !still) {
    var hosts = [];
    if (enter) $$(".wall", enter).forEach(function (w) { hosts.push({ box: w, src: w.querySelector(".clear"), after: w.querySelector(".cells"), host: enter }); });
    if (head) hosts.push({ box: head, src: head.querySelector(".gp"), after: head.querySelector(".frost"), host: head });
    hosts.forEach(function (h) {
      if (!h.src || !h.after) return;
      var l = document.createElement("div"); l.className = "lens"; l.setAttribute("aria-hidden", "true");
      var c = h.src.cloneNode(true); c.removeAttribute("class");
      $$("img", c).forEach(function (i) { i.removeAttribute("fetchpriority"); i.setAttribute("alt", ""); });
      l.appendChild(c);
      h.after.parentNode.insertBefore(l, h.after.nextSibling);
      lenses.push({ el: l, box: h.box, host: h.host });
    });
    var mx = -999, my = -999, lq = false;
    function moveLens() {
      lq = false;
      lenses.forEach(function (L) {
        var r = L.box.getBoundingClientRect();
        L.el.style.setProperty("--mx", (mx - r.left).toFixed(0) + "px");
        L.el.style.setProperty("--my", (my - r.top).toFixed(0) + "px");
      });
    }
    addEventListener("pointermove", function (e) { mx = e.clientX; my = e.clientY; if (!lq) { lq = true; requestAnimationFrame(moveLens); } }, { passive: true });
    document.addEventListener("pointerleave", function () { mx = my = -999; moveLens(); });
  }

  var seen = new Set();
  if ("IntersectionObserver" in window && !still) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      tick();
    }, { rootMargin: "10% 0px" });
    plates.forEach(function (el) { el.style.setProperty("--f", "1"); io.observe(el); });
  }

  var queued = false;
  function frame() {
    queued = false;
    var vh = innerHeight;
    if (enter && !still) {
      var r = enter.getBoundingClientRect();
      var p = clamp(-r.top / Math.max(1, r.height - vh));
      var st = enter.style;
      var w = ease(0, .12, p), f = ease(.03, .2, p);
      var m = f * (1 - ease(.8, .9, p)), c = ease(.84, .95, p);
      st.setProperty("--w", w.toFixed(3));
      st.setProperty("--f", f.toFixed(3));
      st.setProperty("--m", m.toFixed(3));
      st.setProperty("--c", c.toFixed(3));
      enter.classList.toggle("frosted", f > .995);
      enter.classList.toggle("past-words", w > .995);
      enter.classList.toggle("at-end", c > .5);
      // each block clears on its own, from the middle outwards
      cellsets.forEach(function (set) {
        if (!set.wall.offsetParent && set.wall.offsetWidth === 0) return;
        for (var i = 0; i < set.cells.length; i++) {
          var cl = set.cells[i];
          var a = .22 + cl.t * .5;
          var o = 1 - ease(a, a + .08, p);
          o = Math.round(o * 50) / 50;
          if (o !== cl.o) { cl.o = o; cl.el.style.opacity = o; }
        }
      });
      lenses.forEach(function (L) { if (L.host === enter) L.el.style.setProperty("--l", (f * (1 - ease(.2, .3, p))).toFixed(3)); });
    }
    if (head && !still) {
      var h = head.getBoundingClientRect();
      var hf = ease(0, .9, -h.top / Math.max(1, h.height));
      head.style.setProperty("--f", hf.toFixed(3));
      lenses.forEach(function (L) { if (L.host === head) L.el.style.setProperty("--l", hf.toFixed(3)); });
    }
    seen.forEach(function (el) {
      var b = el.getBoundingClientRect();
      var cc = (b.top + Math.min(b.height, vh) * .35) / vh;
      var ff = ease(.62, .98, cc);
      el.style.setProperty("--f", ff.toFixed(3));
      el.classList.toggle("clear", ff === 0);
    });
    // the exhibition: the next room comes up over this one, which settles back
    if (rooms.length && !still && innerWidth > 900 && vh >= 620) {
      for (var k = 0; k < rooms.length; k++) {
        var rin = rooms[k].firstElementChild;
        var top = rooms[k].getBoundingClientRect().top;
        var nxt = rooms[k + 1] ? rooms[k + 1].getBoundingClientRect().top : vh * 2;
        var come = ease(0, 1, 1 - top / vh);             // 0 while below the fold, 1 once it fills the screen
        var go = ease(0, 1, 1 - nxt / vh);               // 1 once the next room covers it
        var o = (.35 + .65 * come) * (1 - .9 * go);
        rin.style.setProperty("--o", o.toFixed(3));
        rin.style.setProperty("--y", ((1 - come) * 60).toFixed(1) + "px");
        rin.style.setProperty("--k", (1 - .05 * go).toFixed(4));
      }
    }
  }
  function tick() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  addEventListener("scroll", tick, { passive: true });
  addEventListener("resize", function () { align(); tick(); });
  addEventListener("load", align);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(align);
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

// Phone menu: the bar's Menu button opens the drawer of links.
(function () {
  var btn = document.querySelector(".menu-btn");
  var drawer = document.getElementById("drawer");
  if (!btn || !drawer) return;
  function set(open) {
    drawer.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.textContent = open ? "Close" : "Menu";
  }
  btn.addEventListener("click", function () { set(!drawer.classList.contains("open")); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
  addEventListener("resize", function () { if (innerWidth > 900) set(false); });
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
