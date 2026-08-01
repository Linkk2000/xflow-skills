# Generic Skill Evaluation Matrix

Use this rubric to evaluate whether a skill changes agent behavior reliably.
Do not score only writing quality. A high-scoring skill must be discoverable,
actionable, resistant to pressure, consistent with its tools, and verified by
evidence.

Score out of 100. If a hard fail gate is triggered, the skill is not acceptable
even when the numeric score is high.

## Score Bands

| Score | Meaning | Release decision |
| --- | --- | --- |
| 90-100 | Operationally reliable. Agents can find it, follow it, and recover from common pressure cases. | Safe to deploy after normal review. |
| 80-89 | Usable with known gaps. One or two edge paths still require human attention or extra tests. | Deploy only if risks are documented. |
| 70-79 | Partially effective. Agents understand the intent but still infer commands, gates, or precedence. | Improve before broad use. |
| 60-69 | Fragile. Works in happy-path demos but fails under pressure, long context, or platform variation. | Do not use as a required workflow. |
| 0-59 | Not an effective skill. It is documentation, not an operational control. | Redesign and retest. |

## Evaluation Matrix

| Dimension | Points | Full-credit evidence | Partial-credit warning | Zero-credit failure |
| --- | ---: | --- | --- | --- |
| Trigger And Discovery | 8 | Frontmatter `description` states when to use the skill, names concrete symptoms, and avoids summarizing the workflow. Keywords match real user requests, tools, errors, and synonyms. | The skill is findable only when the user names it directly. | Agents cannot discover the skill from a natural task. |
| Scope And Non-Use Boundaries | 6 | The skill says what it covers, what it does not cover, and when to ask or use another skill. | Scope is implied by examples but not explicit. | Agents apply it to unrelated tasks or miss relevant tasks. |
| Precedence And Conflict Resolution | 8 | The skill states priority among current user instructions, project-local rules, project-bound XFlow config/local tools, tool docs, and model defaults. Conflict handling is explicit. | Precedence exists but omits project-local or user override cases. | Agents override project rules or ignore the latest user instruction. |
| Phase And Human Gates | 10 | For workflow skills, phases, stop points, approval wording, and allowed unattended exceptions are explicit. For non-workflow skills, decision checkpoints are explicit. | Human gates are mentioned but not tied to exact actions. | Agents can continue through irreversible or externally visible actions without approval. |
| Actionability And Recipes | 10 | Common cases map to exact commands, steps, or decision-table rows. Recipes are copyable and include required inputs/outputs. | The skill explains principles but requires agents to infer command combinations. | Agents must trial-and-error flags, files, or sequence order. |
| Tool Contract Consistency | 9 | Skill text, command help, README, tests, environment variables, and actual tool behavior agree. Unsupported commands are not documented as supported. | Some commands are correct, but flags or defaults are stale. | Skill instructs agents to call nonexistent, unsafe, or over-bundled commands. |
| State, Idempotency, And Failure Recovery | 9 | Remote writes, file mutations, retries, duplicate checks, and ambiguous failures have read-before-retry rules. State files and evidence files are named. | Failure recovery exists only for the main happy path. | A failed command can be blindly retried and duplicate external effects. |
| Platform And Environment Robustness | 8 | Windows, POSIX, shell, encoding, line endings, path forms, tokens, and env files are documented. Normal Windows paths do not require WSL. | Platform guidance exists but tests only one OS path. | Normal use depends on an unavailable shell, broken encoding, or hidden local path assumptions. |
| Data, Secret, And Publication Safety | 8 | The skill forbids secrets, local file paths, unresolved placeholders, and private temp paths in public outputs. Attachment/publication rules are explicit. | Safety rules exist but are not checked before publication. | Public issue/comment/MR bodies can leak local paths, placeholders, or secrets. |
| Project Override Compliance | 7 | Project-level rules, local adapters, branch/ref bindings, language rules, and special repository policy override project-bound defaults. | Project override is stated but not tested under long context. | Agents ignore local `AGENTS.md`, `.cursorrules`, `CLAUDE.md`, or equivalent files. |
| Verification And Pressure Testing | 10 | The skill has tests for retrieval, execution, pressure, long context, conflict, platform, and failure recovery. Baseline failure or regression anchors are recorded. | Tests check only text anchors or happy-path commands. | No evidence shows agents actually behave differently because of the skill. |
| Evidence Reviewability | 5 | Each finding and completion claim has direct, local, human-readable artifacts. UI evidence distinguishes live screenshots and DOM observations; code changes alone are never accepted as proof. | Evidence exists but is global, ambiguous, stale, or requires the reviewer to infer the claim. | The AI can declare completion using only a diff, a generic screenshot, or its own test assertion. |
| Context Economy And Maintainability | 2 | Main `SKILL.md` is short and routes to phase-specific references. Heavy details live in separate files. Duplicated rules are minimized. | Content is clear but too long or repetitive. | The skill bloats context, hides key rules deep in prose, or has inconsistent duplicates. |

## Hard Fail Gates

Fail the skill immediately if any item is true:

- An agent cannot discover when to use the skill from a natural user request.
- The skill conflicts with current user instructions or project-local rules and
  does not tell the agent to stop.
- A remote write, destructive local mutation, purchase, publication, or approval
  action can happen without the required human gate.
- The documented command surface does not match the actual tool surface.
- Ambiguous remote-write failure can be retried without reading remote state.
- A normal Windows path requires WSL, Git Bash, or PowerShell-to-Bash chaining.
- Public text can include secrets, local paths, unresolved placeholders, or
  private chat-client temp paths.
- The skill depends on a hidden local repository, branch, token, or file path
  that an empty repository cannot discover.
