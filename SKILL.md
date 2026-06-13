---
name: xflow-tdd-workflow
description: 通用型 Git & Issue TDD 开发工作流。适用于在本地通过 AI 助手梳理原始需求，生成规范化 issue 和开发分支（feature/编号-标题），并采用测试驱动（TDD）及 Planning with Files（基于项目内文件看板）方式开发、提交 PR/MR 并清理的自适应流程。
---

# 通用 Git & Issue TDD 开发工作流

## 目的 (Purpose)

本 Skill 用于引导 AI 助手遵循高标准、高品质的项目闭环开发工作流。AI 助手将遵循本地 `devctl` 工作流工具（一般以子模块形式挂载在项目根目录下的 `_ops` 目录或直接存放在根目录下），执行包含：原始需求梳理、远程 issue 创建、开发分支检出、测试先行开发（TDD）、Planning with Files 进度落盘、Pull Request 发起及本地关闭分支与 Issue 的闭环控制。

本工作流通过**项目上下文自适应探查协议**，实现与具体项目结构、语言及路径的完全解耦。

---

## 探索当前项目上下文 (Non-Negotiable)

在开始任何实质性工作之前，AI 助手**必须首先**自适应探查当前仓库的环境。禁止假定任何固定物理路径或特定的技术栈：

1. **确定执行根目录 `<current_repo>`**：即当前执行 `devctl` 或操作文件所在的 Git 仓库根目录。
2. **自适应阅读说明**：优先阅读 `<current_repo>/AGENTS.md`（项目特定规约说明）和 `<current_repo>/README.md`。AI 助手应从中获知：
   - 这是一个什么类型的项目（如 Java 后端、Vue 前端、Markdown 笔记库等）。
   - 该项目特定的编译、构建、测试与静态校验（Lint/Typecheck）指令。
   - 项目专属的架构逻辑、约束以及开发黑盒。
3. **安全凭证加载**：检查统一存放于 `~/gitee.env.local` 或环境变量中的 `GITHUB_TOKEN` 和 `GITEE_TOKEN`。禁止打印任何 Token 的明文值。

---

## 非妥协原则 (Non-Negotiables)

0. **语言规范**：除非用户另有要求，Issue 描述、PR/MR 标题及正文、工作进度看板以及最终交付总结一律使用**中文**。
1. **远程操作确认原则**：创建远程 issue、推送分支或发起 PR/MR 被视为高特权网络操作。在未向用户展示具体的内容预览（如 Issue Title/Body、Labels、PR Body）及拟执行命令前，**禁止**擅自执行创建或推送操作。
2. **KISS 与架构秩序平衡**：保持架构简单、易维护。但 **KISS 绝不等于无秩序**。合理的目录划分与职责隔离是 KISS 的基石。严禁以“简单”为借口将不同职责的代码混塞在同一个文件或目录中。
3. **测试先行（TDD）**：对于行为层面的修改，实现代码之前必须确保存在一个对应的失败测试用例，或明确在规划中写出客观的验收测试脚本。
4. **范围约束**：严格遵守 issue 划定的开发范围。不要顺手重构或修改任何与当前任务无关 of 公共设施或模块。
5. **架构边界与目录秩序**：在引入任何新文件、新模块或新类库时，必须评估其对整体架构和目录拓扑的影响。严禁无序扩张目录，严禁引入违反项目既有层级依赖的反向依赖（例如底层工具依赖上层业务）。

---

## 需求梳理与 Issue 创建

当用户提出口头需求或修改意见时：

1. **需求提炼**：用简短的一段话提炼用户的核心诉求，并结合探查到的技术栈划分波及范围（如：前端、后端、数据层或文档层）。
2. **编写 Issue 描述**：依据 [references/issue-template.md](references/issue-template.md) 进行格式化起草，包含背景、目标、待验证的 TDD 验收标准以及建议测试命令。
3. **分支名预览**：根据远程 Issue 编号及标题的 ASCII Slug 组合，拟定规范的分支名预览。
4. **获取批准**：向用户展示 Issue 全文及拟执行的 `devctl issue create` 命令，待用户确认后执行创建，并捕获返回的 Issue 编号与 URL。若 Issue 正文包含多行 Markdown、反引号、代码块、JSON 或 shell 片段，必须先写入临时 Markdown 文件，再使用 `devctl issue create "<title>" --body-file <file>`；禁止把复杂正文直接放入 `--body` 参数。

