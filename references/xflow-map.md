# XFlow Project Map For TDD Work

## XFlow Workflow References

- `workflow-state-machine.md`: phase order, states S0-S7, and gates G1-G5.
- `bootstrap-policy.md`: how an empty repository obtains XFlow files and local devctl entrypoints.
- `restore-policy.md`: how an existing XFlow repository is rehydrated on a new machine.
- `source-resolution.md`: source/ref/submodule priority and project binding rules.
- `human-gates.md`: valid and invalid human approval wording.
- `priority-and-overrides.md`: rule precedence and project override boundaries.
- `platform-adapters.md`: Windows/POSIX command and encoding expectations.
- `devctl-contract.md`: devctl entrypoints, environment variables, and command semantics.
- `git-policy.md`: Git action matrix, branch, commit, issue, MR/PR, and conflict rules.
- `issue-policy.md`: issue drafting, duplicate checks, body-file usage, and retry safety.
- `scoring-rubric.md`: 100-point effectiveness rubric and hard-fail conditions.
- `ops-lessons.md`: concise operational lessons for remote writes, shell boundaries, and context drift.

## Repositories

- Frontend: `D:\04-code\018-xflow\xflow`
- Backend: `D:\04-code\018-xflow\xflow-server`

Each repository has its own git history and `devctl`. Use the native entrypoint for the current platform: `.\devctl.ps1` on Windows, `./devctl` on POSIX.

## devctl Commands

Run from the owning repository.

Windows:

```powershell
.\devctl.ps1 help
.\devctl.ps1 init --target D:\path\to\repo
.\devctl.ps1 doctor
.\devctl.ps1 check encoding
.\devctl.ps1 check commit-msg --message-file FILE
.\devctl.ps1 check branch-scope --issue N
.\devctl.ps1 issue create "<title>" --body-file .xflow-local/issue-body.md --labels "tdd,frontend"
.\devctl.ps1 git push
```

POSIX:

```bash
./devctl help
./devctl init --target /path/to/repo
./devctl issue create "<title>" --body-file .xflow-local/issue-body.md --labels "tdd,frontend"
./devctl issue close <number>
./devctl issue list --state open --limit 20
./devctl issue show <number>
./devctl git start <slug> --issue <number>
./devctl git status
./devctl git commit-msg -a
./devctl git commit-msg -ac
./devctl git push
./devctl git mr --title "<title>" --body-file .xflow-local/mr-body.md --issue <number>
./devctl git done
```

For issue creation and comments, use `--body` only for short single-line text. Multi-line Markdown, fenced code, inline backticks, JSON, or shell snippets must be written to a file and passed with `--body-file` so shells do not reinterpret the content.

Remote issue/MR commands require `GITEE_TOKEN` through `~/gitee.env.local` or the environment.

Canonical XFlow branches use slash form: `feature/<issue>-<slug>` or `fix/<issue>-<slug>`. Use `devctl git start <slug> --issue <number>` as the canonical branch creation command.

`devctl issue close` closes a remote Gitee issue after the user confirms the implementation satisfies the issue.

## Frontend Key Paths

- Studio shell: `apps/xflow/src/views/xflow/design/designer/index.vue`
- Studio JSON panel: `apps/xflow/src/views/xflow/design/studio/StudioJsonDebugPanel.vue`
- Plugin registration: `apps/xflow/src/plugins/xflow.ts`
- Flowable plugin: `apps/xflow/src/plugins/flowable.ts`
- Shared plugin contract: `packages/shared-types/src/index.ts`
- WarmFlow plugin wrapper: `packages/plugin-warmflow/src/index.ts`
- WarmFlow designer: `packages/warmflow-designer/src`
- WarmFlow serialization: `packages/warmflow-designer/src/adapter/defJsonAdapter.ts`
- WarmFlow edge geometry: `packages/warmflow-designer/src/adapter/edgeGeometry.ts`
- WarmFlow properties: `packages/warmflow-designer/src/properties/PropertyPanel.vue`
- API request client: `apps/xflow/src/api/request.ts`
- Design routes: `apps/xflow/src/router/routes`

## Backend Key Paths

- Platform API: `xflow-app/src/main/java/io/xflow/app/web/PlatformController.java`
- WarmFlow runtime API: `xflow-app/src/main/java/io/xflow/app/web/WarmFlowRuntimeController.java`
- Model lifecycle: `xflow-app/src/main/java/io/xflow/app/service/ModelLifecycleService.java`
- Domain service: `xflow-app/src/main/java/io/xflow/app/service/DomainService.java`
- Security: `xflow-app/src/main/java/io/xflow/app/config/SecurityConfig.java`
- Engine plugin contract: `xflow-core/src/main/java/io/xflow/core/plugin/EnginePlugin.java`
- WarmFlow adapter: `plugins/warmflow-engine-plugin`
- Entities: `xflow-infra/src/main/java/io/xflow/infra/entity`
- Migrations: `xflow-infra/src/main/resources/db/migration`
- DTOs: `xflow-api/src/main/java/io/xflow/api/dto`

## TDD Targets By Change Type

- Model lifecycle: test `ModelLifecycleService` transitions and saveDraft rules.
- New API: test DTO shape and controller/service behavior; avoid exposing entities.
- Migration: add a new Flyway migration, never edit released V1-V5.
- WarmFlow serialization: test DefJson loading/saving, `coordAnchor`, node type mapping, and skipList output.
- Edge behavior: test geometry/simplification without storing stale runtime paths.
- Studio actions: test shared action dispatch where possible; browser-check toolbar behavior.
- Property panel: test emitted patch behavior or adapter updates, then browser-check selected node/edge editing.
- Runtime deploy/start/tasks: test adapter/service boundary where feasible and verify API behavior.

## Local Validation Commands

Frontend:

```bash
pnpm typecheck
pnpm build:packages
pnpm build
```

WarmFlow package:

```bash
pnpm -F @warm-flow/designer-vueflow run typecheck
```

Backend examples:

```bash
mvn -pl xflow-app test
mvn -pl xflow-app -am test
mvn -pl xflow-app spring-boot:run
```

Use focused commands first. Run broader builds only when the changed surface justifies it.
