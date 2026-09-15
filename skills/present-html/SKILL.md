---
name: present-html
description: Build any HTML page for Huy — technical report, postmortem, spec, memo, one-pager, dashboard, diagram page — whether it is published as an Artifact or lives as a file in a repo. Use whenever the output is .html/.css, whenever an analysis or report is being turned into a page, whenever a diagram needs drawing, and when Huy says "xuất ra HTML", "làm báo cáo HTML", "trang HTML", "present html", or asks for a page to be prettier. Owns the 2-theme kit (Slate Light / Dracula), the embedded Vietnamese-capable fonts, the hand-drawn SVG diagram rules, and the mandatory render-and-look check before anything is handed over.
---

# present-html

Huy reads these pages to sync technical knowledge — bright office, dimmer at home, sometimes
forwarded to his lead or to QA. One kit, two themes, no invented palettes. His word > this kit >
my taste.

Everything lives in `~/Projects/EEP/skills/present-html/kit/` (`~/.claude/assets/html-kit` is a symlink
kept for older references).

## Fast path

Write a **fragment** — `<header class="hdr">` plus `<main>` holding `<section class="card">`
blocks — then build, then look at it:

```bash
K=~/Projects/EEP/skills/present-html/kit
python3 $K/build.py body.html out.html --title "Short Distinctive Noun" \
  --shot /tmp/shot.png --shot-size 1500x3000
python3 $K/build.py body.html out.html --title "…" --shot /tmp/dark.png --shot-theme dark
```

`build.py` embeds fonts + tokens + components + diagram layer + 97 Lucide icons + fullscreen overlay
+ theme toggle + `steps.js`, pins mermaid directives, **validates, then writes atomically**.
Component reference: `kit/README.md`. Design laws and the catalogue of bugs that produced them:
`references/design-rules.md`. Regenerate the icon sprite with `kit/build_sprite.py`.

## Delivery gate — all four, every time

1. **`build.py` exits 0.** A non-zero exit is never success and never gets described as one. Fix
   the fragment; do not work around the validator.
2. **Open the screenshot and actually look at it.** Reading your own markup is not verification.
   The Chrome extension refuses `file://`, which is exactly how a page with smeared diagram text
   got delivered once — `--shot` exists so that can't happen again. Check: text inside its box,
   nothing overflowing, Vietnamese diacritics, the sans/mono split, spacing.
3. **Check the dark theme too** (`--shot-theme dark`). Category colors must keep their meaning in
   both; contrast may change, meaning may not.
4. **Never counterfeit a fit.** Not with `overflow:hidden`, not by clipping, not by an inner
   scroller, not by shrinking type below the floor. Cut words or widen the box. (Rule borrowed
   verbatim in spirit from archify, which names this failure explicitly.)

Need computed styles rather than pixels: `python3 -m http.server` in the directory and drive
`http://localhost:PORT/out.html` with the Chrome extension — `http://` is allowed, `file://` is not.

## Giao kết quả bằng LINK HTTP, không bao giờ bằng đường dẫn file

Huy ngồi ở máy khác, nối vào máy này qua **VS Code Remote SSH**. Với anh ấy, `file:///Users/Leo/...`
là vô nghĩa hai lần: browser máy anh không thấy ổ đĩa máy này, còn VS Code thì bắt lấy đường dẫn và
mở bằng **editor** chứ không phải browser. Đưa `file://` là giao một thứ không mở được — đã xảy ra
03/09/2026.

**Luật:** mọi trang HTML giao cho Huy đều đi kèm một URL `http://…` mở được ngay, không phải đường
dẫn file. Thứ tự ưu tiên:

1. **URL tailnet (mặc định, đã dựng thường trực 04/09/2026).** `~/reports` được phục vụ liên tục
   trên cổng 8777, bind vào IP tailnet của máy này. **Chỉ cần copy file vào `~/reports/` là có
   link ngay**, không phải mở server gì nữa:

   ```
   http://100.95.154.119:8777/<đường-dẫn-trong-reports>
   ```

   Mở được từ máy Windows của Huy, điện thoại, mọi thiết bị trong tailnet — không lộ ra internet.
   Tên MagicDNS `mac-mini.tail978c61.ts.net:8777` cũng có thể chạy tuỳ thiết bị, nhưng **IP là thứ
   luôn đúng, đưa IP**. Sắp xếp: mỗi việc một thư mục con
   (`~/reports/html-samples/`, `~/reports/<tên-việc>/`); gốc chưa có index nên trình duyệt hiện
   danh sách thư mục — đủ dùng, đừng dựng thêm gì.

   | Việc | Lệnh |
   |---|---|
   | Kiểm còn sống | `curl -sS -o /dev/null -w "%{http_code}" http://100.95.154.119:8777/` |
   | Xem log | `tail ~/reports/.serve.log` |
   | Dựng lại | `launchctl kickstart -k gui/$(id -u)/ai.trivita.reports` |

   Cơ chế: LaunchAgent `ai.trivita.reports` (`~/Library/LaunchAgents/ai.trivita.reports.plist`)
   chạy `~/reports/.serve.sh`, `KeepAlive` nên bị giết là tự lên lại trong ~15s (đã thử: giết pid,
   15s sau có pid mới, HTTP 200). Script đọc IP tailnet mỗi lần chạy chứ không ghi cứng — Tailscale
   chưa lên thì thoát để launchd gọi lại. Agent chạy ở phiên đăng nhập, nên máy reboot mà chưa ai
   đăng nhập thì chưa có server.
