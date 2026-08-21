---
name: ue5-blueprint-authoring
description: "Design, inspect, or modify UE5.4+ Blueprints and Blueprint assets through Unreal Editor, MCP, or scripting while preserving graph correctness, compile status, defaults, references, and source-control recoverability."
---

# UE5 Blueprint Authoring

## 适用范围

用于 Blueprint Class、Function/Macro Library、Widget Blueprint、Animation Blueprint 和图表/变量/默认值编辑。C++ API 暴露问题同时加载 `ue5-cpp-blueprint-interop`。

## 版本门槛

最低 UE5.4。UE5.8 可通过原生 MCP Toolsets 操作；UE5.4–5.7 使用 Editor/UI/Python/Utility 等当前项目已有路径。任何版本都禁止直接改二进制资产字节。

## 工作流

### 1. 建立恢复点

保存当前资产并提交/搁置。确认目标 Blueprint 路径、父类、依赖资产、是否正被多人编辑、PIE 是否运行。批量修改前先在副本或沙箱验证。

### 2. 只读检查

读取：

- Blueprint 类型、父类和接口；
- 变量、组件、函数、图、节点和 Pin 类型；
- Class Defaults 与实例覆盖；
- 当前编译状态、警告和循环依赖；
- 引用者和重定向器风险。

不要仅凭截图或资产名猜图结构。

### 3. 设计最小图变更

优先函数化、组件化、接口和数据驱动；避免在 Event Graph 堆叠巨大流程。控制纯函数副作用、Latent 节点上下文、Timer/Delegate 解绑和 Event Tick 成本。对关键 C++ 不变量不要只靠 Blueprint 图约定。

### 4. 通过 Editor API 修改

使用 MCP/Editor Python/Blueprint 工具时：先描述 Tool schema，逐步创建变量/节点/连接，验证每个返回值。不要并行改同一 Blueprint。对删除、重命名、父类变更和 Pin 重连取得明确许可。

### 5. 编译、保存、重读

每个逻辑步骤后编译 Blueprint；有错误立即停止。保存明确资产，然后重新查询变量、图和编译结果。必要时打开 Editor 验证默认值、组件层级和运行行为。

### 6. 审查资产差异

使用 Unreal Diff/Source Control 工具，而不是文本 diff 假装理解 `.uasset`。确认没有意外修改依赖资产、默认对象、重定向器或大量重新保存。

完整安全规则见 `references/blueprint-safety.md`。

## 验证

- Blueprint 编译为 Success 且无新增重要 warning；
- 目标图、Pin、变量类型和默认值与计划一致；
- PIE/Standalone 中执行路径正确；
- Source Control 只包含预期资产；
- 重开 Editor 后资产仍能加载、编译和保存。
