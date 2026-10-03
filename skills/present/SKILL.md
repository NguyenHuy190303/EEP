---
name: present
description: Turn an explanation into something a person can see — an HTML page (report, postmortem, spec, memo, interactive explorable), a diagram (concept sheet or architecture), or a narrated explainer video — plus the plain-English prose those artifacts use. Use whenever the output is .html/.css or .mp4, a report is being turned into a page, a diagram or explainer is needed, or the user asks to "export as HTML", "make a video", "explain this visually" or for a prettier page. Asks the user to pick a style first; owns the palettes, embedded Vietnamese-capable fonts and the render-and-look check.
---

# present

Every style below came out of one same-topic sample round (2026-10-03). **Fewer words** was half
the brief: labels and numbers over paragraphs; the visual or the interaction carries it.

`$K` in every command = this skill's base directory (printed as "Base directory for this skill"
when it loads). Do not rely on `CLAUDE_PLUGIN_ROOT`: it is unset when the skill is installed as a
plain skills folder. Shell variables do not persist between Bash calls, so start each command
with `K="<base directory>";` or paste the literal path.

## 1. Ask the style first, then cook

Never build samples to show styles: the gallery is pre-built. Run
`python3 $K/gallery/show.py <server folder>`; it rebuilds the sample pages from the templates into
`<server folder>/present-gallery/` (about 2 s, no tokens). Then `open` its `index.html` URL. Then ask
with `AskUserQuestion`: one question per output type the request needs (max 4), options from this
table, the default first and marked "(Recommended)", the gallery URL in the question text. Skip
all of this only when the user already named a style in this conversation.

| Type | Style | Start from |
|---|---|---|
| Writing | **B, 80% STE** (default) · A, strict STE · C, dense engineering | `references/writing.md` |
| Page / explorable | **W1, reading room** (default): paper + serif, deep-green dark, TOC + cards + interactive panel | `templates/explorable/README.md`; plain report: `kit/README.md` |
| | W2, explorable on a drawing sheet. *Light only, bypasses `build.py`; say so when offering it* | `templates/explorable-sheet/README.md` |
| Diagram, a concept | **D1, drawing sheet** (default): lettered panels, zone ruler, title block; white / blueprint | `templates/sheet/README.md` |
| Diagram, architecture / stack | **D2, archify** (default): lanes + arrows | `templates/archify/README.md` |
| Video, 20–40 s narrated | **V1, 3b1b** (default): manim palette on black · V2, drawing sheet inked live | `templates/video/README.md` |

## 2. Workflow

1. Read the chosen style's README. Copy its KV-cache worked example; keep the structure, replace
   the content. Interactive or animated parts (panel script, `core.js`, `render(t)`) are
   topic-specific: rewrite them.
2. Write the prose in the chosen writing style.
3. Build with the README's command. `kit/build.py` embeds fonts, tokens, components, icons, the
   theme toggle and fullscreen overlay, **validates first, then writes atomically**.
4. Pass the delivery gate below.

## 3. Delivery gate: all of these, every time

1. **The build exits 0.** A non-zero exit is never success. Fix the input; do not route around
   the validator.
2. **Look at the screenshot, in both themes.** Reading your own markup is not verification.
   Check that text sits inside its box, nothing overflows, Vietnamese diacritics render, and the
   type is right. Explorable: also one interacted state (URL parameter). Video: 3–4 stills,
   each checked against what the narration says at that moment.
3. **Never counterfeit a fit.** No `overflow:hidden`, no clipping, no inner scroller, no type
   below 11px. Cut words or widen the box.
4. **Serve it and open it yourself.** Copy it into a dated subfolder of the user's private static
   server folder (base URL and folder are in their global instructions; if absent, ask once),
   then run `open "<http-url>"`. Several pages: open the index. A `file://` path is not a
   delivery. No server: `python3 -m http.server` on `127.0.0.1` plus a port-forward. Never bind
   `0.0.0.0` or push to a public host without explicit go-ahead.

## 4. Hard rules

- **Never Read, cat or grep `kit/fonts.css`** (1.3 MB of base64, ~400k tokens), `*.woff2`, or a
  built page. `build.py` inlines them; `kit/embed_fonts.py` regenerates `fonts.css`.
- Never invent a palette. Changing one: `references/palettes.md`.
- Hand-drawn SVG follows `references/svg.md`; `build.py` rejects violations.
- Vietnamese prose: `eep:vietnamese-writing`, not STE.

## 5. Where things live

| Path | Read when |
|---|---|
| `gallery/` | showing the styles (`show.py`); media is committed, pages are rebuilt |
| `templates/<style>/README.md` | building that style |
| `kit/README.md` | building a plain page; component and token reference |
| `references/writing.md` | writing prose (styles A / B / C) |
| `references/palettes.md` | touching a colour |
| `references/svg.md` | hand-drawing SVG |
| `references/infographic.md` | inline node flows, step-by-step diagrams, GIF export |
| `references/design-rules.md` | changing the kit; the bug catalogue behind every validator |

## 6. Maintenance

- **After any change** to `kit/` or `templates/`: `python3 $K/kit/selftest.py` rebuilds every
  shipped example (CI runs it too), then screenshot what you touched in both themes.
- **Add a style:** `templates/<name>/` with a worked example + README (what, files, build
  command, verify), a row in §1, a job in `kit/selftest.py`, a card in `gallery/index.html`, a
  CHANGELOG line.
- **After changing a template's look:** `python3 $K/gallery/show.py --refresh-media` re-shoots the
  page thumbnails (macOS + Chrome). Videos: re-render per `templates/video/README.md`, copy the mp4
  and a still to `gallery/media/`.
- **Change a palette:** `node $K/kit/validate_palette.mjs "#hex,…" --surface "#paper" --mode
  light|dark`; every text colour clears 4.5:1.
- **New component:** only when no mix of `.card` / `.alert` / `.tw` / `.code` / `.checklist` /
  `.fig` / `.metrics` carries it. `var()` for every colour, text beside any colour signal, and a
  matching guard in `build.py` so the next mistake fails loudly.
- **Release:** bump both `plugin.json` files and add a CHANGELOG entry.
