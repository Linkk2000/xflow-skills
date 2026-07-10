# XFlow Bootstrap Policy

Use this when the target repository is empty or does not contain project-level XFlow files.

## Canonical Sources

- XFlow Skill source: `git@github.com:Linkk2000/xflow-skills.git`
- devctl source: `git@github.com:Linkk2000/xflow-devctl.git`

Local ignored vendor mode is the default. Bootstrap should bind XFlow inside
the target repository under `.xflow/ops/` rather than relying on a user-level
installed skill or PATH devctl.

If the network source is unavailable and no project-bound copy exists, stop and
ask the user where to obtain XFlow. Do not silently use a global installed
Skill or global devctl entrypoint.

## Natural Language Entry

The user should not need to paste shell commands for normal bootstrap. Treat these as valid bootstrap requests:

- "Initialize the current directory as an XFlow project."
- "Initialize this repository as an XFlow project: <repo-url>"
- "Initialize XFlow. Use stable for devctl and main for skill."

The agent executes the required local commands. Do not answer by making the user run command sequences manually unless execution is impossible in the current environment.

## Source Strategy Gate

Before first-time bootstrap, ask the user to choose the XFlow source strategy when it is not already clear:

1. Project-local ignored vendor checkouts under `.xflow/ops/` on main branch.
2. Project-local ignored vendor checkouts on a specific branch for skill and/or devctl.
3. Explicit project submodules pinned to a specific branch, tag, or commit.

The project default is `local-ignored-vendor` mode on the main branch. A
project may record source, ref, mode, and path in `.xflow/xflow.json`; that
project binding is the authority for future restore.

## Bootstrap Trigger

Enter bootstrap before development when any of these are missing:

- `AGENTS.md`
- `devctl.ps1` on Windows or `devctl` on POSIX
- `.cursor/rules/xflow-workflow.mdc`, `CLAUDE.md`, `GEMINI.md`, or `.agents/*` adapters when the user expects cross-agent use

If `.xflow/xflow.json` already exists, use restore instead of bootstrap.

## Bootstrap Command

Preferred:

```text
devctl init --target <repo>
```

Windows:

```powershell
.\devctl.ps1 init --target <repo>
```

POSIX:

```bash
./devctl init --target <repo>
```

The command must be idempotent. It may add or refresh XFlow-managed files, but it must not create issues, create branches, push, create MR/PRs, close issues, delete branches, or resolve conflicts.

## Expected Result

After bootstrap, the project should contain:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.cursor/rules/xflow-workflow.mdc`
- `.agents/agents.md`
- `.agents/skills/xflow-workflow.md`
- `.agents/workflows/xflow-start.md`
- `.xflow/xflow.json`
- `.xflow/config.env.example`
- local `devctl.ps1` and `devctl` entrypoints

The project should also contain:

- `.xflow/ops/devctl`
- `.xflow/ops/workflow`
- `.gitignore` entries for `.xflow/ops/devctl/`, `.xflow/ops/workflow/`, and
  `.xflow/local/`

The agent is responsible for cloning or refreshing those project-local tool
directories during bootstrap. Do not ask the user to run the Git commands
manually unless the current environment cannot execute Git commands.

## Post-Bootstrap Stop

After bootstrap:

1. Run local checks such as `devctl doctor` and `devctl check encoding` when available.
2. Summarize the files created or skipped.
3. Stop and ask the user to review the bootstrap result.

Do not proceed to issue drafting or development until the user explicitly approves the next phase.
