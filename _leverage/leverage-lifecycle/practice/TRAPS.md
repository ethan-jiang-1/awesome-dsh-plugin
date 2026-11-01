---
title: "TRAPS · 照抄就中招的十五条"
domain: lifecycle
kind: guide
positioning: "从 25 张产品卡、15 张本册样本与两轮实测里抽出的十五种失败形态：症状、机制、反例、正确做法。"
read_when: "发布前自查；或排查“明明装好了却不对”的问题。"
status: living
updated: 2026-11-01
budget: 120
---
# 照抄就中招

> 每条都给**反例**。没有反例的提醒没人记得住。

## 1. 装完 `exit 0`，功能不在

**症状**：安装成功、重启、界面里没有你的东西。
**机制**：包没声明 `dsh.bundle.patch`，只算普通依赖，不进 `dsh.profile.bundles`。
**反例**：实测装一个无 `dsh.bundle` 的包——**退出码 0**，只一句 stderr `declares no dsh.bundle — installed as a plain dependency, not a profile layer` `[RUN]`。
**做法**：把"能在 `--dump-config` 里看到自己的行"写进发布验收。

## 2. 在 Desktop 上装进了 `profiles/web`

**症状**：提示安装成功，App 里没有。
**机制**：Desktop 用 `profiles/desktop`；`--profile web` 写的是另一个目录。
**反例**：产品线 `51` 卡已量到"报告成功但不出现" `[CARD]`。
**做法**：安装说明只写应用内装；写 CLI 的必须标"仅 `dsh web`"。

## 3. 把 `--profile desktop add` 写进文档

**症状**：用户照抄，得到 `error: profile "desktop" is managed exclusively by the Electron application`。
**机制**：CLI 对 `desktop` 双门禁闭（启动与 `plugin` 都给拒），只有 Electron carrier 用程序化开关能进。
**反例**：`[RUN]` 实测两次都被拒；`bin.js:36`、`:119` `[DSH]`。
**做法**：永远不要在文档里给这条命令。

## 4. 用 home 层给所有 profile "供货"

**症状**：`--dump-config` 里有这行，启动后功能没有。
**机制**：`$DSH_HOME/cordis.patch.yml` 只改行、不改依赖；该 profile 没装这个包就 import 不到。
**反例**：`[RUN]` 启动报 `ERR_MODULE_NOT_FOUND … imported from profiles/web/`，且**服务照常起来**。
**做法**：home 层只用来覆盖已存在的行；分发给每个 profile 各自装。

## 5. 以为"启动全有或全无"

**症状**：按这个假设设计救生逻辑，结果用户遇到的是"应用能开、功能没有"，而不是"起不来"。
**机制**：单个 row 的导入失败被隔离成 `warning: N entry did not activate`，进程继续。
**反例**：`[RUN]` E8——报错同时服务照常监听并打印 URL。
**做法**：按三级描述失败（bundle / row / 整体），并给"静默缺失"一条自检路径。

## 6. 装完不重启，以为已生效

**症状**：开发时改了包，页面没变，怀疑插件没写对。
**机制**：CLI 安装是另一个进程，**宿主不知道**；应用内装才会给 `restart-required`。
**反例**：`[RUN]` 运行中装 bundle，同一进程再取首屏，`__DSH_BOOT__` 里没有新模块；宿主 stderr 静默；重启后才出现。
**做法**：CLI 场景写明"重启"；不要写"装完刷新即可"。

## 7. 只声明 peer，不声明 `engines.dsh`

**症状**：在一条宿主线上被拦，在另一条线上悄悄放行。
**机制**：`engines.dsh` 是地板门，`dsh.compatibility.dshReleases` 是逐版本枚举，两者在不同宿主线上各自是门禁。
**反例**：产品线 `BORROW` 第 4 条已把这条列为规则 `[CARD]`。
**做法**：两个都写；只在 README 里写"支持 0.2.x"不算门。

## 8. 把首启交给 `welcome-notice`

**症状**：web 上有欢迎语，Desktop 上没有，且没有任何报错。
**机制**：那一步在 Desktop 里**根本不注册**（`if (!('dshDesktop' in globalThis))`）。
**反例**：`[DSH]` `dsh-client-ui-settings-models/lib/client.js:4502`。
**做法**：首屏不要依赖单个 step；必须依赖时给 Desktop 分支。

## 9. 把 localStorage 当配置的家

