---
title: "证据 14 · tinyfish 源码复核（0.13.0）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、覆盖行原文与“name 是断言”的作者注释。"
read_when: "复核 install/14；或要写一条覆盖宿主行的 patch。"
status: observed
updated: 2026-11-01
budget: 90
---
# tinyfish 源码复核

> **固定版本**：`dsh-tinyfish@0.13.0`
> **gitHead**：`25dc04e6c1809707cf2dad82a466fd131a908b8b`
> **tarball**：`https://registry.npmjs.org/dsh-tinyfish/-/dsh-tinyfish-0.13.0.tgz`
> **sha256（前 24 位）**：`b3a66cf2c7a3ae3c1bb231aa…` · **大小**：57,966 B · **文件数**：12
> **抽取位置**：`.work/mine/dsh-tinyfish/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.13.0` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`） |
| `bin` | 无 |

## 2. 符号命中（S3）

九类载体符号**零命中**——它不改路由、不挂槽位、不注册命令。载体是 **patch 覆盖行**本身，按 `CARRIERS` §3.1 兜底以 patch 声明为准。

## 3. 关键原文

```yaml
# cordis.patch.yml:7-11 —— 作者注释（本卡核心）
# The selection override below matches the web row by `id` alone, with no
# `name`. That is deliberate. In the patch format a `name` field *asserts* the
# target's existing plugin name — it does not rename anything — so writing the
# official web package's scoped name in a third-party bundle claims that
# identity, which is what a patch-safety check reads as impersonation. `name`
# is optional, and a config override needs nothing but the id.
```

```yaml
# cordis.patch.yml:13-18 —— 宿主如何覆盖回来
#   - id: web
#     config:
#       searchProvider: deepseek-official
#       fetchProvider: http
```

```yaml
# cordis.patch.yml:46-49 —— 实际覆盖行（注意：无 name）
- id: web
  config:
    searchProvider: tinyfish
    fetchProvider: tinyfish
```

```yaml
# cordis.patch.yml:40-42 —— 自有行
- insert:
    - id: ...
      name: "dsh-tinyfish"
```

## 4. 与其它卡的呼应

- `config` 整体替换的语义与 [`install/12`](../12_让安装器认你-dsh-origin-plugin.md)「config-only 覆盖且带全字段」是同一条。
- 与 [`config/32`](../../config/32_三档接管-dsh-free-search.md) 改同一个 `web` 行：一个是**安装期覆盖**，一个是**运行时判定接管**。

## 5. 未复核

- 宿主 patch 安全检查判"冒名"的具体实现。
- `searchProvider: tinyfish` 的凭据要求与缺凭据降级。
- 与 free-search 同时装时的优先级。
- 未实机装。
