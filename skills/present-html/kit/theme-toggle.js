// Bấm sáng/tối. Mặc định theo OS (media query trong tokens.css, không cần JS) —
// script này chỉ xử lý lựa chọn TAY, luôn thắng OS theo cả 2 hướng.
// Việc đọc localStorage lúc mới mở trang nằm ở snippet inline riêng (build.py
// chèn ngay sau <meta charset>, chạy trước khi paint) để tránh chớp sai theme;
// file này chỉ lo phần bấm nút sau đó.
(function () {
  "use strict";

  var KEY = "kit-theme";

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* file:// có thể chặn — bỏ qua */ }
  }

  function current() {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    return dark ? "dark" : "light";
  }

  function apply(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    store(theme);
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".theme-toggle");
    if (!btn) return;
    apply(current() === "dark" ? "light" : "dark");
  });

  // Đồng bộ nếu Huy đổi theme ở 1 tab/file rồi mở lại tab khác cùng phiên
  // (chỉ có tác dụng nếu browser thật sự share localStorage giữa các file://
  // — chưa chắc, xem html-style.md).
  window.addEventListener("storage", function (e) {
    if (e.key === KEY && e.newValue) {
      document.documentElement.setAttribute("data-theme", e.newValue);
    }
  });
})();
