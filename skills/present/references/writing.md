# Writing styles

Read when writing prose inside a present artifact. Chat replies are out of scope. The user picks
A, B or C up front; B is the default. Vietnamese prose: STE is an English spec, so use
`eep:vietnamese-writing` instead.

## B, 80% of the way to ASD-STE100 (default)

- Answer first: one line that says the whole thing.
- One idea per sentence. Most sentences stay ≤20 words; descriptive ones may reach 25.
- Active voice. Same word for the same thing every time.
- Ordinary vocabulary and "because" are allowed; STE's approved dictionary is not required.
- Keep jargon, but gloss it once on first use.
- Check: `python3 $K/kit/ste_check.py FILE --max 25` exits 1 and lists every sentence over the
  limit. It reads `.md`, `.txt` and `.html`.

## A, strict ASD-STE100

B's limits (procedure ≤20 words, description ≤25), plus:
- approved-dictionary words where known;
- numbered sections: Function, Operation, Procedure;
- `CAUTION:` / `WARNING:` before the step it protects, as a command, then the risk.

Check with `ste_check.py --max 20` for procedures.

## C, dense engineering

No sentence limit, symbols and `i.e.` inline, jargon glossed once. Fastest to write, slowest to
read. No checker.

The KV-cache sample of all three sits side by side in the user's style gallery (link in their
global instructions).
