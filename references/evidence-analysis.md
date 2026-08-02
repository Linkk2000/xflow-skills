# Evidence-Backed Gap Analysis And Completion Verification

Use this reference for a reported defect, UX/UI discrepancy, design comparison,
behavioral gap, or claimed completion. In XFlow, a code diff or an AI statement
does not prove a finding or a result. The human reviewer must be able to open
the cited local artifacts and judge each conclusion directly.

`gap-analysis.md` is the XFlow difference-analysis file. It may also be called
the gap-analysis file or problem/gap-analysis file in a user's request.

## Evidence Rules

1. Create one direct evidence bundle per finding or acceptance criterion. Do
   not make the reviewer infer which global screenshot, log, or source snippet
   supports which claim.
2. Separate observation from analysis. Record what was observed first; mark a
   root cause as proven, supported, or unknown rather than presenting a guess
   as fact.
3. Store issue-level artifacts under
   `.xflow/issues/issue-<id>/evidence/` (or `issue-draft/evidence/`). Store
   subtask artifacts only under that subtask's `evidence/` directory. Use
   relative Markdown links. Do not move Issue-local evidence to COS/OSS/object storage or HTTP URLs.
4. For UI evidence, when a browser is available, include both a live screenshot
   under `evidence/screenshots/` and a DOM observation under `evidence/dom/`.
   Record the target URL and visible state. A prototype or source file may
   describe the target, but does not prove the live behavior.
5. For non-UI evidence, include the most direct local artifact: focused test
   output, command output, API response, log, fixture, or source reference.
   State how the reviewer can interpret it.
6. After implementation, collect fresh post-change evidence. Do not reuse a
   pre-change artifact or claim closure from changed code alone.

## UI Environment Identity

Every UI finding and completion bundle must bind all of these values:

- product URL and page identity
- model identity or exact data/fixture identity
- repository commit, branch, and worktree
- browser, viewport, and capture time
- screenshot path and DOM or runtime-state path

The screenshot and DOM/runtime-state artifact must describe the same page and
model identity. A localhost page from another worktree, a design prototype, or
an unbound screenshot is not product evidence. Store the identity record next
to the Issue-local evidence and use repository-relative links.

## Product Integration Evidence Bundle

Before claiming real product-page or integration verification, store these exact
files under the current Issue's evidence directory: `product-url.txt`,
`page-identity.txt`, `model-identity.txt`, `screenshot.png`, and
`dom-runtime-state.json`. They must be bound to the same real product-page
capture, made only after an explicitly navigated real product URL. A capture
from `about:blank, prototype, or test harness` is not product evidence and
must not claim integration passed.

## Approval Binding Check

On a cross-worktree, cross-Issue, or cross-branch request, or when an approval
is old or its binding is inconsistent, use the governance route and create
`.xflow/issues/issue-<current>/approval-binding-check.md`. This is evidence,
not approval. It records Repository, Worktree, Branch, Current Issue, Exact
Action, Reviewed File Relative Path, SHA256, Candidate Approval Provenance,
Binding Verdict, and Required Next Human Gate. The check must not reuse an old
approval or push; stop until the Required Next Human Gate is satisfied.

## Gap-Analysis Finding Bundle

Each `gap-analysis.md` must have `## Evidence-Backed Findings` with one or
more numbered bundles in this exact shape:

```markdown
### Finding F-001: <short observable discrepancy>

#### Finding Type
ui|non-ui

#### Observation
<what was directly observed and how it was reproduced>

#### User Impact
<why the discrepancy matters>

#### Evidence
- [focused command output](evidence/logs/f-001-before.txt)

#### Analysis
<proven cause, supported hypothesis, or explicit unknown>

#### Proposed Change
<smallest change that addresses the finding>

#### Acceptance
- [ ] <observable condition that will prove this finding addressed>

#### Human Review
- [ ] Confirm the observation, evidence, and proposed change.
```

For `ui`, the `#### Evidence` list must include both an artifact under
`evidence/screenshots/` and one under `evidence/dom/`. For `non-ui`, replace
them with the applicable local artifacts. `devctl check gap-analysis` rejects
missing fields, remote evidence, evidence outside `evidence/`, and UI bundles
that omit either required artifact class.

## Completion Verification Bundle

Each `resolution-report.md` must have `## Completion Verification` with one or
more numbered bundles. It is a fresh, reviewer-facing proof of an acceptance
criterion, not a restatement of the implementation.

```markdown
### Criterion C-001: <acceptance criterion being verified>

#### Verification Type
ui|non-ui

#### Expected Result
<the observable result that would satisfy the criterion>

#### Evidence
- [focused post-change output](evidence/logs/c-001-after.txt)

#### Actual Result
<what the linked evidence shows>

#### Human Review
- [ ] Confirm the evidence supports this result.
```

For `ui`, include both `evidence/screenshots/` and `evidence/dom/` artifacts.
For `non-ui`, link the relevant test, command, API, log, fixture, or source
artifact. If an expected verification cannot run, state it in `Actual Result`,
do not claim `resolved`, and use `reduced` or `blocked` as appropriate.

## Reviewability Checklist

- Each finding or criterion has a direct local evidence bundle.
- Every link opens a file under the correct local `evidence/` directory.
- Evidence identifies the before/after state and the claimed result.
- UI artifacts show a real navigated page, not `about:blank` or a prototype
  presented as live behavior.
- UI artifacts bind the same product URL, page identity, model identity,
  commit, branch, worktree, browser, viewport, and capture time.
- The report distinguishes verified facts from hypotheses and remaining risks.
- A human-review checkbox asks for a concrete judgment, rather than merely
  declaring that the AI tested the work.
