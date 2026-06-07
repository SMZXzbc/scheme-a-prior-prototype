import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from schema.radiomap_prior_schema_v2 import RadioMapPriorV2


INPUT_PATH = PROJECT_ROOT / "data" / "gpt_radiomap_priors_v2.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "radiomap_prior_vectors_v2.json"


DOMINANT_MECHANISM_ORDER = [
    "LOS",
    "reflection",
    "diffraction",
    "scattering",
    "penetration",
    "mixed"
]

LEVEL_MAP = {
    "low": 0.0,
    "medium": 0.5,
    "high": 1.0
}


FEATURE_NAMES = [
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


def one_hot_dominant_mechanism(mechanism: str):
    return [
        1.0 if mechanism == item else 0.0
        for item in DOMINANT_MECHANISM_ORDER
    ]


def encode_prior(prior: RadioMapPriorV2):
    w = prior.mechanism_weights

    dominant_vector = one_hot_dominant_mechanism(
        prior.dominant_mechanism
    )

    mechanism_vector = [
        w.los,
        w.reflection,
        w.diffraction,
        w.scattering,
        w.penetration
    ]

    level_vector = [
        LEVEL_MAP[prior.pathloss_level_hint],
        LEVEL_MAP[prior.building_density_hint]
    ]

    final_vector = dominant_vector + mechanism_vector + level_vector

    return final_vector


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        raw_priors = json.load(f)

    encoded_results = []

    for item in raw_priors:
        prior = RadioMapPriorV2(**item)

        passed, total = prior.check_weight_sum()
        if not passed:
            raise ValueError(
                f"{prior.case_id} mechanism_weights sum is {total}, not close to 1.0"
            )

        vector = encode_prior(prior)

        encoded_results.append({
            "case_id": prior.case_id,
            "condition": prior.condition,
            "radio_map_task": prior.radio_map_task,
            "feature_names": FEATURE_NAMES,
            "conditioning_vector": vector,
            "vector_length": len(vector),
            "conditioning_summary": prior.conditioning_summary
        })

        print(f"{prior.case_id} encoded, vector length = {len(vector)}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(encoded_results, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()