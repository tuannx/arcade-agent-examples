# OSS evaluations — November 2026

Deterministic architecture analysis of large open-source codebases with
[arcade-agent](https://github.com/arcade-agent/arcade-agent) 0.4.2.
Same input, same verdict, every run. No LLM judge.

15 codebases scanned. Every one had at least one high-severity
dependency cycle at its core. Three of them:

## Neon — serverless PostgreSQL (Rust)

- 12,742 entities · 53 components · 25,412 edges
- **Dependency cycle, high severity, spanning 26 components**
  (ComputeApi, ControlPlane, Pageserver, PageserverApi, …)
- `Utils` is depended on by 27 components (52% of the system)
- RCI 0.7528 · Balanced 0.5519 · 9 smells
- Run: https://github.com/tuannx/neon/actions/runs/44942347349

## AWS Advanced JDBC Wrapper (Java)

- 4,565 entities · 16 components · 8,798 edges
- **Dependency cycle, high severity, spanning 14 of 16 components**
- `Util` is depended on by 13 components — **87% of the system**
- Balanced 0.3386, the lowest of the 15 · RCI 0.4300 · 17 smells (11 high)
- Run: https://github.com/tuannx/aws-advanced-jdbc-wrapper/actions/runs/44942389244

## CloudNativePG — Kubernetes PostgreSQL operator (Go)

- 3,567 entities · 30 components · 6,549 edges
- **Dependency cycle, high severity, spanning 18 components**
- Balanced 0.4982 (Poor) · RCI 0.6819 · 8 smells
- Run: https://github.com/tuannx/cloudnative-pg/actions/runs/44940629207

## Why this matters for agent-written code

A dependency cycle at the core scatters related code across the whole
graph. An agent working in that codebase has to pull far-apart context
into every task — more tokens per task, more chances to break a
distant dependent. Structure is not a style preference; it is a
per-task cost.

Reproduce any of these: add the workflow to a fork and run it.

```yaml
- uses: arcade-agent/arcade-agent/actions/analyze@v0.4.2
```
