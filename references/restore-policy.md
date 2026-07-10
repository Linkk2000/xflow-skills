# XFlow Restore Policy

Use this when a repository already contains XFlow configuration and the user is setting up a new machine, recloned workspace, or missing local devctl wrappers.

## Trigger

Enter restore instead of init when any of these are true:

- `.xflow/xflow.json` exists.
- The user says they changed computers or recloned a repository.
- `AGENTS.md` exists but local `devctl.ps1`, `devctl`, or `.xflow/devctl` is missing.
- `.xflow/ops/devctl` or `.xflow/ops/workflow` is missing or incomplete.

## Authority

Read `.xflow/xflow.json` first. Existing project binding is authoritative.
Do not fall back to a global installed skill, a user-level devctl on PATH, or
any user-level tool checkout when restoring a project.

Do not ask the source strategy gate again unless:

- `.xflow/xflow.json` is missing or invalid.
- `.xflow/xflow.json` conflicts with the actual `.xflow/ops/` layout.
- The recorded source, ref, or path cannot be accessed.
- The user explicitly asks to change the XFlow version.

## Restore Flow

The agent should execute the required local commands:

1. Read `.xflow/xflow.json`.
2. If mode is `local-ignored-vendor`, clone or refresh the recorded sources
   under `.xflow/ops/` without overwriting local modifications.
3. If mode is `submodule`, validate or run `git submodule update --init --recursive`.
4. If an old repository records mode `cache`, ask the user whether to migrate
   to project-local `.xflow/ops/` before continuing. Do not silently use the
   cache path.
5. Restore `.xflow/devctl` from the project-bound devctl source.
6. Restore root `devctl.ps1` and `devctl` wrappers if missing.
7. Run local checks such as `devctl doctor` and `devctl check encoding` when available.
8. Write or summarize a restore report.
9. Stop for human review.

## Boundaries

Restore is local setup only. It may read Git metadata, clone project-local tool
repositories under `.xflow/ops/`, initialize explicitly configured submodules,
and write local workflow files. It must not create issues, create feature
branches, commit, push, create MR/PRs, merge, close issues, delete branches, or
resolve conflicts without the later human gate for that exact action.
