import subprocess
import logging
from typing import List

class GHCopilotCLI:
    """Interface to GitHub Copilot via the `gh` CLI extension."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def ask(self, prompt: str, mode: str = "suggest") -> str:
        """Send a prompt to `gh copilot` and return the response.

        Parameters
        ----------
        prompt : str
            Question or instruction for Copilot.
        mode : str
            Either "suggest" or "explain". Defaults to "suggest".
        """
        cmd: List[str] = ["gh", "copilot", mode, prompt]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except FileNotFoundError:
            self.logger.error("gh CLI not found")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"gh copilot error: {e}")
        return ""

