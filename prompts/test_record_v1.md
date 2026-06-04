# Test Record v1

## 测试目的

验证 `system_prompt_v1.md` + `demonstrations_v1.md` 是否可以引导 GPT Plus 生成符合 schema 的 structured electromagnetic prior。

---

## 使用文件

- prompts/system_prompt_v1.md
- prompts/demonstrations_v1.md
- data/gpt_test_priors.json
- scripts/validate_priors.py

---

## Test 1：Dense Urban + 28 GHz + Street Corner NLOS

### 测试输入

```text
case_id: DU_004
scene_type: dense urban
frequency_GHz: 28
condition: street corner NLOS
```

---

### GPT 输出结果

```json
{
  "case_id": "DU_004",
  "scene_type": "dense urban",
  "frequency_GHz": 28,
  "condition": "street corner NLOS",
  "dominant_mechanism": "reflection",
  "mechanism_weights": {
    "los": 0.03,
    "reflection": 0.62,
    "diffraction": 0.10,
    "scattering": 0.20,
    "penetration": 0.05
  },
  "blockage_risk": "high",
  "channel_sparsity": "high",
  "expected_delay_spread": "high",
  "expected_angular_spread": "medium",
  "beam_alignment_sensitivity": "high",
  "reasoning_summary": "In dense urban 28 GHz street corner NLOS, the direct path is blocked, so reflections dominate while diffraction and penetration remain weak."
}
```

---

### 权重检查

```text
0.03 + 0.62 + 0.10 + 0.20 + 0.05 = 1.00
```

权重总和为 1.0，符合要求。

---

### 程序检查结果

运行命令：

```bash
python scripts/validate_priors.py
```

输出结果：

```text
case_id: DU_004
schema 检查通过
weight total: 1.0
权重检查通过
------------------------------
```

---

## Test 1 结论

GPT Plus 成功生成了完整 JSON prior。

该 prior：

- 字段完整
- schema 检查通过
- mechanism_weights 总和为 1.0
- 权重检查通过
- 物理判断基本合理

说明 `system_prompt_v1.md` + `demonstrations_v1.md` 可以初步引导 GPT Plus 生成符合要求的 structured electromagnetic prior。

---

## Batch Test v1

| case_id | condition | schema检查 | 权重检查 | 物理合理性 | 备注 |
|--------|--------------------------------|------------|----------|------------|-------------------|
| DU_004 | street corner NLOS             | 通过       | 通过     | 合理       | reflection 主导   |
| DU_005 | glass building reflection      | 通过       | 通过     | 合理       | reflection 增强   |
| DU_006 | open square LOS                | 通过       | 通过     | 合理       | LOS 主导          |
| DU_007 | building blockage NLOS         | 通过       | 通过     | 合理       | blockage 风险高   |
| DU_008 | rough concrete scattering      | 通过       | 通过     | 合理       | scattering 增强   |
| DU_009 | moving user beam misalignment  | 通过       | 通过     | 合理       | beam sensitivity 高 |

---

## Batch Test v1 结论

本次共测试 6 条 dense urban / 28 GHz 场景 prior：

- DU_004 street corner NLOS
- DU_005 glass building reflection
- DU_006 open square LOS
- DU_007 building blockage NLOS
- DU_008 rough concrete scattering
- DU_009 moving user beam misalignment

结果显示：

- 6 / 6 条 JSON 字段完整
- 6 / 6 条通过 Pydantic schema 检查
- 6 / 6 条 mechanism_weights 权重检查通过
- 权重总和均接近 1.0
- 输出结果基本符合 dense urban / 28 GHz 的传播物理规律

说明 `system_prompt_v1.md` + `demonstrations_v1.md` 在当前小规模测试中，可以稳定引导 GPT Plus 生成符合 schema 的 structured electromagnetic prior。

## Batch Test v2

继续使用同一版 `system_prompt_v1.md` 和 `demonstrations_v1.md`，扩展测试更多 dense urban / 28GHz 场景。

| case_id | condition | schema检查 | 权重检查 | 物理合理性 | 备注 |
|--------|----------------------------------------------|------------|----------|------------|-------------------|
| DU_010 | vehicle blockage                             | 通过       | 通过     | 合理       | blockage 风险高   |
| DU_011 | narrow street canyon NLOS                    | 通过       | 通过     | 合理       | reflection 主导   |
| DU_012 | high-rise building reflection                | 通过       | 通过     | 合理       | reflection 增强   |
| DU_013 | indoor penetration from outdoor base station | 通过       | 通过     | 合理       | penetration 增强  |
| DU_014 | heavy pedestrian blockage                    | 通过       | 通过     | 合理       | blockage 风险高   |
| DU_015 | multiple reflected paths                     | 通过       | 通过     | 合理       | 多反射路径明显    |

---

## Batch Test v2 结论

本次继续测试 6 条 dense urban / 28 GHz 场景 prior：

- DU_010 vehicle blockage
- DU_011 narrow street canyon NLOS
- DU_012 high-rise building reflection
- DU_013 indoor penetration from outdoor base station
- DU_014 heavy pedestrian blockage
- DU_015 multiple reflected paths

结果显示：

- 6 / 6 条 JSON 字段完整
- 6 / 6 条通过 Pydantic schema 检查
- 6 / 6 条 mechanism_weights 权重检查通过
- 权重总和均为 1.0
- 输出结果基本符合 dense urban / 28 GHz 的传播物理规律

结合 Batch Test v1，目前共测试 12 条 GPT-generated prior，全部通过 schema 检查和权重检查。

说明 `system_prompt_v1.md` + `demonstrations_v1.md` 在当前小规模测试中具有较好的输出稳定性。

---

## 当前阶段总总结

目前使用同一版 `system_prompt_v1.md` 和 `demonstrations_v1.md`，共测试了 12 条 dense urban / 28 GHz 场景的 GPT-generated structured electromagnetic prior。

测试范围包括：

- LOS
- NLOS
- street corner NLOS
- glass building reflection
- open square LOS
- building blockage NLOS
- rough concrete scattering
- moving user beam misalignment
- vehicle blockage
- narrow street canyon NLOS
- high-rise building reflection
- indoor penetration from outdoor base station
- heavy pedestrian blockage
- multiple reflected paths

测试结果：

- 12 / 12 条 JSON 字段完整
- 12 / 12 条通过 Pydantic schema 检查
- 12 / 12 条 mechanism_weights 权重检查通过
- 权重总和均接近或等于 1.0
- 输出结果整体符合 dense urban / 28 GHz 的基本传播规律

阶段结论：

`system_prompt_v1.md` + `demonstrations_v1.md` 可以在当前小规模测试中稳定引导 GPT Plus 生成符合 schema 的 structured electromagnetic prior。
