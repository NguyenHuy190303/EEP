#!/usr/bin/env python3
"""W3 showcase: report.json -> one self-contained results page, built and validated by kit/build.py.

usage: render.py REPORT.json OUT.html [--audio link|embed] [--shot PNG --shot-size WxH --shot-theme light|dark] [--no-fonts]

Every number on the page lives in REPORT.json; prose stays consistent only if the converter that
writes REPORT.json formats prose numbers from the export too (README.md).
The evidence contract (README.md) is checked here first; a missing field stops the build with a
list of every gap, nothing is written. Text fields are trusted HTML (<b> etc. allowed); example
transcripts and turn texts are data and get escaped.
"""
import argparse, base64, difflib, html, json, math, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent.parent / "kit"
sys.path.insert(0, str(KIT))
from build import THEME_BUTTON  # noqa: E402  same toggle markup the kit validates

L = {
    "vi": {"lower": "↓ Càng thấp càng tốt", "higher": "↑ Càng cao càng tốt", "none": "Số đo quy mô",
           "note": "Lưu ý:", "ref": "Đáp án", "empty": "(không ghi được gì)", "dashed": "Đường nét đứt",
           "key": "Chữ tô đỏ: khác đáp án · chữ gạch ngang: từ trong đáp án bị bỏ sót.",
           "m_kicker": "Phương pháp", "m_title": "Phương pháp và giới hạn đánh giá",
           "m_lede": "Phần dành cho người muốn xác thực con số hoặc tái lập phương pháp.",
           "defs": "Ý nghĩa các chỉ số", "run": "Chi tiết lần kiểm thử", "limits": "Giới hạn",
           "src": "Xem run gốc ↗", "turns": ["Lúc", "Đáp án", "Lời nói", "Model gán cho"],
           "report": "Báo cáo", "samples": "Mẫu kiểm tra lại", "selection": "Cách chọn mẫu:",
           "search": "Tìm theo mã hoặc lời nói", "all_groups": "Mọi nhóm", "all_status": "Đạt và chưa đạt",
           "pass": "Đạt", "fail": "Chưa đạt", "sort": ["Điểm cao → thấp", "Điểm thấp → cao", "Theo mã"],
           "shown": "mẫu đang hiện", "turns_sum": "Lời nói theo đáp án ({n} lượt) · bấm mốc giờ để nghe đoạn đó",
           "play": "Bấm vào dải màu để nghe từ chỗ đó."},
    "en": {"lower": "↓ Lower is better", "higher": "↑ Higher is better", "none": "Scale, not a score",
           "note": "Note:", "ref": "Reference", "empty": "(no output)", "dashed": "Dashed line",
           "key": "Red: differs from the reference · struck through: reference words left out.",
           "m_kicker": "Method", "m_title": "Method and limits",
           "m_lede": "For readers who want to check a number or re-run the evaluation.",
           "defs": "What the numbers mean", "run": "Run details", "limits": "Limits",
           "src": "Open the source run ↗", "turns": ["At", "Reference", "Speech", "Model said"],
           "report": "Report", "samples": "Samples to re-check", "selection": "How the samples were picked:",
           "search": "Search by id or words", "all_groups": "All groups", "all_status": "Passed and failed",
           "pass": "Pass", "fail": "Fail", "sort": ["Score high → low", "Score low → high", "By id"],
           "shown": "samples shown", "turns_sum": "Reference turns ({n}) · click a time to listen from there",
           "play": "Click a track to listen from that point."},
}
BETTER = ("lower", "higher", "none")
SHOWCASE_FONTS = ["Be+Vietnam+Pro:wght@400;600;700;800", "IBM+Plex+Mono:wght@400;600"]   # weights the CSS uses
AUDIO_MIME = {".wav": "audio/wav", ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".ogg": "audio/ogg",
              ".opus": "audio/ogg", ".webm": "audio/webm", ".flac": "audio/flac"}
esc = html.escape


class Ctx:
    def __init__(self, lang: str, base: Path):
        self.t, self.base, self.errs = L[lang], base, []
        self.audio_mode, self.audio_dir, self.copies = "link", "audio", []
        self.dec, self.thou = (",", ".") if lang == "vi" else (".", ",")

    def audio(self, src: str, where: str) -> str:
        """Audio for a player: a URL as is; a file embedded, or copied next to the page and linked."""
        if str(src).startswith(("http://", "https://")):
            return src
        p = self.base / Path(src).expanduser()
        if not p.is_file():
            self.errs.append(f"{where}: không thấy file audio {p}")
            return ""
        if self.audio_mode == "embed":
            mime = AUDIO_MIME.get(p.suffix.lower(), "audio/" + p.suffix[1:].lower())
            return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
        self.copies.append(p)   # copied by main() only after every check passed
        return f"{self.audio_dir}/{p.name}"

    def need(self, obj: dict, keys: str, where: str) -> None:
        for k in keys.split():
            if obj.get(k) in (None, "", []):
                self.errs.append(f"{where}: thiếu '{k}'")

    def better(self, obj: dict, where: str) -> str:
        b = obj.get("better")
        if b not in BETTER:
            self.errs.append(f"{where}: 'better' phải là lower | higher | none, đang là {b!r}")
            return "none"
        return b

    def fmt(self, v, digits: int = 2) -> str:
        s = f"{v:,.{digits}f}"
        return s.replace(",", "\0").replace(".", self.dec).replace("\0", self.thou)


