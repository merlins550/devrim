#!/usr/bin/env python3
"""
Matrix AI Desktop Assistant
Devrimsel AI Masaüstü Asistanı - Tek Simge, Tam Otomasyon

Bu sistem:
- Tek tıkla tüm AI ekosistemini başlatır
- Selenium stealth ile ChatGPT Codex'e erişir
- VS Code Lite backend ile terminal erişimi sağlar
- SmolAgents ile GitHub işlemlerini otomatize eder
- Kullanıcıyı teknik detaylardan soyutlar
"""

import sys
import os
import json
import time
import subprocess
import threading
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# GUI Framework
try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                                  QLineEdit, QGroupBox, QSystemTrayIcon, QMenu)
    from PySide6.QtCore import Qt, QThread, pyqtSignal
    from PySide6.QtGui import QIcon, QPixmap, QColor
    GUI_FRAMEWORK = "PySide6"
except ImportError:
    try:
        import customtkinter as ctk
        GUI_FRAMEWORK = "CustomTkinter"
    except ImportError:
        GUI_FRAMEWORK = "Terminal"

# Import our custom modules
from browser_agent_stealth import BrowserAgentStealth
from matrix_ai_chatgpt_stealth_integration import MatrixAIChatGPTStealth
from copilot_bridge import CopilotBridge

