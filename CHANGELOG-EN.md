# Changelog

All notable changes are documented here, following [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).


## [0.3.0] - 2026-08-08

### Added (0.3.0)

- **Confusion-pair library** (`src/data/confusion_pairs.json`·10 pairs·machine-readable·anti routing-hallucination R3)
- **Stability protocol** (`docs/architecture/stability.md`·pruning rollback snapshots / threshold calibration / SoT injection)
- **Threshold calibration protocol** (no magic numbers · all parameters calibratable · router_log ≥30 triggers first calibration)

### Verified (0.3.0)

- Confusion pairs: 10/10 machine-readable validation passed
- Stability criteria defined: routing blind-test 7/7 · rollback ≤20% · calibration within 2 weeks

[0.3.0]: https://github.com/Dr-Z0531/skill-chain-paradigm/releases/tag/0.3.0


### Fixes & Sync (0.3.0 · 2026-08-08 late night · driven by full-package review)

- **Code sync**: 4 files aligned with local runtime baseline (misroute ≥2-word fix / verification always appended length=2 / deep-review complex support / SKILL_CHAIN_SKILLS_ROOT env var) · release adaptation (src/data relative paths)
- **Sanitization**: internal words → generic terms (names/tools/paths) · final scan zero hits
- **Data sync**: confusion pairs full 13 pairs (local state authoritative · extracted from mapping table)
- **Signing**: SHA256SUMS (after sync) → SHA256SUMS (after 13 pairs) → SHA256SUMS (after doc sync) · re-sign on every change
- **Verified**: 22/22 tests · zero-leak scan · full doc-implementation consistency check

## [0.2.0] - 2026-08-08

### Added (v0.2.0 open-source candidate)

- **src/ standard package layout**: router (deep-anchor routing + chain generation) · verifier (three-signal verification) · pruner (dual-signal pruning) · store (chain-store convergence) · data (routing rules / test cases)
- **tests/ pytest suite**: routing 13-case regression (positive/negative/long-tail/confusion) · verification three-signal branches · pruning overlap detection · chain-store convergence
- **examples/**: delegation chain · single-skill chain · skill index example
- **docs/**: logo + 4 SVG architecture figures (four layers / closed loop / state machine / ecosystem) + bilingual architecture and getting-started docs
- **Governance files**: LICENSE (MIT · the maintainers) · CODE_OF_CONDUCT · CONTRIBUTING · SECURITY (bilingual)
- **Bilingual README**: full 15-section TOC + linked docs + shields + gradual upgrade path

### Fixed

- Component paths adapted to src/data relative references · long-tail index env-var driven (SKILL_CHAIN_SKILLS_ROOT) · zero hardcoded paths
- Copyright holder unified: the maintainers (MIT compliance)

## [0.1.0] - 2026-08-07
## [Unreleased]

### Added (v0.1.0 design milestone)
- Core theory: skill-as-atom, chain-as-only-work-unit, five axioms.
- Routing protocol R1–R4.
- Dynamic pruning design (dual signals; dormant state; reversible).
- Chain JSON schema v1 and call protocol (event → route → generate → execute → verify → log).
- Verification signal model (task completion / user feedback / artifact exists).
- Reference implementation skeleton: `src/router`, `src/pruner`, `src/store`, `src/verifier`.

### Planned (v0.2.0)
- router_log data pipeline and threshold calibration tooling.
- Chain clustering (co-trigger matrix → new chain discovery).
- Long-tail quota mechanism (weekly rotation probe).
- Chain visualization dashboard.
