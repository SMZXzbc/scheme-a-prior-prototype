# Prior Encoding Design for Radio Map Prior v2

## 1. 目的

当前的 v2 prior 是 JSON 格式，里面包含了很多人能看懂的字段，例如：

- dominant_mechanism
- mechanism_weights
- pathloss_level_hint
- building_density_hint
- los_region_hint
- shadowing_region_hint
- reflection_region_hint
- map_pattern_hint

这些字段可以帮助我们理解一个场景下 Radio Map / Pathloss Map 应该大概呈现什么规律。

但是下游 Radio Map 生成模型通常不能直接使用自然语言描述，所以需要先把一部分稳定、结构化的字段转换成 numerical conditioning vector。

简单来说：

```text
v2 JSON prior
        ↓
numerical conditioning vector
        ↓
downstream Radio Map generator
```

---

## 2. 为什么需要 encoding？

v2 prior 当前更像“人能看懂的说明书”。

例如：

```json
{
  "dominant_mechanism": "reflection",
  "pathloss_level_hint": "high",
  "building_density_hint": "high"
}
```

人可以理解为：

```text
这个场景以反射为主
路径损耗较高
建筑密度较高
```

但是模型更适合接收数字形式，例如：

```text
reflection → [0, 1, 0, 0, 0, 0]
high → 1
medium → 0.5
low → 0
```

所以 encoding 的目的就是把 prior 里稳定的结构化信息转换成模型可用的数字输入。

---

## 3. 第一版先编码哪些字段？

第一版先不要太复杂，只编码最稳定、最容易转成数字的字段：

```text
1. dominant_mechanism
2. mechanism_weights
3. pathloss_level_hint
4. building_density_hint
```

原因：

- `dominant_mechanism` 是固定类别，可以做 one-hot 编码。
- `mechanism_weights` 本来就是数字，可以直接使用。
- `pathloss_level_hint` 是 low / medium / high，可以映射成数字。
- `building_density_hint` 也是 low / medium / high，可以映射成数字。

其他字段，例如：

```text
los_region_hint
nlos_region_hint
shadowing_region_hint
blockage_region_hint
reflection_region_hint
diffraction_region_hint
scattering_region_hint
material_hint
effective_scatterer_hint
spatial_variation_hint
map_pattern_hint
conditioning_summary
```

当前先保留为文本解释信息，后续可以再考虑转成 text embedding 或更细的人工类别特征。

---

## 4. 编码规则

### 4.1 dominant_mechanism 编码

`dominant_mechanism` 使用 one-hot 编码。

固定顺序为：

```text
LOS, reflection, diffraction, scattering, penetration, mixed
```

对应向量长度为 6。

例如：

```text
LOS → [1, 0, 0, 0, 0, 0]
reflection → [0, 1, 0, 0, 0, 0]
diffraction → [0, 0, 1, 0, 0, 0]
scattering → [0, 0, 0, 1, 0, 0]
penetration → [0, 0, 0, 0, 1, 0]
mixed → [0, 0, 0, 0, 0, 1]
```

---

### 4.2 mechanism_weights 编码

`mechanism_weights` 直接使用原始数值。

固定顺序为：

```text
los, reflection, diffraction, scattering, penetration
```

例如：

```json
"mechanism_weights": {
  "los": 0.03,
  "reflection": 0.65,
  "diffraction": 0.08,
  "scattering": 0.20,
  "penetration": 0.04
}
```

编码后为：

```text
[0.03, 0.65, 0.08, 0.20, 0.04]
```

---

### 4.3 pathloss_level_hint 编码

`pathloss_level_hint` 使用 low / medium / high 映射：

```text
low = 0
medium = 0.5
high = 1
```

例如：

```text
pathloss_level_hint = high → 1
pathloss_level_hint = medium → 0.5
pathloss_level_hint = low → 0
```

---

### 4.4 building_density_hint 编码

`building_density_hint` 也使用 low / medium / high 映射：

```text
low = 0
medium = 0.5
high = 1
```

