---
title: "CHECKLIST · 分发前自检"
domain: lifecycle
kind: guide
positioning: "发布前的十八项检查，按装/起/配/首启/文档分组，每项都写“怎么核”。"
read_when: "要把一个 bundle 发出去之前；或 review 别人的安装说明。"
status: living
updated: 2026-11-01
budget: 90
---
# 分发前自检

> 每项都给**怎么核**。核不了的项，就是 `[OPEN]`，不要当通过。

## 装

- [ ] **包声明了 `dsh.bundle.patch`。** 核：`node -e "console.log(require('./package.json').dsh)"`。
- [ ] **装完进 roster。** 核：`dsh plugin --profile <p> add <pkg>` 后读 `profiles/<p>/package.json` 的 `dsh.profile.bundles`。
- [ ] **行在合成配置里。** 核：`dsh --profile <p> --dump-config | grep -n "id: <你的 row id>"`。
- [ ] **离线可装。** 核：`pnpm pack` 出 `.tgz`，再 `dsh plugin --profile <p> add file:$PWD/xxx.tgz`。**相对 `file:` 路径按 profile 目录解析，不是 cwd**。
- [ ] **版本门在 manifest 里。** 核：`engines.dsh`（或 DSH peer 范围）覆盖你实际测过的宿主版本；`dsh.compatibility.*` 只是市场/CI 元数据，rc.3 不读，不能当门。

## 起

- [ ] **真启动一次，stderr 干净。** 核：`dsh --profile <p>` 后看有没有 `did not activate` / `skipping profile bundle`。
- [ ] **重启语义写对。** 核：改宿主行 → "重启"；新增/更换客户端模块 → "重启"；只有宿主已重新下发模块（HMR/开发态）时，刷新才等于重载。
- [ ] **不假设全有或全无。** 核：你的文档里没有"起不来就说明装坏了"这类句子。

## 配

- [ ] **默认值在 bundle 层。** 核：不依赖用户手动配置也能跑。
- [ ] **配置选对了家。** 核：需要跨 profile 的放 home 层或自有文件；不需要的放 profile/settings。
- [ ] **没往 home 层插新包。** 核：`grep -c "insert" $DSH_HOME/cordis.patch.yml` 应为 0，或插入的包在每个 profile 都装了。

## 首启

- [ ] **回答了"第一次看到什么"。** 核：全新 profile 装完，第一次打开有人在。
- [ ] **首启可推迟。** 核：点"稍后"之后，产品仍然可用（只是少了配置）。
- [ ] **Desktop 上仍成立。** 核：先问是保留名 carrier 还是社区壳；社区壳的 `DSH_HOME` 是私有的；不依赖 `welcome-notice`。

## 文档

- [ ] **安装那句不需要区分面。** 核：句子是"在 Plugins 页安装 X"，没有"如果……请用……"。
- [ ] **CLI 命令标了“仅 `dsh web`”。** 核：命令后紧跟限定语；社区桌面壳还要说明 `DSH_HOME` 不同。
- [ ] **没有 `--profile desktop`。** 核：全文搜索一遍。
- [ ] **偏离有登记。** 核：文档没有把自更新/自带安装器/运行时 reclaim/绝对路径写成默认；每个偏离都有代价与退出条件（见 [`REFERENCE` §4](../reference/REFERENCE.md)）。
