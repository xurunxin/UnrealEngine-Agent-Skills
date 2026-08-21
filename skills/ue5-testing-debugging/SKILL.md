---
name: ue5-testing-debugging
description: "Plan, implement, run, and diagnose UE5.4+ tests and failures using Automation specs, functional tests, logs, ensures/checks, crash artifacts, focused reproduction, and CI-friendly commands."
---

# UE5 Testing and Debugging

## 适用范围

用于新测试、回归、Automation、Functional Test、崩溃、ensure、编译后运行失败、CI 不稳定和日志诊断。

## 版本门槛

最低 UE5.4。测试命令和 flags 应从实际 Engine 帮助/现有 CI 验证；旧 UE4 命令只作为迁移线索，不复制后直接运行。

## 工作流

### 1. 先构造最小复现

记录 Engine commit、Target、Configuration、Platform、地图、PIE/Standalone/Commandlet、启用插件和输入数据。把“偶发”转成可重复步骤；不要先大范围重构。

### 2. 选择测试层级

- 纯算法/值类型：低成本 Automation；
- UObject/模块行为：EditorContext spec；
- World/Actor：带测试 World 或 Functional Test；
- 资产编译/导入：Editor/Commandlet 测试；
- 网络：专用 client/server harness；
- Cook/Package：UAT smoke 与打包产物启动测试。

### 3. 编写稳定测试

测试名按产品域分层，显式创建/销毁状态，不依赖测试顺序、本机 Content Browser 或固定时间 sleep。异步测试等待明确条件并有超时。每个错误分支使用预期日志/错误断言。

### 4. 诊断顺序

1. 第一个编译/UHT/加载错误；
2. 首个 ensure/check 调用栈；
3. 本模块日志和对象生命周期；
4. 线程、World、NetMode；
5. 最近差异；
6. 最小源码/配置二分。

不要被后续成百上千条级联日志带偏。

### 5. 崩溃资料

保存完整日志、Callstack、minidump、CrashContext、构建符号和 commit。确认是否发生在退出/GC/异步回调。只在证据支持时归因于引擎 Bug。

### 6. CI

使用 `UnrealEditor-Cmd`、`-unattended`、明确测试过滤器和报告目录。失败时保留日志/报告/Crash artifacts。把快速门禁和长时 Cook/平台测试分层。

参考 `references/test-matrix.md`。

## 验证

- 新测试在无缓存/干净进程至少运行一次；
- 失败测试确实因修复前问题失败；
- 没有依赖本机绝对路径、UI 或顺序；
- CI 命令返回值与报告结果一致；
- 调试结论有日志、调用栈或源码路径证据。
