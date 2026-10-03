#!/usr/bin/env python3
"""Sentence-length check for the 80%-STE register. usage: ste_check.py FILE [--max 20] [--all]

Reads .md / .txt / .html (tags and <style>/<script> stripped). Prints every sentence longer than
--max words (default 20, STE's procedural limit; 25 is the descriptive one). Exit 1 if any.
Symbols (× = · →) are not words; 1,000 is one word."""
import html, re, sys

def sentences(text: str) -> list[str]:
    text = re.sub(r"<(style|script)\b.*?</\1>", " ", text, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", "\n", text))
    text = re.sub(r"(\d),(\d)", r"\1\2", text)
    parts = re.split(r"(?<=[.!?:;])\s+|\n\s*\n|\n(?=\s*[-*\d]+[.)]?\s)", text)
    return [" ".join(p.split()) for p in parts if len(p.split()) >= 2]

def words(s: str) -> int:
    return sum(any(c.isalnum() for c in w) for w in s.split())

if __name__ == "__main__":
    args = sys.argv[1:]
    limit = int(args[args.index("--max") + 1]) if "--max" in args else 20
    sents = sentences(open(args[0], encoding="utf8").read())
    n = [words(s) for s in sents]
    long = [(w, s) for w, s in zip(n, sents) if w > limit]
    for w, s in long:
        print(f"{w:3d}  {s}")
    print(f"{len(n)} sentences · avg {sum(n)/max(len(n),1):.1f} words · longest {max(n, default=0)} · over {limit}: {len(long)}")
    sys.exit(1 if long else 0)
