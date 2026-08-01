# Capability Contract Method

Use this method when an Issue may change a participant-visible capability. The
contract is a design artifact for downstream AI; it is not an implementation
plan, an API sketch, or a substitute for review.

## Trigger Matrix

| Signal | Route | First artifact |
| --- | --- | --- |
| New participant-visible outcome, boundary, value, or failure meaning | `capability-change` | `contract-change-proposal.md` then contract YAML |
| Existing contract is found and implementation fails to honor it | `implementation-gap` | `gap-analysis.md` |
| Existing contract is found and only presentation is wrong | `ui-defect` | `issue-draft.md` |
| Shared runtime, platform, or independently owned prerequisite | `infrastructure` | `dependency-issue-proposal.md` |
| Policy/process concern | `governance` | `issue-draft.md` |
| Deliberately deferred capability | `future` | `futureCapabilitiesOutOfScope` or `future-task-proposal.md` |

Lightweight route: capture the original request, search contracts, write
`.xflow/issues/issue-<id>/classification.yaml`, run
`devctl check classification --issue <id>`, then create only the route's next
artifact. Do not turn a known implementation gap into a new capability merely
because the fix is difficult.

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

Linting proves only structure. A design enters `accepted-design` only after the
human accepts exact contract objects through the contract-acceptance workflow
and the matching tracked acceptance record is retained in the Issue workspace.
See `contract-authoring.md` and `traceability.md` before entering development.
