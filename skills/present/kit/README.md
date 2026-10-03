# present kit — reading room: paper / deep green

Default style for every HTML page built with this skill. Kit này thuộc skill `present` —
quy trình và luật nằm ở `../SKILL.md`, lý do và catalogue lỗi ở `../references/design-rules.md`.
File này chỉ là tham chiếu component + token.

```bash
python3 $K/kit/build.py body.html out.html --title "Tên Trang" \
  --shot /tmp/shot.png --shot-size 1500x3000   # rồi MỞ ẢNH RA XEM
```

| File | Nội dung |
|---|---|
| `build.py` | Ghép + kiểm. Thoát khác 0 là có lỗi, đừng publish |
| `fonts.css` | Inter 400–700 + Fira Code 400–600 + Newsreader 400–600 (display serif), embedded as data URIs with the Vietnamese subset |
| `tokens.css` | ~28 token màu (2 theme) + kiểu chữ + toàn bộ component gốc + nút đổi theme |
| `components.css` | `.fig` `.ba` `.amp` `.big` `.flow-edge` `.flow-pulse` — bổ sung cho tài liệu có sơ đồ |
| `fullscreen.css` + `fullscreen.js` | Nút và lớp phủ xem sơ đồ toàn màn hình (dùng chung cho mermaid VÀ svg vẽ tay) |
| `theme-toggle.js` | Bấm đổi sáng/tối, lưu `localStorage`, luôn thắng `prefers-color-scheme` |
| `sprite.html` | 20 icon, dùng qua `<svg class="i"><use href="#ic-…"/></svg>` |
| `overlay.html` | Khung lớp phủ — `build.py` tự cắm |

## Color tokens: two themes, same variable names

Default page palette since 2026-10-03 (style W1). Paper is `:root`. Deep green is
`:root[data-theme="dark"]`, or automatic under `prefers-color-scheme:dark` until the user forces
light. Every text colour clears 4.5:1 on its paper (`validate_palette.mjs`); change none without
re-running it.

| Role | Paper | Deep green |
|---|---|---|
| Page / card / inner / subtle | `#f3f1e8` `#f9f7f0` `#f3f1e8` `#e4e9d8` | `#14241a` `#1a2e21` `#142519` `#223a2b` |
| Panel / code body / code header (deep green in both) | `#1f3b2c` `#18301f` `#132619` | `#1f3b2c` `#0f1d14` `#0b170f` |
| Text heading / body / muted / subtle | `#1c2620` `#3a443d` `#646b62` `#9aa096` | `#ecefe4` `#d3d9cc` `#93a597` `#5f7465` |
| `--red` broken · `--yellow` risk · `--green` verified | `#b3412a` `#8a6400` `#2f6b47` | `#ef9a7a` `#e3c76a` `#cde98d` |
| `--blue` info · `--cyan` · `--violet` · `--magenta` · `--orange` | `#2b5c8a` `#2a6f75` `#6b4c9a` `#a23b6b` `#a65a1c` | `#9cc7e8` `#8fc9b0` `#bba6e6` `#e8a0c4` `#e9a66b` |

`--on-dark-*` (text on the always-green panel / code block) is declared once for both themes.
`--serif` is the display face (h1, h2, `.metrics .v`); `--sans` is the body; `--mono` is for
eyebrows, table heads and code.

**Mọi rgba/tint trong component đi qua `color-mix(in srgb, var(--x) N%, transparent)`, không
hardcode hex** — đây là điều dễ quên nhất khi thêm component mới; hardcode là component đó sẽ "kẹt"
ở 1 theme dù `:root` đã đổi.

## Component

**Khung trang** — `<header class="hdr">` (masthead on paper: mono `.eyebrow` + serif `h1`, one rule below) rồi `<main>`
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

Validator nằm ngay trong kit — `node kit/validate_palette.mjs "#hex,…" --mode light --surface "#f8fafc" --pairs all`
(contrast WCAG + CVD OKLab) trước khi đổi bất kỳ accent nào. Chi tiết lệnh ở `../references/design-rules.md`.

## Nguồn gốc

Original "Cà phê sữa" preset, first used in an early report (2026-08-17) — one fixed theme.
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

## Delivering to the user

Do not hand over `file://` if the user connects remotely — see `../SKILL.md`, "Delivery gate", item 4.
