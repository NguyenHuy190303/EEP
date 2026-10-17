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
    "W3-showcase": [sys.executable, str(T / "showcase/render.py"), str(T / "showcase/example.report.json"), "{out}"],
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
    if not evidence_guard_holds(out_dir):
        failed.append("W3-evidence-guard")
    return 1 if failed else 0


def evidence_guard_holds(out_dir: Path) -> bool:
    """W3 must refuse a report with a gap in its evidence and write nothing. Kept out of JOBS:
    the gallery builds every job and this one is meant to fail."""
    import json
    rep = json.loads((T / "showcase/example.report.json").read_text(encoding="utf8"))
    del rep["sections"][0]["blocks"][0]["items"][0]["basis"]   # a KPI without its denominator
    del rep["hero"]["note"]                                    # a headline without "what it is not"
    rep["method"]["source"]["href"] = "#"                       # no link to the source run
    bad, out = out_dir / "broken.report.json", out_dir / "broken.html"
    bad.write_text(json.dumps(rep), encoding="utf8")
    for f in (T / "showcase/example_audio").iterdir():          # keep audio paths resolvable
        (out_dir / "example_audio").mkdir(exist_ok=True)
        (out_dir / "example_audio" / f.name).write_bytes(f.read_bytes())
    r = subprocess.run([sys.executable, str(T / "showcase/render.py"), str(bad), str(out)],
                       capture_output=True, text=True)
    ok = r.returncode == 1 and not out.exists() and all(
        k in r.stderr for k in ("'basis'", "'note'", "method.source.href"))
    print(f"{'PASS' if ok else 'FAIL'}  W3-evidence-guard  (refuses 3 gaps, writes nothing)")
    if not ok:
        print((r.stdout + r.stderr).strip()[-1500:])
    return ok


if __name__ == "__main__":
    sys.exit(main())
