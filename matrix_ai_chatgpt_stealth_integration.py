#!/usr/bin/env python3
"""
Matrix AI ChatGPT Stealth Integration
ChatGPT Codex ile stealth bağlantı kurma modülü
"""

import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_agent_stealth import BrowserAgentStealth


class MatrixAIChatGPTStealth:
    """ChatGPT Codex ile stealth bağlantı yöneticisi"""
    
    def __init__(self, browser_agent: BrowserAgentStealth = None):
        # Initialize browser agent if not provided
        self.browser_agent = browser_agent or BrowserAgentStealth()
        self.driver = None
        self.is_connected = False
        self.conversation_id = None
        
    def connect_to_chatgpt(self) -> bool:
        """ChatGPT'ye stealth bağlantı kur"""
        try:
            self.driver = self.browser_agent.setup_driver()
            self.driver.get("https://chatgpt.com")
            
            # Sayfa yüklenene kadar bekle
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Login gerekiyorsa yapılacak aksiyonlar
            self._handle_login_if_needed()
            
            # Codex moduna geç
            self._switch_to_codex_mode()
            
            self.is_connected = True
            return True
            
        except Exception as e:
            print(f"ChatGPT bağlantı hatası: {e}")
            return False
            
    def _handle_login_if_needed(self):
        """Gerekirse login işlemini gerçekleştir"""
        try:
            # Login button varsa tıkla
            login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))
            )
            login_btn.click()
            
            # Manuel login için bekle
            print("Manual login gerekebilir. Lütfen tarayıcıda giriş yapın...")
            time.sleep(15)
            
        except Exception as e:
            logging.debug(f"Login button not found or login not needed: {e}")
            
    def _switch_to_codex_mode(self):
        """ChatGPT'yi kod yazma moduna geçir"""
        try:
            # Model seçici dropdown'u bul ve tıkla
            model_selector = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='model-switcher']"))
            )
            model_selector.click()
            
            # GPT-4 Codex'i seç
            codex_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'GPT-4')]"))
            )
            codex_option.click()
            
        except Exception as e:
            logging.debug(f"Model switcher not found, using default model: {e}")
            
    def send_message(self, message: str) -> str:
        """ChatGPT'ye mesaj gönder ve yanıt al"""
        if not self.is_connected:
            return "Hata: ChatGPT'ye bağlı değil"
            
        try:
            # Mesaj input alanını bul
            message_input = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//textarea[@data-id='root']"))
            )
            
            # Mesajı yazalım
            message_input.clear()
            message_input.send_keys(message)
            
            # Gönder butonunu bul ve tıkla
            send_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='send-button']"))
            )
            send_button.click()
            
            # Yanıt bekleme
            time.sleep(2)
            
            # Yanıtı al
            response = self._get_latest_response()
            return response
            
        except Exception as e:
            return f"Mesaj gönderme hatası: {e}"
            
    def _get_latest_response(self) -> str:
        """En son ChatGPT yanıtını al"""
        try:
            # Yanıt alanlarını bekle
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-message-author-role='assistant']"))
            )
            
            # En son assistant mesajını al
            response_elements = self.driver.find_elements(By.XPATH, "//div[@data-message-author-role='assistant']")
            
            if response_elements:
                latest_response = response_elements[-1]
                return latest_response.text
            else:
                return "Yanıt alınamadı"
                
        except Exception as e:
            return f"Yanıt alma hatası: {e}"
            
    def start_new_conversation(self) -> bool:
        """Yeni konuşma başlat"""
        try:
            # Yeni chat butonu
            new_chat_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New chat')]"))
            )
            new_chat_btn.click()
            
            self.conversation_id = None
            return True
            
        except Exception as e:
            print(f"Yeni konuşma başlatma hatası: {e}")
            return False
            
    def close_connection(self):
        """ChatGPT bağlantısını kapat"""
        if self.driver:
            self.driver.quit()
        self.is_connected = False
        self.conversation_id = None