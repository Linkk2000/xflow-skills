# Platform Adapters

## Windows

- Use `devctl.ps1`.
- Use UTF-8 without BOM for generated Markdown and scripts.
- Avoid WSL for XFlow commands.
- Avoid `wsl --exec bash -lc` for XFlow commands.
- Avoid long quoted one-liners across shells.

## POSIX

- Use `devctl`.
- Run `bash -n` on changed shell scripts before execution.
- Prefer LF line endings.

## Cross-Platform Rule

When a command fails because of quoting, encoding, path, or shell parsing, classify it as an environment failure first. Do not repeat a remote write until remote state has been read.
