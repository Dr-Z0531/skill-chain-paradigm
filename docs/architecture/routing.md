# 路由协议（R1–R4）

路由是意图→技能的匹配。它的失败模式是**表面词幻象**：描述里写着"agents"，于是所有沾"代理"的请求都匹配上，即使结构上根本不合适。

## R1 — 深度优先于表面

用**深度锚点**（每个技能"核心判断"章节的机制词）匹配意图，绝不用描述文字。

**为什么**：描述是"给读者看的广告"，锚点是"技能实际做什么"的机制词。广告会夸大（"全能代理"），机制词不会骗人（"四字段认知循环"只属于战略推理技能）。

**反例**：用户说"三个代理协作开发怎么分工"——表面词"代理"会命中所有代理类技能；锚点"分工/编排"命中 orchestration，"推理/意图"命中 strategic——深度锚点直接指向正确技能。

## R2 — 边界排除先行

意图包含某技能的边界排除词 → 该技能在任何正向匹配前就被排除。

**为什么**：负例路由必须零容忍。一个"单代理决策"场景路由到战略推理技能，产出必然是错的。排除比匹配更便宜、更可靠。

**例子**：strategic 的边界排除词含"单代理/非博弈"——"帮我做个单代理决策"直接排除，绝不再看它的锚点。

## R3 — 混淆对显式区分

容易混淆的技能携带显式区分词对：

| 混淆对 | 区分判据 |
|:---|:---|
| orchestration ↔ strategic | "分工/编排"→orchestration · "推理/意图/博弈"→strategic |
| verification ↔ evaluation | "验证架构/蕴含/假阳性"→verification · "评分/校准"→evaluation |
| context-engineering ↔ memory | "状态栏/临时进度"→context · "长期记忆/跨会话"→memory |

双方都命中时，区分词对裁决，败者出局。

**为什么**：混淆对的双方锚点高度相似（都会说"多智能体""验证"），如果不显式区分，路由每次都在两者之间摇摆——区分词对把"二选一"变成确定性规则。

## R4 — 结果信号回验

路由执行后，用技能的"结果信号"对照实际结果。不达标 → 标记 `suspected_mistake` → 反馈回路由表（特征迭代）。

**为什么**：路由可能错（锚点覆盖不全/意图太新）。没有回验，错误路由永远不被发现；有了回验，每个错误路由都是特征表的改进输入。

## 分层路由

- **核心技能**（有深度锚点）：精确路由。
- **长尾技能**（暂无锚点）：按分类目录宽路由——降级但不错误。高使用率长尾自动升级深度锚定。

## 路由日志

每次路由都记录（指纹/候选集/选中/证据/结果）。日志是修剪、聚类、自学习的唯一数据源——**日志先行，决策后置**。

---

## 算法规格（Algorithm Spec·R1-R4 可执行定义）

### route(text, rules) 伪代码

```
输入: 事件文本text·路由规则rules（skills[].anchors/exclusions/confusions）
输出: {selected, level, candidates}

1. feats = extract_features(text)          # 原文词 + 同义词桥归一化（R1.5·仅归一化）
2. results = []
   for sk in rules.skills:
     if any(e in text for e in sk.exclusions):  # R2排除先行·零容忍
        results.append({name, status: excluded}); continue
     hits = [a for a in sk.anchors if a in text or a in feats]   # R1深度锚点
     results.append({name, status: candidate if hits else no_anchor, anchor_count: len(hits)})
3. cands = sort(results.candidates, by anchor_count desc)
   if not cands: return {selected: [], level: none}
4. top = cands[0]
   # R3混淆裁决: 前两名是易混淆对→区分词对裁决
   if len(cands) >= 2 and top.confusions contains cands[1].name:
      pair = top.confusions[second].pair      # pair[0]=本方·pair[1]=对方
      if pair[1] in text and pair[0] not in text: swap(top, second)  # 对方胜出
5. level = high if top.anchor_count >= 2 else (medium if == 1 else low)
6. return {selected: [top], level, candidates}
```

### 参数表

| 参数 | 值 | 含义 | 校准 |
|:---|:---|:---|:---|
| anchor_count≥2 | high | 双锚点=高置信 | 2周数据校准 |
| anchor_count=1 | medium | 单锚点=中置信 | 同上 |
| misroute门槛 | ≥2关键词 | 长尾单关键词=一词多义→不路由 | 2026-08-08实证 |
| 桥权重 | α=0.7/β=0.3 | 锚点优先·桥降级（R1.5） | C11 |

### 边界条件

- 负例保护: 通用编码请求（"帮我写/写个脚本/写个python/写一段代码"）→直接不路由
- 无候选: no_route→长尾兜底（route_longtail·≥2关键词·取Top-3）→仍无→no_route（记log）
- 验证必加: 主技能非验证类→链追加 skill-verification（协议V每链必有）
