"""Verdict and focus pages for facebook/react#33152.

Inputs are plain dicts already written to the summary JSON. No clock, no
live GitHub counters.
"""

FOCUS_LIMIT = 18


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def verdict_label(summary: dict) -> str:
    shifts = summary["shifts"]
    smells_new = summary["smells_new"]
    entities_added = summary["entities_added"]
    if shifts == 0 and smells_new == 0 and entities_added > 0:
        return "SAFE FEATURE"
    if shifts == 0 and smells_new == 0 and entities_added == 0 and summary["entities_deleted"] == 0:
        return "NEUTRAL"
    return "REVIEW"


def _one_thing(deep: dict) -> str:
    names = [row["name"] for row in deep["components_only_in_head"]]
    if not names:
        return "No head-only component at pkg_depth=2."
    listed = ", ".join(names)
    return (
        f"pkg_depth=2 head-only components: {listed}. "
        "Overview recovery stays on the same components."
    )


def _metric_bits(changelog: dict) -> str:
    metrics = changelog.get("metrics") or {}
    parts = []
    for name in ("TurboMQ", "RCI"):
        row = metrics.get(name)
        if not row:
            continue
        parts.append(f"{name} {row['a']} → {row['b']} (delta {row['delta']})")
    return " · ".join(parts)


def _page(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{_escape(title)}</title><style>"
        "*{box-sizing:border-box}body{background:#0d1117;color:#e6edf3;"
        "font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;margin:0}"
        ".wrap{max-width:920px;margin:0 auto;padding:0 16px}a{color:#58a6ff}"
        "code{background:#ffffff14;padding:2px 6px;border-radius:6px}"
        "</style></head><body><div class=\"wrap\">"
        f"{body}</div></body></html>\n"
    )


def _stat(value: str, label: str) -> str:
    return (
        "<div style=\"background:#161b22;border:1px solid #30363d;border-radius:12px;padding:14px\">"
        f"<div style=\"font-size:24px;font-weight:900\">{value}</div>"
        f"<div style=\"color:#8b949e;font-size:11px\">{_escape(label)}</div></div>"
    )


def render_verdict_page(report: dict) -> str:
    change = report["changelog"]["summary"]
    label = verdict_label(change)
    base = report["base_stats"]
    head = report["head_stats"]
    deep = report["deep"]
    entity_delta = head["entities"] - base["entities"]
    entity_sign = f"{entity_delta:+d}"
    metrics = _metric_bits(report["changelog"])
    deep_base = deep["base"]["components"]
    deep_head = deep["head"]["components"]
    main_base = deep["base"]["main_source_entities"]
    main_head = deep["head"]["main_source_entities"]
    prefix = deep["main_source_prefix"]
    version = report["analyzer"]["version"]
    commit = report["analyzer"]["upstream_commit"]
    body = (
        "<div style=\"padding:18px 0\">"
        "<span style=\"background:#3fb95022;color:#3fb950;border:1px solid #3fb950;"
        f"padding:6px 12px;border-radius:20px;font-weight:800\">Verdict: {_escape(label)}</span></div>"
        f"<h1 style=\"margin:6px 0\">facebook/react#{report['pr']}</h1>"
        f"<p style=\"color:#8b949e;margin:0\">{_escape(report['title'])} · "
        f"<a href=\"{_escape(report['url'])}\">{_escape(report['url'])}</a></p>"
        "<div style=\"display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0\">"
        + _stat(f"{base['entities']:,} → {head['entities']:,}", f"ENTITIES {entity_sign}")
        + _stat(f"{base['components']} → {head['components']}", "COMPONENTS")
        + _stat(
            f"{base['smells']} → {head['smells']}",
            f"SMELLS · {change['smells_new']} NEW",
        )
        + "</div>"
        "<h2>1. Numbers</h2>"
        "<div style=\"background:#161b22;border:1px solid #30363d;border-radius:12px;"
        "padding:14px;line-height:1.9;font-size:14px\">"
        f"entities {entity_sign} · edges {base['edges']:,} → {head['edges']:,} · "
        f"shifts {change['shifts']}"
        + (f"<br>{_escape(metrics)}" if metrics else "")
        + f"<br>Base <code>{report['base'][:8]}</code> · Head <code>{report['head'][:8]}</code>"
        "</div>"
        "<h2>2. One thing to look at</h2>"
        f"<p>{_escape(_one_thing(deep))}</p>"
        f"<h2>Deep — { _escape(prefix) }.* (pkg_depth={deep['pkg_depth']})</h2>"
        "<div style=\"background:#161b22;border:1px solid #30363d;border-radius:12px;"
        "padding:14px;line-height:1.9;font-size:14px\">"
        f"Deep components <b>{deep_base} → {deep_head}</b><br>"
        f"main source <code>{_escape(prefix)}.*</code> "
        f"{main_base:,} → {main_head:,} entities ({main_head - main_base:+d})"
        "</div>"
        "<h2>3. Reports</h2>"
        "<ol style=\"line-height:1.9\">"
        "<li><a href=\"pr_react-33152_base.html\">Base report</a></li>"
        "<li><a href=\"pr_react-33152_head.html\">Head report</a></li>"
        "<li><a href=\"pr_react-33152.json\">Summary JSON</a></li>"
        "<li><a href=\"pr_react-33152_base_deep.html\">Deep base</a></li>"
        "<li><a href=\"pr_react-33152_head_deep.html\">Deep head</a></li>"
        "<li><a href=\"pr_react-33152_focus.html\">Focus</a></li>"
        "</ol>"
        "<footer style=\"color:#8b949e;font-size:12px;padding:16px 0;"
        "border-top:1px solid #30363d\">"
        f"arcade-agent { _escape(version) } · { _escape(commit) } · "
        "facebook/react#33152 · heuristic recovery, not ground truth</footer>"
    )
    return _page(f"facebook/react#{report['pr']} — {label}", body)


