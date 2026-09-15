#!/usr/bin/env python3
"""Ghép một fragment HTML thành trang publish được, theo bộ "Cà phê sữa".

    python3 ~/Projects/EEP/skills/present-html/kit/build.py body.html out.html --title "Tên Trang"

Fragment đầu vào chỉ cần phần nội dung: <header class="hdr"> + <main> với các
<section class="card">. Script tự lo phần còn lại:

  · nạp fonts.css + tokens.css + components.css + fullscreen.css
  · cắm sprite icon, lớp phủ toàn màn hình, và fullscreen.js
  · gắn chỉ thị %%{init}%% đúng loại cho từng sơ đồ mermaid (ghi đè cái có sẵn)
  · thêm nút "Toàn màn hình" vào mọi .fig-hd còn thiếu
  · KIỂM rồi mới ghi ra: thẻ đóng/mở, icon, id mà JS gọi, init hợp lệ,
    và không có nền tối nào trong sơ đồ

Thoát khác 0 nếu có lỗi — đừng publish khi script chưa xanh.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent

# ── màu sơ đồ: nền SÁNG, chữ TỐI, không ngoại lệ ──────────────────────────
# Mermaid tự suy màu chữ từ độ sáng nền và suy SAI trên nền tối. Cách sửa
# không phải chọn màu chữ khác mà là không bao giờ dùng nền tối trong sơ đồ.
BASE = (
    "'background':'#FAF4EA','mainBkg':'#FAF4EA','primaryColor':'#FAF4EA',"
    "'primaryTextColor':'#2B1E10','primaryBorderColor':'#C4A67C',"
    "'nodeTextColor':'#2B1E10','nodeBorder':'#C4A67C',"
    "'secondaryColor':'#EFE3CF','secondaryTextColor':'#2B1E10','secondaryBorderColor':'#C4A67C',"
    "'tertiaryColor':'#F3E7D3','tertiaryTextColor':'#2B1E10','tertiaryBorderColor':'#C4A67C',"
    "'lineColor':'#6F4522','textColor':'#2B1E10','titleColor':'#120B03',"
    "'fontFamily':'Inter,sans-serif','fontSize':'13px',"
    "'clusterBkg':'#EFE3CF','clusterBorder':'#C4A67C',"
    "'edgeLabelBackground':'#FAF4EA','labelBackground':'#FAF4EA','labelTextColor':'#2B1E10',"
    "'noteBkgColor':'#F8EEDC','noteTextColor':'#2B1E10','noteBorderColor':'#C4A67C'"
)

PER_KIND = {
    "pie": (
        "'pie1':'#E5B3A8','pie2':'#E3CE9B','pie3':'#CBD7A4','pie4':'#B9CBD8',"
        "'pieStrokeColor':'#FAF4EA','pieStrokeWidth':'2px','pieOuterStrokeColor':'#6F4522',"
        "'pieOuterStrokeWidth':'1px','pieTitleTextColor':'#120B03',"
        "'pieSectionTextColor':'#120B03','pieSectionTextSize':'13px','pieLegendTextColor':'#2B1E10'"
    ),
    # CẢ BA biến màu chữ của gantt đều đặt tối: mermaid chọn biến nào cũng ra
    # chữ tối trên thanh sáng. taskTextDarkColor là cái bẫy đã dẫm một lần.
    "gantt": (
        "'taskBkgColor':'#E8D7BE','taskBorderColor':'#6F4522',"
        "'taskTextColor':'#2B1E10','taskTextDarkColor':'#120B03','taskTextLightColor':'#120B03',"
        "'taskTextOutsideColor':'#2B1E10','taskTextClickableColor':'#175A87',"
        "'activeTaskBkgColor':'#F1DCD2','activeTaskBorderColor':'#B02A1E',"
        "'gridColor':'#C4A67C','sectionBkgColor':'#FAF4EA','altSectionBkgColor':'#F3E7D3',"
        "'sectionBkgColor2':'#FAF4EA','todayLineColor':'#B02A1E'"
    ),
    "sequenceDiagram": (
        "'actorBkg':'#E8D7BE','actorBorder':'#6F4522','actorTextColor':'#120B03',"
        "'actorLineColor':'#C4A67C','signalColor':'#6F4522','signalTextColor':'#2B1E10',"
        "'activationBkgColor':'#EFE3CF','activationBorderColor':'#6F4522',"
        "'loopTextColor':'#2B1E10','sequenceNumberColor':'#120B03'"
    ),
    "stateDiagram": (
        "'labelBoxBkgColor':'#FAF4EA','labelBoxBorderColor':'#C4A67C',"
        "'transitionColor':'#6F4522','transitionLabelColor':'#2B1E10',"
        "'stateLabelColor':'#120B03','altBackground':'#EFE3CF'"
    ),
}

# nền quá tối để mermaid đặt chữ lên — chặn ở cửa
DARK_FILLS = re.compile(r"fill:#(?:3A2413|28180C|6F4522|B02A1E|7A1D14|120B03|2B1E10)\b", re.I)

BUTTON = (
    '<button class="fig-zoom" type="button" aria-label="Mở sơ đồ toàn màn hình">'
    '<svg class="i"><use href="#ic-expand"/></svg> Toàn màn hình</button>'
)

THEME_BUTTON = (
    '<button class="theme-toggle" type="button" aria-label="Đổi giao diện sáng/tối">'
    '<svg class="i tt-sun"><use href="#ic-sun"/></svg>'
    '<svg class="i tt-moon"><use href="#ic-moon"/></svg></button>'
)

# Chạy TRƯỚC style/body — đọc lựa chọn tay đã lưu và set [data-theme] ngay, để
# tránh chớp sai theme (media query trong tokens.css lo phần theo-OS, script
# này chỉ lo phần override tay đã lưu từ lần trước).
THEME_BOOT = (
    "<script>try{var t=localStorage.getItem('kit-theme');"
    "if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>\n"
)

TAGS = ("style script svg symbol main header section div pre table thead tbody "
        "tr td th ol ul li p span button figure figcaption").split()


def kind_of(src: str) -> str:
    for k in ("pie", "gantt", "sequenceDiagram", "stateDiagram", "erDiagram", "classDiagram"):
        if re.search(r"^\s*" + k, src, re.M):
            return k
    return "flowchart"


def init_for(kind: str) -> str:
    tv = BASE + ("," + PER_KIND[kind] if kind in PER_KIND else "")
    return "%%{init:{'theme':'base','themeVariables':{" + tv + "}}}%%"


def pin_mermaid(body: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        inner = re.sub(r"^\s*%%\{init:.*?\}%%\s*\n", "", m.group(1), flags=re.S)
        return ('<pre class="mermaid">\n' + init_for(kind_of(inner)) + "\n"
                + inner.lstrip("\n") + "</pre>")

    return re.subn(r'<pre class="mermaid">(.*?)</pre>', repl, body, flags=re.S)


def add_buttons(body: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        head = m.group(1)
        return m.group(0) if "fig-zoom" in head else head + BUTTON + m.group(2)

    return re.subn(r'(<div class="fig-hd">.*?)(\s*</div>)', repl, body, flags=re.S)


def add_theme_toggle(body: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        head = m.group(1)
        return m.group(0) if "theme-toggle" in head else head + THEME_BUTTON + m.group(2)

    return re.subn(r'(<header class="hdr">.*?)(\s*</header>)', repl, body, flags=re.S)


def strip_inline(html: str) -> str:
    """Bỏ nội dung <script>/<style> — thẻ trong comment JS không phải thẻ thật."""
    html = re.sub(r"<script\b[^>]*>.*?</script>", "<script></script>", html, flags=re.S)
    return re.sub(r"<style\b[^>]*>.*?</style>", "<style></style>", html, flags=re.S)


def check(doc: str) -> list[str]:
    errs: list[str] = []
    lean = re.sub(r"base64,[A-Za-z0-9+/=]+", "base64,X", doc)
    bare = strip_inline(lean)

    for tag in TAGS:
        o = len(re.findall(rf"<{tag}[\s>]", bare))
        c = len(re.findall(rf"</{tag}>", bare))
        sc = len(re.findall(rf"<{tag}\b[^>]*/>", bare))
        if o - sc != c:
            errs.append(f"thẻ <{tag}> lệch: {o} mở / {sc} tự đóng / {c} đóng")

    # `bare` chứ không phải `lean`: steps.js dựng nút bằng chuỗi JS có
    # <use href="#..."> nối động, soi trong script sẽ báo icon ảo.
    symbols = set(re.findall(r'<symbol[^>]*id="([^"]+)"', lean))
    for ref in sorted(set(re.findall(r'<use href="#([^"]+)"', bare)) - symbols):
        errs.append(f"<use> trỏ tới icon không có trong sprite: #{ref}")

    dom = set(re.findall(r'id="([^"]+)"', lean))
    called = {a or b for a, b in re.findall(r'getElementById\("([^"]+)"\)|\bel\("([^"]+)"\)', lean)}
    for missing in sorted(called - dom - {""}):
        errs.append(f"JS gọi id không tồn tại trong DOM: {missing}")

    for i, blob in enumerate(re.findall(r"%%\{init:(\{.*?\})\}%%", lean), 1):
        try:
            json.loads(blob.replace("'", '"'))
        except Exception as exc:
            errs.append(f"init sơ đồ {i} không phải JSON hợp lệ: {exc}")

    for i, blk in enumerate(re.findall(r'<pre class="mermaid">(.*?)</pre>', lean, re.S), 1):
        lines = [l for l in blk.split("\n") if l.strip()]
        if not lines or not lines[0].startswith("%%{init:"):
            errs.append(f"sơ đồ {i}: init không ở dòng đầu")
        if blk.count("%%{init:") != 1:
            errs.append(f"sơ đồ {i}: có {blk.count('%%{init:')} chỉ thị init")
        for bad in DARK_FILLS.findall(blk):
            errs.append(f"sơ đồ {i}: nền tối {bad} — sơ đồ chỉ dùng nền sáng, "
                        f"nhấn mạnh bằng stroke-width và font-weight")

    figs = len(re.findall(r'class="fig-hd"', lean))
    btns = len(re.findall(r'class="fig-zoom"', lean))
    if figs != btns:
        errs.append(f"{figs} hình nhưng {btns} nút toàn màn hình")

    # SVG vẽ tay không được tự khai font: Inter/Fira Code chỉ tồn tại khi
    # fonts.css được nhúng, còn "Inter, sans-serif" viết tay sẽ rơi về
    # Helvetica/Courier — lệch hẳn phần chữ còn lại của trang, và dấu tiếng
    # Việt vỡ. Dùng var(--sans) qua CSS, chữ mono thì class="m".
    for bad in re.findall(r'font-family\s*=\s*"([^"]*)"', lean):
        errs.append(f'SVG khai font-family="{bad}" — bỏ đi, kit tự ép '
                    f'var(--sans); chữ mono thì thêm class="m"')

    # Sơ đồ chạy theo bước: số bước phải liên tục từ 1. Thiếu một số ở giữa là
    # người xem bấm "sau" mà không thấy gì đổi.
    steps = sorted({int(s) for s in re.findall(r'data-step="(\d+)"', lean)})
    if steps and steps != list(range(1, len(steps) + 1)):
        errs.append(f"data-step không liên tục từ 1: thấy {steps}")
    if steps and not re.search(r'class="[^"]*\bstepped\b', lean):
        errs.append("có data-step nhưng không phần tử nào mang class stepped — "
                    "sẽ không có gì chạy")

    # Sàn chữ: dưới 11px là metadata, không phải câu để đọc. Muốn nhét thêm
    # chữ vào sơ đồ thì cắt chữ hoặc nới khung, không thu nhỏ font.
    for size in re.findall(r'font-size\s*=\s*"([\d.]+)"', lean):
        if float(size) < 11:
            errs.append(f"SVG có chữ {size}px — sàn là 11px; cắt chữ hoặc "
                        f"nới khung chứ đừng thu nhỏ font")

    hdrs = len(re.findall(r'<header class="hdr">', lean))
    toggles = len(re.findall(r'class="theme-toggle"', lean))
    if hdrs != toggles:
        errs.append(f"{hdrs} header nhưng {toggles} nút đổi theme")

    if len(doc) > 16 * 1024 * 1024:
        errs.append(f"file {len(doc)/1e6:.1f} MB — trần publish là 16 MB")

    return errs


CHROMES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
)


def shoot(html: Path, png: Path, size: str, theme: str) -> str | None:
    """Chụp trang ra PNG bằng Chrome headless. Trả None nếu xong, chuỗi lỗi nếu hỏng.

    Lý do tồn tại: extension Chrome từ chối URL file://, nên cách duy nhất để
    TỰ soi lại trang vừa build là headless. Không có bước này thì lỗi hiển thị
    (font rơi về Courier, chữ tràn khung, dấu tiếng Việt vỡ) chỉ lộ ra khi Huy
    mở file — tức là sau khi đã giao.
    """
    import shutil
    import subprocess
    import tempfile

    exe = next((c for c in CHROMES if Path(c).exists()), None) or shutil.which("chrome")
    if not exe:
        return "không tìm thấy Chrome"
    m = re.fullmatch(r"(\d+)x(\d+)", size.strip())
    if not m:
        return f"--shot-size {size!r} phải dạng RỘNGxCAO"

    # Ép [data-theme] cho CẢ hai chiều. Trước đây chỉ ép "dark" và để "light"
    # phó mặc prefers-color-scheme — máy chuyển sang dark lúc chiều là ảnh
    # chụp "light" ra tối, sai lặng lẽ.
    tmp = Path(tempfile.mkstemp(suffix=".html", dir=html.parent)[1])
    tmp.write_text(html.read_text(encoding="utf8")
                   + f'\n<script>document.documentElement.dataset.theme="{theme}"</script>\n',
                   encoding="utf8")
    src = tmp
    try:
        subprocess.run(
            [exe, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=2", f"--window-size={m[1]},{m[2]}",
             f"--screenshot={png}", f"file://{src.resolve()}?still=1"],
            capture_output=True, timeout=90, check=True,
        )
    except subprocess.CalledProcessError as exc:
        return (exc.stderr or b"").decode()[-200:] or "chrome thoát khác 0"
    except subprocess.TimeoutExpired:
        return "chrome quá 90s"
    finally:
        if tmp:
            tmp.unlink(missing_ok=True)
    print(f"    ảnh: {png} ({size}, theme {theme}) — MỞ RA XEM trước khi giao")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("body", type=Path, help="fragment: header.hdr + main")
    ap.add_argument("out", type=Path, help="file html để publish")
    ap.add_argument("--title", required=True, help="tên trang — danh từ ngắn, đặc trưng")
    ap.add_argument("--no-fonts", action="store_true",
                    help="bỏ font nhúng (~950 KB) — CHỈ khi build nháp để xem thử; "
                         "bản giao cho người khác luôn nhúng font")
    ap.add_argument("--shot", type=Path, default=None,
                    help="chụp trang ra PNG bằng Chrome headless để tự soi lại "
                         "(extension Chrome không mở được file://)")
    ap.add_argument("--shot-size", default="1400x2400",
                    help="khung chụp RỘNGxCAO, mặc định 1400x2400. Đặt CAO lớn "
                         "để lấy trọn trang dài")
    ap.add_argument("--shot-theme", choices=("light", "dark"), default="light",
                    help="chụp ở theme nào, mặc định light")
    args = ap.parse_args()

    body = args.body.read_text(encoding="utf8")
    body, n_mmd = pin_mermaid(body)
    body, _ = add_buttons(body)
    body, _ = add_theme_toggle(body)

    css = ["" if args.no_fonts else (KIT / "fonts.css").read_text(encoding="utf8")]
    css += [(KIT / f).read_text(encoding="utf8")
            for f in ("tokens.css", "components.css", "diagram.css", "fullscreen.css")]

    # charset tường minh: khi mở trang bằng http.server hay file://, không có header
    # charset nào và Chrome rơi về windows-1252 — toàn bộ tiếng Việt thành mojibake.
    # Lúc publish artifact thì wrapper tự lo, nên chỗ này chỉ cứu đường mở cục bộ.
    # THEME_BOOT đứng NGAY sau charset, trước cả <style> — đọc lựa chọn tay đã lưu
    # và set [data-theme] sớm nhất có thể để đỡ chớp sai theme lúc mở lại trang.
    doc = ('<meta charset="utf-8">\n' + THEME_BOOT
           + f"<title>{args.title}</title>\n<style>\n" + "\n".join(css) + "\n</style>\n"
           + (KIT / "sprite.html").read_text(encoding="utf8") + "\n"
           + body + "\n"
           + (KIT / "overlay.html").read_text(encoding="utf8") + "\n"
           + "<script>\n" + (KIT / "fullscreen.js").read_text(encoding="utf8") + "\n</script>\n"
           + "<script>\n" + (KIT / "theme-toggle.js").read_text(encoding="utf8") + "\n</script>\n"
           + "<script>\n" + (KIT / "steps.js").read_text(encoding="utf8") + "\n</script>\n")

    errs = check(doc)
    if errs:
        print("KHÔNG GHI — có lỗi:", file=sys.stderr)
        for e in errs:
            print(f"  · {e}", file=sys.stderr)
        return 1

    # Ghi nguyên tử: build hỏng giữa chừng không được để lại file cụt cho
    # người khác mở phải.
    tmp_out = args.out.with_suffix(args.out.suffix + ".part")
    tmp_out.write_text(doc, encoding="utf8")
    tmp_out.replace(args.out)
    lean_kb = len(strip_inline(re.sub(r"base64,[A-Za-z0-9+/=]+", "", doc))) / 1024
    print(f"OK  {args.out}  ·  {len(doc)/1024:.0f} KB (nội dung {lean_kb:.0f} KB)")
    print(f"    {n_mmd} sơ đồ đã gắn init · nút toàn màn hình đủ · thẻ khớp · icon khớp")
    if args.shot:
        rc = shoot(args.out, args.shot, args.shot_size, args.shot_theme)
        if rc:
            print(f"    (ảnh chụp lỗi — {rc})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