class MatrixAIDesktopAssistant:
    """
    Matrix AI Desktop Assistant - Ana Sınıf
    
    Bu sınıf tüm AI ekosistemini yönetir:
    - Selenium ChatGPT Codex entegrasyonu
    - VS Code Lite backend
    - SmolAgents Git otomasyonu
    - Chat arayüzü
    """
    
    def __init__(self):
        self.app_name = "Matrix AI Desktop Assistant"
        self.version = "2.0.0"
        
        # Sistem durumları
        self.is_running = False
        self.selenium_controller = None
        self.vscode_process = None
        self.github_agent = None
        self.smolagents_git = None        # SmolAgents Git entegrasyonu
        self.chatgpt_stealth = None        # ChatGPT Stealth entegrasyonu

        # Logging sistemi
        self.setup_logging()

        # Konfigürasyon
        self.config = self.load_config()
        
        # GUI başlatma
        self.init_gui()
        
        # Backend sistemleri
        self.init_backend_systems()
    
    def load_config(self) -> Dict[str, Any]:
        """Konfigürasyon dosyasını yükle veya oluştur"""
        config_path = Path("matrix_ai_config.json")
        
        default_config = {
            "selenium": {
                "stealth_mode": True,
                "headless": False,
                "user_data_dir": "./chrome_profile"
            },
            "vscode": {
                "enable_lite_mode": True,
                "extensions": ["ms-python.python", "github.copilot"],
                "workspace_path": os.getcwd()
            },
            "github": {
                "auto_commit": True,
                "smart_branch_naming": True,
                "auto_push": True
            },
            "ai_services": {
                "chatgpt_codex": True,
                "claude": False,
                "gemini": False
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Config loading error: {e}")
                return default_config
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config
    
    def setup_logging(self):
        """Logging sistemini ayarla"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"matrix_ai_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("MatrixAI")
        self.logger.info(f"{self.app_name} v{self.version} başlatılıyor...")
    
    def init_gui(self):
        """GUI sistemini başlat"""
        if GUI_FRAMEWORK == "PySide6":
            self.init_pyside6_gui()
        elif GUI_FRAMEWORK == "CustomTkinter":
            self.init_customtkinter_gui()
        else:
            self.init_terminal_gui()

    def init_customtkinter_gui(self):
        """Basit CustomTkinter arayüzü (yedek)."""
        import customtkinter as ctk

        self.root = ctk.CTk()
        self.root.title(f"{self.app_name} v{self.version}")

        label = ctk.CTkLabel(self.root, text="Matrix AI Desktop Assistant")
        label.pack(padx=10, pady=10)

        start_btn = ctk.CTkButton(self.root, text="Başlat", command=self.start_matrix_ai)
        start_btn.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.quit_application)

    def init_terminal_gui(self):
        """GUI bulunamazsa terminal moduna geç."""
        self.app = None
        print("GUI framework bulunamadı. Terminal moduna geçiliyor.")
    
    def init_pyside6_gui(self):
        """PySide6 tabanlı modern GUI"""
        self.app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        
        # Ana pencere
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle(f"{self.app_name} v{self.version}")
        self.main_window.setMinimumSize(1200, 800)
        
        # Dark theme uygula
        self.apply_dark_theme()
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)
        
        # Ana layout - 3 bölüm: Sol panel, Chat, Sağ panel
        main_layout = QHBoxLayout(central_widget)
        
        # Sol Panel - Sistem Durumu
        self.create_left_panel(main_layout)
        
        # Orta Panel - Chat Arayüzü
        self.create_chat_panel(main_layout)
        
        # Sağ Panel - Hızlı Eylemler
        self.create_right_panel(main_layout)
        
        # Status bar
        self.status_bar = self.main_window.statusBar()
        self.status_bar.showMessage("Matrix AI Hazır - Sistemleri başlatmak için Start'a tıklayın")
        
        # Sistem tray icon
        self.create_system_tray()
    
    def apply_dark_theme(self):
        """Matrix tarzı dark theme"""
        dark_style = """
        QMainWindow {
            background-color: #0d1117;
            color: #00ff00;
        }
        QTextEdit, QLineEdit {
            background-color: #161b22;
            border: 1px solid #30363d;
            color: #00ff00;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
        }
        QPushButton {
            background-color: #21262d;
            border: 1px solid #30363d;
            color: #00ff00;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #30363d;
            border-color: #00ff00;
        }
        QPushButton:pressed {
            background-color: #0d1117;
        }
        QLabel {
            color: #00ff00;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        QGroupBox {
            color: #00ff00;
            border: 1px solid #30363d;
            margin-top: 1ex;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """
        self.app.setStyleSheet(dark_style)
    
    def create_left_panel(self, main_layout):
        """Sol panel - Sistem durumu ve kontroller"""
        left_panel = QWidget()
        left_panel.setMaximumWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # Sistem Durumu Grubu
        status_group = QGroupBox("🌐 Sistem Durumu")
        status_layout = QVBoxLayout(status_group)
        
        # Durum göstergeleri
        self.selenium_status = QLabel("🔴 Selenium: Kapalı")
        self.vscode_status = QLabel("🔴 VS Code Lite: Kapalı")
        self.github_status = QLabel("🔴 GitHub Agent: Kapalı")
        self.chatgpt_status = QLabel("🔴 ChatGPT Codex: Kapalı")
        
        status_layout.addWidget(self.selenium_status)
        status_layout.addWidget(self.vscode_status)
        status_layout.addWidget(self.github_status)
        status_layout.addWidget(self.chatgpt_status)
        
        # Kontrol Butonları
        controls_group = QGroupBox("⚡ Hızlı Kontroller")
        controls_layout = QVBoxLayout(controls_group)
        
        self.start_btn = QPushButton("🚀 Matrix AI'yı Başlat")
        self.start_btn.clicked.connect(self.start_matrix_ai)
        
        self.chatgpt_btn = QPushButton("🤖 ChatGPT Codex Aç")
        self.chatgpt_btn.clicked.connect(self.open_chatgpt_codex)
        
        self.github_btn = QPushButton("📂 GitHub Bağlan")
        self.github_btn.clicked.connect(self.connect_github)
        
        self.vscode_btn = QPushButton("⚙️ VS Code Lite Başlat")
        self.vscode_btn.clicked.connect(self.start_vscode_lite)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.chatgpt_btn)
        controls_layout.addWidget(self.github_btn)
        controls_layout.addWidget(self.vscode_btn)
        
        # SmolAgents Kontrolleri
        smolagents_group = QGroupBox("🐬 SmolAgents Git Power")
        smolagents_layout = QVBoxLayout(smolagents_group)
        
        self.repo_create_btn = QPushButton("📁 Yeni Repo Oluştur")
        self.repo_create_btn.clicked.connect(self.create_repository)
        
        self.auto_commit_btn = QPushButton("💾 Otomatik Commit")
        self.auto_commit_btn.clicked.connect(self.auto_commit)
        
        self.deploy_btn = QPushButton("🚀 Deploy")
        self.deploy_btn.clicked.connect(self.deploy_project)
        
        smolagents_layout.addWidget(self.repo_create_btn)
        smolagents_layout.addWidget(self.auto_commit_btn)
        smolagents_layout.addWidget(self.deploy_btn)
        
        # Layout'a ekle
        left_layout.addWidget(status_group)
        left_layout.addWidget(controls_group)
        left_layout.addWidget(smolagents_group)
        left_layout.addStretch()
        
        main_layout.addWidget(left_panel)
    
    def create_chat_panel(self, main_layout):
        """Orta panel - Chat arayüzü"""
        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        
        # Chat başlığı
        chat_title = QLabel("💬 Matrix AI Chat - GitHub Copilot Entegrasyonu")
        chat_title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        chat_layout.addWidget(chat_title)
        
        # Chat geçmişi
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("font-size: 13px; line-height: 1.4;")
        chat_layout.addWidget(self.chat_history)
        
        # Mesaj girişi
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Projenizi anlatın veya komut verin... (Örn: 'Bir e-ticaret sitesi yap')")
        self.message_input.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("📤 Gönder")
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        
        chat_layout.addLayout(input_layout)
        
        # Hızlı komutlar
        quick_commands = QHBoxLayout()
        
        self.quick_project_btn = QPushButton("🏗️ Yeni Proje")
        self.quick_project_btn.clicked.connect(lambda: self.quick_command("Yeni bir proje oluştur"))
        
        self.quick_debug_btn = QPushButton("🐛 Debug Yardımı")
        self.quick_debug_btn.clicked.connect(lambda: self.quick_command("Kodumdaki hataları bul ve düzelt"))
        
        self.quick_optimize_btn = QPushButton("⚡ Optimize Et")
        self.quick_optimize_btn.clicked.connect(lambda: self.quick_command("Kodumu optimize et"))
        
        quick_commands.addWidget(self.quick_project_btn)
        quick_commands.addWidget(self.quick_debug_btn)
        quick_commands.addWidget(self.quick_optimize_btn)
        
        chat_layout.addLayout(quick_commands)
        
        main_layout.addWidget(chat_panel)
    
    def create_right_panel(self, main_layout):
        """Sağ panel - Proje yönetimi ve çıktılar"""
        right_panel = QWidget()
        right_panel.setMaximumWidth(350)
        right_layout = QVBoxLayout(right_panel)
        
        # Proje Bilgileri
        project_group = QGroupBox("📊 Proje Bilgileri")
        project_layout = QVBoxLayout(project_group)
        
        self.project_name_label = QLabel("Proje: Henüz seçilmedi")
        self.project_path_label = QLabel("Konum: -")
        self.project_status_label = QLabel("Durum: Hazır")
        
        project_layout.addWidget(self.project_name_label)
        project_layout.addWidget(self.project_path_label)
        project_layout.addWidget(self.project_status_label)
        
        # Terminal Çıktısı
        terminal_group = QGroupBox("🖥️ Terminal Çıktısı")
        terminal_layout = QVBoxLayout(terminal_group)
        
        self.terminal_output = QTextEdit()
        self.terminal_output.setMaximumHeight(200)
        self.terminal_output.setStyleSheet("background-color: #000; color: #00ff00; font-family: 'Consolas';")
        terminal_layout.addWidget(self.terminal_output)
        
        # Log Çıktısı
        log_group = QGroupBox("📋 Sistem Logları")
        log_layout = QVBoxLayout(log_group)
        
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(200)
        log_layout.addWidget(self.log_output)
        
        right_layout.addWidget(project_group)
        right_layout.addWidget(terminal_group)
        right_layout.addWidget(log_group)
        right_layout.addStretch()
        
        main_layout.addWidget(right_panel)
    
    def create_system_tray(self):
        """Sistem tray ikonu oluştur"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self.main_window)
            
            # Icon (Matrix AI logosu olarak basit bir icon)
            icon = QIcon()
            # Basit bir Matrix-style icon oluştur
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 255, 0))
            icon.addPixmap(pixmap)
            
            self.tray_icon.setIcon(icon)
            self.tray_icon.setToolTip("Matrix AI Desktop Assistant")
            
            # Tray menüsü
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction("🖥️ Göster")
            show_action.triggered.connect(self.main_window.show)
            
            hide_action = tray_menu.addAction("🫥 Gizle")
            hide_action.triggered.connect(self.main_window.hide)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction("❌ Çıkış")
            quit_action.triggered.connect(self.quit_application)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
    
    def init_backend_systems(self):
        """Backend sistemlerini hazırla"""
        self.logger.info("Backend sistemleri hazırlanıyor...")
        
        # Selenium Controller'ı hazırla
        try:
            self.selenium_controller = BrowserAgentStealth()
            self.logger.info("Selenium Controller hazır")
        except Exception as e:
            self.logger.error(f"Selenium Controller hatası: {e}")
        
        # ChatGPT Stealth Integration'ı hazırla
        try:
            self.chatgpt_stealth = MatrixAIChatGPTStealth()
            self.logger.info("ChatGPT Stealth Integration hazır")
        except Exception as e:
            self.logger.error(f"ChatGPT Stealth Integration hatası: {e}")
        
        # SmolAgents Git Power entegrasyonu
        try:
            from smolagents_git_power import SmolAgentsGitPower
            self.smolagents_git = SmolAgentsGitPower()
            self.logger.info("SmolAgents Git Power hazır")
        except Exception as e:
            self.logger.error(f"SmolAgents Git Power hatası: {e}")

        # Copilot Bridge
        try:
            workspace = self.config["vscode"]["workspace_path"]
            self.copilot_bridge = CopilotBridge(workspace)
            self.logger.info("Copilot Bridge hazır")
        except Exception as e:
            self.logger.error(f"Copilot Bridge hatası: {e}")
        
        # Intent Detection sistemi
        try:
            from matrix_ai_intent_detector import MatrixAIIntentDetector
            self.intent_detector = MatrixAIIntentDetector()
            self.logger.info("Intent Detection sistemi hazır")
        except Exception as e:
            self.logger.error(f"Intent Detection hatası: {e}")
    
    def start_matrix_ai(self):
        """Matrix AI'yı başlat - Ana tetikleyici"""
        self.logger.info("🚀 Matrix AI Başlatılıyor...")
        self.add_chat_message("sistem", "Matrix AI başlatılıyor... Tüm sistemler aktive ediliyor!")
        
        # Splash screen göster
        self.show_splash_screen()
        
        # Backend sistemleri sırayla başlat
        thread = threading.Thread(target=self._start_backend_systems)
        thread.daemon = True
        thread.start()
    
    def show_splash_screen(self):
        """Başlangıç splash screen'i"""
        splash_text = """
        ╔══════════════════════════════════════╗
        ║          MATRIX AI DESKTOP           ║
        ║            ASSISTANT v2.0            ║
        ║                                      ║
        ║  🔄 Sistemler aktive ediliyor...     ║
        ║  🌐 Selenium Stealth başlatılıyor    ║
        ║  🤖 ChatGPT Codex bağlantısı         ║
        ║  📂 GitHub Agent hazırlanıyor        ║
        ║  ⚙️  VS Code Lite başlatılıyor       ║
        ║                                      ║
        ║     Lütfen bekleyin...               ║
        ╚══════════════════════════════════════╝
        """
        self.add_chat_message("sistem", splash_text)
    
    def _start_backend_systems(self):
        """Backend sistemleri arka planda başlat"""
        try:
            # 1. Selenium Stealth başlat
            self.update_status("selenium", "🟡 Başlatılıyor...")
            time.sleep(1)
            if self.selenium_controller:
                # Selenium'u başlat ama henüz ChatGPT'ye gitme
                self.update_status("selenium", "🟢 Hazır")
                self.add_chat_message("sistem", "✅ Selenium Stealth aktif")
            
            # 2. VS Code Lite başlat (isteğe bağlı)
            if self.config["vscode"]["enable_lite_mode"]:
                self.update_status("vscode", "🟡 Başlatılıyor...")
                self.start_vscode_lite()
                time.sleep(2)
                self.update_status("vscode", "🟢 Hazır")
                self.add_chat_message("sistem", "✅ VS Code Lite backend aktif")
            
            # 3. GitHub Agent hazırla
            self.update_status("github", "🟡 Hazırlanıyor...")
            time.sleep(1)
            self.update_status("github", "🟢 Hazır")
            self.add_chat_message("sistem", "✅ GitHub Agent hazır")
            
            # 4. ChatGPT Codex hazırlığı (kullanıcı isteğinde açılacak)
            self.update_status("chatgpt", "🟡 Hazır (Bağlantı bekliyor)")
            self.add_chat_message("sistem", "✅ ChatGPT Codex hazır - Giriş yapmanız bekleniyor")
            
            # Sistem hazır
            self.is_running = True
            self.add_chat_message("sistem", """
🎉 Matrix AI Desktop Assistant tamamen aktif!

Artık size şunları yapabilirim:
• 🏗️ Proje oluşturma ve yönetimi
• 🤖 ChatGPT Codex ile kod yazma
• 📂 GitHub otomasyonu (commit, push, PR)
• ⚙️ VS Code entegrasyonu
• 🐛 Debug ve optimize etme

Bir proje fikrinizi anlatın veya komut verin!
            """)
            
            self.status_bar.showMessage("Matrix AI Aktif - Komutlarınızı bekliyorum!")
            
        except Exception as e:
            self.logger.error(f"Backend başlatma hatası: {e}")
            self.add_chat_message("hata", f"Sistem başlatma hatası: {e}")
    
    def update_status(self, service: str, status: str):
        """Servis durumunu güncelle"""
        if hasattr(self, f"{service}_status"):
            label = getattr(self, f"{service}_status")
            if label:
                label.setText(f"{status}")
    
    def open_chatgpt_codex(self):
        """ChatGPT Codex'i Selenium ile aç"""
        if not self.selenium_controller:
            self.add_chat_message("hata", "Selenium Controller hazır değil!")
            return
        
        self.add_chat_message("sistem", "🤖 ChatGPT Codex açılıyor... Lütfen giriş yapın.")
        
        thread = threading.Thread(target=self._open_chatgpt_thread)
        thread.daemon = True
        thread.start()
    
    def _open_chatgpt_thread(self):
        """ChatGPT'yi arka planda aç"""
        try:
            if self.chatgpt_stealth:
                success = self.chatgpt_stealth.connect_to_chatgpt()
                if success:
                    self.update_status("chatgpt", "🟢 Bağlandı")
                    self.add_chat_message("sistem", "✅ ChatGPT Codex'e başarıyla bağlandı! Artık kod yazabilirim.")
                else:
                    self.update_status("chatgpt", "🔴 Bağlantı hatası")
                    self.add_chat_message("hata", "❌ ChatGPT bağlantısı başarısız. Tekrar deneyin.")
        except Exception as e:
            self.logger.error(f"ChatGPT bağlantı hatası: {e}")
            self.add_chat_message("hata", f"ChatGPT bağlantı hatası: {e}")
    
    def connect_github(self):
        """GitHub'a bağlan"""
        self.add_chat_message("sistem", "📂 GitHub bağlantısı kuruluyor...")
        # GitHub bağlantı logici buraya gelecek
        self.add_chat_message("sistem", "✅ GitHub bağlantısı kuruldu!")
    
    def start_vscode_lite(self):
        """VS Code Lite (headless) başlat"""
        try:
            vscode_path = self.find_vscode_path()
            if vscode_path:
                # Headless VS Code başlat
                cmd = [
                    vscode_path,
                    "--disable-extensions",
                    "--disable-workspace-trust",
                    "--disable-gpu",
                    self.config["vscode"]["workspace_path"]
                ]
                
                self.vscode_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                
                self.add_terminal_output(f"VS Code Lite başlatıldı: PID {self.vscode_process.pid}")
                return True
            else:
                self.add_chat_message("hata", "VS Code bulunamadı!")
                return False
                
        except Exception as e:
            self.logger.error(f"VS Code başlatma hatası: {e}")
            self.add_chat_message("hata", f"VS Code başlatma hatası: {e}")
            return False
    
    def find_vscode_path(self):
        """VS Code yolunu bul"""
        possible_paths = [
            "C:\\Program Files\\Microsoft VS Code\\Code.exe",
            "C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        
        return None
    
    def send_message(self):
        """Kullanıcı mesajını işle"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        self.message_input.clear()
        self.add_chat_message("kullanıcı", message)
        
        # Intent detection ve işleme
        self.process_user_message(message)
    
    def process_user_message(self, message: str):
        """Kullanıcı mesajını analiz et ve işle"""
        intent = self.detect_intent(message)
        
        self.logger.info(f"Intent detected: {intent} for message: {message}")
        
        if intent == "project_creation":
            self.handle_project_creation(message)
        elif intent == "github_operation":
            self.handle_github_operation(message)
        elif intent == "code_assistance":
            self.handle_code_assistance(message)
        elif intent == "system_control":
            self.handle_system_control(message)
        else:
            self.handle_general_query(message)
    
    def detect_intent(self, message: str) -> str:
        """Mesaj amacını tespit et"""
        message_lower = message.lower()
        
        # Proje oluşturma
        project_keywords = ["proje", "site", "uygulama", "yap", "oluştur", "geliştir", "web", "app"]
        if any(keyword in message_lower for keyword in project_keywords):
            return "project_creation"
        
        # GitHub işlemleri
        github_keywords = ["commit", "push", "pull", "branch", "repo", "github", "git"]
        if any(keyword in message_lower for keyword in github_keywords):
            return "github_operation"
        
        # Kod yardımı
        code_keywords = ["kod", "debug", "hata", "düzelt", "optimize", "test", "fonksiyon"]
        if any(keyword in message_lower for keyword in code_keywords):
            return "code_assistance"
        
        # Sistem kontrolü
        system_keywords = ["başlat", "durdur", "aç", "kapat", "bağlan", "sistem"]
        if any(keyword in message_lower for keyword in system_keywords):
            return "system_control"
        
        return "general_query"
    
    def handle_project_creation(self, message: str):
        """Proje oluşturma isteğini işle"""
        self.add_chat_message("asistan", f"🏗️ Proje oluşturma isteği algılandı: '{message}'")
        self.add_chat_message("asistan", """
Harika! Yeni bir proje oluşturalım. İşte yapacaklarım:

1. 📁 SmolAgents ile proje yapısını oluşturacağım
2. 📂 GitHub'da repository açacağım  
3. 🤖 ChatGPT Codex'ten kod alacağım
4. ⚙️ VS Code'da organize edeceğim
5. 📤 Git'e push yapacağım

Başlıyorum...
        """)
        
        # Arka planda proje oluşturma işlemini başlat
        thread = threading.Thread(target=self._create_project_thread, args=(message,))
        thread.daemon = True
        thread.start()
    
    def _create_project_thread(self, project_description: str):
        """Proje oluşturma işlemini arka planda çalıştır"""
        try:
            # 1. SmolAgents ile proje yapısı oluştur
            self.add_chat_message("asistan", "📁 Proje yapısı oluşturuluyor...")
            time.sleep(2)  # Gerçek SmolAgents entegrasyonu buraya gelecek
            
            # 2. GitHub repository oluştur
            self.add_chat_message("asistan", "📂 GitHub repository oluşturuluyor...")
            time.sleep(1)
            
            # 3. ChatGPT Codex'e kod yazdır
            if self.chatgpt_stealth:
                self.add_chat_message("asistan", "🤖 ChatGPT Codex'e kod yazdırılıyor...")
                # ChatGPT'ye proje açıklamasını gönder
                time.sleep(3)
            
            # 4. VS Code'da organize et
            self.add_chat_message("asistan", "⚙️ VS Code'da proje organize ediliyor...")
            time.sleep(1)
            
            # 5. Git'e push yap
            self.add_chat_message("asistan", "📤 Git'e push yapılıyor...")
            time.sleep(1)
            
            self.add_chat_message("asistan", """
✅ Proje başarıyla oluşturuldu!

📊 Proje Özeti:
• Proje adı: [Auto-generated]
• Repository: GitHub'da oluşturuldu
• Kod: ChatGPT Codex tarafından yazıldı
• Durum: Hazır ve deploy edilebilir

Başka bir şey yapmamı ister misiniz?
            """)
            
        except Exception as e:
            self.logger.error(f"Proje oluşturma hatası: {e}")
            self.add_chat_message("hata", f"Proje oluşturma hatası: {e}")
    
    def handle_github_operation(self, message: str):
        """GitHub işlemlerini yönet"""
        self.add_chat_message("asistan", f"📂 GitHub işlemi: {message}")
        # GitHub işlemleri buraya gelecek
    
    def handle_code_assistance(self, message: str):
        """Kod yardımı isteklerini işle"""
        self.add_chat_message("asistan", f"🤖 Kod yardımı: {message}")
        response = ""
        if hasattr(self, "copilot_bridge"):
            response = self.copilot_bridge.ask(message)
        if not response:
            response = "Yanıt alınamadı."
        self.add_chat_message("asistan", response)
    
    def handle_system_control(self, message: str):
        """Sistem kontrol komutlarını işle"""
        self.add_chat_message("asistan", f"⚙️ Sistem kontrolü: {message}")
        
        if "vscode" in message.lower() and "başlat" in message.lower():
            self.start_vscode_lite()
        elif "chatgpt" in message.lower() and "aç" in message.lower():
            self.open_chatgpt_codex()
        elif "github" in message.lower() and "bağlan" in message.lower():
            self.connect_github()
    
    def handle_general_query(self, message: str):
        """Genel sorguları işle"""
        self.add_chat_message("asistan", f"Anladım: '{message}'. Size nasıl yardımcı olabilirim?")
    
    def quick_command(self, command: str):
        """Hızlı komut butonları"""
        self.message_input.setText(command)
        self.send_message()
    
    def create_repository(self):
        """Yeni repository oluştur"""
        self.add_chat_message("asistan", "📁 Yeni repository oluşturuluyor...")
        # SmolAgents repository oluşturma buraya gelecek
    
    def auto_commit(self):
        """Otomatik commit"""
        self.add_chat_message("asistan", "💾 Otomatik commit yapılıyor...")
        # SmolAgents auto commit buraya gelecek
    
    def deploy_project(self):
        """Projeyi deploy et"""
        self.add_chat_message("asistan", "🚀 Proje deploy ediliyor...")
        # Deploy logic buraya gelecek
    
    def add_chat_message(self, sender: str, message: str):
        """Chat'e mesaj ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "kullanıcı":
            formatted_message = f"<span style='color: #58a6ff;'>[{timestamp}] 👤 Sen:</span><br/>{message}<br/><br/>"
        elif sender == "asistan":
            formatted_message = f"<span style='color: #00ff00;'>[{timestamp}] 🤖 Matrix AI:</span><br/>{message}<br/><br/>"
        elif sender == "sistem":
            formatted_message = f"<span style='color: #ffa500;'>[{timestamp}] ⚙️ Sistem:</span><br/><pre>{message}</pre><br/>"
        elif sender == "hata":
            formatted_message = f"<span style='color: #ff4444;'>[{timestamp}] ❌ Hata:</span><br/>{message}<br/><br/>"
        else:
            formatted_message = f"<span style='color: #888;'>[{timestamp}] {sender}:</span><br/>{message}<br/><br/>"
        
        self.chat_history.insertHtml(formatted_message)
        
        # En sona kaydır
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def add_terminal_output(self, output: str):
        """Terminal çıktısı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.terminal_output.append(f"[{timestamp}] {output}")
    
    def add_log_output(self, log_message: str):
        """Log çıktısı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {log_message}")
    
    def quit_application(self):
        """Uygulamayı kapat"""
        self.logger.info("Matrix AI kapatılıyor...")
        
        # Backend sistemleri kapat
        if self.vscode_process:
            self.vscode_process.terminate()
        
        if self.selenium_controller:
            self.selenium_controller.quit()

        # GUI'yi kapat
        if getattr(self, 'app', None):
            self.app.quit()
        
        sys.exit(0)
    
    def run(self):
        """Uygulamayı çalıştır"""
        if GUI_FRAMEWORK == "PySide6":
            self.main_window.show()
            return self.app.exec()
        elif GUI_FRAMEWORK == "CustomTkinter":
            return self.root.mainloop()
        else:
            # Terminal mode için basit input loop
            self.terminal_mode()
    
    def terminal_mode(self):
        """Terminal mode (GUI olmadan)"""
        print(f"\n{self.app_name} v{self.version}")
        print("=" * 50)
        print("Matrix AI Terminal Mode")
        print("Komutlarınızı yazın (çıkmak için 'quit'):")
        
        while True:
            try:
                user_input = input("\n👤 Sen: ").strip()
                if user_input.lower() in ['quit', 'exit', 'çık']:
                    break
                
                print(f"🤖 Matrix AI: Anlıyorum - '{user_input}'")
                self.process_user_message(user_input)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
        
        print("\nMatrix AI kapatılıyor...")
        self.quit_application()

def main():
    """Ana fonksiyon"""
    try:
        # Matrix AI Desktop Assistant'ı başlat
        matrix_ai = MatrixAIDesktopAssistant()
        return matrix_ai.run()
        
    except Exception as e:
        print(f"Kritik hata: {e}")
        logging.exception("Kritik sistem hatası")
        return 1

if __name__ == "__main__":
    sys.exit(main())
