# adr-autopsy-011 — Jaeger: Custom Distributions via Public Facade Packages

**Proves:** an ADR's structural claims can be graded against code.

- ADR: `jaegertracing/jaeger` `docs/adr/011-custom-distributions.md`
- Implementing PR: `jaegertracing/jaeger#8800` (+1,410/−41, 102 files)
- Boundary: base `11b08c08` → head `8c5ed8c3`
- Result: 0 responsibility shifts, 0 new smells, metrics flat → **effectiveness +0.75**
- Honest blind spot: Go parser doesn't extract package-level `var` declarations, so the
  87 one-liner facade files (`var NewFactory = impl.NewFactory`) are invisible —
  claims C1/C2 graded UNVERIFIABLE, documented as a parser improvement item.

```bash
python run.py --out ../../docs/reports
```
