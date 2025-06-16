import os
from pathlib import Path
from typing import List, Dict

import requests


class CopilotAPI:
    """Minimal wrapper for the GitHub Copilot chat API."""

    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        self.token = token
        self.base_url = base_url.rstrip("/")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send a chat completion request.

        Parameters
        ----------
        messages: List of chat messages following the OpenAI format.

        Returns the assistant response text.
        """
        url = f"{self.base_url}/copilot/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        payload = {"messages": messages, "model": "gpt-4"}
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


def load_project_summary() -> str:
    """Return a short summary of the project for context."""
    parts: List[str] = []
    if Path("metadata.json").exists():
        parts.append(Path("metadata.json").read_text())
    if Path("TODO.md").exists():
        parts.append(Path("TODO.md").read_text())
    bat_files = list(Path('.').glob('*.bat'))
    if bat_files:
        parts.append("\n".join(f.name for f in bat_files))
    return "\n\n".join(parts)


__all__ = ["CopilotAPI", "load_project_summary"]
