# fork-corpus

**Proves:** arcade-agent covers the full language matrix on real small/medium
libraries — Rust, Go, and C complete the Python/Java/Kotlin/TypeScript set
already exercised elsewhere.

| Target | Fork | Upstream | Entities | Smells | Time |
|---|---|---|---|---|---|
| clap (rust) | [tuannx/clap](https://github.com/tuannx/clap) | [clap-rs/clap](https://github.com/clap-rs/clap) | 1,872 | 1 | ~6s |
| cobra (go) | [tuannx/cobra](https://github.com/tuannx/cobra) | [spf13/cobra](https://github.com/spf13/cobra) | 285 | 0 | ~3s |
| hiredis (c) | [tuannx/hiredis](https://github.com/tuannx/hiredis) | [redis/hiredis](https://github.com/redis/hiredis) | 742 | 2 | ~4s |

Reports: `corpus_clap.html`, `corpus_cobra.html`, `corpus_hiredis.html`,
plus `corpus_summary.json` with fork/upstream URLs and pinned SHAs.
All targets are pinned by SHA inside `run.py` so re-runs are deterministic.

Notes:

- clap is a Cargo workspace; repo-root ingest recovers 9 components.
- cobra's flat package layout recovers one component per file with `pkg`;
  try `wca`/`acdc` for coarser clustering on Go targets.

```bash
python run.py --out ../../docs/reports
```
