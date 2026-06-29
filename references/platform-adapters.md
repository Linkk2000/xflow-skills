# Platform Adapters

## Windows

- Use `devctl.ps1`.
- `devctl.ps1` routes normal XFlow commands to Python core.
- Validate with Python commands such as `python tests/python-core.py` and
  `python tests/entrypoint-routing.py`.
- Use UTF-8 without BOM for generated Markdown and scripts.
- Avoid WSL for XFlow commands.
- Avoid `wsl --exec bash -lc` for XFlow commands.
- Avoid bare `bash` or Git Bash for normal XFlow validation on Windows.
- Avoid long quoted one-liners across shells.

## POSIX

- Use `devctl`.
- Run `bash -n` only for changed POSIX shell compatibility scripts, and only
  when an explicit POSIX shell is selected outside Windows.
- Prefer LF line endings.

## Cross-Platform Rule

When a command fails because of quoting, encoding, path, or shell parsing, classify it as an environment failure first. Do not repeat a remote write until remote state has been read.
