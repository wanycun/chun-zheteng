---
title: 大火花：Electron 版自媒体账号批量管理，停在半成品
summary: 想做一个小工具把多个平台的账号统一管起来，Electron 壳和界面都成了，卡在原生绑定那一层，最后没继续。
status: 暂停
startDate: 2026-05-31
endDate: 2026-06-02
cost: 0
hours: 14
stack: [Electron, Node.js, IPC, 前端]
tags: [Electron, 桌面应用, 半成品]
changelog:
  - date: 2026-05-31
    note: 主界面和账号列表跑起来。
  - date: 2026-06-02
    note: 卡在原生模块绑定，调试脚本一堆但没解决。
---

## 背景

手上同时维护好几个平台的账号，每次都要重复登录、重复发内容、重复看数据。
想做个本地小工具：**账号在一个界面里，发布和查看都从这里走**。

为什么是 Electron：我需要真实浏览器内核（登录态、页面交互），又要桌面端的本地文件能力，Electron 是唯一顺手的选择。

## 方案

```
main.js      主进程：窗口、文件、原生能力
preload.js   只暴露必要的 IPC 接口（不开 nodeIntegration）
renderer/    界面：账号列表 + 操作面板
accounts.json 账号配置
```

安全上刻意做了限制：渲染进程不开 Node 集成，所有能力走 `preload` 白名单。

## 过程

界面部分很快：账号增删改查、分组、状态展示，两天就成型了。

然后撞上 Electron 的老问题——**原生模块（native binding）和 Electron 的 ABI 不匹配**。
表现是一调用就崩，或者直接报 `NODE_MODULE_VERSION` 不一致。

那一阵留下了不少调试残骸，现在还在目录里：

```
test_binding_detailed.js
test_binding_names.js
test_electron_binding.js
bindings_output.txt
electron_err.txt
```

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 加载原生模块直接崩 | 模块按 Node 的 ABI 编译，Electron 是另一套 ABI | 需要 `electron-rebuild` 重编译，或改用 `prebuild` 版本 |
| 重编译后 ABI 对上了但运行时报别的错 | 模块依赖的系统库版本不一致 | 放弃该模块，换纯 JS 实现 |
| 打包后体积巨大 | 直接打入了 `node_modules` 全量 | 用 `electron-builder` 的 asar + 白名单 |
| 调试信息看不到 | 主进程日志没接出来 | 主进程日志写文件 + `--enable-logging` |

## 结果

**半成品，停在这里。**

- 主界面、账号管理能用
- 发布流程没接完
- 卡点是原生绑定，不是业务逻辑

## 复盘

- **Electron + 原生模块是最大的坑**，能用纯 JS 解决的就别碰 native
- 半成品其实不算失败：它验证了"统一界面管账号"这件事的结构是可行的
- 真正该反省的是**范围**——账号管理 + 发布 + 数据看板一次做完，注定做不完；只做"账号列表 + 一键打开对应后台"反而当天就能用

现在类似的活儿基本用浏览器自动化 + 脚本解决了，Electron 这一层其实不需要。
