## 1. Ask the style first, then cook

Never build samples to show styles: the gallery is pre-built. Run
`python3 $K/gallery/show.py <server folder>`; it rebuilds the sample pages from the templates into
`<server folder>/present-gallery/` (about 2 s, no tokens). Then `open` its `index.html` URL. Then ask
with `AskUserQuestion`: one question per output type the request needs (max 4), options from this
table, the default first and marked "(Recommended)", the gallery URL in the question text. Skip
all of this only when the user already named a style in this conversation.

**Every question ends with one more option: "None fits — Claude designs it".** Pick that path too
when the user says no style fits, or asks for something new. On it, design the layout and visual
form from the content itself. Do not copy a template or a worked example. Three things stay fixed:
build through `kit/build.py` with your own `--css` (it embeds the Vietnamese fonts and runs the
validators); colours come from the `tokens.css` variables, or from a new palette that passes
`kit/validate_palette.mjs` in both themes; the delivery gate (§3) is unchanged. If the design
turns out reusable, offer to add it as a style (§6).

| Type | Style | Start from |
|---|---|---|
| Writing | **B, 80% STE** (default) · A, strict STE · C, dense engineering | `references/writing.md` |
| Page / explorable | **W1, reading room** (default): paper + serif, deep-green dark, TOC + cards + interactive panel | `templates/explorable/README.md`; plain report: `kit/README.md` |
| | W2, explorable on a drawing sheet. *Light only, bypasses `build.py`; say so when offering it* | `templates/explorable-sheet/README.md` |
| Page, results shown to people who act on them (eval, benchmark, status for leadership) | **W3, showcase** (default for results): brand band + headline metric, KPI cards, comparisons, real examples, method & limits, and a samples view with every audio to re-check against the reference. `report.json` in; the build stops when evidence is missing | `templates/showcase/README.md` |
| Diagram, a concept | **D1, drawing sheet** (default): lettered panels, zone ruler, title block; white / blueprint | `templates/sheet/README.md` |
| Diagram, architecture / stack | **D2, archify** (default): lanes + arrows | `templates/archify/README.md` |
| Video, 20–40 s narrated | **V1, 3b1b** (default): manim palette on black · V2, drawing sheet inked live | `templates/video/README.md` |
