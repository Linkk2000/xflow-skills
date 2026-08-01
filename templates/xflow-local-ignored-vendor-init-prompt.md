# XFlow Local Ignored Vendor Init Prompt

Copy this prompt to an AI assistant when a repository or directory should use
XFlow locally without committing the XFlow tool repositories.

```text
你现在负责在当前目录初始化 XFlow 工作流。

重要目标：
- 使用项目本地 XFlow，不使用全局 skill/devctl。
- 不使用 git submodule。
- 不提交 xflow-skills 或 xflow-devctl 源码。
- 将工具 clone 到当前项目：
  - .xflow/ops/workflow
  - .xflow/ops/devctl
- 这两个目录必须被当前项目 .gitignore 忽略。
- `.xflow/issues/` 默认 tracked；不得将 `.xflow/issues/` 加入 `.gitignore`。
- 只有项目规则显式声明 `issueWorkspace.mode: local` 时才允许例外。
- 不要依赖用户级 .codex、PATH devctl、临时开发目录或 WSL。
- Windows 下优先使用 PowerShell 原生命令和 devctl.ps1。
- 不要把多个 native git 命令写在同一行。
- 不要使用 `2>&1 | Out-String` 包裹 git clone、git fetch、git checkout。
- 本次只允许本地初始化，不允许 push，不允许创建 issue，不允许创建 MR/PR，不允许远端写操作。

工具来源：
- xflow-skills: git@github.com:Linkk2000/xflow-skills.git
- xflow-devctl: git@github.com:Linkk2000/xflow-devctl.git
- 默认分支: main

你需要先判断当前目录属于哪种情况：

A. 无 git 空目录：
- 可以执行 `git init`。
- 创建基础 XFlow 目录和入口文件。
- 不要 commit，除非用户明确批准。

B. 无 git 非空目录：
- 如果用户明确要求“把当前目录作为项目初始化”，可以执行 `git init`。
- 不要移动、删除、覆盖已有业务文件。
- 初始化前后都输出文件变化报告。
- 不要 commit，除非用户明确批准。

C. 有 git 空仓库：
- 使用已有 git 仓库。
- 不要改远端地址。
- 不要 push。
- 初始化 XFlow 本地工具和入口文件。

D. 有 git 已有项目：
- 使用当前项目。
- 不要重新 clone 业务仓库。
- 不要改远端地址。
- 不要覆盖已有 AGENTS.md、SKILL.md、.cursorrules；如需更新，先合并或生成备份说明。
- 不要 commit，除非用户明确批准。

初始化步骤：

1. 确认仓库状态：
   - 当前路径
   - 是否 git 仓库
   - 是否仓库根目录
   - 当前分支
   - 远端地址
   - git status --short

2. 创建目录：
   - .xflow/ops/
   - .xflow/issues/
   - .xflow/local/
   - .xflow/runtime/
   - .xflow/tools/

3. 更新 .gitignore，确保包含：
   - .xflow/ops/devctl/
   - .xflow/ops/workflow/
   - .xflow/local/
   - .xflow/runtime/
   - .xflow/issues/**/approvals/local-review.md
   - 不得添加 `.xflow/issues/`、`.xflow/issues/**` 或其他会忽略整个 Issue workspace 的规则。

4. 初始化工具：
   - 如果 .xflow/ops/devctl 不存在，clone `git@github.com:Linkk2000/xflow-devctl.git` 到 `.xflow/ops/devctl`，checkout main。
   - 如果 .xflow/ops/workflow 不存在，clone `git@github.com:Linkk2000/xflow-skills.git` 到 `.xflow/ops/workflow`，checkout main。
   - 如果目录已存在且是 git 仓库，只允许 fetch/checkout main，不得覆盖本地未提交修改。
   - 如果目录已存在但不是 git 仓库，停止并报告给用户。

5. 创建或更新 .xflow/xflow.json：
   使用 local-ignored-vendor 模式，记录：
   - workflow path: .xflow/ops/workflow
   - devctl path: .xflow/ops/devctl
   - source URL
   - ref: main
   - mode: local-ignored-vendor
   - humanGated: true
   - issueWorkspace: { "mode": "tracked" }
   - contracts: { "root": "docs/requirements" }

6. 同步入口文件：
   - 以 `.xflow/ops/workflow/SKILL.md` 为项目本地方法来源，不使用用户级或全局 Skill。
   - 读取 `.xflow/ops/workflow/templates/ai-rules.json`，逐一处理其中每个 target-template 映射，不得漏装任何目标。
   - 目标不存在时，从对应 template 创建；目标存在时只合并 XFlow 管理段。
   - 若项目自有文本与模板冲突，必须报告冲突并保留项目自有文本；不得覆盖项目自有文本，也不得用整文件复制替换。
   - 所有适配器只保留短硬规则，并路由到项目本地 `.xflow/ops/workflow/SKILL.md` 及其 references。
   - 创建根目录 `devctl.ps1`，调用 `.xflow/ops/devctl/devctl.ps1`。
   - 创建根目录 `devctl`，调用 `.xflow/ops/devctl/devctl`。
   - wrapper 必须从当前项目根目录运行。

7. 验证：
   - git status --short --branch
   - .\devctl.ps1 help
   - .\devctl.ps1 preflight
   - 确认 git status 中没有出现 `.xflow/ops/devctl/` 或 `.xflow/ops/workflow/` 内源码文件。
   - 确认 `.xflow/issues/` 未被忽略，且 Issue 过程材料可被 Git 跟踪。
   - 确认 `.xflow/local/`、`.xflow/runtime/` 和所有活动 `approvals/local-review.md` 被忽略。
   - 确认 `.xflow/ops/devctl` 和 `.xflow/ops/workflow` 各自有 git commit SHA。

8. 输出初始化报告：
   - 当前项目路径
   - 场景类型：A/B/C/D
   - 当前分支
   - 远端地址
   - devctl 本地路径、分支、commit SHA
   - workflow 本地路径、分支、commit SHA
   - 创建/更新的文件
   - .gitignore 是否正确忽略 ops/local
   - `.xflow/issues/` 是否保持 tracked，以及所有入口映射的安装/合并/冲突结果
   - 验证命令结果
   - 是否建议提交
   - 如果建议提交，生成提交计划和中文多行提交信息草稿，但不要自行 commit

硬性限制：
- 不要 push。
- 不要创建 issue。
- 不要创建 MR/PR。
- 不要把“继续”“都可以”“你看着办”当作 commit/push/issue/MR 批准。
- 不要把工具源码加入业务仓库 git。
- 不要提交 `.xflow/local/`、`.xflow/runtime/` 或活动审批文件。
- 不要使用 submodule。
```
