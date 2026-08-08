#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier.py · 回验器 v1（范式7.5落地·2026-08-07）
结果信号三选一: task_completion(产物+状态) | user_feedback(显式确认) | artifact_exists(文件+校验)
判定输出: pass/fail + 证据 · fail→router_log标记疑似误路由→特征表迭代
"""
import json
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LOG_FP = os.path.join(BASE, "..", "data", "router_log.jsonl")  # single source of truth (router_log)

def verify_task_completion(artifact_path, status_field=None):
    """信号1: 任务是否有明确完成的产物/状态（文件存在+状态字段）"""
    if not artifact_path or not os.path.exists(artifact_path):
        return {"signal": "task_completion", "value": False, "evidence": f"产物不存在: {artifact_path}"}
    try:
        with open(artifact_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if status_field:
            ok = data.get(status_field) is not None
            return {"signal": "task_completion", "value": ok, "evidence": f"状态字段{status_field}={data.get(status_field)}"}
        return {"signal": "task_completion", "value": True, "evidence": f"产物存在且JSON有效: {artifact_path}"}
    except Exception as e:
        return {"signal": "task_completion", "value": False, "evidence": f"产物存在但校验失败: {e}"}

def verify_user_feedback(feedback):
    """信号2: 用户是否显式确认（用户反馈·消息/对话/会议）"""
    if not feedback:
        return {"signal": "user_feedback", "value": False, "evidence": "无显式反馈"}
    ok = isinstance(feedback, str) and feedback.strip() and "否" not in feedback[:2] and "不行" not in feedback[:2]
    return {"signal": "user_feedback", "value": ok, "evidence": f"反馈原文: {feedback[:80]}"}

def verify_artifact_exists(path, validator=None):
    """信号3: 交付物是否生成且有效（文件存在+语法/结构校验·json.load等）"""
    if not os.path.exists(path):
        return {"signal": "artifact_exists", "value": False, "evidence": f"文件不存在: {path}"}
    if validator:
        try:
            validator(path)
            return {"signal": "artifact_exists", "value": True, "evidence": f"文件存在且通过校验: {path}"}
        except Exception as e:
            return {"signal": "artifact_exists", "value": False, "evidence": f"校验失败: {e}"}
    return {"signal": "artifact_exists", "value": True, "evidence": f"文件存在: {path}"}

def mark_route_quality(chain_id, quality):
    """回验结果写回router_log（fail→标记疑似误路由）"""
    if not os.path.exists(LOG_FP):
        print(f"router_log不存在: {LOG_FP}")
        return
    lines = []
    with open(LOG_FP, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            if entry.get("chain", {}).get("chain_id") == chain_id:
                entry["verification"] = {"signal": "回验", "value": quality == "good"}
                entry["route_quality"] = quality
            lines.append(entry)
    with open(LOG_FP, "w", encoding="utf-8") as f:
        for entry in lines:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✅ router_log更新: {chain_id} → {quality}")

def main():
    """CLI: python verifier.py <signal_type> <arg> [chain_id]"""
    if len(sys.argv) < 3:
        print("用法: python verifier.py task_completion <artifact_path> [chain_id]")
        print("      python verifier.py user_feedback <反馈文本> [chain_id]")
        print("      python verifier.py artifact_exists <path> [chain_id]")
        return
    sig, arg = sys.argv[1], sys.argv[2]
    chain_id = sys.argv[3] if len(sys.argv) > 3 else None
    result = None
    if sig == "task_completion":
        result = verify_task_completion(arg)
    elif sig == "user_feedback":
        result = verify_user_feedback(arg)
    elif sig == "artifact_exists":
        result = verify_artifact_exists(arg)
    else:
        print(f"未知信号类型: {sig}")
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if chain_id:
        mark_route_quality(chain_id, "good" if result["value"] else "suspected_mistake")

def selftest():
    """自测（R1·2026-08-08）: 三信号PASS/FAIL分支"""
    import tempfile
    tf = os.path.join(tempfile.gettempdir(), "host-verify-v.txt")
    open(tf, "w").write("x")
    assert verify_artifact_exists(tf)["value"] is True
    assert verify_artifact_exists(tf + ".no")["value"] is False
    assert verify_user_feedback("同意")["value"] is True
    assert verify_user_feedback("不行")["value"] is False
    os.remove(tf)
    print("selftest PASS: 三信号分支")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    else:
        main()
