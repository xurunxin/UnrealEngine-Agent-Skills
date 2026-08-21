---
name: ue5-project-bootstrap
description: "Bootstrap or normalize a UE5.4+ project workspace, including engine detection, project files, AGENTS instructions, source-control hygiene, plugins, and the first compile/test loop."
---

# UE5 Project Bootstrap

## 适用范围

用于新建、接管或规范化 UE5.4+ C++ 项目/插件工作区，以及为 Coding Agent 建立可重复的首次构建流程。不是 Gameplay 功能实现 Skill。

## 版本门槛

最低 UE5.4。UE5.8 MCP 只是可选能力；没有 MCP 时项目仍应可通过普通构建与 Editor 工作流开发。

## 工作流

### 1. 识别工作区

定位唯一 `.uproject`，记录：

- Engine 根目录与 `Build.version`；
- Source Build 还是 Launcher/Installed Build；
- 主 Editor Target、Game Target、Server Target；
- `Source/`、`Plugins/`、`Config/` 与测试位置；
- Git/LFS/Perforce 状态和二进制资产策略。

如果存在多个 `.uproject`，不要自动选择；用调用方指定的项目路径贯穿所有命令。

### 2. 检查工具链

- Windows：匹配该引擎支持的 Visual Studio/MSVC/Windows SDK；从 UBT 日志确认实际选择，而非只看已安装版本。
- macOS/Linux：确认 Xcode/Clang/SDK 与目标平台。
- Source Build：确认依赖已准备并能生成项目文件；Installed Build：确认 Editor/UBT/UAT 路径。
- 不要把本机绝对 Engine 路径写进可提交的 Build.cs 或配置。

### 3. 建立项目级 Agent 说明

创建精简 `AGENTS.md`，只记录代码无法自动发现的约束：目标 UE 版本、构建命令、模块边界、资产目录、测试入口、禁止操作。不要复制本仓库全部规则。

可从 `examples/project/AGENTS.md` 起步并替换占位符。

### 4. 生成并构建最小 Target

优先调用引擎提供的 GenerateProjectFiles 脚本，然后构建 `<Project>Editor` Development。首次循环只证明：

1. UBT 能解析 Target/Module；
2. UHT 成功；
3. C++ 编译链接成功；
4. Editor 能加载项目模块；
5. 一个聚焦 Automation 测试可运行。

不要在首次构建中同时启用所有可选插件、全平台打包和 Derived Data 预热。

### 5. 源码控制基线

提交源码、配置、描述符和必要内容资产；忽略 `Binaries/`、`Intermediate/`、`Saved/`、`DerivedDataCache/`。团队需要版本化大型资产时使用已约定的 LFS/Perforce 规则，不要由 Agent 擅自迁移仓库。

### 6. 可选启用 UE5.8 MCP

仅在用户需要 live Editor 操作时加载 `ue5-mcp-operator`。先在沙箱项目启用 `ModelContextProtocol` 和最小 Toolset 集，而不是默认启用 `AllToolsets`。

## 验证

- `python <skills-repo>/scripts/verify_engine.py --engine-root <EngineRoot>` 通过；
- Editor Target Development 构建成功；
- Editor 启动时没有项目模块加载失败；
- 项目 `AGENTS.md` 包含真实命令和边界；
- Git 状态不包含生成目录或意外的大型二进制文件。
