import json
import sys
from pathlib import Path

# 把项目根目录 prior 加入 Python 的搜索路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from schema.prior_schema import ChannelPrior


with open("data/gpt_test_priors.json", "r", encoding="utf-8") as f:
    priors = json.load(f)


for item in priors:
    try:
        prior = ChannelPrior(**item)

        passed, total = prior.check_weight_sum()

        print("case_id:", prior.case_id)
        print("schema 检查通过")
        print("weight total:", total)

        if passed:
            print("权重检查通过")
        else:
            print("权重检查失败")

    except Exception as e:
        print("schema 检查失败")
        print(e)

    print("-" * 30)