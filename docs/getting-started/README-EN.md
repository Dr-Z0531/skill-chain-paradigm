# Getting Started

Zero to a running chain in ~10 minutes.

## Prerequisites
- Python 3.10+
- A set of skills with `SKILL.md` files (or the example file)

## Step 1: Define your skills

Skills are declared in a JSON index. Minimal entry:

```json
{
  "skill_id": "verification",
  "state": "active",
  "deep_anchors": ["verify", "false-positive", "artifact", "logic layer"],
  "boundary_exclusions": ["single-line check", "no domain knowledge"],
  "confusable_with": [{"skill": "eval", "disambiguator": "verify→verification · score→eval"}],
  "result_signal": "artifact exists + json.load passes"
}
```

See `examples/skills.example.json` for a complete file.

## Step 2: Build the routing table

```bash
python -m src.router.build --skills examples/skills.example.json
```

## Step 3: Run an event

```bash
python -m src.router.generate "verify sub-agent output, fear false positives"
```

The generator returns a chain (JSON): main skill + support skills, length ≥ 1. If only one skill matches, you get a **single-skill chain** — still a chain, still verified, still logged.

## Step 4: Execute and verify

```bash
python -m src.store.execute --chain-id chain-xxx
python -m src.verifier.verify --chain-id chain-xxx --artifact path/to/output.json
```

Verification uses deterministic signals only (artifact exists + parses; task status; explicit user confirmation). The chain never trusts its own self-report.

## Next steps
- [Architecture](docs/architecture/README-EN.md) — the full model
- [Routing](docs/architecture/routing-EN.md) — the R1–R4 protocol
- [Pruning](docs/architecture/pruning-EN.md) — reversible governance
