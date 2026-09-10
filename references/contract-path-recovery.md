# Recover a pre-design contract path binding

Use only when an older task sealed the candidate path instead of its formal
`contracts.root` path. Requires a devctl runtime with the commands below.
If unavailable, stop and request the runtime update; do not hand-edit runtime
authority or use activation as a bypass.

1. Verify the active Issue, repository, worktree and final branch. Recovery is
   limited to capability-change, S2/S3, classified/declaring, without design
   acceptance history or pending acceptance claims. It is not a contract change.
2. Materialize identical candidate bytes at the intended formal path. Keep the
   source. ID, version, content and configuration must remain unchanged.
3. Prepare the exact request:

   ```text
   devctl task prepare-contract-relocation --issue <id> --to <contract-root>/<capability>/contract.yaml
   ```

4. Stop for the human to review `contract-relocation.json` and the prepared
   approval. Only the human may approve action `task-contract-relocate`.
   This is never unattended and grants neither design acceptance nor development.
5. Execute:

   ```text
   devctl task relocate-contract --issue <id> --file .xflow/issues/issue-<id>/contract-relocation.json
   devctl task status
   devctl check classification --issue <id>
   ```

The correction preserves source/destination files and original approvals. It
archives exact request/review and before images under
`approvals/history/contract-relocations/`, and records consumption separately.
After interruption, retry the same execution command with the same request;
do not prepare a replacement or delete authority, snapshots or active pointers.
Unrelated state changes fail closed and require investigation.

Commit the trackable correction evidence and updated task-state promptly as an
artifacts-only commit. Resume ordinary contract acceptance separately. Remote
writes and development still require their own gates.
