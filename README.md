# arcade-agent-examples

Deterministic, reproducible architecture-analysis demos — the same idea as
`mvn-perf/mvn-perf-examples`, but for **software architecture** instead of build time.

Every scenario in `scenarios/` runs with **one command**, locally and in CI, and publishes
its HTML report to GitHub Pages. Numbers are re-generated monthly by CI so they never rot.

## Scenarios

| Scenario | What it proves | Reproduce |
|---|---|---|
| `synthetic-smells` | Planted cycle + god module → refactored → `changelog_architecture` reports 2 resolved, 0 new | `make synthetic` |
| `adr-autopsy-011` | Jaeger ADR-011 verified claim-by-claim against PR #8800 (effectiveness +0.75) | `make adr011` |
| `adr-autopsy-014` | Jaeger ADR-014 as neutral control: behavioral ADR → zero structural delta | `make adr014` |
| `smell-sweeps` | Smell reports for Apache Commons (3 libs), Spring (4 modules), Kafka | `make sweeps` |

## One-command reproduce

```bash
pip install "arcade-agent[languages]"
make all        # runs every scenario, writes reports to docs/reports/
```

CI (`.github/workflows/refresh.yml`) runs `make all` on a monthly cron and deploys
`docs/` to GitHub Pages.

## Referencing this repo

Every report embeds the exact git SHAs analyzed. Cite a scenario like:

> arcade-agent-examples, `adr-autopsy-011`: Jaeger PR #8800 base `11b08c08` → head `8c5ed8c3`,
> 0 responsibility shifts, 0 new smells. Report: <url>

## License

MIT — same as [arcade-agent](https://github.com/arcade-agent/arcade-agent).
