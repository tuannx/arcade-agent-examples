"""Synthetic deterministic demo (mvn-perf style): planted smells -> refactor.

- synthetic/before : billing<->notifications cycle + utils god module
- synthetic/after  : cycle broken via events, god module split
Runs analyze on both, computes changelog_architecture, writes JSON + HTML.

Usage: python run.py [--out docs/reports]
"""
import argparse
import json
import os
import time
from pathlib import Path

SCEN = Path(__file__).resolve().parent
SYN = SCEN / "synthetic"
DEFAULT_OUT = SCEN.parents[1] / "docs" / "reports"


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("AAE_OUT", str(DEFAULT_OUT)))
    return ap.parse_args()


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    return str(o)


def main():
    from arcade_agent.source.ingest import ingest
    from arcade_agent.tools.parse import parse
    from arcade_agent.tools.recover import recover
    from arcade_agent.tools.detect_smells import detect_smells
    from arcade_agent.tools.compute_metrics import compute_metrics
    from arcade_agent.tools.changelog_architecture import changelog_architecture
    from arcade_agent.tools.visualize import visualize

    OUT = Path(parse_args().out)
    OUT.mkdir(parents=True, exist_ok=True)

    versions = {}
    for label in ("before", "after"):
        src = SYN / label
        print(f"[{label}] ...", flush=True)
        t0 = time.time()
        repo = ingest(str(src), language="python")
        graph = parse(repo.path, language="python")
        arch = recover(graph, algorithm="pkg")
        smells = detect_smells(arch, graph)
        metrics = compute_metrics(arch, graph)
        dt = time.time() - t0
        versions[label] = dict(graph=graph, arch=arch, smells=smells, metrics=metrics)
        print(f"  entities={len(graph.entities)} edges={len(graph.edges)} "
              f"components={len(arch.components)} smells={len(smells)} in {dt:.1f}s",
              flush=True)
        for sm in smells:
            print(f"    smell: {sm.smell_type} [{sm.severity}] "
                  f"{','.join(sm.affected_components)}", flush=True)
        rep = OUT / f"synthetic_{label}.html"
        try:
            visualize(f"arch-demo ({label})", label, graph, arch, smells,
                      output=str(rep))
            print(f"  report: {rep.name}", flush=True)
        except Exception as e:
            print(f"  visualize failed: {e}", flush=True)

    print("[changelog] ...", flush=True)
    cl = changelog_architecture(
        versions["before"]["arch"], versions["before"]["graph"],
        versions["after"]["arch"], versions["after"]["graph"],
        smells_a=versions["before"]["smells"], smells_b=versions["after"]["smells"],
        metrics_a=versions["before"]["metrics"], metrics_b=versions["after"]["metrics"],
        ref_a="before (planted smells)", ref_b="after (refactored)",
    )
    summary = {
        "demo": "synthetic deterministic arch-demo",
        "before_stats": {
            "entities": len(versions["before"]["graph"].entities),
            "edges": len(versions["before"]["graph"].edges),
            "components": len(versions["before"]["arch"].components),
            "smells": len(versions["before"]["smells"]),
        },
        "after_stats": {
            "entities": len(versions["after"]["graph"].entities),
            "edges": len(versions["after"]["graph"].edges),
            "components": len(versions["after"]["arch"].components),
            "smells": len(versions["after"]["smells"]),
        },
        "changelog": clean(cl),
    }
    (OUT / "synthetic_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["changelog"].get("summary", {}), indent=2))
    print("DONE")


if __name__ == "__main__":
    main()
