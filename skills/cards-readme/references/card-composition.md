## What makes it read as top-tier

- **Hero block**: centered name, one-line tagline that says what it is *for*, one row of ≤6 badges
  (license, base model, paper, demo, downloads), optional one hero image ≤1 MB.
- **Highlights**: 3–5 bullets, each a concrete claim with a number or a named capability. No adjectives
  without a noun to hold them.
- **Quickstart** within the first screen: one code block that runs as-is, pinned to the library version
  that actually works (`transformers>=4.51` style), with the known-failure error text if there is one.
- **Spec table** instead of prose for size, context length, tokenizer, dtype, hardware footprint
  (use hf-mem for the memory row).
- **Results table** with a source column. Bold the best per row only when the comparison is like-for-like.
- **Collapsible `<details>`** for long training config, full eval breakdowns, prompt templates.
- **Limitations and intended use** stay short and specific — "trained on Vietnamese legal text; not
  evaluated on medical" beats a generic ethics paragraph.
- Dataset cards additionally lead with a **row example** and a **field table** (name, type, description,
  in schema order), then splits/sizes, then how it was built (source → filter → dedup, with counts at
  each stage), then provenance.
