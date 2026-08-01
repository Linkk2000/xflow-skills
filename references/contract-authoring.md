# Contract Authoring

## Start With Meaning

先回答能力问题，再填写 YAML。 Use the discovery answers as the source of
truth, not an implementation's current classes or endpoints. Author in this
order: `purpose → constraints → context → roles → values → failures →
interactions → verification → projections → dependencies → preconditions →
futureCapabilitiesOutOfScope → references`.

## Field Semantics

- Root `id`, `version`, `name`, `status`, `created`, and `note` identify the
  contract; `note` is non-normative background.
- `capabilityContract` states one purpose, participants, inputs, outputs, and
  constraints. A constraint is a rule that must survive every traced path.
- `semanticValueContracts` define the meanings participants may depend on;
  `failureReasonContracts` name stable failures and what each preserves.
- `context` sets entry/completion conditions and responsibilities.
  `contextRoles` declare the responsibility and `doesNotOwn` boundary for each
  role in that context.
- Each `interactionContracts` item joins context, participants, accepted
  values, produced values, constraints, and explicit failure expectations.
- Every `verificationMatrix` item traces interaction/constraint IDs and has
  `given`, `when`, `then`, and one or more `verifyBy` targets.
- `engineeringProjections` describe authority and derived representations;
  they cannot add business semantics. `dependsOn` names external contracts and
  owning repositories. `preconditionsToResolve` records `open|deferred|resolved`
  questions with `accepted-design|engineering-projection|implementation|never`.
- `futureCapabilitiesOutOfScope` is an explicit non-commitment. `references`
  retain source links such as an Issue or decision record.

## Stable IDs And Versions

Use meaningful, stable dotted IDs such as `billing.interaction.submit-payment`.
Never reuse an ID for a different meaning. Every root and contract object uses
`MAJOR.MINOR.PATCH` versioning. Preserve a replaced object's identity in its
`supersedes` list. Raise the object version with its semantic change and the
root contract version with the released aggregate change; apply the exact
PATCH/MINOR/MAJOR rules in `contract-evolution.md`.

## Human Acceptance Is A Gate

Contract acceptance starts only after the remote Issue ID exists, safe draft
artifacts have moved to `.xflow/issues/issue-<id>/`, canonical task state exists,
and that Issue is active in the current worktree. Before Issue creation, a
candidate may be reviewed under `.xflow/issues/issue-draft/`, but there is no
pre-Issue contract-acceptance command and AI must not implement it.

Materialize the exact candidate under the configured contract root, then run:

```text
devctl task activate --issue <id>
devctl check classification --issue <id>
devctl contract lint --file <contract.yaml>
devctl approval prepare --issue <id> --action contract-acceptance --file <contract.yaml> --objects <approved-id-list>
devctl contract accept --issue <id> --file <contract.yaml> --objects <approved-id-list>
```

Issue-create approval does not satisfy this recipe. A successful acceptance
binds `accepted-design`; it does not approve entering development. Obtain the
separate development-start approval before branch creation or implementation.

Human Approval Is Non-Delegable. AI may prepare the file, object list,
evidence, and command draft, but it must never satisfy the gate or edit
`Approved: no` to `Approved: yes`.

YAML `status: accepted-design` alone is not approval. The gate closes only
when task state references an exact tracked acceptance record under
`.xflow/issues/issue-<id>/approvals/history/`. That record must bind the
repository, worktree/recorded branch, Issue, approved file, contract ID and
version, both SHA-256 values, `semanticDecision: accepted-design`,
`source: local-review`, `action: contract-acceptance`, and normalized existing
`acceptedObjects`. Any mismatch, stale digest, missing object, or changed
branch fails closed. `Human Approval Ref` is required at `accepted-design` and
later; reopening a contract requires a new exact acceptance record, never an
edited historical approval.

## Anti-Patterns

- Starting with endpoint names or database tables instead of a participant outcome.
- Calling a schema-valid file accepted because `status: accepted-design` is set.
- Hiding a rejection behind a generic error instead of naming its preserved state.
- Letting a projection invent a new invariant not present in the contract.
- Reusing an ID for a changed meaning, or silently changing a contract after approval.
- Writing vague verification such as "tests pass" instead of a traceable observation.

## Complete Interaction And Verification Example

For a user operation, declare `example.interaction.perform-operation` in
`example.context.operation`: role `example.role.operator` accepts
`example.value.request`, produces `example.value.result`, and is constrained
by `example.constraint.preserve-state-on-rejection`. Its failure expectation
is `example.failure-reason.invalid-state`, preserving the existing business
state. Verify success with a Given legal prior state, When the participant
requests the operation, Then an observable result exists; verify rejection
with a Given illegal prior state, When the same request is made, Then the
stable failure reason is returned and the existing state is unchanged. Each
verification traces the exact interaction and, for rejection, the constraint.
