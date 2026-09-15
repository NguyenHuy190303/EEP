#!/usr/bin/env python3
"""Xuất một sơ đồ chạy-theo-bước thành GIF (và MP4) để dán LinkedIn/Slack.

    python3 gif.py trang.html --figure "#luong" --steps 6 --out /tmp/luong.gif

Cách làm: mở chính trang HTML đã build bằng Chrome headless, mỗi bước một lần
với `?step=N&still=1` (steps.js đọc query, đứng yên ở bước đó và ẩn thanh điều
khiển), chụp từng khung rồi ghép bằng ffmpeg. Không có runtime nào thêm, không
tái tạo lại sơ đồ ở chỗ khác — thứ lên GIF đúng bằng thứ người ta thấy trong
trang, nên hai bên không bao giờ lệch nhau.

Đầu ra mặc định kèm cả .mp4: GIF cho feed, MP4 nhẹ hơn ~10 lần cho Slack.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROMES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
)

# Cô lập đúng một hình: ẩn mọi thứ khác nhưng vẫn giữ nguyên chuỗi tổ tiên để
# không mất token/theme. `visibility` thay vì `display` để layout không nhảy.
ISOLATE = """
<style id="__iso">
  body > * {{ display: none !important }}
  body {{ background: var(--bg-page); padding: {pad}px !important; margin: 0 !important }}
  #__wrap {{ display: block !important; max-width: none !important }}
  .steps, .fig-zoom, .theme-toggle {{ display: none !important }}
</style>
<script>
(function () {{
  document.documentElement.dataset.theme = {theme!r};
  var t = document.querySelector({sel!r});
  if (!t) {{ document.title = "NOTFOUND"; return; }}
  var fig = t.closest("figure, .fig, .card") || t;
  var w = document.createElement("div"); w.id = "__wrap";
  document.body.appendChild(w); w.appendChild(fig);
  // Ghi chiều cao thật ra title để gif.py đo rồi cắt khung vừa khít —
  // đoán chiều cao là ra GIF thừa một vùng trống to bằng nửa ảnh.
  document.title = "H" + Math.ceil(w.getBoundingClientRect().height + 2 * {pad});
}})();
</script>
"""


def chrome() -> str:
    exe = next((c for c in CHROMES if Path(c).exists()), None) or shutil.which("chrome")
    if not exe:
        sys.exit("không tìm thấy Chrome")
    return exe


def frame(exe: str, html: Path, step: int, png: Path, size: str, theme: str) -> None:
    subprocess.run(
        [exe, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", f"--window-size={size}",
         f"--screenshot={png}", f"file://{html.resolve()}?step={step}&still=1"],
        capture_output=True, timeout=90, check=True)


def measure(exe: str, html: Path, width: int) -> int | None:
    """Chiều cao thật của hình, đọc từ <title> mà script cô lập ghi vào."""
    r = subprocess.run(
        [exe, "--headless", "--disable-gpu", "--dump-dom",
         f"--window-size={width},900", f"file://{html.resolve()}?step=1&still=1"],
        capture_output=True, timeout=90)
    m = re.search(r"<title>H(\d+)</title>", r.stdout.decode("utf8", "replace"))
    return int(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path, help="trang đã build bằng build.py")
    ap.add_argument("--figure", required=True,
                    help="CSS selector của phần tử .stepped hoặc hình chứa nó")
    ap.add_argument("--steps", type=int, required=True, help="tổng số bước")
    ap.add_argument("--out", type=Path, required=True, help="file .gif để ghi")
    ap.add_argument("--size", default="1200x900",
                    help="RỘNGxCAO — chỉ RỘNG được dùng, CAO tự đo theo hình")
    ap.add_argument("--pad", type=int, default=28, help="lề quanh hình, px")
    ap.add_argument("--fps", type=float, default=0.7,
                    help="khung/giây — 0.7 ≈ mỗi bước dừng 1.4s, đủ để đọc")
    ap.add_argument("--theme", choices=("light", "dark"), default="light")
    ap.add_argument("--no-mp4", action="store_true")
    a = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("cần ffmpeg")
    exe = chrome()
    src = a.html.read_text(encoding="utf8")
    if "steps.js" not in src and "data-step" not in src:
        sys.exit(f"{a.html} không có sơ đồ chạy theo bước (không thấy data-step)")

    tmp = Path(tempfile.mkdtemp(prefix="gif-"))
    page = a.html.parent / f".{a.html.stem}.shot.html"
    page.write_text(src + ISOLATE.format(sel=a.figure, pad=a.pad, theme=a.theme),
                    encoding="utf8")
    try:
        w = int(a.size.split("x")[0])
        h = measure(exe, page, w)
        if h is None:
            sys.exit(f"không tìm thấy {a.figure!r} trong {a.html}")
        size = f"{w},{h}"
        print(f"  hình cao {h}px (đo thật, không đoán)", file=sys.stderr)
        for i in range(1, a.steps + 1):
            frame(exe, page, i, tmp / f"f{i:02d}.png", size, a.theme)
            print(f"  bước {i}/{a.steps}", file=sys.stderr)
        pat = str(tmp / "f%02d.png")
        pal = tmp / "pal.png"
        # palettegen/paletteuse: GIF 256 màu mà không bị vỡ chữ do dither ẩu
        subprocess.run(["ffmpeg", "-y", "-framerate", str(a.fps), "-i", pat,
                        "-vf", "scale=1200:-1:flags=lanczos,palettegen=stats_mode=diff",
                        str(pal)], capture_output=True, check=True)
        subprocess.run(["ffmpeg", "-y", "-framerate", str(a.fps), "-i", pat, "-i", str(pal),
                        "-lavfi", "scale=1200:-1:flags=lanczos[x];[x][1:v]paletteuse="
                                  "dither=bayer:bayer_scale=3",
                        "-loop", "0", str(a.out)], capture_output=True, check=True)
        print(f"OK  {a.out}  ·  {a.out.stat().st_size/1024:.0f} KB  ·  {a.steps} bước")
        if not a.no_mp4:
            mp4 = a.out.with_suffix(".mp4")
            subprocess.run(["ffmpeg", "-y", "-framerate", str(a.fps), "-i", pat,
                            "-vf", "scale=1200:-2:flags=lanczos,format=yuv420p",
                            "-movflags", "+faststart", str(mp4)],
                           capture_output=True, check=True)
            print(f"OK  {mp4}  ·  {mp4.stat().st_size/1024:.0f} KB")
    except subprocess.CalledProcessError as exc:
        sys.exit((exc.stderr or b"").decode()[-400:] or "ffmpeg/chrome thoát khác 0")
    finally:
        page.unlink(missing_ok=True)
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
