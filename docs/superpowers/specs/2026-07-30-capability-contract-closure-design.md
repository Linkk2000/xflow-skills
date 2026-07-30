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

## 4. 能力契约编写协议

机械结构不能替代语义质量。Skill 必须指导 AI 先回答能力问题，再填写 YAML，禁止打开模板后逐字段编造内容。

### 4.1 编写前的自然语言发现

在创建或修改契约前，AI 依次确认：

1. 谁依赖这项能力？
2. 参与者获得的核心价值是什么？
3. 能力在哪个上下文中生效？
4. 当前接受哪些业务意图、对象和必要前态？
5. 成功后产生什么可观察、可依赖的结果？
6. 哪些事实在任何合法路径中都不能被破坏？
7. 什么情况下必须拒绝，拒绝时必须保留什么状态？
8. 哪些相邻能力明确不属于当前承诺？
9. 哪些问题尚未收敛，并会阻止当前设计继续？
10. 什么证据足以让独立审核者判断能力已经兑现？

Discovery 对话规则：

- 保留用户原始陈述，不先翻译成接口、表结构或组件任务。
- 一次只确认一个会改变能力边界的问题。
- 对关键取舍给出 2-3 个方案、推荐理由和保护的不变量。
- 每轮区分已确认、待确认和不影响当前合法性的判断。
- 关键语义未获明确认可前，不编辑实现代码，也不把候选结论写成正式契约状态。

### 4.2 契约编写顺序

正式写入或更新 `contract.yaml` 时按以下顺序，而不是按模板从上到下机械填表：

1. `purpose`：写参与者价值和明确边界，不写技术手段。
2. 合法状态与核心 `constraints`：每条规则可以判定真假。
3. `context`：入口条件、完成条件和当前承担的责任。
4. `contextRoles`：每个角色的责任与 `doesNotOwn`。
5. `interactionContracts`：当前必须兑现的业务意图。
6. 成功与失败：为每个交互补齐 `accepts`、`produces`、`constraints` 和 `failureExpectations`。
7. `semanticValueContracts` 与 `failureReasonContracts`：提取跨层共享的稳定含义和失败代码。
8. `verificationMatrix`：先把承诺写成 Given/When/Then 可观察场景。
9. `engineeringProjections`：再说明前端、后端、协议、存储、引擎和版本如何承接语义。
10. `dependsOn`、`preconditionsToResolve`、`futureCapabilitiesOutOfScope` 和 `references`。

验证矩阵为空时不得进入工程投影。工程投影不得反向增加未经人工认可的能力语义。

### 4.3 推荐结构和字段职责

```yaml
id: example.contract.capability-name
version: 0.1.0
name: 能力名称
status: draft | accepted-design | active | deprecated
created: YYYY-MM-DD
note: 非规范性背景

capabilityContract: {}
semanticValueContracts: []
failureReasonContracts: []
context: {}
contextRoles: []
interactionContracts: []
engineeringProjections: []
verificationMatrix: []
dependsOn: []
preconditionsToResolve: []
futureCapabilitiesOutOfScope: []
references: []
```

字段规则：

- `purpose` 描述系统持续承担的价值，不写“增加组件”“新增接口”或具体框架。
- `inputs` 与 `outputs` 描述业务对象、意图和可观察结果，不等同于函数参数和 DTO。
- `constraints` 写可以判定真假的不变量，不使用“合理”“友好”“尽量”等模糊词。
- `failureExpectations` 写拒绝原因、稳定失败含义和失败后保留状态，不只写“显示错误”。
- `doesNotOwn` 防止角色或模块不断吸收相邻职责。
- `engineeringProjections` 明确权威表示、派生表示、转换边界和替换技术时必须保持的不变量，不列逐文件实现步骤。
- `preconditionsToResolve` 保存会影响当前设计合法性的未决问题；`note` 只能保存非阻塞背景。
- `futureCapabilitiesOutOfScope` 明确为什么当前不承诺，且不能进入当前验证矩阵。

简单能力允许保留不适用的空数组，但不得省略决定当前合法状态、失败和验收的内容。

### 4.4 稳定 ID

推荐格式：

```text
<namespace>.<artifact-type>.<domain-or-context>.<specific-name>
```

示例：

```text
xflow.contract.process-ui-responsibility-partition
xflow.capability.process-responsibility-partition
xflow.interaction.reassign-flow-node
xflow.constraint.node-membership
xflow.failure-reason.lane_not_empty
xflow.verify.case.cross-lane-reassignment
```

