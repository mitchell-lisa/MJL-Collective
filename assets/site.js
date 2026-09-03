// The pinned bar goes solid as soon as the page leaves the top.
(function () {
  var bar = document.getElementById("top");
  function onScroll() { bar.classList.toggle("solid", window.scrollY > 24); }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

// Scale each preview iframe so the render fits its frame. The render width is
// --vw on the frame, which the stylesheet drops to a phone width on small
// screens, so a phone visitor sees the client's mobile layout rather than a
// shrunken desktop one. Computed in JS because container-query units are not
// applied reliably in every mobile WebKit view; the cqw value is the fallback.
(function () {
  var screens = document.querySelectorAll(".screen");
  function fit() {
    for (var i = 0; i < screens.length; i++) {
      var base = parseFloat(getComputedStyle(screens[i]).getPropertyValue("--vw")) || 1280;
      screens[i].style.setProperty("--s", (screens[i].clientWidth / base).toFixed(4));
    }
  }
  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(fit);
    for (var i = 0; i < screens.length; i++) ro.observe(screens[i]);
  } else {
    addEventListener("resize", fit);
  }
  fit();
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