例如：

```text
building_density_hint = high → 1
building_density_hint = medium → 0.5
building_density_hint = low → 0
```

---

## 5. 最终 conditioning vector 结构

第一版 conditioning vector 由四部分组成：

```text
dominant_mechanism_one_hot
+ mechanism_weights
+ pathloss_level_hint
+ building_density_hint
```

向量长度为：

```text
6 + 5 + 1 + 1 = 13
```

也就是说，每一条 v2 prior 最后会被转成一个 13 维数字向量。

---

## 6. 示例：DU_011

原始 v2 prior 的关键信息：

```text
case_id: DU_011
condition: narrow street canyon NLOS
dominant_mechanism: reflection
mechanism_weights:
  los: 0.03
  reflection: 0.65
  diffraction: 0.08
  scattering: 0.20
  penetration: 0.04
pathloss_level_hint: high
building_density_hint: high
```

### 6.1 dominant_mechanism

```text
reflection → [0, 1, 0, 0, 0, 0]
```

### 6.2 mechanism_weights

```text
[0.03, 0.65, 0.08, 0.20, 0.04]
```

### 6.3 pathloss_level_hint

```text
high → 1
```

### 6.4 building_density_hint

```text
high → 1
```

### 6.5 final conditioning vector

```text
[0, 1, 0, 0, 0, 0, 0.03, 0.65, 0.08, 0.20, 0.04, 1, 1]
```

---

## 7. feature_names

为了让向量里的每一维都能解释，定义 feature_names：

```text
[
  "dominant_LOS",
  "dominant_reflection",
  "dominant_diffraction",
  "dominant_scattering",
  "dominant_penetration",
  "dominant_mixed",

  "weight_los",
  "weight_reflection",
  "weight_diffraction",
  "weight_scattering",
  "weight_penetration",

  "pathloss_level",
  "building_density"
]
```

这样以后看到一个向量：

```text
[0, 1, 0, 0, 0, 0, 0.03, 0.65, 0.08, 0.20, 0.04, 1, 1]
```

就能知道每一维分别代表什么。

---

## 8. 输出文件设计

后续编码脚本将读取：

```text
data/gpt_radiomap_priors_v2.json
```

并输出：

```text
data/radiomap_prior_vectors_v2.json
```

输出文件中每一条数据包含：

```json
{
  "case_id": "DU_011",
  "condition": "narrow street canyon NLOS",
  "radio_map_task": "pathloss_map_generation",
  "feature_names": [
    "dominant_LOS",
    "dominant_reflection",
    "dominant_diffraction",
    "dominant_scattering",
    "dominant_penetration",
    "dominant_mixed",
    "weight_los",
    "weight_reflection",
    "weight_diffraction",
    "weight_scattering",
    "weight_penetration",
    "pathloss_level",
    "building_density"
  ],
  "conditioning_vector": [
    0,
    1,
    0,
    0,
    0,
    0,
    0.03,
    0.65,
    0.08,
    0.20,
    0.04,
    1,
    1
  ],
  "vector_length": 13,
  "conditioning_summary": "..."
}
```

---

## 9. 当前阶段结论

当前阶段先完成第一版简单 encoding。

第一版只编码结构稳定、容易量化的字段：

```text
dominant_mechanism
mechanism_weights
pathloss_level_hint
building_density_hint
```

这样可以先建立从：

```text
v2 prior JSON
```

到：

```text
numerical conditioning vector
```

的最小可运行流程。

后续如果需要更深入，可以继续把文本字段转成：

```text
text embedding
人工类别标签
空间区域 mask
更细粒度的 map condition
```

但当前阶段先不做复杂扩展。

---

## 10. 下一步

实现编码脚本：

```text
scripts/encode_radiomap_priors_v2.py
```

该脚本将完成：

```text
读取 gpt_radiomap_priors_v2.json
验证每条 prior
编码成 13 维 conditioning vector
保存到 radiomap_prior_vectors_v2.json
```