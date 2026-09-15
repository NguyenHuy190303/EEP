# html-kit — 2 theme: Slate Light / Dracula

Style mặc định cho mọi trang HTML làm cho Huy. Kit này thuộc skill `present-html` —
quy trình và luật nằm ở `../SKILL.md`, lý do và catalogue lỗi ở `../references/design-rules.md`.
File này chỉ là tham chiếu component + token.

```bash
python3 ~/Projects/EEP/skills/present-html/kit/build.py body.html out.html --title "Tên Trang" \
  --shot /tmp/shot.png --shot-size 1500x3000   # rồi MỞ ẢNH RA XEM
```

| File | Nội dung |
|---|---|
| `build.py` | Ghép + kiểm. Thoát khác 0 là có lỗi, đừng publish |
| `fonts.css` | Inter 400/500/600/700 + Fira Code 400/500/600, nhúng data URI, có subset tiếng Việt |
| `tokens.css` | ~28 token màu (2 theme) + kiểu chữ + toàn bộ component gốc + nút đổi theme |
| `components.css` | `.fig` `.ba` `.amp` `.big` `.flow-edge` `.flow-pulse` — bổ sung cho tài liệu có sơ đồ |
| `fullscreen.css` + `fullscreen.js` | Nút và lớp phủ xem sơ đồ toàn màn hình (dùng chung cho mermaid VÀ svg vẽ tay) |
| `theme-toggle.js` | Bấm đổi sáng/tối, lưu `localStorage`, luôn thắng `prefers-color-scheme` |
| `sprite.html` | 20 icon, dùng qua `<svg class="i"><use href="#ic-…"/></svg>` |
| `overlay.html` | Khung lớp phủ — `build.py` tự cắm |

## Token màu — 2 theme, cùng tên biến

Slate Light (mặc định, `:root`; Tailwind slate + accent bậc 600 — cùng bộ archify dùng, đổi
15/09/2026 thay Solarized) và Dracula (`:root[data-theme="dark"]`, hoặc tự động khi
`prefers-color-scheme:dark` và chưa ai bấm ép sáng). Không đổi hex — 8 accent đã qua
`validate_palette.mjs` trên `#ffffff` và `#f8fafc`: contrast non-text ≥3.0:1, cặp gần nhất
orange/amber ΔE76 21.9.

| Vai trò | Slate Light | Dracula |
|---|---|---|
| Nền trang / card / trong cùng | `#f8fafc` `#ffffff` `#f8fafc` | `#282a36` `#363a4a` `#21222c` |
| Thanh nổi (header/code) — luôn tối ở cả 2 | `#0f172a` / `#0f172a` / `#020617` | `#44475a` / `#21222c` / `#191a21` |
| Chữ heading/body/muted/subtle | `#0f172a` `#334155` `#64748b` `#94a3b8` | `#f8f8f2` `#e6e6e0` `#6272a4` `#4d5273` |
| `--red` crit | `#e11d48` | `#ff5555` |
| `--yellow` warn | `#d97706` | `#f1fa8c` |
| `--green` ok | `#059669` | `#50fa7b` |
| `--blue`/`--cyan` info | `#2563eb` / `#0891b2` | `#8be9fd` (chung, Dracula không có blue riêng) |
| `--violet` / `--magenta` | `#7c3aed` / `#db2777` | `#bd93f9` (Purple) / `#ff79c6` (Pink) |

`--on-dark-*` (dùng trong `.code-bd`, luôn nền tối ở CẢ 2 theme) **không đổi theo theme** — 1 bộ
dùng chung (accent Dracula, đọc tốt trên cả `#0f172a` và `#21222c`). `--sans`/`--mono`/`--r-*` cũng
chỉ khai 1 lần, không cần lặp lại theo theme.

**Mọi rgba/tint trong component đi qua `color-mix(in srgb, var(--x) N%, transparent)`, không
hardcode hex** — đây là điều dễ quên nhất khi thêm component mới; hardcode là component đó sẽ "kẹt"
ở 1 theme dù `:root` đã đổi.

## Component

**Khung trang** — `<header class="hdr">` dính trên (luôn tối, chữ sáng ở cả 2 theme) rồi `<main>`
(72rem, flex column, gap 1.5rem) chứa các `<section class="card">`. Trong `.card` các con cách nhau
bằng `gap`, nên **bọc từng nhóm văn trong `<div>`** thay vì dựa vào margin của `<p>`.

**`.theme-toggle`** — nút sáng/tối trong `.hdr`, `build.py` tự chèn nếu thiếu (cùng cơ chế nút toàn
màn hình). 2 icon `ic-sun`/`ic-moon` bên trong, CSS tự ẩn/hiện theo `[data-theme]` — không cần JS
đổi icon tay.

**`.card-top`** — hàng tiêu đề: khối chữ bên trái, badge trạng thái bên phải.

**`.metrics`** — dải 4 số: `<div><span class="l">nhãn</span><span class="v">số</span></div>`.

**`.alert{ok|warn|err|info}`** — hộp có viền trái dày: `<div class="h">` là tiêu đề, rồi `<p>`.

**`.badge{ok|warn|crit|info|blue}`** — chip trạng thái, LUÔN kèm chữ (không bao giờ chỉ 1 chấm màu
— lý do ở `../references/design-rules.md`). Trên thanh header dùng `.hdr .badge` (biến thể trong suốt, tự áp dụng).

**`.tw` + `<table>`** — bọc bảng để cuộn ngang được. `class="num"` cho ô số (đã `tabular-nums`).
`tr.hl` làm nổi một dòng. `<caption>` nằm dưới bảng, dùng ghi nguồn số đo.

