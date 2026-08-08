# -*- coding: utf-8 -*-
"""Example: a single-skill chain — the shortest valid unit of work (n = 1)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.router.generator import ChainGenerator
from src.verifier.verifier import Verifier

with open(os.path.join(os.path.dirname(__file__), "skills.example.json"), encoding="utf-8") as f:
    SKILLS = json.load(f)

event = "verify the output artifact, I fear false positives"

gen = ChainGenerator(SKILLS)
chain = gen.generate(event)
print(json.dumps(chain, ensure_ascii=False, indent=2))

# The chain is the only unit of work: even n=1 goes through the full protocol.
assert chain["length"] == 1
assert "single-skill chain" in chain.get("note", "")

# Verification is deterministic — the chain never trusts its own self-report.
with open("output.json", "w", encoding="utf-8") as f:
    json.dump({"ok": True}, f)
verdict = Verifier().verify(chain, {"artifact_path": "output.json"})
print("verification:", verdict)
