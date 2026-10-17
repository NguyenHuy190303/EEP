## Dataset columns — order is the first thing a reader sees

The Hub viewer shows columns in **parquet schema order**. The card's field table does not change it.
Set the order in the script that writes the parquet (`table.select(cols)`, `ds.select_columns(cols)`,
`df[cols]`); keep the field table and any `dataset_info.features` in the same order. If a pushed
dataset is wrong, rewrite the parquet — reordering the card alone fixes nothing.

1. **Media** — `audio`, `image`, `video`. Always column 0: the viewer row opens with the player.
2. **Target / label** — `text`, `rttm`, `segments`, `label`, `term`: what the row is for.
3. **Facets people filter on** — `speaker_id`, `gender`, `region`, `domain`, `source`, `tier`, `duration`.
4. **Per-row provenance** — `label_source`, `annotated_by`, `reviewed_by`, `review_status`.
5. **Ids, hashes, paths, technical** — `id`, `*_id`, `*_sha256`, `path`, `url`, `sample_rate`,
   `channels`. Last, as one block.

`speaker_id` is the one `_id` that stays with the facets. `check_card.py --data` enforces 1 and 5.

## Provenance — every label says who or what made it, and how to rerun it

Dataset cards get a `## Provenance and reproduction` section: one row per build stage or label column.

| Column / stage | Produced by | Code or tool | Reviewed by | Date | Rows |
|---|---|---|---|---|---|
| `text` | STT `acme-asr-v3-step78000-fp16` (staging) | `acme/speech-data@40fd576` `scripts/x.py --split test` | A. Reviewer, B. Reviewer — Label Studio project `diarization-review`, export 2026-10-09 | 2026-10-09 | 1,425 / 1,425 |
| `rttm` | human, hand-drawn | Label Studio export `golden_test_set` | A. Reviewer | 2026-10-07 | 117 |

- **Code**: `org/repo@commit` + path + the exact command. Never a local path (`/Users/...`, `/tmp/...`):
  it resolves on no other machine, and workspace scripts get deleted after porting.
- **Model labels**: exact model id and revision used at run time, not the endpoint name — an endpoint
  can switch models mid-run.
- **LLM labels**: model, thinking level, prompt file at a commit.
- **Human labels**: reviewers by name, the tool (Label Studio project + export file + date, or the QC
  page and its localStorage key), and how many rows they reviewed out of how many.
- **Unknown**: write `not recorded` in the cell. Keep the row — missing provenance is information.
