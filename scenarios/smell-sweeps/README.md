# smell-sweeps

**Proves:** arcade-agent scales to real-world codebases in seconds.

| Target | Entities | Smells | Time |
|---|---|---|---|
| apache/commons-lang | 2,820 | 22 | 0.6s |
| apache/commons-io | 2,072 | 13 | 0.4s |
| apache/commons-collections | 3,578 | 21 | 0.6s |
| spring-core / beans / context / web | 5.4k / 2.6k / 3.5k / 5.7k | 11 / 15 / 11 / 17 | <2s each |
| apache/kafka (java) | 31,450 | 11 | 11.5s |

Headline findings live in the per-target reports. All targets are pinned by SHA inside
`run.py` so re-runs are deterministic.

```bash
python run.py --out ../../docs/reports
```
