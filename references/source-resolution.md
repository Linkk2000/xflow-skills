# XFlow Source Resolution

Use this when deciding which XFlow Skill or devctl version controls a repository.

## Default Sources

- XFlow Skill: `https://github.com/Linkk2000/xflow-skills`
- devctl: `https://github.com/Linkk2000/xflow-devctl`
- Default ref: `main`
- Default cache on Windows: `%USERPROFILE%\.xflow\sources\`
- Default cache on POSIX: `~/.xflow/sources/`

## Priority

Apply sources in this order:

1. Current user instruction for this task.
2. Project `.xflow/xflow.json` source/ref/mode/path.
3. Project `AGENTS.md`.
4. Project-bound git submodules under `.xflow/sources/`.
5. Default local cache under the user's home directory.
6. Globally installed Skill/devctl.
7. Agent defaults.

Global XFlow is only a fallback. If a project explicitly records or vendors XFlow sources, the agent must use the project-bound version unless the user explicitly overrides it.

## Project Binding Schema

Recommended `.xflow/xflow.json` shape:

```json
{
  "version": 1,
  "skill": {
    "source": "https://github.com/Linkk2000/xflow-skills",
    "ref": "main",
    "mode": "cache",
    "path": "~/.xflow/sources/xflow-skills"
  },
  "devctl": {
    "source": "https://github.com/Linkk2000/xflow-devctl",
    "ref": "main",
    "mode": "cache",
    "path": "~/.xflow/sources/xflow-devctl"
  },
  "humanGated": true
}
```

For submodule mode, use:

```json
{
  "skill": {
    "mode": "submodule",
    "path": ".xflow/sources/xflow-skills"
  },
  "devctl": {
    "mode": "submodule",
    "path": ".xflow/sources/xflow-devctl"
  }
}
```

## Rules

- Ask before choosing a non-default ref during first bootstrap.
- Do not switch Skill/devctl branches, tags, commits, or submodules after bootstrap without explicit human approval.
- Initializing XFlow authorizes local bootstrap work only. It does not authorize issue creation, branch creation, commit, push, MR/PR, merge, issue close, or branch cleanup.
- If `.xflow/xflow.json` and a submodule disagree, stop and ask the user which binding is authoritative.
- For an existing repository with `.xflow/xflow.json`, restore the recorded binding before considering global defaults.
