# SVG and figure rules

Read when hand-drawing SVG for any page or sheet. `kit/build.py` enforces the table; the rest is
convention.

| Rule | Why |
|---|---|
| No `font-family=` inside SVG | the embedded fonts only exist through CSS; a hand-written stack lands on Helvetica |
| `stroke` never reaches `<text>` | `<g stroke=…>` outlines every glyph; tone marks fuse into letters |
| 11px floor | below that it is metadata, not prose |
| `currentColor` strokes; `<text>` without `fill` follows the theme | no re-render on theme switch |

Monospace inside a diagram: `class="m"`. Wrap in `<figure class="fig">` + `<figcaption
class="fig-cap">`, with `role="img"` and an `aria-label` that matches the caption. Mermaid only
when the page is certainly published through the Artifact tool. Design laws and the bug
catalogue: `design-rules.md`.
