# 任务目标：补齐与更新模型六维评测数据
请读取项目中的 data/raw/models.json 文件，针对列表中各模型的六大维度能力（Agentic、编程能力、推理能力、长文本能力、创意写作、数据分析）进行深度检索与数据更新。
为了避免概念模糊导致的数据缺失（null / N/A），请严格执行下述【执行工作流】、【双语检索路由】、【三级检索漏斗】及【六维检索锚点】。

---

### 一、 核心执行工作流与防偷懒纪律（必读）

1. **第一步：解析现有 Schema 与增量识别**
   - 先读取 data/raw/models.json，分析现有的 JSON 字段结构（确认各维度是存储纯数字评分、对象结构还是字符串）。
   - 优先识别当前数据中为 null、0、N/A 或明显缺失的维度进行定向补齐；若已有明确且高置信度的数据，可予以保留或微调校验。
2. **第二步：强制分批执行（Batch Processing）**
   - **严禁一次性更新整个模型库的评测！** 每次仅提取 **3 ~ 5 个模型** 进行深度搜索。
   - 每完成一批（3~5 个模型）的检索后，立即更新进 data/raw/models.json（或输出该批次的 JSON 片段），汇报本批检索依据，并暂停等待我输入“继续”后再处理下一批。
3. **第三步：分数标准化映射（防止破坏前端数据结构）**
   - 若 models.json 要求某维度为统一量纲的数值（如 0-100 分），请根据检索到的【T1 跑分】或【T2 口碑评级】，按行业梯队折算为标准分填入数值字段（例如：S级/顶尖 = 90-98，A级/优秀 = 80-89，B级/可用 = 70-79，C级/偏弱 = 60-69）。
   - 如果 JSON 结构允许保留描述性字段（如 description、notes、evidence），请将具体的跑分（如 SWE-bench: 49%）和口碑摘要写入描述字段；若 JSON 仅接收纯数字，请在对话回复中列出每个数字对应的【检索依据与口碑摘要】供我核对。

---

### 二、 中英双语交叉检索路由（Language Routing）

调用 Web Search 工具时，**严禁仅使用单一中文关键词搜索**，必须按维度与模型属性分流：
1. **硬指标（Tier 1）100% 强制纯英文检索**：
   - 搜索跑分、排行榜与技术报告时，必须将搜索词转换为纯英文（如 "[Model Name] SWE-bench Verified score" 或 "[Model Name] RULER benchmark"），直接命中 HuggingFace、GitHub、ArXiv 及英文权威榜单。
2. **用户口碑（Tier 2）执行“中英分流”检索**：
   - **国际模型 & 理科维度（Agentic/编程/推理/数据分析）**：优先用**英文**检索 Reddit 与海外开发者社区（如 "[Model Name] coding review site:reddit.com/r/LocalLLaMA"）。
   - **国产大模型（DeepSeek、Qwen、GLM、豆包等）**：中英文同步检索，重点抓取国内极客社区（知乎、V2EX、Linux.do）的一手实测。
   - **【创意写作】维度（特殊双语处理）**：必须**分别检索中、英文口碑**。先用英文搜其在 SillyTavern / Roleplay / Prose 上的表现，再用**中文**专门检索 "[模型名称] 写小说 / 文笔 / 翻译腔 / AI味"，综合评定其“英文创作表现”与“中文创作水准（有无翻译腔/说教味）”。

---

### 三、 三级检索漏斗策略（按优先级向下兜底，严禁留白）

对于每个缺失维度，严格按以下顺序检索：
1. **【Tier 1：硬核基准分（优先）】**：检索官方 Technical Report、权威排行榜（LMSYS Chatbot Arena 细分榜、LiveBench、OpenCompass、Artificial Analysis）的具体量化得分。
2. **【Tier 2：真实用户口碑（次优兜底）】**：若未公布某项冷门 Benchmark（尤其是“创意写作”、“数据分析”或闭源模型的特定能力），立即切换关键词检索极客社区实测反馈。
   - **重点检索源**：Reddit（r/LocalLLaMA、r/singularity、r/ClaudeAI）、HuggingFace 评论区、X (Twitter)、知乎、V2EX、Linux.do、小红书深度测评。
   - **提取内容**：总结真实体感（如：“逻辑严密但文风有AI爹味”、“写前端极强但长文本过64K后降智”），转化为梯队评级（S / A / B / C）及标准分。
