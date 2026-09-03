# Git Policy

## Git Action Matrix

| Action | Required state | Human gate | Required preflight | Allowed command |
|---|---|---|---|---|
| Inspect status | Any | No | None | `git status`, `devctl git status` |
| Create and activate final task branch | Issue created, no implementation | Yes: exact `task-branch-start` identity approval | Base branch active; canonical task-state binds the final branch; changes limited to the matching Issue workspace | `devctl git start <slug> --issue <number> --file .xflow/issues/issue-<number>/task-state.md` |
| Early artifact commit after `git start` | Final task branch just activated; Issue workspace / process files written | No, unless project requires commit approval | Artifacts-only staging; no product implementation paths | `git add` scoped process files, then `devctl git commit-msg` / `git commit` |
| Enter development | Final task branch active; required contract acceptance or gap recognition is bound; prior early artifact commits done | Yes: separate development-start approval | Route semantic exit verified; process artifacts not left untracked dominating the worktree | Set `S4_TDD_AND_IMPLEMENTATION`, then begin TDD |
| Stage files | Task branch active (artifact commits allowed before development; implementation staging during development) | No | Scope matches issue; artifact commits exclude active `local-review.md` and runtime-only files | `git add <scoped files>` |
| Commit | Task branch active (early artifact commits before G2/S4; implementation commits during development) | No, unless project requires | Read project rules, run tests/checks, run `devctl check commit-msg`; keep artifact commits separate from implementation | `devctl git commit-msg` or native `git commit` if message passes checks |
| Pull/rebase base | Before branch or conflict work | Ask if conflicts likely | Clean worktree or stash plan | `git pull --ff-only`, explicit rebase only after strategy preview |
| Push branch | After verification | Yes: approve push | `devctl check current-task`, tests/checks completed, no base branch | `devctl git push --issue <id> --file <evidence.md>` |
| Sync target branch before MR/PR | After branch push, before MR/PR approval | Ask if merge/rebase may create conflicts; approval required for non-trivial conflict resolution | Clean worktree, target branch fetched, target branch SHA recorded | `git fetch origin <base>` then `git merge origin/<base>`; explicit rebase only after strategy preview |
| Create MR/PR | Branch pushed and target branch synced into the task branch | Yes: approve MR/PR | MR title/body preview, issue link, verification list, target branch SHA, sync result | `devctl git mr` |
| Resolve conflicts | During pull/rebase/merge | Yes for non-trivial conflicts | Conflict file list, strategy preview | Native git plus explicit file edits |
| Merge MR/PR | Remote review phase | Human performs or explicitly authorizes | CI/review status known | Provider UI/API only if authorized |
| Close issue | After merge or explicit cancellation | Yes: approve close | Confirm MR merged or task canceled | `devctl issue close <number>` |
| Delete branch / cleanup | After remote PR/MR merge or close | Yes: exact `git-cleanup`; forced deletion uses exact `git-cleanup-force` | PR merged/closed (unless force); discard Issue process residuals under `.xflow/issues/issue-<id>/` and `.xflow/publish/issues/issue-<id>/` only; unrelated dirty paths fail closed—do not stash | `devctl git done --issue <id> --file <resolution-report.md>` |

## Branch Requirements

- Development must happen on an issue-bound branch: `feature/<issue>-<slug>` or `fix/<issue>-<slug>`.
- Do not develop on `master`, `main`, `develop`, protected branches, or release branches.
- Do not push directly to protected branches through XFlow.
- Do not switch issues on the same branch. If scope changes, ask whether to create a new issue and branch.

## Commit Requirements

- Early XFlow artifact commit: after `devctl git start` succeeds, commit the
  Issue workspace and other newly written trackable process files alone before
  contract acceptance, gap recognition, G2, or implementation. After each later
  major gate that adds trackable process files—at least `contract-acceptance` /
  `gap-recognition` and other pre-development gates that append
  `approvals/history/`—again commit those artifacts alone before changing
  product implementation paths. Keep artifact commits separate from
  implementation commits. Do not delay solely because G2 is still pending:
  once contract or gap history is on disk, commit the process files. If the
  project still requires explicit human approval to commit, request that
  approval immediately after the gate, not at the end of implementation. Do
  not stage active `approvals/local-review.md` or machine-local/runtime-only
  files. Early artifact commit does not authorize push, MR/PR, or entering
  development. Still obey “no Issue number, no commit” and scoped staging.
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
- If no Issue number is known, stop before committing. Run `devctl task status`,
  verify the worktree-local pointer, and open the matching
  `.xflow/issues/issue-<id>/task-state.md`; never infer authority from a branch
  name or repository singleton. For an explicitly requested legacy migration,
  use `devctl task migrate-current` once and then rely on v2 Issue state.
- Do not include unrelated formatting, drive-by refactors, or generated noise in the same commit.

## Cleanup Approval Boundary

Task-scoped unattended mode never satisfies `git-cleanup` or `git-cleanup-force`.
Normal cleanup uses only `git branch -d` after exact
human approval and fails when Git reports the branch is not merged. There is
no implicit fallback to forced deletion. `--force` is a separate destructive
choice and requires exact human approval for `git-cleanup-force`.

Post-merge Issue residual discard: after the remote PR/MR is merged, do not
propose further feature-branch commits or pushes for that Issue. `devctl git
done` discards uncommitted residuals under `.xflow/issues/issue-<id>/` and
`.xflow/publish/issues/issue-<id>/` when they are the only dirt, then lands on
a clean base aligned with `origin/<base>`. Do not stash those residuals (or
unrelated work) to pass a clean-worktree check and restore them onto base, and
do not propose committing discarded residuals afterward. Unrelated dirty paths
outside those prefixes must be preserved; finish or move them before retrying
cleanup. Do not backfill post-merge residuals into the already-merged PR.

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
- `task-branch-start` creates and activates only the exact final branch. It
  authorizes neither implementation nor remote write. Immediately after
  `git start`, perform the first Early XFlow artifact commit (or immediately
  request commit approval) before further gates.
- Development may not begin merely because an issue or task branch exists. For
  capability work, contract acceptance occurs on the final branch, and the
  user must separately approve development afterward. Contract or gap history
  may be committed as artifacts before that development approval.

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