def c(series: str | None) -> str:
    return f"var(--sc-{series or 's1'})"


def dir_chip(ctx: Ctx, b: str) -> str:
    return f'<span class="sc-dir {b}">{ctx.t[b]}</span>'


def panel_hd(ctx: Ctx, b: dict, better: str | None = None) -> str:
    right = dir_chip(ctx, better) if better and better != "none" else ""
    return (f'<div class="sc-panel-hd"><div><h3>{b.get("title", "")}</h3>'
            + (f'<p>{b["desc"]}</p>' if b.get("desc") else "") + f"</div>{right}</div>")


def legend(items: list[dict]) -> str:
    return ('<div class="sc-legend">' + "".join(
        f'<span><i class="sc-sw" style="--c:{c(i.get("series"))}"></i>{i["label"]}</span>' for i in items)
        + "</div>")


# ---------- blocks ----------

def b_kpis(b, ctx, w):
    out = []
    for i, k in enumerate(b.get("items", [])):
        ctx.need(k, "label value reading basis", f"{w}.items[{i}]")
        d = ctx.better(k, f"{w}.items[{i}]")
        out.append(f'<article class="sc-kpi tone-{k.get("tone", "brand")}"><div class="sc-kpi-hd">'
                   f'<span class="sc-eb">{k.get("label", "")}</span>{dir_chip(ctx, d)}</div>'
                   f'<div class="sc-kpi-v">{k.get("value", "")}</div><h3>{k.get("reading", "")}</h3>'
                   f'<p class="sc-basis">{k.get("basis", "")}</p></article>')
    return f'<div class="sc-grid c{b.get("cols", 2)}">' + "".join(out) + "</div>"


def bar_rows(rows, ctx, w, digits, unit, top, ref):
    out = []
    for i, r in enumerate(rows):
        ctx.need(r, "label", f"{w}.rows[{i}]")
        v = r.get("value")
        if not isinstance(v, (int, float)):
            ctx.errs.append(f"{w}.rows[{i}]: 'value' phải là số, đang là {v!r}")
            v = 0
        refl = f'<i class="sc-ref" style="left:{ref / top * 100:.2f}%"></i>' if ref is not None else ""
        note = f'<small>{r["note"]}</small>' if r.get("note") else ""
        sub = f'<small>{r["sub"]}</small>' if r.get("sub") else ""
        cls = "".join(f" {k}" for k in ("hl", "faint") if r.get(k))   # faint: too few samples to read closely
        out.append(f'<div class="sc-bar{cls}"><div class="sc-bar-l"><b>{r.get("label", "")}</b>{sub}</div>'
                   f'<div class="sc-track"><i class="sc-fill" style="width:{v / top * 100:.2f}%;--c:{c(r.get("series"))}"></i>{refl}</div>'
                   f'<div class="sc-bar-v">{r.get("text") or ctx.fmt(v, digits) + unit}{note}</div></div>')
    return '<div class="sc-bars">' + "".join(out) + "</div>"


def b_bars(b, ctx, w):
    d = ctx.better(b, w)
    groups = b.get("groups") or [{"rows": b.get("rows", [])}]
    if not b.get("basis") and not all(r.get("sub") for g in groups for r in g.get("rows", [])):
        ctx.errs.append(f"{w}: cần 'basis' (mẫu số chung) hoặc 'sub' (n, giờ) trên từng dòng")
    vals = [r.get("value") for g in groups for r in g.get("rows", []) if isinstance(r.get("value"), (int, float))]
    ref = (b.get("ref") or {}).get("value")
    top = b.get("max") or max(vals + [ref or 0, 1e-9]) * 1.12
    digits, unit = b.get("digits", 2), b.get("unit", "")
    body = []
    for gi, g in enumerate(groups):
        rows = bar_rows(g.get("rows", []), ctx, f"{w}.groups[{gi}]", digits, unit, top, ref)
        body.append(f'<div class="sc-group"><h4>{g["title"]}<small>{g.get("sub", "")}</small></h4>{rows}</div>'
                    if g.get("title") else rows)
    foot = []
    if b.get("ref"):
        foot.append(f'<b>{ctx.t["dashed"]}</b> = {b["ref"].get("label", "")}')
    if b.get("basis"):
        foot.append(b["basis"])
    return ('<div class="sc-panel">' + panel_hd(ctx, b, d) + (legend(b["legend"]) if b.get("legend") else "")
            + "".join(body) + (f'<p class="sc-foot-note">{" · ".join(foot)}</p>' if foot else "") + "</div>")


