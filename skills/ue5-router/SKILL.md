---
name: ue5-router
description: "Route Unreal Engine 5.4+ development requests to the smallest relevant skill set; use at the start of any UE project, C++, Blueprint, module, build, testing, migration, or MCP task."
---

# UE5 Skill Router

## 适用范围

所有 Unreal Engine 项目任务先经过本 Skill。目标是识别版本、执行模式、主要风险和最小 Skill 组合，而不是一次加载全部知识。

## 版本门槛

- 核心范围：UE5.4+。
- UE5.8 原生 MCP：仅在检测到 5.8+ 且插件存在时启用。
- UE5.0–5.3 与 UE4：先路由到 `ue5-version-migration`，旧经验不得直接进入实现阶段。

## 工作流

### 1. 建立上下文

先确定：

- `.uproject` 路径、Engine 版本和 Source/Installed Build；
- 当前目标是 Runtime、Editor、Server、Client、Program 还是 Plugin；
- 变更是否涉及二进制资产、反射声明、模块依赖、Cook/Package 或运行中 Editor；
- 工作区是否有未提交改动和项目级 `AGENTS.md`。

缺少版本信息时，读取 `Engine/Build/Build.version`、`.uproject` 的 `EngineAssociation` 或构建日志。不要凭目录名猜版本。

### 2. 选择执行模式

| 模式 | 典型任务 | 必要约束 |
|---|---|---|
| 文件模式 | C++、Build.cs、Target.cs、Config、测试 | 编译最小 Target，检查模块所有权 |
| Editor 模式 | Blueprint、DataAsset、关卡、材质、重定向器 | 不直接写 `.uasset`/`.umap`；建立恢复点 |
| MCP 模式 | UE5.8 运行中 Editor 查询/修改 | 先发现 Toolset；串行；检查每次结果 |
| 迁移模式 | UE4/UE5.0–5.3 代码或跨 Minor 插件 | 先建立兼容矩阵，再改代码 |

### 3. 路由到主要 Skill

- 初始化工作区：`ue5-project-bootstrap`
- 找引擎 API、模块或当前实现：`ue5-source-navigation`
- 架构、职责和依赖：`ue5-project-architecture`
- Gameplay C++：`ue5-cpp-gameplay`
- UHT、反射、GC、对象指针：`ue5-uobject-reflection`
- Module/Plugin/Build.cs/Target.cs：`ue5-modules-plugins`
- Blueprint 图和资产：`ue5-blueprint-authoring`
- C++/Blueprint API 边界：`ue5-cpp-blueprint-interop`
- Editor Python、Commandlet、Utility：`ue5-editor-automation`
- 测试、崩溃和日志：`ue5-testing-debugging`
- Build/Cook/Stage/Package/Patch：`ue5-build-cook-package`
- 性能：`ue5-performance-profiling`
- 旧版本或跨版本：`ue5-version-migration`
- UE5.8 MCP 调用：`ue5-mcp-operator`
- UE5.8 自定义 Toolset：`ue5-mcp-tool-authoring`
- UE5.8 项目内 AgentSkill：`ue5-agent-skill-authoring`

一个任务通常只需要一个主要 Skill 和一至两个伴随 Skill。Blueprint 中新增 C++ 基类时，主要 Skill 是 `ue5-cpp-blueprint-interop`，伴随 `ue5-uobject-reflection`；不要因此加载构建、性能和 MCP 全部内容。

### 4. 设定完成定义

在编辑前写出：目标版本、受影响模块/资产、最小验证命令、是否需要 Editor 重启、是否有破坏性操作。任务完成必须同时满足实现、编译/资产编译、测试和差异审查。

## 验证

- 已记录准确 Engine 版本；
- 已选择唯一主要 Skill；
- 已区分文件/Editor/MCP/迁移模式；
- 已识别恢复点和最小验证；
- 未将 UE4 或 UE5.3 以前经验直接用作新实现。
