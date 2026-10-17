# W3 — showcase: results shown, evidence inside

For people who will be **shown** a result and act on it, not taught how it works: an evaluation
report, a benchmark, a capacity test, a status for leadership. W1 explains a mechanism; W3 presents
numbers, and carries enough evidence that nobody has to ask "measured on what?".

Look: brand band with the headline metric, numbered sections on white / pale blue, KPI cards with a
direction chip, comparison bars, real examples with diffs, a method-and-limits section linking the
source run. Light and dark. Fonts: Be Vietnam Pro + IBM Plex Mono (`kit/fonts-showcase.css`,
~200 KB; Vietnamese included; `render.py` downloads it once if the file is missing).

| File | Role |
|---|---|
| `render.py` | `report.json` → page. Checks the evidence contract, then calls `kit/build.py` |
| `showcase.css` | layout + palette, both themes (checked with `validate_palette.mjs`) |
| `showcase.js` | section tabs, report / samples views, sample filters, audio playhead and seek |
| `example.report.json` | worked example, made-up data, every block type and a samples view (`example_audio/tone.wav` stands in for real audio) |

```bash
python3 $K/templates/showcase/render.py report.json out.html --shot shot.png --shot-size 1440x9000 --shot-theme light
```

Same flags as `build.py` for the screenshot. Pages taller than 8,192 px are shot at 1x (2x blanks
the bottom). Set the height to the page height, then look at every part of the image.

## Where report.json lives

The numbers usually come from a run export. Write a small converter (export → `report.json`) next
to the output, not in this repo: real reports carry run ids, internal links and sometimes
transcripts. Keep the converter, so a rerun regenerates the page.

## report.json

Every number on the page lives in this one file. That keeps cards and charts consistent, but
not prose: a sentence that quotes a number agrees with the chart only if the converter formats it
from the export too. Never paste a number into prose by hand. Text fields are HTML (`<b>`
allowed). Example transcripts and turn texts are data and are escaped.

- `meta`: `lang` (`vi` | `en`, sets labels and number format), `title`, `date`, `stamp` (nav pill),
  `brand` {`name`, `sub`, `logo`: image path, relative to report.json or `~/…`}, `footer`.
- `hero`: `kicker`, `title`, `accent` (second line, green), `lede`, `card` {`title`, `tag`},
  `stats` (1–2), `join` (word between them), `facts` (footer strip), `note`.
- `sections[]`: `id`, `nav`, `kicker`, `title`, `lede`, `blocks[]`. Numbered 01, 02… in order;
  backgrounds alternate.
- `method`: `defs[]` {`term`, `html`}, `limits[]`, `run[]` [[label, value]…], `source` {`href`,
  `label`}. Always rendered last.
- `samples` (optional): a second view, "samples to re-check", switched from the nav (`#samples`).
  One card per sample: audio player, reference against every model, metric chip with pass / fail,
  filter by group and status, sort by score, search by id or words. **`selection`** (how the
  samples were picked: all of them, or the rule for a subset) and **`items[]`** {**`id audio`**,
  `group`, `metric`, `pass`, `facts`, then `ref` + `hyps[]` for text, or `tracks` + `turns` for a
  timeline}. `metric` {`label`, `unit`, `digits`}; `legend` and `label_width` for timelines. On a
  timeline a playhead follows the audio, a click on a track seeks there, and a turn's time (`s`,
  seconds) is a button that plays from it.

Audio: `--audio link` (default) copies each file to `OUT_audio/` next to the page; ship the folder
with the page. `--audio embed` inlines it for a one-file page, within the 16 MB cap (about 45 min
of 48 kbps AAC). Large sets: transcode first (the converter's job), e.g.
`ffmpeg -i in.wav -ac 1 -c:a aac -b:a 48k out.m4a`; 3.4 h of speech came to 73 MB.

| Block `type` | Fields (**required**) | Use for |
|---|---|---|
| `kpis` | `items[]`: **`label value better reading basis`**, `tone` (brand/good/warn/bad); `cols` 2–4 | the headline numbers |
| `bars` | **`better`**, `rows[]` {**`label value`**, `sub`, `series`, `hl`, `faint` (too few samples), `text`, `note`} or `groups[]` {`title`, `sub`, `rows`}; **`basis` or every row's `sub`**; `unit`, `digits`, `max`, `ref` {`value`, `label`}, `legend` | a rate per group or per model; `ref` draws the dashed overall line |
| `stack` | **`better parts rows`** (`rows[].values` keyed by part) | an error rate split into its parts |
| `composition` | **`total parts`**, `callout`, `bar_label`, `caption` | what the test set is made of |
| `table` | **`head rows`**, `num` (column indexes), `total_last`, `diag` (confusion matrix), `caption`; a cell may be `{"text", "heat": 0–1}` | exact numbers; shaded cross-tabs |
| `examples` | `items[]`: **`title id ref hyps`** | reference vs outputs; red = differs, struck = left out |
| `timeline` | **`title id duration tracks legend`**, `turns[]` {**`t who text`**, `got`, `ok`}, `start`, `tick`, `label_width` | who spoke when: reference, model, error positions |
| `insights` | `items[]`: `kicker title text tone` | strength / gap cards |
| `tabs` · `details` · `cols` | nested `blocks` | drill-down without a long scroll |
| `quote` · `callout` · `html` | text | one line that frames the section |

`better` is `lower`, `higher` or `none` (a scale such as hours). It must be said out loud for every
number; that is what the chip shows. Series colours: `s1`…`s8`.

## Evidence contract: the build stops without it

`render.py` lists every gap and writes nothing; `build.py` re-checks the HTML (KPI count = direction
chips = basis lines; a `#method` section; a `http(s)` link to the source run).

1. Every headline number and KPI: unit, which way is better, and what it was counted on (n, hours).
2. The hero says what the metric is **not** (`hero.note`).
3. Charts: a direction, and the denominator for each row or the whole chart.
4. Examples and timelines carry the sample id, so a reader can find the audio.
5. The samples view states how the samples were picked; each card has an id and its audio file
   (a missing file stops the build).
6. Method: definitions, at least one limit, at least two run facts, the source-run link.

Prose rules for this style: `../../references/writing.md`, "Presenting results".

## Verify

Build exit 0; screenshot both themes at full page height; check the hero, one chart, one example,
the method section, and `#samples`; open a tab and a `details`, play one sample and click a track. Then the delivery gate in `SKILL.md`.
