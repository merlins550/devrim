import subprocess
from pathlib import Path
import uuid
import logging
import os

class CopilotBridge:
    """Minimal interface to trigger GitHub Copilot via VS Code."""

    def __init__(self, workspace: str | Path, vscode_path: str | Path | None = None):
        self.workspace = Path(workspace)
        self.logger = logging.getLogger(__name__)
        self.vscode_path = Path(vscode_path) if vscode_path else None

        if self.vscode_path is None:
            env_path = os.getenv("VSCODE_PATH")
            if env_path:
                self.vscode_path = Path(env_path)
            else:
                try:
                    from matrix_ai_desktop_assistant import MatrixAIDesktopAssistant
                    self.vscode_path = MatrixAIDesktopAssistant.find_vscode_path(None)
                except Exception as e:
                    self.logger.debug(f"find_vscode_path failed: {e}")
                    self.vscode_path = None

    def ask(self, prompt: str) -> str:
        """Send a prompt to VS Code Copilot and return the response if possible."""
        self.logger.info("Copilot prompt received")
        prompt_file = self.workspace / f"copilot_prompt_{uuid.uuid4().hex}.txt"
        prompt_file.write_text(prompt, encoding="utf-8")

        # In a real implementation, a VS Code extension would read this file and
        # write the response to `<prompt_file>.out`. This is just a placeholder
        # to demonstrate how integration might be triggered without using an API.
        vscode_cmd = str(self.vscode_path) if self.vscode_path else "code"

        try:
            subprocess.run([vscode_cmd, str(prompt_file)], check=True)
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

