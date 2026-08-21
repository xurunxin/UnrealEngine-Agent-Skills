---
name: ue5-performance-profiling
description: "Investigate and improve UE5.4+ CPU, GPU, memory, loading, shader, asset, and network performance using evidence-first profiling and changes that preserve frame and thread safety."
---

# UE5 Performance Profiling

## 适用范围

用于帧率、卡顿、内存、加载、Shader、资产体积、网络和 Editor/Build 性能问题。只有存在测量目标或性能回归时触发。

## 版本门槛

最低 UE5.4。工具界面可能随 Minor 变化，但证据流程不变；使用目标版本 Unreal Insights 和平台 GPU 工具。

## 工作流

### 1. 定义预算和场景

明确平台、构建配置、地图、镜头/玩家数、分辨率、目标帧时间、测试时长和是否 Editor。不要用 Editor Development 的偶然数据代表 Shipping 性能。

### 2. 先分类瓶颈

通过 `stat unit`/Insights/平台工具判断 Game、Render、RHI、GPU、IO、Memory 或 Network。不要在不知道主瓶颈时随机改 Tick、材质或线程。

### 3. 捕获可比较 Trace

固定输入与暖机过程，记录 commit 和配置。捕获基线、修改后和回归场景。关注长尾 spike，而不仅是平均值。

### 4. 从高成本调用路径下钻

- Game Thread：Tick、Blueprint VM、Actor/Component 数、同步加载、GC；
- Render/GPU：Pass、Draw/Primitive、材质、阴影、带宽；
- Loading：Asset Manager、依赖树、IO、解压、Shader/PSO；
- Memory：对象/纹理/网格/容器、泄漏和峰值；
- Network：复制频率、属性/Actor 数、RPC、带宽和队列。

### 5. 做单一可归因改动

先减少工作量，再缓存，再异步/并行；并行前证明数据和 UObject 线程安全。不要用关闭验证、延长 GC 或牺牲正确性的开关掩盖根因。

### 6. 建立门禁

保存可重复的 profile 场景、关键统计和允许波动。对性能敏感模块增加 trace marker、计数器或自动 smoke，而不是只留截图。

## 验证

- 同场景同配置有前后数据；
- 改动改善主瓶颈而非把成本转移到另一线程；
- 视觉、网络和 Gameplay 正确性不回退；
- 内存峰值和加载时间同时检查；
- 结果在目标硬件而非仅开发机复现。
