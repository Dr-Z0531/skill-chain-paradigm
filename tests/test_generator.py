# -*- coding: utf-8 -*-
"""test_generator.py — 路由生成器测试（13案例回归·pytest）"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from router.generator import build_chain, load_rules  # noqa: E402

DOC = os.path.join(os.path.dirname(__file__), "..", "src", "data")


def _cases():
    with open(os.path.join(DOC, "router_test_cases.json"), encoding="utf-8") as f:
        return json.load(f)["cases"]


def test_positive_routes():
    """正例: 6核心案例路由"""
    rules = load_rules()
    expected = {
        "三个代理协作开发怎么分工": "skill-domain-design",
        "review round-table里多个AI怎么推理彼此的意图": "skill-strategic",
        "委派给子代理的产出怎么验证可靠？怕假阳性": "skill-verification",
        "长会话后期引用早期事实越来越难": "skill-context",
        "微调SFT还是RL？奖励怎么设计": "skill-posttraining",
        "改得好不好？要不要换模型": "skill-eval",
    }
    for text, expect in expected.items():
        chain = build_chain(text, rules)
        assert chain["skills"][0] == expect, f"{text} -> {chain['skills']}"


def test_negative_no_route():
    """负例: 通用编码请求零路由"""
    rules = load_rules()
    chain = build_chain("帮我写个python脚本读Excel", rules)
    assert not chain.get("skills"), f"负例误路由: {chain}"


def test_all_cases_regression():
    """全案例回归（13项·长尾按SKILL_CHAIN_SKILLS_ROOT条件判定·开源降级语义）"""
    rules = load_rules()
    has_skills_root = bool(os.environ.get("SKILL_CHAIN_SKILLS_ROOT"))
    for case in _cases():
        text, expect = case["text"], case["expect"]
        chain = build_chain(text, rules)
        got = chain["skills"][0] if chain.get("skills") else "no_route"
        if expect == "domain-courseware-dev":
            # 长尾案例: 有技能库→命中长尾·无→降级no_route（开源环境预期）
            if has_skills_root:
                assert got == expect, f"{text}: {got} != {expect}"
            else:
                assert got == "no_route", f"{text}: 无技能库应降级, got {got}"
        else:
            assert (got == expect) if expect else (got == "no_route"), f"{text}: {got} != {expect}"
