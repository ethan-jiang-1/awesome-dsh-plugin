# `_digested/` 工作纪律(供 agent 执行)

本目录是对 awesome-dsh-plugin 上游的研究消化。两个动作会改它:**upstream 同步**和**视图重建**。下面是两者的强制流程;所有数字必须可由脚本复现,复现不了的结论放 `_leverage/`,不放这里。

## 同步流程(upstream 有新提交时)

按 [`_change_log/00-index.md`](_change_log/00-index.md) 的完整纪律执行,要点:

1. fetch 后先探规模:`git rev-list --count`、`git diff --stat`。**先看源码侧**(`scripts/`、`.github/`、`package.json`)是否有 diff——零 diff 轮和有 diff 轮的后续工作量差一个量级。
2. merge(https 通道 + `-c http.lowSpeedLimit=1000 -c http.lowSpeedTime=60`,后台跑,等 job 结束再判断卡死)。
3. **重跑 census 并核对分母**:`python3 _digested/ecosystem/census.py`。若 stderr 出现「解析失败」或总数与 `ls data/plugins | wc -l` 不符,**先修 `census.py` 的解析再落任何数字**——手写子集解析器对 js-yaml 合法形态的漏收已发生六次(行内注释、JSON-in-.yml、折叠标量、整文件缩进、缩进支持引入的 en/zh 回归),每次都会静默少分母。核对标签命中数与中文描述数不塌缩(塌缩 = description 解析坏了)。
4. 写当期 `_change_log/NNNN-<from>-to-<to>.md`,七个专题逐个给判定(需复核 / 已核验 / 无对应 diff,每专题一句理由)。有真实 diff 的专题:逐行读 diff 后改写对应 mechanics 档案,才能把「需复核」降为「已核验」。
5. 更新 `_coverage/00-index.md` 矩阵、`_digested/00-index.md` 审计基线行、`_faq_on_digested/` 时效提示。
6. **重建视图**(下节)。
7. `node _digested/verify.mjs` 通过才算完成。

## 视图重建(`_view/`)

`_view/` 是呈现层,每轮同步后**覆盖式重建**——整页重写,不追加、不打补丁;历史归 `_change_log/`。规则:

1. **视图零原创**:`_view/` 里每个数字必须能由 `census.py` 或 `delta.py`(用法:`python3 _digested/ecosystem/delta.py <old-ref> <new-ref>`)复现;机制性断言必须链接到档案层(`mechanics/`、`_leverage/`)。发现档案里没有依据的说法,删掉或先去档案补证据。
2. 三块板的口径固定:①emerging(新 owner ≥2 条、标签增长)②heat-map(类目占比漂移、单件作者占比判真/假热闹)③anchors(热闹类目的存量头部 + 新增头部,标注星标边车为历史采样)。本期区间、基线 hash、数据截止日是每页必填字段。
3. **星标边车是历史采样**(冻结于 2026-08-19),凡引用必带 ⚠ 标注;「新增头部」为空是采样缺口,写成缺口,不写成「无影响力」。
4. `view_<领域>/` 是一级子目录,入口固定 `README.md`(一屏答案 + 快照 + 锚表 + 稳定性判读);立册门槛三条(体量 ≥400 且新增 ≥100;存量有 ≥100 星或源码级锚;owners ≥300 且单件 <95%)写在 [`_view/00-front.md`](_view/00-front.md)。够格才立;不够格的领域列候补,不预建空页。
5. **醒目突出的例子单独立卡**:册内 `NN-<slug>.md`,由 README 的「册内页」表链接。锚卡四段固定——一屏事实表 / 为什么它是锚 / 可复现数字 / 看点与待验证;必须标注证据等级(★ 注册表自述 · ★★ 读过源码或文档 · ★★★ 实测)并链回档案层。**「被模仿」是锚的硬判据**:第三方提及/衍生数由 `delta.py` ③b 现算,不依赖星标边车。
6. 人力预算花在锚上:每轮对 1-5 个锚条目补证据深度(★ → ★★ → ★★★),优先补声量与扩散两轴都高的;新卡先占位再补深度,不写没有出处的断言。

## 完成判据

- `node _digested/verify.mjs` 通过;
- census 分母与工作区条目数一致、0 解析失败;
- `_view/` 每页顶部一屏能回答该板问题 + 数据截止日;
- `_change_log` 当期记录末尾回写:复核日期 + 核对到的短 hash。

数字引用前必读 [`_method/00-index.md`](_method/00-index.md)(下载/星标数字的时效边界)。
