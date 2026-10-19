# AI 模型六维能力评测

跟踪 Agentic、编程、推理、长文本、创意写作和数据分析能力。分数为 0–100，保留来源等级与证据。

> 当前两条为结构示例，所有分数和口碑均为未核验的演示占位值，不代表真实评测结论。

| 模型 | 提供方 | Agentic | 编程能力 | 推理能力 | 长文本能力 | 创意写作 | 数据分析 | 一句话口碑 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| GPT-5 (示例) | OpenAI | 88 (A) | 90 (A) | 92 (S) | 86 (A) | 84 (A) | 87 (A) | 示例数据，待核验。 |
| Claude (示例) | Anthropic | 86 (A) | 88 (A) | 90 (A) | 93 (S) | 91 (S) | 85 (A) | 示例数据，待核验。 |

## Schema

模型字段：id、name、provider、last_updated、reputation、dimensions。六个维度键为 agentic、coding、reasoning、long_context、creative_writing、data_analysis。维度对象字段为 score、tier、source_tier、evidence。来源等级为 T1_Benchmark、T2_Community、T3_Estimated 或 null。

## 校验

运行 python scripts/validate.py 检查 JSON、必填字段、分数范围和空评分，并查看六维完整率。
