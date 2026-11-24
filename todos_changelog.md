# Model Forge (`model-forge`) — Engineering Tracker & Changelog

**Owner**: Smart Industries LLC (Mikel Smart)  
**Classification**: Public Open-Source Engineering & Release Tracker  
**License**: GNU Affero General Public License v3.0 (AGPL-3.0)  

---

## 1. Feature Roadmap & Upcoming Milestones

This tracker consolidates planned enhancements, architectural milestones, and pending work for `model-forge` within the broader **appEcosystem** (`appEcosystem`, `AegisSIEM`, `cyber-agents`, `AI-for-Survival`, `OpenEye`, `MagicMirror-Custom`).

### Core Engine & Subprocess Orchestration
- [ ] **FORGE-01: Upstream Non-Interactive Heretic Contribution**: Upstream PR to Heretic repository providing first-class `--non-interactive` flag and `--save-path` configuration to prevent interactive prompts on completion.
- [ ] **FORGE-02: Automated GGUF Conversion Tooling**: Direct integration with `llama.cpp`'s `convert_hf_to_gguf.py` and quantization binaries (`quantize`) to automate the transition from ablated FP16 PyTorch weights to multi-tier GGUF (`Q4_K_M`, `Q5_K_M`, `Q8_0`).
- [ ] **FORGE-03: SkyPilot Remote Cloud Offloading**: SkyPilot task definition (`sky/heretic.yaml`) allowing compute-heavy T3 models (14B–70B) to train on spot GPU instances (RunPod, Lambda Labs) and synchronize signed `.gguf` weights back to the local ecosystem hub.
- [ ] **FORGE-04: Direct Ollama Management API**: Automate model registration via Ollama's REST API (`POST /api/create`) upon pipeline completion, eliminating manual terminal interaction.

### Evaluation & Benchmarks
- [ ] **FORGE-05: Real-Time Multi-Domain Task Suites**: Expand synthetic benchmark suite into full live test suites:
  - MITRE ATT&CK event classification and JSON proposal parsing for `AegisSIEM` and `cyber-agents`.
  - Offline emergency medical triage, water sanitation, and radio frequency guidance for `AI-for-Survival`.
  - KL divergence calculation against FP16 baseline embeddings.
- [ ] **FORGE-06: Refusal Suppression Profiling**: Automated measurement of refusal rates on benign cybersecurity and survival queries to verify effective representation engineering.

### Ecosystem Integration & Security
- [ ] **FORGE-07: Key Management & Hardware Token Signing**: Support for Ed25519 signing via PKCS#11 hardware security keys (YubiKey) for high-assurance provenance manifests.
- [ ] **FORGE-08: Automatic Task-Model Catalog Registration**: Automatic broadcast of newly forged models to `appEcosystem` hub's `task_models` catalog via authenticated HMAC event dispatch (`model.published`).

---

## 2. Release History & Changelog

### v0.1.0 — Initial Standalone Release (2026-11-23)

#### Core Features
- **Standalone AGPL-3.0 Architecture**: Initial release with strict licensing and process isolation boundaries. Zero code imported into MIT ecosystem repositories.
- **Hardware Tier Classifier (`tier_selector.py`)**: Automatic mapping of host RAM, discrete/Metal GPU presence, and VRAM into hardware tiers (T0–T3) with recommended base models (SmolLM2-360M, Qwen2.5-1.5B, Llama-3.1-8B, Qwen2.5-14B).
- **Subprocess Pipeline Runner (`pipeline.py`)**: Non-interactive Heretic runner executing representation engineering and layer ablation in an isolated subprocess.
- **JSON Proposal Modelfile Generator (`modelfile.py`)**: Automatic generation of Ollama Modelfile enforcing temperature limits (0.2) and the ecosystem JSON proposal contract (`{action, action_class, target, rationale}`) with explicit PolicyEngine gating instructions.
- **Ed25519 Cryptographic Provenance Manifests (`manifest.py`)**: SHA-256 payload integrity hashing and Ed25519 signature generation and verification.
- **Evaluation Benchmark Suite (`benchmarks.py`)**: Scoring criteria for refusal suppression, KL divergence degradation thresholds (< 1.0), and triage proposal validity.
- **CLI Commands (`cli.py`)**:
  - `model-forge recommend`: Hardware profiling and tier selection.
  - `model-forge build`: End-to-end dry-run and production ablation pipeline.
