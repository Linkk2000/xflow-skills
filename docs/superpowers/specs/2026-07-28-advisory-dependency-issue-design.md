# XFlow 建议性依赖 Issue 工作流设计

## 1. 目标

当主 Issue 在开发、实现或测试期间发现新的依赖工作时，XFlow 应帮助开发人员建立清晰的所有权、依赖关系、集成路径和证据闭环，但不得把依赖关系机械升级为硬性停工门禁。

本设计需要同时支持：

- 主功能分支直接承载主 Issue 范围内的开发。
- 主能力内部、具有独立交付边界的子功能 Issue。
- 可被多个功能复用的共享基础能力 Issue。
- 位于其他仓库、服务或组织边界之外的外部依赖。
- GitHub 数字 Issue 编号和 Gitee 字母数字 Issue 编号。

## 2. 非目标

- 不要求主功能的每个组成部分都创建子 Issue。
- 不根据未完成依赖自动禁止开发、提交或测试。
- 不让 devctl 判断业务依赖是否真正阻塞。
- 不允许 AI 自行批准创建远端依赖 Issue。
- 不用依赖 Issue 自身的测试替代主 Issue 的集成证据。

## 3. 依赖分类

开发中发现新工作时，先判断是否需要独立 Issue。

### 3.1 主 Issue 直接范围

符合以下条件时继续在主功能分支开发，不创建依赖 Issue：

- 已属于主 Issue 确认的能力和验收范围。
- 没有独立交付价值或独立所有权。
- 不需要单独的分支、审核和解决报告。

### 3.2 `child-feature`

主能力内部的子功能，具有独立范围、测试和交付边界，但通常不能脱离主能力单独交付。它从主功能分支建立依赖分支，完成后合回主功能分支。

### 3.3 `shared-infrastructure`

可被多个能力、模块或引擎复用的基础机制。它从目标主干建立独立分支，独立完成并优先合入主干；主功能随后同步主干并完成联合验证。

不得把共享基础能力分支直接归入某个主功能分支，否则会模糊所有权并限制复用。

### 3.4 `external`

由其他仓库、服务、团队、权限或外部条件提供的能力。本仓只记录依赖、状态和证据，不伪造本仓提交。

## 4. 本地依赖清单

主 Issue 在以下位置维护建议性依赖图：

```text
.xflow/issues/issue-<id>/dependencies.yaml
```

示例：

```yaml
version: 0.1.0
issue: IK152D

dependencies:
  - issue: IK17AW
    repository: xflow-web
    type: shared-infrastructure
    requiredFor:
      - xflow.verify.case.stable-edge-anchor
    integrationTarget: mainline
    status: integrated

    blockingAssessment: partial
    decision: continue
    rationale: 属性编辑可继续，最终画布验证依赖统一端点能力。

    delivery:
      branch: fix/IK17AW-canonical-endpoints
      commit: abc1234
      mergeRequest: "56"

    integration:
      commit: def5678
      verifiedBy:
        - C-004
        - C-005
      evidence:
        - evidence/logs/c-004-integration-tests.txt
        - evidence/screenshots/c-005-after.png
        - evidence/dom/c-005-after.json

    closureAssessment:
      affectsClosure: true
      decision: integrated
      rationale: 相关验收已在主功能分支重新验证。
```

`requiredFor` 应引用能力契约、交互或验证 ID；没有能力契约的局部任务可以引用明确的验收条件 ID。

## 5. 生命周期

依赖状态采用：

```text
discovered -> active -> available -> integrated
                            \-> superseded
```

- `discovered`：已发现，尚未完成人工分类或远端 Issue 创建。
- `active`：依赖 Issue 已建立并正在开发。
- `available`：依赖自身已经完成，可以被主功能使用。
- `integrated`：主功能已经引入依赖并重新完成联合验证。
- `superseded`：设计变化后不再需要，必须记录原因。

状态不自动决定主 Issue 是否停工。开发人员需要显式填写：

- `blockingAssessment`: `none | partial | full`
- `decision`: `continue | pause-affected-scope | wait | use-temporary-adapter`
- `rationale`: 当前判断依据

这些字段属于开发判断。AI 可以准备分析材料，但不能把自己的判断伪装成人工结论。

## 6. 建议性而非硬阻塞

devctl 可以提示存在未完成依赖，但不得因为依赖处于 `discovered`、`active` 或 `available` 而禁止：

- 继续开发不受影响的部分。
- 创建本地提交。
- 运行测试和采集证据。
- 使用明确记录的临时适配机制。

开发人员可以根据影响范围选择继续、局部暂停、等待或使用临时适配。临时适配必须记录移除条件，不得被误认为最终基础能力。

最终完成声明仍受证据约束：

- 未集成依赖不影响当前验收时，可以声明 `resolved`，但必须填写 `affectsClosure: false` 和充分理由。
- 未集成依赖影响部分验收时，主 Issue 应为 `reduced`。
- 依赖导致当前工作无法继续时，主 Issue才为 `blocked`。
- `affectsClosure: true` 的依赖只有在 `integrated` 或有经审核的 `superseded` 结论后，才能支持主 Issue 的 `resolved`。

## 7. 分支与集成

### 7.1 主功能直接开发

主 Issue 范围内的开发直接发生在主功能分支，不创建形式化子 Issue。

