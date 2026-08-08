# 动态修剪

修剪是技能生态的治理：没有它，技能库无边界增长。

## 为什么需要修剪

技能库的自然趋势是只增不减。技能蒸馏流程每批产出新技能，旧技能从不消失——最终 数百个技能中一半从未被调用，但它们占据着路由空间和上下文预算。修剪回答的问题是：**哪些技能该暂时退场，让生态保持轻量？**

## 双信号评估

技能成为修剪候选，必须**两个信号同时触发**：

| 信号 | 类型 | 首版判据（保守） |
|:---|:---|:---|
| 锚点重叠 | 静态 | 与邻居的锚点词汇重叠 ≥ 40% |
| 共触发频率 | 动态 | 14 天内同一事件同时触发两个技能 ≥ 3 次 |

**为什么双信号**：单信号会误判——锚点重叠高可能是巧合（两个技能都提"验证"但领域不同）；共触发高可能是场景巧合（两个技能恰好都匹配但各司其职）。双信号 AND 才修剪：静态证明"结构上像"，动态证明"行为上真的冲突"。

**为什么首版保守**：误剪的代价（好技能被藏起来）高于漏剪的代价（多留一个技能）。首版阈值故意偏高，运行 2 周后用日志数据按信号分布校准——**拒绝魔法数，校准后才生效**。

## 临时迁移（不是删除）

修剪 = `active → dormant`。**永不删除。**

**为什么**：删除不可逆，休眠可恢复。技能的价值可能在未来场景出现（新的蒸馏方向、新的任务类型）。休眠技能保留全部内容，只是暂时不参与路由。

## 台账与周盘点

每次修剪记录：`pruned_at` / `reason` / `restore_condition` / `verify_status`。每周盘点核对台账。依赖被剪技能的链在修剪**之前**失效（先链后剪）。

**为什么先链后剪**：链可能引用将被休眠的技能——先失效链，再修剪技能，避免"链引用了被剪技能"的悬空状态。

## 回验恢复（误剪闭环）

被剪技能的原场景路由质量下降 → 自动恢复 + 标记"误剪"。

**为什么**：修剪可能是错的（阈值过严/场景变化）。回验让修剪变成自校正机制：误剪会被发现、恢复、并记录——每次误剪都是阈值校准的输入。

## 防误伤三机制

1. **长尾配额**：每周至少 1 次长尾技能轮换探测——防修剪偏见（只剪不用的，结果更不用的被剪得更多）；
2. **马太效应防制**：高频链不得垄断路由空间——配额保证长尾曝光公平；
3. **沉默修剪禁止**：一切修剪在台账中可见——没有悄悄消失的技能。

---

## 算法规格（Algorithm Spec·两阶段修剪可执行定义）

### structural_overlap(rules) 伪代码（阶段1·静态）

```
输入: rules.skills（anchors列表）
输出: overlaps[].pair/overlap_anchors/ratio

for i in range(len(skills)):
  for j in range(i+1, len(skills)):
    inter = set(skills[i].anchors) & set(skills[j].anchors)
    denom = min(len(a.anchors), len(b.anchors))
    if denom > 0 and len(inter)/denom >= 0.4:   # 阈值40%
      overlaps.append({pair, overlap_anchors, ratio})
```

### dynamic_prune_signal（阶段2·动态·2周数据后）

```
co = {}   # (event_fingerprint, route) -> count（从router_log逐行统计）
for line in router_log:
  e = json.loads(line)
  if e.event_fingerprint and e.route_result.selected.name:
    co[(fp, route)] += 1
conflicts = {skill: events} where count >= 3    # 共触发阈值3
calibration: "待C11校准（2周数据后·拒绝魔法数）"
```

### restore_check（L5回验恢复）

```
for name, st in states:
  if st.status == dormant:
    eff = effectiveness_rate(name)              # pass/fail统计
    if eff.pass > 0 and eff.fail == 0:          # 原场景回验全过
      st.status = active; st.restored = True; st.restore_reason = "误剪恢复"
```

### 参数表

| 参数 | 值 | 含义 | 校准 |
|:---|:---|:---|:---|
| 重叠阈值 | 40%（交集/小锚点集） | 结构重叠判据 | 2周 |
| 共触发阈值 | 3次 | 动态冲突证据 | C11（2周数据） |
| 混淆对豁免 | R3已处理 | 设计区分不剪 | 恒定 |
