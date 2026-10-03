# D1 — drawing sheet (default for explaining a concept)

One static sheet: zone ruler 1–8 / A–D, lettered panels, title block. White paper, blueprint dark.

| File | Role |
|---|---|
| `kv-cache.body.html` | worked example: copy it, keep the frame, panels and title block |
| `sheet.css` | the sheet palette and layout, light + blueprint |

```bash
python3 $K/kit/build.py my.body.html out.html --title "Short Distinctive Noun" \
  --css $K/templates/sheet/sheet.css \
  --shot shot.png --shot-size 1920x1200 [--shot-theme dark]
```

The theme toggle sits in the title block as `class="theme-toggle flip"`. Hand-drawn SVG in panels
follows `references/svg.md`.