规则：

- 使用小写英文、数字、点和连字符。
- ID 表达稳定语义，不包含日期、Issue、分支、组件、数据库或框架名称。
- 标题和文案可以修改，外部引用后的 ID 不因措辞优化而变化。
- 语义上替换原对象时保留 `supersedes` 或迁移说明，不静默复用或删除旧 ID。
- 验证 ID 描述行为场景，不描述测试文件名。

### 4.5 契约对象版本

根契约和可被引用的子对象都拥有语义版本：

- `PATCH`：澄清措辞或注释，不改变合法行为集合。
- `MINOR`：向后兼容地新增可选输入、交互、验证或语义。
- `MAJOR`：改变既有参与者可依赖的行为、合法状态、约束或失败语义。

版本变更必须说明：

- 哪些稳定 ID 发生变化。
- 合法行为集合是否改变。
- 旧实现是否仍满足新契约。
- 是否需要数据迁移或兼容策略。

`contract diff` 只能标记可能需要升级的对象，最终版本判断由人工审核。

### 4.6 最小交互示例

```yaml
interactionContracts:
  - id: example.interaction.delete-lane
    version: 0.1.0
    context: example.context.process-design.partition
    participants:
      - example.role.process-designer
    accepts:
      - 删除目标泳道的业务意图
      - 当前可编辑流程定义
    produces:
      - 空泳道被删除且其他结构保持有效
    constraints:
      - 含有流程节点的泳道不得删除
    failureExpectations:
      - 引用 example.failure-reason.lane_not_empty
      - 拒绝后泳道、节点、边和责任归属全部保持不变

verificationMatrix:
  - id: example.verify.case.reject-populated-lane-deletion
    version: 0.1.0
    traces:
      - example.interaction.delete-lane
    given: 目标泳道仍包含流程节点
    when: 设计者请求删除目标泳道
    then: 操作被拒绝，返回稳定原因，全部结构和归属保持不变
    verifyBy:
      - automated
      - ui
```

这个示例强调失败保持与可观察验证，不规定按钮、Toast 样式或具体实现函数。

### 4.7 人工认可和重新打开

- `draft` 不能作为实现门槛。
- 人工明确认可具体契约段落和验证场景后，状态才能进入 `accepted-design`。
- “可以”“继续”“你看着办”不自动表示契约认可。
- 认可记录绑定契约 ID、版本、文件哈希和被认可的段落或对象 ID。
- 实现中发现新约束时，先分类；若改变用户可依赖承诺，暂停实现并重新打开契约门禁。
- `active` 表示已有正式实现和验证基线，不等于未来无需演进。

### 4.8 常见反模式

- 框架能力反向定义契约，例如把 `parentNode` 当成责任归属本身。
- 只写成功路径，不写拒绝原因和失败后保持状态。
- 把 UI 样式、文件名、事件名和数据库字段塞进顶层能力。
- 用 `note` 隐藏会改变当前合法性的未决问题。
- 因为测试难写而缩小已经确认的能力责任。
- 每个 bug 都修改契约，使契约退化为问题日志。
- 为了通过 Schema 填写无法验证的空泛句子。

Skill 实施时应新增并按阶段加载：

```text
references/capability-contract-method.md
references/contract-authoring.md
references/contract-evolution.md
templates/capability-contract.yaml
schemas/capability-contract.schema.json
```

`contract-authoring.md` 负责本节的操作规则；模板和 Schema 只负责产物形状，不能替代编写方法。

## 5. 双轴状态模型

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

## 6. 并行任务与 worktree 绑定

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

## 7. 产物与所有权

### 7.1 长期语义权威

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

### 7.2 Issue 过程材料

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

### 7.3 跨仓语义所有权

- 一个能力契约只有一个语义权威仓库。
- 存在总控仓时，跨仓能力可以由总控仓持有。
- Web、Server 等实现仓只维护工程投影、任务追踪和本仓证据，不复制并独立演化同一契约。
- 没有总控仓时，由能力所有者仓持有契约。
- 外部契约引用包含稳定契约 ID、版本和可定位来源。

## 8. Git 跟踪和审批记录

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

## 9. devctl 命令合同

### 9.1 契约命令

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

### 9.2 分类和任务命令

```text
devctl check classification --issue <id|draft>
devctl task activate --issue <id>
devctl task status
devctl task list
devctl task migrate-current
```

