# adr-autopsy-014 — Jaeger: Synchronous Elasticsearch writes (control)

**Proves:** the method doesn't hallucinate architectural impact for behavioral ADRs.

- ADR: `jaegertracing/jaeger` `docs/adr/014-synchronous-elasticsearch-writes.md`
- Implementing PR: `jaegertracing/jaeger#9093` (+178/−17, 7 files)
- Result: +4 entities, 0 shifts, 0 new smells, metrics flat → **neutral, as promised**

```bash
python run.py --out ../../docs/reports
```
