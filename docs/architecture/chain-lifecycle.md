# 链生命周期

## 链是什么（机制层面）

链 = 有序技能序列 `C = [S1..Sn]`，`n ≥ 1`。它是唯一工作单元——技能不被直接调用，事件必须通过链执行。

**一个链实例长这样**（JSON）：

```json
{
  "chain_id": "chain-9f3a2b1c-1",
  "event_fingerprint": "9f3a2b1c",
  "skills": [
    {"skill_id": "strategic", "role": "main"},
    {"skill_id": "orchestration", "role": "support"},
    {"skill_id": "verification", "role": "verify"}
  ],
  "length": 3,
  "execution_mode": "sequential"
}
```

## 生成流程

```
事件 → 特征提取 → 锚点匹配（R1-R4）→ 候选排序
     → 主技能（首候选）→ 支持技能（相关候选）→ 链组装（长度≥1）→ chain_id
```

**链长度由什么决定**（公理4）：事件复杂度 × 可用技能集 × 历史效果。

- 简单事件 → 单技能链（n=1）；
- 复杂事件 → 多技能链（n=2-4）；
- 修剪收缩可用集 → 链长度下降。

## 执行模式

| 模式 | 语义 | 示例 |
|:---|:---|:---|
| `sequential` | 顺序执行·前步输出喂后步 | 委派链：strategic → orchestration → verification → eval |
| `parallel` | 独立技能并行 | 同一产物的 verification + eval 并行 |
| `hybrid` | 段内并行·段间顺序 | 蒸馏流水线 |

## 收敛与缓存

同事件链连续 3 次相同 → 收敛 → 入链库缓存（重放不重路由）。漂移（序列/长度变化）→ 触发路由表迭代。

**为什么收敛判据是 3 次**：1 次是偶然，2 次是巧合，3 次是模式。首版保守值，2 周后按分布校准。

## 版本联动

技能携带 `dependent_chains` 列表。技能被 patch → 依赖链失效 → 下次使用重路由。每周全量版本核对覆盖老技能。

**为什么**：链缓存引用的是技能的旧版本——技能更新后链还是旧逻辑，等于用过期方法论。版本失效让链永远追得上技能。

## 回收（防链库膨胀）

低频链（30 天未用 + 效果率低）→ 归档。**链库不能成为第二个技能库**——缓存必须回收，否则膨胀从技能转移到链。

---

## 算法规格（Algorithm Spec·链生命周期可执行定义）

### add_chain(chain) 伪代码

```
fp = fingerprint(chain)   # "skill1+skill2|len2"（技能序列+长度）
if store.chains contains fp:
  found.count += 1; found.last_seen = now
  found.converged = (found.count >= 3)          # 收敛阈值: 3次稳定
else:
  store.chains.append({fingerprint, skills, length, mode,
                       count: 1, converged: False, version_valid: True,
                       skill_versions: {s: "v1"}})   # 技能版本快照
save_store(store)
```

### invalidate_on_patch(skill_name)

```
for c in store.chains:
  if skill_name in c.skills:
    c.version_valid = False                     # 技能patch→依赖链失效
    c.invalidated_at = now
```

### recycle(threshold=1)

```
for c in store.chains:
  if c.count <= 1 and not c.archived:          # 低频（≤1次）
    c.archived = True; c.archived_at = now     # 归档≠删除·可恢复
```

### present(limit=1)

```
valid = [c for c in chains if c.converged and c.version_valid and not c.archived]
sort by count desc; return valid[:limit]        # 1条链·ctx渐进披露
```
