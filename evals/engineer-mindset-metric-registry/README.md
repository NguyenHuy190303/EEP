# engineer-mindset: metric registry and data-driven view

A manual eval case, not in `claude plugin eval` format. The question is whether a model with the
skill designs an eval dashboard where a new metric is one registry entry, aggregates ratio metrics
correctly, and reads the Hub dataset in place instead of copying it to disk.

## Prompt (Vietnamese, as run)

> Team ASR có script eval: `load_dataset("org/asr-eval")` rồi `save_to_disk`, tính WER và DER bằng
> jiwer/pyannote, ghi `results.json` `{model, wer, der}`. FE React hard-code type `{model; wer; der}`
> và 2 cột WER, DER. Sắp thêm KER (keyword error rate), sau này còn thêm metric nữa. Dataset và kết
> quả để trên Hugging Face Hub (private). Thiết kế lại cho dễ bảo trì: trước/sau, code ngắn cho
> Python và FE.

No fixture. Each arm is a fresh subagent with no repository access beyond the skill files it is
given. The skill arm reads `skills/engineer-mindset/SKILL.md` and only the references it routes to.

## Checklist (8 points)

1. One registry defines each metric once with label, unit and direction; every layer iterates it.
2. Ratio metrics keep numerator and denominator and aggregate as sum/sum, not a mean of per-sample
   WER/DER.
3. Results stored long (one row per metric), or the answer names the wide-schema mismatch across
   runs/shards.
4. Reads the Hub in place (`hf://` with DuckDB/Polars, or streaming) instead of `save_to_disk`, and
   pins a revision.
5. FE builds columns, headers and formatting from descriptors in the response; unknown unit and
   missing value have a fallback.
6. The HF token stays server-side.
7. States that adding KER touches one place and zero FE code.
8. No speculative machinery: no plugin framework, DI container or ABC hierarchy with one
   implementation.

## Results

See `results.md` beside this file.
