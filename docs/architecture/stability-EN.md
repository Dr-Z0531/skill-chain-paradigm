# Skill Ecosystem Stability Protocol (V0.3.0)

> Source: 2026-08-08 black-box harness governance analysis (4 skill-ecosystem gaps) + "top-tier commercial delivery standard"
> Companion: router_rules.json (confusion pairs) · pruner.py (rollback snapshots) · calibration protocol

## 1. Confusion-Pair Library (anti routing-hallucination · R3 reinforcement)

- Data: `src/data/confusion_pairs.json` (10 pairs · machine-readable)
- Use: user language hits either side of a pair → confusion adjudication (R3) · decide by deep anchors · never by surface words
- Maintenance: new neighbors in mapping table → sync into library (weekly review)

## 2. Pruning Rollback Snapshots (reversible)

```
1. Snapshot: full SKILL.md + references copied to archives/skills/snapshots/<name>-<date>/ before pruning
2. Declare: pruning record into router_log (time / dual-signal data / snapshot path)
3. Rollback: archived state restore = copy snapshot back + append restore record to router_log
4. Criterion: routing quality drops within 2 weeks after pruning (blind test < pre-pruning) → auto rollback
```

## 3. Threshold Calibration Protocol (no magic numbers)

- All parameters calibratable (trigger θ_t / edge weight θ_e / K_max / consensus θ_c / independence θ_i / anchor α / bridge β / learning rate η)
- Trigger: router_log ≥30 entries OR keypoints ≥10 covered → first calibration
- Discipline: every adjustment must carry data evidence · recorded in router_log · reversible

## 4. SoT-style Injection (preplay-prune-inject · harness-ized)

```
① Who preplays: low-token divergent preplay reasoning before complex tasks (anchor-point trigger → subgraph activation → Top-K)
② How to prune: 8-axiom filter + keep only "decision-affecting constraints + fact snapshots" (architecture constraints never summarized)
③ Where to inject: prefix tail (static anchoring) or status bar (max attention) · SoT two-step: skeleton first, then execute
④ How to verify: A/B before/after injection (deterministic checks) · unobservable difference → withdraw injection
```

## 5. Stability Criteria

```
1. Routing hallucination rate: blind-test accuracy ≥7/7 (regression after every integration round)
2. Pruning damage: rollback rate ≤20% (within 2 weeks)
3. Calibration execution: completed within 2 weeks after first trigger · adjustments carry data
4. Injection verification: SoT A/B observability rate = 100%
```

---

## Algorithm Spec (stability parameters executable definition)

| param | meaning | initial | calibration | source |
|:---|:---|:---|:---|:---|
| θ_t | trigger threshold | 0.5 | 2w | trigger-contribution |
| θ_e | edge weight threshold | 0.3 | 2w | subgraph contribution |
| K_max | max divergent heads | 5 (7 complex / 3 simple) | 2w | K+1 gain<5% caps |
| θ_c | consensus cluster | 0.7 | 4w | consensus-human agreement |
| θ_i | independence | 0.4 | 4w | fake-parallel detection |
| α/β | anchor/bridge weights | 0.7/0.3 | 4w | hit contribution |
| η | learning rate | 0.1 | 8w | weight prediction accuracy |

SoT injection four steps: preplay (trigger θ_t → subgraph θ_e → Top-K) → prune (8-axiom filter + constraints + fact snapshots only) → inject (prefix tail or status bar · skeleton-first) → verify (A/B deterministic · unobservable → withdraw)
