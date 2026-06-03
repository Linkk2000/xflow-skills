# XFlow Issue And MR Templates

## Issue Draft Template

Use this shape when converting an oral request into a remote issue.

Before creation, also propose:

- issue kind: `feature` or `fix`
- issue key preview: `feature/<issue-id>-<short_slug>` or `fix/<issue-id>-<short_slug>`
- final branch name after issue creation (`feature/<issue-id>-<slug>`)

```markdown
## 背景
<为什么现在要做这个问题，用户遇到了什么阻碍。>

## 问题
<当前行为或缺口。写成可验证的问题，不写泛泛愿望。>

## 目标
<完成后用户/系统应该能做什么。>

## 范围
- 前端:
- 后端:
- 流程设计器:
- 数据库/迁移:
- 不包含:

## TDD 验收标准
- [ ] 先补充或确认一个失败用例/验收检查，覆盖 <核心行为>
- [ ] 实现后 <具体行为> 通过
- [ ] 回归 <相关风险点> 不被破坏

## 建议测试
- <最小测试命令或测试文件>
- <需要浏览器验证时写清楚页面和动作>

## 影响路径
- `<path>`

## 备注
<约束、兼容性、后续工作。>
```

## Label Hints

Use comma-separated labels for `devctl issue create --labels`.

- `frontend`
- `backend`
- `designer`
- `warmflow`
- `api`
- `runtime`
- `bug`
- `enhancement`
- `tdd`
- `test`
- `docs`

## MR Body Template

```markdown
## Summary
- Closes #<issue>
- <what changed>

## TDD / Test plan
- [x] <failing test or acceptance check first>
- [x] <focused validation command>
- [x] <browser/manual check if applicable>

## Risk
- <remaining risk or "低: ...">
```

## Clarifying Questions

仅在严重阻碍 Issue 质量和明确性时提问。优秀的通用澄清问题示例：

- 这是个缺陷修复（Bug Fix）还是属于新能力扩展（Feature）？
- 我们是优先做最小可行性产品（MVP），还是需要一次性把完整功能、配置及边缘分支全部补全？
- 这个问题应该落在哪个特定的核心模块（或子项目/子文件夹）？是否涉及跨系统/多仓库的协同？
- 验收此功能时，你期望看到的验证证据是什么（例如：编译通过、单元测试输出、数据库状态变化，还是 UI 交互截图）？