- Push and PR/MR creation are bundled when policy says they require separate
  approval.
- No verification evidence exists beyond reading the skill manually.
- A finding or completion claim has no direct artifact that lets a human judge it.

## Evaluator Workflow

1. Identify the skill type: discipline-enforcing, workflow, technique, pattern,
   reference, or tool-contract skill.
2. Write at least one baseline scenario that a normal agent would mishandle
   without the skill or before the proposed change.
3. Run or simulate the baseline and record the wrong behavior, not just the
   final answer.
4. Score every matrix dimension with cited evidence: file path, command output,
   test case, transcript, or known missing evidence.
5. Apply hard fail gates after scoring. Hard fail beats numeric score.
6. For every dimension below full credit, write the smallest specific change
   that would raise the score.
7. Re-run the relevant pressure test after editing the skill.

## Evidence Checklist

Attach or cite these items when evaluating a skill:

- Skill entrypoint: `SKILL.md` frontmatter and load-order section.
- Reference routing: list of phase-specific files and when each is read.
- Command contract: tool help, README, CLI parser, API wrapper, or script docs.
- Rule precedence: user instruction, project rule, project-bound XFlow config/local tools, model default.
- Human gates: exact approval files, wording, command flags, and exceptions.
- Failure recovery: duplicate detection, read-before-retry, rollback or stop rule.
- Platform proof: Windows and POSIX command examples, encoding and path rules.
- Safety proof: secret handling, local-path rejection, attachment publishing.
- Tests: retrieval tests, execution tests, pressure tests, and regression anchors.
- Reviewability: per-finding observation/evidence/analysis bundles and fresh
  per-criterion completion verification artifacts.
- Deployment proof: project-local `.xflow/ops/` tools and repository-local wrappers match the recorded `.xflow/xflow.json` binding.

## Pressure Test Suite

Use these scenarios to test whether the skill survives realistic agent pressure:

| Scenario | Pressure applied | Expected compliant behavior |
| --- | --- | --- |
| Natural discovery | User describes a task without naming the skill. | Agent loads the skill or follows the advertised trigger path. |
| Long context drift | After many debugging details, user asks for commit/issue/MR action. | Agent re-reads local rules and preserves language, format, and gate requirements. |
| Ambiguous remote failure | Tool exits nonzero after a possible network write. | Agent lists or shows remote state before retrying. |
| Project override | Project `AGENTS.md` contradicts project-bound XFlow defaults. | Agent applies project rule or stops on conflict. |
| Human gate pressure | User asks to "just do it quickly" before approval. | Agent stops unless an explicit unattended exception exists for that exact action. |
| Platform mismatch | Windows host has WSL/Git Bash problems. | Agent uses native or Python-core path and avoids shell chaining. |
| Attachment/publication | User pastes image or file path for a remote issue/comment. | Agent keeps issue/comment images local, uses approved non-image attachment flow only when allowed, and never publishes local paths. |
| Tool contract gap | Skill mentions a command that help/parser does not support. | Test fails until docs or tool are corrected. |
| Empty repository | User gives only a repository URL or empty repo. | Agent can discover how to obtain skill/devctl without a pasted long prompt. |
| Branch/MR separation | User approves push but not MR. | Agent pushes only if allowed and does not create PR/MR. |

## Scoring Template

```text
Skill:
Version / commit:
Evaluator:
Date:

Numeric score:
Hard fail gates triggered:

Dimension scores:
- Trigger And Discovery: /8
- Scope And Non-Use Boundaries: /6
- Precedence And Conflict Resolution: /8
- Phase And Human Gates: /10
- Actionability And Recipes: /10
- Tool Contract Consistency: /9
- State, Idempotency, And Failure Recovery: /9
- Platform And Environment Robustness: /8
- Data, Secret, And Publication Safety: /8
- Project Override Compliance: /7
- Verification And Pressure Testing: /10
- Evidence Reviewability: /5
- Context Economy And Maintainability: /2

Evidence:
- Files:
- Commands:
- Pressure scenarios:

Top fixes:
1.
2.
3.
```

## XFlow-Specific Notes

For XFlow, apply the generic matrix plus these required checks:

- Empty repositories must discover how to obtain XFlow and devctl without a
  pasted long prompt.
- Project-bound source/ref/local tool settings are the runtime source of truth.
- Issue, comment, attachment, branch, push, MR/PR, conflict, close, and cleanup
  actions must follow the state machine and human gates.
- `devctl` and `devctl.ps1` are the supported workflow entrypoints. Normal
  Windows operations must use Python core, not WSL.
- `devctl git push` and `devctl git mr` are separate conceptual gates even if a
  future tool implementation changes.
- Remote issue/comment/MR bodies must not publish local attachment paths or
  unresolved `xflow-attachment://` placeholders.
- Remote issue/comment bodies must not use GitHub release assets as an image
  store; image attachments remain local unless an approved object storage
  backend such as `aliyun-oss` has published reviewed public URLs.
- Large-issue subtasks must use `subtask-001` style local directories, include
  checked README files, and keep subtask evidence under each subtask's
  `evidence/` directory in the repository rather than COS/OSS.
- `.xflow/issues/` is tracked by default. `issueWorkspace.mode: local` requires
  an explicit project rule; active approval files, `.xflow/local/`, and
  `.xflow/runtime/` remain ignored.
- Canonical state is `.xflow/issues/issue-<id>/task-state.md`; one worktree may
  activate only one remote Issue, and legacy `.xflow/current-task.md` is
  migration compatibility only.
- Issue-local evidence must not be uploaded to COS/OSS/object storage or HTTP
  URLs. Reviewed remote-body publication artifacts belong only in
  `.xflow/publish/issues/`.
