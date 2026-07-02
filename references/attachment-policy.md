# Attachment Policy

Use this reference when a user pastes files, screenshots, image paths, or
other local artifacts that should appear in a remote Issue, issue comment, or
PR/MR body. Issue/comment image attachments are currently disabled. Images and
screenshots stay local by default. They may be published into issue/comment
bodies only after an approved object storage backend records reviewed public
URLs in the attachment manifest.

## Core Rule

Remote GitHub/Gitee Markdown cannot safely reference local paths such as
`C:\...`, `/tmp/...`, `.xflow/...`, or `file://...`. Before a remote write, the
AI must convert local artifacts into reviewed attachment records and approved
publishable URLs, or stop and ask the human to choose an attachment backend.
For issue/comment images or screenshots, the only supported publishing path is
an approved object storage backend such as Aliyun OSS. GitHub release assets
are not an approved issue image store.

Search anchor: GitHub release assets are not an approved issue image store.

Never publish:

- raw local file paths
- unresolved `xflow-attachment://<id>` placeholders
- private temp paths from chat clients, browsers, shells, or WSL mounts
- filenames without a reviewed storage plan
- issue/comment images or screenshots via GitHub release assets
- AccessKey IDs, AccessKey Secrets, tokens, or other object storage credentials

## Local Storage

Use these default locations:

```text
.xflow/issues/issue-draft/attachments/manifest.json
.xflow/issues/issue-draft/attachments/files/
.xflow/issues/issue-<id>/attachments/manifest.json
.xflow/issues/issue-<id>/attachments/files/
```

Copy or register the artifact locally before drafting the remote body. The
manifest is the review target; it lets the human see exactly what will be
published and where.

Subtask evidence must stay in the repository. Store subtask screenshots, small
files, logs, and local proof under
`.xflow/issues/issue-<id>/subtask-001/evidence/`, not in COS/OSS or any object
storage backend. Object storage is only for rendered GitHub/Gitee issue,
comment, or PR/MR bodies.

## Manifest Shape

```json
{
  "version": 1,
  "issue": "draft",
  "items": [
    {
      "id": "att-001",
      "filename": "screenshot.png",
      "localPath": ".xflow/issues/issue-draft/attachments/files/screenshot.png",
      "sha256": "<sha256>",
      "mime": "image/png",
      "size": 12345,
      "placeholder": "xflow-attachment://att-001",
      "markdown": "![screenshot](xflow-attachment://att-001)",
      "publishedUrl": null,
      "backend": null
    }
  ]
}
```

The body draft may use `xflow-attachment://<id>` while still local. A final
remote body must replace every placeholder with a reviewed `publishedUrl`.
Issue/comment image placeholders may be rendered only when the manifest item
was published by an approved object storage backend such as `aliyun-oss`.

## Backend Modes

The project or user may choose one mode for attachments:

- `object`: upload to an approved object store or asset service.
- `aliyun-oss`: use devctl's Aliyun OSS attachment backend.
- `repo`: commit small public artifacts under an approved repository path.
- `provider`: use a supported GitHub/Gitee attachment flow only when the
  project policy explicitly approves it for the artifact type.
- `none`: do not publish the artifact; describe it textually or ask the human
  to provide a public URL.

If no backend is configured, fail closed. Do not guess a public host and do not
paste a local path into the remote body.

`github-release` is a legacy devctl backend for generic files. It rejects image
attachments and must not be used as an issue/comment image store. Current
`devctl issue create` and `devctl issue comment` reject image MIME types and
Markdown image attachments unless the manifest shows a reviewed approved
backend such as `aliyun-oss`.

## Aliyun OSS Attachment Backend

Aliyun OSS attachment backend is an approved object storage option when the
user or project config provides credentials. Use it for issue/comment images
only through devctl:

```text
devctl attachment add --issue draft --file screenshot.png --as image
devctl attachment publish --issue draft --backend aliyun-oss --manifest .xflow/issues/issue-draft/attachments/manifest.json
devctl attachment render --issue draft --manifest .xflow/issues/issue-draft/attachments/manifest.json --input issue.md --output issue.final.md
devctl approval prepare --issue draft --action issue-create --file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl check local-review --issue draft --file issue.final.md --action issue-create --attachments .xflow/issues/issue-draft/attachments/manifest.json
devctl issue create "<title>" --body-file issue.final.md --attachments .xflow/issues/issue-draft/attachments/manifest.json
```

Credential config belongs in user or project local env files:

