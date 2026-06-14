# Academic XFlow Workflow

This file defines the Academic XFlow product line for the `academic` branch.
The `main` branch remains the general code-development workflow. The
`academic` branch is a long-lived product branch for academic research,
paper writing, translation, polishing, review, submission, and academic
skill orchestration.

## Core Principle

Academic XFlow uses two review layers:

1. Local human review confirms that the AI or Claude result is useful,
   directionally correct, and worth publishing to the remote platform.
2. Remote MR/PR review provides formal audit, CI, reviewer discussion,
   and merge protection.

TDD or verification output never replaces human judgement. It only proves
that the basic, machine-checkable target has been reached.

## Branch Semantics Rule

`academic` is the XFlow tool product line branch for `xflow-devctl` and
`xflow-skills`. It is not the paper repository's default branch and not the
normal task branch for paper work.

Paper repositories keep their own base branch, usually `main`, `master`, or a
human-defined branch. Academic tasks run on ordinary task branches such as
`feature/<issue>-<slug>`, `review/<issue>-<slug>`, or
`chore/update-academic-xflow-<date>`.

Every academic issue and MR draft must declare these three hidden fields:

```text
<!-- workflow-product-line: academic -->
<!-- paper-base-branch: <main|master|user-defined> -->
<!-- task-branch: <feature/<issue>-<slug>|review/<issue>-<slug>|chore/update-academic-xflow-<date>> -->
```

Do not create or push an `academic` branch in the paper repository unless the
human reviewer explicitly approves that repository policy. A paper repository
MR/PR should target the paper base branch, not the tool product line branch.

## Python Runtime Preflight

Academic devctl uses a Python 3.10+ core for UTF-8, path, template, and approval
gate handling. Before remote writes or local installer actions, AI assistants
must run `devctl preflight` and record the result in the TDD result sheet.

If Python 3.10+ is missing, devctl must fail closed. AI assistants must not
silently install Python. Installation requires a local human review approval
that names the installer command and the reason it is needed.

Python bytecode caches must not pollute workflow repositories. Academic devctl
launchers set `PYTHONDONTWRITEBYTECODE=1` before invoking the Python core.

## Windows Execution Surface

Windows users should default to PowerShell plus Python devctl. A normal
academic paper repository must not require WSL for initialization, remote Issue
or PR operations, Claude delegation, rule entrypoint sync, or local approval
checks.

WSL is a developer compatibility path for tool-repository tests and legacy Bash
fallback only. Upper AIs must not switch a paper repository workflow to WSL
unless the human reviewer explicitly requests it or the specific task cannot be
performed through PowerShell plus Python devctl.

Terminal status lines emitted by devctl wrappers, PowerShell helpers, and Bash
fallback scripts should stay ASCII. Chinese academic content, long Markdown,
remote Issue/MR bodies, Claude outputs, and human-review details should be
written as UTF-8 files and passed with file-based arguments such as
`--body-file`.

## Cursor And Three-Repository Setup

Academic users do not need Codex to use this workflow. A Cursor-like upper AI
can initialize and operate the workflow if it can see these three repositories:

1. `xflow-devctl@academic`: the executable local workflow tool.
2. `xflow-skills@academic`: the academic workflow rules and templates.
3. The user's paper repository: the Markdown, LaTeX, data, and `.xflow/`
   artifacts for a specific research project.

The paper repository should keep paper materials and workflow machinery in
separate areas. The recommended v2 layout is:

```text
<paper-repo>/
  manuscript/             -> paper text, LaTeX, Markdown, chapters
  assets/                 -> figures, tables, appendix media
  data/                   -> research or experiment data when tracked
  references/             -> bibliography, notes, citation materials

  .xflow/
    ops/devctl/           -> xflow-devctl academic
    ops/workflow/         -> xflow-skills academic
    issues/issue-<id>/    -> task, TDD, Claude, MR, review artifacts
    tools/                -> local workflow helpers
    local/                -> temporary body files, logs, scratch outputs

  devctl                  -> project wrapper
  devctl.ps1              -> project wrapper
  SKILL.md                -> synced workflow entrypoint
  AGENTS.md               -> Codex rule entrypoint when Codex initializes
  .cursorrules            -> Cursor rule entrypoint when Cursor is enabled
```

The paper repository `.gitmodules` must keep tool submodules on SSH URLs and
set `ignore = untracked` for both tool paths:

