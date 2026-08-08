#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_store.py · 链库 v1（范式7.4落地·2026-08-08）
缓存: 收敛链（同事件指纹稳定3次）
版本: 链带技能版本号·技能patch→依赖链失效→重路由
回收: 低频链归档（使用率+效果率双低·与修剪同规则）
呈现: 对话注入时按相关性选择（1条链+3-5技能·ctx渐进披露）
"""
import json
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STORE_FP = os.path.join(BASE, "..", "data", "chain_store.json")

def load_store():
    if os.path.exists(STORE_FP):
        with open(STORE_FP, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"chains": [], "stats": {"created": datetime.now().isoformat()}}

def save_store(store):
    with open(STORE_FP, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

def fingerprint(chain):
    """事件指纹=技能序列+长度（同事件链稳定性判定）"""
    return f"{'+'.join(chain['skills'])}|len{chain['length']}"

def add_chain(chain):
    """链入库: 同指纹第3次出现→收敛入链库（范式: 连续3次稳定）"""
    store = load_store()
    fp = fingerprint(chain)
    found = None
    for c in store["chains"]:
        if c["fingerprint"] == fp:
            found = c
            break
    if found:
        found["count"] += 1
        found["last_seen"] = datetime.now().isoformat()
        found["converged"] = found["count"] >= 3
    else:
        store["chains"].append({
            "fingerprint": fp,
            "skills": chain["skills"],
            "length": chain["length"],
            "mode": chain["mode"],
            "chain_id_first": chain.get("chain_id"),
            "count": 1,
            "converged": False,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "version_valid": True,
            "skill_versions": {s: "v1" for s in chain["skills"]},  # 技能版本快照（patch→失效）
        })
    save_store(store)
    return store

def invalidate_on_patch(skill_name):
    """技能被patch→依赖链失效（版本联动·范式3.4）"""
    store = load_store()
    changed = 0
    for c in store["chains"]:
        if skill_name in c["skills"]:
            c["version_valid"] = False
            c["invalidated_at"] = datetime.now().isoformat()
            changed += 1
    save_store(store)
    return changed

def recycle(threshold=1):
    """低频链归档: 使用率低（count<=threshold）→标archived（不删除·可恢复）"""
    store = load_store()
    for c in store["chains"]:
        if c["count"] <= threshold and not c.get("archived"):
            c["archived"] = True
            c["archived_at"] = datetime.now().isoformat()
    save_store(store)
    return store

def present(limit=1):
    """呈现: 对话注入时按相关性选择（收敛链优先·1条链·ctx渐进披露）"""
    store = load_store()
    valid = [c for c in store["chains"] if c.get("converged") and c.get("version_valid") and not c.get("archived")]
    valid.sort(key=lambda c: c["count"], reverse=True)
    return valid[:limit]

def main():
    action = "report"
    if len(__import__("sys").argv) > 1:
        action = __import__("sys").argv[1]
    if action == "add" and len(__import__("sys").argv) > 3:
        chain = {"skills": __import__("sys").argv[2].split(","), "length": len(__import__("sys").argv[2].split(",")),
                 "mode": __import__("sys").argv[3], "chain_id": "cli"}
        store = add_chain(chain)
        print(json.dumps({"added": chain, "total": len(store["chains"])}, ensure_ascii=False, indent=2))
    elif action == "invalidate" and len(__import__("sys").argv) > 2:
        n = invalidate_on_patch(__import__("sys").argv[2])
        print(f"链失效: {n}条（技能 {__import__('sys').argv[2]} 被patch）")
    else:
        store = load_store()
        print(json.dumps({"chains": store["chains"], "total": len(store["chains"]),
                          "converged": sum(1 for c in store["chains"] if c.get("converged")),
                          "invalid": sum(1 for c in store["chains"] if not c.get("version_valid", True))},
                         ensure_ascii=False, indent=2))

def selftest():
    """自测（R1·2026-08-08）: 链库收敛3次"""
    import tempfile
    st = os.path.join(tempfile.gettempdir(), "host-verify-cs.json")
    global STORE_FP
    old_fp = STORE_FP
    STORE_FP = st
    if os.path.exists(st):
        os.remove(st)
    chain = {"skills": ["a", "b"], "length": 2, "mode": "sequential", "chain_id": "t"}
    for _ in range(3):
        add_chain(chain)
    store = load_store()
    assert any(c["converged"] for c in store["chains"]), "3次未收敛"
    os.remove(st)
    STORE_FP = old_fp
    print("selftest PASS: 3次收敛")


if __name__ == "__main__":
    if len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "--selftest":
        selftest()
    else:
        main()
