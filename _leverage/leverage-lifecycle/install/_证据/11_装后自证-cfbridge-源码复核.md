---
title: "证据 11 · cfbridge 源码复核（0.13.2）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、符号命中与 files 白名单的原始记录，用于复核装后自证卡。"
read_when: "复核 samples/install/11；或想知道这条结论是怎么从 tarball 里读出来的。"
status: observed
updated: 2026-11-01
budget: 90
---
# cfbridge 源码复核

> **固定版本**：`@wenaixi/cfbridge@0.13.2`
> **gitHead**：`0e46aa200e291ab8c05b0cd570d3cacb9ed0e304`
> **tarball**：`https://registry.npmjs.org/@wenaixi/cfbridge/-/cfbridge-0.13.2.tgz`
> **sha256（前 24 位）**：`64521a2d5e9b38a97dc57f3b…` · **大小**：200,864 B · **文件数**：32
> **抽取位置**：`.work/mine/_wenaixi_cfbridge/package/`（`.work/` 已 gitignore）

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.13.2` |
| `dsh.bundle` | 有（`./cordis.patch.yml`） |
| `dsh.client` | 有（`platform: web`） |
| `bin` | **无** |
| `files` | `cordis.patch.yml` · `lib/` · `skills/` · `locale/` · `icon.png` · `README.md` · `LICENSE` · `.env.example` · `README.zh.md`（`package.json:37`） |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

| 符号 | 命中 | 位置 |
|---|---|---|
| `failOnStartupError` | 10 | `lib/config-healer.js`（多处）、`cordis.patch.yml:25` |
| `!!js` | 3 | `lib/config-healer.js`、`cordis.patch.yml:23` |
| 其他载体符号 | 0 | — |

**说明**：没有 `webServer.register` / `commands.register` / `agents.create` / `installBundle` 命中，所以本卡的载体是 `host-row` + npm scripts，不是自带 CLI。

## 3. 关键原文

```yaml
# cordis.patch.yml:16-31
- id: mcp-cloudflare
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    headers:
      Authorization: !!js '`Bearer ${process.env.CLOUDFLARE_API_TOKEN}`'   # :23
    failOnStartupError: false                                             # :25
    reconnect: { enabled: true, initialDelayMs: 500, maxDelayMs: 30000, maxAttempts: 10 }
```

```json
// package.json:63-67
"install:bundle":   "node scripts/install-bundle.js",
"uninstall:bundle": "node scripts/uninstall-bundle.js",
"validate:bundle":  "node scripts/validate-bundle.js",
"dump:config":      "node scripts/dump-config.js",
"repair:config":    "node scripts/repair-config.js"
```

## 4. 负向事实（本卡核心）

```text
$ find . -type f | wc -l
32
$ find . -name '*install-bundle*' -o -name 'scripts' -maxdepth 2
（空）
```

- `files` 白名单（`package.json:37`）不含 `scripts/`；
- tarball 内不存在 `scripts/` 目录，也不存在任何 `*-bundle.js`；
- 而五条 npm scripts 全部指向 `scripts/*.js`。

**结论**：五条自证命令只对仓库克隆者可用；对 npm 安装者全部不可执行。这是一条 `[SRC-TARGET]` 级负向事实，不是推测。

## 5. 未复核

- `scripts/validate-bundle.js` 的真实校验内容（tarball 内不存在，需装仓库源码）。
- `lib/config-healer.js` 的 `failOnStartupError` 十处命中分别做什么（本卡只引了 patch 那一处）。
