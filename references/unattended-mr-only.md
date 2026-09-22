# MR-only unattended mode

This is the authoritative policy for new Task-Scoped Unattended Mode sessions
(`approvalPolicy: mr-only-v1`). It changes approval scheduling, not task scope
or execution permissions. Unattended sections elsewhere that describe a
remote-write-only mode are legacy compatibility rules, not additional gates
for this policy. Manual mode retains its existing human gates.

## One authorization, one review point

Enable only from the user's explicit current-message safety word
`XFLOW_HUMAN_UNATTENDED_ALL`, through the repository-local tool.
Record the repository, worktree, task scope and intended integration target.
No AI-generated safety word, forged human identity or editing Approved to yes.

Once enabled, perform ordinary in-scope work without approval files or repeated
"continue" prompts: issue create/comment, branch start, contract acceptance,
gap recognition, development start, test/rework, artifact and implementation
commits, target synchronization, push, MR creation and metadata updates.
Prepare and check the same artifacts as manual mode. Accepting a design under
delegated authority is NOT a human review: record `source: unattended`,
policy version, authorization lineage, exact object IDs and content hashes.
Do not fabricate a `source: local-review` record or bypass a failing check.

The single human review point is **the published MR/PR before merge**.
Creating the MR is automatic; do not ask for a local "approve MR creation"
file first. Show the MR link, delivered scope, verification and remaining
risks. Stop there. Never approve one's own MR or infer approval from silence,
CI success, an earlier contract decision, or the initial safety word.
The human's MR decision must bind the current head and target; a changed head
requires fresh review. This is the same review point, not an extra workflow gate.
Provider branch protections and required checks still apply. A remote review
does not by itself request the agent to merge; merge only if already included
in the explicit delivery scope or separately requested. Otherwise leave it for
the human to merge.

## Transition rules

The machine-readable [policy matrix](unattended-mr-only-policy.json) lists
covered actions and lifecycle transitions for compatibility tests. It is a
specification, not a replacement runtime or a grant for the current session.

- draft → confirmed Issue: atomically migrate authorization to the returned
  remote ID, preserving source scope and provenance; do not ask to enable again.
- Issue → approved-shape final branch: bind the exact target branch/base and
  keep authorization. `git start` must not unconditionally disable this mode.
- classified → accepted-design/gap-recognized → implementation: automated
  artifact validation plus delegated semantic decision; no local-review wait.
  A verification matrix still precedes projection and implementation.
- implementation → verified → pushed → MR-open: automatic after checks.
- MR-open → merged: only after the human MR decision described above.
- merged → closed/cleaned: ordinary in-scope Issue closure and safe cleanup
  need no new approval. Use non-forced deletion only for this task's fully
  merged branch/worktree, with no uncommitted data. If unsafe, retain it and
  report; never discard local residuals or use force to finish cleanup.
- explicit disable, cancellation or completed safe cleanup retires authorization.
  Unrelated task/repository/worktree switches are NOT migrations and fail closed.

Record immutable provenance for semantic transitions so audit can distinguish
human-reviewed design from agent decisions made under user-delegated authority.
Retain current-task, branch/base identity, artifact integrity, exact evidence,
test, attachment and sensitive-data checks. Do not flatten accepted-design to
"skip contract"; do not confuse a prototype with product integration.

## Scope and failure boundaries

No expansion to unrelated work, secret/permission changes, force push, history
rewrite, destructive deletion or automatic conflict resolutions that may lose
user changes. These actions are outside the authorization, not routine extra
approval gates. Choose a safe alternative or stop with a concrete blocker.
A material product-scope ambiguity also warrants a question, not a fabricated
requirement. "Only MR approval" does not mean inventing missing authority.

An independently owned dependency never inherits a parent's token silently.
An explicitly authorized multi-repository task may register each named child
with its own repository/worktree identity and recorded scope under the original
authorization; no repeated approvals for already-scoped children. Newly
discovered shared infrastructure outside that scope is deferred/reported, not
implemented using the parent token. Before integration, require real evidence.

Unknown remote outcomes are reconciled against authoritative remote state,
without blindly repeating writes or inventing success. If the installed tool
cannot safely reconcile automatically, stop with the exact blocker, not a
fabricated receipt.

## Runtime compatibility and rollout

Skill text cannot grant capabilities an installed devctl does not implement.
Before advertising MR-only behavior, verify that the tool reports support for
`mr-only-v1`, delegated semantic records, atomic draft/Issue/branch migration,
and the human MR barrier. Do not invent a CLI flag or silently downgrade to
legacy mode. If unsupported, report the tool dependency once; do not lead the
user through repeated approval files while calling that "unattended".

Required devctl changes:
1. Version the authorization state; legacy states must not silently acquire
   broader privileges. Offer an explicit user-authorized migration.
2. Replace per-step approval requirements with a policy resolver for covered
   actions; preserve all non-approval checks.
3. Allow source=unattended for task-branch-start, contract acceptance and gap
   recognition records with exact byte/object binding; preserve human-only
   semantics in manual mode and validate provenance on replay.
4. Preserve authorized lineage at Issue creation and branch activation.
5. Allow MR creation, but exclude MR review/approval and unchecked merge.
   Enforce approved current head/target and branch protection before merge.
6. Allow safe post-merge closure/cleanup, never forced deletion or data discard.
7. Update generated repository adapters and regression tests together. A new
   SKILL.md with old hard-coded generated AGENTS rules is not a complete rollout.

The current change defines skill policy; it does not claim an older runtime
implements this protocol. Do not edit downstream runtime authority or consume
old approvals to simulate support.
