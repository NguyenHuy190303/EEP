"""Inline the narration timeline into an animation page. usage: build_page.py src.html timeline.json out.html"""
import sys
from pathlib import Path
src, tl, out = sys.argv[1:4]
Path(out).write_text(Path(src).read_text().replace("/*TIMELINE*/", Path(tl).read_text()))