2. **`http://localhost:8777` + port forward của VS Code** — dùng khi Tailscale trục trặc. Cần thêm
   một tiến trình nữa bind vào `127.0.0.1` (hai server, hai địa chỉ, cùng cổng 8777 là hợp lệ). Nói
   Huy kiểm tab **PORTS** cạnh tab TERMINAL, hoặc `ssh -L 8777:127.0.0.1:8777`.
3. **Đừng** bind `0.0.0.0`. Nó phơi tài liệu nội bộ ra toàn bộ LAN của máy này. Bind đúng địa chỉ
   cần dùng: IP tailnet cho tailnet, `127.0.0.1` cho SSH forward.
4. **Đừng đẩy lên host công khai** (Vercel / Netlify / Cloudflare Pages / trycloudflare) nếu Huy
   chưa đồng ý *cho đúng trang đó*. Các trang này thường chứa endpoint nội bộ, tên service, số liệu
   hệ thống — Tailscale cho đúng thứ cần (xem được ở mọi nơi) mà không phải xuất bản gì ra ngoài.

Đường dẫn file vẫn nên nói kèm, nhưng là **phần phụ**, để anh ấy biết file nằm đâu mà `scp` hay mở
trong editor — không phải cách để xem.

## Non-negotiables

- **Never invent a palette.** Slate Light (Tailwind slate + 600-step accents, the set archify strokes with) at `:root`, Dracula at `[data-theme="dark"]` and under
  `prefers-color-scheme:dark`. Every component reads `var(--x)`; tints go through
  `color-mix(in srgb, var(--x) N%, transparent)` — a hardcoded `rgba()` freezes that layer in one
  theme. Verify any accent change with
  `node ~/Projects/EEP/skills/present-html/kit/validate_palette.mjs "#hex,…" --mode light --surface "#bg" --pairs all`.
- **Always embed the fonts.** `--no-fonts` is for a throwaway preview only. Inter and Fira Code are
  not installed on this Mac; `fonts.css` carries the Vietnamese unicode-range subset
  (`U+1EA0-1EF9`, `U+0102-0103`, `U+01A0-01B0`…) that makes diacritics sit correctly. 1 MB per file
  is the right trade. Regenerate with `kit/embed_fonts.py` if the subset ever needs changing.
- **A badge or alert always carries text**, never a bare colored dot — orange/amber sit at ΔE76 21.9,
  the closest pair in the set; text makes the category unambiguous regardless.
- **Wide content gets its own `overflow-x:auto` box** (`.tw` for tables). The page body never
  scrolls horizontally.
- **Title is a short distinctive noun.** `9 Tool Trong Graph, 6 Tới Model`, not
  `Tool Calling Status Report`. No explainer after a dash — that goes in the publish description.

## Diagrams

**Architecture, workflow, sequence, data-flow, lifecycle → archify first.** Run the archify skill to
produce the diagram, then embed its SVG in a `<figure class="fig">` (same palette family, so it
sits on the page without re-colouring); present-html only lays out the page around it. Hand-drawn
SVG stays for the small inline ones — a 3-box flow, a timeline strip — where archify's schema is
more ceremony than the drawing.

Hand-drawn SVG for anything living in a repo. Mermaid **only** when the page is certainly published
through the Artifact tool — the mermaid runtime doesn't exist in a static file, so `<pre
class="mermaid">` renders as raw text, and mermaid bakes color in at render time so it can't follow
the theme toggle. Details and the mermaid palette: `references/design-rules.md`.

Four SVG rules the kit enforces so they can't be forgotten:

| Rule | Why | Enforcement |
|---|---|---|
| No `font-family=` inside SVG | Inter/Fira Code only exist when embedded; a hand-written stack lands on Helvetica/Courier | `build.py` fails the build |
| Never let `stroke` reach `<text>` | `<g stroke="currentColor" stroke-width="1.5">` outlines every glyph — text goes bold and mushy, tone marks fuse into the letter | `components.css` pins `stroke:none;paint-order:fill` |
| 11px floor | Below that it is metadata, not prose | `build.py` fails the build |
| `currentColor` for strokes, one token accent | Follows the theme with no re-render | review |

Monospace inside a diagram: `class="m"`. That is the only typeface switch available, on purpose.
Wrap in `<figure class="fig">` + `<figcaption class="fig-cap">`, keep `role="img"` and an
`aria-label` that matches the caption; `build.py` adds the fullscreen button itself.

## Infographic layer — khi trang cần "đọc như một tấm poster"

Thêm 2026-09-03 sau khi Huy đối chiếu với ByteByteGo / các infographic trên LinkedIn. Toàn bộ
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
python3 $K/gif.py trang.html --figure "#luong" --steps 6 --out /tmp/luong.gif --size 1000x0
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