---

## 分支命名规范

本地分支名必须由已确认 of Issue 编号派生，不得随意发明：

* **功能分支 (Feature Branch)**：`feature/<issue-id>-<short_slug>`
* **缺陷分支 (Defect Branch)**：`fix/<issue-id>-<short_slug>`

其中 `<short_slug>` 应由确认的 Issue 标题转换而来，仅包含小写 ASCII 字母、数字及横杠 `-`。若远程 Issue 编号在创建前未知，可在预览时先以 `<issue-id>` 代替，并在创建成功后对其进行具象化。

*示例*：
- `feature/12-integrate-github-provider`
- `fix/105-resolve-escape-error-in-wsl`

---

## 平台与 Shell 稳定性准则

在 Windows + WSL + 中文仓库环境中执行本工作流时，AI 助手必须先降低平台噪音，而不是把环境问题误判为业务问题：

详细经验与案例见 `references/ops-lessons.md`，遇到 shell、编码、dev server、远程 issue/MR 命令异常时应优先读取。

1. **WSL 优先且单一执行面**：若用户已明确 WSL 可用，开发、测试、git、devctl、服务启动优先全部在 WSL 内执行；不要在同一任务中频繁混用 PowerShell 与 WSL。
2. **避免复杂跨 shell 一行命令**：从 PowerShell 调用 `wsl --exec bash -lc` 时，禁止把复杂引号、正则、`$()`、长管道和多层嵌套塞进一行。优先使用项目内脚本、`devctl` 命令、短命令或 heredoc。
3. **不要依赖中文终端输出做补丁锚点**：中文 Markdown / shell 输出可能显示为 mojibake。编辑中文文档时优先使用 ASCII 锚点、结构位置、行号附近上下文或追加章节，避免用乱码文本作为 patch 匹配依据。
4. **避免无边界递归扫描**：在 `/mnt/c`、`/mnt/d` 等 Windows 挂载盘上，优先使用 `git grep`、限定目录的 `find -maxdepth` 或精确文件读取；不要用无边界 `grep -R` 扫大型 monorepo。
5. **进程管理必须精确**：长期服务使用项目脚本或 pid 文件管理。禁止用宽泛 `pkill -f` 模式清进程，因为它可能匹配并杀死当前 shell。若必须清理，先 `pgrep -a` 核对 PID，再按 PID 处理。
6. **后台服务必须验证存活**：启动 dev server 后，必须在新的 shell 调用中再次检查 `pid`、端口监听和 HTTP 响应，避免进程随 WSL shell 退出而短暂成功。
7. **环境阻塞与业务修复分线处理**：若 dev server、编码、shell、权限或包管理器问题阻塞 UI 验证，应把它作为独立 B 线记录到 Planning with Files；业务线只能声明已通过的单测/typecheck，不能把未完成的 UI 验证说成已完成。

---

## Planning with Files 规范 (去平台依赖与沙盒化归档)

为了保证长周期开发的可打断性、多 AI 客户端（如 Cursor、Cline、Gpt 网页端）的绝对兼容，以及历史设计决策的永久可追溯性，AI 助手必须在当前项目根目录下的 `.xflow/issue-<number>/` 独立目录中创建和维护规划文件（其中 `<number>` 为当前 Issue 编号，如 `.xflow/issue-12/task.md`）。禁止依赖任何特定 AI 平台的内置 Artifact 机制或在根目录下直接写入单一文件：

1. **方案设计（.xflow/issue-<number>/implementation_plan.md）**：
   在开始任何任务或重大修改前，必须先在项目内的 issue 文件夹中创建此文件。内容应包括：
   - 目标描述与背景
   - 待澄清的开放性问题
   - 拟修改的文件列表与架构设计方案（如涉及新文件/新目录，**必须以目录树 diff 形式**显式画出新建目录及其模块职责归属）
   - 依赖关系评估（确认无循环依赖、无反向越界依赖）
   - 该方案被用户确认后，方可进入开发。

