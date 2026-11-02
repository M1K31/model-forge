"""Ollama Modelfile generator with explicit JSON-proposal policy instructions."""

from __future__ import annotations

from pathlib import Path


def generate_modelfile_content(
    gguf_filename: str,
    temperature: float = 0.2,
    role: str = "security",
) -> str:
    """Generate an Ollama Modelfile enforcing the JSON proposal contract."""
    system_prompts = {
        "security": (
            "You are the ecosystem security analyst. You propose actions as JSON: "
            '{"action": "<action>", "action_class": "<investigate|contain|remediate>", "target": {...}, "rationale": "<reason>"}. '
            "You never execute actions directly; the ecosystem PolicyEngine gates and enforces all executions."
        ),
        "survival": (
            "You are the emergency survival assistant. You provide structured technical guidance as JSON: "
            '{"topic": "<medical|water|power|shelter>", "recommendation": "<text>", "urgency": "<low|medium|high>"}. '
            "All recommendations adhere to offline survival protocols."
        ),
    }

    selected_system = system_prompts.get(role, system_prompts["security"])

    lines = [
        f"FROM ./{gguf_filename}",
        f"PARAMETER temperature {temperature}",
        'PARAMETER stop "<|eot_id|>"',
        'PARAMETER stop "<|end_of_text|>"',
        f'SYSTEM """{selected_system}"""',
    ]
    return "\n".join(lines) + "\n"


def write_modelfile(
    output_path: Path | str,
    gguf_filename: str,
    role: str = "security",
) -> Path:
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    content = generate_modelfile_content(gguf_filename, role=role)
    p.write_text(content, encoding="utf-8")
    return p
