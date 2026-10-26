# AI 模型六维评测数据

原始库收录 **24 个模型、144/144 维评测**，当前激活 **22 个**。2026-10-27 新增 GPT-6.1 Terra、Kimi K3.1 Pro、MiniMax M3.1 Flash，见[本批研究与估算缺口](data/research/2026-10-27-batch-01.md)。2026-10-21 已升级/锁定四个模型，并完成其余17个模型的新规则更新。低置信度维度共 48 个（含停用模型）。[版本升级记录](data/research/2026-10-21-batch-01.md)；[其余17个模型更新汇总](docs/remaining17-update-summary.md)。

## 使用

仅需 Python 3.10+ 标准库，无额外依赖。在项目目录运行：

```bash
python scripts/build_radar_data.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

脚本按自身位置定位数据，从其他目录调用也可；支持 `--input` / `--output` 自定义路径，不允许覆盖输入文件。构建失败不会覆盖已有输出。校验同时检查原始字段和衍生数据是否与当前脚本一致，缺失或过期均失败。

## 数据契约

- `data/raw/models.json`：唯一原始库，仍是数组；保留全部历史字段。新增模型级 `is_active`，维度级 `vendor_score` / `third_party_score` / `community_score`（可选、null 或 0–100 有限数），以及 `raw_metrics` 对象。
- `data/processed/radar_ready.json`：只读衍生库，根对象包含 `schema_version`、`dimension_order`、`scoring`、`models`。保留来源、证据、置信度、版本等，新增 `raw_score`、`display_score`、`score_method`、`is_low_confidence`、`overall_score`、`overall_tier`、`rank`。
- 六维顺序：reasoning、coding、agentic、long_context、data_analysis、creative_writing。
- 三源权重 25% / 45% / 30%，只对非 null 项重新归一化；0 为有效分数。三项全空回退历史 `score`，标注 `score_method: legacy_score`。当前 126/144 维已有至少一类三源分，其余回退历史或明确估算的 `score`；未获得证据的来源保持 null。
- 衍生维度的 `score` 与 `raw_score` 同步为加权结果；转换仅更新深拷贝，原始库历史 `score` 不变。
- `raw_score` 是编辑梯队分（加权或历史分），不是原始 benchmark 成绩或客观能力真值。原始成绩写入 `raw_metrics` / `evidence`。低置信度不会因加权自动提升。
- `display_score = round(22 + ((clamp(raw_score, 60, 98) - 60) / 38) ** 1.35 * 74, 1)`，用于绘图半径，不反馈修改原始评分。显示参数和权重集中在 `scripts/build_radar_data.py` 顶部，输出包含参数快照。
- 总分为六维 raw_score 的算术平均，保留 1 位小数；S+≥90、S≥85、A≥80、其余 B。维度 tier 根据派生分重新计算（S≥90、A≥80、B≥70、其余 C），原始 tier 不改。
- 数组默认严格按 `rank` 从 N 递减至 1；`SORT_ASCENDING=False` 时从 1 递增至 N。同分模型也遵循该出场顺序；`rank` 始终 1 为最高。相同的一位小数均分按 id 排序分配序号，仅为稳定展示，不能据此认定同分模型存在实力差异。
- 按方案停用 `minimax-m3.1-flash-preview` 和 `claude-mythos-5.1`，保留原始记录与 `activation_notes`；重新激活后重建即可。

维护前阅读 [AGENTS.md](AGENTS.md) 与 [检索和维护规则](prompts/update_rule.md)。基准索引是待核实的检索候选，不能仅凭文档认定名称、版本或成绩属实。结构验证不代表来源真实性或评测结论已重新核验。

## 当前激活模型排名

以下总分来自当前原始库及三源加权；2026-10-27新增三个模型见[本批研究](data/research/2026-10-27-batch-01.md)，包含四项T3临时估算，排名仅供展示；此前17个模型见[17模型汇总](docs/remaining17-update-summary.md)，新版升级记录见[2026-10-21批次](data/research/2026-10-21-batch-01.md)。研究记录：[第一批](data/research/2026-10-19-batch-01.md)、[第二批](data/research/2026-10-19-batch-02.md)、[第三批](data/research/2026-10-19-batch-03.md)、[第四批](data/research/2026-10-19-batch-04.md)、[第五批](data/research/2026-10-19-batch-05.md)。

| 排名 | 模型 | 六维均分 | 评级 |
|---:|---|---:|---|
| 1 | GPT-6 Astra | 93.3 | S+ |
| 2 | Claude Fable 5.1 | 92.5 | S+ |
| 3 | Claude Opus 5.5 | 92.5 | S+ |
| 4 | Kimi K3.1 Pro | 92.2 | S+ |
| 5 | Gemini 4 Argon | 90.8 | S+ |
| 6 | GPT-6.1 Sol | 90.8 | S+ |
| 7 | Claude Sonnet 5.5 | 90.0 | S+ |
| 8 | Muse Spark 1.3 | 88.4 | S |
| 9 | Kimi K3 | 88.3 | S |
| 10 | GPT-6 Sol | 87.5 | S |
| 11 | Grok 4.7 | 87.0 | S |
| 12 | GLM-5.3 | 86.8 | S |
| 13 | MiMo V2.6 Pro | 86.7 | S |
| 14 | MiniMax M3.1 Flash | 86.7 | S |
| 15 | DeepSeek V4.1 Flash (1017) | 86.1 | S |
| 16 | GLM-5.3-Flash | 85.8 | S |
| 17 | Qwen3.8 Max (0902) | 85.8 | S |
| 18 | Gemini 3.8 Flash | 85.6 | S |
| 19 | GPT-6.1 Terra | 84.2 | A |
| 20 | DeepSeek V4 Pro 0813 | 83.3 | A |
| 21 | Hy3（正式版对照） | 78.4 | B |
| 22 | Mistral Medium 3.5 | 72.6 | B |

[初次迁移验证与当时输出前两个模型完整结构（历史快照）](docs/data-refactor-verification.md)。本轮只处理数据管道，不实现视频项目。

升级前的四条完整记录保存在 `data/archive/2026-10-21-before-version-upgrades.json`，不参与当前排名。旧id写入aliases用于追溯，不代表旧版本API别名保证指向新版；current_version与version_policy标明锁定范围。







其余17个模型的升级前评测保存在 `data/archive/2026-10-21-before-remaining17.json`；研究记录为2026-10-21的第02–06批，低置信度和剩余估算见[更新汇总](docs/remaining17-update-summary.md)。

本次同分出场排序与字段同步修复、DeepSeek 1017 AA 补证见[第07批研究记录](data/research/2026-10-21-batch-07.md)，[实际出场顺序与验证](docs/radar-fix-verification.md)。
