---
name: ue5-blueprint-authoring
description: "Inspect or edit UE5.4+ Blueprint graphs and assets through Editor tools, with compile and reference validation."
---

# UE5 Blueprint Authoring

## 适用范围

用于 Blueprint Class、Function/Macro Library、Widget Blueprint、Animation Blueprint 和图表/变量/默认值编辑。C++ API 暴露问题同时加载 `ue5-cpp-blueprint-interop`。

## 版本门槛

最低 UE5.4。UE5.8 可通过原生 MCP Toolsets 操作；UE5.4–5.7 使用 Editor/UI/Python/Utility 等当前项目已有路径。任何版本都禁止直接改二进制资产字节。

## 工作流

### 1. 建立恢复点

只读检查不要求修改 Editor 状态。写入前保存当前资产并提交/搁置，确认目标路径、父类、依赖和多人编辑状态，停止 PIE 并等待编译/加载完成。批量修改先在副本或沙箱验证。

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

使用 MCP/Editor Python/Blueprint 工具时：先描述 Tool schema，逐步创建变量/节点/连接，验证每个返回值。不要并行改同一 Blueprint。对删除、重命名、父类变更和 Pin 重连检查现有明确授权是否覆盖目标；未覆盖时展示具体变更后再确认。

### 5. 编译、保存、重读

每个逻辑变更后编译 Blueprint；出现错误先暂停后续图修改，在已授权范围内定位并修复本次变更，再编译验证。结果不明确时先重读，不能盲目重试写入。保存明确资产，然后重新查询变量、图和编译结果。必要时打开 Editor 验证默认值、组件层级和运行行为。

### 6. 审查资产差异

使用 Unreal Diff/Source Control 工具，而不是文本 diff 假装理解 `.uasset`。确认没有意外修改依赖资产、默认对象、重定向器或大量重新保存。

涉及图替换、父类/类型变化或批量操作时，读取 [资产安全检查](references/blueprint-safety.md)。

## 验证

只读任务交付实际图/类型/编译状态。以下检查用于资产修改；重开 Editor 重点验证父类、反射或序列化变化，普通查询不触发重启。

- Blueprint 编译为 Success 且无新增重要 warning；
- 目标图、Pin、变量类型和默认值与计划一致；
- PIE/Standalone 中执行路径正确；
- Source Control 只包含预期资产；
- 重开 Editor 后资产仍能加载、编译和保存。
