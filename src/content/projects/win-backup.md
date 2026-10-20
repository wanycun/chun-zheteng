---
title: PowerShell 增量备份：把重要目录按天同步到移动硬盘
summary: 不想装同步盘客户端，用 60 行 PowerShell 做一套带日志、带保留策略的增量备份，插上硬盘自动跑。
status: 已跑通
startDate: 2026-08-11
endDate: 2026-08-14
cost: 0
hours: 4
stack: [PowerShell, robocopy, 任务计划程序]
tags: [Windows, 自动化, 备份, 脚本]
featured: true
changelog:
  - date: 2026-08-12
    note: 加 robocopy /MIR 镜像模式，实测比 Copy-Item 快 3 倍。
  - date: 2026-08-14
    note: 接入事件日志，失败时弹通知。
---

## 背景

重要目录大概 40GB：照片、文档、几个项目的源码。
同步盘方案试过，问题是不想为了备份再养一个客户端，而且云端上传 40GB 太慢。

其实我要的只是：**插上移动硬盘，把变过的文件复制过去**。

## 方案

三个零件拼起来，全都自带：

1. **robocopy** —— Windows 自带的镜像复制，支持增量、支持多线程、能返回状态码
2. **PowerShell 脚本** —— 定义源/目标、写日志、判断返回码
3. **任务计划程序** —— 插上硬盘（事件触发）或每天固定时间跑

关键决策：用 `/MIR`（镜像）还是 `/E`（增量不清删）？

- `/MIR` 会让目标盘**严格等于**源目录，源里删了目标也删 —— 适合做「镜像」，但源文件误删会同步过去
- 最后选了 `/MIR` + **每天另外保留一份当天的压缩快照**（`Compress-Archive` 只压变更目录）

## 过程

核心就一条命令：

```powershell
$src  = 'D:\Documents'
$dst  = 'F:\Backup\Documents'
$log  = "F:\Backup\logs\$(Get-Date -f yyyy-MM-dd).log"

robocopy $src $dst /MIR /R:2 /W:2 /MT:8 /NP /TEE /LOG:$log
$code = $LASTEXITCODE

# robocopy 的 0-7 都算成功，8 以上才是错误
if ($code -ge 8) {
    Write-EventLog -LogName Application -Source 'PowerShell' -EventId 1001 `
        -EntryType Error -Message "备份失败，退出码 $code，详见 $log"
}
```

几个参数值得记：

- `/MT:8` 多线程，机械硬盘上别开太高，8 差不多
- `/R:2 /W:2` 重试 2 次、每次等 2 秒，默认是 100 万次（真的），遇到占用文件会卡死
- `/TEE` 让日志同时进文件和控制台

## 踩坑

| 现象 | 原因 | 解法 |
| --- | --- | --- |
| 半夜任务一直不结束 | 有个文件被占用，robocopy 默认重试到天荒地老 | `/R:2 /W:2` 限制重试 |
| 计划任务里跑 `$LASTEXITCODE` 永远是 0 | 任务计划用的是 `powershell.exe -Command`，脚本没真正接入退出码 | 改成 `-File backup.ps1`，并在脚本里 `exit $code` |
| 系统休眠时错过时间 | 任务计划默认不唤醒 | 勾选「如果错过计划开始时间，请尽快启动任务」 |
| 移动硬盘盘符变了 | USB 顺序不固定 | 用卷标匹配：`Get-Volume -FileSystemLabel BACKUP` |

## 结果

跑了两个月，稳定。

- 首次全量 40GB 约 35 分钟，之后每天增量 10~30 秒
- 日志按天分文件，出问题直接看当天那份
- 失败会写事件日志，配合一个弹窗通知脚本，能第一时间知道

唯一没解决的是**离线异地备份** —— 硬盘和主机在同一个房间，火灾/进水就一起没了。
下一步打算把每周快照再同步一份到 NAS 之外的地方。
