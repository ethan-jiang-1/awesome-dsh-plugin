---
title: "会话接力：接管的是什么，不是什么"
domain: agent-crossing
kind: card
positioning: "跨会话接力的第一问：替换的是会话、进程、端口还是 UI；以 09 takeover 与 14 rooms 对照，划清“接力”与“搬家”的边界。"
takeaway: "大多数“接管”只新建会话并投递接力指令；不夺进程/端口，也不自动回滚。"
read_when: "要做跨会话接力/接管，或评估一个 takeover 类插件时。"
status: observed
updated: 2026-11-01
---
# 01 · 会话接力

> “takeover”听起来像夺进程，实际多数实现只做**会话层**：新建一个会话、改名、投递一条 `/resume-*` 或 `/inbox` 指令，让模型接着读外部记录。

## 1. 替换对象清单

| 候选 | `dsh-takeover` 是否替换 | 实际 |
|---|---|---|
| 会话 | **是** | `controller.create({})` → `rename` → `prompt(queue, "/resume-<provider> <id>")` |
| 宿主进程 | 否 | `src` 无 spawn/kill/listen/createServer |
| 端口 | 否 | 只在宿主已有 listener 上注册 `/dsh-takeover` 前缀 |
| profile | 否 | 不碰 profile 目录 |
| UI | 否（叠加） | composer chip + settings 卡 + 临时遮罩 |

来源：[`09 memo`](./_证据/09-takeover-源码复核.md)（`afbc55c`，server.ts:256-269）。

## 2. 状态与恢复

- **无自动回滚**：create 成功、rename/prompt 失败时，错误只回传孤儿 `sessionId`，需手动删；外部会话只读，原进程从未被碰。
- **cwd 不继承**：新会话 `create({})` 不传 cwd，模型要先确认目录。
- **权限**：回环 + Host/Origin + `Sec-Fetch-Site` 守卫，但无 token；本机进程可伪造头（与威胁模型“本机可信”一致）。

## 3. 与 rooms 的区别

`team-rooms` 是**房间存储权威 + 成员日志重建**：它不“接管”外部会话，而是让多个会话共享一个房间时间线；在 rc.3 上 `team-room/fact` 被禁，重建副本退化。两者共同点：**跨会话的状态归属必须显式**，否则“接力”只是复制文本。

## 4. 借用与判定

1. 接管替换的到底是哪一层？会话、进程、端口、profile、UI 分别答。
2. 失败时留下什么？孤儿会话、半写文件，还是可回滚的快照？
3. 外部记录是只读还是可写？写坏谁负责？
4. 权限边界是本机用户、回环、token，还是无？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 09 只替换会话，不夺进程/端口/profile | `[SRC-TARGET]` | [`09 memo`](./_证据/09-takeover-源码复核.md)（afbc55c） | 入站路由挂在宿主 listener |
| 09 无自动回滚，失败回传孤儿 sessionId | `[SRC-TARGET]` | 同上（server.ts:297-303） | 外部侧不受影响 |
| 09 的 claim 60s 清扫只在列目录时触发 | `[SRC-TARGET]` | 同上 | 不是定时器；打开失败都报“另一进程” |
| 14 的 fact 事件在 rc.3 被禁 | `[SRC-TARGET]` | [`14 memo`](./_证据/14-team-rooms-源码复核.md)（1.0.8） | 旧日志已有 fact 仍可 fold |
| “接管的是会话不是进程”是跨样本共性 | `[OBS]` | 09/14 横向对照 | 归纳性判断 |

**未验证**：`/resume-*` 在 rc.3 上是否真能读入外部会话、孤儿会话清理后的 relay 残留，均 `[OPEN]`。
