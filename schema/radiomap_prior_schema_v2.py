from pydantic import BaseModel, Field
from typing import Literal


class MechanismWeights(BaseModel):
    los: float = Field(ge=0, le=1)
    reflection: float = Field(ge=0, le=1)
    diffraction: float = Field(ge=0, le=1)
    scattering: float = Field(ge=0, le=1)
    penetration: float = Field(ge=0, le=1)


class RadioMapPriorV2(BaseModel):
    case_id: str

    scene_type: Literal[
        "dense urban",
        "suburban",
        "rural",
        "indoor"
    ]

    frequency_GHz: float
    condition: str

    radio_map_task: Literal[
        "pathloss_map_generation",
        "rss_map_generation",
        "channel_knowledge_map_generation"
    ]

    dominant_mechanism: Literal[
        "LOS",
        "reflection",
        "diffraction",
        "scattering",
        "penetration",
        "mixed"
    ]

    mechanism_weights: MechanismWeights

    pathloss_level_hint: Literal[
        "low",
        "medium",
        "high"
    ]

    los_region_hint: str
    nlos_region_hint: str
    shadowing_region_hint: str
    blockage_region_hint: str
    reflection_region_hint: str
    diffraction_region_hint: str
    scattering_region_hint: str

    building_density_hint: Literal[
        "low",
        "medium",
        "high"
    ]

    material_hint: str
    effective_scatterer_hint: str
    spatial_variation_hint: str
    map_pattern_hint: str

    conditioning_summary: str

    def check_weight_sum(self):
        w = self.mechanism_weights

        total = (
            w.los
            + w.reflection
            + w.diffraction
            + w.scattering
            + w.penetration
        )

        return abs(total - 1.0) < 0.05, total