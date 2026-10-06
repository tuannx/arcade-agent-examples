"""Pinned arcade-agent release.

analyzer-pin.json is the only place the release is named. Makefile, CI, and
every summary JSON read it from here.
"""

import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path

PIN_PATH = Path(__file__).resolve().parents[1] / "analyzer-pin.json"
_REQUIRED = (
    "package",
    "extras",
    "version",
    "upstream",
    "upstream_tag",
    "upstream_commit",
)
_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_pin() -> dict:
    pin = json.loads(PIN_PATH.read_text())
    missing = [key for key in _REQUIRED if key not in pin]
    if missing:
        raise SystemExit(f"{PIN_PATH.name} missing {missing}")
    extras = pin["extras"]
    if not isinstance(extras, list) or not all(isinstance(item, str) for item in extras):
        raise SystemExit(f"{PIN_PATH.name} extras must be a list of strings")
    if not _HEX40.match(pin["upstream_commit"]):
        raise SystemExit(f"{PIN_PATH.name} upstream_commit must be 40 hex chars")
    return pin


def requirement(pin: dict | None = None) -> str:
    pin = load_pin() if pin is None else pin
    extras = pin["extras"]
    extra = f"[{','.join(extras)}]" if extras else ""
    return f"{pin['package']}{extra}=={pin['version']}"


def install() -> None:
    spec = requirement()
    subprocess.check_call([sys.executable, "-m", "pip", "install", spec])


def _installed_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError as exc:
        raise SystemExit(f"{package} is not installed. Run: make install") from exc


def _installed_vcs_commit(package: str) -> str | None:
    dist = importlib.metadata.distribution(package)
    raw = dist.read_text("direct_url.json")
    if not raw:
        return None
    vcs = json.loads(raw).get("vcs_info") or {}
    commit = vcs.get("commit_id")
    if isinstance(commit, str) and _HEX40.match(commit):
        return commit
    return None


def identity() -> dict:
    pin = load_pin()
    package = pin["package"]
    installed = _installed_version(package)
    if installed != pin["version"]:
        raise SystemExit(
            f"installed {package}=={installed} does not match "
            f"{PIN_PATH.name} ({pin['version']}). Run: make install"
        )
    installed_commit = _installed_vcs_commit(package)
    return {
        "package": package,
        "version": pin["version"],
        "installed_version": installed,
        "upstream": pin["upstream"],
        "upstream_tag": pin["upstream_tag"],
        "upstream_commit": installed_commit or pin["upstream_commit"],
        "upstream_commit_source": "installed-vcs" if installed_commit else "pin",
    }


def write_summary(path: Path, payload: dict) -> dict:
    body = {"analyzer": identity(), **payload}
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(body, indent=2) + "\n")
    return body


def check_docs() -> None:
    pin = load_pin()
    version = pin["version"]
    root = PIN_PATH.parent
    readme = (root / "README.md").read_text()
    index = (root / "docs" / "index.html").read_text()
    refresh = (root / ".github" / "workflows" / "refresh.yml").read_text()
    errors: list[str] = []

    def need(label: str, text: str, needle: str) -> None:
        if needle not in text:
            errors.append(f"{label} missing {needle!r}")

    def forbid(label: str, text: str, needle: str) -> None:
        if needle in text:
            errors.append(f"{label} still contains {needle!r}")

    need("README", readme, f"arcade-agent[languages]=={version}")
    need("README", readme, f'arcade-agent-version: "{version}"')
    need("README", readme, f"actions/analyze@v{version}")
    need("README", readme, "arcade-agent/analyze-action@v1")
    need(
        "README",
        readme,
        "arcade-self-analysis --source . --output-html report.html --output-json report.json",
    )
    need("README", readme, "make install")
    need("README", readme, "make react33152")
    forbid("README", readme, "workflows/analyze.yml")
    forbid("README", readme, "arcade analyze")
    need("index", index, f"actions/analyze@v{version}")
    need("index", index, f'arcade-agent-version: "{version}"')
    need("index", index, "make install")
    need("index", index, "make react33152")
    forbid("index", index, "workflows/analyze.yml")
    need("refresh", refresh, "make install")
    forbid("refresh", refresh, "arcade-agent[languages]")
    if errors:
        raise SystemExit("\n".join(errors))


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    command = args[0] if args else "install"
    if command == "install":
        install()
    elif command == "identity":
        print(json.dumps(identity(), indent=2))
    elif command == "requirement":
        print(requirement())
    elif command == "check-docs":
        check_docs()
    else:
        raise SystemExit(f"unknown command {command}")


if __name__ == "__main__":
    main()
