"""Pre-built style gallery: what the user looks at when picking a style. Costs no tokens.

usage:
  python3 show.py DEST              build the gallery into DEST/present-gallery/, print the index path
  python3 show.py --refresh-media   maintainers, after changing a template (needs Chrome + macOS sips):
                                    re-shoot the page thumbnails in media/

The sample pages are rebuilt from the templates on every run (about 2 s, stdlib only), so the
gallery always shows what the templates produce now. Only small media is committed: thumbnails,
the archify render, and the two videos. Re-render a video with templates/video/README.md, then
copy the mp4 + a still over media/v1.* or media/v2.*.
"""
import shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "kit"))
from selftest import JOBS  # noqa: E402  one list of shipped examples, shared with the self-test

# thumbnail: (page job, theme, viewport). Kit pages are shot by build.py at 2x.
THUMBS = {
    "txt": ("writing-abc", "light", "1400x900"),
    "w1-light": ("W1-explorable", "light", "1600x1000"),
    "w1-dark": ("W1-explorable", "dark", "1600x1000"),
    "w2": ("W2-explorable-sheet", "light", "1600x1000"),
    "d1-light": ("D1-sheet", "light", "1920x1200"),
    "d1-dark": ("D1-sheet", "dark", "1920x1200"),
}


def build_pages(pages: Path) -> None:
    pages.mkdir(parents=True, exist_ok=True)
    for name, cmd in JOBS.items():
        out = pages / f"{name}.html"
        r = subprocess.run([str(out) if c == "{out}" else c for c in cmd], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"{name} failed to build:\n{(r.stdout + r.stderr)[-1500:]}")


def show(dest: Path) -> None:
    out = dest / "present-gallery"
    build_pages(out / "pages")
    shutil.copy2(HERE / "index.html", out / "index.html")
    shutil.copytree(HERE / "media", out / "media", dirs_exist_ok=True)
    shutil.copytree(ROOT / "templates/video/fonts", out / "fonts", dirs_exist_ok=True)
    print(out / "index.html")


def refresh_media() -> None:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="present-gallery-"))
    build_pages(tmp)
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    for thumb, (job, theme, size) in THUMBS.items():
        png = tmp / f"{thumb}.png"
        page = tmp / f"{job}.html"
        if JOBS[job][1].endswith("build.py"):
            subprocess.run([str(tmp / "x.html") if c == "{out}" else c for c in JOBS[job]]
                           + ["--shot", str(png), "--shot-size", size, "--shot-theme", theme],
                           check=True, capture_output=True)
        else:  # W2 bypasses build.py: shoot it directly
            w, h = size.split("x")
            subprocess.run([chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                            f"--window-size={w},{h}", "--virtual-time-budget=1500",
                            f"--screenshot={png}", f"file://{page}?still=1"], check=True, capture_output=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "75", "-Z", "1280",
                        str(png), "--out", str(HERE / "media" / f"{thumb}.jpg")], check=True, capture_output=True)
        print(f"media/{thumb}.jpg")


if __name__ == "__main__":
    if sys.argv[1:] == ["--refresh-media"]:
        refresh_media()
    elif len(sys.argv) == 2:
        show(Path(sys.argv[1]).expanduser())
    else:
        sys.exit(__doc__)
