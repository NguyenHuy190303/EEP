## 2. Workflow

1. Read the chosen style's README. Copy its worked example; keep the structure, replace
   the content. Interactive or animated parts (panel script, `core.js`, `render(t)`) are
   topic-specific: rewrite them. On "None fits", skip the worked example: start from
   `kit/README.md` (components, tokens, theme toggle) and your own `--css`.
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

- **Never Read, cat or grep `kit/fonts.css` or `kit/fonts-showcase.css`** (base64, up to ~400k
  tokens), `*.woff2`, or a built page. `build.py` inlines them; `kit/embed_fonts.py` regenerates
  them (usage in its docstring).
- Never invent a palette, except on the "None fits" path, and even there it must pass
  `validate_palette.mjs`. Changing one: `references/palettes.md`.
- Hand-drawn SVG follows `references/svg.md`; `build.py` rejects violations.
- Vietnamese prose: `eep:vietnamese-writing`, not STE.
