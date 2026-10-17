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
