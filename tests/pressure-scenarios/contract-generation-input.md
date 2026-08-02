# Contract Generation Input

## Natural-Language Capability Request

在一台新电脑上，用户进入一个空目录、非 Git 项目、没有远端或远端为空的
Git 项目、或者已经有远端的 Git 项目时，只用自然语言要求启用 XFlow。系统应
仅在确认的项目根目录内完成本地初始化或恢复，使用项目自己的
`.xflow/ops/workflow` 和 `.xflow/ops/devctl`；不得依赖全局安装或临时开发目录。

默认使用本地 ignored vendor；如果项目已经明确、完整地配置了 submodule，保留
该选择。恢复时保留既有代码、项目规则、Issue 过程资料和工具选择；冲突绝不覆盖，
可以继续执行独立的安全动作，但必须把冲突和阻塞原因留给人工处理。Git、Python 等
机器级前提只能检查和报告，不能安装。任何 push、远端 Issue、PR/MR 或其他远端写入
必须停止并请求人工审核。

## Required Discovery Stop

在边界决策获得批准前，代理只能搜索现有契约并一次提出一个会改变边界的问题，给出
互斥选项与推荐项；不得生成 YAML、修改实现或进入开发。
