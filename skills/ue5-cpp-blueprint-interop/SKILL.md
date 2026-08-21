---
name: ue5-cpp-blueprint-interop
description: "Choose and implement UE5.4+ C++ and Blueprint interoperability, including exposure metadata, events, interfaces, function libraries, data contracts, soft references, and stable designer-facing APIs."
---

# UE5 C++ and Blueprint Interop

## 适用范围

用于决定哪些能力暴露给 Blueprint、如何设计 UFUNCTION/UPROPERTY/接口/事件，以及修复 Blueprint 调用或继承问题。

## 版本门槛

最低 UE5.4。修改反射签名后按 `ue5-uobject-reflection` 执行冷编译和 Blueprint 兼容验证。

## 工作流

### 1. 定义设计者契约

先写出 Blueprint 使用者需要完成的任务，而不是逐个暴露 C++ 内部函数。API 应使用领域名词、明确单位、合理默认值和窄输入范围。

### 2. 选择交互形式

- C++ 提供操作：`BlueprintCallable`；
- 无副作用查询：谨慎使用 `BlueprintPure`，避免隐含昂贵工作；
- Blueprint 必须实现：`BlueprintImplementableEvent`；
- C++ 有默认实现且 Blueprint 可覆写：`BlueprintNativeEvent`；
- 多类型协作：UInterface；
- 无状态通用操作：Blueprint Function Library；
- 设计数据：USTRUCT/DataAsset；
- 异步流程：Latent/Async Action，并定义取消和 World Context。

### 3. 保持数据边界稳定

公开 USTRUCT 字段和函数参数会进入资产序列化与图连接。重命名/改类型前规划迁移、重定向或兼容包装。优先软资产引用，避免设计数据无意强加载大型内容树。

### 4. 限制可写范围

默认 `BlueprintReadOnly`，通过方法维护不变量。只有设计师确实需要任意写入且不会破坏状态时使用 `BlueprintReadWrite`。私有属性通过 `AllowPrivateAccess` 暴露前确认这不是绕过封装。

### 5. 错误和上下文

不要让 Blueprint 依赖空 World、固定玩家 0 或 Editor-only 单例。对可失败操作返回清晰的 bool/enum/result struct，并用日志补充诊断；不要让失败静默产生半修改状态。

### 6. 兼容改动

新增 API 优先；废弃旧 API 时提供迁移窗口和 DeprecationMessage。修改事件名、参数顺序、枚举值或 Struct 布局前查引用并测试已有 Blueprint 资产加载。

## 验证

- C++ 完整编译并重启 Editor；
- Blueprint 节点显示名称、类别、Pin 和默认值正确；
- 旧资产加载时没有断 Pin/Unknown Struct/失效父类；
- 失败路径在 Blueprint 可判断；
- 公开 API 未泄露 Editor-only 类型或内部所有权。