```ini
[submodule ".xflow/ops/devctl"]
    path = .xflow/ops/devctl
    url = git@github.com:Linkk2000/xflow-devctl.git
    branch = academic
    ignore = untracked

[submodule ".xflow/ops/workflow"]
    path = .xflow/ops/workflow
    url = git@github.com:Linkk2000/xflow-skills.git
    branch = academic
    ignore = untracked
```

Use `ignore = untracked`, not `ignore = all`. This hides accidental untracked
tool byproducts from the parent repository status while preserving visibility
for tracked submodule modifications and reviewed submodule pointer updates.

An upper AI must read the paper repository's own rule entrypoint, `SKILL.md`,
and relevant `references/*.md` files, then use `devctl` commands instead of
relying on Codex-specific skill installation.

AI-client rule entrypoints are managed by
`.xflow/ops/workflow/templates/ai-rules.json`. During initialization, sync the
entrypoint for the tool currently being used:

```bash
./devctl rules list
./devctl rules sync codex
./devctl rules sync cursor
```

On Windows PowerShell:

```powershell
.\devctl.ps1 rules list
.\devctl.ps1 rules sync codex
.\devctl.ps1 rules sync cursor
```

Only sync the entrypoint needed for the current tool. If a repository was
initialized by Codex and later opened in Cursor, add Cursor with
`devctl rules sync cursor`. If a target rule file already exists and differs,
review it locally before using `--force`.

Also copy `.xflow/ops/workflow/templates/xflow-powershell-native.ps1` to
`<paper-repo>/.xflow/tools/xflow-powershell-native.ps1`. PowerShell scripts
that run native commands should dot-source this helper.

The first local check in a paper repository is:

```bash
./devctl preflight
```

On Windows, PowerShell users may run:

```powershell
.\devctl.ps1 preflight
```

## GitHub Issue And PR Provider

In Academic XFlow, GitHub Issue and PR operations are handled by the Python
devctl core in academic mode. For GitHub repositories, set `GITHUB_TOKEN` in
the environment before running remote commands.

Read-only Issue commands do not require local approval:

```bash
./devctl issue list --state open --limit 20
./devctl issue show <id>
```

Issue creation requires an approved body file:

```bash
./devctl issue create "<title>" --body-file .xflow/issues/issue-draft/issue-draft.md --labels "academic"
```

On Windows PowerShell:

```powershell
.\devctl.ps1 issue create "<title>" --body-file .\.xflow\issues\issue-draft\issue-draft.md --labels "academic"
```

The command must not be run until the human reviewer has approved the exact
issue draft file and `.xflow/issues/issue-draft/approvals/local-review.md`
contains the matching SHA256. If the repository has no detectable GitHub
origin, set `DEVCTL_OWNER` and `DEVCTL_REPO` explicitly.

Issue comments and close operations are remote writes. Prepare the exact file,
obtain local human approval, then run:

```bash
./devctl issue comment <id> --body-file .xflow/issues/issue-<id>/comment-draft.md
./devctl issue close <id>
```

For `issue close`, the default approved file is
`.xflow/issues/issue-<id>/walkthrough.md`. Use
`DEVCTL_ACADEMIC_APPROVED_FILE` only when the reviewer intentionally approves a
different evidence file. Inline `--body` is rejected for issue comments in
academic Python mode.

For GitHub PR creation, prepare and approve the MR draft first:

```bash
./devctl git mr --title "<title>" --body-file .xflow/issues/issue-<id>/mr-draft.md --base main --issue <id>
```

On Windows PowerShell:

```powershell
.\devctl.ps1 git mr --title "<title>" --body-file .\.xflow\issues\issue-<id>\mr-draft.md --base main --issue <id>
```

The command validates `.xflow/issues/issue-<id>/approvals/local-review.md`
before pushing or creating the PR. Inline `--body` is rejected in academic
Python mode; use `--body-file` or the default issue MR draft.

`Approved Action: git-mr` covers the full PR publication sequence: pushing the
task branch, creating the PR, recording the returned PR number/URL in local
metadata or task artifacts, and pushing one metadata-only follow-up commit to
the same task branch before remote review starts. This metadata writeback must
not require a second approval file.

