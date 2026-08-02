# Capability Contract Method

Use this method when an Issue may change a participant-visible capability. The
contract is a design artifact for downstream AI; it is not an implementation
plan, an API sketch, or a substitute for review.

## Trigger Matrix

| Signal | Route | First artifact |
| --- | --- | --- |
| New participant-visible outcome, boundary, value, or failure meaning | `capability-change` | `contract-change-proposal.md` then contract YAML |
| Existing contract is found and implementation fails to honor it | `implementation-gap` | `gap-analysis.md` |
| Only presentation is wrong, with found or not-found contract evidence | `ui-defect` | `lightweight-route-complete` terminal sentinel |
| Shared runtime, platform, or independently owned prerequisite | `infrastructure` | `dependency-issue-proposal.md` |
| Policy/process concern | `governance` | `issue-draft.md` |
| Deliberately deferred capability | `future` | `futureCapabilitiesOutOfScope` or `future-task-proposal.md` |

For `implementation-gap`, AI may prepare analysis and an approval draft but
cannot recognize its own gap. Only exact human action `gap-recognition`,
consumed into an immutable non-reusable record bound to the analysis bytes,
authorizes `gap-recognized`; contract acceptance and unattended mode do not.

Lightweight pre-Issue route: capture the original request, search contracts,
write `.xflow/issues/issue-draft/classification.yaml`, run
`devctl check classification --issue draft`, then create only the route's next
draft artifact under `.xflow/issues/issue-draft/`. For a capability change,
prepare the candidate contract and verification matrix there, but do not run
contract acceptance and do not edit implementation code. Do not turn a known
implementation gap into a new capability merely because the fix is difficult.

After the separately approved remote Issue is created, migrate the safe draft
artifacts to `.xflow/issues/issue-<id>/`, create canonical task state, and run
`devctl task activate --issue <id>`. Only then may an exact contract under the
configured contract root enter the contract-acceptance workflow.

## Discovery Questions

Ask one question, record its answer, then ask the next unresolved question.

1. Which participant gains or loses a dependable outcome?
2. What purpose does that participant rely on, without naming a technical solution?
3. What request/value enters the interaction?
4. What observable value or stable refusal must leave it?
5. Which state, permission, ordering, or safety rule must remain true?
6. In what context is the interaction allowed to begin and complete?
7. Which role owns the decision, and what explicitly does that role not own?
8. Which failure reasons are distinguishable, and what does each preserve?
9. What Given/When/Then observation can prove success and rejection?
10. Which dependency, unanswered precondition, or future capability is outside this commitment?

## One Decision At A Time

Do not ask a stakeholder to approve a large YAML blob. First settle the
participant-visible purpose. Then settle constraints and failure preservation.
Then settle context and role boundaries. Then settle interactions and their
verification. Finally decide projections, dependencies, preconditions, and
out-of-scope work. Record uncertainty as a precondition with its exact
`requiredBefore` value; do not invent a decision to make the file look complete.

## Method Exit

Linting proves only structure. Issue-create approval creates identity only; it
does not accept a contract. A design enters `accepted-design` only after the
remote Issue exists and the human accepts exact contract objects through the
contract-acceptance workflow, with the matching tracked acceptance record
retained in the Issue workspace. Contract acceptance does not approve entering
development; that remains a later exact human gate.
See `contract-authoring.md`, `scope-routing.md`, and `traceability.md` before
entering development.
