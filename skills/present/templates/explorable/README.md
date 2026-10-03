# W1 — reading-room explorable (default page style)

TOC on the left, question cards, one interactive panel on deep green. The panel is driven by a
small inline script inside the body; the KV-cache example shows the pattern.

| File | Role |
|---|---|
| `kv-cache.body.html` | worked example: copy it, keep the structure, replace content and the panel script |
| `explorable.css` | layout only; colours come from `kit/tokens.css` through the alias block at the top |

```bash
python3 $K/kit/build.py my.body.html out.html --title "Short Distinctive Noun" \
  --css $K/templates/explorable/explorable.css \
  --shot shot.png --shot-size 1920x3000 [--shot-theme dark]
```

Verify: screenshot in both themes plus one interacted state (drive it with a URL parameter, as
the example does). A plain report page (no panel) needs no template: `kit/build.py` with kit
components only (`kit/README.md`).
