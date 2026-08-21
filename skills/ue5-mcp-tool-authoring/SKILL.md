---
name: ue5-mcp-tool-authoring
description: "Design, implement, register, test, and secure UE5.8 MCP Toolsets or direct protocol tools using ToolsetRegistry, typed AICallable functions, async results, schemas, and explicit privilege boundaries."
---

# UE5.8 MCP Tool Authoring

## 适用范围

用于新增/扩展 Toolset、把 Editor 能力暴露给 Agent、设计 `AICallable` API、异步 Tool、schema/converter 和直接 `IModelContextProtocolTool`。仅调用已有工具时使用 `ue5-mcp-operator`。

## 版本门槛

要求 UE5.8+ ToolsetRegistry/ModelContextProtocol。当前 API map 以 UE5.8.1 commit 为准；Experimental API 升级必须重新探测。

## 工作流

### 1. 证明能力缺失

先运行 list/describe，搜索现有 Toolsets 和项目插件。若已有通用能力，复用它；不要为单一资产类型复制 Object/Asset/Blueprint 通用操作。

### 2. 选择实现层

- 首选 Python Toolset：目标 API 在当前 `Intermediate/PythonStub/unreal.py` 完整可用且团队接受脚本分发；
- C++ `UToolsetDefinition`：需要未暴露 API、强类型、性能、生命周期或自动化测试；
- 直接 `IModelContextProtocolTool`：仅在 schema/工具集合必须动态生成或需要低层协议生命周期时。

不要用任意 Python 执行器绕过缺失的领域 API。

### 3. 设计小而完整的工具

工具名称和描述面向任务，参数/返回值使用真实 UE 类型或 USTRUCT，不把结构塞进 JSON 字符串。支持合理 CRUD 对称，但默认先做只读。每个 mutation 校验对象路径、World、权限和前置状态。

### 4. C++ 约定

- 继承 `UToolsetDefinition`；
- 所有 Tool 是 `static UFUNCTION(meta=(AICallable))`；
- 非 Tool UFUNCTION 标记 `AIIgnore` 或不暴露；
- 模块启动/关闭时对称 `RegisterToolsetClass`/`UnregisterToolsetClass`；
- 长任务返回现有或自定义 `UToolCallAsyncResult`，只完成一次并支持取消；
- 错误通过 Toolset 的脚本错误/async error 契约返回，不用“成功 bool + 错误字符串”混合结构。

### 5. 文档和 schema

类说明定义域；函数说明写非显然语义、单位、空值和副作用。Schema 必须让 Agent 能在不读实现的情况下正确调用。避免几十个布尔开关组成“万能工具”。

### 6. 编译和刷新

仅函数体变化可尝试 Live Coding；新增或改变反射 UFUNCTION/USTRUCT 时执行完整编译并重启 Editor。插件启用后运行 `ModelContextProtocol.RefreshTools`，重新 describe 验证 schema。

### 7. 测试与威胁审查

每个 Tool 测试成功、所有输入错误、对象失效、PIE/无 World、异步取消和重复调用。Mutation 在临时资产/地图运行，并验证清理。审查是否能越权访问文件系统、执行代码或批量删除。

API 路径与检查表见 `references/ue5.8.1-api-map.md`，Python Toolset 约定见 `references/python-toolsets.md`；原始 C++ 示例见 `examples/mcp-toolset/`。

## 验证

- schema 可通过 Registry API/describe 读取；
- Toolset 能注册、Refresh 后仍存在、关闭模块时注销；
- success/error/cancel 测试通过；
- 调用串行且不会阻塞 Game Thread 做无界工作；
- 默认权限最小，破坏性副作用在描述和代码中显式。
