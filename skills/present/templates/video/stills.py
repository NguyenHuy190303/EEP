"""Preview stills: uv run --with playwright python stills.py page.html out_prefix t1 t2 ..."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
page, pre, *ts = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(Path(page).resolve().as_uri()); pg.evaluate("document.fonts.ready")
    for t in ts:
        pg.evaluate(f"render({t})"); pg.screenshot(path=f"{pre}{t}.png")
    b.close()
