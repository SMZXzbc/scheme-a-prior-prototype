[README.md](https://github.com/user-attachments/files/28678064/README.md)
# Scheme A Prior Prototype

> Minimal prototype for **Scheme A: LLM-based structured prior generation for Radio Map / Channel Knowledge Map generation**.

本项目用于验证方案 A 的前半段流程：

```text
Scene Description
        ↓
LLM / GPT
        ↓
Structured Prior
        ↓
Schema Validation
        ↓
Numerical Conditioning Vector
        ↓
Future Downstream Radio Map Generator
```

---

## 1. Project Goal

本项目的目标是探索：

```text
如何让 LLM 生成可检查、可编码、可用于下游模型的无线传播 prior？
```

更具体地说：

```text
给定 dense urban / 28 GHz 等无线传播场景
        ↓
GPT 生成 structured electromagnetic / radio-map-oriented prior
        ↓
Pydantic schema 检查字段和取值是否合法
        ↓
检查 mechanism_weights 是否接近归一化
        ↓
将 prior 编码成 numerical conditioning vector
```

后续这些 conditioning vector 可以作为条件信息，接入：

```text
Diffusion Model
Flow Matching
U-Net
RadioDiff
PhysFlow
其他 Radio Map Generator
```

---

## 2. Current Progress

### v1: Structured Electromagnetic Prior

v1 主要用于验证 GPT 是否可以生成结构化无线传播先验。

v1 prior 关注：

```text
dominant_mechanism
mechanism_weights
blockage_risk
channel_sparsity
expected_delay_spread
expected_angular_spread
beam_alignment_sensitivity
reasoning_summary
```

当前 v1 已完成：

```text
system prompt 设计
few-shot demonstrations
Pydantic schema
GPT-generated prior 数据
12 条 dense urban / 28 GHz case 测试
schema 检查
mechanism_weights 权重检查
```

---

### v2: Radio-Map-Oriented Prior

v2 在 v1 的基础上进一步升级。

v2 prior 不再只关注传播机制，而是更关注 Radio Map / Pathloss Map / Channel Knowledge Map 生成所需的空间提示信息。

v2 prior 增加了：

```text
radio_map_task
pathloss_level_hint
los_region_hint
nlos_region_hint
shadowing_region_hint
blockage_region_hint
reflection_region_hint
diffraction_region_hint
scattering_region_hint
building_density_hint
material_hint
effective_scatterer_hint
spatial_variation_hint
map_pattern_hint
conditioning_summary
```

当前 v2 已完成：

```text
Radio Map prior schema
v2 system prompt
v2 demonstrations
10 条 dense urban / 28 GHz case prior 生成
schema 检查
mechanism_weights 权重检查
13 维 conditioning vector 编码
v2 test record
prior encoding design
```

---

## 3. Project Structure

```text
scheme-a-prior-prototype/
│
├── README.md
│
├── data/
│   ├── gpt_test_priors.json
│   ├── gpt_radiomap_priors_v2.json
│   └── radiomap_prior_vectors_v2.json
│
├── prompts/
│   ├── system_prompt_v1.md
│   ├── demonstrations_v1.md
│   ├── system_prompt_radiomap_v2.md
│   └── demonstrations_radiomap_v2.md
│
├── schema/
│   ├── prior_schema.py
│   └── radiomap_prior_schema_v2.py
│
├── scripts/
│   ├── validate_priors.py
│   ├── validate_radiomap_priors_v2.py
│   └── encode_radiomap_priors_v2.py
│
└── docs/
    ├── test_record_v1.md
    ├── test_record_radiomap_v2.md
    └── prior_encoding_design.md
```

---

## 4. File Description

### `prompts/`

| File                            | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| `system_prompt_v1.md`           | v1 system prompt，用于生成 structured electromagnetic prior |
| `demonstrations_v1.md`          | v1 few-shot examples                                   |
| `system_prompt_radiomap_v2.md`  | v2 system prompt，用于生成 radio-map-oriented prior         |
| `demonstrations_radiomap_v2.md` | v2 few-shot examples                                   |

### `schema/`

| File                          | Description                                   |
| ----------------------------- | --------------------------------------------- |
| `prior_schema.py`             | v1 prior 的 Pydantic schema                    |
| `radiomap_prior_schema_v2.py` | v2 radio-map-oriented prior 的 Pydantic schema |

### `data/`

| File                             | Description                                  |
| -------------------------------- | -------------------------------------------- |
| `gpt_test_priors.json`           | v1 GPT-generated prior 数据                    |
| `gpt_radiomap_priors_v2.json`    | v2 GPT-generated radio-map-oriented prior 数据 |
| `radiomap_prior_vectors_v2.json` | v2 prior 编码后的 13 维 conditioning vector       |

### `scripts/`

| File                             | Description                             |
| -------------------------------- | --------------------------------------- |
| `validate_priors.py`             | 验证 v1 prior 是否符合 schema，并检查权重           |
| `validate_radiomap_priors_v2.py` | 验证 v2 prior 是否符合 schema，并检查权重           |
| `encode_radiomap_priors_v2.py`   | 将 v2 prior 编码成 13 维 conditioning vector |

### `docs/`

| File                         | Description                            |
| ---------------------------- | -------------------------------------- |
| `test_record_v1.md`          | v1 prior 测试记录                          |
| `test_record_radiomap_v2.md` | v2 prior 生成、验证和编码测试记录                  |
| `prior_encoding_design.md`   | v2 prior 到 conditioning vector 的编码设计说明 |

---

## 5. Current Pipeline

### Step 1: Generate Prior

使用：

```text
system_prompt_radiomap_v2.md
+
demonstrations_radiomap_v2.md
+
new input case
```

让 GPT 生成一条 radio-map-oriented prior。

Example input:

```text
case_id: DU_011
scene_type: dense urban
frequency_GHz: 28
condition: narrow street canyon NLOS
```

### Step 2: Validate Prior

运行：

```bash
python scripts/validate_radiomap_priors_v2.py
```

检查内容：

```text
字段是否完整
字段类型是否正确
枚举值是否合法
mechanism_weights 是否在 0 到 1 之间
mechanism_weights 总和是否接近 1.0
```

### Step 3: Encode Prior

运行：

```bash
python scripts/encode_radiomap_priors_v2.py
```

将 v2 prior 编码成 13 维 conditioning vector。

当前第一版 vector 结构为：

```text
6 维 dominant_mechanism one-hot
5 维 mechanism_weights
1 维 pathloss_level
1 维 building_density
```

即：

```text
6 + 5 + 1 + 1 = 13
```

---

## 6. Current Results

### v1 Test Result

当前 v1 共测试 12 条 dense urban / 28 GHz case。

结果：

```text
12 / 12 schema validation passed
12 / 12 mechanism_weights validation passed
```

### v2 Test Result

当前 v2 共测试 10 条 dense urban / 28 GHz case：

```text
DU_006 open square LOS
DU_011 narrow street canyon NLOS
DU_014 heavy pedestrian blockage
DU_016 glass building reflection
DU_017 vehicle blockage near street corner
DU_018 dense urban intersection NLOS
DU_019 building blockage NLOS
DU_020 rough concrete scattering
DU_021 moving user beam misalignment
DU_022 indoor penetration from outdoor base station
```

结果：

```text
10 / 10 schema validation passed
10 / 10 mechanism_weights validation passed
10 / 10 conditioning vector encoding passed
```

这说明 v2 prompt 可以在多个 dense urban / 28 GHz 场景下稳定生成字段完整、格式正确、物理含义基本合理的 radio-map-oriented prior。

---

## 7. Conditioning Vector Design

当前第一版 conditioning vector 长度为 13。

### Feature Names

```text
dominant_LOS
dominant_reflection
dominant_diffraction
dominant_scattering
dominant_penetration
dominant_mixed

weight_los
weight_reflection
weight_diffraction
weight_scattering
weight_penetration

pathloss_level
building_density
```

### Example

For:

```text
case_id: DU_011
condition: narrow street canyon NLOS
dominant_mechanism: reflection
pathloss_level_hint: high
building_density_hint: high
```

The vector is:

```text
[0, 1, 0, 0, 0, 0,
 0.03, 0.65, 0.08, 0.20, 0.04,
 1, 1]
```

---

## 8. Summary

本项目目前完成了从：

```text
Scene Description
```

到：

```text
GPT-generated structured prior
```

再到：

```text
13-dimensional numerical conditioning vector
```

的最小可运行流程。

当前阶段结论：

```text
v2 radio-map-oriented prior can be generated, validated, and encoded into a numerical conditioning vector.
```

后续重点是将该 conditioning vector 接入下游 diffusion / flow matching 等 Radio Map generation model。


