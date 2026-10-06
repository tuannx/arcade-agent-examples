# pr-react-33152 — facebook/react#33152

**Proves:** a feature PR can be graded base vs head from pinned commits.

- PR: [facebook/react#33152](https://github.com/facebook/react/pull/33152)
- Issue: [tuannx/arcade-agent-examples#1](https://github.com/tuannx/arcade-agent-examples/issues/1)
- Boundary: base `2b4064eb9b40f65d20a03ce93b246ad762d562e6` → head `b5f88376aace22604c0694463bdbc96f23635c89`
- Overview uses auto `pkg` depth. `pkg_depth=2` is the packages.* view.
- Not part of `make all`. The checkout is the full React tree at two commits.

```bash
make react33152
```

Reports: `docs/reports/pr_react-33152.html`, `pr_react-33152.json`.
