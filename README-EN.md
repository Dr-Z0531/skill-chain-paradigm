<p align="center">
  <img src="docs/logo.png" alt="the maintainers" width="560"/>
</p>
<p align="center">
  <em style="font-size:2.2em;font-weight:700;letter-spacing:1px;background:linear-gradient(90deg,#1cd6ff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">⚡ Skill-Chain Paradigm</em>
</p>
<p align="center">
  <em>Skills as atoms. Chains as the only unit of work. Pruning as governance. Verification as judge.</em><br>
  <em>技能即原子 · 链是唯一的工作单元 · 修剪即治理 · 验证即裁判</em>
</p>

<p align="center">
<a href="https://github.com/Dr-Z0531/skill-chain-paradigm/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-%231cd6ff" alt="License: MIT">
</a>
<a href="https://pypi.org/project/skill-chain-paradigm/">
    <img src="https://img.shields.io/badge/PyPI-v0.2.0-%23a78bfa" alt="Version 0.2.0">
</a>
<a href="https://github.com/Dr-Z0531/skill-chain-paradigm">
    <img src="https://img.shields.io/badge/python-3.10%2B-%2325d697" alt="Python 3.10+">
</a>
</p>

---

**📖 Documentation**: [Getting Started](docs/getting-started/README-EN.md) · [Architecture](docs/architecture/README-EN.md) · [Routing](docs/architecture/routing-EN.md) · [Pruning](docs/architecture/pruning-EN.md) · [Chain Lifecycle](docs/architecture/chain-lifecycle-EN.md) · [Verification](docs/architecture/verification-EN.md)

**🌐 Language**: English · [简体中文](README.md)

**🧩 Examples**: [Delegation Chain](examples/delegation_chain.py) · [Single-Skill Chain](examples/single_skill_chain.py) · [Skill Index Example](examples/skills.example.json)

---

## Table of Contents