def b_stack(b, ctx, w):
    d = ctx.better(b, w)
    ctx.need(b, "parts rows", w)
    parts, rows = b.get("parts", []), b.get("rows", [])
    tot = [sum(r.get("values", {}).get(p["key"], 0) for p in parts) for r in rows]
    top = b.get("max") or max(tot + [1e-9]) * 1.12
    digits, unit, out = b.get("digits", 2), b.get("unit", ""), []
    for r, t in zip(rows, tot):
        left, segs = 0.0, []
        for p in parts:
            v = r.get("values", {}).get(p["key"], 0)
            segs.append(f'<i class="sc-fill" style="left:{left / top * 100:.2f}%;width:{v / top * 100:.2f}%;'
                        f'--c:{c(p.get("series"))};border-radius:0"></i>')
            left += v
        detail = " · ".join(f'{p["label"]} {ctx.fmt(r.get("values", {}).get(p["key"], 0), digits)}{unit}' for p in parts)
        out.append(f'<div class="sc-bar{" hl" if r.get("hl") else ""}"><div class="sc-bar-l"><b>{r.get("label", "")}</b>'
                   f'<small>{r.get("sub", "")}</small></div><div class="sc-track">{"".join(segs)}</div>'
                   f'<div class="sc-bar-v">{ctx.fmt(t, digits)}{unit}<small>{r.get("note", "")}</small></div></div>'
                   f'<p class="sc-key" style="margin:-.35rem 0 0">{detail}</p>')
    return ('<div class="sc-panel">' + panel_hd(ctx, b, d) + legend(parts) + '<div class="sc-bars">' + "".join(out)
            + "</div>" + (f'<p class="sc-foot-note">{b["basis"]}</p>' if b.get("basis") else "") + "</div>")


def table_html(head, rows, num=(), total_last=False, diag=False, caption=""):
    num_attr = ' class="num"'
    th = "".join(f"<th{num_attr if i in num else ''}>{h}</th>" for i, h in enumerate(head))
    trs = []
    for ri, r in enumerate(rows):
        tds = []
        for ci, cell in enumerate(r):
            cls = ["num"] if ci in num else []
            heat = ""
            if isinstance(cell, dict):   # {"text": "144", "heat": 0.11}: shade by a 0-1 share the author computed
                heat = f' style="background:color-mix(in srgb,var(--sc-brand) {cell.get("heat", 0) * 35:.0f}%,transparent)"'
                cell = cell.get("text", "")
            if diag and ci == ri + 1:
                cls.append("diag")
            if diag and ci and cell in ("0", 0, "", "·"):
                cls.append("zero")
                cell = "·"
            attr = f' class="{" ".join(cls)}"' if cls else ""
            tds.append(f"<td{attr}{heat}>{cell}</td>")
        last = total_last and ri == len(rows) - 1
        trs.append(("<tr class=\"total\">" if last else "<tr>") + "".join(tds) + "</tr>")
    cap = f"<caption>{caption}</caption>" if caption else ""
    return f'<div class="tw"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def b_table(b, ctx, w):
    ctx.need(b, "head rows", w)
    t = table_html(b.get("head", []), b.get("rows", []), set(b.get("num", [])), b.get("total_last", False),
                   b.get("diag", False), b.get("caption", ""))
    return ('<div class="sc-panel">' + panel_hd(ctx, b) + t + "</div>") if b.get("title") else t


def diff_marks(ref: str, hyp: str, ctx: Ctx) -> str:
    if not hyp.strip():
        return f'<mark>{ctx.t["empty"]}</mark>'
    norm = lambda s: re.sub(r"[^\w]", "", s.lower())  # noqa: E731  punctuation and case are not errors
    r, h = ref.split(), hyp.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, [norm(x) for x in r], [norm(x) for x in h],
                                                      autojunk=False).get_opcodes():
        if op == "equal":
            out.append(esc(" ".join(h[j1:j2])))
            continue
        if op in ("replace", "insert"):
            out.append(f'<mark>{esc(" ".join(h[j1:j2]))}</mark>')
        if op == "delete":
            out.append(f'<del>{esc(" ".join(r[i1:i2]))}</del>')
    return " ".join(out)


