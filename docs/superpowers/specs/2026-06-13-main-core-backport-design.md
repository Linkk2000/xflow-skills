# Main Workflow Core Backport Design

## Background

`xflow-skills` also has two long-lived product branches:

- `main` defines the general software-development workflow.
- `academic` defines the academic research and writing workflow.

The academic branch introduced useful workflow rules that are not limited to
academic writing. The main branch should learn from those rules by defining a
general, platform-neutral workflow core. Academic-specific rules should remain
in the academic branch as a profile layered on top of the core.

## Design Goal

The main branch should describe a reusable development workflow that works for
Codex, Cursor, Claude, Gemini, and other upper AI tools.

The main branch should not become an academic workflow. It should not include
AcademicForge, paper-directory conventions, Claude academic task packages, or
academic-specific MR templates as default behavior.

## Core Concepts For Main

Main should define these domain-neutral concepts:

- Task-driven development through Issues or local task records.
- TDD or verification evidence before remote publication.
- Local human review before remote writes.
- Project-local tool execution through `devctl`.
- Pinned tool submodules for reproducibility.
- File-based bodies for shell-sensitive text.
- Platform-specific AI guardrails generated from the same source rules.

The general workflow should be:

```text
request -> local issue/task draft -> human approval -> task branch
-> implementation and tests -> TDD result -> human review
-> remote write or PR/MR -> remote review -> cleanup
```

## Local Human Approval

The local approval mechanism should be retained in main. It should be described
as "local remote-write approval" rather than "academic approval".

Any upper AI must stop before remote writes and present the exact artifact to
the human reviewer. Remote writes include:

- Issue creation;
- Issue comments;
- Issue close;
- branch push;
- PR/MR creation;
- global configuration writes;
- installer-like actions that modify shared tools.

The approval artifact should live under:

```text
.xflow/issues/issue-<id>/approvals/local-review.md
```

This path is the active approval file. AI clients must not create alternate
active approval names such as `local-review-mr.md`, `local-review-issue.md`, or
client-specific approval files. Cursor, Claude, Gemini, Codex, and any other
upper AI must all use the same active approval path before remote writes.

Historical approvals should be preserved under:

```text
.xflow/issues/issue-<id>/approvals/history/local-review-<action>-<timestamp>.md
```

Historical files are audit records. They do not satisfy the executable gate by
themselves. The active gate should read `approvals/local-review.md` unless a
human explicitly performs a reviewed recovery procedure that restores a
historical approval as the active file and confirms the reviewed file hash still
matches.

The reviewed artifact should usually be one of:

```text
.xflow/issues/issue-draft/issue-draft.md
.xflow/issues/issue-<id>/comment-draft.md
.xflow/issues/issue-<id>/mr-draft.md
.xflow/issues/issue-<id>/walkthrough.md
```

The approval file should bind the human decision to the exact reviewed file
with `Approved File`, `Approved Action`, and `Approved SHA256`.

Academic may require extra academic sections, but the hash-bound approval
pattern should belong to main.

## MR Review File Rule

Main should document the distinction between MR draft checks and local review
checks.

The MR draft is the file that becomes the PR/MR body:

```text
.xflow/issues/issue-<id>/mr-draft.md
```

The MR draft check should confirm required body sections and evidence links.
It should not be treated as proof that the human approved the MR.

The local review file is:

```text
.xflow/issues/issue-<id>/approvals/local-review.md
```

For PR/MR creation, the review file must approve the exact `mr-draft.md` that
will be sent remotely. The expected action should be `git-mr` or a documented
general remote-write action. A changed MR draft invalidates the approval until
the reviewer re-approves the new file hash.

This rule should be common to main and academic.

If MR approval happens over multiple rounds, the old active approval should be
archived into `approvals/history/` before writing the new active
`approvals/local-review.md`. The final active approval must still bind
`Approved Action: git-mr` to the exact `mr-draft.md` being submitted.

## PR Publication And Sealing Rule

The `git-mr` approval should authorize the complete PR publication sequence:

- push the task branch;
- create the remote PR/MR;
- write the returned PR/MR number and URL to local task artifacts;
- create and push one metadata-only follow-up commit when it only records PR/MR
  number, URL, and publication evidence.

This metadata writeback must not require a new active approval file. It belongs
to the same reviewed `git-mr` action and prevents infinite review loops caused
by auditing the audit record.

After the PR/MR is merged, the task board is sealed. AI clients must not reopen
the original task branch or create another PR only to check off a local
post-merge item, record that the PR merged, or update a checklist.

If the remote Issue was not automatically closed through `Closes #<id>`, manual
Issue close is a separate maintenance action. It may require a fresh
`Approved Action: issue-close`, but it is not part of the original PR/MR task
completion criteria and should not block sealing the original task.

## Tool And Skill Relationship

Main must clarify that there are three different tool surfaces:

1. Global source repositories:
   - `xflow-devctl`
   - `xflow-skills`
2. Project-local pinned submodules:
   - `.xflow/ops/devctl`
   - `.xflow/ops/workflow`
3. Project-root AI guardrail files:
   - `AGENTS.md`
   - `.cursorrules`
   - `CLAUDE.md`
   - `GEMINI.md`
   - `SKILL.md` when used by Codex

The execution source of truth is the project-local `devctl` and pinned
submodules. AI guardrail files help an AI client choose the right commands, but
they do not replace executable checks.

Already-initialized projects should update by pinning reviewed SHAs, testing,
asking for human review, and committing the submodule pointer changes. They
should not silently follow the latest remote branch head.

## Multi-Platform Templates

Main should provide platform-specific guardrail templates with equivalent
rules:

- `templates/agents.md` for AGENTS-compatible clients.
- `templates/cursorrules` for Cursor.
- `templates/CLAUDE.md` for Claude.
- `templates/GEMINI.md` for Gemini.
- `SKILL.md` for Codex skill installation when applicable.

Each template should say:

- read repository-local rules first;
- use repository-local `devctl`;
- write long bodies to files;
- do not perform remote writes without local human review;
- do not invent approval file names; the active approval file is
  `.xflow/issues/issue-<id>/approvals/local-review.md`;
- preserve superseded approvals under `.xflow/issues/issue-<id>/approvals/history/`;
- treat PR/MR metadata writeback immediately after creation as part of the same
  `git-mr` approval, and seal the task after the PR/MR merges;
- do not silently update tool submodules;
- do not depend on Codex-specific skill installation.

The templates may differ in file name and client wording, but they should not
define different workflow rules.

## What Stays Academic

The following should remain in `academic` and not be copied into main defaults:

- AcademicForge references;
- Claude academic task package requirements;
- paper repository layout such as `manuscript/`, `assets/`, `data/`, and
  `references/`;
- academic issue and MR headings;
- academic reviewer wording;
- rules about not using `academic` as a paper repository branch.

Academic can continue to require all main core rules plus its own stricter
profile-specific checks.

## Documentation Changes To Make Later

After the design is approved, implementation should update main branch docs:

- Add a general workflow contract reference.
- Add a tool/source relationship reference.
- Add a remote-write approval reference.
- Add multi-platform template files.
- Update `SKILL.md` so it no longer assumes Codex is the only AI surface.
- Add tests that check required references and reject academic-only leakage.

## Verification

The skills backport is acceptable only when:

- every new main reference is linked from `SKILL.md`;
- platform templates contain the same remote-write approval rule;
- tests verify the global/source, submodule, and guardrail file relationship;
- tests reject accidental AcademicForge or paper-layout references in main
  defaults;
- `git diff --check` passes.
