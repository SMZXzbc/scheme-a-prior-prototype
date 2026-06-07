[test_record_radiomap_v2.md.md](https://github.com/user-attachments/files/28677858/test_record_radiomap_v2.md.md)
# Test Record: Radio Map Prior v2

> 目的：记录 Radio Map oriented prior v2 的生成、验证和编码结果。  
> 当前阶段结论：v2 prompt 已经可以稳定生成字段完整、格式正确、物理含义基本合理的 radio-map-oriented prior，并且可以进一步编码为 13 维 numerical conditioning vector。

---

## 1. 测试目标

本测试用于验证以下三个部分是否可以形成稳定闭环：

```text
system_prompt_radiomap_v2.md
↓
demonstrations_radiomap_v2.md
↓
GPT-generated radio-map-oriented prior
↓
radiomap_prior_schema_v2.py 检查
↓
13 维 conditioning vector 编码
```

v2 prior 的目标不是只描述传播机制，而是为下游 Radio Map / Pathloss Map / Channel Knowledge Map 生成提供 conditioning information。

---

## 2. 使用文件

| 文件                                       | 作用                                      |
| ---------------------------------------- | --------------------------------------- |
| `prompts/system_prompt_radiomap_v2.md`   | 规定 GPT 的角色、输出格式、字段规则和物理规则               |
| `prompts/demonstrations_radiomap_v2.md`  | 提供 few-shot examples，引导 GPT 输出稳定 JSON   |
| `schema/radiomap_prior_schema_v2.py`     | 定义 v2 prior 的 Pydantic schema           |
| `data/gpt_radiomap_priors_v2.json`       | 保存 GPT 生成的 v2 prior                     |
| `scripts/validate_radiomap_priors_v2.py` | 检查 schema 和 mechanism_weights           |
| `scripts/encode_radiomap_priors_v2.py`   | 将 v2 prior 编码为 13 维 conditioning vector |
| `data/radiomap_prior_vectors_v2.json`    | 保存编码后的 numerical conditioning vector    |

---

## 3. 测试流程

```text
输入 dense urban / 28 GHz case
        ↓
使用 v2 system prompt + demonstrations
        ↓
GPT 生成 radio-map-oriented prior JSON
        ↓
保存到 data/gpt_radiomap_priors_v2.json
        ↓
运行 validate_radiomap_priors_v2.py
        ↓
检查字段、类型、枚举值和 mechanism_weights
        ↓
运行 encode_radiomap_priors_v2.py
        ↓
生成 13 维 conditioning vector
```

---

## 4. Batch Test v2-mini

### 4.1 测试目的

先使用 demonstrations 中的典型样例，验证 v2 prompt 和 schema 是否能够支持基本场景。

### 4.2 测试样例

| case_id | condition                 | schema 检查 | 权重检查 | radio-map prior 合理性 | 备注                       |
| ------- | ------------------------- | --------- | ---- | ------------------- | ------------------------ |
| DU_006  | open square LOS           | 通过        | 通过   | 合理                  | LOS 区域明显，pathloss 中等     |
| DU_011  | narrow street canyon NLOS | 通过        | 通过   | 合理                  | 反射主导，NLOS 和 shadowing 明显 |
| DU_014  | heavy pedestrian blockage | 通过        | 通过   | 合理                  | 动态遮挡明显，局部 pathloss 高     |

### 4.3 运行命令

```bash
python scripts/validate_radiomap_priors_v2.py
```

### 4.4 阶段结论

3 条基础样例均通过：

```text
schema 检查
mechanism_weights 权重检查
radio-map prior 合理性检查
```

说明 v2 system prompt 和 demonstrations 能够支持基本 dense urban / 28 GHz 场景的 structured prior 生成。

---

## 5. New Case Test v2

### 5.1 测试目的

验证 v2 prompt 是否能泛化到未出现在 demonstrations 中的新场景。

### 5.2 测试样例

| case_id | condition                           | schema 检查 | 权重检查 | radio-map prior 合理性 | 备注                                                        |
| ------- | ----------------------------------- | --------- | ---- | ------------------- | --------------------------------------------------------- |
| DU_016  | glass building reflection           | 通过        | 通过   | 合理                  | 玻璃幕墙反射明显，reflection region、material hint 和 map pattern 合理 |
| DU_017  | vehicle blockage near street corner | 通过        | 通过   | 合理                  | 车辆遮挡和街角阻塞明显，局部 high-loss region 合理                        |
| DU_018  | dense urban intersection NLOS       | 通过        | 通过   | 合理                  | 城市路口 NLOS 场景中 reflection、shadowing 和 spatial variation 合理 |

### 5.3 阶段结论

本轮测试使用 v2 system prompt 和 v2 demonstrations 生成了 3 条新 case：

```text
DU_016 glass building reflection
DU_017 vehicle blockage near street corner
DU_018 dense urban intersection NLOS
```

3 条新生成的 radio-map-oriented prior 均通过：

```text
schema 检查
mechanism_weights 权重检查
radio-map prior 合理性检查
```

这说明 v2 prompt 不仅能复现 demonstrations 中的样例，也能对新的 dense urban / 28 GHz 场景生成格式稳定、字段完整、物理含义合理的 Radio Map prior。

---

## 6. Prior Encoding Test v2

### 6.1 测试目的

验证 `scripts/encode_radiomap_priors_v2.py` 是否可以将 v2 structured prior 转换为 numerical conditioning vector。

### 6.2 编码规则

当前第一版 conditioning vector 长度为 13：

```text
6 维 dominant_mechanism one-hot
5 维 mechanism_weights
1 维 pathloss_level
1 维 building_density
```

也就是：

```text
6 + 5 + 1 + 1 = 13
```

### 6.3 使用文件

| 文件                                     | 作用                          |
| -------------------------------------- | --------------------------- |
| `data/gpt_radiomap_priors_v2.json`     | 输入：GPT 生成的 v2 prior         |
| `scripts/encode_radiomap_priors_v2.py` | 编码脚本                        |
| `data/radiomap_prior_vectors_v2.json`  | 输出：13 维 conditioning vector |

### 6.4 测试结果

| case_id | condition                           | vector_length | 编码结果 | 备注                                                    |
| ------- | ----------------------------------- | -------------:| ---- | ----------------------------------------------------- |
| DU_006  | open square LOS                     | 13            | 通过   | LOS one-hot、机制权重、pathloss level、building density 编码正常 |
| DU_011  | narrow street canyon NLOS           | 13            | 通过   | reflection one-hot 和 high pathloss 编码正常               |
| DU_014  | heavy pedestrian blockage           | 13            | 通过   | mixed one-hot 和 high pathloss 编码正常                    |
| DU_016  | glass building reflection           | 13            | 通过   | reflection one-hot 和 medium pathloss 编码正常             |
| DU_017  | vehicle blockage near street corner | 13            | 通过   | reflection one-hot 和 high pathloss 编码正常               |
| DU_018  | dense urban intersection NLOS       | 13            | 通过   | reflection one-hot 和 high pathloss 编码正常               |

### 6.5 阶段结论

本轮测试说明 v2 prior 已经可以从 JSON 文本形式转换为 13 维 numerical conditioning vector。

这一步完成了：

```text
v2 prior JSON
        ↓
numerical conditioning vector
        ↓
downstream Radio Map generator input
```

---

## 7. Additional Case Test v2

### 7.1 测试目的

继续增加不同传播条件的 dense urban / 28 GHz case，检查 v2 prior 生成和 encoding 是否稳定。

### 7.2 测试样例

| case_id | condition                                    | schema 检查 | 权重检查 | encoding 检查 | 备注                                                           |
| ------- | -------------------------------------------- | --------- | ---- | ----------- | ------------------------------------------------------------ |
| DU_019  | building blockage NLOS                       | 通过        | 通过   | 通过          | 建筑遮挡 NLOS 场景，shadowing、blockage 和 high pathloss 合理           |
| DU_020  | rough concrete scattering                    | 通过        | 通过   | 通过          | 粗糙混凝土散射场景，scattering 和 material hint 合理                      |
| DU_021  | moving user beam misalignment                | 通过        | 通过   | 通过          | 移动用户波束失配场景，spatial variation 和 beam-sensitive map pattern 合理 |
| DU_022  | indoor penetration from outdoor base station | 通过        | 通过   | 通过          | 室外基站到室内穿透场景，penetration、shadowing 和 high pathloss 合理         |

### 7.3 阶段结论

新增 4 条 case 均通过：

```text
schema 检查
mechanism_weights 权重检查
13 维 conditioning vector 编码
```

这说明 v2 prompt 对多种 dense urban / 28 GHz 传播条件具有一定稳定性。

---

## 8. 10-Case Test 总结

### 8.1 已测试 case

当前 v2 radio-map-oriented prior 共测试 10 条 dense urban / 28 GHz case：

| case_id | condition                                    | 场景类型                      |
| ------- | -------------------------------------------- | ------------------------- |
| DU_006  | open square LOS                              | LOS                       |
| DU_011  | narrow street canyon NLOS                    | NLOS / street canyon      |
| DU_014  | heavy pedestrian blockage                    | dynamic blockage          |
| DU_016  | glass building reflection                    | reflection / material     |
| DU_017  | vehicle blockage near street corner          | vehicle blockage          |
| DU_018  | dense urban intersection NLOS                | intersection NLOS         |
| DU_019  | building blockage NLOS                       | building blockage         |
| DU_020  | rough concrete scattering                    | scattering / material     |
| DU_021  | moving user beam misalignment                | mobility / beam-sensitive |
| DU_022  | indoor penetration from outdoor base station | penetration               |

### 8.2 总体验证结果

所有样例均通过：

```text
schema 检查
mechanism_weights 权重检查
13 维 numerical conditioning vector 编码
```

### 8.3 总体结论

当前测试说明：

```text
v2 prompt 可以在多个 dense urban / 28 GHz 场景下，
稳定生成字段完整、格式正确、物理含义基本合理的 radio-map-oriented prior。
```

同时，v2 prior 已经可以进一步转换为：

```text
13 维 numerical conditioning vector
```

这说明当前阶段已经完成：

```text
GPT-generated radio-map-oriented prior
        ↓
schema / weight validation
        ↓
conditioning vector encoding
```

---
