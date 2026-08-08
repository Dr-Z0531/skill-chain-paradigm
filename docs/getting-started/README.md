# 入门指南

10 分钟从零到运行一个链。

## 前置条件

- Python 3.10+
- 一组技能（SKILL.md 文件，或使用示例文件）

## 第 1 步：定义你的技能

技能以 JSON 索引声明。最小条目：

```json
{
  "skill_id": "verification",
  "state": "active",
  "deep_anchors": ["verify", "false-positive", "artifact", "logic layer"],
  "boundary_exclusions": ["single-line check", "no domain knowledge"],
  "confusable_with": [{"skill": "eval", "disambiguator": "verify→verification · score→eval"}],
  "result_signal": "artifact exists + json.load passes"
}
```

字段说明：

| 字段 | 作用 | 为什么必须有 |
|:---|:---|:---|
| `skill_id` | 技能唯一标识 | 路由、修剪、链库都以此引用 |
| `state` | 三态（active/dormant/archived） | 公理3：只有激活态可被路由 |
| `deep_anchors` | 深度锚点（核心判断层机制词） | R1：路由判定依据，防表面词幻象 |
| `boundary_exclusions` | 边界排除词 | R2：出现即不路由，负例零容忍 |
| `confusable_with` | 易混淆邻居+区分词对 | R3：混淆对显式区分 |
| `result_signal` | 用对的结果信号 | R4：路由后回验，防空转 |

完整示例见 `examples/skills.example.json`。

## 第 2 步：构建路由表

```bash
python -m src.router.build --skills examples/skills.example.json
```

## 第 3 步：运行一个事件

```bash
python -m src.router.generate "verify sub-agent output, fear false positives"
```

生成器返回一个链（JSON）：主技能 + 支持技能，长度 ≥ 1。如果只有一个技能匹配，你会得到一个**单技能链**——它仍然是链，仍然被验证，仍然被记录。

## 第 4 步：执行并验证

```bash
python -m src.store.execute --chain-id chain-xxx
python -m src.verifier.verify --chain-id chain-xxx --artifact path/to/output.json
```

验证只用确定性信号（产物存在且可解析 / 任务状态 / 显式用户确认）。链永远不会信任自己的自述。

## 一个事件从进入框架到完成的完整旅程

```
用户意图: "verify sub-agent output, fear false positives"
    │
    ▼
① 特征提取: {verify, output, false, positives}（规范化+同义词映射）
    │
    ▼
② 路由 R1-R4: 深度锚点"verify/false-positive/artifact"命中 verification
              "score/calibration"命中 eval（支持技能）
    │
    ▼
③ 链生成: [verification(main) → eval(support)]  length=2  mode=sequential
    │
    ▼
④ 链执行: verification方法论（防自述可信/逻辑层判定）→ eval（长期效果评估）
    │
    ▼
⑤ 结果回验: artifact_exists（产物存在+JSON有效）→ pass
    │
    ▼
⑥ router_log记录: chain_id/长度/回验结果/路由质量
```

## 下一步

- [架构总览](docs/architecture/README.md) — 完整模型
- [路由协议 R1–R4](docs/architecture/routing.md) — 判定机制详解
- [动态修剪](docs/architecture/pruning.md) — 可逆治理机制
