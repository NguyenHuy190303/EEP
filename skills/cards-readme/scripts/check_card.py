#!/usr/bin/env python3
"""Fail on the three things that make a card look finished when it is not.

usage: check_card.py README.md --type model|dataset|readme
"""
import re, sys
from pathlib import Path

PLACEHOLDERS = re.compile(r"\[More Information Needed\]|\bTBD\b|\bTODO\b|coming soon|(?<![=\w])\{[a-z_]+\}", re.I)  # ponytail: lookbehind skips BibTeX `key={x}`
NUMBER = re.compile(r"\b\d+(\.\d+)?\b")
SOURCE = re.compile(r"\]\(|https?://|leaderboard|eval log|source", re.I)

def tables(md):
    rows, cur = [], []
    for line in md.splitlines():
        if line.lstrip().startswith("|"):
            cur.append(line)
        elif cur:
            rows.append(cur); cur = []
    if cur: rows.append(cur)
    return rows

def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--type":
        sys.exit(__doc__)
    path, kind = Path(sys.argv[1]), sys.argv[3]
    md = path.read_text()
    errors = []

    if m := PLACEHOLDERS.search(md):
        errors.append(f"placeholder left in card: {m.group(0)!r}")

    # A results table = a table where the header mentions a benchmark-ish word and cells hold numbers.
    for t in tables(md):
        head = t[0].lower()
        if not re.search(r"benchmark|metric|acc|score|result|f1|bleu|wer", head):
            continue
        body = "\n".join(t[2:])
        if NUMBER.search(body) and not SOURCE.search("\n".join(t)):
            errors.append("results table has numbers but no source column/link:\n  " + t[0].strip())

    if kind in ("model", "dataset"):
        from huggingface_hub import ModelCard, DatasetCard  # local install, verified 1.15.0
        Card = ModelCard if kind == "model" else DatasetCard
        try:
            card = Card.load(path)
            card.validate(repo_type=kind)  # calls the Hub's validate-yaml endpoint
        except Exception as e:  # ValueError from validation, HTTPError from the Hub
            errors.append(f"Hub validation: {type(e).__name__}: {e}")

    for e in errors:
        print("FAIL:", e)
    print("OK" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