After the PR is merged, the task is sealed. Do not reopen the task branch or
create another PR only to check off a local task-board item, record that the PR
merged, or rewrite the local checklist. If `Closes #<id>` did not close the
remote Issue automatically, `devctl issue close <id>` is a separate maintenance
remote write with a new `Approved Action: issue-close`; it is not part of the
original PR completion criteria.

PR inspection is read-only and does not require local approval:

```bash
./devctl git pr-get <number>
```

The Python academic provider currently supports GitHub Issue
create/list/show/comment/close, PR creation, and PR lookup. Gitee Issue/PR
creation remains available only through the legacy shell provider path and must
not be assumed available in academic Python mode until it is ported.

## Updating An Initialized Paper Repository

Already-initialized paper repositories must not silently track the latest
`academic` branch heads. Updates are reviewable repository changes, not
background maintenance.

Use this sequence for a paper repository that already contains `.xflow/ops/devctl`
and `.xflow/ops/workflow`:

```text
fetch -> pin reviewed SHA -> test -> human review -> commit
```

Recommended local branch:

```bash
git switch -c chore/update-academic-xflow-<date>
```

Fetch the two tool repositories without changing the parent repository yet:

```bash
git -C .xflow/ops/devctl fetch origin academic
git -C .xflow/ops/workflow fetch origin academic
```

Pin reviewed SHA values, not whatever happens to be latest at execution time:

```bash
git -C .xflow/ops/devctl checkout <reviewed-devctl-sha>
git -C .xflow/ops/workflow checkout <reviewed-workflow-sha>
```

After pinning, sync generated or copied guardrail files from the workflow
submodule. Sync only the current or explicitly requested AI entrypoint:

```bash
cp .xflow/ops/workflow/SKILL.md ./SKILL.md
./devctl rules list
./devctl rules sync <codex|cursor>
```

On Windows PowerShell:

```powershell
Copy-Item .\.xflow\ops\workflow\SKILL.md .\SKILL.md -Force
.\devctl.ps1 rules list
.\devctl.ps1 rules sync <codex|cursor>
New-Item -ItemType Directory -Force .\.xflow\tools | Out-Null
Copy-Item .\.xflow\ops\workflow\templates\xflow-powershell-native.ps1 .\.xflow\tools\xflow-powershell-native.ps1 -Force
```

Use `devctl rules sync --all` only when the human reviewer explicitly wants all
declared AI entrypoints created or refreshed.

Run local checks before requesting review:

```bash
./devctl preflight
./devctl help
./devctl claude doctor
./devctl check tdd-result --issue <id>
./devctl check submodule-hygiene
```

On Windows PowerShell:

```powershell
.\devctl.ps1 preflight
.\devctl.ps1 help
.\devctl.ps1 claude doctor
.\devctl.ps1 check tdd-result --issue <id>
.\devctl.ps1 check submodule-hygiene
```

The update commit in the paper repository should contain only intentional
update surfaces:

- `.xflow/ops/devctl`: commit the submodule pointer to the reviewed devctl SHA.
- `.xflow/ops/workflow`: commit the submodule pointer to the reviewed workflow SHA.
- `SKILL.md`: commit the synced workflow entrypoint when it changed.
- `AGENTS.md`, `.cursorrules`, or other AI rule entrypoints: commit synced
  guardrails when they changed.
- `devctl` and `devctl.ps1`: commit wrapper changes only when the update
  explicitly requires wrapper changes.
- `.xflow/`: commit or archive local review evidence according to the paper
  repository policy.

If any check fails, do not continue to remote writes. Either fix the update on a
new local task branch or restore the previous reviewed submodule pointers.

## Submodule Hygiene Rule

`.xflow/ops/devctl` and `.xflow/ops/workflow` are read-only tool submodules from the paper
repository point of view. Workflow artifacts, logs, Claude outputs, TDD
results, and review files must be written to `.xflow/` or `.xflow/local/`, not
inside `.xflow/ops/*`.

Before local review, run:

```bash
./devctl check submodule-hygiene
```

On Windows PowerShell:

```powershell
.\devctl.ps1 check submodule-hygiene
```

The hygiene check verifies:

- `.xflow/ops/devctl` has no tracked modifications.
- `.xflow/ops/workflow` has no tracked modifications.
- common byproducts such as `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.tmp`,
  and `*.log` are not present under `.xflow/ops/*`.
- `.gitmodules` uses `ignore = untracked` for both tool submodules.

