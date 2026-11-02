"""CLI interface for model-forge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import ForgePipeline


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

    args = parser.parse_args()

    if args.command == "build":
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

