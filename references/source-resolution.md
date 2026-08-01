# XFlow Source Resolution

Use this when deciding which XFlow Skill or devctl version controls a repository.

## Default Sources

- XFlow Skill: `git@github.com:Linkk2000/xflow-skills.git`
- devctl: `git@github.com:Linkk2000/xflow-devctl.git`
- Default ref: `main`

Project-local `.xflow/ops/` tools are the runtime source of truth. New and
restored projects should bind XFlow under the repository, normally:

- `.xflow/ops/devctl`
- `.xflow/ops/workflow`

The preferred project-local binding mode is `local-ignored-vendor`: clone or
copy the tool repositories under `.xflow/ops/` and ignore those directories in
the parent repository. Explicit submodules are allowed only when the project
chooses that mode.

## Priority

Apply sources in this order:

1. Current user instruction for this task.
2. Project `.xflow/xflow.json` source/ref/mode/path.
3. Project-local tools under `.xflow/ops/`.
4. Project `AGENTS.md`.
5. Repository-local wrappers such as `devctl.ps1`, `devctl`, and `.xflow/devctl`.
6. Agent defaults.

There is no global XFlow fallback. If project bindings are missing, initialize
or restore them into `.xflow/ops/` inside the project. Do not read an installed
global Skill or a user-level devctl from PATH to decide a repository workflow.

## Project Binding Schema

Recommended `.xflow/xflow.json` shape:

```json
{
  "version": 1,
  "issueWorkspace": {
    "mode": "tracked"
  },
  "contracts": {
    "root": "docs/requirements"
  },
  "skill": {
    "source": "git@github.com:Linkk2000/xflow-skills.git",
    "ref": "main",
    "mode": "local-ignored-vendor",
    "path": ".xflow/ops/workflow"
  },
  "devctl": {
    "source": "git@github.com:Linkk2000/xflow-devctl.git",
    "ref": "main",
    "mode": "local-ignored-vendor",
    "path": ".xflow/ops/devctl"
  },
  "humanGated": true
}
```

## Rules

- Ask before choosing a non-default ref during first bootstrap.
- Do not switch Skill/devctl branches, tags, commits, local vendor checkouts, or submodules after bootstrap without explicit human approval.
- Initializing XFlow authorizes local bootstrap work only. It does not authorize issue creation, branch creation, commit, push, MR/PR, merge, issue close, or branch cleanup.
- If `.xflow/xflow.json` and `.xflow/ops/` disagree, stop and ask the user which binding is authoritative.
- For an existing repository with `.xflow/xflow.json`, restore the recorded project binding. Do not fall back to globally installed Skill/devctl.
- `issueWorkspace.mode` defaults to `tracked` when absent. An explicit
  `issueWorkspace.mode: local` is allowed only when project rules explain the
  exception; tools must not silently change tracked mode to local.
