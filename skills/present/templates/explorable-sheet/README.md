# W2 — explorable on a drawing sheet

The same interactions as W1, laid out inside a zone-ruled drawing sheet with a title block.

**Status: as sampled, light only, bypasses `kit/build.py`.** It has no dark theme and no
validation, so it fails delivery-gate item 2 until both are added. Tell the user before picking it.

| File | Role |
|---|---|
| `explorable.core.html` | content markup; `<!--tb-->` marks where the title block goes |
| `core.js` | the interactions (KV-cache specific: rewrite for a new topic) |
| `explorable.css` + `theme-sheet.css` | layout + sheet look |
| `assemble.py` | stitches everything + `kit/fonts.css` into one page; title block text lives here |

```bash
python3 $K/templates/explorable-sheet/assemble.py out.html
```

To bring it up to the gate: add the blueprint dark theme from `../sheet/sheet.css` and a
`theme-toggle`, or port it onto `kit/build.py --css` the way W1 was.
