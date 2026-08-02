# Contract Generation Decisions

## Source of Truth

This scenario replays the approved D01-D22 decisions in
`.superpowers/sdd/2026-07-30-capability-contract-closure-implementation/task-13-discovery.md`.
The generated contract is the design candidate; this record does not constitute
contract acceptance or authorization to enter development.

## Replay Outcome

The capability is limited to project-local XFlow initialization and recovery.
It preserves existing project material, fails closed on unsafe or ambiguous
conditions, and stops before remote writes or implementation. The detailed
D01-D22 decision-to-object map below is part of this replay evidence.

## Approved Decision Coverage

| Decision | Adopted boundary | Contract coverage |
| --- | --- | --- |
| D01 | Bootstrap-only entry leaves the authority chain after project-local verification. | `xflow.constraint.project-local-authority`, `xflow.verify.bootstrap-handoff-and-independent-gates` |
| D02 | A confirmed non-Git project may run local `git init`; future audit proves no `.git` before, a local repository after, and no commit, remote, or push. | `xflow.constraint.local-git-initialization-boundary`, `xflow.verify.project-route.non-git-project` |
| D03 | Conflict targets remain unchanged and yield needs-review or blocked; independent, deterministic safe local actions continue with separate applied/skipped/conflicts audit, and unresolved conflict blocks development. | `xflow.constraint.partial-safe-recovery`, `xflow.verify.recovery-artifact-and-git-preservation` |
| D04 | Each tool records source, expectedRef, and resolvedCommit; restoration fixes that commit and does not upgrade implicitly. | `xflow.value.tool-binding-record`, `xflow.constraint.tool-binding-reproducibility`, `xflow.verify.tool-binding.reproducible-modes` |
| D05 | Workflow and devctl each use only vendor or submodule; only different per-tool modes form aggregate mixed, and every submodule needs configuration, .gitmodules, and gitlink agreement. | `xflow.value.tool-binding-record`, `xflow.constraint.tool-binding-reproducibility`, `xflow.verify.tool-binding.reproducible-modes` |
| D06 | Only known managed rule blocks change; external and unknown text stays byte-for-byte. | `xflow.constraint.managed-configuration-and-ignore-preservation`, `xflow.verify.managed-text-config-and-ignore-preservation` |
| D07 | Natural language authorizes only local inspection and safe initialization or recovery. | `xflow.constraint.enablement-authorization-boundary`, `xflow.verify.project-route.empty-directory` |
| D08 | Writes stay at a confirmed contained root; bare, outside, symlink, junction, and reparse roots fail closed. | `xflow.constraint.confirmed-root-and-trusted-source`, `xflow.verify.root-source-prerequisite-fail-closed` |
| D09 | Sources require project binding, exact instruction, or allowlist; public search and global or temporary fallback are prohibited. | `xflow.constraint.confirmed-root-and-trusted-source`, `xflow.verify.root-source-prerequisite-fail-closed` |
| D10 | Missing machine prerequisites are reported, never installed. | `xflow.constraint.machine-and-commit-preparation-boundary`, `xflow.verify.root-source-prerequisite-fail-closed` |
| D11 | Bootstrap acquires and verifies project tools, then `project-local-devctl` takes over initialize/recover and bootstrap exits authority. | `xflow.role.project-local-devctl`, `xflow.constraint.project-local-authority`, `xflow.verify.bootstrap-handoff-and-independent-gates` |
| D12 | Unknown xflow.json fields remain; only managed fields reconcile; invalid or conflicting configuration blocks unchanged. | `xflow.constraint.managed-configuration-and-ignore-preservation`, `xflow.verify.managed-text-config-and-ignore-preservation` |
| D13 | Vendor is acquired only when absent; only clean matching checkout aligns; dirty/non-Git content remains and reset is forbidden. | `xflow.constraint.recovery-artifact-and-git-preservation`, `xflow.verify.recovery-artifact-and-git-preservation` |
| D14 | Exact ignore rules only append with effective-ignore verification; broad Issue-hiding rules remain conflicts. | `xflow.constraint.managed-configuration-and-ignore-preservation`, `xflow.verify.managed-text-config-and-ignore-preservation` |
| D15 | Missing empty XFlow structure may be added; existing Issue, task, approval, and evidence stay byte-for-byte, without move, deletion, or rewrite. | `xflow.constraint.recovery-artifact-and-git-preservation`, `xflow.verify.recovery-artifact-and-git-preservation` |
| D16 | Only missing or known generated wrappers change; unknown same-name files remain conflicts. | `xflow.constraint.recovery-artifact-and-git-preservation`, `xflow.verify.recovery-artifact-and-git-preservation` |
| D17 | Branch, detached state, worktree, and local edits remain; remote operations do not write remotely. Fetch is limited to an explicit temporary ref or records FETCH_HEAD/refs effects, and never changes business branch/index/worktree/remotes/business remote-tracking refs. | `xflow.constraint.recovery-artifact-and-git-preservation`, `xflow.verify.recovery-artifact-and-git-preservation` |
| D18 | Initial-commit preparation only proposes files, checks, and a message draft; it never stages or commits. | `xflow.constraint.machine-and-commit-preparation-boundary`, `xflow.verify.project-route.no-or-empty-remote-git` |
| D19 | History remains evidence but active approval, unattended state, and old authorization never carry forward; AI cannot edit approval. | `xflow.constraint.approval-noninheritance-and-remote-gate`, `xflow.verify.bootstrap-handoff-and-independent-gates` |
| D20 | Ready requires each tool source, expectedRef, resolvedCommit, vendor/submodule mode, aggregate-mixed submodule proof when applicable, compatibility, wrapper, adapter, effective ignore, and no blocker. | `xflow.constraint.ready-result-audit`, `xflow.verify.ready-result-audit` |
| D21 | Results are ready, needs-review, or blocked and future evidence retains bindings, byte/hash comparisons, Git audits, effective-ignore output, planned, applied, skipped, conflicts, commits, and verification. | `xflow.value.implementation-evidence-record`, `xflow.value.recovery-audit-record`, `xflow.verify.ready-result-audit` |
| D22 | Bootstrap stops for human review; Issue, task, acceptance, development, commit, push, and PR/MR have separate later gates. Current replay has only negative `Approved: no` gate evidence. | `xflow.constraint.enablement-authorization-boundary`, `xflow.verify.bootstrap-handoff-and-independent-gates` |

The candidate is deliberately not an implementation plan. These directly stated
semantic requirements are projected only after their verification obligations
are met; projections may not invent reconciliation authority or later gates.

The deferred provider-details precondition is required only before a
provider-specific implementation or adapter. It does not block the current
generic local semantic contract or engineering projection.

## Verification Design Boundary

Every `verifyBy` in the candidate names a planned
`.xflow/local/evidence/project-local-initialization-recovery/` implementation
evidence artifact. These files do not exist in Task 13 and this decision record
does not substitute for them. Task 13 assesses whether the Skill can generate a
testable contract; implementation evidence remains `NOT_RUN` until an approved
engineering projection and implementation phase.
