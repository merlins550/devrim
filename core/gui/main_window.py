"""Qt based minimal UI for Matrix AI."""

from __future__ import annotations

import threading
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QPushButton,
    QStatusBar,
)

from ..integrations.chatgpt_integration import ChatGPTStealthIntegration
from ..agents.github_agent import GitHubAgent


class MatrixAIMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.chatgpt_integration: ChatGPTStealthIntegration | None = None
        self.github_agent: GitHubAgent = GitHubAgent()
        self.current_project: Path | None = None
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("\U0001F916 Matrix AI Desktop Assistant")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_matrix_theme()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.chat_display = QTextEdit(readOnly=True)
        main_layout.addWidget(self.chat_display, 3)

        self.chat_input = QTextEdit()
        self.chat_input.setMaximumHeight(80)
        self.chat_input.setPlaceholderText("Komut girin... (Shift+Enter)")
        self.chat_input.keyPressEvent = self.handle_key_press
        main_layout.addWidget(self.chat_input, 1)

        send_btn = QPushButton("Gönder")
        send_btn.clicked.connect(self.send_message)
        main_layout.addWidget(send_btn)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("\U0001F916 Matrix AI başlatıldı - Komut bekleniyor...")

        self.chat_display.append("\U0001F680 Matrix AI Desktop Assistant başlatıldı")
        self.chat_display.append("\U0001F4AC Projenizi tanımlayın, tüm teknik detayları ben halledeceğim!")

    def setup_matrix_theme(self) -> None:
        """Apply a simple Matrix-style color scheme."""
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'Consolas', monospace;
            }
            QTextEdit {
                background-color: #001a00;
                color: #00ff00;
                border: 1px solid #008000;
                font-size: 14px;
            }
            QPushButton {
                background-color: #003300;
                color: #00ff00;
                border: 1px solid #008000;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005500;
            }
            QStatusBar {
                background-color: #001100;
                color: #00ff00;
            }
            """
        )

    def handle_key_press(self, event) -> None:
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            self.send_message()
        else:
            super().keyPressEvent(event)

    def send_message(self) -> None:
        message = self.chat_input.toPlainText().strip()
        if not message:
            return
        self.chat_display.append(f"👤 {message}")
        self.chat_input.clear()
        self.status_bar.showMessage("İşleniyor...")
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def process_message(self, message: str) -> None:
        try:
            response = self.handle_command(message)
        except Exception as exc:
            response = f"❌ Hata: {exc}"
        QTimer.singleShot(0, lambda: self.display_response(response))

    def display_response(self, response: str) -> None:
        self.chat_display.append(f"🤖 {response}")
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
        self.status_bar.showMessage("Hazır")

    # Command handling
    def handle_command(self, message: str) -> str:
        message_lower = message.lower()
        if "proje" in message_lower:
            return self.handle_project_creation(message)
        if "github" in message_lower or "repo" in message_lower:
            return self.handle_github_operation(message)
        if "kod" in message_lower:
            return self.handle_code_request(message)
        return self.handle_general_query(message)

    def handle_project_creation(self, description: str) -> str:
        if not self.current_project:
            return "❌ Önce bir proje klasörü seçin"
        if not self.chatgpt_integration:
            self.chatgpt_integration = ChatGPTStealthIntegration()
        return self.chatgpt_integration.create_project(description, str(self.current_project))

    def handle_github_operation(self, command: str) -> str:
        if "init" in command:
            return self.github_agent.initialize_repo()
        if "commit" in command:
            msg = command.replace("commit", "").strip() or "auto commit"
            return self.github_agent.commit_changes(msg)
        if "push" in command:
            return self.github_agent.push_changes()
        if "pull" in command:
            return self.github_agent.pull_changes()
        return "Tanımsız GitHub komutu"

    def handle_code_request(self, request: str) -> str:
        if not self.chatgpt_integration:
            self.chatgpt_integration = ChatGPTStealthIntegration()
        return self.chatgpt_integration.generate_code(request)

    def handle_general_query(self, query: str) -> str:
        if not self.chatgpt_integration:
            self.chatgpt_integration = ChatGPTStealthIntegration()
        return self.chatgpt_integration.ask_question(query)
