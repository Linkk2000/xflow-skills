# Git Policy

## Git Action Matrix

| Action | Required state | Human gate | Required preflight | Allowed command |
|---|---|---|---|---|
| Inspect status | Any | No | None | `git status`, `devctl git status` |
| Create branch | Issue created | Yes: approve development | Clean worktree, issue number known | `devctl git start <slug> --issue <number>` |
| Stage files | Development | No | Scope matches issue | `git add <scoped files>` |
| Commit | Development | No, unless project requires | Read project rules, run tests/checks, run `devctl check commit-msg` | `devctl git commit-msg` or native `git commit` if message passes checks |
| Pull/rebase base | Before branch or conflict work | Ask if conflicts likely | Clean worktree or stash plan | `git pull --ff-only`, explicit rebase only after strategy preview |
| Push branch | After verification | Yes: approve push | `devctl check current-task`, tests/checks completed, no base branch | `devctl git push --issue <id> --file <evidence.md>` |
| Sync target branch before MR/PR | After branch push, before MR/PR approval | Ask if merge/rebase may create conflicts; approval required for non-trivial conflict resolution | Clean worktree, target branch fetched, target branch SHA recorded | `git fetch origin <base>` then `git merge origin/<base>`; explicit rebase only after strategy preview |
| Create MR/PR | Branch pushed and target branch synced into the task branch | Yes: approve MR/PR | MR title/body preview, issue link, verification list, target branch SHA, sync result | `devctl git mr` |
| Resolve conflicts | During pull/rebase/merge | Yes for non-trivial conflicts | Conflict file list, strategy preview | Native git plus explicit file edits |
| Merge MR/PR | Remote review phase | Human performs or explicitly authorizes | CI/review status known | Provider UI/API only if authorized |
| Close issue | After merge or explicit cancellation | Yes: approve close | Confirm MR merged or task canceled | `devctl issue close <number>` |
| Delete branch / cleanup | After merge/close | Yes: exact `git-cleanup`; forced deletion uses exact `git-cleanup-force` | Confirm base updated, branch merged | `devctl git done --issue <id> --file <resolution-report.md>` |

## Branch Requirements

- Development must happen on an issue-bound branch: `feature/<issue>-<slug>` or `fix/<issue>-<slug>`.
- Do not develop on `master`, `main`, `develop`, protected branches, or release branches.
- Do not push directly to protected branches through XFlow.
- Do not switch issues on the same branch. If scope changes, ask whether to create a new issue and branch.

## Commit Requirements

- Before commit, re-read project rules or run the project-rule check.
- Commit messages must be portable, scoped, Chinese-dominant, multi-line, and issue-linked.
- First line format: `type(scope): 中文核心摘要[#Issue编号]`, where `scope`
  names the touched workflow, module, or issue area.
- The body uses Chinese-dominant bullet lines to describe actual changes, the
  corresponding contract, Finding, or acceptance condition, and test results
  with repository-relative evidence paths.
- Direct main-feature commits use the main Issue ID.
- Child-feature and shared-infrastructure commits use their direct dependency
  Issue ID and link the parent or known consumers in the body.
- Ordinary subjects contain one direct-owner Issue ID. Only `merge(...)` integration subjects may contain two Issue IDs, for example
  `merge(canvas): 集成统一容器事务能力[#IK152D][#IK17AW]`.
- GitHub numeric IDs and Gitee alphanumeric IDs are both valid, for example
  `[#123]` and `[#IK17AW]`.
- Portable means plain Git text that travels across GitHub/Gitee: no AI-client trailers, no local absolute paths, no machine-specific usernames, and no provider-only metadata.
- If no issue number is known, stop before committing and recover the active issue from the branch, `.xflow/current-task.md`, or the human reviewer.
- Do not include unrelated formatting, drive-by refactors, or generated noise in the same commit.

## Cleanup Approval Boundary

Task-scoped unattended mode never satisfies `git-cleanup` or `git-cleanup-force`.
Normal cleanup uses only `git branch -d` after exact
human approval and fails when Git reports the branch is not merged. There is
no implicit fallback to forced deletion. `--force` is a separate destructive
choice and requires exact human approval for `git-cleanup-force`.

Required downstream shape:

```text
type(scope): 中文核心摘要[#Issue编号]

- 中文说明实际修改
- 中文说明对应的契约、Finding 或验收条件
- 中文说明测试结果和证据位置
```

## Issue Requirements Before Development

- Issue must have title, background, scope, acceptance criteria, and verification commands.
- Branch slug must derive from the approved issue title and issue number.
- Development may not begin merely because an issue exists; the user must approve development.

## MR/PR Requirements

- MR/PR body must link the issue, summarize changed files, list tests/checks run, and name any skipped verification.
- Push and MR/PR creation are separate human gates. MR/PR creation requires separate approval after push approval.
- Push approval only authorizes `devctl git push`; it does not authorize `devctl git mr`.
- `devctl git mr` must not push implicitly. If the branch has no upstream, fail and ask for push approval first, then request MR approval after `devctl git push` completes.
- After PR/MR creation succeeds, devctl may create and push one metadata-only
  state backfill commit containing XFlow PR number/URL state. This post-MR
  push is covered by the `git-mr` approval and must not include business code
  or unrelated files.
- Before MR/PR approval, the task branch must be synchronized with the target branch.
- Synchronization means: fetch the target branch, merge `origin/<base>` into the current task branch, resolve conflicts if any, rerun relevant checks, and record the target branch SHA plus the sync result in the MR/PR draft or local task evidence.
- Rebase is allowed only when the user or project policy explicitly prefers it and the agent previews the strategy first. The default XFlow strategy is merge target branch into the task branch.
- If synchronization creates conflicts, stop before non-trivial conflict resolution, show the conflict file list and intended strategy, and continue only after human approval.
- Do not create MR/PR if the task branch has not been synchronized with the current target branch or if post-sync checks have not been rerun.

## Conflict Requirements

- For simple lockfile or formatting conflicts, summarize the intended resolution before editing.
- For source-code conflicts, show affected files and choose a strategy: keep current, keep incoming, manually merge, or abort.
- Do not continue a rebase/merge after conflict resolution until checks relevant to touched files pass.