def _sizes(rows: list[dict]) -> dict[str, int]:
    return {row["name"]: row["entities"] for row in rows}


def render_focus_page(report: dict) -> str:
    deep = report["deep"]
    base_sizes = _sizes(deep["base"]["components_by_size"])
    head_rows = deep["head"]["components_by_size"]
    largest = head_rows[0]["entities"] if head_rows else 1
    bars = []
    for row in head_rows[:FOCUS_LIMIT]:
        name = row["name"]
        head_n = row["entities"]
        base_n = base_sizes.get(name, 0)
        width = f"{(100.0 * head_n / largest):.1f}" if largest else "0.0"
        delta = head_n - base_n
        delta_html = (
            f" <span style=\"color:#3fb950;font-size:12px\">{delta:+d}</span>"
            if delta
            else ""
        )
        bars.append(
            "<div style=\"display:grid;grid-template-columns:220px 1fr 140px;"
            "gap:10px;align-items:center;margin:7px 0\">"
            f"<div style=\"font-weight:600;font-size:14px\">{_escape(name)}{delta_html}</div>"
            "<div style=\"background:#21262d;border-radius:6px;height:22px\">"
            f"<div style=\"background:#58a6ff;width:{width}%;height:22px;border-radius:6px\"></div></div>"
            "<div style=\"font-variant-numeric:tabular-nums;font-size:13px\">"
            f"{base_n} → <b>{head_n}</b></div></div>"
        )
    new_rows = deep["components_only_in_head"]
    if new_rows:
        new_html = "".join(
            f"<li><b>{_escape(row['name'])}</b> · {row['entities']} entities</li>"
            for row in new_rows
        )
    else:
        new_html = "<li>none</li>"
    version = report["analyzer"]["version"]
    body = (
        "<div style=\"padding:18px 0 6px\">"
        "<span style=\"background:#3fb95022;color:#3fb950;border:1px solid #3fb950;"
        "padding:6px 12px;border-radius:20px;font-weight:800\">deep focus</span></div>"
        f"<h1 style=\"margin:8px 0\">facebook/react#{report['pr']} — pkg_depth={deep['pkg_depth']}</h1>"
        "<div style=\"display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0\">"
        + _stat(
            f"{deep['base']['components']} → {deep['head']['components']}",
            "COMPONENTS · DEEP",
        )
        + _stat(
            f"{deep['base']['main_source_entities']:,} → {deep['head']['main_source_entities']:,}",
            f"MAIN SOURCE {deep['main_source_prefix']}.*",
        )
        + _stat(str(len(new_rows)), "HEAD-ONLY COMPONENTS")
        + "</div>"
        f"<h2>1. Top {FOCUS_LIMIT} components — base → head</h2>"
        "<div style=\"background:#161b22;border:1px solid #30363d;border-radius:12px;padding:16px\">"
        + "".join(bars)
        + "</div>"
        "<h2>2. Head-only components</h2><ul>"
        + new_html
        + "</ul><h2>3. Raw</h2><ol style=\"line-height:1.9\">"
        "<li><a href=\"pr_react-33152_head_deep.html\">Deep head</a></li>"
        "<li><a href=\"pr_react-33152_base_deep.html\">Deep base</a></li>"
        "<li><a href=\"pr_react-33152.html\">Overview</a></li>"
        "</ol>"
        "<footer style=\"color:#8b949e;font-size:12px;padding:16px 0;"
        "border-top:1px solid #30363d\">"
        f"arcade-agent {_escape(version)} · pkg_depth={deep['pkg_depth']} · "
        f"focus {_escape(deep['main_source_prefix'])}.* · heuristic, not ground truth</footer>"
    )
    return _page(f"react#{report['pr']} deep focus", body)
