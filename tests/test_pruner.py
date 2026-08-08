# -*- coding: utf-8 -*-
"""test_pruner.py — 修剪器测试（结构重叠·混淆对排除·dry_run台账）"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pruner.pruner as pr  # noqa: E402

# 隔离数据路径（防污染真实data/）
TMP = os.path.join(os.path.dirname(__file__), "_tmp_pruner")
os.makedirs(TMP, exist_ok=True)
pr.RULES_FP = os.path.join(TMP, "router_rules.json")
pr.LOG_FP = os.path.join(TMP, "router_log.jsonl")
pr.STATES_FP = os.path.join(TMP, "skill_states.json")
pr.LEDGER_FP = os.path.join(TMP, "prune_ledger.json")


def _mk_rules(skills):
    """构造最小rules"""
    return {
        "meta": {"version": "test"},
        "protocol": {},
        "skills": skills,
    }


def _skill(name, anchors, confusions=None):
    return {
        "name": name,
        "core_layer": name,
        "anchors": anchors,
        "exclusions": [],
        "confusions": confusions or [],
        "result_signal": "",
        "dep_chains": [],
    }


def _clean():
    for f in ["router_rules.json", "router_log.jsonl", "skill_states.json", "prune_ledger.json"]:
        fp = os.path.join(TMP, f)
        if os.path.exists(fp):
            os.remove(fp)


def test_structural_overlap_detects_40pct():
    """锚点交集>=40% → 结构重叠候选"""
    _clean()
    # A: 4锚点 · B: 与A交集2个（2/4=50%>=40%）
    rules = _mk_rules([
        _skill("skill-a", ["锚点1", "锚点2", "锚点3", "锚点4"]),
        _skill("skill-b", ["锚点1", "锚点2", "锚点5", "锚点6"]),
    ])
    overlaps = pr.structural_overlap(rules)
    assert len(overlaps) == 1, f"应检出1对重叠, got {overlaps}"
    assert set(overlaps[0]["pair"]) == {"skill-a", "skill-b"}
    assert overlaps[0]["ratio"] >= 0.4


def test_structural_overlap_below_threshold():
    """锚点交集<40% → 不判重叠"""
    _clean()
    rules = _mk_rules([
        _skill("skill-a", ["锚点1", "锚点2", "锚点3", "锚点4", "锚点5"]),
        _skill("skill-b", ["锚点1", "锚点6", "锚点7", "锚点8", "锚点9"]),
    ])
    assert pr.structural_overlap(rules) == []


def _write_rules(rules):
    """写rules到隔离路径（load_states初始化依赖）"""
    with open(pr.RULES_FP, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False)


def test_prune_excludes_confusion_pairs():
    """有混淆对关系的重叠是设计区分（R3）·修剪必须排除"""
    _clean()
    rules = _mk_rules([
        _skill("skill-a", ["锚点1", "锚点2", "锚点3", "锚点4"],
               confusions=[{"peer": "skill-b", "pair": ["区分词X", "区分词Y"]}]),
        _skill("skill-b", ["锚点1", "锚点2", "锚点5", "锚点6"]),
    ])
    _write_rules(rules)
    states = pr.load_states()
    entry = pr.prune(states, rules, dry_run=True)
    assert entry["total_overlaps"] == 1, "结构上有1对重叠"
    assert entry["structural_candidates"] == [], "混淆对必须被排除出修剪候选"


def test_prune_dry_run_records_ledger():
    """dry_run: 候选记台账·技能状态不迁移"""
    _clean()
    rules = _mk_rules([
        _skill("skill-a", ["锚点1", "锚点2", "锚点3", "锚点4"]),
        _skill("skill-c", ["锚点1", "锚点2", "锚点5", "锚点6"]),
    ])
    _write_rules(rules)
    states = pr.load_states()
    entry = pr.prune(states, rules, dry_run=True)
    assert entry["mode"] == "dry_run"
    assert len(entry["structural_candidates"]) == 1
    # 状态未被迁移（仍是active）
    assert all(s["status"] == "active" for s in states.values())
    # 台账已写入
    ledger = pr.load_ledger()
    assert len(ledger) == 1 and ledger[-1]["mode"] == "dry_run"
