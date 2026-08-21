---
name: ue5-build-cook-package
description: "Build, cook, stage, package, archive, or patch UE5.4+ projects with UBT, UAT, BuildCookRun, IoStore, configuration control, log triage, and reproducible artifact checks."
---

# UE5 Build, Cook, and Package

## 适用范围

用于 UBT 编译、UAT、BuildCookRun、Cook、Stage、Pak/IoStore、Archive、Dedicated Server、补丁与构建失败。普通代码编译问题可先用 `ue5-modules-plugins`。

## 版本门槛

最低 UE5.4。命令行参数和默认值按目标 Engine 的 UAT 帮助与 AutomationTool 源码验证；不要把旧版本博客命令作为固定模板。

## 工作流

### 1. 固定构建契约

记录 Engine commit、`.uproject`、Target、Platform、Configuration、Cook flavor、是否 client/server、是否 Pak/IoStore、Archive 目录和 Source Control 模式。一个命令只对应一个可描述产物。

### 2. 分阶段定位

将失败分为：

1. UBT/UHT 编译；
2. Cook 资产加载/引用；
3. Stage 文件布局；
4. Pak/IoStore 容器；
5. Deploy/Archive；
6. 打包程序启动与运行时依赖。

先运行失败的最小阶段，不反复清空所有缓存碰运气。

### 3. 使用 Engine 脚本入口

Windows 使用 `Build.bat`/`RunUAT.bat`，Unix 使用对应 `.sh`。统一传入绝对 `.uproject` 和显式输出目录，开启 UTF-8 日志。CI 不依赖交互式 Project Launcher 配置。

### 4. Cook 诊断

关注第一个 LoadError、Unknown Cook Failure 之前的真实错误、缺失类/插件、重定向器、Editor-only 引用、Primary Asset 规则和大小写差异。不要把“在 Editor 能打开”当作 Cook 可用证明。

### 5. IoStore/Patch

补丁必须基于固定且可追溯的基线 manifest/container。保持版本号、Cook 参数、加密/签名和 Chunk 规则一致；先在副本安装目录验证。不要把硬件/云分发问题混进内容差异算法。

### 6. 产物验证

记录文件哈希、版本元数据、容器列表、启动日志和 smoke test。对 Client/Server 分别验证目标可执行文件、地图和网络握手。

常用命令模板见 `references/commands.md`。

## 验证

- 构建命令可从干净 shell 重现；
- Cook/Stage/Package 每阶段日志可定位；
- Archive 不混入旧产物；
- 打包程序在未安装开发工具的测试环境启动；
- 补丁只修改预期容器并能从指定基线升级。
