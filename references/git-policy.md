# Git Policy

## Git Action Matrix

| Action | Required state | Human gate | Required preflight | Allowed command |
|---|---|---|---|---|
| Inspect status | Any | No | None | `git status`, `devctl git status` |
| Create branch | Issue created | Yes: approve development | Clean worktree, issue number known | `devctl git start <slug> --issue <number>` |
| Stage files | Development | No | Scope matches issue | `git add <scoped files>` |
| Commit | Development | No, unless project requires | Read project rules, run tests/checks, run `devctl check commit-msg` | `devctl git commit-msg` or native `git commit` if message passes checks |
| Pull/rebase base | Before branch or conflict work | Ask if conflicts likely | Clean worktree or stash plan | `git pull --ff-only`, explicit rebase only after strategy preview |
| Push branch | After verification | Yes: approve push | `devctl check branch-scope`, tests/checks completed, no base branch | `devctl git push` |
| Sync target branch before MR/PR | After branch push, before MR/PR approval | Ask if merge/rebase may create conflicts; approval required for non-trivial conflict resolution | Clean worktree, target branch fetched, target branch SHA recorded | `git fetch origin <base>` then `git merge origin/<base>`; explicit rebase only after strategy preview |
| Create MR/PR | Branch pushed and target branch synced into the task branch | Yes: approve MR/PR | MR title/body preview, issue link, verification list, target branch SHA, sync result | `devctl git mr` |
| Resolve conflicts | During pull/rebase/merge | Yes for non-trivial conflicts | Conflict file list, strategy preview | Native git plus explicit file edits |
| Merge MR/PR | Remote review phase | Human performs or explicitly authorizes | CI/review status known | Provider UI/API only if authorized |
| Close issue | After merge or explicit cancellation | Yes: approve close | Confirm MR merged or task canceled | `devctl issue close <number>` |
| Delete branch / cleanup | After merge/close | Yes: approve cleanup | Confirm base updated, branch merged | `devctl git done` |

## Branch Requirements

- Development must happen on an issue-bound branch: `feature/<issue>-<slug>` or `fix/<issue>-<slug>`.
- Do not develop on `master`, `main`, `develop`, protected branches, or release branches.
- Do not push directly to protected branches through XFlow.
- Do not switch issues on the same branch. If scope changes, ask whether to create a new issue and branch.

## Commit Requirements

- Before commit, re-read project rules or run the project-rule check.
- Commit messages must follow project-level language and format rules.
- If no project-specific format exists, use Chinese summary plus a concise body when the change is non-trivial.
- Do not include unrelated formatting, drive-by refactors, or generated noise in the same commit.

## Issue Requirements Before Development

- Issue must have title, background, scope, acceptance criteria, and verification commands.
- Branch slug must derive from the approved issue title and issue number.
- Development may not begin merely because an issue exists; the user must approve development.

## MR/PR Requirements

- MR/PR body must link the issue, summarize changed files, list tests/checks run, and name any skipped verification.
- Push and MR/PR creation are separate human gates. MR/PR creation requires separate approval after push approval.
- Push approval only authorizes `devctl git push`; it does not authorize `devctl git mr`.
- `devctl git mr` must not push implicitly. If the branch has no upstream, fail and ask for push approval first, then request MR approval after `devctl git push` completes.
- Before MR/PR approval, the task branch must be synchronized with the target branch.
- Synchronization means: fetch the target branch, merge `origin/<base>` into the current task branch, resolve conflicts if any, rerun relevant checks, and record the target branch SHA plus the sync result in the MR/PR draft or local task evidence.
- Rebase is allowed only when the user or project policy explicitly prefers it and the agent previews the strategy first. The default XFlow strategy is merge target branch into the task branch.
- If synchronization creates conflicts, stop before non-trivial conflict resolution, show the conflict file list and intended strategy, and continue only after human approval.
- Do not create MR/PR if the task branch has not been synchronized with the current target branch or if post-sync checks have not been rerun.

## Conflict Requirements

- For simple lockfile or formatting conflicts, summarize the intended resolution before editing.
- For source-code conflicts, show affected files and choose a strategy: keep current, keep incoming, manually merge, or abort.
- Do not continue a rebase/merge after conflict resolution until checks relevant to touched files pass.
