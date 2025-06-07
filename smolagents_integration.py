from __future__ import annotations
import os
from typing import Optional

try:
    from smolagents import CodeAgent, HfApiModel, Tool
except Exception:  # pragma: no cover - optional dependency
    CodeAgent = None  # type: ignore
    HfApiModel = None  # type: ignore
    Tool = object


class CommitMessageTool(Tool):
    """Simple tool to summarise a git diff."""

    name = "summarize_diff"
    description = "Summarize a git diff into a short commit message"
    inputs = {"diff": {"type": "string", "description": "Git diff text"}}
    output_type = "string"

    def forward(self, diff: str) -> str:  # type: ignore[override]
        added = sum(1 for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
        removed = sum(bool(line.startswith("-") and not line.startswith("---"))
        return f"Add {added} lines and remove {removed} lines"


class SmolAgentsIntegration:
    """Wrapper around `smolagents.CodeAgent` for commit message generation."""

    def __init__(self, hf_token: Optional[str] = None) -> None:
        self.hf_token = hf_token or os.getenv("HF_API_TOKEN")
        self.agent = None
        if CodeAgent and HfApiModel and self.hf_token:
            model = HfApiModel(model_id="google/gemma-2b-it", token=self.hf_token)
            tool = CommitMessageTool()
            self.agent = CodeAgent(tools=[tool], model=model)

    def generate_commit_message(self, diff: str) -> str:
        if self.agent:
            try:
                return str(self.agent.run(f"Summarize this diff for a git commit:\n{diff}"))
            except Exception as e:  # pragma: no cover - runtime failure
                return f"AI summary failed: {e}"
        tool = CommitMessageTool()
        return tool.forward(diff)
