# 其余17个模型更新汇总（2026-10-21）

本轮按4+3+4+3+3分五批完成17个模型、102个维度，含停用的Mythos与MiniMax Preview。前一轮升级/锁定的Sonnet5.5、MiMo2.6Pro、Qwen0902、DeepSeek1017四条记录逐字段保持不变。总库21个、激活19个。

## 覆盖与置信度

- 全库111/126维有至少一类非空三源分；本轮93/102维有来源支持，9/102维保留T3估算。
- 全库low维度40个，包含停用模型；相较本轮前30个有所增加，原因是明确暴露了中文文学、快照与跨任务泛化缺口，不因填入来源分而自动提升置信度。
- 权重仍为官方25%、独立第三方45%、社区30%；空来源重归一化。缺证留null，不为凑三类来源把厂商转报或旧分复制成独立证据。
- 测试条件记录在raw_metrics.configuration和source_assessments；缺原始任务/完整轨迹、小样本、模型评委、版本不清均写明。

## 17个模型的分数变化

均分是六维编辑梯队分的平均，不是原始百分比。整数梯队存在主观判断，0.1来自权重运算，并不代表测量精度或统计显著性。

| 模型 | 更新前均分 | 更新后均分 | 当前状态 |
|---|---:|---:|---|
| GPT-6 Astra | 93.3 | 93.3 | 激活 |
| Claude Fable 5.1 | 92.5 | 92.5 | 激活 |
| Gemini 3.8 Flash | 86.7 | 85.6 | 激活 |
| Muse Spark 1.3 | 89.2 | 88.4 | 激活 |
| GLM-5.3 | 85.8 | 86.8 | 激活 |
| GLM-5.3-Flash | 85.8 | 85.8 | 激活 |
| DeepSeek V4 Pro 0813 | 84.2 | 83.3 | 激活 |
| Kimi K3 | 89.2 | 88.3 | 激活 |
| Hy3（正式版对照） | 80.8 | 78.4 | 激活 |
| Mistral Medium 3.5 | 74.2 | 72.6 | 激活 |
| Claude Mythos 5.1 | 91.7 | 91.7 | 停用 |
| GPT-6 Sol | 88.3 | 87.5 | 激活 |
| GPT-6.1 Sol | 91.7 | 90.8 | 激活 |
| Claude Opus 5.5 | 92.5 | 92.5 | 激活 |
| Gemini 4 Argon | 92.5 | 90.8 | 激活 |
| Grok 4.7 | 87.5 | 87.0 | 激活 |
| MiniMax-M3.1-Flash-Preview | 76.7 | 77.0 | 停用 |

## 重要变化

- Muse Spark1.3：Plotly原站现在明确总分40/43，数据分析由不完整证据估算转为第三方支持；MRCR检索很强、AA-LCR推理较弱，分别给分后加权。
- Gemini3.8Flash：补到AA高档LCR81%，长文维度由估算转为第三方支持；英文约束故事榜与中文文案口碑分开，综合写作分更保守。
- Grok4.7、KimiK3、DeepSeekPro0813、Hy3、Mistral：厂商旧版/窄域高成绩与独立难终端测试存在差异，体现到分源评分，不只摘高分。
- GLM5.3：英文故事比较榜与中文单人盲测方向不一，T90/C80分开再加权，保持low。
- MiniMax官方M Plan文档已说明Preview退役且旧名转向GA。本条保持历史Preview、停用，新增lifecycle_status、successor_model、version_policy；GA/匿名SpaceBunny/Plotly GA41/43均不写成Preview成绩。

## 折算一致性

三源分是本项目编辑判断，没有跨基准通用公式。优先对照相同基准/版本/条件的本库参照，使用5分档位，避免从单项百分比生成虚假精度。本轮AA-LCR v1.1统一参照：85–89→90、80–84→85、75–79→80、65–74→75；它仅适用于同一LCR任务，不套用MRCR/GraphWalks。Sol/6.1Sol的84/83因此更新到85，与Sonnet5.5/Qwen0902的既有85对齐。

