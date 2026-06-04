# Prior 测试文件说明

这是 GPT-generated structured electromagnetic prior 的小规模测试结果。

主要目的是验证：

`system_prompt_v1.md` + `demonstrations_v1.md` 是否可以引导 GPT Plus 生成符合 schema 的 JSON prior。

---

## 文件说明

### system_prompt_v1.md

第一版 system prompt。

作用：

规定 GPT 的角色、输出格式、字段规则、物理规则，以及最终只能输出 JSON。

---

### demonstrations_v1.md

第一版 few-shot examples。

作用：

提供 3 条标准示例，让 GPT 模仿这些例子生成新的 structured electromagnetic prior。

---

### test_record_v1.md

测试记录文件。

作用：

记录本次测试过程和结果，包括：

- 测试了哪些 case
- schema 检查是否通过
- 权重检查是否通过
- 当前阶段结论

---

### gpt_test_priors.json

GPT Plus 实际生成的 prior 数据。

目前包含 DU_004 到 DU_015，共 12 条 dense urban / 28 GHz 场景的 JSON prior。

---

### prior_schema.py

Pydantic schema 文件。

作用：

规定一条 prior 必须包含哪些字段、字段类型是什么、哪些取值是允许的。

---

### validate_priors.py

验证脚本。

作用：

读取 `gpt_test_priors.json`，并检查：

- JSON 字段是否符合 schema
- 字段取值是否合法
- mechanism_weights 是否接近归一化为 1

---

## 运行方式

在项目根目录运行：

```bash
python scripts/validate_priors.py
```


