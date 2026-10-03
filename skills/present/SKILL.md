---
name: present
description: Turn an explanation into something a person can see — an HTML page (report, postmortem, spec, memo, interactive explorable), a diagram (drawing sheet for explaining a concept; archify for architecture/stack), or a narrated 3Blue1Brown-style explainer video — plus the 80%-STE prose register those artifacts use. Use whenever the output is .html/.css or .mp4, whenever an analysis or report is being turned into a page, whenever a diagram or explainer is needed, and when the user asks to "export as HTML", "make a video", "explain this visually", or for a page to be prettier. Owns the style catalogue and asks the user to pick a style before building (writing A/B/C, pages W1 reading room / W2 sheet explorable, diagrams D1 drawing sheet / D2 archify, video V1 3b1b / V2 inked sheet), the embedded Vietnamese-capable fonts, the SVG rules, and the mandatory render-and-look check.
---

# present

Every style below came out of one same-topic sample round (2026-10-03). **Fewer words** was
half the brief: labels and numbers over paragraphs, let the visual or the interaction carry it.

## Ask the style first, then cook

Before building anything, ask the user which style to use, with `AskUserQuestion`: one
question per output type the request needs (at most 4), options from the catalogue below, the
default first and marked "(Recommended)". If the user's private sample gallery is in memory,
link it in the question text so they can compare. Skip the question only when the user already
named a style in this request or in this conversation.

| Type | Style | Look | Start from |
|---|---|---|---|
| Writing | **B, 80% STE** (default) | answer first, ≤20–25 words, plain words, jargon glossed once | **Writing** below |
| | A, strict STE | ASD-STE100 limits, numbered sections, CAUTION before the step | **Writing** below |
| | C, dense engineering | terse, no sentence limit, symbols inline | **Writing** below |
| Page / explorable | **W1, reading room** (default) | cream paper + serif, deep green dark, TOC + question cards + interactive panel | `kit/build.py` (plain page) · `templates/explorable/` |
| | W2, drawing-sheet explorable | the same interactions inside a zone-ruled sheet with a title block | `templates/explorable-sheet/` |
| Diagram, a concept | **D1, drawing sheet** (default) | lettered panels, zone ruler, title block; white / blueprint | `templates/sheet/` |
| Diagram, architecture / stack | **D2, archify** (default) | lanes + arrows | the `archify` skill; example `templates/archify/kv-decode.workflow.json` |
| Video | **V1, 3b1b** (default) | manim palette on black, STIX serif math | `templates/video/kv-cache.src.html` |
| | V2, drawing sheet inked live | the sheet look, panels drawn in as the voice speaks | `templates/video/kv-cache.sheet.src.html` |

Each template ships the KV-cache worked example. Copy it, replace the content, keep the
structure. Prose anywhere in these follows the chosen **Writing** style.

## Writing

Applies to prose *inside* present artifacts, not to chat replies. Default **B, 80% of the way to
ASD-STE100**:
- Answer first: one line that says the whole thing.
- One idea per sentence. Most sentences stay ≤20 words; descriptive ones may reach 25.
- Active voice. Same word for the same thing every time.
- Ordinary vocabulary and "because" are allowed; STE's approved dictionary is not required.
- Keep jargon, but gloss it once on first use.
- Check with `python3 kit/ste_check.py FILE --max 25`. It exits 1 and lists every sentence over the limit.
- Vietnamese prose: STE is an English spec. Use `eep:vietnamese-writing` instead.

**A, strict STE**: B's limits (procedure ≤20 words, description ≤25) plus approved-dictionary words
where known, numbered sections (Function, Operation, Procedure), and `CAUTION:`/`WARNING:` before
the step it protects. **C, dense engineering**: no sentence limit, symbols and `i.e.` inline,
jargon glossed once. Fastest to write and slowest to read.

## Build

```bash
K=${CLAUDE_PLUGIN_ROOT}/skills/present
python3 $K/kit/build.py body.html out.html --title "Short Distinctive Noun" \
  [--css $K/templates/explorable/explorable.css | --css $K/templates/sheet/sheet.css] \
  --shot shot.png --shot-size 1920x3000 [--shot-theme dark]
```

