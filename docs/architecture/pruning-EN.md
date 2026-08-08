# Dynamic Pruning

Pruning is governance for the skill ecosystem: without it, skill libraries grow without bound.

## Dual signals
A skill becomes a prune candidate only when **both** signals fire:

| Signal | Type | Criterion (v0.1 conservative) |
|:---|:---|:---|
| Anchor overlap | static | overlap ≥ 40% of anchor vocabulary with a neighbor |
| Co-trigger frequency | dynamic | same event triggers both skills ≥ 3 times in 14 days |

Thresholds are conservative by design. After two weeks of log data, they are recalibrated from the observed signal distribution (no magic numbers — calibration before effect).

## Temporary transition
Pruning = `active → dormant`. **Never delete.** Restoration is automatic when re-verification shows the pruned skill's original scenarios degrading (the "mis-prune" loop).

## Ledger
Every prune is recorded: `pruned_at`, `reason`, `restore_condition`, `verify_status`. Weekly review reconciles the ledger. Chains depending on the pruned skill are invalidated **before** the prune (chain-first, then prune).

## Anti-patterns guarded
1. **Pruning bias** — long-tail skills are protected by a weekly rotation quota (≥1 long-tail probe per week).
2. **Matthew effect** — high-frequency chains must not monopolize routing; the quota keeps exposure fair.
3. **Silent pruning** — everything is in the ledger; nothing disappears unnoticed.

---

## Algorithm Spec (two-phase pruning executable definition)

### structural_overlap pseudocode (phase 1 · static)

```
for i,j pairs in skills:
  inter = anchors[i] ∩ anchors[j]
  denom = min(|anchors[i]|, |anchors[j]|)
  if denom > 0 and |inter|/denom >= 0.4: overlaps.append(...)   # 40% threshold
```

### dynamic_prune_signal (phase 2 · after 2 weeks data)

```
co[(event_fingerprint, route)] += 1 per router_log line
conflicts = {skill: events} where count >= 3      # co-trigger threshold 3
calibration: "pending C11 (2-week data · no magic numbers)"
```

### restore_check (L5 rollback)

```
dormant skill with eff.pass > 0 and eff.fail == 0 → restored (mis-prune)
```