3. **【Tier 3：官方特性与同级标定（保底）】**：若既无跑分也缺乏广泛讨论，检索其官方宣称的核心架构特性（如原生 Tool Use、Code Interpreter 支持情况），结合同参数量级表现给出合理标定。**严禁在未执行搜索的情况下凭空瞎编。**

---

### 四、 六维度定义与精准检索锚点（Search Queries）

请在调用搜索工具时，组合使用“模型名称 + 英文/中文检索锚点”：

**1. Agentic（智能体与工具调用）**
- **硬指标检索词**：SWE-bench Verified、BFCL (Berkeley Function-Calling Leaderboard)、GAIA benchmark、TAU-bench、WebArena、Tool Use score。
- **口碑检索词**：Agent 实测、Function calling 稳定性、cline / cursor / windsurf 配合体验、死循环/幻觉率、tool use experience site:reddit.com。

**2. 编程能力 (Coding)**
- **硬指标检索词**：LMSYS Coding Arena Elo、LiveCodeBench、Aider Polyglot Benchmark (极高参考价值)、BigCodeBench、HumanEval+。
- **口碑检索词**：写代码 实测、重构代码能力、前端生成、Debug 能力、coding comparison site:reddit.com/r/LocalLLaMA。

**3. 推理能力 (Reasoning)**
- **硬指标检索词**：LMSYS Hard Prompts Elo、GPQA Diamond、AIME 2024 / 2025、MATH-500、LiveBench Reasoning、ARC-AGI。
- **口碑检索词**：复杂逻辑 实测、数学推理 翻车、弱智吧测试、reasoning capability review。

**4. 长文本能力 (Long-Context)**
- **硬指标检索词**：Context Window、RULER benchmark (测真实有效上下文)、Fiction.liveBench、MRCR、BABILong。（注：忽略单纯的100%大海捞针NIAH宣传，重点看有效上下文衰减）。
- **口碑检索词**：长文本 降智、长文总结 遗忘、吃书情况、有效上下文 实测、long context degradation。

**5. 创意写作 (Creative Writing)** *(中英文分别检索；采用下述统一三源权重，不私自增减权重)*
- **硬指标检索词**：LMSYS Creative Writing Elo、EQ-Bench (Creative Writing)、Creative Writing v3 benchmark。
- **口碑检索词**：写小说 实测、文笔 / AI味 / 翻译腔、角色扮演 (RP / Roleplay / SillyTavern 酒馆体验)、分镜脚本生成、活人感、creative writing prose site:reddit.com/r/LocalLLaMA。

**6. 数据分析 (Data Analysis)**
- **硬指标检索词**：BIRD-Bench (SQL)、Spider、DABStep、ChartQA、DataBench、DocVQA、Code Interpreter evaluation。
- **口碑检索词**：Excel 处理实测、表格分析 准确率、SQL 生成能力、财报分析/研报提取、data analysis pandas accuracy。




---

### 五、Raw → Processed 双层维护规则（2026-10-21）