```text
%USERPROFILE%\.xflow\env.local
~/.xflow/env.local
.xflow/local/env.local
```

Required keys are `ALIYUN_OSS_BUCKET`, `ALIYUN_OSS_REGION`,
`ALIYUN_OSS_ACCESS_KEY_ID`, and `ALIYUN_OSS_ACCESS_KEY_SECRET`. Optional keys
include `ALIYUN_OSS_ENDPOINT`, `ALIYUN_OSS_PUBLIC_BASE_URL`, and
`ALIYUN_OSS_PREFIX`.

`ALIYUN_OSS_ACCESS_KEY_SECRET` must not be written to attachment manifests.
Credentials also must not appear in issue bodies, comments, commits, or
Markdown guides. The manifest records only backend, bucket, object key, file
hashes, MIME/size metadata, and `publishedUrl`.

## AI Decision Table

Choose one row and follow it exactly. Do not probe by retrying random flag
combinations.

| Situation | Required command path |
| --- | --- |
| Plain unattended issue | `devctl issue create "<title>" --body-file issue.md --no-local-review` |
| Plain unattended comment | `devctl issue comment <number> --body-file comment.md --no-local-review` |
| Issue/comment image or screenshot present without object storage approval | Do not upload. Keep local evidence and stop before remote write. |
| Reviewed Aliyun OSS image issue | `attachment add --as image` -> `attachment publish --backend aliyun-oss` -> `attachment render` -> `approval prepare` -> `check local-review` -> `issue create --body-file issue.final.md --attachments manifest.json` |
| Reviewed non-image issue attachment | `attachment add --as file` -> `attachment publish --backend manual --url att-001=https://public.example/file` -> `attachment render` -> `approval prepare` -> `check local-review` -> `issue create --body-file issue.final.md --attachments manifest.json` |
| Reviewed non-image comment attachment | `attachment add --as file` -> `attachment publish --backend manual --url att-001=https://public.example/file` -> `attachment render` -> `approval prepare --action issue-comment` -> `check local-review` -> `issue comment --body-file comment.final.md --attachments manifest.json` |
| No public URL available for a non-image file | Keep the file local as evidence or ask the human for an approved storage decision. |

Images are recognized by MIME type or `--attach-as image`; issue/comment
commands fail closed unless the manifest item was published by an approved
object storage backend. Non-image files render as normal Markdown links after
an approved URL is recorded. `GITHUB_TOKEN` is required for GitHub
issue/comment remote writes.

## Human Approval Gate

For `issue-create`, `issue-comment`, and `git-mr`, approval must cover:

- the exact body file SHA256
- the attachment manifest SHA256
- filenames, MIME types, byte sizes, and SHA256 values
- selected backend mode and target URL/path plan
- the rendered Markdown after placeholder replacement
- confirmation that issue/comment image attachments are either unpublished
  local evidence or published through an approved object storage backend

The reviewer approves the exact body plus attachment manifest. Changing either
requires a new local approval.

## Supported Flows

Two-step flow:

1. Create or update the draft body with placeholders.
2. Add attachments to the manifest.
3. Run attachment checks.
4. Publish attachments to the approved backend.
5. Render the final body with reviewed URLs.
6. Prepare local approval for the final body and manifest.
7. Execute the remote write.

One-step natural-language flow:

1. The user asks to create an issue/comment and may provide files or images.
2. The AI saves or registers each artifact into the XFlow attachment directory.
3. The AI creates the body draft and manifest together.
4. If any issue/comment attachment is an image or screenshot, publish it only
   through an approved object storage backend such as `aliyun-oss`; otherwise
   stop before the remote write. Do not use `--upload-attachments github` or
   release assets.
5. If the user explicitly requested no-human handling and there are no
   attachments, run `devctl issue create ... --no-local-review` for that exact
   action.
6. If only approved non-image attachments are present, follow the reviewed
   manifest and approved URL plan.
7. Otherwise, the AI stops at the same local approval gate before any remote
   write.

## Required Checks

Before a remote write, `devctl` or the AI must reject body files containing:

- `xflow-attachment://`
- Windows local paths matching drive-letter forms such as `C:\` or `D:\`
- `file://`
- POSIX local temp/home paths such as `/tmp/`, `/mnt/`, or `/home/`
- `.xflow/` paths in public Markdown bodies
- image MIME types or Markdown image attachments in issue/comment manifests
  unless they were published by an approved object storage backend

This check is a publication guard. Local drafts may contain placeholders; final
remote bodies may not.
