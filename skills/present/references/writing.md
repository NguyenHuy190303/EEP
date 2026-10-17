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

## Presenting results (W3 showcase)

The reader is shown a result and acts on it; they will not re-derive it. Every number has to stand
on its own:

- **Value, unit, direction, denominator, together.** "WER 7.40% (lower is better), mean over
  31,204 segments / 48.6 h". Never a bare percentage.
- **One plain reading per rate:** "about 7 of every 100 words are wrong". Then say what it is
  **not**: "not a sentence error rate".
- **Small groups get a warning, not a decimal place:** "2.1 h only; treat as a direction".
- **Comparisons name what was held equal:** same set, same references, same scoring. Otherwise
  do not put the numbers side by side.
- **Real examples, both kinds, with ids:** one that works and one that fails, with the sample id,
  so the claim can be checked.
- **Separate the model's error from the measurement's:** label conventions, normalisation, or
  thresholds that move the number without the model changing.
- **No adjective without a number.** "Better" says by how much, on what.
- **Limits are part of the result:** sample size, how references were made, what was not measured.
