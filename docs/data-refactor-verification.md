# 数据管道重构验证（2026-10-21）

> 此报告是版本升级前的迁移快照。当前模型、评分和排名请看README与data/research/2026-10-21-batch-01.md。

## 无损迁移

逐字段递归对比迁移前后原始库：全部原有模型、字段和值保持不变；包括 sources、confidence、evaluated_version（存在时）等。仅增加激活开关、停用原因、三源评分空值和原始指标空对象。last_updated 仍为原始评测日期，本轮未重新评测。

输出 19 个激活模型，原始库仍为 21 个。三源评分均为空，126 维继续使用历史 score；无需从混合证据反推或捏造三源分。

## 激活模型总分排名

| 排名 | 模型 | 六维均分 | 评级 |
|---:|---|---:|---|
| 1 | GPT-6 Astra | 93.3 | S+ |
| 2 | Claude Fable 5.1 | 92.5 | S+ |
| 3 | Claude Opus 5.5 | 92.5 | S+ |
| 4 | Gemini 4 Argon | 92.5 | S+ |
| 5 | GPT-6.1 Sol | 91.7 | S+ |
| 6 | Kimi K3 | 89.2 | S |
| 7 | Muse Spark 1.3 | 89.2 | S |
| 8 | GPT-6 Sol | 88.3 | S |
| 9 | Grok 4.7 | 87.5 | S |
| 10 | DeepSeek V4.1 Flash | 86.7 | S |
| 11 | Gemini 3.8 Flash | 86.7 | S |
| 12 | GLM-5.3 | 85.8 | S |
| 13 | GLM-5.3-Flash | 85.8 | S |
| 14 | Qwen3.8-Max-0902 | 85.8 | S |
| 15 | DeepSeek V4 Pro 0813 | 84.2 | A |
| 16 | Claude Sonnet 5 | 82.5 | A |
| 17 | Hy3（正式版对照） | 80.8 | A |
| 18 | MiMo-V2.5-Pro | 80.8 | A |
| 19 | Mistral Medium 3.5 | 74.2 | B |

## 输出数组前两个模型的完整结构

数组是由低到高的出场顺序，rank 为由高到低的实力排序。当前前两个为 Mistral Medium 3.5 和 Hy3。

