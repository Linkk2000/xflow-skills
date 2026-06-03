# XFlow 操作经验与防重复规则

## Shell 与 WSL

- 优先在 WSL 中执行项目命令；不要在同一次任务里混用 PowerShell 和 WSL 语义。
- 从 Codex 工具调用 WSL 时，复杂 Bash 命令容易被外层 PowerShell 解析。避免在一行命令中使用这些结构：
  - `$(...)`
  - here-doc
  - 未转义的 `|`
  - 多层嵌套引号
  - 带括号的提交信息
- 需要多行正文、复杂 jq、复杂 curl payload 时，优先写入临时正文文件，再传 `--body-file` 或让脚本读取文件。
- 临时脚本只能用于绕开 shell 转义问题，执行后必须删除，不能形成每个 issue 一个临时脚本的习惯。
- 使用 `wsl bash -lc 'cd /mnt/d/04-code/018-xflow/xflow && <simple command>'` 这种简单形态。若命令涉及 Markdown 正文、jq 过滤、JSON payload，应拆成多步。

## GitHub/Gitee Issue

- 创建 issue 必须使用完整 Markdown 正文，不允许只创建标题。
- 多行 issue 正文优先落到临时文件，通过仓库 devctl 的 `--body-file` 能力传递，避免在 WSL 命令行发生多重嵌套转义灾难。
- issue 在 PR/MR 审批/合并前不要关闭。开发完成后先发 PR/MR，等待评审。
- 开发分支开发完成后，必须使用 `devctl issue comment <number> --body "开发已完成。开发分支为 feature/<number>-<slug>"` 在 Issue 评论中进行状态反馈。
- issue 评论也可以通过文件传递：`./devctl issue comment <issue> --body-file <file>`。评论中的图片若不是平台已上传附件，应使用分支内版本化证据文件的 raw 链接。

## GitHub PR / Gitee MR

- PR/MR 标题不要手工包含 `[#ISSUE]`。`./devctl git mr --issue <issue>` 会自动加一次 issue 前缀，避免标题重复。
- PR/MR body 必须包含：
  - 关联 issue (使用 `Closes #<issue>` 格式以便合并后联动自动关闭)
  - 本次实际实现内容
  - 测试命令和结果
  - 手动验收或截图证据
  - 风险说明
- 不要在 PR/MR 中承诺未实现或未确认的交互能力。用户明确要求不写的功能点，即使本地代码有相关尝试，也不要写进 PR/MR/issue 文案。
- 如果截图需要在 PR/MR/issue 中长期可见，优先放到 `docs/evidence/<issue>/` 并使用远端分支 raw 链接。

## Git 与提交

- 提交前检查 `git status --short --branch`，确认只包含本次相关文件。
- 生成的临时文件必须删除；证据文件可以版本化，但要放到明确目录。
- 若 pre-commit hook 调用仓库不存在的命令导致失败，先运行本次相关的明确验证命令；确认通过后才可用 `git commit --no-verify`，并在最终说明原因。
- 提交信息在当前环境中避免使用复杂括号形式，必要时使用简单英文消息，例如 `fix: refine IJR3SK handle visibility`。

## 自适应验证规约

- 禁止生搬硬套其他仓库特有的验证脚本。
- AI 助手必须随时主动去查阅项目根目录下的 `AGENTS.md` 或者是 `README.md`，并提取出用于本地验证的正确动作。
- 若项目在开发环境中有预设的本地测试账号/端口配置，应将其优先归纳到项目专属的 `AGENTS.md` 中，严禁泄露和混淆平台凭证。