### 7.2 子功能依赖

- 从主功能分支建立子功能分支。
- 子功能提交归属于子功能 Issue。
- 完成后以保留历史的方式合回主功能分支。
- 在主功能分支重新执行联合验证。

### 7.3 共享基础能力

- 从目标主干建立独立分支或 worktree。
- 独立完成测试、证据和解决报告。
- 先合入目标主干。
- 主功能分支再同步主干并重新验证。

### 7.4 外部依赖

记录提供方、可用版本、验证入口和当前状态，不在本仓创建虚假分支或提交。

## 8. 提交格式

所有功能分支提交必须采用中文、多行、带 scope 和 Issue 编号的可移植格式：

```text
type(scope): 中文核心摘要[#Issue编号]

- 中文说明实际修改
- 中文说明对应的契约、Finding 或验收条件
- 中文说明测试结果和证据位置
```

规则：

- 主功能分支直接开发的提交关联主 Issue。
- 子功能依赖分支的提交关联子功能 Issue，正文回链主 Issue。
- 共享基础能力分支的提交关联基础能力 Issue，正文列出已知使用方。
- 普通提交标题只放直接所有者 Issue。
- 明确的集成提交允许同时放主 Issue 和依赖 Issue。
- GitHub/Gitee Issue 编号保持原值，例如 `[#123]`、`[#IK17AW]`。
- `scope` 表示实际所有模块，不使用 `misc` 等无意义值。
- 不加入 AI 客户端签名、本机绝对路径或提供方专属元数据。

集成提交示例：

```text
merge(canvas): 集成统一容器事务能力[#IK152D][#IK17AW]

- 主功能 Issue：#IK152D
- 依赖 Issue：#IK17AW
- 说明集成方式和冲突处理策略
- 说明联合回归与证据
```

## 9. 证据与追溯

依赖 Issue 自己维护完整闭环：分析或契约、实现、测试、证据和解决报告。

主 Issue 不复制依赖 Issue 的全部证据，只维护：

1. 依赖决策证据：为什么拆分、影响哪些契约或验收条件、为什么继续或暂停。
2. 集成证据：主功能实际使用依赖后的新测试和新运行证据。

依赖 Issue 关闭或测试通过只能支持 `available`，不能自动支持 `integrated`。主 Issue 必须在实际集成状态下重新验证。

UI 集成条件继续要求截图与 DOM/运行态模型。共享基础能力合入主干后，主功能证据必须采集自同步后的代码。

## 10. devctl 检查边界

建议增加：

```text
devctl check dependencies --issue <id>
```

机械检查：

- YAML 结构、枚举和必填字段。
- Issue 编号兼容 GitHub/Gitee 标识。
- `requiredFor`、判断理由和决策非空。
- `available`、`integrated`、`superseded` 具备对应信息。
- 本地证据文件存在并位于当前 Issue 目录。
- `integrated` 具备集成提交、主 Issue 验证项和集成证据。
- 依赖 Issue 的解决报告不能被当作主 Issue 集成证据。
- `resolved` 报告具有完整 `closureAssessment`。

工具不判断：

- 依赖是否应该拆分。
- `blockingAssessment` 应为何值。
- 开发人员是否应该停工。
- 依赖的产品语义是否合理。
- 证据是否真正足以支持人工验收。

## 11. Skill 路由

开发、实现或测试期间发现新工作时，Skill 应：

1. 对照现有能力契约和主 Issue 范围。
2. 判断属于主 Issue 直接范围、`child-feature`、`shared-infrastructure` 还是 `external`。
3. 若需要远端依赖 Issue，准备范围、追溯和审批材料，等待人工批准创建。
4. 更新 `dependencies.yaml`，记录开发人员的阻塞评估和继续策略。
5. 根据类型选择父分支集成或主干优先集成。
6. 完成依赖自身闭环后标记 `available`。
7. 在主功能分支重新验证后标记 `integrated`。
8. 在主解决报告中说明依赖对最终结论的影响。

## 12. 验证场景

至少覆盖：

- 主 Issue 范围内的普通开发不会被迫创建子 Issue。
- 子功能依赖从父分支建立并合回父分支。
- 共享基础能力从主干建立并先合入主干。
- 活跃依赖不会阻止普通开发、提交或测试。
- 未集成依赖可以在充分理由下不影响 `resolved`。
- 影响验收的未集成依赖使结论保持 `reduced` 或 `blocked`。
- `integrated` 缺少主 Issue 新证据时检查失败。
- GitHub 数字编号和 Gitee 字母数字编号都通过。
- 普通提交只关联直接所有者 Issue。
- 集成提交可以同时关联主 Issue 和依赖 Issue。
- AI 无法通过填写依赖文件替代远端 Issue 创建审批或人工验收。

## 13. 完成标准

- Skill 能在开发中发现新依赖时正确分类，而不机械拆 Issue。
- 主功能分支继续允许直接开发。
- 依赖状态提供可追溯信息但不形成硬停工门禁。
- 子功能和共享基础能力拥有不同的分支与集成路径。
- 提交格式在主功能、依赖和集成提交中保持一致且可追溯。
- 主 Issue 的完成结论由集成后的新证据支持。
- devctl 只做结构和一致性检查，不替代开发人员和人工审核。