If the check fails, remove the byproduct or restore the tool submodule before
asking for human review. Do not solve this by using `ignore = all`, because that
would also hide real tracked modifications.

## PowerShell Native Git Rule

Windows PowerShell can misreport native command stderr as `NativeCommandError`.
Git also writes ordinary progress and status messages to stderr during commands
such as clone, fetch, checkout, and submodule add. Therefore, AI assistants must
judge native Git success by process exit code, not by the presence of stderr
text.

Use the workflow helper for reusable PowerShell scripts:

```powershell
. .\.xflow\tools\xflow-powershell-native.ps1

Invoke-XFlowGit -GitArguments @(
    "submodule", "add",
    "-b", "academic",
    "git@github.com:Linkk2000/xflow-skills.git",
    ".xflow/ops/workflow"
)
```

Do not use `2>&1 | Out-String` for `git submodule add`, `git clone`, `git fetch`, or `git checkout`.

Do not combine multiple native commands in one PowerShell line. Run one native
command, store its result object or exit code, inspect it, then run the next
command.

Preferred pattern:

```powershell
. .\.xflow\tools\xflow-powershell-native.ps1

$result = Invoke-XFlowGit -GitArguments @(
    "submodule", "add",
    "-b", "academic",
    "git@github.com:Linkk2000/xflow-skills.git",
    ".xflow/ops/workflow"
) -CaptureOutput
```

When logs are needed, use the structured result returned by the helper:

```powershell
$result = Invoke-XFlowGit -GitArguments @("submodule", "status") -CaptureOutput -AllowFailure
if ($result.ExitCode -ne 0) {
    throw "git submodule status failed with exit code $($result.ExitCode)`n$($result.Stdout)`n$($result.Stderr)"
}
```

Messages like `Cloning into ...` are not failures by themselves. After Git
submodule operations, verify the state with:

```powershell
git submodule status
git status --short
Test-Path .\.xflow\ops\workflow
Test-Path .\.gitmodules
```

## Required Local Artifacts

Each academic task must keep auditable files under:

```text
.xflow/issues/issue-<id>/
  issue-draft.md
  implementation_plan.md
  task.md
  tdd-result.md
  claude-task.md
  claude-result.md
  mr-draft.md
  walkthrough.md
  approvals/
    local-review.md
    history/
      local-review-<action>-<timestamp>.md
```

`claude-task.md` and `claude-result.md` are required only when Claude or
AcademicForge skills are used.

## State Machine

```text
S0_REQUEST
S1_LOCAL_ISSUE_DRAFT
G1_LOCAL_APPROVE_ISSUE
S2_CREATE_REMOTE_ISSUE
G2_APPROVE_DEVELOPMENT
S3_START_TASK_BRANCH
S4_EXECUTE_AI_OR_CLAUDE_TASK
S5_WRITE_TDD_RESULT
G3_LOCAL_REVIEW_RESULT
S6_PREPARE_COMMIT_AND_MR_DRAFT
G4_LOCAL_APPROVE_REMOTE_WRITE
S7_PUSH_BRANCH
G5_LOCAL_APPROVE_MR
S8_CREATE_REMOTE_MR
S9_REMOTE_REVIEW_AND_CI
G6_APPROVE_CLEANUP
S10_CLOSE_AND_ARCHIVE
```

## Gates

- `G1_LOCAL_APPROVE_ISSUE`: required before creating a remote issue.
- `G2_APPROVE_DEVELOPMENT`: required before creating or switching to a task branch.
- `G3_LOCAL_REVIEW_RESULT`: required after TDD/verify and before any remote write.
- `G4_LOCAL_APPROVE_REMOTE_WRITE`: required before pushing, commenting, or closing.
- `G5_LOCAL_APPROVE_MR`: required before creating an MR/PR.
- `G6_APPROVE_CLEANUP`: required before closing issues or deleting local branches.

Approval for one gate authorizes only the next action. It does not authorize
later remote writes.

Use machine-readable approval actions in `approvals/local-review.md`:
`issue-create`, `issue-comment`, `issue-close`, `git-mr`, or `remote-write`.

Do not invent active approval filenames such as `local-review-mr.md`. The
active approval file is always `.xflow/issues/issue-<id>/approvals/local-review.md`.
Superseded approvals should be archived under
`.xflow/issues/issue-<id>/approvals/history/` for audit only.

