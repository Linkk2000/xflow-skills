# XFlow 能力契约闭环设计

## 1. 目标

本设计将能力契约作为现有 XFlow Issue、TDD、证据和 Git 工作流的上游语义层。它不替换现有流程，而是确保复杂能力在进入 Issue 和实现前，已经回答“系统承诺什么、如何验证、怎样投影到工程”。

完整传导链为：

```text
用户原话
→ 查找现有契约
→ 请求分类
→ 能力声明与人工确认
→ 验证矩阵
→ 工程投影
→ Issue / 依赖 Issue / 本地 subtask
→ TDD 实现
→ 真实运行证据
→ resolution-report
→ 契约演进
```

本轮覆盖：

- Skill 的触发、路由、状态、模板、证据和多 AI 入口。
- devctl 的契约、追溯、任务激活和审批绑定检查。
- 旧项目迁移、Windows 原生执行和 GitHub/Gitee Issue ID 兼容。
- 单元测试、CLI 集成测试、Skill 压力场景和真实任务回放。

本设计不让 devctl 判断业务设计是否合理，也不要求所有小修复创建大型契约。

## 2. 核心原则

1. 先查现有契约，再分类请求。
2. 新能力和行为边界变化必须经过能力契约人工认可。
3. 验证矩阵必须先于工程投影和实现计划。
4. 已有契约被违反时保持契约稳定，进入差距闭环。
5. 纯 UI、错字、明确局部 bug 和运维任务可以走轻量路径。
6. 契约、交互、验证、Issue、测试、证据和结论使用稳定引用形成追溯链。
7. `.xflow/issues/` 默认随仓库管理；忽略该目录是项目显式声明的例外。
8. 一个 worktree 同一时刻只能激活一个远端 Issue；多个 worktree 可以并行开发。
9. 活跃审批文件是本机一次性状态，不进入 Git；执行后的脱敏审核记录随 Issue 保留。
10. AI 可以准备决策和审核材料，但不能替代人工语义决定或审批。

## 3. 分类路由

所有请求先进行轻量分类，不要求所有任务进入完整建模。

| 分类 | 识别条件 | 后续路径 |
|---|---|---|
| `capability-change` | 改变用户可依赖的结果、合法状态、约束、失败或跨实现语义 | 契约声明、人工认可、验证矩阵、工程投影 |
| `implementation-gap` | 现有契约已经明确，但实现没有兑现 | `gap-analysis.md`、人工认可、修复、`resolution-report.md` |
| `ui-defect` | 只影响展示、文案或操作感受，不改变能力语义 | 轻量 Issue；引用已有契约或需求 |
| `infrastructure` | 多个能力、引擎或容器共享的机制问题 | 独立依赖 Issue；声明父能力依赖和集成目标 |
| `governance` | 只改变开发、审核、Git、证据或工具流程 | 治理 Issue，不污染业务契约 |
| `future` | 当前上下文不需要兑现的相邻能力 | `futureCapabilitiesOutOfScope` 或后续任务 |

分类器只给出结构化建议。语义不明确或可能改变当前能力边界时，由人工负责人决定。

### 3.1 轻量路径

轻量路径仍必须记录：

- 用户原始陈述或明确请求。
- 分类、理由和已查找的契约结果。
- 当前 Issue 或需求引用。
- 验收和证据要求。

它不需要创建完整 `contract.yaml`，但不能绕过现有 Issue、TDD、证据和远端写入门禁。

## 4. 双轴状态模型

现有 `S0_REQUEST` 到 `S10_DONE` 继续表示 Issue、分支、实现和 Git 交付状态，避免破坏下游仓库。

新增独立语义状态轴：

```text
none
discovery
classified
declaring
accepted-design
verification-designed
projected
gap-analysis
gap-recognized
```

每个 Issue 的持久状态文件为：

```text
.xflow/issues/issue-<id>/task-state.md
```

至少记录：

```text
Issue
Execution State
Semantic Phase
Classification
Contract
Contract File
Contract Change Required
Branch
Base
Allowed Actions
Forbidden Actions
Human Gate
```

### 4.1 语义退出条件