**`.code`** — khối số/lệnh nền tối (cả 2 theme): `.code-hd` là strip trên, `.code-bd` là thân. Span
tô màu trong thân: `.k` từ khoá · `.f` hàm · `.s` chuỗi · `.t` số/kiểu · `.c` chú thích.

**`.checklist`** — danh sách có số/nhãn: `<span class="n">` là chip, rồi `<b>` tiêu đề và
`<div class="d">` diễn giải.

**`.tl`** — dòng thời gian: `<span class="when">` mốc, `<b>` tiêu đề, `<div class="d">` nội dung.
`li.now` làm nổi mốc hiện tại.

**`.fig`** — khung hình chung cho SƠ ĐỒ (mermaid HOẶC svg vẽ tay — xem `../references/design-rules.md` về
khi nào dùng cái nào): `.fig-hd` strip tối có nhãn mono (`.t` trái, `.r` phải), `.fig-bd` chứa
`<pre class="mermaid">` hoặc trực tiếp `<svg>`, `.fig-cap` chú thích dưới. Dùng thẻ thật
`<figure class="fig">`/`<figcaption class="fig-cap">` khi nội dung là svg vẽ tay (semantics/a11y);
CSS/JS chỉ quan tâm class nên không cần đổi gì. `build.py` tự thêm nút toàn màn hình vào `.fig-hd`;
`fullscreen.js` tìm `svg` bất kỳ trong `.fig-bd` (không chỉ mermaid) nên hoạt động với cả hai.

**`.flow-edge`** — nét đứt chạy dọc 1 cạnh svg, biểu diễn dữ liệu di chuyển (dùng RẤT tiết chế, 1
cạnh/hình, không phải mọi cạnh). **`.flow-pulse`** — nốt nhấp nháy nhẹ cho 1 điểm đang là trọng tâm.
Cả hai thuần CSS `@keyframes`, tự tắt theo rule `prefers-reduced-motion` đã có ở `tokens.css`.

**`.ba`** — trước/sau cạnh nhau từ 900px: `<div class="before">` viền trên đỏ,
`<div class="after">` viền trên xanh, mỗi bên mở đầu bằng `<div class="lbl">`.

**`.amp`** — dải khuếch đại số: các `.n` (thêm `.hot` cho ô cuối) xen `.ar` làm mũi tên.

**`.eyebrow`** — nhãn nhỏ in hoa trên tiêu đề. **`.big{hot|ok}`** — số nổi trong dòng văn, dùng
tiết chế.

## Icon

`ic-zap ic-warn ic-err ic-ok ic-info ic-clock ic-cpu ic-monitor ic-server ic-branch ic-activity
ic-search ic-layers ic-list ic-eye ic-net ic-expand ic-shrink ic-sun ic-moon`

## Kiểm màu

`scripts` không có trong kit này — dùng `~/.claude/skills/dataviz/scripts/validate_palette.js`
(contrast WCAG + CVD OKLab) trước khi đổi bất kỳ accent nào. Chi tiết lệnh ở `../references/design-rules.md`.

## Nguồn gốc

Preset gốc "Cà phê sữa" do Huy chốt, dùng lần đầu ở báo cáo LP-167 (17/08/2026) — 1 theme cố định.
**24/08/2026: đổi hẳn sang 2 theme** (Solarized Light / Dracula) + nút đổi tay + component sơ đồ vẽ
tay thay mermaid cho file tĩnh trong repo — lý do đầy đủ ở `../references/design-rules.md`. Bảng màu 2 theme tra từ
nguồn chính thức (draculatheme.com/spec, ethanschoonover.com/solarized), không tự chỉnh lệch.

## Lớp infographic (thêm 03/09/2026) — `diagram.css` + `steps.js` + `gif.py`

| Component | Dùng để |
|---|---|
| `.poster` + `<span class="hl">` | tiêu đề kiểu poster, khối màu đặc sau cụm từ trọng tâm (1 lần/trang) |
| `.panels` › `.panel.<cat>` › `.panel-hd`/`.panel-bd`/`.panel-note` | lưới N ô, mỗi ô một thanh tiêu đề màu + sơ đồ con |
| `.nd.<cat>` (+ `.lg .sm .row .round .gate`) | node có icon, TỰ CO theo chữ nên không bao giờ tràn |
| `<span class="step">N</span>` | badge số cắm góc trên-trái node hoặc `.grp` |
| `.grp` + `.grp-tab` | khung nhóm có nhãn |
| `.arw` / `.arw.r` (+ `.dashed .fb .ok .no`, `<span class="lbl">`) | mũi tên có nhãn giữa 2 node |
| `.stepped` + `data-step` + `data-label` | sơ đồ hé dần từng bước, `steps.js` tự dựng thanh điều khiển |

`<cat>`: `fe` client · `be` service · `db` dữ liệu · `infra` hạ tầng · `sec` bảo mật/chặn ·
`warnc` rủi ro · `model` suy luận · `ext` ngoài phạm vi. Tên theo **vai trò**, không theo màu.

Icon: 97 icon Lucide (MIT) trong `sprite.html`, dùng `<svg class="i"><use href="#ic-db"/></svg>`.
Thêm icon mới: sửa dict `ICONS` trong `build_sprite.py` rồi chạy lại nó.

Xuất GIF/MP4 cho feed:
```bash
python3 gif.py trang.html --figure "#id-so-do" --steps 6 --out ra.gif --size 1000x0
```

## Giao cho Huy

Không đưa `file://` — anh ấy nối vào bằng VS Code Remote SSH nên đường dẫn file vô nghĩa với máy anh. Copy trang vào `~/reports/<việc>/` rồi đưa link `http://100.95.154.119:8777/<việc>/trang.html`. Chi tiết ở `../SKILL.md` mục "Giao kết quả".
