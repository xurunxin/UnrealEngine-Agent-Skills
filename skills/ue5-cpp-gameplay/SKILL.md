---
name: ue5-cpp-gameplay
description: "Implement or review UE5.4+ gameplay C++ using Unreal ownership, lifecycle, delegates, components, subsystems, async work, containers, logging, and safe UObject-aware patterns."
---

# UE5 C++ Gameplay

## 适用范围

用于 Actor、Component、Subsystem、Gameplay 服务、输入、状态、委托、异步任务和一般 Runtime C++。反射声明细节同时加载 `ue5-uobject-reflection`；公开给 Blueprint 时加载 `ue5-cpp-blueprint-interop`。

## 版本门槛

最低 UE5.4。任何从旧教程带入的 include、指针或生命周期模式都必须在当前源码中验证。

## 工作流

### 1. 识别对象和生命周期

确认代码运行于构造函数、`PostInitProperties`、`OnRegister`、`BeginPlay`、Tick、销毁还是 Subsystem 生命周期。构造函数只创建默认子对象和设置默认值，不读取尚未存在的 World/玩家/资产状态。

### 2. 选择引用类型

- 反射持有的强 UObject 引用：优先 `UPROPERTY` + `TObjectPtr`；
- 可失效非拥有引用：`TWeakObjectPtr`；
- 延迟加载资产/类：`TSoftObjectPtr` / `TSoftClassPtr`；
- 类型约束：`TSubclassOf`；
- 非 UObject 资源：RAII、`TUniquePtr`/`TSharedPtr`，不要让 SharedPtr 管理 UObject。

跨帧保存 raw UObject 指针必须有明确生命周期证明；否则改用受 GC 感知的类型。

### 3. 保持 Game Thread 边界

多数 UObject、Actor、World 和资产操作在 Game Thread。后台任务只处理线程安全的值数据；回到 Game Thread 后再次验证弱引用。不要从 worker thread 广播会触碰 UObject 的委托。

### 4. 减少隐式每帧成本

默认关闭 Tick，只有真正每帧工作时启用；优先事件、Timer、Subsystem 更新或批处理。缓存查找结果前先证明失效策略。避免在 Tick 中同步加载、遍历全 World、构造日志字符串或频繁分配。

### 5. 错误、日志和不变量

- 可恢复输入问题：返回明确结果或记录分级日志；
- 开发期不变量：`ensure` 允许继续，`check` 只用于不可恢复且确实不应发生的条件；
- 不要吞掉失败，也不要在高频路径刷屏；
- 日志包含对象、World/NetMode 和关键参数，不包含秘密。

### 6. 小步实现

先写数据契约和最小行为，再接 Blueprint/网络/资产。一次变更同时更新头文件、实现、模块依赖和测试，避免“先让它编译再补生命周期”的半成品。

更多模式见 `references/gameplay-patterns.md`。

## 验证

- 构造、BeginPlay、销毁与地图切换路径正确；
- PIE 多实例和 Dedicated Server 不依赖本地玩家/Editor；
- worker thread 不触碰非线程安全 UObject 状态；
- 反射引用可被 GC 正确追踪；
- 最小 Editor/Game Target 编译并运行聚焦自动化测试。
