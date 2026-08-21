---
name: ue5-agent-skill-authoring
description: "Create, review, export, or update UE5.8 project-native UAgentSkill assets and portable SKILL.md instructions, with explicit user permission, concise routing metadata, and project-specific precedence."
---

# UE5.8 Agent Skill Authoring

## 适用范围

用于编写本仓库的 portable `SKILL.md`，或在 UE5.8 项目中创建/更新 `UAgentSkill` 资产。仅使用技能完成任务时不触发。

## 版本门槛

- portable `SKILL.md`：可用于支持 Agent Skills 的客户端，UE 核心内容以 5.4+ 为基线；
- `UAgentSkill`/`AgentSkillToolset`：要求 UE5.8+ ToolsetRegistry，当前核验 UE5.8.1。

## 工作流

### 1. 判断 Skill 是否必要

只有当知识具有明确触发、反复出现、无法从代码直接发现、并且需要一套稳定决策/验证流程时创建 Skill。一次性说明、API 列表或项目 README 不自动升级成 Skill。

### 2. 先查已有技能

portable 仓库检查 `MANIFEST.json`；Editor 内调用 `AgentSkillToolset.ListSkills`。若现有 Skill 能通过一个 reference 扩展，不创建重叠 Skill。

### 3. 写路由元数据

`name` 稳定、kebab-case；`description` 同时写“何时用”和关键排除条件，避免“帮助开发 Unreal”这类会匹配所有任务的描述。正文采用渐进披露：决策在 SKILL，长资料在 references。

### 4. 写可执行流程

必须包含适用范围、版本门槛、工作流、验证；对 Editor/MCP 变更写恢复点和权限。项目 Skill 只记录该项目特有的目录、命名、工具、资产约束和 canonical workflow，不重复通用 UE 知识。不要把易变的具体 Tool 名列表写死；要求 Agent 在运行时发现 schema。

### 5. 选择 UE5.8 原生实现

- **Python `UAgentSkill` 子类**：属于代码插件、需要随插件版本控制和加载时自动注册；使用 `@agent_skill` 装饰器，docstring 作为 Description，`instructions` 作为正文。
- **UAsset Skill**：只属于某个项目、希望在 Content Browser 中维护且无需代码。

Python Skill 修改后必须重新加载插件 Python package 再验证；不要把 Remote Execution 默认暴露到不可信网络。两种实现细节见 `references/native-implementations.md`。

### 6. 创建项目原生 UAsset Skill

`CreateSkill`/`UpdateSkill` 是写资产操作，只在用户明确指示后调用。先确认 FolderPath/AssetName，保存前展示 description 和 instructions 摘要。更新前 GetSkills 并保留原内容以便比较。

可先运行：

```bash
python scripts/export_agent_skills.py --selected ue5-blueprint-authoring --output build/agent-skills.json
```

该脚本只生成 payload，不直接修改 Editor。

### 7. 验证触发和冲突

用至少三个正例、三个负例测试 description；检查项目 Skill 与通用 Skill 是否冲突。项目特有规则可覆盖通用偏好，但不能覆盖安全、版本或许可边界。

## 验证

- frontmatter/manifest 校验通过；
- Skill 有清晰非触发场景；
- 只加载 Skill 即可完成核心决策，references 按需读取；
- Editor 原生创建/更新得到用户明确许可；
- List/Get 后内容、路径和描述正确，资产保存可审查。