`build.py` embeds the fonts (Inter, Fira Code, and Newsreader for display, all with the Vietnamese
subset), tokens, components, icons, the fullscreen overlay, the theme toggle and `steps.js`. It
**validates first, then writes atomically**. Every page must be able to switch to its dark
theme; the build fails without a toggle. It inserts one into `.hdr` or `.toc-ft` itself. A
sheet carries `class="theme-toggle flip"` in its title block.

Video has its own pipeline (`templates/video/README.md`): `say` narration → `render(t)` page →
headless Chrome frames → ffmpeg. Look at stills before the full render.

## The palettes

- **Reading room** (`kit/tokens.css`): cream paper + Newsreader display serif + mono eyebrows. Dark =
  deep green. The interactive panel and code blocks are deep green in both themes. Semantic colors
  keep one meaning each: red broken/cost, yellow risk, green verified, blue info.
- **Drawing sheet** (`templates/sheet/sheet.css`): white paper, near-black ink, one drafting blue
  for annotation, one red for cost / not-approved. Dark = blueprint. Used by D1, W2 and V2.
- **W2 / V2** reuse the drawing-sheet palette with IBM Plex. W2 is light only as sampled: add the
  blueprint dark from `templates/sheet/sheet.css` before delivery.
- **Video V1**: manim's palette and its black background (`templates/video/kv-cache.src.html` cites
  the source file). On screen: math, numbers, and 1–3-word labels only.

Never invent a new palette. A change to an existing one is re-validated with
`node kit/validate_palette.mjs "#hex,…" --surface "#paper" --mode light|dark`: every text color
must clear 4.5:1 on its paper. Tints go through `color-mix(in srgb, var(--x) N%, transparent)`.

## Delivery gate: all of these, every time

1. **The build exits 0.** A non-zero exit is never success. Fix the input; do not route around
   the validator.
2. **Look at the screenshot, in both themes.** Reading your own markup is not verification.
   Check that text sits inside its box, nothing overflows, Vietnamese diacritics render, and the
   type is right. For an explorable, also screenshot one interacted state (drive it with a URL
   parameter). For a video, extract 3–4 frames and check each against what the narration says
   at that moment.
3. **Never counterfeit a fit.** No `overflow:hidden`, no clipping, no inner scroller, no type
   below 11px. Cut words or widen the box.
4. **Serve it and open it yourself.** Put it in a dated subfolder of the folder the user's
   private-network static server publishes. The base URL and folder are in memory; if not, ask
   once. Then run `open "<http-url>"` so it is already on their screen; for several pages, open
   the index. A `file://` path is not a delivery. No server: `python3 -m http.server` on
   `127.0.0.1` plus a port-forward.
   Never bind `0.0.0.0` and never push to a public host without explicit go-ahead. Mention the
   file path as a secondary detail.

## SVG rules (enforced by build.py)

| Rule | Why |
|---|---|
| No `font-family=` inside SVG | the embedded fonts only exist through CSS; a hand-written stack lands on Helvetica |
| `stroke` never reaches `<text>` | `<g stroke=…>` outlines every glyph; tone marks fuse into letters |
| 11px floor | below that it is metadata, not prose |
| `currentColor` strokes; `<text>` without `fill` follows the theme | no re-render on theme switch |

Monospace inside a diagram: `class="m"`. Wrap in `<figure class="fig">` + `<figcaption
class="fig-cap">`, with `role="img"` and an `aria-label` that matches the caption. Mermaid only
when the page is certainly published through the Artifact tool. Design laws and the bug
catalogue: `references/design-rules.md`.

## Infographic layer — khi trang cần "đọc như một tấm poster"

> Since 2026-10-03: a concept explained at a glance goes on a **drawing sheet**, not a poster.
> This layer is for small inline node flows inside a page.

Thêm 2026-09-03 after comparing against ByteByteGo / các infographic trên LinkedIn. Toàn bộ
nằm trong `kit/diagram.css`, không cần lib ngoài.