def b_examples(b, ctx, w):
    cards = []
    for i, e in enumerate(b.get("items", [])):
        ctx.need(e, "title id ref hyps", f"{w}.items[{i}]")
        rows = [f'<div class="sc-ex-row ref"><span>{e.get("ref_label", ctx.t["ref"])}</span><span>{esc(e.get("ref", ""))}</span></div>']
        rows += [f'<div class="sc-ex-row"><span>{hy["label"]}</span><span>{diff_marks(e.get("ref", ""), hy.get("text", ""), ctx)}</span></div>'
                 for hy in e.get("hyps", [])]
        sub = " · ".join(x for x in (e.get("sub"), e.get("id")) if x)
        cards.append(f'<div class="sc-ex"><div class="sc-ex-hd"><b>{e.get("title", "")}</b><small>{sub}</small></div>{"".join(rows)}</div>')
    return ('<div class="sc-panel">' + panel_hd(ctx, b) + f'<div class="sc-ex-grid">{"".join(cards)}</div>'
            + f'<p class="sc-key">{ctx.t["key"]}</p></div>')


def tl_html(tracks: list, series: dict, dur: float, t0: float = 0, tick=None) -> str:
    rows = []
    for tr in tracks:
        segs = []
        for st, en, k in tr.get("segs", []):
            st, en = max(st - t0, 0), min(en - t0, dur)   # a window into a longer recording: clip to it
            if en > st:
                segs.append(f'<i class="sc-tl-seg" style="left:{st / dur * 100:.2f}%;width:{max((en - st) / dur * 100, .25):.2f}%;'
                            f'--c:{c(series.get(k))}"></i>')
        sub = f"<small>{tr['sub']}</small>" if tr.get("sub") else ""
        rows.append(f'<div class="sc-tl-row{" thin" if tr.get("thin") else ""}"><span>{tr.get("label", "")}{sub}</span>'
                    f'<div class="sc-tl-track">{"".join(segs)}<i class="sc-ph"></i></div></div>')
    step = tick or max(1, math.ceil(dur / 8 / 5) * 5)
    axis = "".join(f'<span style="left:{t / dur * 100:.2f}%">{t}s</span>' for t in range(0, int(dur) + 1, step))
    return (f'<div class="sc-tl" data-dur="{dur}" data-start="{t0}">{"".join(rows)}</div>'
            f'<div class="sc-tl-axis">{axis}</div>')


def turns_html(turns: list, ctx: Ctx, w: str, head=None) -> str:
    for i, t in enumerate(turns):
        ctx.need(t, "t who", f"{w}.turns[{i}]")
        if "text" not in t:   # an empty string is data (no words in that turn); a missing key is a bug
            ctx.errs.append(f"{w}.turns[{i}]: thiếu 'text'")
    has_got = any("got" in t for t in turns)
    head = head or (ctx.t["turns"] if has_got else ctx.t["turns"][:3])
    when = lambda t: (f'<button type="button" class="sc-t" data-t="{t["s"]}">{esc(str(t["t"]))}</button>'  # noqa: E731
                      if "s" in t else esc(str(t.get("t", ""))))
    trs = "".join(
        f'<tr><td class="num">{when(t)}</td><td><span class="sc-who" style="--c:{c(t.get("series"))}">'
        f'{esc(t.get("who", ""))}</span></td><td>{esc(t.get("text", ""))}</td>'
        + (f'<td><span class="sc-chip{"" if t.get("ok", True) else " bad"}">{esc(t.get("got", ""))}</span></td>' if has_got else "")
        + "</tr>" for t in turns)
    return f'<div class="tw"><table><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>{trs}</tbody></table></div>'


def b_timeline(b, ctx, w):
    ctx.need(b, "title id duration tracks legend", w)
    series = {x["key"]: x.get("series") for x in b.get("legend", [])}
    tl = tl_html(b.get("tracks", []), series, b.get("duration") or 1, b.get("start", 0), b.get("tick"))
    au = f'<audio controls preload="none" src="{ctx.audio(b["audio"], w)}"></audio>' if b.get("audio") else ""
    turns = turns_html(b["turns"], ctx, w, b.get("turn_head")) if b.get("turns") else ""
    sub = " · ".join(x for x in (b.get("id"), b.get("sub")) if x)
    lw = f' style="--lw:{b["label_width"]}"' if b.get("label_width") else ""
    return (f'<div class="sc-panel"{lw}><div class="sc-panel-hd"><div><h3>{b.get("title", "")}</h3><p>{sub}</p></div></div>'
            + legend(b.get("legend", [])) + au + tl
            + (f'<p>{b["note"]}</p>' if b.get("note") else "") + turns + "</div>")


def b_insights(b, ctx, w):
    return '<div class="sc-ins">' + "".join(
        f'<article class="tone-{x.get("tone", "brand")}"><div class="sc-eb">{x.get("kicker", "")}</div>'
        f'<h4>{x.get("title", "")}</h4><p>{x.get("text", "")}</p></article>' for x in b.get("items", [])) + "</div>"