`task activate` 建立 worktree 本机指针，并验证任务状态声明的分支。`task status` 明确输出仓库、worktree、分支、Issue 和语义阶段。`task migrate-current` 将旧 `.xflow/current-task.md` 转换为 Issue 级任务状态，但不删除用户文件。

### 9.3 审批绑定

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

## 10. 机械检查与人工判断边界

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

## 11. 多 AI 入口

通用语义存放在项目本地 Skill references。`AGENTS.md`、`.cursorrules`、Cursor MDC、`CLAUDE.md` 和 `GEMINI.md` 只包含短硬规则和 Skill 路径，避免复制整套方法后漂移。

所有入口必须包含：

1. 先查现有契约再分类。
2. 能力变化未经人工认可不得实现。
3. 验证矩阵先于工程投影。
4. `.xflow/issues/` 默认随仓库管理。
5. 一个 worktree 只能激活一个远端 Issue。
6. AI 不得满足人工门禁。

主 Skill 按阶段加载 references，不在每轮载入完整方法、全部证据和所有 Git 规则。

## 12. 兼容与迁移

### 12.1 旧单例任务状态

- 没有 Issue 级状态时，可以只读解析 `.xflow/current-task.md`。
- 第一次显式迁移后生成 `issue-<id>/task-state.md` 和本机活跃指针。
- 迁移后旧文件只用于兼容提示，不再参与审批判断。
- 不静默猜测 Issue、分支或审批归属。

### 12.2 被忽略的 Issue 工作区

- 工具报告 `.xflow/issues/` 当前是否被 Git 忽略。
- 不擅自删除 `.gitignore` 规则或执行 `git add`。
- 迁移前检查凭据、活跃审批、大文件和本地绝对路径。
- 用户确认后才将安全的过程材料和证据纳入 Git。
- 特殊仓库可保持 `mode: local`。

### 12.3 平台与依赖

- Windows 使用 Python core 和 `devctl.ps1`，不引入 WSL 调用链。
- YAML 使用当前 devctl 已声明的 PyYAML 依赖和 `safe_load`。
- GitHub 数字 Issue 和 Gitee 字符 Issue 使用同一结构规则。
- 所有命令在 `help.txt` 和 README 中提供可直接照抄的完整示例。

## 13. 失败策略

### 13.1 硬失败

- 能力变化未获人工认可就进入实现。
- 验证矩阵为空但已经存在工程投影。
- 稳定 ID 重复或引用断裂。
- worktree、分支、Issue 或审批绑定不一致。
- `resolved` 缺少直接变更后证据。
- UI 证据把独立测试页声明为真实产品页。
- 从 A 的审批文件执行 B 的动作。

### 13.2 警告并要求人工判断

- 契约版本提升是否足以表达语义变化。
- 某问题属于共享基础设施还是父功能。
- 证据是否真正支持体验或业务结论。
- 跨仓能力的语义所有者是否正确。

### 13.3 允许轻量继续

- 纯样式、错字和明确局部 bug。
- 已有契约或需求足以限定行为。
- 分类理由、任务引用和验收已经记录。

## 14. 验证策略

### 14.1 结构单元测试

- 合法和非法契约 YAML。
- 重复 ID、断裂引用、非法版本和未覆盖约束。
- 开放阻塞问题和 future/current 混用。
- 分类、任务绑定、审批隔离和追溯矩阵。

### 14.2 CLI 集成测试

- Windows 原生入口。
- GitHub 与 Gitee Issue ID。
- A、B 两个 worktree 并行激活。
- 分支切换使旧状态失效。
- A 的审批不能用于 B。
- 旧任务状态迁移。
- tracked/local 两种 Issue 工作区模式。

### 14.3 Skill 压力场景

- 新能力先形成契约和验证矩阵。
- 已有契约 bug 保持契约稳定并进入差距闭环。
- 纯 UI 不创建大型 YAML。
- 共享基础设施提出依赖 Issue。
- 未来能力进入 out-of-scope。
- 模糊“可以/继续”不能跨越语义或远端门禁。
- 独立测试页截图不能冒充真实产品证据。
- 自动测试通过但真实运行证据冲突时，结论必须降级。

### 14.4 真实任务回放

回放折叠子流程、Call Activity、同包部署、父子 Issue、跨仓投影、错误证据和并行任务场景，检查 Skill 是否在正确阶段暂停并要求人工决定。

## 15. 分阶段实施

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

## 16. 完成定义

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
