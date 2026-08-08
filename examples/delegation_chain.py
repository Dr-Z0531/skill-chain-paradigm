# -*- coding: utf-8 -*-
"""Example: a delegation chain — multi-skill, sequential (n = 4)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.router.generator import ChainGenerator

with open(os.path.join(os.path.dirname(__file__), "skills.example.json"), encoding="utf-8") as f:
    SKILLS = json.load(f)

# Add an eval skill to show the full delegation chain
SKILLS.setdefault("eval", {
    "skill_id": "eval", "state": "active", "version": "1.0.0",
    "deep_anchors": ["evaluate", "score", "which change helped"],
    "boundary_exclusions": [], "confusable_with": [],
    "result_signal": "answer which change made it better",
})

event = "delegate to agents: multi-agent cooperation, division of work, verify the output"
gen = ChainGenerator(SKILLS)
chain = gen.generate(event)
print(json.dumps(chain, ensure_ascii=False, indent=2))
print(f"length={chain['length']} mode={chain['execution_mode']}")
