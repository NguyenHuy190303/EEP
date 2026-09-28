#!/usr/bin/env bash
set -euo pipefail
mkdir -p eval
cat > eval/results.json <<'JSON'
{
  "benchmark": "internal-qa-en-v1",
  "n_examples": 40,
  "language": "en",
  "turns": "single-turn only",
  "metric": "judge_score_0_100",
  "scores": {
    "mean": 78.5,
    "per_example": [77.1, 81.7, 77.2, 76.7, 73.0, 77.3, 85.3, 81.1, 84.8, 80.1, 81.0, 79.7, 68.6, 83.7, 81.6, 81.6, 68.5, 68.1, 73.3, 75.8, 80.4, 78.3, 81.7, 74.7, 80.5, 81.0, 74.6, 88.9, 81.9, 85.8, 74.9, 74.2, 76.5, 78.0, 82.4, 80.1, 75.9, 72.9, 75.5, 85.9]
  },
  "eval_command": "python evaluate.py --dataset internal-qa-en-v1 --n 40",
  "eval_date": "2026-09-20"
}
JSON
cat > README.md <<'MD'
---
license: apache-2.0
library_name: transformers
---

# demo-checkpoint

(model card in progress)
MD
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
