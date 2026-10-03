# Palettes

Read before touching a colour, or when a template's look needs explaining. Never add a new
palette; a change to an existing one is re-validated as below.

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
