# Privacy Policy

**Product**: Model Forge (`model-forge`)  
**Maintainer**: Smart Industries LLC (Mikel Smart)  
**Effective Date**: November 2026  

---

## 1. Local Model Generation & Zero Telemetry

`model-forge` operates strictly as a **local-first build tool**. It contains no background daemons, network analytics, advertising trackers, or telemetry beacons.

- **Local Execution**: All model distillation, tensor manipulation, benchmark execution, and GGUF conversions take place entirely on local hardware (or administrator-configured private compute nodes).
- **No Data Uploads**: Prompts, steering vectors, and evaluation benchmark transcripts are stored strictly on local disk within your configured output directory. They are never transmitted to third parties or remote cloud endpoints without explicit administrative action.

---

## 2. Training Data & Evaluation Prompts

1. **Synthetic & Standard Prompts**: Default benchmarks use static synthetic security events and benign refusal-probe datasets included in the repository.
2. **Local Sensitive Data Protection**: If custom prompt logs or incident telemetry are supplied as steering sets, they remain strictly on the local filesystem. Model Forge never exposes training corpora beyond the local host.

---

## 3. Cryptographic Keys & Manifests

- **Ed25519 Private Keys**: Model signing keys (`device_ed25519.key`) are stored locally with restrictive owner-only permissions (`0600`). Private keys are never embedded in generated model files, manifests, or public repositories.
- **Public Provenance**: Provenance manifests contain only cryptographic hashes (SHA-256) of base weights and outputs, along with the signer's public key. No personal identifiable information (PII) is included in the manifest.

---

## 4. Contact Information

For inquiries regarding Model Forge or security disclosures:  
**Smart Industries LLC** (Mikel Smart)

