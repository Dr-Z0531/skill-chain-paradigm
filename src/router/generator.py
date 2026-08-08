#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_generator.py · 技能链生成器 v1（范式7.1落地·2026-08-07）
输入: 事件意图文本 + router_rules.json（映射表六列代码化）+ 技能三态索引 + 链库
输出: chain实例（JSON·chain_id+技能序列+长度+执行模式）
协议: E→R→G→X→V→Log 之 R+G 环节
"""
import json
import os
import re
import sys
import uuid
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
RULES_FP = os.path.join(BASE, "..", "data", "router_rules.json")
CHAIN_STORE_FP = os.path.join(BASE, "..", "data", "chain_store.json")
LOG_FP = os.path.join(BASE, "..", "data", "router_log.jsonl")  # single source of truth (router_log)

SYNONYM_BRIDGE = {
    # 用户高频说法 -> 锚点语（R1.5·仅归一化·非独立路由）·短语级优先·防误触
    "记不住": "状态栏", "越聊越笨": "上下文腐化", "历史太长": "渐进披露",
    "长会话": "上下文腐化", "引用早期事实": "上下文腐化", "早期的事实": "上下文腐化",
    "被网页骗": "提示注入", "插件安全": "护栏分层", "工具权限": "最小权限",
    "自我改进": "在线离线双循环", "越用越聪明": "跨轨迹对照",
    "记住偏好": "只追加不删除", "知识库": "先提炼再索引", "RAG": "双层记忆",
    "微调": "先SFT后RL", "奖励设计": "防Goodhart", "换模型": "三层验证器",
    "证明变好": "校准kappa>0.7", "技术可行性": "辩论脚本", "效率原则": "四字段认知循环", "领域代理": "多Agent编排", "多Agent分工": "多Agent编排",
    "怎么分工": "多Agent编排", "分工": "多Agent编排", "编排": "多Agent编排",
    "协作开发": "多Agent编排", "多个代理": "多Agent编排", "委派": "多Agent编排",
    "复盘": "跨轨迹对照", "任务分派": "多Agent编排", "今日任务": "多Agent编排",
    "对手意图": "OpponentIntent", "彼此的意图": "OpponentIntent", "推理对手": "OpponentIntent",
    "推理彼此的意图": "OpponentIntent", "博弈": "self-play失效", "战略推理": "四字段认知循环",
    "对手": "OpponentIntent",
    "防假阳性": "防自述可信", "假阳性": "防自述可信", "不可信": "防自述可信",
    "可靠验证": "独立逻辑层判定", "验证可靠": "独立逻辑层判定", "验证器": "双保险",
    "验证链": "双保险", "全链走一遍": "双保险", "E到R到G": "双保险", "回验": "独立逻辑层判定",
    "五步法": "五步闭环", "多轮审查": "收敛检查表", "全面推演": "辩论脚本",
    "证据链": "五维15检查", "Agent审查": "Task Episode",
}

def load_rules():
    with open(RULES_FP, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_features(text):
    """意图特征提取: 原文词 + 同义词桥归一化词"""
    feats = set()
    for w in SYNONYM_BRIDGE:
        if w in text:
            feats.add(w)
            feats.add(SYNONYM_BRIDGE[w])
    return list(feats)

def route(text, rules):
    """路由R1-R4: 排除先行→锚点匹配→混淆裁决→置信度分级"""
    protocol = rules["protocol"]
    feats = extract_features(text)
    results = []
    for sk in rules["skills"]:
        name = sk["name"]
        # R2 边界排除先行
        excluded = [e for e in sk["exclusions"] if e in text]
        if excluded:
            results.append({"name": name, "status": "excluded", "by": excluded[0]})
            continue
        # R1 深度锚点匹配
        hits = [a for a in sk["anchors"] if a in text or a in feats]
        if hits:
            results.append({"name": name, "status": "candidate", "anchor_hits": hits,
                            "anchor_count": len(hits)})
        else:
            results.append({"name": name, "status": "no_anchor"})
    # 候选排序: 锚点命中数降序
    cands = [r for r in results if r["status"] == "candidate"]
    cands.sort(key=lambda r: r["anchor_count"], reverse=True)
    if not cands:
        return {"selected": [], "level": "none", "candidates": results}
    top = cands[0]
    # R3 混淆裁决: 若前两名是易混淆对→用区分词对
    if len(cands) >= 2:
        second = cands[1]
        for sk in rules["skills"]:
            if sk["name"] == top["name"]:
                for cf in sk.get("confusions", []):
                    if cf["peer"] == second["name"]:
                        # 区分词对: pair[0]=本方·pair[1]=对方
                        if cf["pair"][1] in text and cf["pair"][0] not in text:
                            top, cands[1] = cands[1], top  # 对方胜出
                        break
    # 置信度分级
    # medium语义（反思2026-08-08）: 1锚点命中·若有混淆对候选→R3裁决已执行·无对可裁决=直路由（等价实现）
    conf = "high" if top["anchor_count"] >= 2 else ("medium" if top["anchor_count"] == 1 else "low")
    return {"selected": [top], "level": conf, "candidates": cands, "feats": feats}



def route_longtail(text, rules, core_results):
    """M4分层路由: 11核心深度锚定 + 长尾目录兜底（宽路由·降级但不出错）"""
    # 长尾技能=不在router_rules核心11中的技能·从SKILL.md description提取关键词
    # 负例保护（2026-08-08案例回归: 通用编码请求单关键词误触）
    generic_code = ["帮我写", "写个脚本", "写个python", "写一个", "脚本读", "做个脚本", "写段代码"]
    if any(g in text for g in generic_code):
        return []
    longtail = _load_longtail_index()
    hits = []
    for name, desc_kw in longtail.items():
        matched = [k for k in desc_kw if k in text]
        if matched:
            hits.append({"name": name, "matched": matched, "count": len(matched)})
    # 质量门槛（2026-08-08 misroute修正）: 单关键词命中=一词多义风险→不路由（记unrouted·交人工）
    # 只有≥2个独立关键词命中才认为语境明确（如"可视化报告生成"需同时含可视化+报告类词）
    hits = [h for h in hits if h["count"] >= 2]
    hits.sort(key=lambda h: h["count"], reverse=True)
    return hits[:3]

_LONGTAIL_INDEX = None
def _load_longtail_index():
    """长尾技能索引: skills目录下SKILL.md的description前57字关键词（入档自动抽取·升锚数据源）"""
    global _LONGTAIL_INDEX
    if _LONGTAIL_INDEX is not None:
        return _LONGTAIL_INDEX
    idx = {}
    # 长尾索引目录（开源可配置: 环境变量SKILL_CHAIN_SKILLS_ROOT·默认相对hostDate）
    skills_root = os.environ.get("SKILL_CHAIN_SKILLS_ROOT",
                                 os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "hostDate", "skills"))
    for root, dirs, files in os.walk(skills_root):
        if "SKILL.md" in files:
            fp = os.path.join(root, "SKILL.md")
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                name = os.path.basename(root)
                # description提取（frontmatter）
                import re
                m = re.search(r'description:\s*["\']?(.+?)[\"\']?\n', content)
                desc = m.group(1)[:120] if m else ""
                # 关键词: 中文短语（2-6字）+英文词
                kw = set(re.findall(r'[\u4e00-\u9fa5]{2,6}', desc))
                kw |= set(re.findall(r'[a-zA-Z]{4,}', desc))
                if kw:
                    idx[name] = list(kw)
            except Exception:
                continue
    _LONGTAIL_INDEX = idx
    return idx

def build_chain(text, rules):
    """链组装: 主技能+支持技能+验证技能·长度由事件复杂度×可用集×历史效果"""
    r = route(text, rules)
    if not r["selected"]:
        # M4长尾兜底（2026-08-08案例回归暴露: 长尾层未接入主流程）
        lt = route_longtail(text, rules, r)
        if lt:
            chain_id = f"chain-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
            return {"chain_id": chain_id, "skills": [lt[0]["name"]], "length": 1,
                    "mode": "sequential", "route": {"selected": {"name": lt[0]["name"], "status": "longtail"},
                    "confidence": "low", "evidence": lt[0]["matched"]},
                    "created": datetime.now().isoformat()}
        return {"chain_id": None, "error": "no_route", "detail": r}
    main = r["selected"][0]
    chain = [main["name"]]
    # 支持/验证技能: 范式协议E→R→G→X→V→Log中V验证=每链必有（2026-08-08protocol refinement: 原实现只在文本含"验证/可靠"时追加→实际全单链）
    # 标准链=主技能+验证技能(length=2)·除非主技能本身是验证类
    if main["name"] != "skill-verification":
        chain.append("skill-verification")
    # 复杂事件追加支持技能（多锚点命中/长文本→加深度支持）
    complexity = len(r.get("feats", [])) + len(text)
    if complexity > 80 and main["name"] not in ("skill-verification", "skill-deep-review"):
        chain.append("skill-deep-review")  # 复杂任务审查支持
    mode = "sequential" if len(chain) <= 1 else ("hybrid" if len(chain) >= 3 else "sequential")
    chain_id = f"chain-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    return {
        "chain_id": chain_id,
        "skills": chain,
        "length": len(chain),
        "mode": mode,
        "route": {"selected": main, "confidence": r["level"], "evidence": r["feats"]},
        "created": datetime.now().isoformat(),
    }

def log_chain(chain, event_text, route_source="auto"):
    """router_log记录（7.2 schema·唯一数据源）·2026-08-08修复: 补skills·verdict字段统一"""
    entry = {
        "log_id": f"log-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "event_fingerprint": re.sub(r"\s+", " ", event_text)[:60],
        "event_text": event_text[:120],
        "route_result": chain.get("route"),
        "chain": {"chain_id": chain.get("chain_id"), "skills": chain.get("skills") or [],
                  "length": chain.get("length"), "mode": chain.get("mode")},
        "skills": chain.get("skills") or [],   # 顶层冗余（兼容统计·单一事实=chain.skills）
        "length": chain.get("length") or len(chain.get("skills") or []),
        "execution": {"status": "pending"},
        "verdict": {"signal": None, "value": None},   # 统一verdict（旧条目verification字段兼容读取）
        "route_quality": "pending",
        "route_source": route_source,   # auto=路由生成 / user=用户显式指定 / manual=no_route后人工选择
    }
    with open(LOG_FP, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

def main():
    if len(sys.argv) < 2:
        print("用法: python chain_generator.py '<事件意图文本>'")
        return
    text = sys.argv[1]
    rules = load_rules()
    chain = build_chain(text, rules)
    if chain.get("chain_id"):
        log_chain(chain, text)
    else:
        # 负例也记录（试点2026-08-08: no_route须入router_log·防统计缺失）
        log_chain({"chain_id": None, "skills": [], "length": 0, "mode": "none",
                   "route": {"selected": {"name": "no_route"}, "confidence": "none", "evidence": []}}, text)
    print(json.dumps(chain, ensure_ascii=False, indent=2))

def selftest():
    """自测（R1·2026-08-08）: 核心路由+负例"""
    rules = load_rules()
    ch = build_chain("三个代理协作开发怎么分工", rules)
    assert ch["skills"][0] == "agentic-domain-design", f"路由失败: {ch}"
    ch2 = build_chain("帮我写个python脚本读Excel", rules)
    assert not ch2.get("skills"), f"负例误路由: {ch2}"
    print("selftest PASS: 路由+负例")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
    else:
        main()
