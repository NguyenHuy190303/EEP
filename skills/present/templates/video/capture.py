"""Deterministic frame capture: window.render(t) per frame in real Google Chrome (N parallel workers), then ffmpeg.
No -shortest: with a sparse subtitle stream ffmpeg 7/8 deadlocks near the last cue. Frame count = audio length, so streams already match.
usage: uv run --with playwright python capture.py page.html narration.wav captions.srt out.mp4 [--fps 30] [--workers 6]"""
import argparse, subprocess, tempfile, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def work(args):
    page, tmp, fps, frames = args
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        pg.goto(Path(page).resolve().as_uri()); pg.evaluate("document.fonts.ready")
        for i in frames:
            pg.evaluate(f"render({i / fps})")
            pg.screenshot(path=f"{tmp}/f{i:05d}.jpg", type="jpeg", quality=94)
        b.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("page"); ap.add_argument("wav"); ap.add_argument("srt"); ap.add_argument("out")
    ap.add_argument("--fps", type=int, default=30); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.wav]))
    n = int(dur * a.fps); tmp = tempfile.mkdtemp(); t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        list(ex.map(work, [(a.page, tmp, a.fps, range(w, n, a.workers)) for w in range(a.workers)]))
    cap = time.time() - t0
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-framerate", str(a.fps), "-i", f"{tmp}/f%05d.jpg", "-i", a.wav, "-i", a.srt,
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
                    "-movflags", "+faststart", a.out], check=True)
    print(f"{a.out}: {n} frames @ {a.fps}fps, capture {cap:.0f}s, total {time.time() - t0:.0f}s")
