// W3 showcase: section tabs, the report / samples views, sample filters, audio playhead and seek.
(function () {
  "use strict";
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  $$(".sc-tabs").forEach(function (t) {
    var b = $$("[role=tab]", t), p = $$("[role=tabpanel]", t);
    b.forEach(function (x, i) {
      x.addEventListener("click", function () {
        b.forEach(function (y, j) { y.setAttribute("aria-selected", j === i); p[j].hidden = j !== i; });
      });
    });
  });

  // Two views on one page: #samples shows the re-check list, any other hash shows the report.
  var views = $$("[data-view]");
  function route() {
    var samples = location.hash === "#samples";
    views.forEach(function (v) { v.hidden = (v.getAttribute("data-view") === "samples") !== samples; });
    $$(".sc-viewlink").forEach(function (a) { a.classList.toggle("on", (a.getAttribute("href") === "#samples") === samples); });
    if (!samples && location.hash.length > 1) {
      var el = document.querySelector(location.hash);
      if (el) el.scrollIntoView();
    }
  }
  if (views.length) { window.addEventListener("hashchange", route); route(); }

  var list = document.querySelector(".sc-smp-list");
  if (list) {
    var cards = $$(".sc-smp", list), q = document.querySelector(".sc-smp-q"), grp = document.querySelector(".sc-smp-g"),
        st = document.querySelector(".sc-smp-s"), srt = document.querySelector(".sc-smp-o"), cnt = document.querySelector(".sc-smp-n");
    var apply = function () {
      var term = (q.value || "").toLowerCase(), g = grp ? grp.value : "", s = st ? st.value : "", shown = 0;
      cards.forEach(function (c) {
        var ok = (!term || c.getAttribute("data-q").indexOf(term) >= 0) && (!g || c.getAttribute("data-group") === g)
          && (!s || c.getAttribute("data-pass") === s);
        c.hidden = !ok; if (ok) shown++;
      });
      var o = srt ? srt.value : "";
      if (o) {
        var key = function (c) { return o === "id" ? c.getAttribute("data-id") : parseFloat(c.getAttribute("data-metric")); };
        cards.slice().sort(function (a, b) {
          var x = key(a), y = key(b);
          return o === "id" ? (x < y ? -1 : x > y ? 1 : 0) : o === "asc" ? x - y : y - x;
        }).forEach(function (c) { list.appendChild(c); });
      }
      cnt.textContent = shown;
    };
    [q, grp, st, srt].forEach(function (el) { if (el) el.addEventListener("input", apply); });
  }

  // Audio <-> timeline: a playhead follows the audio; a click on a track or a turn time seeks.
  $$(".sc-smp, .sc-panel").forEach(function (card) {
    var au = card.querySelector("audio"), tl = card.querySelector(".sc-tl[data-dur]");
    if (!au || !tl) return;
    var dur = parseFloat(tl.getAttribute("data-dur")), t0 = parseFloat(tl.getAttribute("data-start") || "0");
    var heads = $$(".sc-ph", tl);
    au.addEventListener("timeupdate", function () {
      var pct = Math.max(0, Math.min(100, (au.currentTime - t0) / dur * 100));
      heads.forEach(function (h) { h.style.left = pct + "%"; h.style.display = "block"; });
    });
    $$(".sc-tl-track", tl).forEach(function (tr) {
      tr.addEventListener("click", function (e) {
        var r = tr.getBoundingClientRect();
        au.currentTime = t0 + (e.clientX - r.left) / r.width * dur; au.play();
      });
    });
    $$("[data-t]", card).forEach(function (b) {
      b.addEventListener("click", function () { au.currentTime = parseFloat(b.getAttribute("data-t")); au.play(); });
    });
  });
})();
