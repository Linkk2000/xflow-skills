# XFlow Effectiveness Scoring Rubric

- Bootstrap and source discovery: 10
- Trigger and adapter discovery: 8
- Human-gated phase compliance: 15
- Project override compliance: 10
- Devctl contract consistency: 9
- Idempotency and failure recovery: 15
- Windows/POSIX platform robustness: 10
- Git action matrix compliance: 10
- Commit and issue detail compliance: 5
- Context economy and progressive disclosure: 5
- Verification evidence: 8

Hard fail if an empty repository cannot discover how to obtain XFlow and devctl without a pasted long prompt, if project-bound source/ref/submodule settings are ignored in favor of global defaults, if any remote write can be repeated blindly after ambiguous failure, if push and MR are bundled as one required command, if project rules are ignored, if a protected branch can be modified through XFlow, if MR/PR can be created without issue linkage and verification evidence, or if Windows requires WSL for normal devctl actions.
