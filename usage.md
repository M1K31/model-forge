# Model Forge (`model-forge`) — Usage & Integration Guide

A complete operational guide for utilizing `model-forge` to select hardware tiers, run representation engineering pipelines via non-interactive Heretic subprocesses, evaluate candidate models against multi-domain benchmarks, package quantized `.gguf` artifacts into Ollama `Modelfile` definitions, and sign cryptographic Ed25519 provenance manifests for consumption across the **appEcosystem**.

---

## 1. Installation & Environment Setup

`model-forge` requires Python 3.10+ and operates in an isolated environment to maintain strict licensing boundaries (AGPL-3.0).

### Standard Installation

```bash
cd /path/to/model-forge

# Using uv (recommended)
uv venv .venv
source .venv/bin/activate
uv pip install -e .

# Or using standard pip
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verification

Ensure the `model-forge` CLI entry point is available:

```bash
model-forge --help
```

---

## 2. Hardware Tier Recommendation

Before initiating training or representation engineering, use the `recommend` subcommand to determine the optimal model family, parameter count, and quantization profile for the local hardware:

```bash
# Minimal edge device / Raspberry Pi (4GB RAM, no GPU)
model-forge recommend --ram-gb 4

# Standard laptop / entry desktop (8GB RAM, integrated graphics)
model-forge recommend --ram-gb 8

# Workstation / Mac with Apple Silicon (32GB RAM, Metal GPU)
model-forge recommend --ram-gb 32 --has-gpu --vram-gb 16

# Flagship GPU server (64GB RAM, 24GB VRAM)
model-forge recommend --ram-gb 64 --has-gpu --vram-gb 24
```

### Hardware Tier Reference Matrix

| Tier | Name | Target Specs | Base Model | Parameter Size | Target Quant | Min VRAM |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T0** | Minimal | < 8 GB RAM, CPU | `HuggingFaceTB/SmolLM2-360M-Instruct` | 360M | `Q4_K_M` | 1.0 GB |
| **T1** | Low | 8–16 GB RAM, CPU/iGPU | `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B | `Q4_K_M` | 4.0 GB |
| **T2** | Medium | 16–32 GB RAM, 8GB GPU/Metal | `meta-llama/Llama-3.1-8B-Instruct` | 8B | `Q4_K_M` | 8.0 GB |
| **T3** | High-End | 32+ GB RAM, 16GB+ VRAM | `Qwen/Qwen2.5-14B-Instruct` | 14B | `Q4_K_M` | 16.0 GB |

---

## 3. Running the Forge Pipeline

### Dry-Run Simulation (Testing & Validation)

Validate the pipeline and generate mock artifacts, Modelfiles, and signed manifests without consuming GPU cycles:

```bash
model-forge build --tier 2 --dry-run --out ./dist/models/llama-3.1-8b-simulated
```

### Production Execution

To run full representation engineering via Heretic, benchmark the ablated layers, quantize to GGUF, and sign the provenance manifest:

```bash
model-forge build \
  --tier 2 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --out ./dist/models/llama-3.1-8b-heretic
```

### Pipeline Output Artifacts

Upon successful completion, the output directory contains:

```text
./dist/models/llama-3.1-8b-heretic/
├── decensored/                # Extracted weights from Heretic ablation
│   └── config.json
├── llama-3.1-8b-heretic.Q4_K_M.gguf  # Quantized binary weights
├── Modelfile                  # Ollama configuration with policy prompt
└── provenance.json            # Ed25519-signed manifest & eval scores
```

---

## 4. Ollama Deployment & Registration

After `model-forge` builds the GGUF weights and `Modelfile`, import the model into the local Ollama runtime:

```bash
cd ./dist/models/llama-3.1-8b-heretic

# Create Ollama model instance
ollama create llama3.1-8b-heretic -f ./Modelfile

# Verify installation in Ollama
ollama list | grep llama3.1-8b-heretic

# Run quick inference test
ollama run llama3.1-8b-heretic "Analyze network event: unexpected connection to 192.168.1.50:4444"
```

The output will strictly adhere to the ecosystem JSON proposal contract:
```json
{
  "action": "isolate_host",
  "action_class": "contain",
  "target": {
    "scope": "device",
    "identifier": "192.168.1.50"
  },
  "rationale": "High-confidence reverse shell signature detected."
}
```

---

## 5. Provenance Verification

Ecosystem consumers verify the authenticity and integrity of forged models before loading them into operational pipelines:

### Python Verification API

```python
import json
from pathlib import Path
from model_forge import verify_manifest

manifest_path = Path("./dist/models/llama-3.1-8b-heretic/provenance.json")
manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))

# Verify payload structure and signature
is_valid = verify_manifest(manifest_data)
if not is_valid:
    raise ValueError("Untrusted or corrupted model package: signature check failed.")

print(f"Verified model {manifest_data['model_id']} (Tier {manifest_data['tier']})")
print(f"KL Divergence: {manifest_data['eval_scores']['kl_divergence']}")
print(f"Triage Accuracy: {manifest_data['eval_scores']['cyber_triage_score'] * 100:.1f}%")
```

---

## 6. Multi-App Ecosystem Integration

`model-forge` artifacts seamlessly connect with the ecosystem services while maintaining zero-import licensing isolation:

```text
┌─────────────────┐       Modelfile + .gguf       ┌──────────────────────┐
│   model-forge   │ ────────────────────────────> │        Ollama        │
│   (AGPL-3.0)    │                               │     Local Server     │
└─────────────────┘                               └──────────────────────┘
         │                                                   ▲
         │ provenance.json                                   │
         ▼ (Ed25519 Signed)                                  │ Prompts / JSON
┌─────────────────────────┐                                  │ Proposals
│ appEcosystem Hub        │ <────────────────────────────────┤
│ packages/ecosystem-ai   │                                  │
└─────────────────────────┘                                  │
         │                                                   │
         ├───────────────────────┬───────────────────────────┤
         ▼                       ▼                           ▼
┌──────────────────┐   ┌───────────────────┐   ┌───────────────────────────┐
│ AI-for-Survival  │   │     AegisSIEM     │   │       cyber-agents        │
│ (Cyber Command)  │   │  (Threat Triage)  │   │ (Offensive/Defensive Lab) │
└──────────────────┘   └───────────────────┘   └───────────────────────────┘
```

### Integration Workflow with `appEcosystem`

1. **Model Registration**:
   `appEcosystem`'s `packages/ecosystem-ai` reads `provenance.json`, checks SHA-256 digests of the `.gguf` weights, and confirms the `eval_scores` meet required thresholds (`kl_divergence < 1.0`, `cyber_triage_score >= 0.80`).
2. **Serving Through Hub**:
   `appEcosystem` registers the model under `task_models.security_analyst = "llama3.1-8b-heretic"`.
3. **Action Loop Execution**:
   When `AI-for-Survival` triggers Cyber Command or `AegisSIEM` triages an alert, the `action_loop` prompts `llama3.1-8b-heretic`.
4. **Policy Engine Enforcement**:
   The model returns a JSON proposal. The local `PolicyEngine` evaluates the proposal against active rules (e.g., verifying target is private IP, operator approval if required, freeze status) before any execution occurs.
