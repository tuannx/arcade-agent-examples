"""Fork corpus: small/medium libraries pinned from tuannx forks.

Deterministic: every target is cloned from the arcade-agent org fork and pinned to a
git SHA, checked out in a cached shallow clone before analysis. The summary
records fork + upstream URLs alongside each SHA so every number is traceable
to an exact commit.

Usage: python run.py [--out docs/reports] [--only clap,cobra]
"""
import argparse
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
DEFAULT_OUT = ROOT / "docs" / "reports"

TARGETS = {
    "clap": {
        "url": "https://github.com/arcade-agent/clap.git",
        "upstream": "https://github.com/clap-rs/clap.git",
        "sha": "6cde7384bc47913bdbf456cd2f0e3ebb94cb3557",
        "language": "rust",
    },
    "cobra": {
        "url": "https://github.com/arcade-agent/cobra.git",
        "upstream": "https://github.com/spf13/cobra.git",
        "sha": "adbc8813901bba65827259daa8e22ff94ec1f30e",
        "language": "go",
    },
    "hiredis": {
        "url": "https://github.com/arcade-agent/hiredis.git",
        "upstream": "https://github.com/redis/hiredis.git",
        "sha": "058ebcdf36c5b05b759c613564fb958ec363c90f",
        "language": "c",
    },
}


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def ensure_pinned(name, spec):
    # one cached clone per fork, pinned to the recorded SHA
    key = spec["url"].rsplit("/", 1)[-1].replace(".git", "")
    repo = CACHE / key
    if not (repo / ".git").exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        print(f"[clone] {spec['url']} (shallow)...", flush=True)
        subprocess.run(["git", "clone", "--depth", "1", spec["url"], str(repo)],
                       check=True)
    sh("git", "fetch", "--depth", "1", "origin", spec["sha"], cwd=repo)
    sh("git", "checkout", "--detach", spec["sha"], cwd=repo)
    return repo


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
    from arcade_agent.tools.visualize import visualize

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("AAE_OUT", str(DEFAULT_OUT)))
    ap.add_argument("--only", default="",
                    help="comma-separated subset of targets to run")
    args = ap.parse_args()
    OUT = Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)
    only = {t.strip() for t in args.only.split(",") if t.strip()}

    results = {}
    for name, spec in TARGETS.items():
        if only and name not in only:
            continue
        print(f"[{name}] ...", flush=True)
        repo = ensure_pinned(name, spec)
        t0 = time.time()
        ing = ingest(str(repo), language=spec["language"])
        graph = parse(ing.path, language=spec["language"])
        arch = recover(graph, algorithm="pkg")
        smells = detect_smells(arch, graph)
        metrics = compute_metrics(arch, graph)
        dt = time.time() - t0
        by_type = {}
        for sm in smells:
            by_type[sm.smell_type] = by_type.get(sm.smell_type, 0) + 1
        print(f"  entities={len(graph.entities)} edges={len(graph.edges)} "
              f"components={len(arch.components)} smells={len(smells)} "
              f"in {dt:.1f}s", flush=True)
        results[name] = {
            "fork": spec["url"].removesuffix(".git"),
            "upstream": spec["upstream"].removesuffix(".git"),
            "sha": spec["sha"],
            "language": spec["language"],
            "entities": len(graph.entities),
            "edges": len(graph.edges),
            "components": len(arch.components),
            "smells": len(smells),
            "smell_types": by_type,
        }
        try:
            version = f"{name}@{spec['sha'][:8]}"
            visualize(f"{name} (fork corpus)", version, graph, arch, smells,
                      output=str(OUT / f"corpus_{name}.html"))
        except Exception as e:
            print(f"  visualize failed: {e}", flush=True)

    write_summary(OUT / "corpus_summary.json", {"targets": results})
    for name, r in results.items():
        print(f"  {name}: {r['entities']} entities, {r['smells']} smells")
    print("DONE")


if __name__ == "__main__":
    main()
