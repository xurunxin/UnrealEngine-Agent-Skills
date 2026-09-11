---
name: ue5-mcp-operator
description: "Connect to or operate a running UE5.8 native MCP Editor through discovered Toolsets; excludes source-only questions."
---

# UE5.8 MCP Operator

## 适用范围

连接或操作运行中的 UE5.8 Editor 原生 MCP。纯概念/源码查询使用相应领域 Skill，不启动服务。

## 版本门槛

要求目标引擎包含 `ModelContextProtocol` 和 `ToolsetRegistry` 插件；当前核验 UE5.8.1，属于 Experimental。新 Patch/Minor 先运行 `verify_engine.py`。UE5.4–5.7 不使用原生流程；第三方 MCP 需单独选择和验证。

## 工作流

### 连接与发现

确认正确项目、Editor 实例及实际连接配置；已连接时直接发现任务所需 Toolset，不重新启用插件或重启 Editor。MCP 只绑定 loopback，不通过 Tailscale、Tunnel 或反代直接暴露。只有需要设置/排障时读取 [启动、配置和恢复](references/setup-and-recovery.md)；默认手动启动，auto-start 只在用户选择时修改每用户配置。

`ModelContextProtocol` 提供服务，具体 Toolset 提供领域操作；启用最小插件集合，`AllToolsets` 仅用于受控沙箱。插件变更须在用户明确授权范围内，必要时重启 Editor。

tool-search 模式使用 `list_toolsets`、`describe_toolset`、`call_tool`。已知领域可直接 describe；按返回 schema 构造 typed arguments。项目存在原生技能时按任务匹配 List/Get，避免加载全部项目技能；符合安全和版本要求的项目规则优先。

### 查询与变更

所有 Editor Tool 调用串行并检查结果。只读查询无需为此保存资产或停止 PIE。工具若要求不同 Editor 状态，先检查是否符合用户限定；不符合时说明限制，不为完成查询擅自改变状态。

写入前只读检查目标，停止 PIE、等待编译/加载完成，保存并建立 source-control checkpoint。按“单一修改 → 检查结果 → 必要编译 → 保存明确资产 → 重读”执行。删除、移动、批量创建、父类变化、任意 Python 等需先展示计划并确认授权覆盖范围；已有明确指示不重复确认。

可确定的编译/参数错误在授权范围内修复并重验；结果不明确时暂停后续写入，先重读状态及日志，禁止盲目重试。仅在状态明确、恢复方案可控时继续，否则报告具体阻塞和恢复点。

## 验证

连接任务以 initialize、tools/list 及预期 schema 为完成证据；只读任务以返回的项目/对象状态为证据。写入任务另外验证对应 Blueprint/C++ 编译、指定资产保存、重读结果及 source-control diff。不可用的 Editor/Engine 环境需明确标注，不能声称资产已验证。
