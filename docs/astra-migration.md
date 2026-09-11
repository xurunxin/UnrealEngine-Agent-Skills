# Astra 技能调整

依据 OpenAI 官方文章 [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)（2026-09-11 查阅）调整任务选择与执行契约。目标是让模型按真实问题选择领域指导，减少无关上下文和机械步骤；没有固定模型名、推理预算或专属运行时依赖。

## 本次调整

- 精简 17 个 description，保留可区分的触发范围，同步 `MANIFEST.json` 和生成的 `CATALOG.md`。任务明确时直接进入领域 Skill，router 用于歧义和跨领域选择。
- router、Skill authoring 与 MCP operator 的入口围绕分支和完成条件组织；已有 API 表、实现示例及恢复矩阵按需读取。保留短而具体的领域知识，没有机械拆散所有技能。
- 仓库 `AGENTS.md` 区分文档维护与 Engine 实现验证。只读 MCP 查询不额外保存资产或停止 PIE；工具自己的状态要求仍须满足。
- 已明确授权的具体动作无需重复确认。确定、可恢复的本次编译错误继续修复并重验；写入超时或返回不明先停止后续写入、重读状态，禁止盲目重试。
- UE5.4+ 最低范围、UE5.8.1 源码 pin、Experimental MCP 门槛、Runtime/Editor 边界、反射冷编译、不直接编辑二进制资产、恢复点、Editor 串行调用及受限源码不外传规则均保留。

## 回归任务

可复用 [routing-cases.json](../evals/routing-cases.json) 中新增的五个任务：

| 场景 | 观察结果 |
|---|---|
| 已定位的 UE5.7 Build.cs 缺失依赖 | 直接使用 modules Skill，修复并构建最小目标，不重新初始化或全量打包 |
| 已连接 MCP，在 PIE 中只读查询 Actor | 读取 schema；工具允许时查询，否则说明限制，不自行保存或停止 PIE |
| 已授权的 Blueprint 新节点发生类型错误 | 修复本次 Pin、重新编译、保存指定资产、重读，不重复确认同一授权 |
| MCP 重命名超时且结果不明 | 先查旧/新路径和日志，不盲目再次重命名 |
| 仅优化 portable Skill 描述 | 同步文本、manifest/catalog 并做仓库检查，不创建 UAsset 或连接 Editor |

执行模型回归时记录实际加载的 Skills/参考资料、工具调用、未授权副作用以及完成证据。目录和 fixture 静态通过只能证明结构一致，不能证明触发正确率、模型质量或 token 节省。

## 实际验证

2026-09-11 在无 Unreal Engine/Editor 的 Python 环境中执行：

- `python scripts/generate_catalog.py --check`：通过，生成目录与实际 Skills 一致。
- `python scripts/validate_skills.py`：通过，17 Skills、12 references；包含 frontmatter、manifest、链接、版本门槛和 routing fixtures 的结构检查。
- `python -m unittest discover -s scripts/tests`：4 项通过。
- `python scripts/export_agent_skills.py --output <temporary-json>`：成功导出 17 项；逐项检查 description/instructions 与当前 Skill 内容一致，明确授权标志仍为 true。未调用 Editor。
- `git diff --check`：通过。

17 个 description 合计从 3,224 降至 1,854 字符（约 42.5%）；17 个完整 SKILL.md 合计从 27,114 降至 25,520 字符，UTF-8 文件字节从 46,072 降至 45,632。高风险工作流新增了必要的恢复与授权范围说明，因此没有按统一比例删减正文；字符和字节统计不是模型 token 或效果测量。

未运行真实 Unreal Editor、C++ 编译、资产保存或 Astra 模型性能比较；新增回归任务已完成结构校验，尚未执行真实模型工具调用。原有 Engine pin 不代表本次重新核验。
