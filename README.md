# UnrealEngine Agent Skills

面向 Coding Agent 的 Unreal Engine 5 开发知识与执行工作流。工程以 **UE5.4+** 为最低兼容基线，当前源码核验基准为 **UE5.8.1**；C++、Blueprint、模块/插件、构建测试、版本迁移以及 UE5.8 原生 MCP / Toolset Registry 均被拆成可按需加载的独立 Skill。

> 本仓库不是 Unreal Engine 源码镜像，也不分发 Epic 受限源码。源码相关知识只保存路径索引、接口摘要、验证规则与原创示例。使用者仍须遵守 Unreal Engine EULA，并自行取得相应源码访问权限。

## 兼容范围

| 范围 | 状态 | 规则 |
|---|---|---|
| UE5.8.1 | 已对指定源码提交核验 | MCP、Toolset Registry、AgentSkill 可用 |
| UE5.4–5.7 | 核心 Skills 目标范围 | MCP Skill 自动降级为“不适用/需外部方案” |
| UE5.0–5.3 | 仅迁移参考 | 不把旧示例直接当作 UE5.4+ 实现 |
| UE4.x | 明确排除 | 只允许在迁移分析中引用，禁止作为新项目模板 |

## 三层结构

1. **通用文本 Skills**：兼容支持 `SKILL.md` 的 Coding Agent，入口为 [`skills/ue5-router/SKILL.md`](skills/ue5-router/SKILL.md)。
2. **UE5.8 编辑器原生能力**：通过 ModelContextProtocol、Toolset Registry 和项目内 `UAgentSkill` 驱动 Editor；相关流程位于 `ue5-mcp-*` 与 `ue5-agent-skill-authoring`。
3. **可验证来源层**：`sources.lock.json` 固定源码提交与外部资料，`scripts/verify_engine.py` 在本地校验 Engine 版本和关键路径。

## 快速开始

```bash
# 1. 校验本仓库
python scripts/generate_catalog.py --check
python scripts/validate_skills.py
python -m unittest discover -s scripts/tests

# 2. 校验本地引擎源码（最低 UE5.4）
python scripts/verify_engine.py --engine-root /path/to/UnrealEngine

# 3. 只读探测 UE5.8 MCP 服务
python scripts/probe_mcp.py --url http://127.0.0.1:8000/mcp
```

让 Agent 从 `ue5-router` 开始，根据任务只加载必要 Skill。任何写资产、批量改 Blueprint、执行 Editor Python、创建 AgentSkill 或调用高权限 MCP Toolset 的任务，都必须先建立源码控制恢复点并取得用户明确许可。

### 通过 skills CLI 安装

仓库遵循 Agent Skills 的 `skills/<name>/SKILL.md` 布局，可按需安装，而不是把 17 个 Skill 全部注入项目：

```bash
npx skills add xurunxin/UnrealEngine-Agent-Skills --skill ue5-router
npx skills add xurunxin/UnrealEngine-Agent-Skills --skill ue5-cpp-gameplay
npx skills add xurunxin/UnrealEngine-Agent-Skills --skill ue5-mcp-operator
```

安装到具体 Agent 的目标目录由当前 skills CLI 选择；项目仍应保留自己的精简 `AGENTS.md`。

## 首版 Skills

完整清单见 [`CATALOG.md`](CATALOG.md)，主要覆盖：

- 项目初始化、架构设计、源码导航；
- UE C++、UObject/UHT、Gameplay Framework；
- Module、Plugin、Build.cs、Target.cs；
- Blueprint 设计、C++/Blueprint 边界、Editor 自动化；
- Automation Test、调试、Cook/Package、性能分析；
- UE5.4+ 兼容与 UE5.3 分水岭迁移；
- UE5.8 MCP 操作、自定义 Toolset、项目原生 AgentSkill。

## 设计原则

- **当前项目代码优先**：先读项目的 `AGENTS.md`、模块规则和相邻实现，再查引擎源码。
- **证据优先**：本地当前版本源码 > Epic 官方文档 > 已核验社区经验 > 旧版本文章。
- **小步验证**：一次只完成一个可编译、可测试、可回滚的改动。
- **Blueprint 不做二进制编辑**：不得直接改 `.uasset`/`.umap` 字节；使用 Editor、MCP、Python 或受控工具。
- **MCP 串行调用**：Editor Toolset 通常运行在 Game Thread；不要并行发起依赖 Editor 状态的调用。
- **版本门槛显式化**：涉及 UE5.8-only API 时必须写出 gate 和降级路径。

## 维护

变更流程、来源升级和兼容策略见 [`docs/maintenance.md`](docs/maintenance.md) 与 [`CONTRIBUTING.md`](CONTRIBUTING.md)。当前核验状态见 [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)。

## License

本仓库原创内容使用 MIT License。Unreal Engine、Epic Games 及相关商标和源码仍受各自许可约束。
