import re, pathlib, sys

# Nguồn: gói npm lucide-static (MIT). Lấy lại khi cần thêm icon:
#   cd /tmp && npm pack lucide-static@latest && tar xzf lucide-static-*.tgz
SRC = pathlib.Path("/tmp/lucide-dl/package/icons")

# id trong sprite -> tên file lucide. Giữ nguyên 20 id cũ để trang đã build không vỡ.
ICONS = {
    # --- 20 id cũ, map sang hình lucide tương ứng ---
    "zap":"zap", "warn":"triangle-alert", "err":"circle-x", "ok":"circle-check",
    "info":"info", "clock":"clock", "cpu":"cpu", "monitor":"monitor",
    "server":"server", "branch":"git-branch", "activity":"activity", "search":"search",
    "layers":"layers", "list":"list", "eye":"eye", "net":"network",
    "expand":"maximize", "shrink":"minimize", "sun":"sun", "moon":"moon",
    # --- người & thiết bị ---
    "user":"user", "users":"users", "laptop":"laptop", "phone":"smartphone",
    "browser":"app-window", "globe":"globe",
    # --- hạ tầng ---
    "db":"database", "disk":"hard-drive", "cloud":"cloud", "container":"container",
    "box":"box", "package":"package", "tower":"radio-tower", "plug":"plug",
    "gateway":"door-open", "queue":"align-justify", "cache":"layers-2",
    # --- model / AI ---
    "brain":"brain", "bot":"bot", "sparkle":"sparkles",
    # --- bảo mật ---
    "lock":"lock", "unlock":"lock-open", "shield":"shield", "shield-ok":"shield-check",
    "key":"key-round",
    # --- dữ liệu & file ---
    "file":"file-text", "files":"files", "folder":"folder", "book":"book-open",
    "json":"braces", "code":"code", "terminal":"terminal",
    # --- luồng & điều khiển ---
    "arrow":"arrow-right", "swap":"arrow-right-left", "down":"arrow-down",
    "split":"split", "merge":"git-merge", "commit":"git-commit-horizontal",
    "loop":"repeat", "retry":"rotate-ccw", "refresh":"refresh-cw",
    "workflow":"workflow", "waypoints":"waypoints", "route":"route",
    "filter":"filter", "funnel":"funnel",
    # --- trạng thái ---
    "check":"check", "x":"x", "alert":"circle-alert", "help":"circle-help",
    "flame":"flame", "snow":"snowflake", "flag":"flag", "target":"target",
    "pin":"map-pin", "bell":"bell", "mail":"mail", "hook":"webhook",
    # --- đo lường ---
    "chart":"chart-column", "gauge":"gauge", "timer":"timer", "hourglass":"hourglass",
    "scale":"scale", "trend":"trending-up", "trend-down":"trending-down",
    # --- công cụ ---
    "wrench":"wrench", "gear":"settings", "sliders":"sliders-horizontal",
    "trash":"trash-2", "download":"download", "upload":"upload", "link":"link",
    "share":"share-2",
    # --- điều khiển animation ---
    "play":"play", "pause":"pause", "next":"chevron-right", "prev":"chevron-left",
}

out, missing = [], []
for sid, name in ICONS.items():
    f = SRC / f"{name}.svg"
    if not f.exists():
        missing.append(f"{sid}->{name}")
        continue
    body = f.read_text()
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)            # lucide có comment license
    m = re.search(r"<svg\b[^>]*>(.*)</svg>", body, flags=re.S)   # lấy đúng phần trong
    inner = m.group(1)
    inner = re.sub(r"\s+", " ", inner).strip()
    inner = re.sub(r'\s*(stroke|fill|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"', "", inner)
    out.append(f'<symbol id="ic-{sid}" viewBox="0 0 24 24">{inner}</symbol>')

sprite = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>\n'
          + "\n".join(out) + "\n</defs></svg>\n")
pathlib.Path(__file__).parent / "sprite.html".write_text(sprite)
print(f"{len(out)} icon · thiếu: {missing or 'không'} · sprite {len(sprite)/1024:.1f} KB")
