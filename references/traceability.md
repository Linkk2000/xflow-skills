# Traceability And Closure

Use this exact chain: `contract → interaction → verification → issue → test → evidence → conclusion`.
Every link is an auditable artifact, not an AI assertion.

## Matrix Location And Shape

The matrix is exactly
`.xflow/issues/issue-<id>/traceability-matrix.yaml`; a matrix elsewhere is
invalid. It has `version: 0.1.0`, the exact `issue`, contract `id`, `version`,
and `file`, plus non-empty `entries`. Each entry has `id`, `contractObjects`,
`verification`, `acceptanceCriterion`, non-empty `tests`, `evidence.before`,
and `conclusion`; `evidence.after`, `ui`, and `blocker` are conditional.

`contractObjects` must exactly match the verification's `traces`, and may name
only interaction or constraint objects. Every active contract verification has
one trace entry, each active constraint is traced, and every entry binds one
Issue Acceptance Criterion. Tests use Issue-relative `path` and unique
`selector`. Evidence is Issue-relative and must remain in the repository.

`resolved|reduced` entries require fresh non-empty `evidence.after`; `blocked`
requires a structured external blocker and no after-evidence claim. Before and
after evidence may not be reused, and after evidence must be newer than its
before evidence. UI verification requires the declared screenshot and
structured observation artifacts. A code diff or an AI statement that tests
passed is not completion evidence.

## Recipe

```text
devctl trace check --issue <id> --contract <contract.yaml> --matrix .xflow/issues/issue-<id>/traceability-matrix.yaml
devctl check resolution-report --issue <id>
```

For a contract-bearing task, the trace check also verifies the accepted design:
the task state must reference the exact acceptance history record, contract
digest, accepted object set, Issue, branch/worktree binding, and
`accepted-design` decision. Keep `gap-analysis.md`, `issue-draft.md`, tests,
before/after evidence, and `resolution-report.md` under the tracked Issue
workspace. Do not move local evidence to COS/OSS/object storage or HTTP URLs.
A final
`resolution-report.md` must use one of `resolved|reduced|blocked` and cite the
fresh verification evidence for every claimed criterion.
