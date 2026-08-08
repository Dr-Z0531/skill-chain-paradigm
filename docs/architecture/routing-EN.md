# Routing Protocol (R1–R4)

Routing is intent → skill matching. Its failure mode is **surface-word hallucination**: the description says "agents" so every agent-ish request matches, even when the structural fit is wrong.

## R1 — Depth before surface
Match intent against **deep anchors** (mechanism words from each skill's *core judgment* section), never against the description.

## R2 — Boundary exclusion first
If the intent contains any boundary-exclusion term of a skill, that skill is excluded before any positive matching. Negative routing must be zero-tolerance.

## R3 — Confusable-pair disambiguation
Skills that are easy to confuse carry an explicit disambiguator pair:

| Confusable pair | Disambiguator |
|:---|:---|
| orchestration ↔ strategic-reasoning | "division of work" → orchestration; "reasoning/intent/game" → strategic |
| verification ↔ evaluation | "verify architecture/entailment/false-positive" → verification; "scoring/calibration" → evaluation |
| context-engineering ↔ memory | "status bar/transient progress" → context; "long-term memory/cross-session" → memory |

When both members match, the disambiguator decides and the loser is dropped.

## R4 — Result-signal re-verification
After routing, compare the outcome against the skill's declared "result signal". If unmet, mark the route `suspected_mistake` and feed the case back into the routing table (feature iteration).

## Layered routing
- **Core skills** (deep-anchored): precise routing.
- **Long-tail skills** (no anchors yet): broad routing by category — degraded but not wrong. High-usage long-tail skills get promoted automatically.

## Routing log
Every route is logged (fingerprint, candidates, selection, evidence, outcome). The log is the only data source for pruning, clustering, and self-learning — log first, decide later.

---

## Algorithm Spec (R1–R4 executable definition)

### route(text, rules) pseudocode

```
input: event text, routing rules (skills[].anchors/exclusions/confusions)
output: {selected, level, candidates}

1. feats = extract_features(text)                  # raw words + synonym-bridge normalized (R1.5)
2. results = []
   for sk in rules.skills:
     if any(e in text for e in sk.exclusions):     # R2 exclusion-first · zero tolerance
        results.append({name, status: excluded}); continue
     hits = [a for a in sk.anchors if a in text or a in feats]   # R1 deep anchors
     results.append({name, status: candidate|no_anchor, anchor_count})
3. cands = sort(candidates, by anchor_count desc); if empty: return none
4. top = cands[0]; if top.confusions has cands[1]: # R3 confusion adjudication
     if pair[1] in text and pair[0] not in text: swap(top, second)
5. level = high(≥2 anchors) | medium(1) | low(0)
```

| param | value | meaning | calibration |
|:---|:---|:---|:---|
| anchor_count≥2 | high | dual-anchor confidence | 2-week data |
| misroute gate | ≥2 keywords | single keyword = ambiguity → no route | 2026-08-08 empirical |
| bridge weights | α=0.7/β=0.3 | anchor first · bridge degraded (R1.5) | C11 |
