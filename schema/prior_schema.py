from pydantic import BaseModel, Field
from typing import Literal


class MechanismWeights(BaseModel):
    los: float = Field(ge=0, le=1)
    reflection: float = Field(ge=0, le=1)
    diffraction: float = Field(ge=0, le=1)
    scattering: float = Field(ge=0, le=1)
    penetration: float = Field(ge=0, le=1)


class ChannelPrior(BaseModel):
    case_id: str
    scene_type: Literal["dense urban", "suburban", "rural", "indoor"]
    frequency_GHz: float
    condition: str

    dominant_mechanism: Literal[
        "LOS",
        "reflection",
        "diffraction",
        "scattering",
        "penetration",
        "mixed"
    ]

    mechanism_weights: MechanismWeights

    blockage_risk: Literal["low", "medium", "high"]
    channel_sparsity: Literal["low", "medium", "high"]
    expected_delay_spread: Literal["low", "medium", "high"]
    expected_angular_spread: Literal["low", "medium", "high"]
    beam_alignment_sensitivity: Literal["low", "medium", "high"]

    reasoning_summary: str

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