"""ADR-014 verification: jaegertracing/jaeger PR #9093 (base vs head).

Small neutral control: a behavioral ADR (synchronous Elasticsearch writes)
should produce ~zero structural delta. Proves the method doesn't hallucinate
architectural impact.

Usage: python run.py [--out docs/reports]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCEN = Path(__file__).resolve().parent
ROOT = SCEN.parents[1]
sys.path.insert(0, str(ROOT))

from scenarios.analyzer_pin import write_summary

CACHE = SCEN / "repos"
WORK = SCEN / "worktrees"
DEFAULT_OUT = ROOT / "docs" / "reports"

URL = "https://github.com/jaegertracing/jaeger.git"
BASE = "e25782b69e8b071828f2f79f62383eca80e8c3cd"
HEAD = "f4c6acf1133dfe16e768723353807c9b8fa2ba98"


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def ensure_clone():
    repo = CACHE / "jaeger"
    if not (repo / ".git").exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        print("[clone] jaegertracing/jaeger (shallow)...", flush=True)
        subprocess.run(["git", "clone", "--depth", "1", URL, str(repo)], check=True)
    return repo


def materialize(repo, sha, dest):
    dest = Path(dest)
    if dest.exists():
        return dest
    WORK.mkdir(parents=True, exist_ok=True)
    sh("git", "fetch", "--depth", "1", "origin", sha, cwd=repo)
    sh("git", "worktree", "add", "--detach", str(dest), sha, cwd=repo)
    return dest


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

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("AAE_OUT", str(DEFAULT_OUT)))
    OUT = Path(ap.parse_args().out)
    OUT.mkdir(parents=True, exist_ok=True)

    repo = ensure_clone()
    versions = {}
    for label, sha in (("base", BASE), ("head", HEAD)):
        wt = WORK / f"jaeger014-{label}"
        print(f"[{label}] materializing {sha[:8]}...", flush=True)
        materialize(repo, sha, wt)
        t0 = time.time()
        ing = ingest(str(wt), language="go")
        graph = parse(ing.path, language="go")
        arch = recover(graph, algorithm="pkg")
        smells = detect_smells(arch, graph)
        metrics = compute_metrics(arch, graph)
        dt = time.time() - t0
        versions[label] = dict(graph=graph, arch=arch, smells=smells, metrics=metrics)
        print(f"  entities={len(graph.entities)} edges={len(graph.edges)} "
              f"components={len(arch.components)} smells={len(smells)} in {dt:.1f}s",
              flush=True)
        try:
            visualize(f"jaeger {label} (ADR-014 #{9093})", label, graph, arch,
                      smells, output=str(OUT / f"adr014_{label}.html"))
        except Exception as e:
            print(f"  visualize failed: {e}", flush=True)

    print("[changelog] ...", flush=True)
    cl = changelog_architecture(
        versions["base"]["arch"], versions["base"]["graph"],
        versions["head"]["arch"], versions["head"]["graph"],
        smells_a=versions["base"]["smells"], smells_b=versions["head"]["smells"],
        metrics_a=versions["base"]["metrics"], metrics_b=versions["head"]["metrics"],
        ref_a="base e25782b6", ref_b="head f4c6acf1 (PR #9093)",
    )
    summary = {
        "adr": "jaegertracing/jaeger ADR-014: synchronous Elasticsearch writes",
        "pr": "https://github.com/jaegertracing/jaeger/pull/9093",
        "base": BASE, "head": HEAD,
        "base_stats": {
            "entities": len(versions["base"]["graph"].entities),
            "edges": len(versions["base"]["graph"].edges),
            "components": len(versions["base"]["arch"].components),
            "smells": len(versions["base"]["smells"]),
        },
        "head_stats": {
            "entities": len(versions["head"]["graph"].entities),
            "edges": len(versions["head"]["graph"].edges),
            "components": len(versions["head"]["arch"].components),
            "smells": len(versions["head"]["smells"]),
        },
        "changelog": clean(cl),
    }
    write_summary(OUT / "adr014_summary.json", summary)
    print(json.dumps(summary["changelog"].get("summary", {}), indent=2))
    print("DONE")


if __name__ == "__main__":
    main()
