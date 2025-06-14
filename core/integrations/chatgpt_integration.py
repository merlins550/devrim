"""ChatGPT integration wrapper using existing stealth modules."""

from __future__ import annotations

from typing import Optional

from matrix_ai_chatgpt_stealth_integration import MatrixAIChatGPTStealth
from browser_agent_stealth import BrowserAgentStealth


class ChatGPTStealthIntegration:
    """Simplified interface for ChatGPT operations."""

    def __init__(self, browser_agent: Optional[BrowserAgentStealth] = None) -> None:
        self._stealth = MatrixAIChatGPTStealth(browser_agent=browser_agent)
        self._connected = False

    def ensure_connection(self) -> bool:
        """Ensure a connection to ChatGPT is established."""
        if not self._connected:
            self._connected = self._stealth.connect_to_chatgpt()
        return self._connected

    def send(self, message: str) -> str:
        """Send a message to ChatGPT and return the response."""
        if not self.ensure_connection():
            return "❌ ChatGPT bağlantısı kurulamadı"
        return self._stealth.send_message(message)

    def create_project(self, description: str, path: str) -> str:
        prompt = f"Proje: {description}\nHedef klasör: {path}"
        return self.send(prompt)

    def generate_code(self, request: str) -> str:
        prompt = f"Kod isteği: {request}"
        return self.send(prompt)

    def ask_question(self, question: str) -> str:
        return self.send(question)

    def close(self) -> None:
        self._stealth.close_connection()
        self._connected = False
