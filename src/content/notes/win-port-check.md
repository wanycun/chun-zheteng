---
title: Windows 上一条命令查出谁占用了端口
date: 2026-10-19
tags: [Windows, PowerShell, 排查]
summary: 不用装 netstat 增强工具，两条 PowerShell 命令就能从端口反查到进程和它启动的命令行。
---

被 `Address already in use` 卡住的时候，最快的是这一条：

```powershell
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue |
  Select-Object LocalAddress, LocalPort, State, OwningProcess
```

拿到 `OwningProcess`（PID）之后：

```powershell
Get-Process -Id <PID> | Select-Object Id, ProcessName, Path
```

想连启动参数一起看（能直接看出是哪个项目起的）：

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId = <PID>" |
  Select-Object ProcessId, Name, CommandLine
```

顺手把两个合成一条，以后直接粘贴：

```powershell
$p = 3000
Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue |
  ForEach-Object {
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $($_.OwningProcess)"
    [pscustomobject]@{
      Port  = $p
      PID   = $_.OwningProcess
      Name  = $proc.Name
      Cmd   = $proc.CommandLine
    }
  } | Format-List
```

几个小提醒：

- `Get-NetTCPConnection` 需要管理员权限才能看到**所有**进程的连接，普通权限只能看到自己的
- 端口显示 `TimeWait` 占着，通常等几十秒自己就好了，不用急着杀进程
- 别用 `Stop-Process -Name node`，那会把你正在跑的所有 node 一起杀掉

最后一条是血泪教训。
