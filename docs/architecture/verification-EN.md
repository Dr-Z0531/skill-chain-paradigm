# Verification Signals

## The principle
**LLMs cannot verify their own output.** Verification lands on a deterministic layer: file existence + parse, status + outputs, or explicit user confirmation.

## Signal model (three-way)
| Signal | Definition | Deterministic check |
|:---|:---|:---|
| `task_completion` | Task produced a defined outcome | status == ok AND outputs non-empty |
| `user_feedback` | User explicitly confirmed | confirmation reference present and true |
| `artifact_exists` | Deliverable exists and is valid | file exists + schema/JSON parse |

## Failure handling
- Verification fail → log `suspected_mistake` → route table iteration.
- Chain execution failure → retry once (idempotent) → re-route → after 2 consecutive failures, pause the event type for human review.
- Never treat "retry passed without diagnosis" as a fix.

## Anti-patterns
- Output used as prediction score.
- Pure-shield verification (only checking terminal paths).
- NA bias from silently dropped failed generations.
- Greedy decode non-reproducibility.

---

## Algorithm Spec (three signals executable definition)

| signal | logic | pass |
|:---|:---|:---|
| task_completion | artifact exists + JSON parses + status field non-null | all |
| user_feedback | non-empty + no negative prefix ("no"/"reject") | affirmative |
| artifact_exists | file exists + validator callback (json.load etc.) | all |

mark_route_quality(chain_id, quality): writes verification + route_quality back to router_log · fail → suspected_mistake → feature-table iteration
