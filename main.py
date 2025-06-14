"""Entry point launching the minimal Matrix AI desktop assistant."""

from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path
import platform

from core.gui.main_window import MatrixAIMainWindow


def show_splash_screen(app: QApplication) -> None:
    """Display a simple splash screen while loading."""
    splash_path = Path("resources/splash.png")
    if not splash_path.exists():
        return
    pixmap = QPixmap(str(splash_path))
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    # brief pause to allow underlying systems to spin up
    import time
    time.sleep(2)
    splash.close()


def create_desktop_shortcut() -> None:
    """Create a simple desktop shortcut for the assistant."""
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        return
    script_path = Path(__file__).resolve()
    if platform.system() == "Windows":
        shortcut = desktop / "Matrix_AI_Assistant.bat"
        shortcut.write_text(f"@echo off\npython \"{script_path}\"\npause\n", encoding="utf-8")


def main() -> int:
    app = QApplication(sys.argv)
    show_splash_screen(app)
    window = MatrixAIMainWindow()
    window.show()
    create_desktop_shortcut()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
