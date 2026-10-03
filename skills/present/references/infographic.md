# Infographic layer and stepped diagrams / GIF export

Read when a page needs small inline node flows (`kit/diagram.css`), a diagram that reveals step by
step (`kit/steps.js`), or a GIF/MP4 of one (`kit/gif.py`). A concept explained at a glance goes on
a drawing sheet instead (`templates/sheet/`). `$K` is this skill's base directory.

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

Add an icon: edit the `ICONS` dict in `kit/build_sprite.py`, then re-run it.

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
