"""Unit tests for Model Forge pipeline, Modelfile generator, and signed manifests."""

from __future__ import annotations

import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ed25519

from model_forge import (
    ForgePipeline,
    generate_modelfile_content,
    get_recommendation_for_tier,
    sign_manifest,
    verify_manifest,
    ModelProvenanceManifest,
)


def test_tier_recommendations():
    rec0 = get_recommendation_for_tier(0)
    assert rec0.tier == 0
    assert "SmolLM" in rec0.base_model

    rec2 = get_recommendation_for_tier(2)
    assert rec2.tier == 2
    assert "Llama-3.1-8B" in rec2.base_model


def test_modelfile_generation_embeds_policy_json_instructions():
    content = generate_modelfile_content("model.Q4_K_M.gguf", role="security")
    assert "FROM ./model.Q4_K_M.gguf" in content
    assert "PARAMETER temperature 0.2" in content
    assert "You propose actions as JSON" in content
    assert "PolicyEngine gates and enforces all executions" in content


def test_manifest_signing_and_verification():
    key = ed25519.Ed25519PrivateKey.generate()
    manifest = ModelProvenanceManifest(
        model_id="test-model",
        base_model="meta-llama/Llama-3.1-8B-Instruct",
        tier=2,
        method="heretic_ara",
        eval_scores={"kl_divergence": 0.35, "cyber_triage_score": 0.95},
        gguf_file="test-model.gguf",
        sha256="abc123456",
    )
    signed = sign_manifest(manifest, key)
    assert signed.signature != ""
    assert signed.signer_fingerprint != ""

    # Verify signature
    assert verify_manifest(signed.to_dict()) is True


def test_pipeline_dry_run(tmp_path: Path):
    pipeline = ForgePipeline()
    res = pipeline.run(tier=2, output_dir=tmp_path / "out", dry_run=True)

    assert res.success is True
    assert Path(res.modelfile_path).is_file()
    assert Path(res.manifest_path).is_file()
    assert Path(res.gguf_path).is_file()

    manifest_json = json.loads(Path(res.manifest_path).read_text(encoding="utf-8"))
    assert manifest_json["tier"] == 2
    assert "signature" in manifest_json
    assert manifest_json["eval_scores"]["kl_divergence"] < 1.0

    modelfile_text = Path(res.modelfile_path).read_text(encoding="utf-8")
    assert "PolicyEngine" in modelfile_text

