# Start XFlow Task

1. Read project rules and `.xflow/ops/workflow/SKILL.md`.
2. Locate an existing capability contract and write/check classification.
3. Satisfy the selected semantic exit condition before Issue/TDD/Git work.
4. For a remote Issue, create its `task-state.md` and run
   `devctl task activate --issue <id>`.
5. After `devctl git start`, create an Early XFlow artifact commit of trackable
   process files before contract/G2/implementation; it does not authorize push/MR.

Human Approval Is Non-Delegable. Stop at every gate required by the
project-local Skill.
