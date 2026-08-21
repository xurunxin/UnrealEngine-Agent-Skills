---
name: ue5-version-migration
description: "Migrate or audit Unreal projects and plugins toward UE5.4+ while isolating UE4 and UE5.0–5.3 legacy assumptions, validating source-level API changes, build settings, reflection, assets, and behavior."
---

# UE5 Version Migration

## 适用范围

用于 UE4→UE5、UE5.0–5.3→UE5.4+、跨 UE5 Minor 的项目/插件升级，以及审查来源不明的旧教程代码。它是旧版本输入的唯一默认入口。

## 版本门槛

目标基线 UE5.4+。当前核验目标 UE5.8.1。旧版本内容仅用于识别意图和差异，禁止原样粘贴进新实现。

## 工作流

### 1. 固定源和目标

记录源版本、目标版本、引擎 commit、平台和插件矩阵。复制项目/创建升级分支；不要让新 Engine 原地覆盖唯一资产副本。

### 2. 建立清单

按以下类别扫描：

- BuildSettings、IncludeOrder、工具链与警告；
- include/module/API 所有权；
- UObject 指针、反射、序列化、复制；
- Gameplay/Physics/Rendering/Editor API；
- Blueprint 父类、失效节点、Struct/Enum；
- 插件描述符、平台 allow-list；
- Cook、配置和行为变化。

先打开编译数据库/日志，修第一个错误，不进行全局机械替换。

### 3. 一次迁移一个模块

按依赖 DAG 从底层模块开始。每个模块完成：编译 → 自动化测试 → Editor 加载 → 资产/Blueprint 检查。临时兼容层必须有移除条件。

### 4. 源码验证替代旧经验

对删除或改签名 API，搜索目标 Engine 声明、迁移注释、当前调用点和测试。官方升级说明用于发现变化，不代替源码确认。社区答案若未标版本，默认不可信。

### 5. 编写跨版本代码

只在确实支持多个 Engine Minor 时使用 `UE_VERSION_NEWER_THAN_OR_EQUAL` 等宏，并让每个分支都在 CI 编译。不要用无法测试的预处理器森林维持理论兼容。

### 6. 资产升级

资产在新版本保存后通常不可安全回退。分批打开/编译/保存，审查重定向器、父类、默认值和大量 resave。保留旧版本可恢复分支和原始二进制资产。

更详细矩阵见 `references/compatibility-matrix.md`。

## 验证

- 所有支持版本都有实际构建或明确未验证标记；
- 无 `Latest` 隐式改变跨版本构建契约；
- Blueprint/资产在目标版本重开后稳定；
- Cook/Package 与 Runtime smoke 通过；
- 旧兼容分支和弃用 warning 有清理计划。
