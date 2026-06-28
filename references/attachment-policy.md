# Attachment Policy

Use this reference when a user pastes files, screenshots, image paths, or
other local artifacts that should appear in a remote Issue, issue comment, or
PR/MR body.

## Core Rule

Remote GitHub/Gitee Markdown cannot safely reference local paths such as
`C:\...`, `/tmp/...`, `.xflow/...`, or `file://...`. Before a remote write, the
AI must convert local artifacts into reviewed attachment records and publishable
URLs, or stop and ask the human to choose an attachment backend.

Never publish:

- raw local file paths
- unresolved `xflow-attachment://<id>` placeholders
- private temp paths from chat clients, browsers, shells, or WSL mounts
- filenames without a reviewed storage plan

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
      "publishedUrl": null
    }
  ]
}
```

The body draft may use `xflow-attachment://<id>` while still local. The final
remote body must replace every placeholder with a reviewed `publishedUrl`.

## Backend Modes

The project or user may choose one mode:

- `object`: upload to an approved object store or asset service.
- `repo`: commit small public artifacts under an approved repository path.
- `provider`: use a supported GitHub/Gitee attachment or release asset flow.
- `none`: do not publish the artifact; describe it textually or ask the human
  to provide a public URL.

If no backend is configured, fail closed. Do not guess a public host and do not
paste a local path into the remote body.

## Human Approval Gate

For `issue-create`, `issue-comment`, and `git-mr`, approval must cover:

- the exact body file SHA256
- the attachment manifest SHA256
- filenames, MIME types, byte sizes, and SHA256 values
- selected backend mode and target URL/path plan
- the rendered Markdown after placeholder replacement

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

1. The user asks to create an issue/comment and provides files or images.
2. The AI saves or registers each artifact into the XFlow attachment directory.
3. The AI creates the body draft and manifest together.
4. The AI stops at the same local approval gate before any remote write.

## Required Checks

Before a remote write, `devctl` or the AI must reject body files containing:

- `xflow-attachment://`
- Windows local paths matching drive-letter forms such as `C:\` or `D:\`
- `file://`
- POSIX local temp/home paths such as `/tmp/`, `/mnt/`, or `/home/`
- `.xflow/` paths in public Markdown bodies

This check is a publication guard. Local drafts may contain placeholders; final
remote bodies may not.
