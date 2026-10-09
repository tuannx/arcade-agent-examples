"""SkillEvaluator evaluation: a real forked upstream (NVIDIA/SkillEvaluator)
measured with arcade-agent self-analysis, pinned to one exact commit.

Deterministic: the target is cloned from the tuannx fork and pinned to
FORK_SHA before analysis, so re-runs produce identical numbers.

Usage: python run.py [--out docs/reports]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCEN = Path(__file__).resolve().parent
CACHE = SCEN.parents[1] / "repos"
DEFAULT_OUT = SCEN.parents[1] / "docs" / "reports"

FORK_URL = "https://github.com/tuannx/SkillEvaluator.git"
UPSTREAM_URL = "https://github.com/NVIDIA/SkillEvaluator.git"
FORK_SHA = "f32c88455b6007b7afca9d1d3909283226d52efa"


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def ensure_pinned():
    repo = CACHE / "SkillEvaluator"
    CACHE.mkdir(parents=True, exist_ok=True)
    if not (repo / ".git").exists():
        print(f"[clone] {FORK_URL} ...", flush=True)
        subprocess.run(["git", "clone", "--depth", "1", FORK_URL, str(repo)], check=True)
    sh("git", "fetch", "--depth", "1", "origin", FORK_SHA, cwd=repo)
    sh("git", "checkout", "--detach", FORK_SHA, cwd=repo)
    return repo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("AAE_OUT", str(DEFAULT_OUT)))
    args = ap.parse_args()
    OUT = Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)

    repo = ensure_pinned()
    t0 = time.time()
    env = dict(os.environ, ARCADE_MOCK="1")
    cli = shutil.which("arcade-self-analysis") or str(
        Path(sys.executable).with_name("arcade-self-analysis"))
    subprocess.run(
        [cli,
         "--source", str(repo),
         "--language", "python",
         "--algorithm", "pkg",
         "--filter-non-architectural-helpers",
         "--repo-name", "SkillEvaluator",
         "--output-json", str(OUT / "skillevaluator_analysis.json"),
         "--output-html", str(OUT / "skillevaluator.html")],
        check=True, env=env)
    dt = time.time() - t0

    a = json.loads((OUT / "skillevaluator_analysis.json").read_text())
    smells = a.get("smells") or []
    summary_smells = [{"type": s.get("smell_type"), "severity": s.get("severity"),
                       "components": s.get("affected_components")} for s in smells]
    md = a.get("metrics") or {}
    dm = a.get("derived_metrics") or {}
    summary = {
        "target": "SkillEvaluator",
        "fork": FORK_URL.removesuffix(".git"),
        "upstream": UPSTREAM_URL.removesuffix(".git"),
        "sha": FORK_SHA,
        "language": "python",
        "tool": "arcade-agent 0.4.0 self-analysis (pkg, helper-filtering, ARCADE_MOCK=1)",
        "source_entities": a.get("source_num_entities"),
        "entities": a.get("num_entities"),
        "edges": a.get("num_edges"),
        "components": a.get("num_components"),
        "smells": summary_smells,
        "rci": md.get("RCI"),
        "turbo_mq": md.get("TurboMQ"),
        "balanced_architecture_score": dm.get("BalancedArchitectureScore"),
        "seconds": round(dt, 1),
        "analysis_json": "skillevaluator_analysis.json",
        "report_html": "skillevaluator.html",
    }
    (OUT / "skillevaluator_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print("DONE")


if __name__ == "__main__":
    main()
