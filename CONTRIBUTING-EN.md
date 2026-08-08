# Contributing to Skills Chain Framework

This project follows a lightweight, evidence-based contribution flow. All community members are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Table of Contents
- [Contribution checklist](#contribution-checklist)
- [Development setup](#development-setup)
- [PR process](#pr-process)
- [Code style](#code-style)
- [How to file a good issue](#how-to-file-a-good-issue)
- [Questions](#questions)

## Contribution checklist (all PRs)
- [ ] **One change per PR.** Small diffs review faster and roll back cleaner.
- [ ] **Design doc alignment.** New mechanisms must trace to the normative spec (`docs/architecture/`). If the spec is silent, propose a spec change in the same PR.
- [ ] **Tests for behavior.** Every new mechanism ships with a test that fails before the change and passes after.
- [ ] **No magic numbers.** New thresholds must include their calibration rationale (data source, window, sample size). Uncalibrated thresholds are not accepted as decision logic.
- [ ] **Deterministic verification.** Claims are backed by `pytest`, not by self-reported "it works".
- [ ] **Documentation updated.** README / docs keep the single source of truth current.

## Development setup
```bash
git clone <repo>
cd skills-chain-framework
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## PR process
1. Fork the repo, create a branch (`feat/...`, `fix/...`).
2. Commit with conventional messages (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
3. Open the PR with the checklist above filled in.
4. CI must pass (lint + tests on 3.10–3.12, Ubuntu + Windows).
5. Review: at least one maintainer approves; changes requested are addressed in follow-up commits (no force-push squashing during review).

## Code style
- PEP 8, `black`-formatted, `ruff`-checked.
- Type hints on all public functions.
- Docstrings: one-line summary + Args/Returns for anything non-trivial.

## How to file a good issue
A good issue saves everyone time. Please include:

**For bugs:**
- Framework version and Python version
- OS and environment (venv, pip, CI)
- Full error log (not a summary)
- Minimal reproduction: steps, code, config
- Expected vs actual behavior

**For feature requests:**
- The problem with evidence (observed behavior, logs, data)
- Proposed mechanism with reference to the normative spec
- Threshold/calibration plan if new thresholds are introduced
- Acceptance criteria (how would we verify it works)

Use the issue templates: [bug report](.github/ISSUE_TEMPLATE/bug_report.md) · [feature request](.github/ISSUE_TEMPLATE/feature_request.md)

## Questions
Open a discussion in Issues. For security issues, use [SECURITY.md](SECURITY.md) instead.
