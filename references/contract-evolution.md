# Contract Evolution

Do not edit an accepted contract in place without classifying the semantic
effect and obtaining fresh acceptance for the changed objects.

## Version Decision

- `PATCH`: correct a non-semantic typo, explanatory `note`, or equivalent
  wording that changes no participant-visible meaning, constraint, context,
  interaction, verification outcome, failure preservation, or trace target.
- `MINOR`: add a backward-compatible participant-visible capability, optional
  value, interaction, verification, projection, dependency, precondition, or
  future declaration without changing the meaning of existing objects.
- `MAJOR`: remove, narrow, reinterpret, rename, or otherwise make an existing
  participant-visible meaning, constraint, failure preservation, role boundary,
  interaction, verification expectation, or required dependency incompatible.

Use `supersedes` when an old object is replaced. Keep old IDs stable when their
meaning is unchanged; create new IDs when the meaning is not the same. The
root contract version expresses the aggregate change, while each changed or new
object carries its own version.

## Mechanical Review

```text
devctl contract lint --file <new.yaml>
devctl contract diff --old <old.yaml> --new <new.yaml>
```

The diff informs the human decision; it does not authorize it. Update the
classification and task state when a change is a `capability-change`, then run
the exact contract-acceptance recipe from `contract-authoring.md`. A changed
digest or object list makes the previous acceptance record invalid for the new
contract.

## Reopen Rather Than Erase

If implementation evidence reveals that the design is wrong, return to
`declaring`, revise the contract, create the new exact tracked acceptance
record, then progress again. Do not relabel an implementation gap as a contract
change merely to avoid gap analysis; if the contract remains correct, retain
it and route to `implementation-gap`.
