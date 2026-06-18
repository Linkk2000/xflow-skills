# Priority And Overrides

Apply rules in this order:

1. Current explicit user instruction.
2. Nearest project `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/*.mdc`, or Antigravity `.agents/*` rule.
3. Global XFlow Skill.
4. Agent defaults.

Project rules may override language, commit format, test commands, directory layout, and build commands.

Project rules must not remove human gates for remote writes, destructive actions, or issue/MR lifecycle actions unless the user explicitly confirms in the current conversation.
