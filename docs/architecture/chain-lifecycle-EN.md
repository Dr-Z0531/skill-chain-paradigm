# Chain Lifecycle

## Generation
```
event → feature extraction → anchor matching (R1–R4) → candidates sorted
→ main skill + support skills → chain (length ≥ 1) → chain_id
```

Chain length = event complexity × available skill set × historical effect. Simple events produce single-skill chains; complex events produce multi-skill chains; pruning shrinks the available set and therefore the length.

## Execution modes
| Mode | Semantics | Example |
|:---|:---|:---|
| `sequential` | Skills run in order; each output feeds the next | delegation: strategic → orchestration → verification → eval |
| `parallel` | Independent skills run concurrently | verification + eval on the same artifact |
| `hybrid` | Parallel within segments, sequential between | distillation pipeline |

## Convergence & caching
Same-event chains that are identical 3 times converge and enter the chain store (replay without re-routing). Divergence triggers route-table iteration.

## Versioning
Skills carry a `dependent_chains` list. When a skill is patched, its dependent chains are invalidated and re-routed on next use. Weekly full-version reconciliation covers legacy skills.

## Recycling
Low-frequency chains (unused 30 days + low effect) are archived — the chain store must not become a second skill library.

---

## Algorithm Spec (chain lifecycle executable definition)

```
fingerprint = "skill1+skill2|len2"                # skills + length
add_chain: same fp → count+=1 · converged at count>=3   # convergence threshold
invalidate_on_patch(s): chains containing s → version_valid=False
recycle(threshold=1): count<=1 → archived (never deleted · recoverable)
present(limit=1): converged ∧ valid ∧ not archived · sort by count desc
```
