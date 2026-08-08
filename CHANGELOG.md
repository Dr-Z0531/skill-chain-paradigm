# 变更日志

本项目所有重要变更记录于此，遵循 [Keep a Changelog](https://keepachangelog.com/) 与 [语义化版本](https://semver.org/)。


## [0.3.0] - 2026-08-08

### 新增（0.3.0）

- **混淆词对库**（`src/data/confusion_pairs.json`·10对·机器可读·防路由幻觉R3强化）
- **稳定性协议**（`docs/architecture/stability.md`·修剪回滚快照/阈值校准/SoT注入）
- **阈值校准协议**（拒绝魔法数·全参数可校准·router_log≥30条触发首校）

### 验证（0.3.0）

- 混淆词对: 10/10机器可读校验通过
- 稳定性判据定义: 路由盲测7/7 · 回滚≤20% · 校准2周内

[0.3.0]: https://github.com/Dr-Z0531/skill-chain-paradigm/releases/tag/0.3.0


### 修复与同步（0.3.0·2026-08-08 深夜·full-package review driven）

- **代码同步**: 4文件以本地运行版为基线（misroute≥2词修正/验证必加length=2/deep-review复杂支持/SKILL_CHAIN_SKILLS_ROOT环境变量）·发布适配（src/data相对路径）
- **泄露修复**: 内部词→通用表述（人名/工具名/路径）·终扫零命中
- **数据同步**: 混淆词对全量13对（本地state为权威·映射表提取）
- **校验**: SHA256SUMS（同步后）→SHA256SUMS（词对13对后）→SHA256SUMS（文档同步后）·每次变更必重签
- **验证**: 22/22测试 · 泄露零命中 · 全量文档-实现一致性核验

## [0.2.0] - 2026-08-08

### 新增（v0.2.0 开源候选版）

- **src/ 标准包布局**: router（深度锚点路由+链生成）· verifier（三信号回验）· pruner（双信号修剪）· store（链库收敛）· data（路由规则/测试案例）
- **tests/ pytest 套件**: 路由 13 案例回归（正例/负例/长尾/混淆区分）· 验证三信号分支 · 修剪重叠检测 · 链库收敛
- **examples/**: 委派链 · 单技能链 · 技能索引示例
- **docs/**: LOGO + 4 张 SVG 架构图（四层架构/闭环/状态机/生态）+ 架构与入门双语文档
- **规范文件**: LICENSE（MIT·the maintainers）· CODE_OF_CONDUCT · CONTRIBUTING · SECURITY（双语）
- **README 双语**: 完整目录 15 节 + 关联链接 + shields 徽章 + 渐进升级路径

### 修复

- 组件路径适配 src/data 相对引用 · 长尾索引环境变量化（SKILL_CHAIN_SKILLS_ROOT）· 硬编码路径零残留
- 版权持有者统一: the maintainers（MIT 合规）

## [0.1.0] - 2026-08-07
## [未发布]

### 新增（v0.1.0 设计里程碑）

- **核心理论**：技能即原子 · 链是唯一工作单元 · 五条公理
- **路由协议 R1–R4**：深度锚点匹配 · 边界排除 · 混淆对区分 · 结果信号回验
- **动态修剪设计**：双信号（静态锚点重叠 + 动态共触发）· 休眠态 · 完全可逆
- **链 JSON schema v1** 与调用协议（事件 → 路由 → 生成 → 执行 → 验证 → 记录）
- **验证信号模型**（任务完成 / 用户反馈 / 产物存在 · 确定性三选一）
- **参考实现骨架**：`src/router` · `src/pruner` · `src/store` · `src/verifier`
- **测试套件**：13 项测试全通过（路由 5 · 修剪 4 · 验证 4）
- **测试报告**：TESTING-REPORT.md（中文）/ TESTING-REPORT-EN.md（英文）
- **文档体系**：README 中英双语 · docs 架构五篇中英双语 · 贡献指南 · 安全政策 · 行为准则

### 计划（v0.2.0）

- router_log 数据管道与阈值校准工具
- 链聚类（共触发矩阵 → 新链发现）
- 长尾配额机制（每周轮换探测）
- 链可视化仪表盘
