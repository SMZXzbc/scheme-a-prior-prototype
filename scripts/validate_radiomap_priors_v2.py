import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from schema.radiomap_prior_schema_v2 import RadioMapPriorV2


data_path = PROJECT_ROOT / "data" / "gpt_radiomap_priors_v2.json"

with open(data_path, "r", encoding="utf-8") as f:
    priors = json.load(f)


for item in priors:
    try:
        prior = RadioMapPriorV2(**item)

        passed, total = prior.check_weight_sum()

        print("case_id:", prior.case_id)
        print("condition:", prior.condition)
        print("schema 检查通过")
        print("weight total:", total)

        if passed:
            print("权重检查通过")
        else:
            print("权重检查失败")

    except Exception as e:
        print("schema 检查失败")
        print(e)

    print("-" * 40)