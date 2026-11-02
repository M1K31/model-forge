# Model Forge (`model-forge`)

**Automated Representation Engineering, Distillation, GGUF Quantization & Model Provenance Pipeline**  
*Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0)*

`model-forge` is an independent, standalone model engineering toolkit built for the **appEcosystem**. It orchestrates representation engineering (via non-interactive [Heretic](https://github.com/p-e-w/heretic) subprocesses), rigorous automated benchmark evaluations, GGUF quantization, and cryptographic Ed25519-signed provenance manifest generation.

---

## 1. Architectural & Licensing Isolation Boundaries

- **Strict License Boundary**: `model-forge` is licensed under the AGPL-3.0.
- **Process Isolation Boundary**: `model-forge` invokes `heretic` exclusively as an external subprocess.
- **Zero AGPL Ingestion in MIT Repos**: No code, module, or library from `model-forge` or `heretic` is ever imported into the MIT-licensed repositories (`appEcosystem`, `AegisSIEM`, `cyber-agents`, `AI-for-Survival`, `OpenEye`, `MagicMirror-Custom`).
- **Inter-Process Artifacts Only**: Handoff between `model-forge` and the rest of the ecosystem occurs strictly via standard serialized artifacts: `.gguf` weights, Ollama `Modelfile` definitions, and signed JSON provenance manifests.
- **Fail-Closed Policy Contract**: All generated Ollama models explicitly embed system prompts instructing the model to output structured JSON proposals only (`{action, action_class, target, rationale}`). Models are strictly prohibited from executing commands directly; every action must pass through the local `PolicyEngine`.

---

## 2. End-to-End Pipeline

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Hardware Tier   │ ──> │ Heretic Run     │ ──> │ Multi-Domain    │
│ Selector (T0–T3)│     │ (Subprocess)    │     │ Benchmark Suite │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Ed25519 Signed  │ <── │ Ollama          │ <── │ GGUF Conversion │
│ Manifest        │     │ Modelfile Build │     │ & Quantization  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Pipeline Stages
1. **Hardware Tier Selection (`tier_selector.py`)**:
   - `T0_MINIMAL` (< 8GB RAM, no GPU): Maps to distilled 1.5B–3B compact architectures (e.g. `llama3.2:1b`, `qwen2.5:1.5b`).
   - `T1_LOW` (8–16GB RAM, CPU/integrated): Maps to 3B–7B balanced models (e.g. `llama3.2:3b`, `qwen2.5:3b`).
   - `T2_MEDIUM` (16–32GB RAM, Metal / 8GB VRAM): Maps to 7B–8B workhorse models (e.g. `llama3.1:8b-instruct`, `mistral-nemo:12b`).
   - `T3_HIGH_END` (32GB+ RAM, 16GB+ VRAM): Maps to 14B–70B flagship models (e.g. `qwen2.5:14b`, `llama3.1:70b-instruct`).
2. **Subprocess Representation Engineering (`pipeline.py`)**:
   - Invokes Heretic non-interactively using `--save-path` and `--non-interactive` flags to identify Pareto-optimal ablation layers without prompting for terminal input.
3. **Multi-Domain Benchmark Evaluation (`benchmarks.py`)**:
   - **Refusal Suppression & Alignment**: Evaluates refusal rates and ensures KL divergence remains $< 1.0$ against the baseline model to verify general intelligence is preserved.
   - **Cyber Triage Suite**: Evaluates parsing and attribution accuracy on MITRE ATT&CK security events (for `cyber-agents` and `AegisSIEM`).
   - **Survival & First-Aid Guidance**: Verifies offline medical triage and emergency chemistry extraction accuracy (for `AI-for-Survival`).
4. **Quantization & Modelfile Packaging (`modelfile.py`)**:
   - Quantizes FP16 weights to standard GGUF formats (`Q4_K_M`, `Q5_K_M`, `Q8_0`).
   - Formulates Ollama `Modelfile` embedding temperature limits and the JSON proposal contract.
5. **Cryptographic Manifest Signing (`manifest.py`)**:
   - Computes SHA-256 digests over all base weights, datasets, and output `.gguf` files.
   - Signs the `ModelProvenanceManifest` with the operator's Ed25519 key.

---

## 3. CLI Usage

```bash
# Display recommended model for the host hardware
model-forge recommend --ram-gb 32 --has-gpu --gpu-vram-gb 16

# Run full pipeline for hardware tier T2
model-forge build \
  --tier T2 \
  --base-model meta-llama/Llama-3.1-8B-Instruct \
  --output-dir ./dist/models \
  --key-path ~/.local/share/ecosystem/keystore/device_ed25519.key

# Verify provenance of an existing model package
model-forge verify ./dist/models/llama-3.1-8b-instruct-heretic.manifest.json
```

---

## 4. Evaluation Criteria & Thresholds

| Benchmark Metric | Target Value | Failure Action |
| :--- | :--- | :--- |
| **KL Divergence** | $\le 1.0$ | Discard trial; fallback to unablated base model |
| **Cyber Triage Accuracy** | $\ge 90\%$ | Fail build; report missing ATT&CK schema tokens |
| **Survival Triage Accuracy** | $\ge 92\%$ | Fail build; report degraded emergency knowledge |
| **JSON Proposal Validity** | $100\%$ | Reject Modelfile; re-tune temperature parameter |

---

## 5. License

Copyright © 2026 Smart Industries LLC (Mikel Smart).  
Licensed under the [GNU Affero General Public License v3.0](LICENSE).
