"""Rebuild every shipped example; exit 1 if any build fails.

usage: python3 kit/selftest.py [--keep DIR]

Run after touching the kit, a template or a palette. Stdlib only, no Chrome: it checks that each
example still builds and passes build.py's validators, not how it looks. Look at screenshots for
that (SKILL.md, delivery gate). Video is not covered: it needs macOS `say` and a narration timeline.
"""
import subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "templates"
BUILD = [sys.executable, str(ROOT / "kit/build.py")]

JOBS = {
    "page-specimen": BUILD + [str(T / "specimen.body.html"), "{out}", "--title", "Kit Specimen"],
    "W1-explorable": BUILD + [str(T / "explorable/kv-cache.body.html"), "{out}", "--title", "KV Cache",
                              "--css", str(T / "explorable/explorable.css")],
    "D1-sheet": BUILD + [str(T / "sheet/kv-cache.body.html"), "{out}", "--title", "KV Cache Sheet",
                         "--css", str(T / "sheet/sheet.css")],
    "writing-abc": BUILD + [str(T / "writing/kv-cache.abc.body.html"), "{out}", "--title", "Writing Styles"],
    "W2-explorable-sheet": [sys.executable, str(T / "explorable-sheet/assemble.py"), "{out}"],
}


def main() -> int:
    keep = sys.argv[sys.argv.index("--keep") + 1] if "--keep" in sys.argv else None
    out_dir = Path(keep or tempfile.mkdtemp(prefix="present-selftest-"))
    out_dir.mkdir(parents=True, exist_ok=True)
    failed = []
    for name, cmd in JOBS.items():
        out = out_dir / f"{name}.html"
        r = subprocess.run([str(out) if c == "{out}" else c for c in cmd], capture_output=True, text=True)
        ok = r.returncode == 0 and out.exists() and out.stat().st_size > 0
        print(f"{'PASS' if ok else 'FAIL'}  {name}  ({out.stat().st_size // 1024 if out.exists() else 0} KiB)")
        if not ok:
            failed.append(name)
            print((r.stdout + r.stderr).strip()[-2000:])
    print(f"\n{len(JOBS) - len(failed)}/{len(JOBS)} built -> {out_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