对于其他混合维度，S上段95用于多项前沿证据，S下沿90用于强但非全面领先，A85/80表示可用但有明显限制，B75/70与C65用于本库参照中的短板；每个来源的具体选择见研究记录。私有题集和单篇体验不能证明行业通用梯队。

## 本轮仍未获得直接校准证据的9个维度

| 模型 | 维度 | 保留估算 | 原因 |
|---|---|---:|---|
| Gemini 3.8 Flash | data_analysis | 85 | 原发布表转报Vals Finance61.4%未直接回读Vals，不把转载当官方自测；CharXiv无工具86.2%支持有限图表子维，综合估算85/low，三源留空，待SQL/统计完整测试。 |
| DeepSeek V4 Pro 0813 | data_analysis | 80 | 针对0813检索BIRD/DABstep/SQL发现日文SQL测试原站正文不可读；llmwise仅标V4 Pro不能确认快照。保留80/low估算、三源null，不把未回读或无日期结果当0813实测。 |
| Claude Mythos 5.1 | reasoning | 95 | 官方确认与Fable同底层、不同防护与访问策略；本轮英文硬指标/实测和中英写作补查未取得可单列的Mythos本维直接校准证据。保留同源估算95、low，三源分全null；不能把Fable成绩当Mythos实测。 |
| Claude Mythos 5.1 | agentic | 95 | 官方确认与Fable同底层、不同防护与访问策略；本轮英文硬指标/实测和中英写作补查未取得可单列的Mythos本维直接校准证据。保留同源估算95、low，三源分全null；不能把Fable成绩当Mythos实测。 |
| Claude Mythos 5.1 | long_context | 90 | 官方确认与Fable同底层、不同防护与访问策略；本轮英文硬指标/实测和中英写作补查未取得可单列的Mythos本维直接校准证据。1M仅是规格。保留同源估算90、low，三源分全null；不能把Fable成绩当Mythos实测。 |
| Claude Mythos 5.1 | data_analysis | 90 | 官方确认与Fable同底层、不同防护与访问策略；本轮英文硬指标/实测和中英写作补查未取得可单列的Mythos本维直接校准证据。保留同源估算90、low，三源分全null；不能把Fable成绩当Mythos实测。 |
| Claude Mythos 5.1 | creative_writing | 85 | 官方确认与Fable同底层、不同防护与访问策略；本轮英文硬指标/实测和中英写作补查未取得可单列的Mythos本维直接校准证据。保留同源估算85、low，三源分全null；不能把Fable成绩当Mythos实测。 |
| MiniMax-M3.1-Flash-Preview | long_context | 80 | 官方历史Preview宣称1M；本轮RULER/MRCR检索未取得旧权重有效长度曲线。维持80低置信度估算、三源null。当前官方文档说明已退役，不引用正式版LOCA新成绩。 |
| MiniMax-M3.1-Flash-Preview | creative_writing | 70 | 英文prose/RP与中文小说/文笔检索仍无足够可复核的旧Preview文学测试。维持B下沿70/low，三源null；不能以正式版、M3或匿名模型成绩代替。 |

## 分批研究记录

- [第2批](../data/research/2026-10-21-batch-02.md)
- [第3批](../data/research/2026-10-21-batch-03.md)
- [第4批](../data/research/2026-10-21-batch-04.md)
- [第5批](../data/research/2026-10-21-batch-05.md)
- [第6批](../data/research/2026-10-21-batch-06.md)

## 校验

每批运行build_radar_data.py和validate.py。最终核对17条/102维reviewed_at、归档与原始快照一致、前一轮四模型未变、ID与激活开关未变；同时检查每个非空来源分都具备同类source_assessments及直接URL。14项现有管道测试通过。

结构测试不能证明网址内容永不变化；本轮回读日期与原测试日期分别注明，缺少不可变快照的API评测仍是特定时间点的证据。
