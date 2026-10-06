"""Smell sweeps: Apache Commons, Spring modules, Kafka.

Deterministic: every target is pinned to a git SHA, checked out in a cached
shallow clone before analysis. Spring is analyzed per-module with explicit
source_root (repo-root ingest finds zero entities on multi-module Gradle).
Kafka excludes docker/ and examples/ (non-production noise).

Usage: python run.py [--out docs/reports] [--only commons-lang,spring-web]
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
    "commons-lang": {
        "url": "https://github.com/apache/commons-lang.git",
        "sha": "29624cdb50ecd794207d561345b2fc9ca3a9d326",
        "language": "java",
    },
    "commons-io": {
        "url": "https://github.com/apache/commons-io.git",
        "sha": "2c6bf8dea065e96651661d5e277e35b2f343d879",
        "language": "java",
    },
    "commons-collections": {
        "url": "https://github.com/apache/commons-collections.git",
        "sha": "a350e2c73bf61230afad1bf6f3dc770b2ddb36ee",
        "language": "java",
    },
    "spring-core": {
        "url": "https://github.com/spring-projects/spring-framework.git",
        "sha": "93ff61fb1ff9b30654d5b44f488887ce100974f1",
        "language": "java",
        "module": "spring-core",
    },
    "spring-beans": {
        "url": "https://github.com/spring-projects/spring-framework.git",
        "sha": "93ff61fb1ff9b30654d5b44f488887ce100974f1",
        "language": "java",
        "module": "spring-beans",
    },
    "spring-context": {
        "url": "https://github.com/spring-projects/spring-framework.git",
        "sha": "93ff61fb1ff9b30654d5b44f488887ce100974f1",
        "language": "java",
        "module": "spring-context",
    },
    "spring-web": {
        "url": "https://github.com/spring-projects/spring-framework.git",
        "sha": "93ff61fb1ff9b30654d5b44f488887ce100974f1",
        "language": "java",
        "module": "spring-web",
    },
    "kafka": {
        "url": "https://github.com/apache/kafka.git",
        "sha": "800676c2e366bac8f32625697c67b68db5a817a1",
        "language": "java",
        "exclude_dirs": ["docker", "examples"],
    },
}


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def ensure_pinned(name, spec):
    # one cached clone per upstream repo, pinned to the recorded SHA
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
        kwargs = {"language": spec["language"]}
        if spec.get("module"):
            kwargs["source_root"] = str(
                repo / spec["module"] / "src" / "main" / "java")
        if spec.get("exclude_dirs"):
            kwargs["exclude_dirs"] = spec["exclude_dirs"]
        t0 = time.time()
        ing = ingest(str(repo), **kwargs)
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
            "sha": spec["sha"],
            "entities": len(graph.entities),
            "edges": len(graph.edges),
            "components": len(arch.components),
            "smells": len(smells),
            "smell_types": by_type,
        }
        try:
            visualize(f"{name} (smell sweep)", name, graph, arch, smells,
                      output=str(OUT / f"sweep_{name}.html"))
        except Exception as e:
            print(f"  visualize failed: {e}", flush=True)

    write_summary(OUT / "sweeps_summary.json", {"targets": results})
    for name, r in results.items():
        print(f"  {name}: {r['entities']} entities, {r['smells']} smells")
    print("DONE")


if __name__ == "__main__":
    main()
