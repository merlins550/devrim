"""Lightweight GitHub agent using subprocess."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


class GitHubAgent:
    """Simple Git helper for basic operations."""

    def __init__(self, repo_path: Optional[str] = None) -> None:
        self.repo_path = Path(repo_path).resolve() if repo_path else None

    def set_repo(self, path: str) -> None:
        self.repo_path = Path(path).resolve()

    def _run(self, args: list[str]) -> str:
        if not self.repo_path:
            return "❌ Önce bir proje klasörü seçin"
        try:
            result = subprocess.run(args, cwd=self.repo_path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            return exc.stderr.strip() or str(exc)

    def initialize_repo(self) -> str:
        return self._run(["git", "init"])

    def commit_changes(self, message: str) -> str:
        self._run(["git", "add", "."])
        return self._run(["git", "commit", "-m", message])

    def push_changes(self) -> str:
        return self._run(["git", "push"])

    def pull_changes(self) -> str:
        return self._run(["git", "pull"])
