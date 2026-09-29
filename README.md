# arcade-agent-examples

Deterministic, reproducible architecture-analysis demos — the same idea as
`mvn-perf/mvn-perf-examples`, but for **software architecture** instead of build time.

Every scenario in `scenarios/` runs with **one command**, locally and in CI, and publishes
its HTML report to GitHub Pages. Numbers are re-generated monthly so they never rot.

## Scenarios

| Scenario | What it proves | Reproduce |
|---|---|---|
| `synthetic-smells` | Planted cycle + god module → refactored → `changelog_architecture` reports 2 resolved, 0 new | `make synthetic` |
| `adr-autopsy-011` | Jaeger ADR-011 verified claim-by-claim against PR #8800 (effectiveness +0.75) | `make adr011` |
| `adr-autopsy-014` | Jaeger ADR-014 as neutral control: behavioral ADR → zero structural delta | `make adr014` |
| `smell-sweeps` | Smell reports for Apache Commons (3 libs), Spring (4 modules), Kafka | `make sweeps` |
| `fork-corpus` | Full language matrix on pinned tuannx forks: clap (rust), cobra (go), hiredis (c) | `make corpus` |

## Corpus references

Small/medium libraries analyzed by `fork-corpus`, pinned by SHA in
[`scenarios/fork-corpus/run.py`](scenarios/fork-corpus/run.py). Reports are
served on GitHub Pages; each report header shows its pinned SHA, and
`corpus_summary.json` links every report to its exact fork commit.

| Target | Fork | Upstream | Report |
|---|---|---|---|
| clap (rust) | [tuannx/clap](https://github.com/tuannx/clap) | [clap-rs/clap](https://github.com/clap-rs/clap) | [corpus_clap.html](https://tuannx.github.io/arcade-agent-examples/reports/corpus_clap.html) |
| cobra (go) | [tuannx/cobra](https://github.com/tuannx/cobra) | [spf13/cobra](https://github.com/spf13/cobra) | [corpus_cobra.html](https://tuannx.github.io/arcade-agent-examples/reports/corpus_cobra.html) |
| hiredis (c) | [tuannx/hiredis](https://github.com/tuannx/hiredis) | [redis/hiredis](https://github.com/redis/hiredis) | [corpus_hiredis.html](https://tuannx.github.io/arcade-agent-examples/reports/corpus_hiredis.html) |

Machine-readable index (fork/upstream URLs + SHAs + metrics):
[`corpus_summary.json`](https://tuannx.github.io/arcade-agent-examples/reports/corpus_summary.json).

## One-command reproduce

```bash
pip install "arcade-agent[languages]"
make all        # runs every scenario, writes reports to docs/reports/
```

A monthly scheduled job runs `make all` and commits the refreshed reports in
`docs/reports/` (GitHub Pages serves `docs/` from `main`).
To refresh manually: `pip install "arcade-agent[languages]" && make all`.

## Referencing this repo

Every report embeds the exact git SHAs analyzed. Cite a scenario like:

> arcade-agent-examples, `adr-autopsy-011`: Jaeger PR #8800 base `11b08c08` → head `8c5ed8c3`,
> 0 responsibility shifts, 0 new smells. Report: <url>

## License

MIT — same as [arcade-agent](https://github.com/arcade-agent/arcade-agent).
