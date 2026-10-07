---
name: ue5-agent-skill-authoring
description: "Create or update portable Unreal SKILL.md instructions or UE5.8 project-native UAgentSkill assets."
---

# UE Agent Skill Authoring

## 适用范围

编写本仓库 portable `SKILL.md`，或创建/更新 UE5.8 项目原生 `UAgentSkill`。仅调用既有技能时不触发。

## 版本门槛

portable Skills 的 UE 内容以 5.4+ 为基线；原生 `UAgentSkill`/`AgentSkillToolset` 要求 UE5.8+ ToolsetRegistry，当前核验 UE5.8.1。

## 工作流

先检查 `MANIFEST.json` 或已连接 Editor 的 `AgentSkillToolset.ListSkills`。复用/扩展已有 Skill，避免重复触发；项目 Skill 只保存项目特有、无法从代码廉价发现的约束。

- **portable 文本**：稳定 kebab-case name、简短且可区分的 description；保留适用范围、版本门槛、工作流和验证。核心决策留在正文，分支专用资料放 references 并写明读取条件。相邻技能容易误触时补排除条件，无需堆砌关键词。目标和完成证据优先于固定步骤数量。
- **插件内 Python Skill**：随代码版本控制，使用 `@agent_skill`、docstring description 与 `instructions`；修改后重新加载插件 Python package，并通过 List/Get 验证。
- **项目 UAsset Skill**：适合 Content Browser 维护的项目知识。`CreateSkill`/`UpdateSkill` 是写资产操作，需用户明确指示；已有指示覆盖本次目标时无需重复询问。调用前确定 FolderPath/AssetName，提供内容摘要/差异并建立恢复点；更新先 Get 保留旧内容。依次调用、检查结果、保存指定资产、重读验证，结果不明确时不重试写入。

选择原生实现时读取 [实现和注册参考](references/native-implementations.md)。工具参数从运行时 schema 获取，不猜测固定 Tool 名/签名；不将 Remote Execution 默认暴露到不可信网络。项目偏好不覆盖引擎版本、权限或源码许可边界。

只需导出可审阅 payload 时执行：

```bash
python scripts/export_agent_skills.py --selected ue5-blueprint-authoring --output build/agent-skills.json
```

该脚本不修改 Editor。维护文本不需要连接 Editor 或新建资产。

## 验证

portable 修改通过 manifest/frontmatter、catalog 和链接检查，并用实际正例和容易混淆的负例检查触发范围；只读取相关 references 即可完成任务。原生变更另需 List/Get 的路径、内容、注册/保存状态与要求一致。结构检查不是模型行为测试；实际未运行的引擎/模型验证分别注明。
