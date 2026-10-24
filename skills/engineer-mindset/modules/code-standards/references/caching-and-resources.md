# Caching and resources

Pay once, reuse many times: every piece of data, compute and definition has one owner, and
everything else reads it, caches it by key or derives from it. The repository's existing cache
layer, store and SDK win over a new one.

## Source of truth first

- Name the owner of each input before adding a cache or copy: the dataset revision on the Hub, the
  table in the warehouse, the registry in code. Every other copy is a cache of that owner.
- Read in place with the owner's SDK or query engine (`hf://` with DuckDB/Polars, `datasets`
  streaming, warehouse SQL, object-store range reads) and pin a revision or snapshot.
- A cache that cannot be rebuilt from its owner is a second source of truth; give it a backup and an
  owner, or make it rebuildable.

## When to cache

- **Immutable by revision** (pinned dataset, model checkpoint, a finished run's results, build
  artifacts): cache by default. Key = source revision + code/config version that shaped the value;
  such a key never goes stale, so it needs no TTL, only a size bound and eviction.
- **Mutable** (live tables, user state, upstream APIs): cache only on a hot path shown by a measured
  repeat rate or latency, or by an obvious structural repeat (every request re-reads the same file).
  State the staleness the product accepts and invalidate on write or by TTL within that bound.
- Measure before and after: latency p50/p95, hit rate, upstream calls saved, memory/disk used.

## Layers

Add a layer only when the one below it is measured as too slow or too costly. For each layer state
key, invalidation, size bound, hit-rate metric, and what a miss or failure does.

| Layer | Typical use | Invalidation | Watch for |
|---|---|---|---|
| In-process (LRU, `functools.lru_cache`, memo) | Hot keys within one process | Process lifetime, key includes revision | Unbounded growth, per-worker duplication |
| Local disk (HF cache, parquet/Arrow files) | Large immutable blobs per host | Content or revision key | Disk fill, cleanup policy |
| Shared (Redis, object store, materialized table) | Cross-process, cross-host reuse | Revision key, TTL or write-through | Stampede on cold key, network latency |
| HTTP/CDN (`Cache-Control`, `ETag`) | Responses to many clients | `ETag` from revision, `max-age` | Caching private data, missing `Vary` |

- A miss or a failed cache read falls through to the owner, guarded by single-flight or a lock per
  key so a cold key triggers one upstream fetch, not one per request.
- Retries live at one layer, the one closest to the owner.

## Incremental compute

- Memoize results per `(item, step or metric, input revision, code version)`. A new metric computes
  only itself over existing runs; a code change recomputes only the steps whose version changed.
- Store intermediate outputs that cost more to recompute than to keep (transcripts before scoring,
  embeddings before indexing), keyed the same way.
- Batch and stream large inputs; read only the columns and partitions the step needs.

## Fewer duplicates

- Data: one stored copy per revision; derived tables are rebuildable from it.
- Compute: one job per key; concurrent requests for the same key share it.
- Definitions: one registry or config per concept (see
  [object design](object-design.md#open-sets-one-registry)); use the SDK or library that already
  does the job before writing a wrapper.

## Done when

The owner of each input is named; every cache has key, invalidation, bound and a hit-rate signal;
a rerun with unchanged inputs performs no upstream reads or recompute; adding one metric or step
computes only that metric or step.

## Smells and the smallest fix

| Smell | Smallest in-scope fix |
|---|---|
| `save_to_disk`/download copy that is never refreshed | Read in place at a pinned revision, or key the copy by revision |
| Cache key without revision or code version | Add both to the key |
| Cache used as the only copy of a value | Make it rebuildable from the owner, or promote it to a stored source with an owner |
| Unbounded dict or memo on a long-lived process | Bounded LRU with a size metric |
| Every layer retries the upstream | Keep retries at the layer closest to the owner |
| Whole run recomputed for one new metric | Memoize per item × metric × revision |
