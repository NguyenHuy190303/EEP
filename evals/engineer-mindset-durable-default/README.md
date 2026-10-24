# engineer-mindset: durable default vs explicit urgency

A manual eval case, not in `claude plugin eval` format. The question is whether the skill builds the
long-term, resource-saving shape when the user does not say the work is urgent, and switches to a
labelled quick fix only when they do.

## Prompts (Vietnamese, as run)

**N (not urgent):**

> Dashboard eval nội bộ (FastAPI + React) load chậm: mỗi request `/runs` gọi
> `load_dataset("org/asr-eval-results")` rồi tính lại WER/DER cho mọi run, mất ~20 s. Kết quả trên
> HF Hub private, mỗi ngày thêm vài run mới. Sửa giúp.

**U (urgent):** the same prompt with "Gấp, chiều nay demo cho sếp." prepended.

No fixture. Each arm is a fresh subagent that may read only the skill files it is given.

## Checklist N (6 points)

1. Names the source of truth (the Hub dataset at a revision) and keeps no unkeyed copy as a second
   source.
2. Caches finished runs by revision (immutable, no TTL needed) instead of recomputing per request.
3. Each cache layer it proposes states key, invalidation, bound and a hit-rate or latency signal.
4. Incremental: only new runs (or a new metric) are computed; aggregation is not redone over all
   history per request.
5. Reads in place (`hf://`/DuckDB/streaming, column pruning) rather than a full download.
6. Ends with at most three next improvements with effort/payoff, and does not refactor beyond scope.

## Checklist U (4 points)

1. Gives the fastest working fix (e.g. compute once at startup or memoize, precompute file).
2. Labels it `tactical` with an exit condition.
3. Names the durable follow-up in one line.
4. Does not build multi-layer caching or a new storage layout now.

## Results

See `results.md` beside this file.
