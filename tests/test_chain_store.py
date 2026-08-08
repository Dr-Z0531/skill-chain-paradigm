# -*- coding: utf-8 -*-
"""test_chain_store.py — 链库测试（3次收敛·patch失效·低频回收）"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import store.chain_store as cs  # noqa: E402

# 隔离数据路径
TMP = os.path.join(os.path.dirname(__file__), "_tmp_store")
os.makedirs(TMP, exist_ok=True)
cs.STORE_FP = os.path.join(TMP, "chain_store.json")


def _chain(skills, mode="sequential"):
    return {
        "skills": skills,
        "length": len(skills),
        "mode": mode,
        "chain_id": "test",
    }


def _clean():
    if os.path.exists(cs.STORE_FP):
        os.remove(cs.STORE_FP)


def test_converge_after_3_identical():
    """同指纹链连续3次 → 收敛（converged=True）·前2次不收敛"""
    _clean()
    c = _chain(["skill-a", "skill-b"])
    s1 = cs.add_chain(c)
    assert s1["chains"][0]["converged"] is False, "第1次不收敛"
    s2 = cs.add_chain(c)
    assert s2["chains"][0]["converged"] is False, "第2次不收敛"
    s3 = cs.add_chain(c)
    assert s3["chains"][0]["converged"] is True, "第3次收敛"


def test_diff_fingerprint_not_converged():
    """不同指纹链各自计数·不互相累加"""
    _clean()
    cs.add_chain(_chain(["skill-a", "skill-b"]))
    cs.add_chain(_chain(["skill-a", "skill-b"]))
    cs.add_chain(_chain(["skill-a", "skill-c"]))  # 不同链
    store = cs.load_store()
    assert len(store["chains"]) == 2
    ab = [c for c in store["chains"] if c["skills"] == ["skill-a", "skill-b"]][0]
    ac = [c for c in store["chains"] if c["skills"] == ["skill-a", "skill-c"]][0]
    assert ab["count"] == 2 and ab["converged"] is False
    assert ac["count"] == 1 and ac["converged"] is False


def test_patch_invalidates_dependent_chains():
    """技能被patch → 依赖链失效（版本联动）·无关链保留"""
    _clean()
    cs.add_chain(_chain(["skill-a", "skill-b"]))
    cs.add_chain(_chain(["skill-c"]))
    n = cs.invalidate_on_patch("skill-a")
    assert n == 1, f"应失效1条, got {n}"
    store = cs.load_store()
    ab = [c for c in store["chains"] if c["skills"] == ["skill-a", "skill-b"]][0]
    cc = [c for c in store["chains"] if c["skills"] == ["skill-c"]][0]
    assert ab["version_valid"] is False, "依赖链必须失效"
    assert cc["version_valid"] is True, "无关链不受影响"


def test_recycle_low_frequency_archives():
    """低频链回收: count<=threshold → archived（不删除·可恢复）"""
    _clean()
    cs.add_chain(_chain(["skill-a", "skill-b"]))  # count=1
    cs.add_chain(_chain(["skill-c"]))
    cs.add_chain(_chain(["skill-c"]))  # count=2
    store = cs.recycle(threshold=1)
    ab = [c for c in store["chains"] if c["skills"] == ["skill-a", "skill-b"]][0]
    cc = [c for c in store["chains"] if c["skills"] == ["skill-c"]][0]
    assert ab.get("archived") is True, "低频链应归档"
    assert cc.get("archived") is None, "高频链保留"


def test_present_prefers_converged_valid():
    """呈现: 只选 收敛+有效+未归档 的链·按count降序"""
    _clean()
    cs.add_chain(_chain(["skill-a", "skill-b"]))
    cs.add_chain(_chain(["skill-a", "skill-b"]))
    cs.add_chain(_chain(["skill-a", "skill-b"]))  # 收敛
    cs.add_chain(_chain(["skill-x"]))  # 低频未收敛
    shown = cs.present(limit=1)
    assert len(shown) == 1
    assert shown[0]["skills"] == ["skill-a", "skill-b"], "收敛链优先呈现"
    # patch后收敛链失效 → 不再呈现
    cs.invalidate_on_patch("skill-a")
    assert cs.present(limit=1) == [], "失效链不呈现"
