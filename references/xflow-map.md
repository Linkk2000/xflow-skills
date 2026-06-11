# XFlow Project Map For TDD Work

## Repositories

- Frontend: `D:\04-code\018-xflow\xflow`
- Backend: `D:\04-code\018-xflow\xflow-server`

Each repository has its own git history and `devctl`.

## devctl Commands

Run from the owning repository.

```bash
./devctl help
./devctl issue create "<title>" --body-file .xflow-local/issue-body.md --labels "tdd,frontend"
./devctl issue close <number> --comment "<confirmed summary>"
./devctl issue list --state open --limit 20
./devctl issue show <number>
./devctl git start <slug> --issue <number>
./devctl git start-issue feature <issue-id> <slug>
./devctl git start-issue fix <issue-id> <slug>
./devctl git status
./devctl git commit-msg -a
./devctl git commit-msg -ac
./devctl git mr --title "<title>" --body "<body>" --issue <number>
./devctl git done
```

For issue creation and comments, use `--body` only for short single-line text. Multi-line Markdown, fenced code, inline backticks, JSON, or shell snippets must be written to a file and passed with `--body-file` so shells do not reinterpret the content.

Remote issue/MR commands require `GITEE_TOKEN` through `~/gitee.env.local` or the environment.

`devctl git start` keeps the original `feat/<issue>-<slug>` behavior. Use the additive `devctl git start-issue` command for exact branch names like `feature_<issue-id>_<slug>` and `fix_<issue-id>_<slug>`. Gitee IDs can be alphanumeric; branch names normalize them to lowercase.

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
