# Design rules, and the bugs that produced them

Read when changing the kit itself, adding a component, or deciding how a page should look.
Operational steps are in `../SKILL.md`; component syntax is in `../kit/README.md`.

## Where the kit came from

- **2026-08-17** — first preset ("Cà phê sữa"), one fixed light theme, used on the LP-167 report.
- **2026-09-15** — light theme swapped to **Slate Light** (Tailwind slate grounds, 600-step accents = archify's stroke set) because Solarized beige read as dull beside archify pages; dark stays Dracula. `.panel-hd` moved from saturated bar to 16% tint + heading text + 2px accent rule, since no single text colour clears 4.5:1 on all eight 600-step accents.
- **2026-08-24** — retired that for **two committed themes**, Solarized Light (default) and Dracula,
  switched by a button in the header independent of the OS. Reason: Huy reads these across
  different lighting, and needs to switch on the spot rather than wait on an OS setting. Palettes
  taken from the official sources (ethanschoonover.com/solarized, draculatheme.com/spec), not
  hand-adjusted.
- **2026-09-03** — the kit became this skill. Font embedding made mandatory, SVG text rules added
  and enforced in `build.py`, screenshot verification added, six design laws adopted from archify.

## Six laws taken from archify

Source: `github.com/tt-a1i/archify` — its `DESIGN.md` and `archify/SKILL.md`, read 2026-09-03.
Archify is an agent skill that renders validated architecture diagrams as one self-contained HTML
file; different product, same genre, and its rules are sharper than anything I would have written.
The palette stays ours — these are laws, not colors.

1. **Flat-at-Rest.** A card or control at rest uses border and tone. A shadow must express layering
   or state (overlay, focus, drag). Decorative shadow is banned.
2. **Legibility Floor.** Small type is metadata, never prose. If the reader has to parse a
   *sentence*, promote it to body size. Enforced at 11px inside diagrams; apply the same judgement
   to `.fig-cap`, `caption`, `.metrics .l`.
3. **Semantic color.** Each saturated color carries one fixed meaning document-wide and is never
   reused decoratively. Binding for this kit:
   `--red` broken/blocked · `--yellow` risk or drift · `--green` verified ·
   `--blue`/`--cyan` neutral info · `--violet`/`--magenta` held in reserve — do not spend them on a
   fourth flavour of "important".
4. **Theme Parity.** A theme variant may change material and contrast but must preserve category
   identity: red is still the broken thing in Dracula. Check with `--shot-theme dark`.
5. **Canonical Clean.** Interactive-only chrome (hover, focus ring, the fullscreen button) belongs
   to the live view, not to a static export. Strip it at export time rather than designing around
   it.
6. **No AI-interface clichés.** Archify names them and is right: dense dashboard shells, endless
   identical card grids, decorative glassmorphism, gradient text. Also theirs, and worth repeating:
   never build a "Mermaid beautifier" — changing a theme without improving the information
   architecture is not a diagram.

Two more of archify's, adapted to our delivery step and already in `SKILL.md`: *a non-zero exit can
never be described as success*, and *never counterfeit a pass with `overflow:hidden`, clipped
content, an internal scroller, a stretched SVG height, or smaller typography*.

**What NOT to copy from archify:** it ships zero embedded font bytes and gambles on the system stack
(`JetBrains Mono` → `SFMono-Regular` → `Consolas`…), appending OS-native CJK families for Chinese.
Fine for their audience; wrong here — see the font failure below. Their per-node JSON IR plus schema
validators (431 KB of compiled validators) is also far past what a hand-authored report page needs;
the idea worth keeping is only the *validation contract*, which `build.py` already carries at the
right scale.

Motion, if any: 140–200 ms for state changes, and meaning never lives only in motion — a still frame
must carry the same information. `prefers-reduced-motion` is already handled in `tokens.css`, so
`.flow-edge` / `.flow-pulse` switch themselves off.

## Failure modes that actually happened

Each of these shipped or nearly shipped. The kit now blocks them; the entry stays so the reasoning
survives.

**Diagram text rendered as a bold smear (2026-09-03, delivered to Huy, he had to report it).**
Two independent causes stacked. First, the SVG was drawn as `<g fill="none" stroke="currentColor"
stroke-width="1.5">` and `<text>` inherits `stroke` — every glyph got a 1.5px outline, and Vietnamese
tone marks fused into the letter bodies. Second, the page was built with `--no-fonts` while the SVG
hardcoded `font-family="Inter, sans-serif"`; neither Inter nor Fira Code is installed on this Mac,
so diagram text fell to Helvetica/Courier while the body text fell to SF Pro — three typefaces on
one page. Fix: `components.css` pins `stroke:none` and `font-family:var(--sans)` on SVG text,
`build.py` rejects any `font-family=` inside SVG, and `--no-fonts` is now preview-only.

**`write_file` rendered as `WRITE_FILE` (same day).** `.alert .h`, `.eyebrow`, `.badge`, `thead th`
are `text-transform:uppercase`; a `<code>` identifier inside one of them silently became a different
identifier. Fix: `text-transform:none;letter-spacing:0` for `code` in those contexts.

**A label 58 characters wide in a 320px box.** Inter at 11px averages ~5.6px per character; nothing
in the toolchain warns about SVG overflow. Only the rendered screenshot catches it. Cut the words —
never the type size.

**Believing the markup instead of the render.** The Chrome extension refuses `file://`, so for a
while there was no way to see the page and "validator green" was mistaken for "looks right". Chrome
headless opens `file://` fine; `build.py --shot` now does it, and looking at the PNG is part of the
delivery gate rather than an optional extra.

**Chụp "light" ra ảnh tối (2026-09-03).** `shoot()` chỉ ép `data-theme` khi chụp dark, còn light thì
phó mặc `prefers-color-scheme`. Chiều muộn macOS tự sang dark, ảnh "light" ra tối mà không báo gì.
Giờ ép cả hai chiều. Bài học chung: **không bao giờ để nhánh mặc định là "không làm gì"** khi cái
"không làm gì" đó phụ thuộc trạng thái máy.

**Sơ đồ chạy theo bước làm ảnh tĩnh mất 5/6 nội dung (2026-09-03).** Ảnh chụp bắt đúng bước 1, phần
còn lại ở opacity .16 — vi phạm chính cái luật "khung tĩnh phải mang đủ thông tin" viết ở trên. Sửa:
`?still=1` mà không kèm `step=N` nghĩa là **hiện trọn mọi bước**, và `build.py --shot` luôn tải
trang với `?still=1`. `gif.py` thì luôn kèm `step=N` nên vẫn hé dần bình thường.

**`clip-path` cắt mất viền node (2026-09-03).** Định làm node hình thoi cho cổng quyết định bằng
`clip-path: polygon(...)`; clip-path cắt cả `border`, node mất khung. Không có cách nào giữ viền
với clip-path. Bỏ hình thoi: cổng quyết định giờ báo bằng **viền gạch dày + icon**, nghĩa vẫn rõ mà
không có bug hình học.

**Chữ trắng trên thanh màu Solarized chỉ đạt 2.6:1 (2026-09-03).** `.panel-hd` ban đầu dùng
`color: var(--bg-page)` (kem) trên `--green` #859900 — không đọc được ở theme sáng. Đổi sang chữ
`var(--bg-code)` (tối ở cả hai theme): mọi category vượt 4.2:1 với chữ bold 15px, mà thanh vẫn giữ
màu bão hoà đúng kiểu infographic.

**Lucide có comment license trước `<svg>` (2026-09-03).** Script sinh sprite cắt phần trong bằng
`split(">", 1)` — dấu `>` đầu tiên nằm ở cuối comment, nên cả thẻ `<svg>` bị lồng vào trong
`<symbol>`, ra 98 thẻ mở / 1 thẻ đóng. `build.py` bắt được nhờ đếm thẻ. Cách đúng: xoá comment rồi
regex `<svg\b[^>]*>(.*)</svg>` với DOTALL. Cũng nhân đây sửa một lỗi thật của validator: phần kiểm
`<use href="#…">` soi trên `lean` (còn nguyên script) nên báo icon ảo do `steps.js` nối chuỗi động —
giờ soi trên `bare`.

**Giao trang bằng `file://` cho người ngồi ở đầu kia SSH (2026-09-03).** Năm trang mẫu giao xong,
Huy click không mở được: anh ấy nối vào bằng VS Code Remote SSH, `file://` trỏ vào ổ đĩa máy này chứ
không phải máy anh, và VS Code mở nó bằng editor. Sửa: mọi trang giao kèm URL HTTP qua tailnet
Tailscale — xem `SKILL.md` mục "Giao kết quả". Bài học rộng hơn: **đường dẫn chỉ có nghĩa trên máy
sinh ra nó**; thứ giao đi phải là địa chỉ mà người nhận mở được từ chỗ họ đang ngồi.

## Mermaid, if it is ever the right choice

Only inside an Artifact. In a static repo file the runtime does not exist and `<pre class="mermaid">`
shows as raw text (verified in a real browser, Trivita Law `docs/spec/`, 2026-08-24). Mermaid also
bakes color into the SVG at render time, so it cannot follow the theme button — which is why the
Artifact viewer's single light theme is the only context where it is safe:

```
classDef hot   fill:#F1DCD2,stroke:#B02A1E,stroke-width:3px,color:#120B03,font-weight:700
classDef warn  fill:#F8EEDC,stroke:#75530A,color:#2B1E10
classDef ok    fill:#EAEFD9,stroke:#4C5A0B,color:#2B1E10
classDef info  fill:#DEE9F1,stroke:#175A87,color:#2B1E10
classDef concl fill:#EFE3CF,stroke:#6F4522,stroke-width:3px,color:#120B03,font-weight:700
```

Never a dark fill in a mermaid diagram: mermaid infers text color from background lightness and
infers it wrong. `gantt` has three text-color variables (`taskTextColor`, `taskTextDarkColor`,
`taskTextLightColor`) and there is no telling which it picks — `build.py` sets all three dark and
the bar light. Do not change that back.

## Open question, unverified

Whether `localStorage` keeps the theme choice across different files opened over `file://` depends
on whether the browser coalesces the `file://` origin. Do not assume either way; check by hand when
there is a chance.
