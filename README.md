# AI 模型六维评测数据

当前 `data/raw/models.json` 收录 21 个模型。21 个模型的六维评分、证据与来源已全部补齐（126/126 维）；其中证据不足的维度明确标为低置信度估算。

六维分数是按项目规则作出的 0–100 编辑梯队映射，原始基准成绩、测试限制及置信度另存于各维度字段。`T3_Estimated` 为估算，不是实测。详见研究记录：[第一批](data/research/2026-10-19-batch-01.md)、[第二批](data/research/2026-10-19-batch-02.md)、[第三批](data/research/2026-10-19-batch-03.md)、[第四批](data/research/2026-10-19-batch-04.md)、[第五批](data/research/2026-10-19-batch-05.md)。

国家代码按提供方总部所在国家映射；原始文件未包含国家字段。

| 代码 | 国家 |
|---|---|
| US | 美国 |
| CN | 中国 |
| FR | 法国 |

运行 python scripts/validate.py 可检查基础字段，并查看六维评分完整率。
