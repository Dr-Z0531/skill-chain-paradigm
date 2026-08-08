# Architecture

Skills Chain Framework organizes agent skill ecosystems in four layers:

```
┌─────────────────────────────────────────────┐
│ Layer 4: Governance (pruning · lifecycle)   │
│   three-state transitions · chain recycling │
├─────────────────────────────────────────────┤
│ Layer 3: Workflow (chains · only work unit) │
│   chain generation · execution modes ·      │
│   convergence · chain store · versioning    │
├─────────────────────────────────────────────┤
│ Layer 2: Matching & verification            │
│   deep-anchor mapping · R1–R4 · signals     │
├─────────────────────────────────────────────┤
│ Layer 1: Asset pool (skills · atoms)        │
│   active/dormant/archived · deep anchors    │
└─────────────────────────────────────────────┘
```

## The closed loop

```
event → route → generate chain → execute → verify → log → prune → iterate
```

Every mechanism in every layer is itself verifiable (the meta-principle: no unverifiable judgment → no undiscoverable hallucination).

## Modules

| Module | Responsibility |
|:---|:---|
| `src/router` | Intent → candidate skills (R1–R4), chain generation (length ≥ 1), single-skill chains |
| `src/pruner` | Dual-signal conflict evaluation, dormant transitions, ledger, weekly review, restore-on-reverify |
| `src/store` | Chain store: converged-chain cache, version invalidation, low-frequency archiving |
| `src/verifier` | Deterministic result signals (artifact / completion / feedback) |

## Design documents
- [Routing (R1–R4)](routing-EN.md)
- [Pruning](pruning-EN.md)
- [Chain lifecycle](chain-lifecycle-EN.md)
- [Verification signals](verification-EN.md)