- `capability-change`：只有相关契约段落与验证场景获得明确人工认可，才能进入 `accepted-design`。
- `accepted-design`：验证矩阵完整后进入 `verification-designed`。
- `verification-designed`：工程权威、派生表示和适配边界明确后进入 `projected`。
- `implementation-gap`：差距、范围、证据和验收获得明确人工认可后进入 `gap-recognized`。
- 轻量分类：分类理由与引用完整后，可以进入现有 Issue 流程。

“能力设计认可”“开始实现”“提交”“推送”“创建 MR”“最终验收”是不同门禁，授权不能跨阶段继承。

## 5. 并行任务与 worktree 绑定

仓库可以同时保留多个未完成任务。持久任务状态随 Issue 管理，本机活跃任务按 worktree 管理：

```text
.xflow/issues/issue-A/task-state.md
.xflow/issues/issue-B/task-state.md
.xflow/local/worktrees/<worktree-id>/active-task.json
```

规则：

- 一个 worktree 同一时刻只能激活一个远端 Issue。
- 独立并行任务使用不同分支和 worktree。
- 在同一 worktree 切换分支后，原活跃指针立即失效，必须重新激活任务。
- 本地 `subtask-*` 不建立独立活跃任务，也不拥有远端审批。
- 父 Issue 与本地 subtask 共用父任务；远端依赖 Issue 使用独立任务和分支。
- 若项目确需父 Issue 与远端子 Issue 共用集成分支，任务状态必须显式记录集成关系，不能隐式复用审批。

每次敏感操作校验以下绑定：

```text
repository identity
+ worktree identity
+ current branch
+ issue ID
+ action
+ approved file path
+ file SHA256
```

任何不一致都失败关闭，不从最近文件、分支名或旧对话猜测当前任务。

## 6. 产物与所有权

### 6.1 长期语义权威

长期进入 Git 的默认能力产物为：

```text
<contract-root>/<capability>/contract.yaml
```

默认 `contract-root` 为 `docs/requirements`，项目可以在 `.xflow/xflow.json` 中覆盖。

`contract.yaml` 负责：

- 能力目的、参与者、输入、输出和核心约束。
- 上下文、角色、交互、语义值和失败原因。
- 验证矩阵、工程投影、依赖、阻塞问题和未来范围。
- 稳定 ID、对象版本和契约状态。

### 6.2 Issue 过程材料

普通项目默认跟踪：

```text
.xflow/issues/issue-<id>/
  classification.yaml
  contract-change-proposal.md
  task-state.md
  gap-analysis.md
  traceability-matrix.yaml
  implementation-plan.md
  evidence/
  subtask-001/
  resolution-report.md
  walkthrough.md
```

职责：

- `classification.yaml`：记录契约查找结果、分类和理由。
- `contract-change-proposal.md`：人工认可前的候选语义变化。
- `traceability-matrix.yaml`：连接契约、验证、Issue、测试、证据和结论。
- `gap-analysis.md`：记录变更前事实、差距、可信度和验收条件。
- `resolution-report.md`：记录变更后证据和 `resolved|reduced|blocked` 结论。
- `evidence/`：保存截图、DOM、运行态模型、API、数据库只读结果、日志和小型夹具。

COS/OSS 仅用于远端 Issue、评论和 PR/MR 正文发布，不能替代仓库内证据。

### 6.3 跨仓语义所有权

- 一个能力契约只有一个语义权威仓库。
- 存在总控仓时，跨仓能力可以由总控仓持有。
- Web、Server 等实现仓只维护工程投影、任务追踪和本仓证据，不复制并独立演化同一契约。
- 没有总控仓时，由能力所有者仓持有契约。
- 外部契约引用包含稳定契约 ID、版本和可定位来源。

## 7. Git 跟踪和审批记录

默认 `.xflow/xflow.json`：

```json
{
  "issueWorkspace": {
    "mode": "tracked"
  },
  "contracts": {
    "root": "docs/requirements"
  }
}
```

默认跟踪：

- `.xflow/issues/**`
- `<contract-root>/**/contract.yaml`

始终忽略：

- `.xflow/local/**`
- `.xflow/runtime/**`
- `.xflow/issues/**/approvals/local-review.md`
- 凭据、Token、Cookie、运行锁和临时缓存。

活跃审批文件包含一次性状态，不进入 Git。远端动作完成后生成：

```text
.xflow/issues/issue-<id>/approvals/history/<timestamp>-<action>.yaml
```

