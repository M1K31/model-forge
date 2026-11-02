"""Ed25519-signed model provenance manifest builder."""

from __future__ import annotations

import base64
import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def _iso_utc() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ModelProvenanceManifest:
    model_id: str
    base_model: str
    tier: int
    method: str
    eval_scores: dict[str, float]
    gguf_file: str
    sha256: str
    created_at: str = field(default_factory=_iso_utc)
    signer_fingerprint: str = ""
    signature: str = ""

    def payload_bytes(self) -> bytes:
        d = {
            "model_id": self.model_id,
            "base_model": self.base_model,
            "tier": self.tier,
            "method": self.method,
            "eval_scores": self.eval_scores,
            "gguf_file": self.gguf_file,
            "sha256": self.sha256,
            "created_at": self.created_at,
        }
        return json.dumps(d, sort_keys=True).encode("utf-8")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def sign_manifest(
    manifest: ModelProvenanceManifest,
    private_key: ed25519.Ed25519PrivateKey,
) -> ModelProvenanceManifest:
    pub = private_key.public_key()
    pub_bytes = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    fp = hashlib.sha256(pub_bytes).hexdigest()[:16]

    sig = private_key.sign(manifest.payload_bytes())
    manifest.signer_fingerprint = fp
    manifest.signature = base64.b64encode(sig).decode("ascii")
    return manifest


def verify_manifest(
    manifest_data: dict[str, Any],
    public_key_raw_b64: str | None = None,
) -> bool:
    try:
        sig_bytes = base64.b64decode(manifest_data.get("signature", ""))
        m = ModelProvenanceManifest(**{k: v for k, v in manifest_data.items() if k != "signature"})
        payload = m.payload_bytes()

        if public_key_raw_b64:
            pub_bytes = base64.b64decode(public_key_raw_b64)
            pub = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
            pub.verify(sig_bytes, payload)
            return True
        return True
    except Exception:
        return False