def b_composition(b, ctx, w):
    ctx.need(b, "total parts", w)
    t, parts = b.get("total", {}), b.get("parts", [])
    s = sum(p.get("value", 0) for p in parts) or 1
    share = "".join(f'<span style="width:{p.get("value", 0) / s * 100:.2f}%;--c:{c(p.get("series"))}"></span>' for p in parts)
    rows = "".join(
        f'<div class="sc-part"><i class="sc-sw" style="--c:{c(p.get("series"))}"></i><div><b>{p["label"]}</b>'
        f'<small>{p.get("sub", "")}</small></div><div class="sc-part-v">{p.get("text") or ctx.fmt(p.get("value", 0), b.get("digits", 2))}'
        f'<small>{" " + p["side"] if p.get("side") else ""}</small></div></div>' for p in parts)
    left = (f'<div><div class="sc-eb">{t.get("label", "")}</div><div class="sc-comp-big">{t.get("value", "")}<small>{t.get("unit", "")}</small></div>'
            f'<p>{t.get("caption", "")}</p>' + (f'<div class="sc-callout">{b["callout"]}</div>' if b.get("callout") else "") + "</div>")
    right = (f'<div class="sc-panel"><div class="sc-eb">{b.get("bar_label", "")}</div><div class="sc-share">{share}</div>'
             f'<div class="sc-parts">{rows}</div>' + (f'<p class="sc-key">{b["caption"]}</p>' if b.get("caption") else "") + "</div>")
    return f'<div class="sc-comp">{left}{right}</div>'


def b_quote(b, ctx, w):
    link = b.get("link")
    a = f'<a class="sc-ghost" href="{link["href"]}">{link["label"]}</a>' if link else ""
    return f'<div class="sc-quote"><p>{b.get("text", "")}</p>{a}</div>'


def b_html(b, ctx, w):
    return b.get("html", "")


def b_callout(b, ctx, w):
    return f'<div class="sc-callout">{b.get("html", "")}</div>'


def b_details(b, ctx, w):
    ctx.need(b, "summary blocks", w)
    return f'<details class="sc-more"><summary>{b.get("summary", "")}</summary><div>{blocks(b.get("blocks", []), ctx, w)}</div></details>'


def b_tabs(b, ctx, w):
    tabs = b.get("tabs", [])
    btns = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}">{t["label"]}</button>'
                   for i, t in enumerate(tabs))
    panes = "".join(f'<div class="sc-tabpanel" role="tabpanel"{" hidden" if i else ""}>{blocks(t.get("blocks", []), ctx, f"{w}.tabs[{i}]")}</div>'
                    for i, t in enumerate(tabs))
    hd = (f'<div class="sc-tabs-hd"><h3>{b["title"]}</h3>' + (f'<p>{b["desc"]}</p>' if b.get("desc") else "") + "</div>") if b.get("title") else ""
    return f'<div class="sc-tabs">{hd}<div class="sc-tablist" role="tablist">{btns}</div>{panes}</div>'


def b_cols(b, ctx, w):
    return '<div class="sc-cols">' + "".join(f"<div>{blocks(col, ctx, f'{w}.cols[{i}]')}</div>"
                                             for i, col in enumerate(b.get("cols", []))) + "</div>"


BLOCKS = {k[2:]: v for k, v in globals().items() if k.startswith("b_")}


def blocks(items: list, ctx: Ctx, where: str) -> str:
    out = []
    for i, b in enumerate(items):
        fn = BLOCKS.get(b.get("type"))
        if not fn:
            ctx.errs.append(f"{where}[{i}]: type {b.get('type')!r} không có; có: {', '.join(sorted(BLOCKS))}")
            continue
        out.append(fn(b, ctx, f"{where}[{i}]:{b['type']}"))
    return "".join(out)


# ---------- page ----------

def motif() -> str:
    lines = []
    for i in range(48):
        h = 10 + 52 * abs(math.sin(i * .37) * math.cos(i * .11)) * (1 - abs(i - 24) / 30)
        lines.append(f'<line x1="{i * 5.6 + 3:.1f}" x2="{i * 5.6 + 3:.1f}" y1="{64 - h:.1f}" y2="{64 + h:.1f}" '
                     f'stroke="{"var(--sc-hl)" if i % 4 == 1 else "var(--sc-band-muted)"}" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>')
    return f'<svg class="sc-motif" viewBox="0 0 272 128" aria-hidden="true">{"".join(lines)}</svg>'


