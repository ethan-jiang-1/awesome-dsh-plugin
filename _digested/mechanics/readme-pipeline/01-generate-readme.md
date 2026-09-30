# 01 · generate-readme 逐段机制

> 基线:`upstream@c18ba4a0d`(0002 复核:**仍 215 行、本窗口零 diff**;0001 的增量是 CRLF 归一化 +5 行,全部函数行为未变)。行号可能有 ±5 漂移,机制描述为准。

## 主流程(:80-186)

```
readEntries()(坏 YAML 在这里以可读消息退出,不打堆栈)
→ validateEntries(有问题列出全部后拒绝生成)
→ orderEntries(CAT_IDS 类序 → url localeCompare)
→ for each locale:
    TOC = [Plugins] + 使用中的类目(带 emoji 前缀,仅非 en)+ [Badge, Disclaimer]
      —— awesome-lint 要求目录是一张单一列表,HTML 注释会把列表劈成两半触发
         remark-lint:awesome-toc,所以 marker 包住整张列表、外壳行也由脚本产出(:40-47)
    PLUGINS = 每类一段 ### 标题 + 条目行 `- [name](url) — desc`
      —— en 无 emoji 前缀;缺译渲染 BASE_LOCALE(en)并收集 untranslated
    before !== after 时写盘(w 写模式)/ --check 模式则记 stale
    parsedUrls() 全文集合校验(smuggled / missing 都算 stale)
→ untranslated 清单汇报(≥1 条时)
→ stale 则 exit 1 并提示 regenerate
    (0001 起 --check 只在 PR 手改 README 时才由 pr-check 调用,现位于
     pr-check.yml:171-210 且比对 PR head 而非 merge ref;
     yml-only PR 由 runner 现场无 --check 生成;合并后由 sync-readme.yml 执行。
     0002 另加一道前置门:PR 改了 README 里的插件行却没带任何
     data/plugins/ 文件 → 直接拒(pr-check.yml:105-152,#5845))
```

## 细节摘录

- **replaceBlock**(:49-57):marker 对丢失或逆序直接 exit 1——手编时不小心吃掉注释是常见事故。
- **escapeRefs**(:112-116):按 code span 切片,偶数段(非代码)才做 `(^|[^\\])\[(?![^\]]*\]\()` 的开括号转义;三条既有条目依赖 inline link,不能误伤。
- **破链检查**(:188-197):README 内所有指向 `README*.md` 的链接必须存在(语言切换链接失效会被拦)。
- **category 清单看守**(:204-215 附近):contributing.md 里必须逐字包含 CAT_IDS 反引号拼接串——taxonomy 曾加 usage/vision 后文档仍停在旧十二项,故改为脚本看守。0001:contributing 与 PR 模板列表都已人工同步到含 wsl 的 23 项;PR 模板那份依然无脚本看守(见 00-map)。
- **幂等性**:before==after 不写盘打印 "up to date";整个脚本无增量概念,每次全量重建。
- **CRLF 归一化(0001 新增,+5 行)**:`normalizeNewlines`(:49-53)把 `\r\n?` 归一为 `\n`,`parsedUrls` 切行改 `split(/\r?\n/)`——Windows 下 autocrlf 检出的 README 逻辑内容未变,不应报 stale。"Git sees no content diff" 是判据。

## 它不做的事

- 不碰 `data/plugins/*`(单向:YAML→README);不排序重写 YAML;
- 不管站点(tarball 映射、stars 等都是 build-site 的事);
- 不校验 README 外壳的手工部分(除上述三类守卫)——外壳的评审防线只有 awesome-lint。

## 与 migrate-to-yaml.mjs 的镜像关系

migrate-to-yaml.mjs 是一次性脚本(README→YAML 方向),用同样的 parseReadme 正则与 URL join key;两边共享的正则 `/^- \[(.+?)\]\((https:\/\/github\.com\/[^)]+)\) ([—-]) (.+)$/` 是这个仓库事实上的「条目行格式合同」。写死分隔符允许 em-dash 或 hyphen 两变体([—-]),zh 用 em-dash、en 用 hyphen 也因此成为 locale.sep 的取值依据。
