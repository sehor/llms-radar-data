这两份 Prompt 已经按照我们前面讨论的所有核心架构（**双文件 ETL 解耦、防算术崩盘的三源梯队折算、固定锚点非线性拉伸、以及 Remotion 全局流体变形与 Ghost 残影对比**）彻底固化。  
你可以直接把它们分别复制给对应的 AI 助手执行。

### **Prompt 1：重构与升级【数据收集项目】（发给管理数据仓库的 AI）**

这份 Prompt 会让 AI 在**绝对不破坏你现有 21 个模型心血**的前提下，搭建好 raw ➔ processed 的双层架构、自动转换脚本，并更新以后的联网搜索规则。

Markdown  
\# 任务：重构模型评测仓库为“原始事实层 (Raw) \+ 视频衍生层 (Processed)”双层架构

请帮我对当前的数据仓库进行工程化升级。我们的核心目标是：\*\*将“客观事实检索”与“视频视觉分数计算”彻底解耦\*\*，确保未来调整视频雷达图的拉伸算法或权重时，永远不会破坏辛苦检索到的原始证据。

请依次执行以下 4 步操作：

\---

\#\#\# 第一步：无损升级原始数据库 (\`data/raw/models.json\`)  
请读取现有的 \`data/raw/models.json\`，在\*\*100%保留现有全部模型、score、evidence、sources、confidence、evaluated\_version 等字段\*\*的前提下，为每个模型补充以下结构支持：  
1\. \*\*根节点新增激活开关与版本说明\*\*：  
   \- \`"is\_active": boolean\`：用于控制该模型是否输出到视频衍生库中。请将缺乏独立实测的边缘预览版（如 \`minimax-m3.1-flash-preview\`）或同源马甲模型（如 \`claude-mythos-5.1\`）设为 \`false\`，其余主流模型设为 \`true\`。  
2\. \*\*维度节点支持“三源梯队分”拆分（向后兼容）\*\*：  
   在每个维度对象下，除保留原有的 \`score\` 外，支持以下三个可选字段（0-100 的标准化梯队分，无数据则为 \`null\`）：  
   \- \`"vendor\_score"\`: 官方自报跑分折算的梯队分（占 25% 基准权重）  
   \- \`"third\_party\_score"\`: 独立第三方（AA / LiveBench / Signal65 / Plotly / LMSYS）折算的梯队分（占 45% 基准权重）  
   \- \`"community\_score"\`: 极客与创作者社区（Reddit / Linux.do / Foreverse / EQ-Bench）实测口碑折算的梯队分（占 30% 基准权重）  
   \- \`"raw\_metrics"\`: (可选对象) 记录原始异构跑分，如 \`{"Terminal-Bench 4.0": "66.4%"}\`。

\---

\#\#\# 第二步：编写核心 ETL 转换脚本 (\`scripts/build\_radar\_data.py\`)  
请编写一个 Python 脚本，读取 \`data/raw/models.json\`，计算并输出专门喂给 Remotion 视频项目的衍生文件 \`data/processed/radar\_ready.json\`。

\*\*脚本核心转换逻辑要求：\*\*  
1\. \*\*可调视觉常量（置于脚本顶部，方便我随时微调视频效果）\*\*：  
   \`\`\`python  
   WEIGHTS \= {"vendor": 0.25, "third\_party": 0.45, "community": 0.30}  
   FLOOR \= 60.0       \# 行业及格底线分  
   CEILING \= 98.0     \# 行业理论天花板分  
   MIN\_RADIUS \= 22.0  \# 雷达图最内圈视觉半径  
   MAX\_RADIUS \= 96.0  \# 雷达图最外圈视觉半径  
   GAMMA \= 1.35       \# 非线性拉伸指数（越大则高分越凸出、低分越内凹）  
   SORT\_ASCENDING \= True \# True 为按总分从低到高出场（营造战力步步攀升感）

> 2. **过滤与自适应加权 (raw\_score)**：  
   * 仅处理 is\_active \== True 的模型。  
   * 计算单维度 raw\_score：若存在非空的 vendor\_score / third\_party\_score / community\_score，则按非空项的实际权重归一化加权计算（保留 1 位小数）；若三项均为 null（尚未拆分的历史数据），则直接回退使用该维度原有的 score。  
> 3. **固定锚点非线性拉伸 (display\_score)**：  
   * **严禁使用受极值绑架的动态 Min-Max 归一化！** 必须使用固定锚点幂函数公式，将 60\~98 的 raw\_score 映射为 22\~96 的绘图半径：  
     clamped \= max(FLOOR, min(CEILING, raw\_score))  
     normalized \= (clamped \- FLOOR) / (CEILING \- FLOOR)  
     display\_score \= round(MIN\_RADIUS \+ (normalized \*\* GAMMA) \* (MAX\_RADIUS \- MIN\_RADIUS), 1\)  
> 4. **生成模型汇总指标与简评**：  
   * overall\_score: 六维 raw\_score 的算术平均值（保留 1 位小数）。  
   * overall\_tier: 均分 \>=90 为 "S+"，\>=85 为 "S"，\>=80 为 "A"，其余为 "B"。  
   * is\_low\_confidence: 当该维度 confidence \== "low" 时设为 True（供前端渲染虚线或星号标记）。  
   * 按 overall\_score 进行排序，写入 rank 序号，输出至 data/processed/radar\_ready.json。

### **第三步：更新联网检索与维护规则 (prompts/update\_rule.md)**

请将以下准则写入 prompts/update\_rule.md，作为本仓库后续更新数据的永久铁律：

> 1. **双语交叉检索路由**：硬指标（Tier 1）100% 强制纯英文搜索；社区口碑（Tier 2）国际模型搜 Reddit (r/LocalLLaMA, r/SillyTavernAI)，国产模型同步搜知乎/Linux.do；**【创意写作】必须中英双语分别检索**，严查中文是否存在翻译腔、说教味或长程吃书。  
> 2. **常驻权威三方基准库**：  
   * **推理 (reasoning)**：Humanity's Last Exam (HLE)、GPQA Diamond、CritPt、LiveBench Reasoning。  
   * **编程 (coding)**：Terminal-Bench (区分 2.1 与 4.0 版本)、DeepSWE v1.1、SWE-bench Verified/Pro、SciCode。  
   * **智能体 (agentic)**：AutomationBench、OSWorld 2.0、Toolathlon Verified、AA-Briefcase、Agents' Last Exam。  
   * **长文本 (long\_context)**：AA-LCR v1.1、MRCR v2 (512K-1M)、RULER、GraphWalks（忽略单纯的 100% NIAH 宣传，重点看长程衰减）。  
   * **数据分析 (data\_analysis)**：Plotly DataAnalyticsBench (43题)、Vals Finance Agent、Signal65 PINNACLE、BIRD/DABstep。  
   * **创意写作 (creative\_writing)**：EQ-Bench (Creative Writing v3 / Longform)、NextChapterBench、Foreverse 中文盲测、ToneBench。  
> 3. **严禁原始百分比直接入库加权**：不同 Benchmark 难度差异极大（如 TB4 60% 已是顶峰，而 GPQA 90% 才算一线）。AI 检索到原始分数后，必须先按行业梯队折算为 60-98 的百分制标准分填入 vendor\_score / third\_party\_score / community\_score，将原始百分比记录在 evidence 或 raw\_metrics 中。  
> 4. **每次更新分批不超过 5 个模型**，改完 data/raw/models.json 后自动运行 python scripts/build\_radar\_data.py 与 scripts/validate.py，同步更新 README.md。

### **第四步：立即执行验证**

请立即完成上述改造，运行一次 python scripts/build\_radar\_data.py，向我展示生成的 data/processed/radar\_ready.json 中的前 2 个模型结构，并汇报当前激活模型的总分排名清单。

\---

\#\#\# Prompt 2：建立【动感雷达图视频项目】（发给负责写 Remotion 视频的 AI）

等你把第一个项目生成的 \`radar\_ready.json\` 复制过来后，在一个新文件夹里打开 AI 编程助手（如 Cursor / Windsurf / Claude Code），直接发送这份 Prompt 来生成炫酷的赛博 HUD 视频工程：

\`\`\`markdown  
\# 任务目标  
请帮我使用 Remotion（React \+ TypeScript \+ Tailwind CSS）从零搭建一个“赛博机甲 HUD 战力面板风格”的 AI 大模型六维能力对比动态视频项目。

\*\*核心视觉灵魂\*\*：  
1\. \*\*拒绝死板的 PPT 翻页淡入淡出！\*\* 雷达图机甲底盘全程常驻。当模型切换时，多边形数据层采用\*\*连续流体变形（Polygon Morphing）\*\*，从上一个模型的形状直接弹射拉伸为当前模型的形状。  
2\. \*\*Ghost Trail（上一模型虚线残影对比）\*\*：在当前发光多边形下方，保留上一个模型的半透明白色虚线轮廓，让观众一眼看出战力暴涨或缩水的维度。  
3\. \*\*厂商专属霓虹主题色动态流转\*\*：随着不同厂商（OpenAI / Anthropic / DeepSeek / Google / Qwen / Kimi / Zhipu 等）登场，全屏的径向辉光、多边形霓虹描边、底部能量条随之丝滑变色。

\---

\#\#\# 1\. 数据源规范 (\`src/data/radar\_ready.json\`)  
项目直接读取 \`src/data/radar\_ready.json\`（若本地暂未放入，请先根据以下 Schema 生成一份包含 4 个主流模型的真实感 Mock 数据，并兼容直接替换为完整文件）：  
\- 根节点包含 \`models\` 数组，每个模型对象结构如下：  
  \- \`id\`, \`name\`, \`provider\`, \`country\` ("US" | "CN" | "FR")  
  \- \`rank\`: 排名序号  
  \- \`overall\_score\`: 六维均分 (如 \`92.5\`)  
  \- \`overall\_tier\`: 综合评级 (\`"S+"\` | \`"S"\` | \`"A"\` | \`"B"\`)  
  \- \`evaluation\_notes\`: 简短评测说明  
  \- \`dimensions\`: 包含 6 个固定维度的对象 (\`reasoning\`, \`coding\`, \`agentic\`, \`long\_context\`, \`data\_analysis\`, \`creative\_writing\`)，每个维度包含：  
    \- \`raw\_score\`: 真实得分 (如 \`95\` 或 \`80\`，\*\*用于画面上的文字与数字跳动展示\*\*)  
    \- \`display\_score\`: 经过非线性拉伸后的绘图分 (范围 \`22 \~ 96\`，\*\*专门用于计算 SVG 雷达图顶点半径\*\*；若读取的是未预处理的 \`models.json\` 只有 \`score\`，请在前端用公式 \`22 \+ Math.pow(Math.max(0, Math.min(1, (score \- 60\) / 38)), 1.35) \* 74\` 实时算出 \`display\_score\`)  
    \- \`tier\`: \`"S"\` | \`"A"\` | \`"B"\` | \`"C"\`  
    \- \`confidence\`: \`"high"\` | \`"medium"\` | \`"low"\`  
    \- \`evidence\`: 该维度的核心实测依据文本

\---

\#\#\# 2\. 视频规格与全局连续帧架构（严禁使用隔离的 \`\<Series\>\`）  
\- \*\*画布尺寸\*\*：提供 Props 参数支持 \`aspectRatio: "9:16" | "16:9"\`，默认竖屏 \`1080 x 1920\`（适配短视频），横屏 \`1920 x 1080\`。  
\- \*\*帧率 (FPS)\*\*：\`60 fps\`（确保弹簧形变与数字跳动极致丝滑）。  
\- \*\*单模型展示时长\*\*：\`150 帧\`（2.5 秒/模型），总帧数 \= \`models.length \* 150\`。  
\- \*\*全局状态驱动 (\`MainVideo.tsx\`)\*\*：  
  \- 使用 \`const frame \= useCurrentFrame()\` 计算当前模型索引：\`const currentIndex \= Math.min(models.length \- 1, Math.floor(frame / 150))\` 及局部帧 \`const localFrame \= frame % 150\`。  
  \- 同时提取 \`currentModel \= models\[currentIndex\]\` 与 \`prevModel \= models\[Math.max(0, currentIndex \- 1)\]\`。  
  \- \*\*0 \~ 35 帧（流体变形期）\*\*：使用 \`spring({ frame: localFrame, fps, config: { damping: 13, stiffness: 110 } })\` 计算过渡进度。为 6 个维度设置 \`index \* 2\` 帧的\*\*错峰延迟（Staggered Spring）\*\*，使多边形的 6 个顶点像液态金属波浪一样依次弹射到位！  
  \- \*\*20 \~ 45 帧（S级战力印章砸落）\*\*：右上角的 \`overall\_tier\`（如 \`S+\` / \`S\`）巨型发光徽章带缩放回弹特效砸入画面。  
  \- \*\*35 \~ 150 帧（呼吸扫描与情报读取期）\*\*：雷达图内部顺时针旋转极光扫描扇区（Radar Sweep），顶点微幅呼吸闪烁，底部终端打字机快速打出当前模型最亮眼的 \`evidence\` 摘要。

\---

\#\#\# 3\. 核心视觉组件拆分要求

\#\#\#\# A. 厂商专属霓虹主题引擎 (\`src/theme.ts\`)  
根据 \`provider\` 字符串匹配返回 \`{ primary, secondary, glowRgba, bgGradient }\`：  
\- \*\*OpenAI\*\*: 翡翠赛博绿 (\`\#10B981\`, \`\#34D399\`)  
\- \*\*Anthropic\*\*: 曜石琥珀金 (\`\#F59E0B\`, \`\#FBBF24\`)  
\- \*\*Google\*\*: 星云极光蓝紫 (\`\#3B82F6\`, \`\#A855F7\`)  
\- \*\*DeepSeek\*\*: 深海电光青 (\`\#06B6D4\`, \`\#38BDF8\`)  
\- \*\*Alibaba / Qwen\*\*: 脉冲紫罗兰 (\`\#8B5CF6\`, \`\#C084FC\`)  
\- \*\*Moonshot / Kimi\*\*: 霓虹洋红 (\`\#EC4899\`, \`\#F472B6\`)  
\- \*\*Zhipu / GLM\*\*: 烈焰赤红 (\`\#EF4444\`, \`\#F87171\`)  
\- \*\*其他厂商 (Meta / xAI / Mistral / Tencent / Xiaomi / MiniMax)\*\*: 各自配置高对比度科技霓虹色。  
同时提供国旗徽章映射函数（\`US \-\> 🇺🇸 US\`, \`CN \-\> 🇨🇳 CN\`, \`FR \-\> 🇫🇷 FR\`）。

\#\#\#\# B. 赛博 HUD 顶部信息栏 (\`src/components/HUDHeader.tsx\`)  
\- 左上角：机甲序列号 \`\[MODEL 04 / 18\]\` \+ 国旗地区胶囊徽章 \+ 厂商发光标签。  
\- 主标题：超大号加粗模型名称（切换时带 10 帧的水平滑入与微弱色差故障感）。  
\- 右侧战力计分板：\`OVERALL SCORE\` 滚动数字（从上一模型均分平滑跳动到当前均分，保留 1 位小数）+ 醒目的发光阶级印章（\`S+\` 金色辉光、\`S\` 琥珀色、\`A\` 电光蓝）。

\#\#\#\# C. 流体变形 SVG 雷达图 (\`src/components/MorphingRadar.tsx\`)  
纯手写高精度 SVG（零第三方重型图表库依赖）：  
1\. \*\*SVG 滤镜 (\`\<defs\>\`)\*\*：定义 \`\#neon-glow\` 高斯模糊发光滤镜，以及随当前厂商主题色动态变化的径向渐变填充 \`\#polygon-fill\`。  
2\. \*\*机甲刻度底盘\*\*：  
   \- 最外圈：缓慢逆时针旋转的精密仪表刻度环（\`stroke-dasharray\`）。  
   \- 同心六边形网格：绘制 4 层网格线，其中代表 \`raw\_score \= 90\`（S级分水岭）的那一层用高亮金色/青色虚线特别标出。  
   \- 旋转扫描线：一个半透明渐变扇形围绕圆心顺时针匀速扫描。  
3\. \*\*Ghost 残影层 \+ Active 变形层\*\*：  
   \- 先绘制 \`prevModel\` 的 \`display\_score\` 对应的六边形路径（白色半透明虚线 \`stroke="rgba(255,255,255,0.28)" strokeDasharray="8 6" fill="none"\`）。  
   \- 再绘制从 \`prevModel.display\_score\` 插值到 \`currentModel.display\_score\` 的动态多边形，描边 \`4px\` 并挂载 \`\#neon-glow\` 滤镜。  
4\. \*\*六维轴向标签与跳动分数\*\*：  
   \- 6 个方向依次为：\`科学推理 Reasoning\`、\`编程工程 Coding\`、\`智能体 Agentic\`、\`长上下文 Context\`、\`数据分析 Data\`、\`创意写作 Writing\`。  
   \- 每个轴线外侧显示：维度名称 \+ \*\*插值滚动的 \`raw\_score\` 整数\*\* \+ 彩色 \`tier\` 胶囊。若该维度 \`confidence \=== "low"\`，在分数旁附加一个醒目的黄色 \`\*\` 号并在角落注明 \`\* 低置信度估算\`。

\#\#\#\# D. 底部六维能量条矩阵与终端简评 (\`src/components/HUDFooter.tsx\`)  
为了填满 9:16 竖屏下半部分构图：  
\- \*\*2列 × 3行 能量条矩阵（Stat Bars）\*\*：展示 6 个维度的横向流光进度条，宽度按 \`display\_score\` 动态伸缩，直观对比长短板。  
\- \*\*底部黑客终端框（Terminal Evidence Box）\*\*：带闪烁光标的暗色毛玻璃卡片，截取当前模型最具代表性的 1\~2 条 \`evidence\` 文本（以打字机效果逐字显现），让硬核观众看清跑分依据（如 \`SWE-bench / Terminal-Bench 4.0 / AA-LCR\`）。

\---

\#\#\# 4\. 交付与运行检查  
请完整创建项目结构（\`package.json\`, \`tsconfig.json\`, \`remotion.config.ts\`, \`src/Root.tsx\`, \`src/MainVideo.tsx\` 及各子组件），确保没有任何未定义的变量或缺失依赖，讓我执行 \`npm install && npm run start\` 即可直接在浏览器预览丝滑的 60fps 雷达图变形动画。

### **两个项目联动的极简工作流**

> 1. 先在**数据项目**里把 **Prompt 1** 发给 AI，它会在几秒钟内生成 data/processed/radar\_ready.json。  
> 2. 把这个生成的 radar\_ready.json 复制到**视频项目**的 src/data/ 目录下，然后把 **Prompt 2** 发给视频项目的 AI。  
> 3. 以后如果觉得视频里哪个模型不满意，或者想调整雷达图的夸张程度，去**数据项目**改一行参数重新运行 python scripts/build\_radar\_data.py，把新生成的 JSON 拷过去，视频立刻自动更新！