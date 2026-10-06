# ADR 0001: Pin the arcade-agent release

## Status

Accepted

## Context

`refresh.yml` installed `arcade-agent[languages]` with no version. PyPI
`0.3.0` is the latest release (`v0.3.0`, `576e412dadd6f752f3a5f886201a7e80db93407f`).
Upstream main has unreleased parser changes (Java unused-import filtering,
ACDC, TypeScript path resolution). The next release would change report
numbers with no diff in this repo.

The published React #33152 reports had no scenario, so `make all` could not
regenerate them. A full `facebook/react` checkout is too heavy for the
routine suite.

## Decision

`analyzer-pin.json` is the only name of the analyzer release. `make install`
and the refresh workflow install `requirement()` from that file. Scenario
runners refuse to write a summary when the installed version differs.

Every summary JSON records `analyzer.version`, `analyzer.installed_version`,
and `analyzer.upstream_commit`. The PyPI wheel does not embed a git SHA
(`direct_url.json` is absent), so the commit is the tag SHA stored in the
pin. A VCS install's `direct_url.json` commit replaces it and sets
`upstream_commit_source` to `installed-vcs`.

`make react33152` materialises facebook/react at the SHAs in
`scenarios/pr-react-33152/run.py`. It is not a dependency of `make all`.

Wall-clock seconds are printed and not stored. They are not a property of
the source.

README and `docs/index.html` quote the same version. `make check-pin`
fails if those quotes drift from the pin. The sample workflow is still a
literal, because a GitHub Action input cannot read this file.

## Consequences

A version bump is a pull request that edits `analyzer-pin.json`, updates the
quoted sample, and regenerates reports. The number diff is the review.

Transitive grammar packages (`tree-sitter-*>=…`) stay unpinned. The shifts
called out above live in arcade-agent itself. A lockfile would freeze more
and add a second source of truth.

Routine `make all` stays on the small corpus. React #33152 is opt-in.
CI on pull requests runs the synthetic scenario twice and compares bytes.
The monthly refresh still runs `make all`.
