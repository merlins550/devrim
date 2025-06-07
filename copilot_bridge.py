import subprocess
from pathlib import Path
import uuid
import logging

class CopilotBridge:
    """Minimal interface to trigger GitHub Copilot via VS Code."""

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace)
        self.logger = logging.getLogger(__name__)

    def ask(self, prompt: str) -> str:
        """Send a prompt to VS Code Copilot and return the response if possible."""
        self.logger.info("Copilot prompt received")
        prompt_file = self.workspace / f"copilot_prompt_{uuid.uuid4().hex}.txt"
        prompt_file.write_text(prompt, encoding="utf-8")

        # In a real implementation, a VS Code extension would read this file and
        # write the response to `<prompt_file>.out`. This is just a placeholder
        # to demonstrate how integration might be triggered without using an API.
        try:
            subprocess.run(["code", str(prompt_file)], check=True)
        except FileNotFoundError:
            self.logger.error("VS Code executable not found in PATH")
            return "VS Code bulunamadı."
        except subprocess.CalledProcessError as e:
            self.logger.error(f"VS Code çalıştırma hatası: {e}")
            return "Copilot bağlantı hatası"

        response_file = prompt_file.with_suffix(".out")
        if response_file.exists():
            return response_file.read_text(encoding="utf-8")
        return "Copilot yanıtı elde edilemedi."

