"""test_confusion_pairs.py — 混淆词对库校验（0.3.0新增）

验证:
1. 10对全部可加载·字段完整（a/b/rule）
2. 无自反对（a==b）·无重复对
3. rule非空（每对必须有判定规则）
"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), "..", "src", "data", "confusion_pairs.json")

def load_pairs():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)

def test_pairs_loadable():
    data = load_pairs()
    assert data["version"] == "0.3.0"
    assert len(data["pairs"]) >= 10, f"需≥10对·实际{len(data['pairs'])}"

def test_no_self_reflexive():
    for p in load_pairs()["pairs"]:
        assert p["a"] != p["b"], f"自反对: {p}"

def test_no_duplicates():
    seen = set()
    for p in load_pairs()["pairs"]:
        key = tuple(sorted([p["a"], p["b"]]))
        assert key not in seen, f"重复对: {p}"
        seen.add(key)

def test_rule_present():
    for p in load_pairs()["pairs"]:
        assert p.get("rule"), f"rule缺失: {p}"
