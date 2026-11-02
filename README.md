# Model Forge

Standalone AGPL-3.0 tool for model ablation (via Heretic CLI subprocess), benchmark evaluation, GGUF quantization, Ollama Modelfile packaging, and Ed25519-signed provenance manifest generation.

## Architectural Boundaries

- **License isolation:** `model-forge` is licensed under GNU Affero General Public License v3.0 (AGPL-3.0-or-later).
- **Subprocess invocation:** Calls Heretic as an independent subprocess using `--save-path` and `--non-interactive`.
- **Zero AGPL imports:** MIT repositories (`appEcosystem`, `cyber-agents`, `AI-for-Survival`, `AegisSIEM`) never import from `model-forge` or `heretic`. Communication occurs strictly through standard files (GGUF, Ollama Modelfile, JSON manifests) and HTTP/REST interfaces.
- **Strict policy contract:** All generated Ollama Modelfiles embed explicit JSON-proposal system instructions declaring that the model only proposes actions and cannot execute them without `PolicyEngine` approval.
