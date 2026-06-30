# XFlow Restore Policy

Use this when a repository already contains XFlow configuration and the user is setting up a new machine, recloned workspace, or missing local devctl wrappers.

## Trigger

Enter restore instead of init when any of these are true:

- `.xflow/xflow.json` exists.
- The user says they changed computers or recloned a repository.
- `AGENTS.md` exists but local `devctl.ps1`, `devctl`, or `.xflow/devctl` is missing.
- `.gitmodules` contains `.xflow/sources/xflow-skills` or `.xflow/sources/xflow-devctl`.

## Authority

Read `.xflow/xflow.json` first. Existing project binding is authoritative.
Do not fall back to a global installed skill, a user-level devctl on PATH, or a
developer checkout under `~/.codex/xflow/repos` when restoring a project.

Do not ask the source strategy gate again unless:

- `.xflow/xflow.json` is missing or invalid.
- `.xflow/xflow.json` conflicts with `.gitmodules`.
- The recorded source, ref, or path cannot be accessed.
- The user explicitly asks to change the XFlow version.

## Restore Flow

The agent should execute the required local commands:

1. Read `.xflow/xflow.json`.
2. If mode is `submodule`, validate or run `git submodule update --init --recursive`.
3. If an old repository records mode `cache`, ask the user whether to migrate
   to project submodules before continuing. Do not silently use the cache path.
4. Restore `.xflow/devctl` from the project-bound devctl source.
5. Restore root `devctl.ps1` and `devctl` wrappers if missing.
6. Run local checks such as `devctl doctor` and `devctl check encoding` when available.
7. Write or summarize a restore report.
8. Stop for human review.

## Boundaries

Restore is local setup only. It may read Git metadata, clone source caches, initialize submodules, and write local workflow files. It must not create issues, create feature branches, commit, push, create MR/PRs, merge, close issues, delete branches, or resolve conflicts without the later human gate for that exact action.
