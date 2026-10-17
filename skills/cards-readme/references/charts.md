## Evidence-led charts

Use a chart when it answers a reader's question better than the table alone: benchmark comparisons,
quality versus cost/latency, dataset composition, coverage gaps, or distributions. A chart is optional;
do not add one just to decorate the card.

- **Reuse visualization capabilities.** If the session provides Claude's `dataviz`, a
  `data-visualization` skill, or an equivalent chart tool, use its relevant chart-selection,
  palette-validation and rendering workflow. Resolve the capability available in that session;
  never hardcode a bundled skill's temporary path. Otherwise use an existing plotting package or
  install a suitable tool through the environment's package manager. Do not hand-build a chart
  engine or copy a skill's renderer and validators into this skill.
- **Choose the form before styling.** Compare categories with bars/dots; show distributions with
  histograms/box plots; show quality-cost tradeoffs with scatter plots; show coverage with a heatmap.
  A single number may need only a label. State the useful finding in the title without overstating it.
- **Keep the evidence intact.** Build from the same source data as the adjacent table. Label units,
  sample size, aggregation and whether higher or lower is better. Compare runs only when their
  datasets, conditions and metric definitions match; otherwise separate them. Show uncertainty
  when available, never invent intervals. Keep the source link and exact values accessible.
- **Apply the dataviz checks.** Bar baselines start at zero; use separate panels for different
  scales instead of dual y-axes. Keep entity colors stable, use categorical/sequential/diverging
  colors according to meaning, and distinguish series with labels or shapes as well as color.
  Use the selected tool's palette validator when provided, then inspect the actual export for
  contrast, Vietnamese glyphs, clipped labels and readability. Color validation does not prove layout.
- **Deliver for the card's format.** Embed static chart images for the Hub/GitHub using the image
  patterns in `references/patterns.md`; include meaningful alt text and retain a source table.
  If an interactive version is requested, link it separately and keep the card understandable
  without it. Prefer one useful figure over a dashboard the reader must navigate.