历史记录包含仓库、worktree、分支、Issue、动作、文件哈希、审核身份摘要、执行结果和 `reusable: false`，不能再次满足门禁。

项目可以显式配置 `issueWorkspace.mode: local`，但必须在项目规则中说明原因。工具不能擅自把 tracked 项目切换成 local，也不能擅自修改旧项目 `.gitignore`。

## 8. devctl 命令合同

### 8.1 契约命令

```text
devctl contract lint --file <contract.yaml>
devctl contract diff --old <old.yaml> --new <new.yaml>
devctl trace check --issue <id> --contract <contract.yaml> \
  --matrix .xflow/issues/issue-<id>/traceability-matrix.yaml
```

`contract lint` 检查：

- YAML 结构、必需字段和枚举。
- ID 全局唯一且引用存在。
- 语义版本格式合法。
- 交互包含输入、结果、约束和失败预期。
- 核心约束至少被一个验证场景追踪。
- `current` 上下文没有阻止当前阶段的开放问题。
- `future` 能力没有被当前验证矩阵当成必需结果。

`contract diff` 按稳定 ID 输出新增、删除、修改和版本变化，标记可能改变合法行为集合的字段，并列出需要人工复核的验证和工程投影。工具不自行判定业务兼容性。

`trace check` 检查：

```text
contract → interaction → verification → issue → test → evidence → conclusion
```

引用文件必须存在并位于正确 Issue 工作区；`resolved` 必须有新采集的变更后证据；UI 验证必须同时具有真实页面截图与 DOM 或运行态模型。

### 8.2 分类和任务命令

```text
devctl check classification --issue <id|draft>
devctl task activate --issue <id>
devctl task status
devctl task list
devctl task migrate-current
```

`task activate` 建立 worktree 本机指针，并验证任务状态声明的分支。`task status` 明确输出仓库、worktree、分支、Issue 和语义阶段。`task migrate-current` 将旧 `.xflow/current-task.md` 转换为 Issue 级任务状态，但不删除用户文件。

### 8.3 审批绑定

审批模板增加：

```text
Repository ID
Worktree ID
Branch
Issue
Action
Approved File
Approved SHA256
```

旧审批缺少新绑定字段时不能直接用于新版敏感操作。迁移工具可以重新生成 `Approved: no` 的审批草稿，但不能补造历史批准。

## 9. 机械检查与人工判断边界

工具可以判断：

- 字段、枚举、ID、引用和版本格式。
- 文件位置、证据类型和引用闭合。
- worktree、分支、Issue、动作和审批哈希绑定。
- 验证是否有测试或人工步骤。
- `resolved` 是否存在变更后证据。

工具不能判断：

- 能力目的是否真正表达用户价值。
- 某项约束或失败语义是否合理。
- 契约版本变化是否在业务上兼容。
- 截图是否真正证明体验良好。
- 跨仓语义所有者和基础设施拆分是否合理。
- 用户是否已经认可能力设计。

因此，机械检查只能 fail fast，不能替代人工评审。

## 10. 多 AI 入口

通用语义存放在项目本地 Skill references。`AGENTS.md`、`.cursorrules`、Cursor MDC、`CLAUDE.md` 和 `GEMINI.md` 只包含短硬规则和 Skill 路径，避免复制整套方法后漂移。

所有入口必须包含：

1. 先查现有契约再分类。
2. 能力变化未经人工认可不得实现。
3. 验证矩阵先于工程投影。
4. `.xflow/issues/` 默认随仓库管理。
5. 一个 worktree 只能激活一个远端 Issue。
6. AI 不得满足人工门禁。

主 Skill 按阶段加载 references，不在每轮载入完整方法、全部证据和所有 Git 规则。

## 11. 兼容与迁移

### 11.1 旧单例任务状态

- 没有 Issue 级状态时，可以只读解析 `.xflow/current-task.md`。
- 第一次显式迁移后生成 `issue-<id>/task-state.md` 和本机活跃指针。
- 迁移后旧文件只用于兼容提示，不再参与审批判断。
- 不静默猜测 Issue、分支或审批归属。

### 11.2 被忽略的 Issue 工作区

- 工具报告 `.xflow/issues/` 当前是否被 Git 忽略。
- 不擅自删除 `.gitignore` 规则或执行 `git add`。
- 迁移前检查凭据、活跃审批、大文件和本地绝对路径。
- 用户确认后才将安全的过程材料和证据纳入 Git。
- 特殊仓库可保持 `mode: local`。

