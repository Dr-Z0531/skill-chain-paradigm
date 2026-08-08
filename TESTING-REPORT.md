# 测试报告（TESTING-REPORT）

**项目**: skill-chain-paradigm v0.2.0
**日期**: 2026-08-08
**执行者**: 自动化验证（真实执行·非纸面）

## 1. 执行环境

```
工作目录: skill-chain-paradigm/
配置: pyproject.toml（testpaths=tests）
```

## 2. 执行命令

```bash
python -m pytest tests/ -v --no-header
```

## 3. 结果总览

```
============================= 18 passed in 0.32s ==============================
退出码: 0（全部通过）
```

## 4. 覆盖矩阵（18 项测试·4 个模块·真实清单）

| 模块 | 测试 | 覆盖行为 | 状态 |
|:---|:---|:---|:---|
| test_generator.py | test_positive_routes | R1 正例路由（6 核心案例·深度锚点） | ✅ PASS |
| test_generator.py | test_negative_no_route | 负例（通用编码请求零路由） | ✅ PASS |
| test_generator.py | test_all_cases_regression | 13 案例回归（含长尾降级语义） | ✅ PASS |
| test_verifier.py | test_artifact_exists_pass | 验证信号: 产物存在 | ✅ PASS |
| test_verifier.py | test_artifact_exists_fail | 验证信号: 产物缺失→失败 | ✅ PASS |
| test_verifier.py | test_user_feedback_pass | 验证信号: 显式反馈确认 | ✅ PASS |
| test_verifier.py | test_user_feedback_reject | 验证信号: 反馈拒绝 | ✅ PASS |
| test_verifier.py | test_user_feedback_empty | 验证信号: 空反馈→失败 | ✅ PASS |
| test_verifier.py | test_task_completion_json | 验证信号: JSON 任务完成判定 | ✅ PASS |
| test_pruner.py | test_structural_overlap_detects_40pct | 结构深度: 锚点交集≥40% 判重叠 | ✅ PASS |
| test_pruner.py | test_structural_overlap_below_threshold | 结构深度: <40% 不判重叠 | ✅ PASS |
| test_pruner.py | test_prune_excludes_confusion_pairs | R3 混淆对排除（设计区分不剪） | ✅ PASS |
| test_pruner.py | test_prune_dry_run_records_ledger | dry_run 台账记录·状态不迁移 | ✅ PASS |
| test_chain_store.py | test_converge_after_3_identical | 链库收敛: 同指纹 3 次 | ✅ PASS |
| test_chain_store.py | test_diff_fingerprint_not_converged | 链库: 不同指纹独立计数 | ✅ PASS |
| test_chain_store.py | test_patch_invalidates_dependent_chains | 版本联动: 技能 patch→链失效 | ✅ PASS |
| test_chain_store.py | test_recycle_low_frequency_archives | 低频链归档（不删除·可恢复） | ✅ PASS |
| test_chain_store.py | test_present_prefers_converged_valid | 呈现: 收敛+有效+未归档优先 | ✅ PASS |

## 5. 示例验证（端到端）

```bash
python examples/single_skill_chain.py
# → 单技能链生成（length=1·note=统一协议）
# → verification: {'pass': True, 'evidence': 'artifact exists + JSON valid'}
```

## 6. 覆盖率说明

- 当前为单元级+端到端示例验证；行覆盖率统计（coverage.py）计划后续引入。
- CI（.github/workflows/ci.yml）在每次 push 时运行 3.10–3.12 × Ubuntu+Windows 全矩阵。

## 7. 复现

```bash
git clone <repo> && cd skill-chain-paradigm
pip install -e ".[dev]"
pytest tests/ -v
```

---

*本报告由自动化验证生成·数据真实可复现。*

## 0.3.0 新增测试（2026-08-08）

- **test_confusion_pairs.py**: 4项（加载/无反身/无重复/rule齐备）
- 全量: **22/22 passed in 0.27s**（18旧+4新·pytest实跑）
- 稳定性判据: 路由盲测7/7（整合后回归·integration regression run实证）

## 0.3.0 终检（2026-08-08 深夜·全量审查后）

- 混淆词对: **13对**（本地state全量同步·无自反/重复·字段齐）
- 泄露终扫: 零命中（28份md全量核查）
- 测试: 22/22 passed
- 校验: SHA256SUMS（词对13对后）·文档同步后SHA256SUMS
- 文档一致性: 6份脱节文档已同步（CHANGELOG/README/TESTING-REPORT中英）
