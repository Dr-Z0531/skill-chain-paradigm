# 验证信号

## 核心原则

**LLM 不能验证自己的产出。**

推理：验证的本质是"独立判定"。如果判定者与执行者是同一个模型、同一套逻辑，那么"通过"只证明模型认为自己对——不证明产出真的对。logical-verification paper 的实证（78→98%）：加一个独立逻辑层判定，精度大幅提升。验证必须落在确定性层：文件存在+解析、状态+输出、显式用户确认。

## 信号模型（三选一）

| 信号 | 定义 | 确定性判定 |
|:---|:---|:---|
| `task_completion` | 任务产出了定义好的结果 | status == ok AND outputs 非空 |
| `user_feedback` | 用户显式确认 | 确认引用存在且为 true |
| `artifact_exists` | 交付物存在且有效 | 文件存在 + schema/JSON 解析 |

**为什么三选一**：每个信号都有确定性判定方式——"任务完成"不是感觉是产物+状态，"用户反馈"不是猜测是显式确认，"产物存在"不是声称是文件+校验。确定性 = 可复现 = 可审计。

## 失败处理

| 失败 | 处理 |
|:---|:---|
| 回验失败 | 标记 `suspected_mistake` → 路由表迭代 |
| 链执行失败 | 幂等重试 1 次 → 重新路由 → 连续 2 次失败暂停该事件类型（人工介入） |
| 重试通过但无诊断 | 不算修复——"重试过了"不是"找到原因了" |

## 反模式（禁止）

- 输出当预测分数（验证变成评分）；
- 纯盾牌验证（只检查终止路径）；
- 生成失败静默丢弃导致 NA 偏倚；
- 贪婪解码不可复现。

---

## 算法规格（Algorithm Spec·三信号可执行定义）

### 信号判定

| 信号 | 判定逻辑 | pass条件 |
|:---|:---|:---|
| task_completion | 产物路径存在 + JSON可解析 + 状态字段非空 | 全过 |
| user_feedback | 反馈文本非空 + 非否定前缀（"否"/"不行"开头） | 肯定反馈 |
| artifact_exists | 文件存在 + validator回调通过（json.load等） | 全过 |

### 伪代码

```
verify_artifact_exists(path, validator=None):
  if not os.path.exists(path): return {value: False, evidence: "文件不存在"}
  if validator:
    try: validator(path); return {value: True}   # 结构校验通过
    except: return {value: False, evidence: err}
  return {value: True}

mark_route_quality(chain_id, quality):            # 回验写回router_log
  for entry in router_log:
    if entry.chain.chain_id == chain_id:
      entry.verification = {signal: "回验", value: quality == "good"}
      entry.route_quality = quality
  # fail→route_quality=suspected_mistake→特征表迭代（连续进化）
```
