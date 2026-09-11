---
name: ue5-modules-plugins
description: "Configure UE5.4+ modules and plugins or diagnose Build.cs, Target.cs, exports, dependencies, and loading failures."
---

# UE5 Modules and Plugins

## 适用范围

用于 `.Build.cs`、`.Target.cs`、`.uplugin`、`.uproject` 模块配置、API 导出、链接错误、加载失败和模块重构。

## 版本门槛

最低 UE5.4。不要从旧模板复制 BuildSettings/IncludeOrder 值；从目标 Engine 生成的当前项目/插件和相邻模块取基线。

## 工作流

### 1. 明确模块类型

定义 Runtime、Editor、Developer、Tests 或 Program 的实际消费者。只有 Editor 需要的依赖放入 Editor Module；测试代码不要进入 Shipping Runtime。

### 2. 整理 Public/Private 边界

- Public 头文件只暴露消费者真正需要的类型；
- Public 头中出现的外部类型通常意味着 PublicDependency；
- 只在 `.cpp`/Private 使用的模块放 PrivateDependency；
- 优先前置声明和私有实现，减少传递 include；
- 不用“把所有依赖都放 Public”解决编译错误。

### 3. 配置 ModuleRules/TargetRules

从该版本生成的模板开始，固定明确的 PCH、C++、BuildSettings 和 IncludeOrder 策略。跨 Minor 插件禁止 `Latest`，因为新引擎会改变其含义。只有确有需要时设置定义、异常、RTTI 或 Unity Build 行为。

### 4. 描述符和加载

在 `.uplugin`/`.uproject` 中设置正确 Module Type、LoadingPhase、平台/Target allow-list 和插件依赖。`StartupModule` 做注册，`ShutdownModule` 对称注销；不要在静态初始化阶段访问尚未加载的模块或 UObject 系统。

### 5. 消除依赖环

发现 A↔B 时，不使用 CircularlyReferencedDependentModules 作为常规答案。抽取低层接口/数据模块，或通过委托/模块接口倒置依赖。验证最终 DAG。

### 6. 诊断链接与加载

- 未解析外部符号：检查定义是否编入、API 宏、模块依赖和签名；
- 找不到头：检查拥有模块和 include 路径，不手工加 Engine 私有目录；
- 模块无法加载：检查编译配置、目标类型、二进制版本、插件启用和启动日志。

修改构建规则或排查链接/加载失败时读取 [构建规则检查表](references/build-rules-checklist.md)。

## 验证

- 从干净进程构建最小受影响 Target；
- Runtime Target 不拉入 Editor 模块；
- Public API 消费者无需依赖私有实现模块；
- 插件启用/禁用都得到预期结果；
- Startup/Shutdown 在 Editor 退出和热重载场景无悬空注册。
