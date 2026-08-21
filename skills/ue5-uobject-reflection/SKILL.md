---
name: ue5-uobject-reflection
description: "Author or diagnose UE5.4+ UObject reflection code, UCLASS/USTRUCT/UENUM/UFUNCTION/UPROPERTY metadata, UHT failures, generated headers, GC references, serialization, and object pointers."
---

# UE5 UObject and Reflection

## 适用范围

用于 UHT 报错、反射宏、UObject 类型、GC、序列化、属性暴露、RPC/Blueprint 元数据和 generated header 问题。普通非反射 C++ 不必触发。

## 版本门槛

最低 UE5.4。UE4/早期 UE5 的宏组合和指针习惯只可作为迁移线索。

## 工作流

### 1. 检查头文件结构

- `*.generated.h` 必须是该头文件最后一个 include；
- 反射类型必须含正确的 `GENERATED_BODY()`；
- 声明所在模块的 API 导出宏正确；
- UHT 需要完整认识的反射类型不能只靠普通 C++ 前置声明蒙混过关；
- 先修第一个 UHT 错误，后续错误常是级联。

### 2. 选择是否反射

只有需要 Blueprint、序列化、GC、复制、Details、配置、网络或动态调用时才加 UPROPERTY/UFUNCTION。纯内部辅助类型保持普通 C++，减少 UHT 表面和编译成本。

### 3. 设计属性语义

同时决定：可见/可编辑位置、只读/读写、实例/默认值、保存/瞬态、复制、配置、类别和访问级别。不要用 `BlueprintReadWrite` 代替真正的封装；可通过受控函数或 `BlueprintReadOnly` 暴露。

### 4. 保证 GC 可见性

UObject 所拥有的 UObject 引用应通过 UPROPERTY/TObjectPtr、FGCObject 或引擎支持的引用容器被追踪。普通容器中的裸指针不会自动变得安全。非拥有关系使用弱引用；资产依赖根据加载需求使用软引用。

### 5. 处理 UObject 创建

- 构造函数默认子对象：`CreateDefaultSubobject`；
- 运行时 UObject：`NewObject` 并提供正确 Outer；
- Actor：通过 World `SpawnActor`；
- 不要直接 `new` UObject，也不要由 `TSharedPtr` 管理 UObject 生命周期。

### 6. 修改反射签名后的重建

新增/删除 UCLASS、UPROPERTY、UFUNCTION 或改变反射签名时，不依赖 Live Coding 证明最终正确。关闭 Editor 后执行完整编译，必要时清理对应模块生成产物；重新打开并检查 Blueprint 绑定和默认值。

详细检查表见 `references/reflection-checklist.md`。

## 验证

- UHT 与 C++ 编译均无错误；
- Blueprint 中暴露的名称、类别、可编辑性符合契约；
- GC/弱引用测试能覆盖对象销毁；
- 序列化、复制或配置行为有对应测试/运行验证；
- 反射签名变化后完成冷启动验证。
