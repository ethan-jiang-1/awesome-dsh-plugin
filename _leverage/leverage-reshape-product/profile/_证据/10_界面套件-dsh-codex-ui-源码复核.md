---
title: "源码复核：界面套件 dsh-codex-ui"
domain: reshape-product
kind: evidence
positioning: "固定 npm 2.0.9 与对应源码，核验模块激活、主题恢复、设置隐藏与宿主扩展边界。"
read_when: "复核 profile/12 的界面套件实现、停用回退和 DSH 版本迁移。"
status: observed
updated: 2026-10-31
---
# 源码复核：界面套件 dsh-codex-ui

> 只读 npm 第一方 metadata、固定 GitHub 源码/测试与 checks；未安装、构建或运行。`[SRC]` 是源码行为，`[TEST]` 是测试定义，`[CI]` 是远端检查结果，不等于本地或任意宿主实测。

## 身份与兼容边界

- **[META]** [npm latest](https://registry.npmjs.org/@michengai%2fdsh-codex-ui) 为 `2.0.9`；[精确版本 metadata](https://registry.npmjs.org/@michengai%2fdsh-codex-ui/2.0.9) 的 `gitHead` 为 `29a999ea8c41918e56a16542c669b258a5194e7a`，指向仓库中[同一 commit](https://github.com/MichengAI/dsh-codex-ui/commit/29a999ea8c41918e56a16542c669b258a5194e7a)，其 [manifest 版本亦为 2.0.9](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/package.json#L1-L4)。坐标一致；未解包或逐字节比对发布 artifact。registry 的 tarball SHA-512 为 `sha512-LXEr7Ki5GslqTh0XFVhX4yfz7SdT8UE5HHPQWbccT3mdnoTkKwkZdi/x8Czo85Y1leMZku25vkRbthRY/SWVEQ==`。
- **[SRC]** DSH engine 和各 DSH client peer 的精确区间是 `>=0.2.0-rc.1 <0.3.0-0`，不是简单的 `<0.3.0`；Cordis peer `>=4.0.2 <5.0.0`，React/React DOM `^18.2.0`。开发用 DSH 包 pin `0.2.1-rc.3`，Cordis `4.0.5`；见 [manifest](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/package.json#L19-L23) 和 [peer/dev dependencies](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/package.json#L103-L158)。声明兼容范围不等于每个版本已验证；迁移时需对齐宿主 Slot、theme、settings 和 primitives 契约，不能把 rc.3 开发 pin 外推为整个区间实测。

## 组合、激活与回退

- **[SRC]** [bundle patch](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/cordis.patch.yml#L1-L16) 插入 session-title、settings-skin、composer、sidebar、theme 与主入口六个独立 row，注释称保留官方壳；这是模块化组合，不是证明每个模块完全独立的微内核运行时。主客户端以 Cordis effect 安装各 observer，关于页注册 `settings.section`，工作区分区先探测 sidebar 状态；见 [client 入口](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/index.ts#L18-L58)。Host 子插件例如 [theme endpoint](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/theme-plugin.ts#L20-L52) 根据 profile 停用状态回报 enabled，effect dispose 注销路由。
- **[SRC]** theme 探活非 2xx、异常或未明确 enabled 时视为关闭，移除追踪的 body CSS token 和 surface style、dispose glass，若曾应用自定义主题则按宿主快照/系统偏好恢复根 `data-ds-theme-source`、`colorScheme` 与 body 暗色标记；停用分支避免静默 `setTheme('system')` 改用户持久偏好，并在可见时重试。切回 stock 另有受限的 runtime 恢复逻辑。[实现](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/theme/index.ts#L25-L520)。**限制：**该文件末尾 observer 的最终 dispose 清理订阅、定时器和 glass，但没有直接执行上述 token/surface/root 恢复；不能将探活失败分支推断成任意卸载路径均彻底清理。首帧可先应用状态、异步探活后回退，并非严格零闪烁的 fail-closed。
- **[SRC]** composer 非成功响应/异常返回 false，但 `observeComposerEnhancements` 在异步探活前先 `activate()`；之后关闭时逆序运行 cleaners、移除自建宽度手柄，React portal 节点交给 slot 注销/React 卸载而不手工删除；焦点、设置 DOM 变化与 15 秒可见轮询触发同步。[实现](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/composer/index.tsx#L30-L190)。sidebar 则探活成功才挂载独立 React root，针对宿主按钮/类选择器插入容器并通过样式隐藏原生项，关闭时卸载 root 和样式；不是纯 Slot，也依赖宿主 DOM 结构。[实现](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/sidebar/index.ts#L14-L190)。

## 设置、Slot 与测试边界

- **[SRC]** theme 设置卡片在 `subPluginEnabled` 为 false 时直接 `return null`，因此该卡片自身无 DOM；不能扩张成整个设置页或所有子插件均零 DOM。它使用宿主 `Switch` 与 `SegmentedControl`，但主题按钮仍自行渲染。[卡片](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/theme/ThemeSettingsCard.tsx#L1-L330)。composer 注册 `conversation.input.dock`，主入口注册 `settings.section`；设置皮肤同时依赖 DOM 装饰和 CSS，并非全量通过 primitives/slots 实现。[composer](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/src/client/composer/index.tsx#L80-L120)、[设置测试](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/tests/settings-skin.spec.ts#L40-L145)。
- **[TEST]** [真实 SlotCore 契约测试](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/tests/sidebar-slot-contract.spec.ts#L8-L40) 验证官方 sidebar 负责子声明、重复声明报错及 dispose 释放；[设置注册测试](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/tests/settings-registration.spec.ts#L12-L72) 验证保留官方设置根及其 store。设置测试定义了 404/网络失败、样式清理和导航装饰断言；其中部分手工调用安装/卸载，不能等价于完整真实宿主停用流程。新增 [composer portal 测试](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/tests/composer-plugin.spec.ts#L110-L138) 是模拟清理逻辑而非调用真实 observer，不能单独证明 React portal 集成不崩溃。
- **[CI]** 此 SHA 的 [GitHub checks](https://api.github.com/repos/MichengAI/dsh-codex-ui/commits/29a999ea8c41918e56a16542c669b258a5194e7a/check-runs) 显示 Node.js 22、24 及 release 的相应 job 成功；[CI 定义](https://github.com/MichengAI/dsh-codex-ui/blob/29a999ea8c41918e56a16542c669b258a5194e7a/.github/workflows/ci.yml#L48-L85) 包含 frozen install、Chromium、`pnpm test` 与构建产物 diff。manifest 另列 `test:compat`、`test:host`、`test:fallback-host`，不应仅凭 Node job 成功认定这些独立脚本也执行通过。
- **[RUN]** 本轮无 install/build/test/目标代码运行，也未验证真实 profile 及全 peer 区间；可借鉴声明式 row、针对性 slot、可撤销 effect 与探活回退，但 DOM 选择器、异步首帧、最终 dispose 清理和宿主版本变更均需单独验收。
