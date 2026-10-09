# Autoharness for maintainers

Run this on your repo first:

```yaml
# .github/workflows/arch-drift.yml
- uses: arcade-agent/arcade-agent/actions/analyze@v0.3.0
  with:
    arcade-agent-version: "0.3.0"
```

Same pin on the org action:

```yaml
- uses: arcade-agent/analyze-action@v1
  with:
    arcade-agent-version: "0.3.0"
```

Or locally:

```bash
pip install "arcade-agent[languages]==0.3.0"
arcade-self-analysis --source . --output-html report.html --output-json report.json
```

This repo installs that release from `analyzer-pin.json` (`make install`).
Pin decision: [ADR 0001](docs/adr/0001-pin-arcade-agent-release.md).

## Latest runs — numbers first

| Repo | Entities | Time | Latest PR verdict |
|---|---|---|---|
| [Django](https://tuannx.github.io/django/) | 10,881 | 6.3s | django/django#18036 — SAFE FEATURE |
| [React](https://tuannx.github.io/react/) | 7,861 | 8.4s | facebook/react#37187 — SAFE, -19,239 lines |
| [Vue](https://tuannx.github.io/core/) | 1,630 | 1.4s | vuejs/core#15633 — 5 SHIFTS |

Each number links to a fork Pages with the full report. Report is the product.

## What the harness does daily

1. Scan upstream PRs: >500 lines, >20 files, >15 comments
2. Run `changelog_architecture` base vs head in 2-8 minutes
3. Publish ADHD report to the fork Pages — 5 lines to read
4. Mention upstream as `facebook/react#37187` in this repo only
5. Maintainer decides. No bot comments upstream.

## Try a scenario in 1 command

```bash
make install
make synthetic   # 0.2s, 2 smells → 0
make all         # routine scenarios, reports in docs/reports/
make react33152  # facebook/react#33152 (own target, full checkout)
```

## For maintainers

1. Add the workflow above — 2 minutes, no code change
2. Next PR gets 1 comment: verdict, 3 numbers, 1 thing to look at
3. Remove the workflow to opt out. No lock-in.

MIT · [arcade-agent](https://github.com/arcade-agent/arcade-agent)
