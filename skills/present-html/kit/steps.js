/* steps.js — sơ đồ chạy theo bước.
 *
 * Hợp đồng: MẶC ĐỊNH mọi bước hiện đủ (CSS không ẩn gì). Script này mới hạ
 * các bước chưa tới xuống mờ. Không JS, in ra giấy, hay prefers-reduced-motion
 * → vẫn thấy trọn thông tin. Motion chỉ dẫn nhịp đọc, không giữ nghĩa.
 *
 * Đọc query string, để gif.py chụp từng bước mà không cần tiêm JS:
 *   ?step=3   dừng mọi sơ đồ ở bước 3
 *   ?still=1  ẩn chrome chỉ có khi tương tác (thanh điều khiển, nút zoom, nút theme)
 */
(function () {
  function btn(act, label, icon) {
    return '<button type="button" data-act="' + act + '" aria-label="' + label +
      '"><svg class="i"><use href="#' + icon + '"/></svg></button>';
  }
  var q = new URLSearchParams(location.search);
  var forced = parseInt(q.get("step"), 10);
  var still = q.get("still") === "1";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (still) document.documentElement.classList.add("shooting");

  document.querySelectorAll(".stepped").forEach(function (root) {
    var items = [].slice.call(root.querySelectorAll("[data-step]"));
    if (!items.length) return;
    var max = items.reduce(function (m, el) {
      return Math.max(m, parseInt(el.getAttribute("data-step"), 10) || 0);
    }, 0);
    if (max < 2) return;

    var labels = {};
    items.forEach(function (el) {
      var n = parseInt(el.getAttribute("data-step"), 10);
      if (!labels[n] && el.getAttribute("data-label")) labels[n] = el.getAttribute("data-label");
    });

    // Thanh điều khiển do JS dựng: không JS thì mọi bước hiện đủ, thanh này
    // vô nghĩa — nên nó không nên tồn tại trong HTML tĩnh.
    var bar = document.createElement("div");
    bar.className = "steps";
    bar.innerHTML =
      '<span class="cap"></span><span class="dots"></span>' +
      btn("first", "Về bước đầu", "ic-retry") + btn("prev", "Bước trước", "ic-prev") +
      btn("play", "Chạy hoặc dừng", "ic-pause") + btn("next", "Bước sau", "ic-next");
    (root.closest("figure, .card") || root).appendChild(bar);

    // still=1 mà KHÔNG chốt bước nào → hiện trọn mọi bước. Đây là trạng thái
    // dùng cho ảnh chụp và bản in: khung hình tĩnh phải mang đủ thông tin,
    // không được chỉ thấy bước 1 rồi 5/6 sơ đồ mờ tịt.
    var showAll = still && !(forced > 0);
    var cur = forced > 0 ? Math.min(forced, max) : 1;
    var timer = null;
    var dwell = parseInt(root.getAttribute("data-dwell"), 10) || 1900;

    function paint() {
      items.forEach(function (el) {
        var n = parseInt(el.getAttribute("data-step"), 10);
        el.classList.remove("done", "now", "todo");
        el.classList.add(showAll ? "done" : n < cur ? "done" : n === cur ? "now" : "todo");
      });
      if (!bar) return;
      var cap = bar.querySelector(".cap");
      if (cap) cap.innerHTML = "Bước <b>" + cur + "/" + max + "</b>" +
        (labels[cur] ? " · " + labels[cur] : "");
      [].slice.call(bar.querySelectorAll(".dots i")).forEach(function (d, i) {
        d.className = i + 1 === cur ? "on" : i + 1 < cur ? "past" : "";
      });
      var pp = bar.querySelector('[data-act="play"] use');
      if (pp) pp.setAttribute("href", timer ? "#ic-pause" : "#ic-play");
    }
    function go(n) { cur = ((n - 1 + max) % max) + 1; paint(); }
    function stop() { clearInterval(timer); timer = null; paint(); }
    function play() { if (timer) return stop(); timer = setInterval(function () { go(cur + 1); }, dwell); paint(); }

    if (bar) {
      var dots = bar.querySelector(".dots");
      if (dots && !dots.children.length)
        for (var i = 0; i < max; i++) dots.appendChild(document.createElement("i"));
      bar.addEventListener("click", function (e) {
        var b = e.target.closest("button");
        if (!b) return;
        var a = b.getAttribute("data-act");
        if (a === "play") return play();
        stop();
        go(a === "next" ? cur + 1 : a === "prev" ? cur - 1 : 1);
      });
    }
    paint();

    // Tự chạy khi cuộn tới, dừng khi rời khỏi màn hình. Không tự chạy nếu
    // người dùng đã chốt bước qua query, hoặc hệ thống xin giảm chuyển động.
    if (!(forced > 0) && !reduce && !still && "IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (en.isIntersecting) { if (!timer) play(); }
          else if (timer) stop();
        });
      }, { threshold: 0.45 }).observe(root);
    }
  });
})();
