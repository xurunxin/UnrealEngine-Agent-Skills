---
name: ue5-mcp-operator
description: "Operate the UE5.8 native Model Context Protocol server and Toolset Registry from a Coding Agent, including setup, discovery, serial execution, Blueprint and asset workflows, recovery, and security."
---

# UE5.8 MCP Operator

## 适用范围

用于 Coding Agent 查询或操作一个正在运行的 UE5.8 Unreal Editor：Actor、Blueprint、资产、材质、Sequencer、Niagara、测试、Live Coding 等。纯概念/源码问题不触发；它们使用相应普通 Skill。

## 版本门槛

- 要求 UE5.8+ 源码中存在 `ModelContextProtocol` 和 `ToolsetRegistry` 插件。
- 当前已核验 UE5.8.1；插件为 Experimental，任何新 Patch/Minor 都先运行 `verify_engine.py`。
- UE5.4–5.7 不使用本 Skill，除非用户明确选择并验证第三方 MCP 实现。

## 工作流

### 1. 前置安全检查

确认正确项目和 Editor 实例，停止 PIE，等待编译/加载完成。保存并建立 source-control checkpoint。MCP 端口只绑定 loopback；不要通过 Tailscale、Tunnel 或反代直接暴露。

### 2. 启用最小插件集合

`ModelContextProtocol` 提供服务；Toolset 插件提供操作。优先只启用任务所需 Toolset；`AllToolsets` 仅用于受控沙箱。插件改动需用户明确同意并重启 Editor。

### 3. 启动和连接

手动执行 `ModelContextProtocol.StartServer`，或在每用户 Editor 配置启用 auto-start。默认端口 `8000`、路径 `/mcp`。使用 `ModelContextProtocol.GenerateClientConfig <client>` 生成实际客户端配置。

### 4. 发现再调用

默认 tool-search 模式只暴露：

1. `list_toolsets`；
2. `describe_toolset`；
3. `call_tool`。

如果已知域，直接 describe 候选 Toolset；根据返回 schema 构造 typed arguments，再用 call_tool。不要编造工具名或参数。

### 5. 加载项目技能

对陌生项目先通过 `AgentSkillToolset.ListSkills` 查询项目原生技能，匹配后 `GetSkills` 加载。项目 Skill 在不违反安全和版本门槛时优先于通用默认。

### 6. 串行执行变更

按“只读检查 → 单一修改 → 检查结果 → 编译 → 保存 → 重读”循环。所有 Editor Tool 调用串行；不要并行，即使看似修改不同资产。对删除、移动、批量创建、父类变化、任意 Python 等操作先展示计划并取得许可。

### 7. 恢复

工具缺失时 RefreshTools；端口冲突时改端口并重新生成配置；调用卡住时检查 PIE、编译、模态窗口和 Editor 日志。结果不明确时停止，禁止盲目重试写操作。

设置与故障矩阵见 `references/setup-and-recovery.md`。

## 验证

- `scripts/probe_mcp.py` 能完成 initialize 和 tools/list；
- 发现到预期 Toolset/schema；
- 每个修改调用有明确 success/result；
- Blueprint/C++ 编译和目标资产保存成功；
- 重读状态与用户目标一致，source-control diff 可审查。
