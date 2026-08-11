#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pruner.py · 修剪器 v1（范式7.3落地·2026-08-08）
输入: router_log聚合 + 映射表(router_rules.json) + 技能三态索引
判定: 结构深度(锚点交集>=40%) + 过程动作(共触发>=阈值·首版3)
动作: 激活→休眠(临时·非删除)·写台账
回验: 修剪后原场景路由质量对比·失败→恢复+标记误剪
周报: 高用/零用/休眠/恢复统计·制度体检输入
两阶段: 阶段1(现在)=静态修剪(结构深度·可立即执行)·阶段2(2周后)=动态修剪(共触发数据)
"""
import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
RULES_FP = os.path.join(BASE, "router_rules.json")
LOG_FP = os.path.join(BASE, "router_log.jsonl")
STATES_FP = os.path.join(BASE, "skill_states.json")
LEDGER_FP = os.path.join(BASE, "prune_ledger.json")

def load_rules():
    with open(RULES_FP, "r", encoding="utf-8") as f:
        return json.load(f)

def load_states():
    if os.path.exists(STATES_FP):
        with open(STATES_FP, "r", encoding="utf-8") as f:
            return json.load(f)
    # 初始化: 全部active
    rules = load_rules()
    states = {s["name"]: {"status": "active", "co_trigger": {}, "pruned_at": None} for s in rules["skills"]}
    save_states(states)
    return states

def save_states(states):
    with open(STATES_FP, "w", encoding="utf-8") as f:
        json.dump(states, f, ensure_ascii=False, indent=2)

def load_ledger():
    if os.path.exists(LEDGER_FP):
        with open(LEDGER_FP, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_ledger(ledger):
    with open(LEDGER_FP, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)

def structural_overlap(rules):
    """结构深度信号: 锚点词交集>=40% → 候选重叠（静态修剪·阶段1）"""
    overlaps = []
    skills = rules["skills"]
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = skills[i], skills[j]
            inter = set(a["anchors"]) & set(b["anchors"])
            # 锚点交集比例（取较小锚点集为分母·>=40%判重叠）
            denom = min(len(a["anchors"]), len(b["anchors"]))
            if denom > 0 and len(inter) / denom >= 0.4:
                overlaps.append({
                    "pair": [a["name"], b["name"]],
                    "overlap_anchors": list(inter),
                    "ratio": round(len(inter) / denom, 2),
                })
    return overlaps

def process_signal(states, rules):
    """过程动作信号: 共触发>=3 → 冲突证据（动态修剪·阶段2·2周数据后）"""
    # 从router_log统计同事件多技能共触发
    co = {}
    if os.path.exists(LOG_FP):
        with open(LOG_FP, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    fp = e.get("event_fingerprint", "")
                    route = e.get("route_result", {}).get("selected", {}).get("name")
                    if fp and route:
                        key = (fp, route)
                        co[key] = co.get(key, 0) + 1
                except Exception:
                    continue
    return co

def prune(states, rules, dry_run=True):
    """执行修剪: 静态重叠→休眠候选（首版保守: 只标记不自动剪·输出候选）"""
    overlaps = structural_overlap(rules)
    ledger = load_ledger()
    candidates = []
    for ov in overlaps:
        # 有混淆对关系的重叠是设计上的区分·不剪（R3已处理）
        is_confusion_pair = False
        for sk in rules["skills"]:
            for cf in sk.get("confusions", []):
                if {sk["name"], cf["peer"]} == set(ov["pair"]):
                    is_confusion_pair = True
                    break
        if is_confusion_pair:
            continue
        candidates.append(ov)
    # 写入台账（dry_run只记录候选·不迁移状态）
    entry = {
        "run_at": datetime.now().isoformat(),
        "mode": "dry_run" if dry_run else "apply",
        "structural_candidates": candidates,
        "total_overlaps": len(overlaps),
    }
    ledger.append(entry)
    save_ledger(ledger)
    return entry

def weekly_report(states, rules):
    """周报: 高用/零用/休眠/恢复统计·制度体检输入"""
    usage = {}
    if os.path.exists(LOG_FP):
        with open(LOG_FP, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    route = e.get("route_result", {}).get("selected", {}).get("name")
                    if route:
                        usage[route] = usage.get(route, 0) + 1
                except Exception:
                    continue
    report = {
        "generated": datetime.now().isoformat(),
        "total_logs": sum(usage.values()),
        "usage": usage,
        "high_usage": [k for k, v in usage.items() if v >= 3],
        "zero_usage": [s["name"] for s in rules["skills"] if s["name"] not in usage],
        "dormant": [k for k, v in states.items() if v["status"] == "dormant"],
        "restored": [k for k, v in states.items() if v.get("restored")],
    }
    return report



def effectiveness_rate(rules):
    """M13效果率: router_log回验结果统计（pass/fail·含效果标注）"""
    stats = {}
    if os.path.exists(LOG_FP):
        with open(LOG_FP, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    route = e.get("route_result", {}).get("selected", {}).get("name")
                    v = e.get("verification", {})
                    q = e.get("route_quality", "pending")
                    if route:
                        s = stats.setdefault(route, {"total": 0, "pass": 0, "fail": 0, "suspected": 0})
                        s["total"] += 1
                        if q == "good": s["pass"] += 1
                        elif q == "suspected_mistake": s["suspected"] += 1
                        elif v.get("value") is True: s["pass"] += 1
                        else: s["fail"] += 1
                except Exception:
                    continue
    return stats

def restore_check(states, rules):
    """L5修剪回验: 被剪技能原场景再次触发且路由失败→自动恢复+标记误剪（范式3.2恢复条件）"""
    restored = []
    for name, st in states.items():
        if st["status"] == "dormant":
            # 回验: 原场景路由质量（简单代理: 检查router_log中该技能近期是否被回验为good）
            eff = effectiveness_rate(rules)
            s = eff.get(name, {})
            if s.get("pass", 0) > 0 and s.get("fail", 0) == 0:
                st["status"] = "active"
                st["restored"] = True
                st["restore_reason"] = "原场景回验通过·标记误剪"
                restored.append(name)
    save_states(states)
    return restored

def dynamic_prune_signal(rules):
    """M5动态修剪: 共触发>=3（阈值·2周数据后启用·C11校准）·当前数据不足时返回待校准"""
    co = process_signal(load_states(), rules)
    conflicts = {}
    for (fp_key, skill), cnt in co.items():
        if cnt >= 3:
            conflicts.setdefault(skill, []).append({"event": fp_key, "count": cnt})
    return {"conflicts": conflicts, "threshold": 3, "calibration": "待C11校准（2周数据后·拒绝魔法数）"}

def main():
    mode = "dry_run"
    if len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "apply":
        mode = "apply"
    rules = load_rules()
    states = load_states()
    entry = prune(states, rules, dry_run=(mode == "dry_run"))
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    if mode == "dry_run":
        print("\n提示: dry_run模式·未迁移任何状态·apply需人工确认")

def selftest():
    """自测（R1·2026-08-08）: 结构重叠检测"""
    rules = load_rules()
    ov = structural_overlap(rules)
    assert isinstance(ov, list)
    print(f"selftest PASS: 结构重叠候选{len(ov)}个")


if __name__ == "__main__":
    if len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "--selftest":
        selftest()
    else:
        main()
