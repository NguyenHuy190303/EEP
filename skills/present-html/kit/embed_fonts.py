#!/usr/bin/env python3
"""Fetch Inter + Fira Code from Google Fonts and inline them as data: URIs.

The Artifact CSP blocks every external host, so a <link> to fonts.googleapis.com
fails silently and the page falls back to a system face. Embedding keeps the real
letterforms (and Fira Code's ligatures) without any network request.

Parses @font-face blocks directly and selects by unicode-range rather than by the
"/* latin */" comments — Google emits subset names like `symbols2` and `[1]` that
a name-based split mishandles. Keeps only the ranges Vietnamese text needs.
"""
import base64
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

FAMILIES = ["Inter:wght@400;500;600;700", "Fira+Code:wght@400;500;600"]

FACE = re.compile(r"@font-face\s*\{[^}]*\}", re.S)
URL = re.compile(r"url\((https://[^)]+\.woff2)\)")
RANGE = re.compile(r"unicode-range:\s*([^;]+);")
WEIGHT = re.compile(r"font-weight:\s*(\d+)")

# Latin basic+supplement / Latin Extended-A/B / combining marks / Latin Extended
# Additional (U+1EA0-1EF9 is where most Vietnamese precomposed letters live).
WANT_STARTS = ("U+0000", "U+0100", "U+0102", "U+0301", "U+0000-00FF")


def wanted(rng: str) -> bool:
    """True for the latin / latin-ext / vietnamese subsets, false for cyrillic,
    greek, and the symbol blocks."""
    first = rng.split(",")[0].strip().upper()
    if first.startswith(("U+04", "U+05", "U+03", "U+1F0", "U+2000", "U+E0", "U+F0")):
        return False
    return first.startswith(("U+00", "U+01", "U+02", "U+03", "U+1E"))


def get(url: str) -> bytes:
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90
    ).read()


def main() -> None:
    out, total, skipped = [], 0, 0
    for fam in FAMILIES:
        name = fam.split(":")[0].replace("+", " ")
        css = get(f"https://fonts.googleapis.com/css2?family={fam}&display=swap").decode()
        for block in FACE.findall(css):
            u, r = URL.search(block), RANGE.search(block)
            if not (u and r) or not wanted(r.group(1)):
                skipped += 1
                continue
            try:
                raw = get(u.group(1))
            except Exception as e:                       # one dead subset must not kill the run
                print(f"  ! {name} {u.group(1)[-24:]} {e}", file=sys.stderr)
                continue
            total += len(raw)
            b64 = base64.b64encode(raw).decode()
            out.append(URL.sub(f"url(data:font/woff2;base64,{b64})", block))
            w = WEIGHT.search(block)
            print(f"  {name:11} w{w.group(1) if w else '?':<4} "
                  f"{r.group(1)[:26]:28} {len(raw)/1024:6.1f} KB", file=sys.stderr)

    css_out = "\n".join(out)
    open(sys.argv[1], "w").write(css_out)
    print(f"\n{len(out)} faces kept, {skipped} subsets skipped · "
          f"raw {total/1024:.0f} KB → css {len(css_out)/1024:.0f} KB → {sys.argv[1]}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
