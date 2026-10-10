// Home opening: end the dark band partway down the Lewiston frames so they run
// out into the page, but never above the end of the headline block.
(function () {
  var open = document.querySelector(".opening");
  if (!open) return;
  var lead = open.querySelector(".lead .browser"), words = open.querySelector(".words");
  function fit() {
    var top = open.getBoundingClientRect().top;
    var l = lead.getBoundingClientRect(), w = words.getBoundingClientRect();
    var split = Math.max(l.top - top + l.height * 0.62, w.bottom - top);
    open.style.setProperty("--split", Math.round(split) + "px");
    open.classList.add("split");
  }
  if ("ResizeObserver" in window) new ResizeObserver(fit).observe(open); else addEventListener("resize", fit);
  addEventListener("load", fit);
  fit();
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
