---
name: ue5-editor-automation
description: "Automate UE5.4+ Editor workflows with commandlets, Editor Utility tools, Python, subsystems, asset registry, transactions, and unattended-safe scripts without directly editing binary assets."
---

# UE5 Editor Automation

## 适用范围

用于批量资产处理、导入、检查、重命名、保存、Commandlet、Editor Utility Widget/Blueprint、Editor Python 和 CI Editor 脚本。Live MCP 操作优先加载 `ue5-mcp-operator`。

## 版本门槛

最低 UE5.4。先检查目标版本 Python stub 或 C++ API；Editor API 在 Minor 间变化较快，旧脚本必须重新验证。

## 工作流

### 1. 选择自动化载体

- 一次性探索：Editor Python；
- 团队可视化工具：Editor Utility；
- 可测试、性能/权限敏感：Editor C++ Module；
- 无界面批处理/CI：Commandlet 或 `UnrealEditor-Cmd`；
- UE5.8 Agent live 控制：MCP Toolset。

不要用 UI 点击自动化替代稳定 API，除非目标功能没有可用接口且用户接受脆弱性。

### 2. 先做只读清单

通过 Asset Registry/Editor Subsystem 列出候选资产，输出路径、类、包、引用和预期动作。使用完整对象/包路径，避免显示名歧义。批量写之前让用户审阅清单。

### 3. 事务和脏包

交互式 C++ 编辑使用 `FScopedTransaction`，修改对象前调用 `Modify()`，完成后正确标记包 dirty。批处理保存明确包，不调用“保存全部”掩盖意外修改。Commandlet 中明确处理无 UI、无撤销和错误退出码。

### 4. 资产生命周期

使用 AssetTools/EditorAssetSubsystem 等公开接口创建、移动、重命名和删除；处理重定向器和引用者。不要直接移动 Content 下的文件，也不要反序列化后手写 `.uasset`。

### 5. Python 安全

确认 Python stubs 中存在 API；脚本必须可重入、支持 dry-run、限制路径、记录每个修改和失败。不要用 `eval`/`exec` 拼接不可信输入，也不要默认访问项目外文件系统。

### 6. 无人值守验证

脚本返回非零失败，日志包含汇总和具体资产。关闭弹窗、Source Control 交互和本机 UI 依赖。对可能触发编译/Shader/加载的步骤设置合理等待和超时。

## 验证

- dry-run 清单与实际修改集合一致；
- 失败不会留下部分命名/引用损坏；
- 目标资产可重新加载和保存；
- Commandlet 在无人值守环境返回正确退出码；
- Git/Perforce 差异只包含预期资产和配置。
