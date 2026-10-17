#!/usr/bin/env python3
"""Fail on the things that make a card or dataset look finished when it is not.

usage: check_card.py README.md --type model|dataset|readme [--data PARQUET|DIR|REPO_ID]
       check_card.py --selftest
--data checks the parquet column order the Hub viewer will show: media first, ids/hashes last.
"""
import argparse, re, sys
from pathlib import Path

PLACEHOLDERS = re.compile(r"\[More Information Needed\]|\bTBD\b|\bTODO\b|coming soon|(?<![=\w])\{[a-z_]+\}", re.I)  # ponytail: lookbehind skips BibTeX `key={x}`
NUMBER = re.compile(r"\b\d+(\.\d+)?\b")
SOURCE = re.compile(r"\]\(|https?://|leaderboard|eval log|source", re.I)

MEDIA = re.compile(r"^(audio|image|video)s?$")
TAIL = re.compile(r"(^|_)(ids?|sha\d*|md5|hash|path|uri|url)$|^(sample_rate|channels|file(name)?)$")
FACET_IDS = {"speaker_id"}  # an id people filter on; it belongs with the facets, not the tail
PROVENANCE = re.compile(r"^#+ .*(provenance|reproduc)", re.I | re.M)
TRACEABLE = re.compile(r"\b[0-9a-f]{7,40}\b|https?://|not recorded", re.I)

def column_order_problems(names, media=()):
    """media: names whose type is Audio/Image (struct with bytes), in case the name does not say so."""
    out = []
    med = [n for n in names if MEDIA.match(n) or n in media]
    if med and names[0] not in med:
        out.append(f"media column {med[0]!r} is at position {names.index(med[0])}, must be first")
    tail = [bool(TAIL.search(n)) and n not in FACET_IDS for n in names]
    if any(tail):
        first = tail.index(True)
        late = [n for n, t in zip(names[first:], tail[first:]) if not t]
        if late:
            out.append(f"id/hash/technical columns must be one block at the end; {late} come after {names[first]!r}")
    return out

def parquet_schemas(target):
    """One schema per directory (= config/split), from a local file/dir or a Hub dataset repo id."""
    import pyarrow.parquet as pq
    p = Path(target)
    if p.exists():
        files, opener = ([p] if p.is_file() else sorted(p.rglob("*.parquet"))), open
    else:
        from huggingface_hub import HfFileSystem
        fs = HfFileSystem()
        files, opener = sorted(fs.glob(f"datasets/{target}/**/*.parquet")), fs.open
    firsts = {}
    for f in files:
        firsts.setdefault(str(Path(str(f)).parent), f)
    if not firsts:
        sys.exit(f"no parquet files under {target}")
    for d, f in firsts.items():
        with opener(f, "rb") as fh:
            yield d, pq.read_schema(fh)

def tables(md):
    rows, cur = [], []
    for line in md.splitlines():
        if line.lstrip().startswith("|"):
            cur.append(line)
        elif cur:
            rows.append(cur); cur = []
    if cur: rows.append(cur)
    return rows

def selftest():
    assert not column_order_problems(["audio", "text", "speaker_id", "duration", "reviewed_by", "audio_id", "sample_rate"])
    assert column_order_problems(["text", "audio"])  # media not first
    assert column_order_problems(["audio", "text", "audio_sha256", "group_id", "duration"])  # id before a facet
    assert not column_order_problems(["text", "label"])  # no media, no ids
    assert PROVENANCE.search("## Provenance and reproduction") and TRACEABLE.search("repo@40fd576")
    print("selftest OK")

def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("card", nargs="?")
    ap.add_argument("--type", choices=["model", "dataset", "readme"])
    ap.add_argument("--data")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.card and a.type):
        sys.exit(__doc__)
    path, kind = Path(a.card), a.type
    md = path.read_text()
    errors = []

    if kind == "dataset":
        m = PROVENANCE.search(md)
        if not m:
            errors.append("dataset card has no '## Provenance and reproduction' section")
        elif not TRACEABLE.search(md[m.end():].split("\n## ", 1)[0]):
            errors.append("provenance section names no commit, URL, or explicit 'not recorded'")

    if a.data:
        for d, schema in parquet_schemas(a.data):
            media = [f.name for f in schema if str(f.type).startswith("struct<bytes")]
            errors += [f"{d}: {e}" for e in column_order_problems(schema.names, media)]

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
