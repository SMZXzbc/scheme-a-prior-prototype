# Demonstrations v1

这个文件用于保存 few-shot examples。

作用：

让 GPT 学会根据输入场景，模仿标准格式生成 structured electromagnetic prior。

---

## Demonstration 1: Dense Urban + 28 GHz + LOS

### Input

```text
case_id: DU_001
scene_type: dense urban
frequency_GHz: 28
condition: LOS
```

### Output

```json
{
  "case_id": "DU_001",
  "scene_type": "dense urban",
  "frequency_GHz": 28,
  "condition": "LOS",
  "dominant_mechanism": "mixed",
  "mechanism_weights": {
    "los": 0.45,
    "reflection": 0.35,
    "diffraction": 0.05,
    "scattering": 0.10,
    "penetration": 0.05
  },
  "blockage_risk": "medium",
  "channel_sparsity": "high",
  "expected_delay_spread": "low",
  "expected_angular_spread": "low",
  "beam_alignment_sensitivity": "high",
  "reasoning_summary": "In dense urban 28 GHz LOS, the direct path and building reflections dominate, while diffraction and penetration are weak."
}
```

---

## Demonstration 2: Dense Urban + 28 GHz + NLOS

### Input

```text
case_id: DU_002
scene_type: dense urban
frequency_GHz: 28
condition: NLOS
```

### Output

```json
{
  "case_id": "DU_002",
  "scene_type": "dense urban",
  "frequency_GHz": 28,
  "condition": "NLOS",
  "dominant_mechanism": "reflection",
  "mechanism_weights": {
    "los": 0.05,
    "reflection": 0.60,
    "diffraction": 0.10,
    "scattering": 0.20,
    "penetration": 0.05
  },
  "blockage_risk": "high",
  "channel_sparsity": "high",
  "expected_delay_spread": "high",
  "expected_angular_spread": "medium",
  "beam_alignment_sensitivity": "high",
  "reasoning_summary": "In dense urban 28 GHz NLOS, reflection becomes the main propagation mechanism, while diffraction is weak."
}
```

---

## Demonstration 3: Dense Urban + 28 GHz + Human Blockage

### Input

```text
case_id: DU_003
scene_type: dense urban
frequency_GHz: 28
condition: human blockage
```

### Output

```json
{
  "case_id": "DU_003",
  "scene_type": "dense urban",
  "frequency_GHz": 28,
  "condition": "human blockage",
  "dominant_mechanism": "mixed",
  "mechanism_weights": {
    "los": 0.10,
    "reflection": 0.45,
    "diffraction": 0.05,
    "scattering": 0.30,
    "penetration": 0.10
  },
  "blockage_risk": "high",
  "channel_sparsity": "high",
  "expected_delay_spread": "medium",
  "expected_angular_spread": "medium",
  "beam_alignment_sensitivity": "high",
  "reasoning_summary": "Human blockage at 28 GHz weakens the direct path, making reflected and scattered paths more important."
}
```

---

## 使用方式

后续调用 GPT Plus 时，把以下三部分一起提供：

1. `system_prompt_v1.md`
2. `demonstrations_v1.md`
3. 新的测试输入场景

目标是让 GPT 模仿上面的 examples，生成新的 structured electromagnetic prior。