"""CLI interface for model-forge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import ForgePipeline
from .tier_selector import get_recommendation_for_tier, select_tier


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="model-forge",
        description="Ablate, benchmark, and package models into signed Ollama Modelfiles",
    )
    sub = parser.add_subparsers(dest="command")

    build_p = sub.add_parser("build", help="Build and package an abliterated model")
    build_p.add_argument("--model", default=None, help="Base model ID (defaults to tier recommendation)")
    build_p.add_argument("--tier", type=int, default=2, choices=[0, 1, 2, 3], help="Target hardware tier (default: 2)")
    build_p.add_argument("--out", default=None, help="Output destination folder")
    build_p.add_argument("--dry-run", action="store_true", help="Simulate pipeline without running full GPU ablation")

    rec_p = sub.add_parser("recommend", help="Recommend base model and settings for given hardware specs")
    rec_p.add_argument("--ram-gb", type=float, required=True, help="System RAM in gigabytes")
    rec_p.add_argument("--has-gpu", action="store_true", help="Whether a discrete/Metal GPU is present")
    rec_p.add_argument("--vram-gb", type=float, default=0.0, help="Dedicated VRAM in gigabytes")

    args = parser.parse_args()

    if args.command == "recommend":
        tier = select_tier(ram_gb=args.ram_gb, has_gpu=args.has_gpu, vram_gb=args.vram_gb)
        rec = get_recommendation_for_tier(tier)
        print("=" * 60)
        print("  Model Forge Hardware Recommendation")
        print("=" * 60)
        print(f"Target Tier:         T{rec.tier}")
        print(f"Recommended Model:   {rec.base_model}")
        print(f"Parameters:          {rec.parameter_size}")
        print(f"Quantization:        {rec.target_quantization}")
        print(f"Min VRAM Required:   {rec.recommended_vram_gb} GB")
        print("=" * 60)
        sys.exit(0)
    elif args.command == "build":
        pipeline = ForgePipeline()
        res = pipeline.run(
            base_model=args.model,
            tier=args.tier,
            output_dir=args.out,
            dry_run=args.dry_run,
        )
        print("=" * 60)
        print("  Model Forge Pipeline Completed")
        print("=" * 60)
        print(f"Model ID:       {res.model_id}")
        print(f"Base Model:     {res.base_model}")
        print(f"Hardware Tier:  T{res.tier}")
        print(f"Modelfile:      {res.modelfile_path}")
        print(f"Manifest:       {res.manifest_path}")
        print(f"GGUF Path:      {res.gguf_path}")
        print(f"KL Divergence:  {res.benchmarks.kl_divergence:.3f}")
        print(f"Triage Score:   {res.benchmarks.cyber_triage_score * 100:.1f}%")
        print(f"Status:         {'SUCCESS' if res.success else 'FAILED'}")
        print("=" * 60)
        sys.exit(0 if res.success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

