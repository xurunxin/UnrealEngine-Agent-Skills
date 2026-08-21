---
name: ue5-project-architecture
description: "Design a maintainable UE5.4+ project or plugin architecture, choosing gameplay classes, subsystems, modules, data assets, interfaces, ownership, dependencies, and Blueprint boundaries."
---

# UE5 Project Architecture

## 适用范围

用于新系统设计、模块拆分、插件边界、Gameplay Framework 职责、Subsystem 选择、数据驱动方案和 C++/Blueprint 分工。不是对小函数的通用重构触发器。

## 版本门槛

最低 UE5.4。设计必须以项目支持矩阵为准；UE5.8 MCP 可辅助编辑，不应成为 Runtime 架构依赖。

## 工作流

### 1. 从生命周期和所有权出发

先回答系统由谁拥有、何时创建/销毁、在哪些 World/PIE 实例存在、是否复制、是否保存、是否跨地图。根据答案选择：

- Actor/ActorComponent：World 中的实体或可组合行为；
- UObject：非场景对象且需要反射/GC；
- GameInstance/World/LocalPlayer/Engine Subsystem：对应明确生命周期的服务；
- DataAsset/PrimaryDataAsset：稳定、可审查的数据定义；
- Module/Plugin：编译、加载、发布和依赖边界。

不要用全局单例掩盖生命周期问题，也不要为每个类创建一个模块。

### 2. 划分 Runtime 与 Editor

Runtime 代码不得依赖 UnrealEd、AssetTools 或 Editor 子系统。Editor 工具放入独立 Editor Module；共享纯数据契约放在更低层 Runtime 模块。使用接口、委托或模块服务倒置依赖。

### 3. 定义稳定边界

- C++ 负责不变量、性能关键路径、网络权威、生命周期和可测试逻辑；
- Blueprint 负责内容装配、调参、轻量流程和设计迭代；
- DataAsset/Config 负责版本化配置；
- 接口和事件负责扩展，避免 Blueprint 直接依赖深层实现类。

公开 API 要小；模块的 Public 目录不是“常用头文件堆放区”。

### 4. 控制依赖和加载

绘制模块 DAG，标记 Runtime/Editor/Developer/Tests。对可选插件使用软依赖或功能检测；避免主游戏模块反向依赖具体内容插件。加载阶段只做注册等轻量工作，重资源初始化延后到合适生命周期。

### 5. 设计失败与测试

明确无 World、Dedicated Server、PIE 多实例、热重载/Live Coding、资产缺失和异步取消时的行为。为核心纯逻辑提供无地图测试，为 World 行为提供自动化/功能测试。

## 验证

- 每个长生命周期对象有唯一、可解释的 owner；
- 模块依赖无环且 Runtime 不依赖 Editor；
- C++/Blueprint/Data 边界可被一句话说明；
- Dedicated Server、PIE 和地图切换行为已考虑；
- 关键模块可独立编译并有聚焦测试。