2. **待办追踪（.xflow/issue-<number>/task.md）**：
   这是开发过程中的活性进度看板。
   - 每一项功能或重构任务之前，必须包含一个 `- [ ] 先编写/确认对应的失败测试` 的子待办项。
   - 必须确保该失败测试子项变为已完成 `[x]` 后，方可开始实现对应的业务功能代码（恪守 TDD 原则）。
   - 随着进度，AI 助手需要增量更新此文件的状态，并及时提交到 Git。

3. **变更交付（.xflow/issue-<number>/walkthrough.md）**：
   - 在任务结束且测试全部通过后更新，记录修改的文件、测试命令和运行通过的验证证据。

这些文件是项目仓库本身历史的一部分，应被纳入 Git 版本控制，使任何人在任何机器克隆代码后，均能立即通过读取对应的 issue 目录，还原和接管开发进度。

---

## TDD 开发与验证流程

1. **切换分支**：从主干分支（`main` 或 `master`）拉取最新代码，并以此为基准建立 Issue 分支：
   `devctl git start <slug> --issue <number>`
2. **测试先行**：根据前述的验收标准，先在项目中确定、运行或编写一个会失败的单元测试或手动验收脚本。
3. **小步实现**：编写最少量的业务代码使测试通过。
4. **回归与静态分析**：根据自适应探查出的项目命令，运行对应的静态分析（如 `typecheck`、`lint`）以及完整的模块测试，确保零破坏。
5. **在 Issue 中评论开发进度**：在发起 PR 前，通过命令行发表评论说明开发分支的已完成状态：
   `devctl issue comment <number> --body "开发已完成。开发分支为 feature/<number>-<slug>"`
   若评论包含多行 Markdown、测试清单或代码片段，必须改用 `devctl issue comment <number> --body-file <file>`。

---

## PR/MR 与关闭同步工作流

1. **发起合并**：
   向用户展示 PR/MR 标题及包含 `Closes #<number>` 关联语法的 PR 正文草稿，经批准后运行：
   `devctl git mr --title <title> --body-file .xflow/issues/issue-<number>/mr-draft.md --issue <number>`

## Core Remote Write Review Gate

- Core remote writes are `issue-create`, `issue-comment`, `issue-close`, and `git-mr`.
- Prepare remote body files before running remote-write commands:
  - `.xflow/issues/issue-draft/issue-draft.md`
  - `.xflow/issues/issue-<id>/comment-draft.md`
  - `.xflow/issues/issue-<id>/mr-draft.md`
  - `.xflow/issues/issue-<id>/walkthrough.md` for issue close evidence
- Run `devctl check issue-draft`, `devctl check mr-draft`, and `devctl check local-review` before remote writes.
- The active approval file is always `.xflow/issues/issue-<id>/approvals/local-review.md`; use `.xflow/issues/issue-draft/approvals/local-review.md` before creating a remote issue.
- `Approved Action` must be one of `issue-create`, `issue-comment`, `issue-close`, `git-mr`, or `remote-write`.
- Use `--body-file` for Issue, comment, and MR/PR bodies. Do not pass long Markdown through inline command arguments.
- Remote-published body files must not include internal-only visible titles such as `# Issue Draft`, `# MR Draft`, `# PR Draft`, or `# Merge Request Draft`.

## Git Commit Attribution Rule

- Do not add Cursor co-author trailers.
- Do not append `Co-authored-by: Cursor <cursoragent@cursor.com>` to commit messages.
- Do not use `git commit --trailer` to add Cursor, cursoragent, or AI-client co-author metadata.
- Keep commit attribution limited to the repository's configured Git author unless the human reviewer explicitly requests otherwise.
2. **等待评审**：在远端 PR/MR 审核及合并前，禁止手动关闭 Issue。
3. **合流同步**：一旦远端 PR/MR 完成合并，Issue 亦会被自动关闭。若未自动关闭，则手工运行 `devctl issue close <number>`。
4. **本地清理**：运行 `devctl git done` 自动将本地工作区切回主干、拉取最新代码并安全删除本地已合并的开发分支，恢复工作区绝对纯净。
