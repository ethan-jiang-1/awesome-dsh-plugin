---
title: "换壳保 id · dfy-bundle：把行 id 当公共契约"
domain: lifecycle
kind: sample
positioning: "从单装改成组合包时，靠沿用同一条目 id 让用户配置存活；退役旧包则明确留给用户层。"
takeaway: "行 id 一旦发布就是公共契约：组合包可以复用 id 保住配置，但不能替用户关掉他装过的东西。"
read_when: "要把多个独立包收成一个组合包；或用户升级后配置“全丢了”。"
status: observed
updated: 2026-11-01
budget: 125
---
# 换壳保 id · dfy-bundle

> **阶段**：配 · **载体**：host-row（一条 insert，8 行复用原 id） · **兼看**：装
> **影响力**：npm 近 30 天 **4,766**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`@dfy-plugins/dsh-bundle@0.1.3`（**registry 无 `gitHead`**，按版本 + tarball 摘要钉），sha256 `b8bbb6a3…`（133,547 B，**8 文件**）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（patch 全量、README 迁移段实读；未实机切换）
> **一句话**：它把自己当成"同一批条目的另一种装法"，而不是"一批新条目"。
> **借鉴价值**：**① 换包装形式时复用同 id；② 行 id 是公共契约，改名等于迁移；③ 退役旧包是用户的事，组合包不越权。**

## 它想干什么 · 为什么值得借鉴

**意图。** 把作者原先散发的 8 个独立插件（壁纸、外观、归档、媒体块、图像生成、可视化、轮次守卫、Codex 桥）收成**一个组合包**，让用户少装几次 `[SRC-TARGET]`（`cordis.patch.yml:1-18`）。

**意义。** 生命周期里"配"与"装"的交界处有一类很常见的伤害：**产品换了个包装，用户的配置与行覆盖全丢**。原因往往是新包给条目起了新 id。这个样本的做法是把"**行 id 当公共契约**"写进 patch 第一句注释。

**用户价值。** 装之前，用户面对 8 个包、8 次安装、8 份 README；装之后一次装齐。更关键的是**升级路径**：以前单装过的人，换成组合包后设置还在，因为他自定义的行覆盖仍然按同一个 id 命中 `[SRC-TARGET]`（`:1-2`）。

**表达。** 注释只有两句，但把责任边界也划了 `[DOC]`：

> Keep the same IDs and module names as the standalone bundles so settings and user row overrides survive switching installation forms.

README 里则讲退役（`README.md:26`）：

> 已停用的单独包应转成同名条目的 `disabled: true` 覆盖。组合包沿用原来的条目 ID，…

**代码里只做 id 复用，退役交给用户层**——这是本卡最值得抄的判断。

## 1. 阶段与载体

- **阶段**：配。它决定"换了包装之后，配置与覆盖还认不认"。
- **载体**：`host-row`——一个 `insert` 块、8 行、全是自有包 `[SRC-TARGET]`（`:1-18`）。
- **兼看**：装。同一批条目有两种装法，是分发形态的问题。

## 2. 机制

```yaml
# cordis.patch.yml:1-18（节选）
# Keep the same IDs and module names as the standalone bundles so settings and
# user row overrides survive switching installation forms.
- insert:
    - id: wallpaper
      name: '@dfy-plugins/dsh-wallpaper'
    - id: appearance
      name: '@dfy-plugins/dsh-appearance'
    - id: archive-manager
      name: '@dfy-plugins/dsh-archive-manager'
    … 共 8 行
```

三件事同时成立：

1. **id 复用**：8 个 id 与独立包一致；
2. **模块名复用**：`name` 也一致（换包名就等于换身份）；
3. **不碰别人的行**：全部是自己的 `insert`，没有覆盖宿主行。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **新包改了 id** | 用户既有的行覆盖与设置不再命中 | 设置"回到默认"，像重装过 |
| **两套都装** | 同 id 被插两次 | 重复注册/覆盖，行为异常 |
| **退役没做** | 旧独立包仍然启用，与组合包同 id | 两份都在跑，排查困难 |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 包装形式 | 组合包，不新增能力 | 8 个包仍要各自维护发布 |
| 迁移策略 | 保 id；退役留给用户 | 用户要自己关旧包（README 明确要求） |
| 包体 | 8 个文件、**无客户端** `[PKG]` | 界面全在成员包里 |
| 责任边界 | 不替用户写 `disabled` | 迁移不"全自动"，但不会越权关掉别人 |

## 4. 与宿主既有行的边界

它是**纯声明式 bundle**：8 个文件里没有 `lib/`，没有客户端，只有 patch、README、locale、icon 与一个 `index.js` `[SRC-TARGET]`。这意味着它的"行为"完全由 patch 与成员包决定——**组合包自己几乎不写代码**。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 产品换包装，用户配置会不会丢 | 新包装**复用原来的行 id 与模块名** | `[SRC-TARGET]` `cordis.patch.yml:1-2`（注释）、`:3-18`（8 行同 id） | 设置与用户行覆盖继续命中；代价是 id 一旦错了就再也改不回来 | 把行 id 列为"发布后不可改"的契约 | 只对"用户按 id 写覆盖"的宿主成立 | 改 id → 用户配置静默失效，像重装 |
| 旧包装要不要自动停用 | **组合包不越权**：只保 id，把旧包转成 `disabled: true` 留给用户层 | `[DOC]` `README.md:26`；`[SRC-TARGET]` patch 里**没有任何 `disabled`** | 不会关掉用户还想要的东西；代价是迁移多一步 | 在升级说明里给出用户层的禁用片段 | 只对"bundle 无权处置他人包"的格式成立 | bundle 里硬写 `disabled` → 关掉用户没打算关的包 |
| 行 id 什么时候能改 | 发布即契约：改 id 等于一次迁移，需要 tombstone 或双挂过渡 | `[SRC-TARGET]` 本包全量复用；对照 [`install/12`](../install/12_让安装器认你-dsh-origin-plugin.md) 的 `duplicate loader entry id` 约束 | 兼容旧用户；代价是永久背负旧 id | 规划新 id 时同时给旧 id 的去留策略 | 只对"有已发布用户"的项目成立 | 直接换 id → 老用户配置全丢，且无痕 |
| 组合包与单装共存 | 明确"二选一"，并在文档里写清冲突形态 | `[SRC-TARGET]` 8 行 insert；`[DOC]` README 迁移段 | 用户知道别叠加；代价是文档要维护两种形态 | 给出"检测到同 id 已存在时怎么办" | 只对"可能并存"的生态成立 | 不说 → 用户两套都装，重复注册 |

## 6. 失效与开放问题

- `[OPEN]` 用户层 `disabled: true` 覆盖与组合包 `insert` 的先后关系（按 DSH 的层序，用户层更晚应胜出；未实测）。
- `[OPEN]` 8 个成员包各自的版本约束（本包 README 是否声明，未逐条读）。
- `[OPEN]` 两套同时装时宿主的具体报错形态。
- `[OPEN]` **无 `gitHead`**，物证止于 tarball 摘要。
- `[OPEN]` 未实机切换安装形态。

## 7. 兼看

- 装：与 [`install/11`](../install/11_装后自证-cfbridge.md)、[`install/13`](../install/13_三条安装路径与空安装器-dsh-free-models-hub.md) 都属"包装形式"问题——**11/13 是包装里少了东西，33 是包装换了但身份不变**。
- 配：用户层覆盖的优先级见 [`config/README.md`](./README.md) §1。
