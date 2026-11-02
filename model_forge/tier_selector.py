"""Hardware tier to base model recommendation selector."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TierRecommendation:
    tier: int
    base_model: str
    parameter_size: str
    target_quantization: str
    recommended_vram_gb: float


TIER_RECOMMENDATIONS = {
    0: TierRecommendation(
        tier=0,
        base_model="HuggingFaceTB/SmolLM2-360M-Instruct",
        parameter_size="360M",
        target_quantization="Q4_K_M",
        recommended_vram_gb=1.0,
    ),
    1: TierRecommendation(
        tier=1,
        base_model="Qwen/Qwen2.5-1.5B-Instruct",
        parameter_size="1.5B",
        target_quantization="Q4_K_M",
        recommended_vram_gb=4.0,
    ),
    2: TierRecommendation(
        tier=2,
        base_model="meta-llama/Llama-3.1-8B-Instruct",
        parameter_size="8B",
        target_quantization="Q4_K_M",
        recommended_vram_gb=8.0,
    ),
    3: TierRecommendation(
        tier=3,
        base_model="Qwen/Qwen2.5-14B-Instruct",
        parameter_size="14B",
        target_quantization="Q4_K_M",
        recommended_vram_gb=16.0,
    ),
}


def get_recommendation_for_tier(tier: int) -> TierRecommendation:
    bounded = max(0, min(3, tier))
    return TIER_RECOMMENDATIONS[bounded]
