---
title: "源码复核：生成式界面 dsh-genui"
domain: reshape-product
kind: evidence
positioning: "对生成式界面样本卡作固定提交的一手源码、测试、CI 与 DSH rc.3 合约交叉核验；本文件为证据，不替代样本卡。"
read_when: "要复核 GenUI schema/信任边界、流式 fence 生命周期、action dispatch、错误退化、主题所有权或 rc.3 兼容性。"
status: observed
updated: 2026-10-31
---
# 源码复核：生成式界面 dsh-genui

> 取证时点：2026-10-31。只读 GitHub 一手源、测试、README、CI 与 DSH rc.3 源码；未安装、构建或执行目标代码。下文 `[DOC]` = 上游文档主张，`[SRC-TARGET]` = 目标仓库实现，`[SRC-DSH]` = DSH 宿主实现/契约，`[TEST]` = 仓库测试存在性与覆盖意图，`[CI]` = workflow 声明，`[RUN]` = 本次运行事实。目标固定为 `omdsh-dev/dsh-genui` commit [`e00bdcfbf7d4492afc95d5e52af350d6b68882c6`](https://github.com/omdsh-dev/dsh-genui/commit/e00bdcfbf7d4492afc95d5e52af350d6b68882c6)（2026-10-30，签名 verified）；所有目标代码链接均 pin 此 commit。DSH 固定 `dsh-v0.2.1-rc.3` -> [`1f81c047fc48fa190a683e469daa699857e9afe8`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。

## Provenance 与版本界限

- `[SRC-TARGET]` pinned [`package.json`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/package.json) 将 package name 指向 `@changfenhuang/dsh-genui`、version `0.15.0`，repository 指向本仓库；peer ranges 声明 DSH `^0.2.0-rc.1 || ^0.2.1-rc.1 || ^0.2.2-alpha.2`。这些是仓库内元数据，不是 npm tarball provenance/内容证明。
- 样本卡所记“版本范围”与 repo commit 的 metadata ranges 一致，但卡片并未给出精确 package version；现在审计的是 0.15.0 对应的仓库提交，不应倒推卡片曾读过的 npm 包就是该提交。未取 npm 发布包/attestation，也未比较 tarball 内容，包到源码的精确发布对应关系仍是 `[OPEN]`。
- 本次源码快照的 README 与 `package.json` 均描述当前功能；它不是按卡片日期/旧版本固定的 historical baseline。卡片中的版本范围不足以唯一选定历史 tag，所以以请求的第一方当前固定提交为核验对象，并明确版本错位。

## DOC

- README 描述 `dsh-ui` fenced JSON、白名单组件、streaming incremental mount、malformed node sibling continuation、无效 fence 回退、同轮反馈、action 回传、disabled 无 action 控件、trailing debounce、本地交互、session-fingerprint LRU 200 blocks，以及 CSS surface variables。以上分别是文档口径，见 pinned [`README.md`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/README.md)；不可单凭 README 认定实现/安全属性。
- README 同时称 strict JSON / whitelist / “zero script injection or eval”，但也明确外部样式属于 trusted host config，地图默认 offline blank coordinate map；不能将“安全 UI”理解为 iframe/DOM 隔离或安全沙箱。README 未承诺 CSP、iframe、origin isolation、请求速率限制、CSRF token 或 action idempotency。

## SRC-TARGET

- Schema 与节点限制：`SKILL.md` 是字段级格式说明，package export `./skill` 亦映射此文件；schema tests 覆盖 root shape、invalid input、node guards、ECharts/map guard。见 pinned [`SKILL.md`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/SKILL.md), [`tests/genui-schema.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-schema.spec.ts), [`tests/genui-root-shape.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-root-shape.spec.ts), [`tests/genui-guard.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-guard.spec.ts)。本次只确认有这些一手文件/测试，不声称已逐字段穷举数量、深度、字节数或耗时限制；README 对 strict schema 不等于存在全局 node/action 数量上限。需针对特定 DoS 预算再逐项审计。
- Trust boundary：模型 JSON 作为不可信数据走组件白名单；README 的不执行脚本主张是产品设计说明，不构成浏览器权限边界。ECharts full-option、Mermaid、媒体 URL/链接等复杂输入应按各自 guard/render path 看待。当前复核没有证明所有属性/URL scheme 都拒绝外域或 `data:`，也没有证明隔离。地图文档明确 style 属 trusted host config、非 JSON；见 pinned [`docs/map.md`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/docs/map.md)。
- Streaming/render lifecycle：README 描述 DOM fence channel，测试文件表明存在 DOM fence、partial render、skeleton、fallback、RAF cleanup、ordinal 定位覆盖；见 [`tests/dom-fence.spec.tsx`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/dom-fence.spec.tsx), [`tests/genui-partial-render.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-partial-render.spec.ts), [`tests/dom-fence-raf-cleanup.spec.tsx`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/dom-fence-raf-cleanup.spec.tsx), [`tests/genui-fence-fallback.spec.tsx`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-fence-fallback.spec.tsx)。这是对流式路径有测试，不是对所有异步资源/卸载竞态无泄漏的证明。
- Malformed fallback：独立测试覆盖 invalid input、fence fallback、partial fence/render、repair JSON quote/trailing junk/CJK punctuation 等；见 [`tests/genui-invalid-input.spec.tsx`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-invalid-input.spec.tsx), [`tests/fence-repair-json-quotes.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/fence-repair-json-quotes.spec.ts), [`tests/fence-repair-trailing-junk.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/fence-repair-trailing-junk.spec.ts)。卡片“坏节点单独丢弃、兄弟继续”与 README 的 node-level claim 相符，但此处不把测试文件名/README 代替实现逐分支审读；不支持该块、无效 fence 保留 Markdown 的 fallback 路径有测试。
- Action：README 说 action payload 进入模型 event loop、无 action 按钮 disabled、离散立即/连续 debounce。测试目录有 `genui-debounce`, `genui-debounce-handler`, fence feedback/agentloop、gallery feedback、action-related schema coverage；见 [`tests/genui-debounce.spec.tsx`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/genui-debounce.spec.tsx), [`tests/fence-feedback-agentloop.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/fence-feedback-agentloop.spec.ts), [`tests/fence-feedback.spec.ts`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/tests/fence-feedback.spec.ts)。Action 是传给宿主/模型的交互意图，不是授权后的业务服务调用；本复核未发现可以据以宣称 CSRF 防护、确认 UI、幂等键、重复点击抑制或 at-most-once dispatch。把“用户点击”称为确认并不等于业务操作有独立 confirmation gate。
- CSS/theme ownership：README 记载 surface chain `--dsl-g-surface` -> `--dsh-genui-surface` -> host alias fallback，并为 flat/table 单独留变量；组件 CSS 与 theme tests 在 pinned tree 中。此设计暴露插件 token，不应由插件反写宿主 token；具体 cascading/selector scope 未在本次展开逐声明核验。README 也给出 `card.flat` 与 `table` 默认无表面的例外，故“一个 surface 变量控制全部背景”不准确。
- Source/transport errors：README 指出 ECharts/Mermaid/3D 资源经插件 static route lazy-load；故网络、HTTP/static route 与 engine init 是 UI 资源链路的一部分。repo 有 asset loader / error boundary / lazy asset tests，但未执行网络故障注入。不能声称任意 fetch/engine 错误均退回 Markdown；Markdown fallback 是 fence/schema/render eligibility 路径，不等于 chunk 加载错误可以复原。

## SRC-DSH

- DSH `dsh-v0.2.1-rc.3` 固定到 commit `1f81c047fc48fa190a683e469daa699857e9afe8`。GenUI pinned package peer range 覆盖 rc.3，仓库 CI 的 `current` host-ref 也明确选 `dsh-v0.2.1-rc.3`；这是声明与 CI 配置匹配，不代表本次 CI 实际通过。
- GenUI 通过 conversation DOM/fence 检测集成，而不是一个 native fenced-code replacement slot。DSH rc.3 的 conversation chat node slot 是节点级 UI 接缝；不能把它说成 fence-level parser API。GenUI 的 DOM observation 与 DSH slot contract 属不同机制。本 memo 未把宿主 slot 当作 GenUI 内部实现来源。
- DSH renderer registry/factory 的 disposer 生命周期只在比较插件服务模式时相关；rc.3 源码定义 slot/factory 注册与宿主生命周期，不替 GenUI 的 MutationObserver/DOM patch 生命周期背书。要声称 DOM observers 全都随禁用/卸载清理，必须以目标插件实际 cleanup 实现为证，本次不作推断。

## TEST

- 源树测试集覆盖 schema/root shape、invalid fences/fallback、partial/streaming DOM、RAF cleanup、反馈 agent loop、debounce、theme、asset loader、地图/eCharts/Mermaid guards 与 gallery acceptance。此处只核对测试源存在和覆盖主题，不运行测试、不宣称通过。
- action dispatch 的业务确认/幂等/CSRF 与全局 payload size/node-count 压力边界，未见由上述测试名称或 README 可证明的保障；未读取全体测试断言做覆盖率或 completeness 结论。

## CI

- pinned [`.github/workflows/ci.yml`](https://github.com/omdsh-dev/dsh-genui/blob/e00bdcfbf7d4492afc95d5e52af350d6b68882c6/.github/workflows/ci.yml) 声明 Linux Node 22/24 current rc.3、Node 24 minimum rc.1 lanes；有 typecheck/full unit/build、host API checks、packed smoke/E2E、gallery/computed/map browser acceptance、Windows Node 22/24 build/pack，以及另一个 browser typography/theme/interaction workflow job。workflow 内容只能证明配置存在，不能证明该 commit 的 job 绿灯。
- README 报告真实宿主/打包验收目标与 CI 版本；旧样本卡“只读 README 全文、未单独存盘”的历史证据深度，不能自动升级为当前 commit 源码级验证。

## RUN

- 本轮仅用 GitHub 一手 HTTP 页面/API 只读固定 commit、tag 与文件；没有 clone、安装、构建、测试、运行目标插件或发起 action。
- 因未执行，README 的 60 FPS、sub-millisecond、200–800 token 等作者性能/成本口径均未测量；CI pass 状态也未查询。
