// Mở sơ đồ toàn màn hình, ngay trong trang — không sang tab mới.
// Cuộn để phóng to tại vị trí con trỏ, kéo để di chuyển, Esc để đóng.
// JS thuần: CSP của artifact chặn CDN nên không dùng được thư viện panzoom.
(function () {
  "use strict";

  function el(id) { return document.getElementById(id); }

  var ov = el("zoomOverlay"), stage = el("zoomStage"), layer = el("zoomLayer");
  if (!ov || !stage || !layer) return;
  var pct = el("zoomPct"), name = el("zoomName"), note = el("zoomNote");

  var MIN = 0.15, MAX = 8;
  var s = 1, tx = 0, ty = 0, w = 0, h = 0;
  var dragging = false, lx = 0, ly = 0, lastFocus = null, wentFull = false;

  // ── tìm SVG mermaid đã vẽ ────────────────────────────────────────────────
  // Runtime vẽ mermaid không đồng bộ, và KHÔNG chắc để SVG lại trong
  // thẻ pre.mermaid ban đầu — có thể thay hẳn thẻ đó. Nên thử nhiều đường,
  // và loại các icon sprite (svg.i) ở thanh tiêu đề.
  function findSvg(fig) {
    var cands = fig.querySelectorAll(".fig-bd svg, [class*='mermaid'] svg, svg");
    for (var i = 0; i < cands.length; i++) {
      var c = cands[i];
      if (c.classList.contains("i")) continue;      // icon sprite
      if (c.closest(".fig-hd")) continue;            // icon trong tiêu đề
      return c;
    }
    return null;
  }

  function apply() {
    layer.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + s + ")";
    if (pct) pct.textContent = Math.round(s * 100) + "%";
  }

  function fit() {
    var r = stage.getBoundingClientRect(), pad = 20;
    if (!w || !h || !r.width || !r.height) { s = 1; tx = 0; ty = 0; apply(); return; }
    s = Math.min((r.width - pad * 2) / w, (r.height - pad * 2) / h);
    if (!isFinite(s) || s <= 0) s = 1;
    if (s > 1) s = 1;                                // không phóng quá cỡ thật
    tx = (r.width - w * s) / 2;
    ty = (r.height - h * s) / 2;
    apply();
  }

  // Phóng to quanh một điểm: điểm dưới con trỏ không xê dịch.
  function zoomAt(cx, cy, factor) {
    var ns = Math.min(MAX, Math.max(MIN, s * factor));
    if (ns === s) return;
    var px = (cx - tx) / s, py = (cy - ty) / s;
    tx = cx - px * ns; ty = cy - py * ns; s = ns;
    apply();
  }
  function zoomCenter(f) {
    var r = stage.getBoundingClientRect();
    zoomAt(r.width / 2, r.height / 2, f);
  }

  // ── toàn màn hình thật, nếu trình duyệt cho ───────────────────────────────
  function goFull() {
    var fn = ov.requestFullscreen || ov.webkitRequestFullscreen;
    if (!fn) return;
    try {
      var p = fn.call(ov);
      if (p && p.catch) p.catch(function () { /* iframe không cho — lớp phủ vẫn kín khung */ });
      wentFull = true;
    } catch (e) { /* bỏ qua, lớp phủ vẫn kín khung */ }
  }
  function leaveFull() {
    if (!(document.fullscreenElement || document.webkitFullscreenElement)) return;
    var fn = document.exitFullscreen || document.webkitExitFullscreen;
    if (!fn) return;
    try { var p = fn.call(document); if (p && p.catch) p.catch(function () {}); } catch (e) {}
  }

  function mount(svg) {
    // Đo kích thước thật TRƯỚC khi bỏ ràng buộc width của mermaid.
    var box = svg.getBoundingClientRect();
    var vb = (svg.getAttribute("viewBox") || "").split(/[\s,]+/).map(Number);
    w = (vb.length === 4 && vb[2] > 0) ? vb[2] : box.width;
    h = (vb.length === 4 && vb[3] > 0) ? vb[3] : box.height;

    var c = svg.cloneNode(true);
    c.removeAttribute("style");
    c.removeAttribute("width");
    c.removeAttribute("height");
    c.style.width = w + "px";
    c.style.height = h + "px";
    c.style.maxWidth = "none";

    layer.textContent = "";
    layer.appendChild(c);
    if (note) note.hidden = true;
    fit();
  }

  function open(fig) {
    var t = fig.querySelector(".fig-hd .t");
    if (name) name.textContent = t ? t.textContent.trim() : "Sơ đồ";

    lastFocus = document.activeElement;
    layer.textContent = "";
    if (note) { note.hidden = false; note.textContent = "Đang chờ sơ đồ vẽ xong…"; }
    ov.hidden = false;
    document.body.style.overflow = "hidden";
    goFull();
    var close = el("zoomClose");
    if (close) close.focus();

    // Mermaid vẽ không đồng bộ: thử lại vài nhịp thay vì bỏ cuộc ngay.
    var delays = [0, 250, 600, 1200, 2000], i = 0;
    (function attempt() {
      if (ov.hidden) return;
      var svg = findSvg(fig);
      if (svg) { mount(svg); return; }
      if (++i < delays.length) { setTimeout(attempt, delays[i]); return; }
      if (note) note.textContent = "Không đọc được sơ đồ này. Thử đóng rồi mở lại.";
    })();
  }

  function close() {
    if (ov.hidden) return;
    ov.hidden = true;
    layer.textContent = "";
    document.body.style.overflow = "";
    if (wentFull) { leaveFull(); wentFull = false; }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // ── mở: uỷ quyền sự kiện trên document, không gắn từng nút ───────────────
  // Sống sót cả khi mermaid thay thế node bên trong hình.
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".fig-zoom");
    if (btn) {
      var fig = btn.closest(".fig");
      if (fig) { e.preventDefault(); open(fig); }
      return;
    }
    if (e.target === ov) close();
  });
  document.addEventListener("dblclick", function (e) {
    var bd = e.target.closest && e.target.closest(".fig-bd");
    if (bd && !ov.contains(e.target)) {
      var fig = bd.closest(".fig");
      if (fig) open(fig);
    }
  });

  // ── điều khiển ───────────────────────────────────────────────────────────
  function on(id, fn) { var n = el(id); if (n) n.addEventListener("click", fn); }
  on("zoomClose", close);
  on("zoomIn", function () { zoomCenter(1.25); });
  on("zoomOut", function () { zoomCenter(0.8); });
  on("zoomFit", fit);

  stage.addEventListener("wheel", function (e) {
    e.preventDefault();
    var r = stage.getBoundingClientRect();
    // ctrl+wheel là cử chỉ chụm hai ngón trên trackpad — bước lớn hơn
    var k = e.ctrlKey ? 0.01 : 0.0018;
    zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * k));
  }, { passive: false });

  stage.addEventListener("pointerdown", function (e) {
    if (e.button !== 0) return;
    dragging = true; lx = e.clientX; ly = e.clientY;
    stage.classList.add("grabbing");
    try { stage.setPointerCapture(e.pointerId); } catch (err) {}
  });
  stage.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    tx += e.clientX - lx; ty += e.clientY - ly;
    lx = e.clientX; ly = e.clientY;
    apply();
  });
  function endDrag() { dragging = false; stage.classList.remove("grabbing"); }
  stage.addEventListener("pointerup", endDrag);
  stage.addEventListener("pointercancel", endDrag);

  document.addEventListener("keydown", function (e) {
    if (ov.hidden) return;
    if (e.key === "Escape") { close(); }
    else if (e.key === "+" || e.key === "=") { e.preventDefault(); zoomCenter(1.25); }
    else if (e.key === "-" || e.key === "_") { e.preventDefault(); zoomCenter(0.8); }
    else if (e.key === "0") { e.preventDefault(); fit(); }
  });

  // Thoát toàn màn hình bằng Esc của trình duyệt → đóng luôn lớp phủ.
  function fsChange() {
    var isFull = !!(document.fullscreenElement || document.webkitFullscreenElement);
    if (!isFull && wentFull && !ov.hidden) { wentFull = false; close(); }
    else if (!ov.hidden) fit();
  }
  document.addEventListener("fullscreenchange", fsChange);
  document.addEventListener("webkitfullscreenchange", fsChange);
  window.addEventListener("resize", function () { if (!ov.hidden) fit(); });
})();