**症状**：换一个面、换一个浏览器、换一个端口，设置全没了。
**机制**：localStorage 绑 origin；`dsh web` 的端口每次都可能是新的（`--port 0`）。
**反例**：产品线 `11`、`12` 都把布局状态放在 localStorage `[CARD]`——它们能接受，因为丢掉只是布局。
**做法**：**布局可以丢，配置不能丢**；配置进 settings 或自己的文件。

## 10. 把 `--dump-config` 里有这行当成"装好了"

**症状**：dump 看起来完美，启动就是不行。
**机制**：dump **不 import 模块**，只合成补丁栈。
**反例**：`[RUN]` E7 与 E8 是同一份配置的两种结局。
**做法**：验收加一步**真启动**，并读 stderr 有没有 `did not activate`。

## 11. 在 `inject` 里写"可选依赖"

**症状**：插件明明装了，启动摘要说 `1 entry did not activate`，理由是 `pending (waiting for service: optional)`。
**机制**：Cordis 的 `Inject` 只有两种形式——数组，或"服务名 → 拦截配置"的对象；**对象里的每个键都是必需服务**，没有"可选"这个开关。
**反例**：`[RUN]` 把 `inject` 写成 `{ optional: ['webServer'] }`，宿主去找名为 `optional` 的服务，行停在 pending；改成数组后同一份代码立刻生效。
**做法**：可选依赖不写进 `inject`——用 `ctx.inject([...], callback)` 延迟注册，或运行时 `ctx.get('webServer')` 取并判空。

## 12. 改了包、重装了、跑的却还是旧的

**症状**：修好的代码没生效，日志行为跟改之前一模一样，怀疑构建坏了。
**机制**：用 `file:` 装**同名同版本**的 tarball 时，pnpm 认的就是"这个名字+版本"，不会因为文件内容变了就重装。
**反例**：`[RUN]` E18——把 `inject` 改对、重新 `pnpm pack` 出**同名同版本**的包、`dsh plugin add` 返回 0，启动仍旧是旧的 `pending` 行为；把版本升到 `0.0.2` 才生效。
**做法**：每次改包都升版本号再打包；或者 `remove` 后重装。验收时看的是运行时行为，不是退出码。

## 13. `apply()` 返回值被当成 effect

**症状**：插件装上后 DSH 直接起不来，报 `TypeError: Invalid effect`，堆栈指向 loader，看不出是哪个插件。
**机制**：cordis 把 `apply()` 的返回值当 effect 消费；返回普通对象（比如想"声明一下自己是谁"）就抛错。
**反例**：`[SRC-TARGET]` `dsh-origin-plugin@2.7.3` `index.js:80` 显式 `return void 0`，并在 `:76-79` 注明是 issue #1、DSH ≥0.1.5 必现。
**做法**：`apply` 只做副作用、**不返回值**；插件描述走单独 export。验收时真启动一次，别只看装成功。

## 14. README 里的安装器不在包里

**症状**：照 README 跑 `install.bat` 或 `npm run install:bundle`，报找不到文件；而仓库里一切正常。
**机制**：`package.json` 的 `files` 白名单只列了 `lib/` 与 patch，脚本目录没进包。**装的人拿不到,写的人永远发现不了。**
**反例**：两条独立样本同一个错——`[SRC-TARGET]` `@wenaixi/cfbridge@0.13.2`（`files` 9 项无 `scripts/`，五条 npm scripts 全指向它）；`dsh-free-models-hub@0.3.1`（README 三条 `.bat`，tarball 7 个文件里一个没有）。
**做法**：打包后看 `npm pack --dry-run` 清单，再**逐条执行 README 里写的命令**；把"命令存在性"写进发布检查（[`CHECKLIST`](./CHECKLIST.md) 装段）。

## 15. 隔离环境里装插件，不代表它只碰隔离目录

**症状**：在临时 `DSH_HOME` 里装好插件、启动，以为一切都在沙盒内；实际上插件读写了你的真实 home。
**机制**：`DSH_HOME` 只决定**profile 与宿主数据**的位置；插件自己配置里的绝对路径（状态文件、名单、审计、备份目录）**不会跟着变**。
**反例**：`[RUN]` `dsh-isolation-gate@1.13.7` 在隔离 profile 下回显的默认路径是 `~/.agents/门禁-授权.json`、`~/.agents/门禁-名单.txt`、`~/.dsh/dsh-isolation-gate/access-log.jsonl`，备份目录还是硬编码的 `D:\回收站\门禁-名单改前`——**四条里三条在真实 home，一条是 Windows 专用**。
**做法**：测任何插件前，先读它 patch 里的路径配置，用 `--patch` 覆盖到隔离目录；测完核对真实 home 的目标文件**是否被创建或修改**（本次核对：均未被创建）。