1. **唯一原始库**：只在 `data/raw/models.json` 维护事实、历史编辑分、证据、来源、置信度与版本。原文件仍为模型数组，所有历史字段保留；`data/processed/radar_ready.json` 完全由脚本生成，禁止手改或将显示分反写原始库。
2. **激活策略**：每个模型必须有布尔 `is_active`。停用只影响输出，不删除历史评测。当前按方案停用 `minimax-m3.1-flash-preview` 与 `claude-mythos-5.1`，原因记在 `activation_notes`。这是本轮展示选择，不代替对模型身份、版本关系的事实核验；补证后可重新激活。
3. **三源标准分**：维度可选 `vendor_score`、`third_party_score`、`community_score`，均为 0–100 有限数值或 null。权重统一为 25% / 45% / 30%；脚本只对非 null 项重归一化。三项全空时回退历史 `score`，不得把同一个旧分复制成三类独立证据。`0` 是有效分数，不当作缺失。`raw_metrics` 记录原始指标，默认空对象。
4. **原始基准成绩不可直接加权**：不同基准的百分比、Elo、题数不能直接混合。先记录基准名称/版本、模型版本、工具/推理预算、测试条件、时间、来源及原始成绩，再说明梯队映射依据后填写三源分。新检索的梯队分通常在 60–98；不要为了迁移强行改写既有 0–100 分。缺乏校准依据时留 null，不能制造精确分数。
5. **来源分类看发布主体**：厂商自报归 vendor；独立评测归 third_party；社区一手体验归 community。不能把转载厂商成绩算成独立复测，也不能因为 EQ-Bench 等出现在社区讨论中就重复计入 community。避免同一测试跨类重复加权，折算理由与 URL 必须写入 evidence / sources 或关联研究记录。
6. **检索路由**：Tier 1 硬指标只用英文关键词；国际模型社区优先 Reddit r/LocalLLaMA、r/SillyTavernAI 等，国产模型同时检索知乎/Linux.do。创意写作必须中英文分别检索，记录翻译腔、说教味与长篇一致性，不能把英文短篇结果直接外推成中文长篇能力。
7. **固定锚点**：显示分只由 60/98、22/96 和 gamma=1.35 的固定幂函数产生；禁止按当前模型库极值动态 Min-Max。总分为六维 raw_score 的均值，评级 S+≥90、S≥85、A≥80、其余 B。维度 tier 按加权后的 raw_score 重新派生；原始库的 tier 不改。保留 low 置信度并派生 is_low_confidence，不因多源加权自动提高置信度。
8. **排序契约**：rank 始终 1 为最高分，同分按 id 正序分配唯一序号，不代表统计显著差异。输出数组默认严格按 rank 从 N 递减到 1；SORT_ASCENDING=False 时从 1 递增到 N，同分也不得跳号。衍生维度 score 与 raw_score 同步为计算分，仅更新内存副本，不能回写原始 score。
9. **批次与同步**：每批仅更新 3–5 个模型的研究，除非用户已明确授权更多，批后汇报并等待继续。纯结构迁移可以一次处理全库，但不得顺便重估分数。每批改完 raw 后，必须运行 `python scripts/build_radar_data.py`、`python scripts/validate.py`，同步 README 数量/说明并记录研究依据。脚本或契约改变时运行 `python -m unittest discover -s tests -v`。验证失败先修复，不提交过期 processed。

### 六、优先核查的基准索引

下列名称来自重构方案，是检索候选清单，**不是对存在性、版本号或权威性的背书**。检索时先核实维护方原站、论文或官方仓库；若找不到指定版本，明确记录未找到，使用能核实的基准，不能补写成绩、链接或声称已核验。

| 维度 | 候选基准与核查重点 |
|---|---|
| reasoning | Humanity’s Last Exam (HLE)、GPQA Diamond、CritPt、LiveBench Reasoning；区分工具条件 |
| coding | Terminal-Bench（核查 2.1 / 4.0 具体版本）、DeepSWE v1.1、SWE-bench Verified/Pro、SciCode；不同版本不直接横比 |
| agentic | AutomationBench、OSWorld 2.0、Toolathlon Verified、AA-Briefcase、Agents’ Last Exam；记录执行框架 |
| long_context | AA-LCR v1.1、MRCR v2 (512K–1M)、RULER、GraphWalks；忽略单纯 100% NIAH 宣传，考察长程衰减 |
| data_analysis | Plotly DataAnalyticsBench（核实是否 43 题）、Vals Finance Agent、Signal65 PINNACLE、BIRD/DABstep；记录数据与工具环境 |
| creative_writing | EQ-Bench Creative Writing v3 / Longform、NextChapterBench、Foreverse 中文盲测、ToneBench；核实语言、样本、评委与盲测方法 |
