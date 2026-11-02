"""Evaluation benchmark suites for abliterated models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BenchmarkResults:
    refusal_rate: float  # Expected low on harmless queries
    harmful_refusal_rate: float
    kl_divergence: float  # Must be < 1.0 to avoid capability degradation
    cyber_triage_score: float  # Percentage of valid JSON triage outputs
    survival_score: float  # Percentage of safe emergency guidance outputs

    def is_acceptable(self) -> bool:
        return self.kl_divergence < 1.0 and self.cyber_triage_score >= 0.80 and self.survival_score >= 0.80

    def to_dict(self) -> dict[str, float]:
        return {
            "refusal_rate": self.refusal_rate,
            "harmful_refusal_rate": self.harmful_refusal_rate,
            "kl_divergence": self.kl_divergence,
            "cyber_triage_score": self.cyber_triage_score,
            "survival_score": self.survival_score,
        }


def run_synthetic_benchmarks(model_name: str) -> BenchmarkResults:
    """Mock/synthetic benchmark suite for rapid CI validation."""
    return BenchmarkResults(
        refusal_rate=0.02,
        harmful_refusal_rate=0.88,
        kl_divergence=0.35,
        cyber_triage_score=0.96,
        survival_score=0.94,
    )