- [What Problem It Solves](#what-problem-it-solves)
- [Core Concepts](#core-concepts)
- [How the Framework Works](#how-the-framework-works)
- [Architecture](#architecture)
- [Design Decisions](#design-decisions)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [A Full Event Journey](#a-full-event-journey)
- [Gradual Upgrade Path](#gradual-upgrade-path)
- [Why Use It / When Not To](#why-use-it--when-not-to)
- [Documentation](#documentation)
- [Testing](#testing)
- [Ecosystem](#ecosystem)
- [Contributing](#contributing)
- [License](#license)

---

## What Problem It Solves

Skill libraries grow without bound. After months of distillation, **250+ skills is the norm** (the author measured hundreds) — and no human can remember them all. An uninvoked skill is equivalent to a nonexistent one. Three consequences:

| Problem | Symptom | Consequence |
|:---|:---|:---|
| **Routing hallucination** | Surface-word matching picks the wrong skill | B is used when A was needed; output quality drops |
| **Zombie skills** | Long-unused but occupying asset status | Library bloat; every conversation's context is diluted |
| **Context inflation** | Every skill name injected every time | Attention dilution — "fits but cannot be found" |

Traditional direct invocation also hides a defect: **single-skill and multi-skill scenarios run two different logics** — single skills are called directly (no verification, no logging, no pruning data) while multi-skill flows use workflows. This split means effect evaluation only ever covers half the work.

**Skill-Chain Paradigm answers one question:** *When skills grow from 50 to 500+, how does an agent ecosystem stay "more accurate, lighter, and more stable with use"?*

The answer is a closed loop, not a pile of rules:

```
Event → Route (deep anchors, not descriptions) → Generate chain (length ≥ 1)
     → Execute → Verify (deterministic signals) → Log → Prune → Iterate
```

## Core Concepts

### Skill — an atom, never invoked directly

A skill carries six metadata fields: `deep_anchors`, `boundary_exclusions`, `confusable_with`, `result_signal`, `state` (three states), `version`. Its states:

| State | Definition | Transition |
|:---|:---|:---|
| **Active** | Routable by default | Default on entry; restored from dormant |
| **Dormant** | Temporary folded state from dynamic pruning | Conflict/overlap evidence met; restored on original-scenario verification |
| **Archived** | Long-term retired state | Dormant overdue or low usage + low effect; rollback-able |

**Skills are never deleted** — only state-migrated. Deletion is irreversible; dormancy is recoverable.

### Chain — the only unit of work

A chain is an ordered skill sequence `C = [S₁, S₂, ..., Sₙ]`, `n ≥ 1`. **Every event must execute through a chain — no bare skill invocation.** Single-skill events also go through an `n=1` single-skill chain (verified, logged, and included in the effect-evaluation system).

### Invocation Protocol (E→R→G→X→V→Log)

Any event, any skill count, any chain length — one path. **No exceptions:**

```
① Event E → ② Route R (R1 anchors→R2 exclusion→R3 distinction→rank) → ③ Generate G (main+support, n≥1, chain_id)
→ ④ Execute X (seq/par/hyb, output feeds next) → ⑤ Verify V (signal three-choose-one, deterministic) → ⑥ Log (router_log, single source of truth)
```

## How the Framework Works

<p align="center">
  <img src="docs/fig2-closed-loop.svg" width="720"/>
  <br><em style="font-size:12px;opacity:.6">The event loop (E→R→G→X→V→Log)</em>
</p>

| Mechanism | Input | Mechanism | Output |
|:---|:---|:---|:---|
| **Deep-anchor routing** | Event intent text | R1 anchor-word matching → R2 boundary exclusion first → R3 confusion-pair distinction → confidence tiers (≥2 anchors high / 1 anchor medium / 0 anchors synonym bridge) | Ranked skill candidates |
| **Chain generation** | Ranked candidates | Main = top candidate → support skills appended → length = complexity × available set × history | Chain instance (chain_id + length + mode) |
| **Deterministic verification** | Chain instance | Signal three-choose-one: task_completion / user_feedback / artifact_exists | pass/fail + evidence |
| **Dual-signal pruning** | router_log aggregation | Structural depth (anchor overlap ≥40%) + process action (co-trigger ≥3); two-phase (static now, dynamic after 2 weeks); L5 restore-check | Active→dormant (recoverable) + ledger |
| **Chain-store convergence** | Same-event chains | Stable ×3 → cached (replay without re-routing); skill patch → dependent chain invalidation | Converged chains + version linking |

## Architecture

<p align="center">
  <img src="docs/fig1-architecture.svg" width="720"/>
</p>

Four layers — assets separated from matching, matching from workflow, workflow from governance:

```
┌─────────────────────────────────────────────────┐
│ Layer 4: Governance (pruning · lifecycle)        │
│   Three-state · chain recycling · ledger · review│
├─────────────────────────────────────────────────┤
│ Layer 3: Workflow (chain · only unit of work)    │
│   Generation · modes · convergence cache · ver.  │
├─────────────────────────────────────────────────┤
│ Layer 2: Matching & verification (routing · V)   │
│   Deep-anchor map · R1-R4 · signal three-choose  │
├─────────────────────────────────────────────────┤
│ Layer 1: Asset pool (skills · atoms)             │
│   Six-column map · three states · never delete   │
└─────────────────────────────────────────────────┘
     router_log · single source of truth · log first, decide later
```

**Anti-Illusion Five Layers** (routing hallucination is the ecosystem's primary threat; every mechanism is verifiable):

```
L1 deep-anchor-first → L2 exclusion-first → L3 confusion-pair distinction → L4 result-signal verification → L5 pruning verification
Meta-principle: every mechanism is verifiable; no unverifiable judgment; no undiscoverable illusion.
```

## Design Decisions

<p align="center">
  <img src="docs/fig3-state-machine.svg" width="720"/>
</p>

Every "obvious" design has an alternative and a rejection reason:

| Design | Alternative | Why rejected |
|:---|:---|:---|
| Chain as only work unit | Direct skill invocation | Two-logic split: single skills get no verification/log/pruning data; evaluation covers only half the work |
| Deep-anchor routing | Description matching | Surface-word illusion: descriptions are ads, anchors are mechanism words; ads exaggerate, mechanism words don't lie |
| Dual-signal pruning | Single signal | Similar anchors ≠ real conflict; co-triggers ≠ real overlap; false pruning is unacceptable |
| Deterministic verification | LLM self-review | Verifier = executor means "pass" only proves the model believes it is right; logical-verification agent paper: +independent logic layer 78→98% |
| Temporary dormancy | Permanent deletion | Deletion is irreversible; dormancy is recoverable |
| Conservative initial thresholds | Final values immediately | No magic numbers: thresholds must be calibrated against real distributions after 2 weeks |

## Installation

**Python 3.10+** (pure stdlib, zero external dependencies):

```bash
# Use from source (clone and use directly)
git clone https://github.com/Dr-Z0531/skill-chain-paradigm.git
cd skill-chain-paradigm

# Or install as a package
pip install -e .
```

## Quick Start

```bash
# Component self-tests (R1 · four components)
python -m src.router.generator --selftest
python -m src.verifier.verifier --selftest
python -m src.pruner.pruner --selftest
python -m src.store.chain_store --selftest

# Route an event (set SKILL_CHAIN_SKILLS_ROOT to your skills dir for long-tail routing)
python -m src.router.generator "three agents collaborate on how to divide work"

# Verify an artifact
python -m src.verifier.verifier artifact_exists <path> <chain_id>

# Run test regression
python -m pytest tests/ -v
```

## A Full Event Journey

**Scenario**: the user says "the delegated subagent output — is it reliable? I fear false positives."

| Step | What happens | Intermediate artifact |
|:---|:---|:---|
| ① Feature extraction | Normalize: `{verify, false-positive, reliable, artifact}` | Feature set |
| ② Routing | R1: "false-positive/verify" hits verification; R2: no exclusion; R3: eval candidate but pair-rule decides ("verification architecture"→verification) | [verification(2), eval(1)] |
| ③ Chain generation | Main = verification · length=1 | chain-xxxxx-1 |
| ④ Chain execution | Verification methodology (anti-self-report/ logic layer/ dual insurance) | Verification report |
| ⑤ Verification | artifact_exists: report exists + JSON valid | pass |
| ⑥ Logging | router_log entry (with route-quality marker) | Log → pruning/clustering data |

**If only one skill matches** (e.g., "verify" without "evaluate"): an `n=1` single-skill chain is generated — same ①–⑥, same logging. This is the everyday shape of "no bare invocation."

## Gradual Upgrade Path

### Baseline: single-skill chain (n=1)

```bash
python examples/single_skill_chain.py
```

### Upgrade 1: multi-skill chain (n=2, sequential)

Add `eval` to the skill index; the event "verify + evaluate" auto-generates `[verification → eval]` — **the protocol does not change**, only the length.

### Upgrade 2: delegation chain (n=4, sequential)

Add `strategic`/`orchestration`; "multi-agent collaboration + division + verification" generates `[strategic → orchestration → verification → eval]` — four skills in sequence, each feeding the next.

### Upgrade 3: enable pruning governance

After 2 weeks, router_log accumulates data → `pruner.py` dual-signal evaluation → conflicting skills go dormant → ledger + weekly review + restore-check.

**Common thread**: from n=1 to n=4, from execution to governance — **the protocol never changes**. That is the extensibility proof of "chain" as the only unit of work.

## Why Use It / When Not To

**Use it when:**
- The skill library exceeds 50 and keeps growing — manual routing maintenance fails
- Multi-skill collaboration is frequent (delegation/distillation/verification/evolution) — standardized chain workflows are needed
- A "verifiable" ecosystem is required — every mechanism can be checked by result signals
- Rollback-able governance is required — pruning/archiving/invalidation are all reversible
- Unified evaluation across single- and multi-skill scenarios is required — reject "half the work has no effect data"

**Do not use it when:**
- The library is small (<20) and stable — maintain a plain list
- One-off scripting — the chain protocol is over-engineering
- No "result signal" can be defined — no signal, no verification, no closed loop
- Manual acceptance is already sufficient — this framework solves system-level reliability, not manual process

## Documentation

| Doc | Content |
|:---|:---|
| [Getting Started](docs/getting-started/README-EN.md) | Full tutorial from zero to running |
| [Architecture Overview](docs/architecture/README-EN.md) | Four layers + closed loop + design decisions |
| [Routing Protocol R1–R4](docs/architecture/routing-EN.md) | Per-step judgment mechanism and "why" |
| [Dynamic Pruning](docs/architecture/pruning-EN.md) | Dual-signal evaluation + reversible migration + restore |
| [Chain Lifecycle](docs/architecture/chain-lifecycle-EN.md) | Convergence cache + version linking + recycling |
| [Verification Protocol](docs/architecture/verification-EN.md) | Signal three-choose-one + deterministic judgment |

## Testing

```bash
python -m pytest tests/ -v
```

Covers: routing (13 cases: positive/negative/long-tail/confusion) · pruning (structural overlap · confusion-pair exclusion) · verification (three signals PASS/FAIL branches) · chain store (×3 convergence · patch invalidation · recycling).

## Ecosystem

<p align="center">
  <img src="docs/fig4-ecosystem.svg" width="720"/>
  <br><em style="font-size:12px;opacity:.6">Skill ecosystem (routing · verification · pruning · chaining)</em>
</p>

- **router_log**: single source of truth (JSONL, append-only) — routing evidence + verification results → pruning/clustering/self-learning
- **weekly_review**: weekly review (usage rate + effect rate dual metrics; watch on double-low; restore conditions)
- **Long-tail auto-promotion**: high-usage long-tail skills promoted to deep anchoring (layered routing: 11 core deeply anchored + long-tail directory fallback)
- **Test isolation**: temp paths + cleanup after run (prevent real-data pollution)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Record all changes in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT License](LICENSE) · Copyright (c) 2026 the maintainers

## 0.3.0 Added (2026-08-08)

- **Confusion-pair library**: src/data/confusion_pairs.json (10 pairs · machine-readable · R3 confusion adjudication)
- **Stability protocol**: docs/architecture/stability.md (pruning rollback snapshots / threshold calibration / SoT injection)
- **Tests**: 22/22 passed (incl. 4 pair-validation tests)

### 0.3.0 Final State (2026-08-08 late night · after full-package review fixes)

- **Confusion-pair library**: src/data/confusion_pairs.json (**13 pairs** · full sync from local state · machine-readable · R3 confusion adjudication)
- **Stability protocol**: docs/architecture/stability.md (pruning rollback snapshots / threshold calibration / SoT injection)
- **Code sync**: local runtime baseline (misroute ≥2 words / verification always appended / deep-review / SKILL_CHAIN_SKILLS_ROOT)
- **Verified**: 22/22 tests · zero-leak scan · signed SHA256SUMS · full doc-implementation consistency check passed

### 📐 Algorithm Design

Each architecture doc contains an **executable algorithm spec** (pseudocode + parameter table + edge cases):
- [Routing R1-R4](docs/architecture/routing.md) (anchors/exclusions/confusion adjudication/confidence tiers)
- [Pruning (two-phase)](docs/architecture/pruning.md) (static 40% overlap + dynamic co-trigger ≥3 + restore check)
- [Chain lifecycle](docs/architecture/chain-lifecycle.md) (fingerprint convergence 3x / patch invalidation / archive recycle)
- [Verification (3 signals)](docs/architecture/verification.md) (task_completion / user_feedback / artifact_exists)
- [Stability parameters](docs/architecture/stability.md) (θ_t/θ_e/K_max/θ_c/θ_i/α/β/η · all calibratable)
