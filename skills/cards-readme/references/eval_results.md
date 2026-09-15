# `.eval_results/*.yaml` — structured eval scores on the Hub

Source: https://huggingface.co/docs/hub/eval-results (fetched 2026-09-15; the page is marked
"work in progress"). Spec file: https://github.com/huggingface/hub-docs/blob/main/eval_results.yaml

Scores live in the model repo under `.eval_results/<anything>.yaml`. They appear on the model page and
aggregate into the benchmark dataset's leaderboard. The dataset must be registered as a Benchmark
(has `eval.yaml`; e.g. `cais/hle`, `TIGER-Lab/MMLU-Pro`, `Idavidrein/gpqa`, `openai/gsm8k`).

```yaml
- dataset:
    id: Idavidrein/gpqa        # required, must be a Benchmark dataset
    task_id: gpqa_diamond      # required, from the dataset's eval.yaml
    revision: <hash>           # optional
  value: 0.412                 # required
  date: "2026-09-10"           # optional ISO-8601, defaults to commit time
  source:                      # optional but the card's results table should point here
    url: https://huggingface.co/spaces/you/eval-traces
    name: Eval traces
  notes: "no-tools"
```

Badges the Hub adds: `verified` (has a valid `verifyToken` — eval ran in HF Jobs with inspect-ai),
`community` (submitted via an open PR), `leaderboard`, `source`.

Legacy `model-index` in the README frontmatter is still rendered; use it for benchmarks that are not
registered. Field shape is in `modelcard_spec.md`.

Running the evals themselves: skill `huggingface-community-evals` (local) or `hf jobs` via hf-cli.