## Approval Hash Rule

Local approvals must bind to the reviewed artifact by hash. The approval
record must include:

- reviewer
- approval time
- approved action
- approved file
- approved SHA256

If the approved file changes, the approval is invalid and must be repeated.

## Claude Delegation Rule

Claude is a controlled academic sub-executor. The upper-level AI may call the
local Claude installation automatically, but only through a task package.

Claude output is never final by itself. It must be archived as a reviewable
artifact, checked by `devctl`, and approved by the human reviewer before it can
be used in final documents or remote MR/PRs.

Use this command for controlled delegation:

```bash
devctl claude run --issue <id>
```

The command validates `.xflow/issues/issue-<id>/claude-task.md`, extracts the
explicit `Invocation: /<skill-name>` line, prefixes that invocation to the task
package, passes the resulting prompt to the local Claude CLI, and writes the
result to the task package's `Output File`. The default execution shape is
`claude -p "/<skill-name>\n\n<task-package-content>"`. Skill invocation
arguments may be appended on the `Invocation:` line, for example
`Invocation: /peer-review focus=methodology severity=major`; devctl preserves
the whole invocation line when building the Claude prompt. Advanced users may
override the executable with `DEVCTL_CLAUDE_COMMAND` and append Claude CLI
arguments with `DEVCTL_CLAUDE_ARGS`, which are inserted before `-p`.

Claude task packages must not invent AcademicForge commands. Choose a verified
command from `references/academicforge-skill-catalog.md` and write it in all
three fields:

```text
Claude Skill: peer-review
Skill Source: AcademicForge
Invocation: /peer-review
```

The executable catalog can also be queried through:

```bash
devctl claude skills
```

`devctl claude run` rejects empty output, `Unknown command` output, and obvious
generic replies that ask for the task again. It does not hard-code one academic
review format, because individual Forge skills may return their own valid
formats. The task package should still request `## Summary`,
`## Proposed Changes`, `## Risks`, and `## Questions` when that format is
appropriate, and the human reviewer decides whether the Claude result is useful.

For `Skill Source: AcademicForge`, `devctl claude run` also checks the local
AcademicForge skill before invoking Claude. Claude resolves slash commands from
flat skill directories such as `.claude/skills/peer-review/SKILL.md`.
An official AcademicForge clone under `.claude/skills/academic-forge` is a
source tree; nested paths such as
`.claude/skills/academic-forge/skills/.../peer-review/SKILL.md` are not directly
callable as `/peer-review`. If only the nested source exists, devctl fails
closed and asks for a human-approved mirror or copy to the flat skill path.

Upper AIs must not ask users to manually copy prompts into Claude for normal
workflow execution. The upper AI should prepare the task package, run
`devctl claude run`, inspect the result file, run the required checks, and then
ask for human review.

Before using Claude for academic work, run:

```bash
devctl claude doctor
```

If Claude is available but no AcademicForge-derived skill is available in a
Claude-resolvable flat path, the command must report checked skill roots such as
`.claude/skills` and perform no installation. The upper AI may run the official
AcademicForge installer or mirror skills from an existing source tree only after
explicit human approval, because those actions write to Claude skill storage and
may download external repositories.

## Body File Rule

For Issue, comment, and MR/PR bodies, inline `--body` is only allowed for short
single-line plain text. Multi-line Markdown, fenced code, inline backticks,
JSON, shell snippets, or text containing `$()` must be written to a file and
passed with `--body-file`.

Remote-published body files must be written as public-facing Markdown because
`devctl` sends them to GitHub verbatim. Use hidden `<!-- xflow: ... -->`
comments for machine anchors, and do not include internal-only visible titles
such as `# Academic Issue Draft`, `# Issue Draft`, `# MR Draft`, or
`# PR Draft` in Issue or PR bodies.

Preferred locations:

```text
.xflow/local/<purpose>.md
.xflow/issues/issue-<id>/<purpose>.md
```

## Required Checks

Use these checks before local approval or remote writes:

```bash
devctl check academic-issue --issue <id>
devctl check tdd-result --issue <id>
devctl check claude-package --issue <id>
devctl check academic-mr --issue <id>
devctl check local-review --issue <id> --file <approved-file>
```

The exact command availability is defined by `xflow-devctl@academic`.