```json
{
  "models": [
    {
      "id": "mistral-medium-3.5",
      "name": "Mistral Medium 3.5",
      "provider": "Mistral AI",
      "country": "FR",
      "last_updated": "2026-10-19",
      "dimensions": {
        "agentic": {
          "score": 75,
          "tier": "B",
          "source_tier": "T1_Benchmark",
          "evidence": "官方 τ³-Telecom 91.4%；独立 AA AutomationBench-AA 仅 6%（页面取整）。领域工具任务与通用 SaaS 流程差距明显，综合映射 B，不将两个协议平均。",
          "sources": [
            "https://huggingface.co/mistralai/Mistral-Medium-3.5-128B",
            "https://artificialanalysis.ai/models/comparisons/mistral-medium-3-5-vs-gpt-5-5"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 75,
          "display_score": 43.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "coding": {
          "score": 80,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "官方 SWE-bench Verified 77.6%；AA SciCode 40%，Terminal-Bench 4.0 页面取整为 0%。较早 SWE 测试与新困难终端任务不等价，执行框架影响很大。",
          "sources": [
            "https://huggingface.co/mistralai/Mistral-Medium-3.5-128B",
            "https://artificialanalysis.ai/models/comparisons/mistral-medium-3-5-vs-gpt-5-5"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 80,
          "display_score": 53.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "reasoning": {
          "score": 75,
          "tier": "B",
          "source_tier": "T1_Benchmark",
          "evidence": "AA Humanity’s Last Exam 14%（页面取整），用于困难知识与推理的保守 B 级映射；不把综合 Intelligence Index 14 当作推理百分比。",
          "sources": [
            "https://artificialanalysis.ai/models/comparisons/mistral-medium-3-5-vs-gpt-5-5"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 75,
          "display_score": 43.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "long_context": {
          "score": 80,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "AA-LCR v1.1 69%（页面取整）；采用有效长文推理而非只看窗口。该任务覆盖不代表全窗口小说、所有位置或多轮记忆。",
          "sources": [
            "https://artificialanalysis.ai/models/comparisons/mistral-medium-3-5-vs-gpt-5-5"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 80,
          "display_score": 53.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "creative_writing": {
          "score": 70,
          "tier": "B",
          "source_tier": "T1_Benchmark",
          "evidence": "作者原始 Creative Story Writing 榜：相对胜率 16%、Bradley–Terry 系数 -2.553。为英文约束故事与模型评委，非中文文学评测。中英口碑检索未找到充分可复核中文对照，中文文笔/翻译腔未确认；保守 B。",
          "sources": [
            "https://github.com/lechmazur/writing"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 70,
          "display_score": 34.2,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "data_analysis": {
          "score": 65,
          "tier": "C",
          "source_tier": "T1_Benchmark",
          "evidence": "Plotly DataAnalyticsBench 25/43（58%）；隐藏洞察 0/5、数据质量 0/3。相同 Studio Embedded 框架的 43 题、20M 行单轮测试，非所有 SQL/统计任务。编辑 C 分数不等于原始 58%。",
          "sources": [
            "https://plotly.com/blog/mistral-large-4-plotly-data-analytics-bench/"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 65,
          "display_score": 26.8,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        }
      },
      "evaluation_notes": "2026-10-19 batch-04；0–100 为编辑梯队映射，非原始基准百分比。方法、检索路由及限制见 data/research/2026-10-19-batch-04.md。",
      "is_active": true,
      "overall_score": 74.2,
      "overall_tier": "B",
      "rank": 19
    },
    {
      "id": "hy3",
      "name": "Hy3（正式版对照）",
      "provider": "Tencent",
      "country": "CN",
      "last_updated": "2026-10-19",
      "dimensions": {
        "agentic": {
          "score": 80,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "正式版 AA：AutomationBench-AA 18%、AA-Briefcase v1.1 Elo 947。Tencent 270 位专家真实工作盲测均分 2.67/4 仅作补充；不将 preview 成绩写入本条。",
          "sources": [
            "https://artificialanalysis.ai/models/comparisons/hy3-vs-mistral-small-4",
            "https://huggingface.co/tencent/Hy3"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 80,
          "display_score": 53.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "coding": {
          "score": 80,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "正式版官方卡列 SWE-bench Verified 78%、SWE-bench Pro 57.9%；独立 AA Terminal-Bench 4.0 约 1%。新旧任务差异很大，按可用工程能力与高难终端短板综合给 A 下沿。",
          "sources": [
            "https://huggingface.co/tencent/Hy3",
            "https://artificialanalysis.ai/models/comparisons/hy3-vs-mistral-small-4"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 80,
          "display_score": 53.1,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "reasoning": {
          "score": 85,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "正式版官方卡 GPQA Diamond 90.4%；AA HLE 约 33%、CritPt 约 5%。能力覆盖和评测设置不同，不直接平均百分比。",
          "sources": [
            "https://huggingface.co/tencent/Hy3",
            "https://artificialanalysis.ai/models/comparisons/hy3-vs-mistral-small-4"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 85,
          "display_score": 64.0,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "long_context": {
          "score": 85,
          "tier": "A",
          "source_tier": "T1_Benchmark",
          "evidence": "正式版官方窗口 256K；AA-LCR v1.1 79%（取整）。官方称 MRCR 有改进但本轮未可靠转录分长度原图，因此不填写未经确认的 MRCR 数字。",
          "sources": [
            "https://huggingface.co/tencent/Hy3",
            "https://artificialanalysis.ai/models/comparisons/hy3-vs-mistral-small-4"
          ],
          "confidence": "medium",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 85,
          "display_score": 64.0,
          "is_low_confidence": false,
          "score_method": "legacy_score"
        },
        "creative_writing": {
          "score": 80,
          "tier": "A",
          "source_tier": "T2_Community",
          "evidence": "中文 SoloEnt 三次首章工作流的人类盲评对 Hy3 给出 61.7/100；这不是本项目标准分，且未给完整调用快照。英文检索主要命中译文与产品介绍，没有足够独立英文小说/RP 原始测试；综合暂定 A 下沿。",
          "sources": [
            "https://benchmark.soloent.ai/en/reports/writingflow_18models/"
          ],
          "confidence": "low",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 80,
          "display_score": 53.1,
          "is_low_confidence": true,
          "score_method": "legacy_score"
        },
        "data_analysis": {
          "score": 75,
          "tier": "B",
          "source_tier": "T3_Estimated",
          "evidence": "英文 BIRD/DABstep 与 SQL/pandas、中文 Excel/财报正式版实测检索未核到可复用专门成绩，很多结果属于 preview。正式版官方明确金融建模、文件生成用途；据此保守估算 B，待独立任务验证。",
          "sources": [
            "https://huggingface.co/tencent/Hy3",
            "https://www.tencent.com/tencent-hunyuan-officially-releases-hy3-advancing-agent-capabilities-and-deeper-product-integration/"
          ],
          "confidence": "low",
          "vendor_score": null,
          "third_party_score": null,
          "community_score": null,
          "raw_metrics": {},
          "raw_score": 75,
          "display_score": 43.1,
          "is_low_confidence": true,
          "score_method": "legacy_score"
        }
      },
      "evaluation_notes": "2026-10-19 batch-03；评分是编辑梯队映射，非基准直接平均；版本和证据缺口见 data/research/2026-10-19-batch-03.md。",
      "is_active": true,
      "overall_score": 80.8,
      "overall_tier": "A",
      "rank": 17
    }
  ]
}
```

## 已执行检查

- 原始数据递归对比：全部历史字段、数值、证据与来源保持不变。
- `python -m unittest discover -s tests -v`：14 项测试全部通过；覆盖缺失来源重归一化、零分、锚点/截断、筛选排序、评级阈值、元数据保留、非法输入拒绝、输出过期识别、原子写入与输入保护。
- `python scripts/build_radar_data.py`：成功输出 19 个激活模型。
- `python scripts/validate.py`：21 个模型、126 维和衍生库一致性校验通过。
- `git diff --check`：通过。

本次没有重新核验外部来源，结构测试仅验证迁移和转换行为。
