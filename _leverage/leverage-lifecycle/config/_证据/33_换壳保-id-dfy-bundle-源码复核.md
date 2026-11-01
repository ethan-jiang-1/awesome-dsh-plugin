---
title: "证据 33 · dfy-bundle 源码复核（0.1.3）"
domain: lifecycle
kind: evidence
positioning: "固定版本（无 gitHead）、tarball 摘要、八行同 id 的 patch 全文与 README 迁移段的对照。"
read_when: "复核 config/33；或想知道“换包装不丢配置”靠什么。"
status: observed
updated: 2026-11-01
budget: 90
---
# dfy-bundle 源码复核

> **固定版本**：`@dfy-plugins/dsh-bundle@0.1.3`
> **gitHead**：**registry 未记录**
> **tarball**：`https://registry.npmjs.org/@dfy-plugins/dsh-bundle/-/dsh-bundle-0.1.3.tgz`
> **sha256（前 24 位）**：`b8bbb6a35e2afc15daa30d29…` · **大小**：133,547 B · **文件数**：**8**
> **抽取位置**：`.work/mine/_dfy-plugins_dsh-bundle/package/`

## 1. 完整文件清单（8 个）

```text
./LICENSE
./README.md
./cordis.patch.yml
./icon.png
./index.js
./locale/en.json
./locale/zh.json
./package.json
```

**没有 `lib/`**；`dsh.client` 为 `false`（纯声明式组合包）。

## 2. patch 结构

```text
$ grep -c "^- insert:" cordis.patch.yml
1
$ grep -c "disabled" cordis.patch.yml
0
```

- 一个 `insert` 块，8 行；
- **没有任何 `disabled` 覆盖**。

## 3. 关键原文

```yaml
# cordis.patch.yml:1-2
# Keep the same IDs and module names as the standalone bundles so settings and
# user row overrides survive switching installation forms.

# :3-18 —— 8 行，id 与独立包一致
- insert:
    - id: wallpaper         name: '@dfy-plugins/dsh-wallpaper'
    - id: appearance        name: '@dfy-plugins/dsh-appearance'
    - id: archive-manager   name: '@dfy-plugins/dsh-archive-manager'
    - id: media-blocks      name: '@dfy-plugins/dsh-media-blocks'
    - id: image-generation  name: '@dfy-plugins/dsh-image-generation'
    - id: visualize         name: '@dfy-plugins/dsh-visualize'
    - id: turn-guard        name: '@dfy-plugins/dsh-turn-guard'
    - id: codex-bridge      name: '@dfy-plugins/dsh-codex-bridge'
```

```markdown
<!-- README.md:26 -->
已停用的单独包应转成同名条目的 `disabled: true` 覆盖。组合包沿用原来的条目 ID，…
```

## 4. 文档与包体的差异（本卡核心）

| | 说法 | 实际 |
|---|---|---|
| 保 id | README 与 patch 注释都写了 | ✅ patch 8 行确实复用 id |
| 退役覆盖 | README 说"应转成 `disabled: true` 覆盖" | ❌ **patch 里没有** |

**但这不是遗漏**：组合包无权替用户关掉用户自己装的包。README 的这句是**迁移指引**（写给用户），不是 bundle 的自我声明。本卡把它写成"责任边界"，而不是"文档与代码不一致"——这是本册唯一一次如此判定，理由与依据都在上面。

## 5. 未复核

- 用户层 `disabled: true` 与组合包 `insert` 的层序关系（未实测）。
- 8 个成员包的版本约束声明。
- 两套同装时宿主的具体报错。
- **无 `gitHead`**。
- 未实机切换安装形态。
