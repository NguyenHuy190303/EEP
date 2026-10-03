# Explainer video: V1 (3b1b, default) and V2 (drawing sheet inked live)

Local only: Google Chrome, ffmpeg, and macOS `say`. No paid API, nothing installed globally.

1. `kv-cache.script.txt` holds one sentence per line. Each line is one visual beat, about 80% STE.
2. `kv-cache.src.html` is an SVG page. `render(t)` draws the frame at second `t`. `TL.cues[i].start` is when sentence i starts, so the visuals follow the voice.
3. Colours come from manim's own palette (`manim/utils/color/manim_colors.py`) on manim's default black background. Text is the STIX Two serif from macOS. On screen: math, numbers and 1–3-word labels only.

```bash
python3 tts.py kv-cache.script.txt narration --rate 180 --tail 1.5     # -> narration.wav / .srt / .timeline.json
python3 build_page.py kv-cache.src.html narration.timeline.json page.html
uv run --with playwright python stills.py page.html /tmp/still_ 5 12 29  # look at these before the full render
uv run --with playwright python capture.py page.html narration.wav narration.srt out.mp4
```

V2: same commands with `kv-cache.sheet.src.html`. It loads IBM Plex from `fonts/` (OFL), so build
the page next to that folder.

`capture.py` steps `render(i/fps)` in 6 headless Chrome workers, then encodes H.264 + AAC with a `mov_text` caption track. A 31 s video takes about 15 s.
Do not pass `-shortest`: ffmpeg deadlocks with a sparse caption track.
To show the captions, the player must turn them on. This ffmpeg has no libass, so it cannot burn them in.
