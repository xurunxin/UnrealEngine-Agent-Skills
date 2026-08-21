---
name: ue5-source-navigation
description: "Navigate Unreal Engine 5.4+ source safely and efficiently when locating APIs, modules, ownership, call paths, version changes, or engine examples without copying restricted source."
---

# UE5 Source Navigation

## 适用范围

用于回答“这个 API 在哪、属于哪个模块、当前版本怎样调用、为什么链接失败、旧接口替换成什么”等源码问题。也用于为其他 Skill 提供可核验依据。

## 版本门槛

最低 UE5.4。必须搜索任务实际使用的 Engine checkout；本仓库的 UE5.8.1 pin 只在目标版本一致时是最终证据。

## 工作流

### 1. 从项目调用点开始

先读报错或调用点上下至少一个完整类型/函数，记录 include、命名空间、宏条件、Target 类型和模块。仅凭符号名全局搜索容易选到测试桩、平台实现或废弃重载。

### 2. 找声明、定义和当前使用

按顺序查：

1. 声明头文件；
2. 实现文件；
3. 所属模块 `*.Build.cs`；
4. 同一版本 Engine 中的生产调用点；
5. 自动化测试；
6. 插件描述符和加载阶段。

优先使用 `rg`/IDE 索引。不要读取整个 30GB 仓库或把大段源码塞进上下文。

### 3. 识别模块所有权

从 `Engine/Source/{Runtime,Developer,Editor,Programs}` 或 `Engine/Plugins/.../Source/<Module>` 推断 Target 可用性，并用 Build.cs 验证。Runtime 模块不得依赖 Editor 模块；Editor-only API 必须隔离在 Editor Module 或 `WITH_EDITOR` 边界中。

### 4. 识别版本和条件编译

查 `EngineVersionComparison.h`，优先使用 Engine 提供的比较宏。检查 `WITH_EDITOR`、`WITH_EDITORONLY_DATA`、平台宏和插件启用条件。不要只用 `ENGINE_MINOR_VERSION >= N` 拼接复杂跨 Major 判断。

### 5. 形成最小证据摘要

输出 API 路径、所属模块、需要的 include/dependency、线程/生命周期限制、目标版本和当前调用示例位置。只概述实现，不复制受限源码主体。

详细路径入口见 `references/source-map.md`。

## 验证

- 在实际 Engine checkout 找到符号；
- 声明、定义、模块依赖和至少一个当前调用点一致；
- 目标 Target 可以合法依赖该模块；
- 版本/平台/Editor gate 已记录；
- 建议通过最小编译或测试验证，而不是仅凭搜索结果。
