"""W2: the explorable on a drawing sheet. Stitch core markup + JS + CSS + sheet theme into one page.

usage: python3 assemble.py out.html
Edit explorable.core.html (content) and TB below (title block); the interactions live in core.js.
As sampled on 2026-10-03: light paper only, no theme toggle. Before delivery, add the blueprint
dark theme from ../sheet/sheet.css; the delivery gate requires both themes.
"""
import pathlib, sys

here = pathlib.Path(__file__).parent
fonts = (here / "../../kit/fonts.css").read_text()
css = (here / "explorable.css").read_text() + "\n" + (here / "theme-sheet.css").read_text()
core = (here / "explorable.core.html").read_text()
js = (here / "core.js").read_text()

TB = ('<div class="tb">'
      '<div class="full"><span>Title</span><b>The KV cache: why decoding never recomputes the past</b></div>'
      '<div><span>Model</span><b>Llama 3.1 8B Instruct</b></div><div><span>Shape</span><b>32 L · 8 KV · d 128</b></div>'
      '<div><span>Units</span><b>KiB, GiB (binary)</b></div><div><span>Values</span><b>bfloat16 · 2 B</b></div>'
      '<div><span>Source</span><b>config.json · 2026-10-03</b></div><div><span>Sheet</span><b>1 of 1</b></div>'
      '</div>')

zones = lambda tag, items: f'<div class="ruler {tag}">' + "".join(f"<span>{i}</span>" for i in items) + "</div>"
frame = ('<div class="sheet">' + zones("t", range(1, 9)) + zones("b", range(1, 9))
         + zones("l", "ABCD") + zones("r", "ABCD") + '<div class="frame">')

pathlib.Path(sys.argv[1]).write_text(
    '<!doctype html><html lang="en"><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>KV Cache Sheet</title><style>{fonts}\n{css}</style>\n'
    f'<body>{frame}{core.replace("<!--tb-->", TB)}</div></div>\n{js}</body></html>\n')
