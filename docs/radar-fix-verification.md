# 本次修复验证

15项单元测试通过；构建及完整数据校验通过。全部114个激活维度满足score == raw_score；数组rank严格19→1，无重复、无跳号。

转换前后raw SHA256：`b8a21e6cc121afbdb32709a356bcc8c945d978a2020936b1ec9ae5ce374004c0`。此次raw的有意变更仅限DeepSeek AA补证，区别于转换操作。

| 数组索引（从0开始） | rank | name | overall_score |
|---:|---:|---|---:|
| 0 | 19 | Mistral Medium 3.5 | 72.6 |
| 1 | 18 | Hy3（正式版对照） | 78.4 |
| 2 | 17 | DeepSeek V4 Pro 0813 | 83.3 |
| 3 | 16 | Gemini 3.8 Flash | 85.6 |
| 4 | 15 | Qwen3.8 Max (0902) | 85.8 |
| 5 | 14 | GLM-5.3-Flash | 85.8 |
| 6 | 13 | DeepSeek V4.1 Flash (1017) | 86.1 |
| 7 | 12 | MiMo V2.6 Pro | 86.7 |
| 8 | 11 | GLM-5.3 | 86.8 |
| 9 | 10 | Grok 4.7 | 87.0 |
| 10 | 9 | GPT-6 Sol | 87.5 |
| 11 | 8 | Kimi K3 | 88.3 |
| 12 | 7 | Muse Spark 1.3 | 88.4 |
| 13 | 6 | Claude Sonnet 5.5 | 90.0 |
| 14 | 5 | GPT-6.1 Sol | 90.8 |
| 15 | 4 | Gemini 4 Argon | 90.8 |
| 16 | 3 | Claude Opus 5.5 | 92.5 |
| 17 | 2 | Claude Fable 5.1 | 92.5 |
| 18 | 1 | GPT-6 Astra | 93.3 |