### 11.3 平台与依赖

- Windows 使用 Python core 和 `devctl.ps1`，不引入 WSL 调用链。
- YAML 使用当前 devctl 已声明的 PyYAML 依赖和 `safe_load`。
- GitHub 数字 Issue 和 Gitee 字符 Issue 使用同一结构规则。
- 所有命令在 `help.txt` 和 README 中提供可直接照抄的完整示例。

## 12. 失败策略

### 12.1 硬失败

- 能力变化未获人工认可就进入实现。
- 验证矩阵为空但已经存在工程投影。
- 稳定 ID 重复或引用断裂。
- worktree、分支、Issue 或审批绑定不一致。
- `resolved` 缺少直接变更后证据。
- UI 证据把独立测试页声明为真实产品页。
- 从 A 的审批文件执行 B 的动作。

### 12.2 警告并要求人工判断

- 契约版本提升是否足以表达语义变化。
- 某问题属于共享基础设施还是父功能。
- 证据是否真正支持体验或业务结论。
- 跨仓能力的语义所有者是否正确。

### 12.3 允许轻量继续

- 纯样式、错字和明确局部 bug。
- 已有契约或需求足以限定行为。
- 分类理由、任务引用和验收已经记录。

## 13. 验证策略

### 13.1 结构单元测试

- 合法和非法契约 YAML。
- 重复 ID、断裂引用、非法版本和未覆盖约束。
- 开放阻塞问题和 future/current 混用。
- 分类、任务绑定、审批隔离和追溯矩阵。

### 13.2 CLI 集成测试

- Windows 原生入口。
- GitHub 与 Gitee Issue ID。
- A、B 两个 worktree 并行激活。
- 分支切换使旧状态失效。
- A 的审批不能用于 B。
- 旧任务状态迁移。
- tracked/local 两种 Issue 工作区模式。

### 13.3 Skill 压力场景

- 新能力先形成契约和验证矩阵。
- 已有契约 bug 保持契约稳定并进入差距闭环。
- 纯 UI 不创建大型 YAML。
- 共享基础设施提出依赖 Issue。
- 未来能力进入 out-of-scope。
- 模糊“可以/继续”不能跨越语义或远端门禁。
- 独立测试页截图不能冒充真实产品证据。
- 自动测试通过但真实运行证据冲突时，结论必须降级。

### 13.4 真实任务回放

回放折叠子流程、Call Activity、同包部署、父子 Issue、跨仓投影、错误证据和并行任务场景，检查 Skill 是否在正确阶段暂停并要求人工决定。

## 14. 分阶段实施

### 第一阶段：Skill 路由与 tracked Issue 工作区

- 增加能力契约 references、分类规则和主入口硬门槛。
- 修改 Issue 工作区默认跟踪规则及多 AI 模板。
- 安装契约、分类、追溯和任务状态模板。

### 第二阶段：任务状态与审批隔离

- 实现 Issue 级任务状态和 worktree 活跃指针。
- 实现 activate/status/list/migrate。
- 扩展审批绑定和不可复用历史记录。

### 第三阶段：契约与追溯检查器

- 实现 contract lint、contract diff、classification check 和 trace check。
- 增加结构、引用、版本、证据和跨路径安全测试。

### 第四阶段：压力测试与真实回放

- 运行无新规则基线场景。
- 运行带 Skill 场景并记录新绕过方式。
- 回放真实任务，修复误触发、漏触发和上下文成本问题。

每一阶段都必须保持现有 Issue、GitHub/Gitee、附件、subtask、差距闭环和无人值守测试通过。

## 15. 完成定义

- Skill 能先查契约再稳定分类。
- 新能力不能在未认可时进入实现。
- 验证矩阵先于工程投影。
- 普通小 bug 不被迫创建大型契约。
- `.xflow/issues/` 默认随仓库管理，敏感本机状态保持忽略。
- 多 worktree 并行时任务状态和审批不串线。
- 契约、验证、Issue、测试、证据和结论可以机械追溯。
- devctl 只执行机械检查，不冒充语义审核。
- Codex、Cursor、Claude Code 和 Gemini 入口表达同一组硬规则。
- 压力场景与真实任务回放均通过，且没有破坏现有工作流。
