"""Launch an Ollama instance on Modal and run a small YourBench test."""

from __future__ import annotations
import os
import tempfile
import subprocess
from pathlib import Path

import yaml
import modal


# Modal setup
stub = modal.Stub("yourbench-ollama-modal")

image = (
    modal.Image.debian_slim()
    .apt_install("curl", "gnupg")
    .run_commands(["curl -fsSL https://ollama.ai/install.sh | sh"])
)


@stub.function(image=image, timeout=60 * 60)
@modal.web_server(port=11434)
def ollama_service(model: str) -> None:
    """Start Ollama and keep serving requests."""
    import subprocess as sp

    sp.run(["ollama", "pull", model], check=True)
    sp.run(["ollama", "serve"], check=True)


def run_pipeline(base_url: str) -> None:
    """Run YourBench with the provided base URL."""
    config_path = Path("example/configs/ollama_modal_test.yaml")
    cfg = yaml.safe_load(config_path.read_text())
    cfg["model_list"][0]["base_url"] = base_url

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as tmp:
        yaml.dump(cfg, tmp)
        tmp_path = Path(tmp.name)

    try:
        subprocess.run(["yourbench", "run", "--config", str(tmp_path)], check=True)
    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    model_name = os.environ.get("OLLAMA_MODEL", "llama3")
    with stub.run():
        handle = ollama_service.spawn(model_name)
        run_pipeline(handle.web_url)