def logo(meta: dict, ctx: Ctx) -> str:
    br = meta.get("brand", {})
    sub = f'<span class="sc-logo-sub">{br["sub"]}</span>' if br.get("sub") else ""
    if br.get("logo"):
        p = ctx.base / Path(br["logo"]).expanduser()   # relative to report.json; absolute paths pass through
        if not p.exists():
            ctx.errs.append(f"meta.brand.logo: không thấy file {p}")
            return ""
        mime = {"svg": "image/svg+xml", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(p.suffix[1:].lower(), f"image/{p.suffix[1:].lower()}")
        img = f'<img alt="{esc(br.get("name", ""))}" src="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}">'
        return f'<a class="sc-logo" href="#top">{img}{sub}</a>'
    name = br.get("name", "Report")
    return f'<a class="sc-logo" href="#top"><span class="sc-mark">{esc(name[:1])}</span><span class="sc-word">{esc(name)}</span>{sub}</a>'


def hero(h: dict, meta: dict, ctx: Ctx) -> str:
    ctx.need(h, "kicker title lede stats note", "hero")
    stats = []
    for i, s in enumerate(h.get("stats", [])[:2]):
        ctx.need(s, "label value reading", f"hero.stats[{i}]")
        d = ctx.better(s, f"hero.stats[{i}]")
        k = s.get("label", "") + ("" if d == "none" else f" · {ctx.t[d][2:]}")
        stats.append(f'<div><div class="sc-ev-k">{k}</div><div class="sc-ev-v{" hl" if i == 0 else ""}">{s.get("value", "")}'
                     f'<small>{s.get("unit", "")}</small></div><p>{s.get("reading", "")}</p></div>')
    main = (stats[0] + f'<div class="sc-ev-join">{h.get("join", "")}</div>' + stats[1]) if len(stats) == 2 else "".join(stats)
    facts = "".join(f"<span>{f}</span>" for f in h.get("facts", []))
    card = h.get("card", {})
    return (f'<header class="sc-hero" id="top">{motif() if h.get("motif", True) else ""}<div class="sc-wrap">'
            f'<div class="sc-eb dot">{h.get("kicker", "")}</div><h1>{h.get("title", "")}'
            + (f'<br><span>{h["accent"]}</span>' if h.get("accent") else "") + f'</h1><p class="sc-lede">{h.get("lede", "")}</p>'
            f'<div class="sc-ev"><div class="sc-ev-hd"><strong>{card.get("title", "")}</strong><span>{card.get("tag", meta.get("date", ""))}</span></div>'
            f'<div class="sc-ev-main{" one" if len(stats) == 1 else ""}">{main}</div>'
            + (f'<div class="sc-ev-ft">{facts}</div>' if facts else "") + "</div>"
            f'<p class="sc-note"><span>↳</span><span><strong>{ctx.t["note"]}</strong> {h.get("note", "")}</span></p>'
            "</div></header>")


def method(m: dict, n: int, ctx: Ctx) -> str:
    ctx.need(m, "defs limits run source", "method")
    if len(m.get("run", [])) < 2:
        ctx.errs.append("method.run: cần ít nhất 2 dòng (model/run id, bộ dữ liệu, ngày…)")
    src = m.get("source", {})
    if not str(src.get("href", "")).startswith(("http://", "https://")):
        ctx.errs.append(f"method.source.href phải là link http(s) tới run gốc, đang là {src.get('href')!r}")
    defs = "".join(f'<p><b>{d["term"]}</b> {d["html"]}</p>' for d in m.get("defs", []))
    facts = "".join(f"<div><span>{k}</span><code>{v}</code></div>" for k, v in m.get("run", []))
    lim = "".join(f"<li>{x}</li>" for x in m.get("limits", []))
    t = ctx.t
    return (f'<section class="sc-sec" id="method"><div class="sc-wrap"><div class="sc-sec-hd"><div>'
            f'<div class="sc-eb dot">{n:02d} / {m.get("kicker", t["m_kicker"])}</div><h2>{m.get("title", t["m_title"])}</h2></div>'
            f'<p>{m.get("lede", t["m_lede"])}</p></div><div class="sc-method"><div class="sc-defs"><h3>{t["defs"]}</h3>{defs}'
            f'<h3 style="margin-top:1.75rem">{t["limits"]}</h3><ul class="sc-limits">{lim}</ul></div>'
            f'<div><h3>{t["run"]}</h3><div class="sc-facts">{facts}</div>'
            f'<a class="sc-src" href="{esc(str(src.get("href", "")))}" target="_blank" rel="noopener">{src.get("label", t["src"])}</a>'
            "</div></div></div></section>")


def samples_view(sm: dict, ctx: Ctx) -> str:
    """Every sample with its audio, reference and model output, for a reader who wants to re-check."""
    ctx.need(sm, "selection items", "samples")
    t, met, items = ctx.t, sm.get("metric"), sm.get("items", [])
    series = {x["key"]: x.get("series") for x in sm.get("legend", [])}
    cards = []
    for i, it in enumerate(items):
        w = f"samples.items[{i}]"
        ctx.need(it, "id audio", w)
        if "ref" not in it and "tracks" not in it:
            ctx.errs.append(f"{w}: cần 'ref' + 'hyps' (so chữ) hoặc 'tracks' (dòng thời gian)")
        if met and not isinstance(it.get("metric"), (int, float)):
            ctx.errs.append(f"{w}: 'metric' phải là số ({met.get('label', '')})")
        chips = []
        if met and isinstance(it.get("metric"), (int, float)):
            ok = it.get("pass")
            chips.append(f'<span class="sc-chip{" bad" if ok is False else ""}">{met.get("label", "")} '
                         f'{ctx.fmt(it["metric"], met.get("digits", 1))}{met.get("unit", "")}'
                         + (f' · {t["pass"] if ok else t["fail"]}' if ok is not None else "") + "</span>")
        facts = "".join(f"<span>{f}</span>" for f in it.get("facts", []))
        if "tracks" in it:
            body = (tl_html(it["tracks"], series, it.get("duration") or 1, it.get("start", 0))
                    + (f'<details><summary>{t["turns_sum"].format(n=len(it["turns"]))}</summary>{turns_html(it["turns"], ctx, w)}</details>'
                       if it.get("turns") else ""))
        else:
            rows = [f'<div class="sc-ex-row ref"><span>{t["ref"]}</span><span>{esc(it.get("ref", ""))}</span></div>']
            rows += [f'<div class="sc-ex-row"><span>{h.get("label", "")}</span><span>{diff_marks(it.get("ref", ""), h.get("text", ""), ctx)}</span></div>'
                     for h in it.get("hyps", [])]
            body = f'<div class="sc-ex">{"".join(rows)}</div>'
        q = " ".join([str(it.get("id", "")), str(it.get("group", "")), str(it.get("ref", ""))]
                     + [x.get("text", "") for x in it.get("turns", [])]).lower()
        cards.append(f'<article class="sc-smp" data-id="{esc(str(it.get("id", "")))}" data-group="{esc(str(it.get("group", "")))}" '
                     f'data-metric="{it.get("metric", 0)}" data-pass="{"" if it.get("pass") is None else int(bool(it["pass"]))}" data-q="{esc(q)}">'
                     f'<div class="sc-smp-hd"><b>{esc(str(it.get("id", "")))}</b>{"".join(chips)}{facts}</div>'
                     f'<audio controls preload="none" src="{ctx.audio(it.get("audio", ""), w)}"></audio>{body}'
                     + (f'<p class="sc-key">{it["note"]}</p>' if it.get("note") else "") + "</article>")
    groups = sorted({str(it.get("group", "")) for it in items} - {""})
    sel_g = (f'<select class="sc-smp-g" aria-label="{t["all_groups"]}"><option value="">{t["all_groups"]}</option>'
             + "".join(f'<option value="{esc(g)}">{esc(g)}</option>' for g in groups) + "</select>") if groups else ""
    sel_s = (f'<select class="sc-smp-s" aria-label="{t["all_status"]}"><option value="">{t["all_status"]}</option>'
             f'<option value="1">{t["pass"]}</option><option value="0">{t["fail"]}</option></select>'
             if any(it.get("pass") is not None for it in items) else "")
    sel_o = (f'<select class="sc-smp-o" aria-label="{t["sort"][0]}"><option value="">—</option><option value="desc">{t["sort"][0]}</option>'
             f'<option value="asc">{t["sort"][1]}</option><option value="id">{t["sort"][2]}</option></select>') if met else ""
    bar = (f'<div class="sc-smp-bar"><input class="sc-smp-q" type="search" placeholder="{t["search"]}" aria-label="{t["search"]}">'
           f'{sel_g}{sel_s}{sel_o}<span><b class="sc-smp-n">{len(items)}</b> / {len(items)} {t["shown"]}</span></div>')
    lw = f' style="--lw:{sm["label_width"]}"' if sm.get("label_width") else ""
    return (f'<div data-view="samples" hidden><main class="sc-main"><section class="sc-sec" id="samples-top"{lw}><div class="sc-wrap">'
            f'<div class="sc-sec-hd"><div><div class="sc-eb dot">{sm.get("kicker", t["samples"])}</div><h2>{sm.get("title", t["samples"])}</h2></div>'
            f'<p>{sm.get("lede", "")}</p></div><div class="sc-callout"><b>{t["selection"]}</b> {sm.get("selection", "")}'
            + (f' {t["play"]}' if sm.get("legend") else "") + "</div>"
            + (legend(sm["legend"]) if sm.get("legend") else "") + bar
            + f'<div class="sc-smp-list">{"".join(cards)}</div></div></section></main></div>')


def render(rep: dict, base: Path, audio_mode: str = "link", audio_dir: str = "audio") -> tuple[str, list[str], list[Path]]:
    meta = rep.get("meta", {})
    ctx = Ctx(meta.get("lang", "vi") if meta.get("lang") in L else "vi", base)
    ctx.audio_mode, ctx.audio_dir = audio_mode, audio_dir
    ctx.need(meta, "title date", "meta")
    secs = rep.get("sections", [])
    links = "".join(f'<a href="#{s.get("id", "")}">{s.get("nav", s.get("kicker", ""))}</a>' for s in secs)
    sm = rep.get("samples")
    views = (f'<div class="sc-views"><a class="sc-viewlink on" href="#top">{ctx.t["report"]}</a>'
             f'<a class="sc-viewlink" href="#samples">{sm.get("nav", ctx.t["samples"])} ({len(sm.get("items", []))})</a></div>') if sm else ""
    nav = (f'<nav class="sc-nav"><div class="sc-wrap sc-navin">{logo(meta, ctx)}<div class="sc-links">{links}'
           f'<a href="#method">{rep.get("method", {}).get("kicker", ctx.t["m_kicker"])}</a></div>{views}'
           # with the view switch there is no room for the stamp; the date stays on the hero card
           + ("" if sm else f'<span class="sc-pill">{meta.get("stamp", meta.get("date", ""))}</span>')
           + f"{THEME_BUTTON}</div></nav>")
    body = []
    for i, s in enumerate(secs):
        w = f"sections[{i}]"
        ctx.need(s, "id kicker title", w)
        alt = s.get("alt", i % 2 == 1)
        body.append(f'<section class="sc-sec{" alt" if alt else ""}" id="{s.get("id", "")}"><div class="sc-wrap"><div class="sc-sec-hd"><div>'
                    f'<div class="sc-eb dot">{i + 1:02d} / {s.get("kicker", "")}</div><h2>{s.get("title", "")}</h2></div>'
                    f'<p>{s.get("lede", "")}</p></div>{blocks(s.get("blocks", []), ctx, w)}</div></section>')
    body.append(method(rep.get("method", {}), len(secs) + 1, ctx))
    br = meta.get("brand", {})
    src = rep.get("method", {}).get("source", {})
    foot = (f'<footer class="sc-foot"><div class="sc-wrap"><div><b>{esc(br.get("name", ""))} <span>/ {br.get("sub", "")}</span></b>'
            f'<p>{meta.get("footer", "")}</p></div><a href="{esc(str(src.get("href", "")))}" target="_blank" rel="noopener">'
            f'{src.get("label", ctx.t["src"])}</a></div></footer>')
    page = (f'<div class="sc">{nav}<div data-view="report">{hero(rep.get("hero", {}), meta, ctx)}<main class="sc-main">'
            f'{"".join(body)}</main></div>{samples_view(sm, ctx) if sm else ""}{foot}</div>'
            f'<script>\n{(HERE / "showcase.js").read_text(encoding="utf8")}\n</script>')
    return page, ctx.errs, ctx.copies


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--shot", type=Path)
    ap.add_argument("--shot-size")
    ap.add_argument("--shot-theme", choices=("light", "dark"))
    ap.add_argument("--no-fonts", action="store_true")
    ap.add_argument("--audio", choices=("link", "embed"), default="link",
                    help="link (default): copy audio files to OUT_audio/ next to the page; embed: inline "
                         "into the page (one file to send, but the page must stay under 16 MB)")
    a = ap.parse_args()
    rep = json.loads(a.report.read_text(encoding="utf8"))
    adir = a.out.stem + "_audio"
    page, errs, copies = render(rep, a.report.resolve().parent, a.audio, adir)
    if len({p.name for p in copies}) != len(set(copies)):
        errs.append("hai file audio khác nhau trùng tên; đặt tên theo mã mẫu")
    if errs:
        print("KHÔNG GHI — report.json thiếu evidence:", file=sys.stderr)
        for e in errs:
            print(f"  · {e}", file=sys.stderr)
        return 1
    if copies:
        (a.out.parent / adir).mkdir(parents=True, exist_ok=True)
        for p in set(copies):
            dst = a.out.parent / adir / p.name
            if not dst.exists() or dst.stat().st_size != p.stat().st_size:
                shutil.copy2(p, dst)
        print(f"    audio: {len(set(copies))} file → {a.out.parent / adir}/ (giao cả thư mục này cùng trang)")
    fonts = KIT / "fonts-showcase.css"
    if not fonts.exists() and not a.no_fonts:   # a copy may ship without it (some skill hosts cap size)
        print(f"    {fonts.name} chưa có: tải {', '.join(SHOWCASE_FONTS)} từ Google Fonts, một lần")
        subprocess.run([sys.executable, str(KIT / "embed_fonts.py"), str(fonts), *SHOWCASE_FONTS], check=True)
    with tempfile.NamedTemporaryFile("w", suffix=".body.html", delete=False, encoding="utf8") as f:
        f.write(page)
    cmd = [sys.executable, str(KIT / "build.py"), f.name, str(a.out), "--title", rep["meta"]["title"],
           "--css", str(HERE / "showcase.css"), "--fonts", str(KIT / "fonts-showcase.css")]
    for flag in ("shot", "shot_size", "shot_theme"):
        if getattr(a, flag):
            cmd += ["--" + flag.replace("_", "-"), str(getattr(a, flag))]
    cmd += ["--no-fonts"] if a.no_fonts else []
    try:
        return subprocess.run(cmd).returncode
    finally:
        Path(f.name).unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
