# Human Gates

Human Approval Is Non-Delegable.

AI may prepare approval files, evidence, command drafts, and review notes, but
AI must never satisfy a human gate itself.
AI must never edit `Approved: no` to `Approved: yes`.
If AI approved the file, the approval is invalid.

Valid approval must explicitly name the exact next action. Valid examples:

- "创建 issue"
- "开始开发 issue 12"
- "推送当前分支"
- "创建 MR"
- "按方案 A 解决冲突"
- "清理本地分支并关闭 issue"
- "Create the issue"
- "Push the current branch"
- "Create the PR"

Invalid approval is vague, delegated, or outcome-based. Invalid examples:

- "继续"
- "都可以"
- "你看着办"
- "快点做"
- "测试过了就发"
- "go ahead"
- "looks good"
- "do what you think is best"

`--no-local-review` is a restricted exception, not a default route. It is valid
only when the current user explicitly authorizes the exact unattended
issue/comment command in the current conversation and the command has no
attachments or follows an already approved attachment publication flow.

`--no-local-review` must not be used for push, MR/PR creation, merge, issue
close, branch deletion, conflict resolution, or any destructive action.

When approval wording is ambiguous, ask one short confirmation question naming
the exact action.
