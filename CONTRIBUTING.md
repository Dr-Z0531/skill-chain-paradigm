# 参与贡献（Contributing to Skills Chain Framework）

本项目遵循轻量、以证据为基础的贡献流程。所有社区成员须遵守 [行为准则（CODE_OF_CONDUCT.md）](CODE_OF_CONDUCT.md)。

## 目录

- [贡献清单（所有 PR 必填）](#贡献清单所有-pr-必填)
- [开发环境](#开发环境)
- [PR 流程](#pr-流程)
- [代码风格](#代码风格)
- [如何提交一个好的 Issue](#如何提交一个好的-issue)
- [问题咨询](#问题咨询)

## 贡献清单（所有 PR 必填）

- [ ] **单 PR 单变更。** 小 diff 审查更快、回滚更干净。
- [ ] **与设计文档对齐。** 新机制必须追溯到规范性说明（`docs/architecture/`）。规范未覆盖的，应在同一 PR 中提出规范变更。
- [ ] **行为测试先行。** 每个新机制附带一个测试：变更前失败、变更后通过。
- [ ] **无魔法数字。** 新阈值必须附带校准依据（数据来源/窗口/样本量）。未校准的阈值不得作为决策逻辑。
- [ ] **确定性验证。** 宣称由 `pytest` 支撑，而非自述"可以运行"。
- [ ] **文档同步更新。** README / docs 保持单一事实源。

## 开发环境

```bash
git clone <repo>
cd skills-chain-framework
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## PR 流程

1. Fork 仓库，创建分支（`feat/...`、`fix/...`）。
2. 使用约定式提交信息（`feat:`、`fix:`、`docs:`、`test:`、`refactor:`）。
3. 提交 PR 并勾选上方清单。
4. CI 必须通过（3.10–3.12 · Ubuntu + Windows 的 lint + 测试）。
5. 评审：至少一位维护者批准；修改意见在后续提交中解决（评审期间禁止 force-push 压缩）。

## 代码风格

- PEP 8，`black` 格式化，`ruff` 检查。
- 所有公开函数带类型标注。
- Docstring：一行摘要 + 非平凡逻辑的 Args/Returns。

## 如何提交一个好的 Issue

好的 Issue 节省所有人的时间。请包含：

**Bug 类：**

- 框架版本与 Python 版本
- 操作系统与环境（venv、pip、CI）
- 完整错误日志（不是摘要）
- 最小复现：步骤、代码、配置
- 期望行为 vs 实际行为

**功能类：**

- 问题与证据（观察到的行为、日志、数据）
- 提议机制，并引用规范性说明（`docs/architecture/`）
- 若引入新阈值：数据来源、窗口、校准计划
- 验收标准（如何验证有效）

使用 Issue 模板：[bug report](.github/ISSUE_TEMPLATE/bug_report.md) · [feature request](.github/ISSUE_TEMPLATE/feature_request.md)

## 问题咨询

在 Issues 中发起讨论。安全问题请使用 [SECURITY.md](SECURITY.md)（勿公开发 issue）。
