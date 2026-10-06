"""facebook/react#33152 base vs head.

Pinned commits. Overview recovery (auto pkg depth) grades the PR.
pkg_depth=2 shows the new react-server-dom-vite surface inside packages.*.

Not part of `make all`: the checkout is the full React tree.

Usage: python run.py [--out docs/reports]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCEN = Path(__file__).resolve().parent
ROOT = SCEN.parents[1]
sys.path.insert(0, str(ROOT))

from scenarios.analyzer_pin import identity, write_summary
from verdict_html import render_focus_page, render_verdict_page

CACHE = SCEN / "repos"
WORK = SCEN / "worktrees"
DEFAULT_OUT = ROOT / "docs" / "reports"

URL = "https://github.com/facebook/react.git"
BASE = "2b4064eb9b40f65d20a03ce93b246ad762d562e6"
HEAD = "b5f88376aace22604c0694463bdbc96f23635c89"
PR_NUMBER = 33152
PR_TITLE = "feat: add react-server-dom-vite"
PR_URL = "https://github.com/facebook/react/pull/33152"
LANGUAGE = "typescript"
PKG_DEPTH = 2
MAIN_SOURCE_PREFIX = "packages"


def sh(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def ensure_clone():
    repo = CACHE / "react"
    if not (repo / ".git").exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        print("[clone] facebook/react (partial)...", flush=True)
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--depth", "1", URL, str(repo)],
            check=True,
        )
    return repo


def materialize(repo, sha, dest):
    dest = Path(dest)
    if dest.exists():
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=dest,
            capture_output=True,
            text=True,
        )
        if head.returncode == 0 and head.stdout.strip() == sha:
            return dest
        raise SystemExit(f"{dest} exists but HEAD is not {sha}")
    WORK.mkdir(parents=True, exist_ok=True)
    sh("git", "fetch", "--filter=blob:none", "--depth", "1", "origin", sha, cwd=repo)
    sh("git", "worktree", "add", "--detach", str(dest), sha, cwd=repo)
    return dest


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def main_source_entities(graph, prefix):
    count = 0
    for entity in graph.entities.values():
        package = entity.package or ""
        fqn = entity.fqn or ""
        if package == prefix or package.startswith(prefix + "."):
            count += 1
        elif fqn == prefix or fqn.startswith(prefix + "."):
            count += 1
    return count


def component_sizes(arch):
    rows = [
        {"name": component.name, "entities": len(component.entities)}
        for component in arch.components
    ]
    rows.sort(key=lambda row: (-row["entities"], row["name"]))
    return rows


def only_in(left, right):
    right_names = {row["name"] for row in right}
    return [row for row in left if row["name"] not in right_names]


def load_side(path):
    from arcade_agent.source.ingest import ingest
    from arcade_agent.tools.compute_metrics import compute_metrics
    from arcade_agent.tools.detect_smells import detect_smells
    from arcade_agent.tools.parse import parse
    from arcade_agent.tools.recover import recover

    ingested = ingest(str(path), language=LANGUAGE)
    graph = parse(ingested.path, language=LANGUAGE)
    overview = recover(graph, algorithm="pkg")
    deep = recover(graph, algorithm="pkg", pkg_depth=PKG_DEPTH)
    return {
        "graph": graph,
        "overview": {
            "arch": overview,
            "smells": detect_smells(overview, graph),
            "metrics": compute_metrics(overview, graph),
        },
        "deep": {
            "arch": deep,
            "smells": detect_smells(deep, graph),
            "metrics": compute_metrics(deep, graph),
        },
    }


def side_stats(graph, part):
    return {
        "entities": len(graph.entities),
        "edges": len(graph.edges),
        "components": len(part["arch"].components),
        "smells": len(part["smells"]),
    }


def deep_record(graph, part):
    return {
        "components": len(part["arch"].components),
        "entities": len(graph.entities),
        "edges": len(graph.edges),
        "smells": len(part["smells"]),
        "main_source_entities": main_source_entities(graph, MAIN_SOURCE_PREFIX),
        "components_by_size": component_sizes(part["arch"]),
    }


def write_visualize(out, name, version, graph, arch, smells):
    from arcade_agent.tools.visualize import visualize

    visualize(name, version, graph, arch, smells, output=str(out))


def main():
    from arcade_agent.tools.changelog_architecture import changelog_architecture

    identity()
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.environ.get("AAE_OUT", str(DEFAULT_OUT)))
    out = Path(ap.parse_args().out)
    out.mkdir(parents=True, exist_ok=True)

    repo = ensure_clone()
    loaded = {}
    for label, sha in (("base", BASE), ("head", HEAD)):
        worktree = WORK / f"react33152-{label}"
        print(f"[{label}] materializing {sha[:8]}...", flush=True)
        materialize(repo, sha, worktree)
        loaded[label] = load_side(worktree)
        graph = loaded[label]["graph"]
        overview = loaded[label]["overview"]
        print(
            f"  entities={len(graph.entities)} edges={len(graph.edges)} "
            f"components={len(overview['arch'].components)} "
            f"smells={len(overview['smells'])} "
            f"deep_components={len(loaded[label]['deep']['arch'].components)}",
            flush=True,
        )
        write_visualize(
            out / f"pr_react-33152_{label}.html",
            f"react PR#{PR_NUMBER} {label}",
            sha[:8],
            graph,
            overview["arch"],
            overview["smells"],
        )
        deep = loaded[label]["deep"]
        write_visualize(
            out / f"pr_react-33152_{label}_deep.html",
            f"react PR#{PR_NUMBER} {label} DEEP pkg_depth={PKG_DEPTH}",
            label,
            graph,
            deep["arch"],
            deep["smells"],
        )
        write_summary(
            out / f"pr_react-33152_{label}_deep.json",
            {
                "label": label,
                "sha": sha,
                "pkg_depth": PKG_DEPTH,
                "main_source_prefix": MAIN_SOURCE_PREFIX,
                **deep_record(graph, deep),
            },
        )

    write_visualize(
        out / "pr_react-33152_head_deep.md",
        f"react PR#{PR_NUMBER} head DEEP pkg_depth={PKG_DEPTH}",
        "head",
        loaded["head"]["graph"],
        loaded["head"]["deep"]["arch"],
        loaded["head"]["deep"]["smells"],
    )

    print("[changelog] ...", flush=True)
    base = loaded["base"]
    head = loaded["head"]
    changelog = changelog_architecture(
        base["overview"]["arch"],
        base["graph"],
        head["overview"]["arch"],
        head["graph"],
        smells_a=base["overview"]["smells"],
        smells_b=head["overview"]["smells"],
        metrics_a=base["overview"]["metrics"],
        metrics_b=head["overview"]["metrics"],
        ref_a=f"PR#{PR_NUMBER} base {BASE[:8]}",
        ref_b=f"PR#{PR_NUMBER} head {HEAD[:8]}",
    )
    base_deep = deep_record(base["graph"], base["deep"])
    head_deep = deep_record(head["graph"], head["deep"])
    summary = {
        "repo": "facebook/react",
        "pr": PR_NUMBER,
        "title": PR_TITLE,
        "url": PR_URL,
        "base": BASE,
        "head": HEAD,
        "base_stats": side_stats(base["graph"], base["overview"]),
        "head_stats": side_stats(head["graph"], head["overview"]),
        "deep": {
            "pkg_depth": PKG_DEPTH,
            "main_source_prefix": MAIN_SOURCE_PREFIX,
            "base": base_deep,
            "head": head_deep,
            "components_only_in_head": only_in(
                head_deep["components_by_size"], base_deep["components_by_size"]
            ),
            "components_only_in_base": only_in(
                base_deep["components_by_size"], head_deep["components_by_size"]
            ),
        },
        "changelog": clean(changelog),
    }
    report = write_summary(out / "pr_react-33152.json", summary)
    (out / "pr_react-33152.html").write_text(render_verdict_page(report))
    (out / "pr_react-33152_focus.html").write_text(render_focus_page(report))
    print(json.dumps(report["changelog"].get("summary", {}), indent=2))
    print(
        "deep components",
        base_deep["components"],
        "->",
        head_deep["components"],
        "main_source",
        base_deep["main_source_entities"],
        "->",
        head_deep["main_source_entities"],
    )
    print("head-only", [row["name"] for row in summary["deep"]["components_only_in_head"]])
    print("DONE")


if __name__ == "__main__":
    main()