| Muốn gì | Dùng gì |
|---|---|
| Tiêu đề kiểu poster, có khối màu đặc sau cụm từ trọng tâm | `.poster` + `<span class="hl">` (dùng **một lần** mỗi trang) |
| Lưới N ô, mỗi ô một thanh tiêu đề màu + sơ đồ con | `.panels` › `.panel.<cat>` › `.panel-hd` (`.n` = số thứ tự) + `.panel-bd` + `.panel-note` |
| Node có icon, tự co theo chữ | `.nd.<cat>`, thêm `.lg`/`.sm`/`.row`; `.round` cho model, `.gate` (viền gạch) cho chỗ rẽ nhánh |
| Badge số cắm góc node | `<span class="step">3</span>` |
| Khung nhóm có nhãn (kiểu "THE HARNESS") | `.grp` + `.grp-tab` |
| Mũi tên có nhãn giữa 2 node | `.arw` (dọc) / `.arw.r` (ngang), thêm `.dashed` `.fb` `.ok` `.no`, nhãn là `<span class="lbl">` |
| Icon | 97 icon Lucide (MIT) trong sprite: `<svg class="i"><use href="#ic-db"/></svg>` |

`<cat>` là **vai trò**, không phải màu — `fe` client · `be` service · `db` dữ liệu · `infra` hạ tầng ·
`sec` bảo mật/chặn · `warnc` rủi ro · `model` suy luận · `ext` ngoài phạm vi. Đổi theme thì màu đổi,
nghĩa không đổi.

**Vì sao node là HTML chứ không phải SVG:** hộp tự co theo chữ nên chữ không bao giờ tràn khung —
lỗi tốn thời gian nhất khi vẽ SVG tay. SVG vẫn là lựa chọn đúng cho hình *thật sự dạng graph*
(cung cong, nhánh chéo, đường quay ngược), và khi đó 4 luật SVG ở trên vẫn áp dụng.

## Sơ đồ chạy theo bước, và xuất GIF

Cái làm GIF giải thích của chuyên gia dễ hiểu không phải "có chuyển động", mà là **mỗi lúc chỉ một
thứ đổi, dừng đủ lâu để đọc, không bỏ sót bước nào**. Nên thứ cần dựng là sơ đồ *có bước*, không
phải sơ đồ có animation.

```html
<div class="stepped" id="luong" data-dwell="2000">
  <div class="nd fe" data-step="1" data-label="Bệnh nhân nói một câu"> … </div>
  <div class="arw"  data-step="1"><span class="lbl">HumanMessage</span></div>
  <div class="nd model round" data-step="2" data-label="Gọi model kèm tool schema"> … </div>
</div>
```

`steps.js` tự đếm số bước, tự dựng thanh điều khiển (◀ ▶ ⏸ + chấm tiến độ + nhãn bước), tự chạy khi
cuộn tới và dừng khi ra khỏi màn hình. `build.py` bắt lỗi nếu `data-step` không liên tục từ 1.

**Hợp đồng tĩnh — đừng phá:** CSS mặc định hiện **đủ mọi bước**; JS mới là thứ hạ bước chưa tới
xuống mờ. Không JS, bản in, `prefers-reduced-motion`, và `?still=1` đều thấy trọn thông tin. Motion
chỉ dẫn nhịp đọc, không giữ nghĩa.

Xuất ra file để dán LinkedIn/Slack:

```bash
python3 $K/kit/gif.py trang.html --figure "#luong" --steps 6 --out /tmp/luong.gif --size 1000x0
```

Nó mở chính trang đã build với `?step=N&still=1`, chụp từng bước, đo chiều cao thật của hình rồi cắt
khung vừa khít, ghép bằng ffmpeg (palettegen → paletteuse, chữ không vỡ). Ra kèm `.mp4` nhẹ hơn ~2
lần cho Slack. Vì nguồn là chính trang đó, GIF và trang không bao giờ lệch nhau. `--size` chỉ dùng
phần RỘNG; CAO luôn tự đo.

## When something new is needed

Route it into an existing surface before adding one. A new component earns its place only when no
combination of `.card` / `.alert` / `.tw` / `.code` / `.checklist` / `.fig` / `.metrics` can carry
it. If you do add one: `var()` for every color, text alongside any color signal, and add the
matching guard to `build.py` so the next mistake fails loudly instead of shipping.
