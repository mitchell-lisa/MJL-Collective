// Clear, blur, clear. The glass block photograph sits clear at the top of a page,
// frosts over as the page moves on, and the work comes up clear through it.
// Only opacity changes on scroll; the blur itself is drawn once. Nothing moves
// for people who ask for reduced motion.
(function () {
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (still) return;
  var clamp = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var ease = function (a, b, x) { var t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  var through = document.querySelector(".through");
  var head = document.querySelector(".glass-head");
  var plates = [].slice.call(document.querySelectorAll(".plate.focus"));
  if (through) through.classList.add("live");
  var seen = new Set();
  if ("IntersectionObserver" in window) {
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
    if (through) {
      var r = through.getBoundingClientRect();
      var p = clamp(-r.top / Math.max(1, r.height - vh));
      var st = through.style;
      st.setProperty("--w", ease(0, .26, p).toFixed(3));
      st.setProperty("--f", ease(.06, .44, p).toFixed(3));
      st.setProperty("--s", ease(.28, .44, p).toFixed(3));
      var v = 1 - ease(.46, .8, p);
      st.setProperty("--v", v.toFixed(3));
      through.classList.toggle("clear", v === 0);
    }
    if (head) {
      var h = head.getBoundingClientRect();
      head.style.setProperty("--f", ease(0, .9, -h.top / Math.max(1, h.height)).toFixed(3));
    }
    seen.forEach(function (el) {
      var b = el.getBoundingClientRect();
      var c = (b.top + Math.min(b.height, vh) * .35) / vh;
      var f = ease(.62, .98, c);
      el.style.setProperty("--f", f.toFixed(3));
      el.classList.toggle("clear", f === 0);
    });
  }
  function tick() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  addEventListener("scroll", tick, { passive: true });
  addEventListener("resize", tick);
  frame();
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
