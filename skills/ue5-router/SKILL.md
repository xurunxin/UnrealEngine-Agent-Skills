---
name: ue5-router
description: "Select UE5.4+ domain skills when a request spans workflows or its task, engine version, or execution mode is unclear."
---

# UE5 Skill Router

## 适用范围

用于任务跨领域、版本或执行模式不明时选择 Skill。已明确的任务直接加载对应领域 Skill；不为单个编译错误重复完成项目初始化。

## 版本门槛

核心范围 UE5.4+；UE4/UE5.0–5.3 输入先进入版本迁移。UE5.8 原生 MCP 仅在目标版本和插件存在性已验证时适用。

## 工作流

按当前不确定性读取 `.uproject`、`Build.version`、最近构建日志或项目 `AGENTS.md`，复用本会话已确认的项目和版本，不凭目录名猜测。纯路由问题无需启动 Editor。

| 任务 | 主要 Skill |
|---|---|
| 初始化工作区 | `ue5-project-bootstrap` |
| 查 API、模块归属或调用点 | `ue5-source-navigation` |
| 架构、职责、依赖边界 | `ue5-project-architecture` |
| Gameplay C++ | `ue5-cpp-gameplay` |
| UHT、反射、GC | `ue5-uobject-reflection` |
| Module/Plugin/Build.cs/Target.cs | `ue5-modules-plugins` |
| Blueprint 图和资产 | `ue5-blueprint-authoring` |
| C++ 暴露给 Blueprint | `ue5-cpp-blueprint-interop` |
| Editor Python、Commandlet、Utility | `ue5-editor-automation` |
| 测试、崩溃、日志 | `ue5-testing-debugging` |
| Build/Cook/Package/Patch | `ue5-build-cook-package` |
| 性能测量和回归 | `ue5-performance-profiling` |
| 旧版本或跨 Minor 兼容 | `ue5-version-migration` |
| 运行中 Editor 的原生 MCP | `ue5-mcp-operator` |
| 实现 MCP Toolset | `ue5-mcp-tool-authoring` |
| 编写 portable / 原生 AgentSkill | `ue5-agent-skill-authoring` |

只在依赖实际涉及另一领域时加载伴随 Skill。例如新增 BlueprintNativeEvent 需要 interop 和 reflection；仅查其声明不需要 MCP 或打包流程。各 Skill 的 references 按具体问题读取。

文件变更以最小受影响 Target 验证；反射签名变更需要冷编译/重启检查。资产写入通过 Editor API，先建立恢复点，禁止直接改 `.uasset`/`.umap`。MCP Editor 调用串行，按实际 schema 调用并核对结果。

## 验证

路由完成时已确定适用的主 Skill、文件/Editor/MCP/迁移模式，以及实现所需的版本证据或尚缺信息。实现任务继续到目标行为、相应编译/测试和差异检查完成；授权范围内的可恢复失败应定位并修复。读源码或仅做方案无需编译；无法运行的 Engine 检查明确标为未验证，不用静态检查代替。
