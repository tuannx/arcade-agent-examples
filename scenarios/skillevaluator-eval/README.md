# skillevaluator-eval

**Proves:** arcade-agent measures a real, forked upstream project end-to-end —
the same self-analysis job Arcade uses to score its own PRs — with every number
traceable to one pinned commit.

| Target | Fork | Upstream | Entities | Components | Smells | BalancedScore |
|---|---|---|---|---|---|---|
| SkillEvaluator (python) | [tuannx/SkillEvaluator](https://github.com/tuannx/SkillEvaluator) | [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) | 3,339 | 26 | 7 | 0.5624 |

Reports: `skillevaluator.html` (full interactive report),
`skillevaluator_analysis.json` (complete run artefact)
and `skillevaluator_summary.json` (digest with fork/upstream URLs and pinned SHA).
The target is pinned to `f32c884` inside `run.py` so re-runs are deterministic.

What the run shows (structural observations from static analysis — signals to
confirm with the maintainers, not quality verdicts):

- The largest recovered component is **Tier3** (333 of 642 architectural
  entities); it also carries the only high-severity Concern Overload.
- Two dependency cycles: Tier3↔Utils (low) and
  Deduplication–Embedding–Validators (medium).
- Issue
  [#149](https://github.com/NVIDIA/SkillEvaluator/issues/149) documents a
  separate Tier 3 scoring issue (`check_error_recovery` scores unrecovered
  command failures as first-attempt clean); the fix
  [PR #151](https://github.com/NVIDIA/SkillEvaluator/pull/151) is under
  maintainer review. It affects Tier 3 live-scoring trust only — the static
  Tier 1/2 results and this architecture measurement are unaffected.

```bash
make skillevaluator   # clone the pinned fork, run, write docs/reports/
# or: python run.py --out ../../docs/reports
```
