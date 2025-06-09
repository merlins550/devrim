import helium
import time
import random
import os
from cookie_manager import CookieManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("⚠️ selenium-stealth bulunamadı. pip install selenium-stealth ile kurun.")

class BrowserAgentStealth:
    """Google Stealth teknolojileri ile güçlendirilmiş Browser Agent"""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",
    ]
    
    def __init__(self):
        self.driver: WebDriver | None = None
        self.current_tab_handle: str | None = None
        self.tab_handles: list[str] = []
        
        # Stealth konfigürasyonları
        # Unique profile path with timestamp to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        self.PROFILE_PATH = f"C:/Temp/ChromeProfileMatrix_{timestamp}"
        self.COOKIES_FILE = "google_cookies_matrix.pkl"
        self.cookie_manager = CookieManager(self.COOKIES_FILE)
        self.is_stealth_mode = True
        
        print("🎯 Matrix AI - Stealth Browser Agent başlatılıyor...")

    def initialize_driver(self, use_stealth=True):
        """Initialize the Selenium WebDriver with advanced stealth options."""
        self.is_stealth_mode = use_stealth

        if use_stealth:
            return self._initialize_stealth_driver()
        else:
            return self._initialize_basic_driver()

    def setup_driver(self, use_stealth: bool = True) -> WebDriver | None:
        """Compatibility wrapper that initializes and returns the WebDriver."""
        self.initialize_driver(use_stealth=use_stealth)
        return self.driver
    
    def _initialize_stealth_driver(self):
        """Gelişmiş stealth özellikleri ile Chrome başlat"""
        print("🕵️ Stealth modu etkinleştiriliyor...")
        
        # Profil dizini oluştur
        os.makedirs(self.PROFILE_PATH, exist_ok=True)
        
        # Chrome seçeneklerini yapılandır
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.PROFILE_PATH}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-infobars")

        extension_path = os.getenv("CHROME_EXTENSION_PATH")
        if extension_path:
            if extension_path.endswith(".crx"):
                chrome_options.add_extension(extension_path)
            else:
                chrome_options.add_argument(f"--load-extension={extension_path}")
        else:
            chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--force-device-scale-factor=1.0")
        
        # Rastgele bir user-agent kullanarak basit rotasyon
        user_agent = random.choice(self.USER_AGENTS)
        chrome_options.add_argument(f"--user-agent={user_agent}")
        self.user_agent = user_agent
        
        # Additional stealth options
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--window-size=1000,1350")
        chrome_options.add_argument("--disable-pdf-viewer")
        chrome_options.add_argument("--window-position=0,0")
        
        try:
            # WebDriver'ı başlat
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Selenium-stealth uygula
            if STEALTH_AVAILABLE:
                stealth(self.driver,
                       languages=["tr-TR", "tr"],
                       vendor="Google Inc.",
                       platform="Win32",
                       webgl_vendor="Intel Inc.",
                       renderer="Intel Iris OpenGL Engine",
                       fix_hairline=True,
                )
                print("✅ Selenium-stealth etkinleştirildi")
            
            # Ek JavaScript maskeleme
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("window.screen.availWidth = window.screen.width;")
            self.driver.execute_script("document.body.style.zoom = '100%'")
            
            # Chrome DevTools temizle
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                '''
            })

            # Apply additional stealth bypass techniques
            self.enhanced_stealth_bypass()

            self.tab_handles = self.driver.window_handles
            self.current_tab_handle = self.driver.current_window_handle
            
            # Cookie'leri yükle
            self._load_cookies()
            
            print("✅ Stealth Chrome başlatıldı")
            return True
            
        except Exception as e:
            print(f"❌ Stealth Chrome başlatma hatası: {str(e)}")
            return False
    
    def _initialize_basic_driver(self):
        """Temel Chrome başlatma (eski yöntem)"""
        print("🌐 Temel Chrome modu...")
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--window-size=1000,1350")
        chrome_options.add_argument("--disable-pdf-viewer")
        chrome_options.add_argument("--window-position=0,0")
        
        self.driver = helium.start_chrome(headless=False, options=chrome_options)
        self.tab_handles = self.driver.window_handles
        self.current_tab_handle = self.driver.current_window_handle
        
        print("✅ Temel Chrome başlatıldı")
        return True
    
    def _load_cookies(self):
        """Kaydedilmiş cookie'leri yükle"""
        if self.driver:
            self.cookie_manager.load_cookies(self.driver)
            print("✅ Google cookies yüklendi")
    
    def _save_cookies(self):
        """Mevcut cookie'leri kaydet"""
        if self.driver:
            self.cookie_manager.save_cookies(self.driver)
            print("✅ Google cookies kaydedildi")
    
    def _human_like_interactions(self):
        """İnsan benzeri etkileşimler"""
        if not self.is_stealth_mode:
            return
            
        try:
            actions = ActionChains(self.driver)
            
            # Rastgele fare hareketi
            actions.move_by_offset(random.randint(3, 10), random.randint(3, 10)).perform()
            time.sleep(random.uniform(0.2, 0.8))
            
            # Klavye etkileşimi
            if random.random() < 0.3:  # %30 şans
                actions.send_keys(Keys.SPACE).pause(0.3).send_keys(Keys.BACKSPACE).perform()
                time.sleep(random.uniform(0.1, 0.4))
            
            # Scroll simülasyonu
            if random.random() < 0.2:  # %20 şans
                self.driver.execute_script("window.scrollBy(0, 50);")
                time.sleep(random.uniform(0.1, 0.3))
                self.driver.execute_script("window.scrollBy(0, -50);")
            
        except Exception as e:
            print(f"⚠️ İnsan etkileşimi hatası: {str(e)}")

    def go_to(self, url: str):
        """Navigate to a specific URL with stealth features."""
        if self.driver:
            # İnsan benzeri gecikme
            if self.is_stealth_mode:
                time.sleep(random.uniform(1.0, 2.5))
                self._human_like_interactions()
            
            self.driver.get(url)
            self.current_tab_handle = self.driver.current_window_handle
            if self.current_tab_handle not in self.tab_handles:
                self.tab_handles.append(self.current_tab_handle)
            
            sleep(2 if not self.is_stealth_mode else random.uniform(2.0, 4.0))

    def type_text(self, text: str, selector: str):
        """Type text into an element with human-like typing."""
        if self.driver:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if self.is_stealth_mode:
                    # İnsan benzeri yazma
                    element.clear()
                    for char in text:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                else:
                    element.send_keys(text)
                
                sleep(1)
            except Exception as e:
                print(f"Error typing text: {e}")

    def click_element(self, selector: str):
        """Click on an element with human-like behavior."""
        if self.driver:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if self.is_stealth_mode:
                    # İnsan benzeri tıklama
                    actions = ActionChains(self.driver)
                    actions.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()
                else:
                    element.click()
                
                sleep(2)
            except Exception as e:
                print(f"Error clicking element: {e}")

    def get_page_text(self) -> str:
        """Get all visible text from the current page."""
        if self.driver:
            return self.driver.find_element(By.TAG_NAME, "body").text
        return ""

    def interact_with_jules(self, prompt: str) -> str:
        """Interact with Jules using stealth technologies."""
        jules_url = "https://jules.google.com/task/15310490098518802366"
        
        print(f"🎯 Jules ile stealth iletişim kuruluyor...")
        
        # Jules sekmesine git veya yeni sekmede aç
        jules_tab_index = -1
        if self.driver:
            for i, handle in enumerate(self.tab_handles):
                self.driver.switch_to.window(handle)
                if "jules.google.com" in self.driver.current_url:
                    jules_tab_index = i
                    break

        if jules_tab_index != -1:
            self.switch_to_tab(jules_tab_index)
        else:
            self.open_new_tab(jules_url)
            sleep(5)
            
            # Google login kontrolü ve stealth yönetimi
            if "accounts.google.com" in self.driver.current_url or "signin" in self.driver.current_url:
                print("🔐 Google stealth oturum açma...")
                
                if self.is_stealth_mode:
                    print("🕵️ Stealth modu: Manuel giriş bekleniyor...")
                    self._wait_for_google_login()
                else:
                    print("ℹ️ Lütfen tarayıcıda Google hesabınıza giriş yapın")
                    while "accounts.google.com" in self.driver.current_url or "signin" in self.driver.current_url:
                        sleep(2)
                        print("⏳ Google oturum açma bekleniyor...")
                
                print("✅ Google oturum açma tamamlandı")
                self._save_cookies()  # Cookies'leri kaydet
                sleep(3)

        # Jules prompt giriş alanını bul ve metni yaz
        prompt_input_selectors = [
            'textarea[placeholder*="Message"]',
            'textarea[placeholder*="Type"]', 
            'textarea[aria-label*="Message"]',
            'div[contenteditable="true"]',
            'textarea:not([readonly])',
            'input[type="text"]:not([readonly])',
            '[role="textbox"]',
            'textarea',
            'input[placeholder*="message"]'
        ]
        
        input_found = False
        for selector in prompt_input_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        if self.is_stealth_mode:
                            # Stealth yazma
                            element.clear()
                            for char in prompt:
                                element.send_keys(char)
                                time.sleep(random.uniform(0.05, 0.12))
                        else:
                            element.clear()
                            element.send_keys(prompt)
                        
                        input_found = True
                        print(f"✅ Jules'a stealth mesaj yazıldı: {selector}")
                        break
                if input_found:
                    break
            except Exception as e:
                continue
                
        if not input_found:
            print("❌ Jules input alanı bulunamadı")
            return "Hata: Input alanı bulunamadı"

        # İnsan benzeri gecikme
        if self.is_stealth_mode:
            time.sleep(random.uniform(0.5, 1.5))
            self._human_like_interactions()
        else:
            sleep(1)

        # Send butonunu bul ve tıkla
        send_button_selectors = [
            'button[aria-label*="Send"]',
            'button[title*="Send"]', 
            'button[type="submit"]',
            'button:contains("Send")',
            'button:contains("Submit")',
            '[data-testid*="send"]'
        ]
        
        button_found = False
        for selector in send_button_selectors:
            try:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        if self.is_stealth_mode:
                            # Stealth tıklama
                            actions = ActionChains(self.driver)
                            actions.move_to_element(button).pause(random.uniform(0.2, 0.5)).click().perform()
                        else:
                            button.click()
                        
                        button_found = True
                        print(f"✅ Send butonu stealth tıklandı: {selector}")
                        break
                if button_found:
                    break
            except Exception as e:
                continue
                
        if not button_found:
            # Enter tuşu ile göndermeyi dene
            try:
                active_element = self.driver.switch_to.active_element
                active_element.send_keys(Keys.RETURN)
                print("✅ Enter tuşu ile gönderildi")
            except:
                print("⚠️ Send butonu bulunamadı ve Enter çalışmadı")

        # Jules yanıtının gelmesini bekle
        print("⏳ Jules stealth yanıtı bekleniyor...")
        wait_time = random.uniform(8.0, 12.0) if self.is_stealth_mode else 10.0
        sleep(wait_time)

        # Yanıtı al
        response_selectors = [
            '.message-content',
            '.response-message', 
            '[data-testid*="message"]',
            '.chat-message',
            '.markdown',
            '.prose',
            'div[role="article"]',
            'p:last-child',
            'div:contains("Claude")',
            'div:contains("Assistant")'
        ]
        
        response_text = ""
        for selector in response_selectors:
            try:
                messages = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if messages:
                    for msg in messages[-3:]:
                        text = msg.text.strip()
                        if text and len(text) > 10 and prompt not in text:
                            response_text = text
                            print(f"✅ Jules stealth yanıtı alındı: {selector}")
                            break
                if response_text:
                    break
            except Exception as e:
                continue

        if not response_text:
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                lines = body_text.split('\n')
                for i, line in enumerate(lines):
                    if prompt in line and i < len(lines) - 1:
                        response_text = '\n'.join(lines[i+1:i+5])
                        break
                if not response_text:
                    response_text = "Jules yanıtı tespit edilemedi, ancak sayfa yüklendi."
            except:
                response_text = "Jules ile stealth iletişim kuruldu, ancak yanıt okunamadı."

        return response_text
    
    def _wait_for_google_login(self, timeout=120):
        """Google login bekleme (stealth mode)"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_url = self.driver.current_url
            
            # Başarılı giriş kontrolü
            if ("myaccount.google.com" in current_url or 
                "mail.google.com" in current_url or
                "drive.google.com" in current_url or
                "jules.google.com" in current_url):
                return True
            
            # İnsan benzeri hareket
            if random.random() < 0.1:
                self._human_like_interactions()
            
            time.sleep(2)
            remaining = int(timeout - (time.time() - start_time))
            if remaining % 10 == 0:  # Her 10 saniyede bir bilgi ver
                print(f"⏳ Google giriş bekleniyor... ({remaining}s kaldı)")
        
        return False
    
    def interact_with_openwebui(self, prompt: str) -> str:
        """Interact with Open WebUI (eski fonksiyon korundu)"""
        openwebui_url = "http://localhost:3000"
        
        openwebui_tab_index = -1
        if self.driver:
            for i, handle in enumerate(self.tab_handles):
                self.driver.switch_to.window(handle)
                if openwebui_url in self.driver.current_url:
                    openwebui_tab_index = i
                    break

        if openwebui_tab_index != -1:
            self.switch_to_tab(openwebui_tab_index)
        else:
            self.open_new_tab(openwebui_url)
            sleep(5)

        prompt_input_selector = 'div.px-2.5, textarea[id="chat-input"], textarea[placeholder*="Message"], textarea[aria-label*="Message"], div[contenteditable="true"]'
        self.type_text(prompt, prompt_input_selector)

        send_button_selector = 'button[id="send-button"], button[aria-label*="Send"], button[title*="Send"], button[type="submit"]'
        self.click_element(send_button_selector)

        sleep(15)

        last_message_selector = '.message-content, .markdown, .prose, div[data-testid="message-text"], div.response-message'
        response_text = ""
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR, last_message_selector)
            if messages:
                response_text = messages[-1].text
        except Exception as e:
            print(f"Error getting response text: {e}")

        return response_text

    def close_browser(self):
        """Close the browser and save cookies."""
        if self.driver:
            try:
                if self.is_stealth_mode:
                    self._save_cookies()
                self.driver.quit()
                print("🔴 Stealth browser kapatıldı")
            except:
                pass
            finally:
                self.driver = None
                self.tab_handles = []
                self.current_tab_handle = None

    def quit(self):
        """Compatibility wrapper for closing the browser."""
        self.close_browser()

    def open_new_tab(self, url: str | None = None):
        """Open a new tab, optionally navigate to a URL."""
        if self.driver:
            self.driver.execute_script("window.open('');")
            self.tab_handles = self.driver.window_handles
            self.driver.switch_to.window(self.tab_handles[-1])
            self.current_tab_handle = self.driver.current_window_handle
            if url:
                self.go_to(url)
            sleep(1)

    def switch_to_tab(self, tab_index: int):
        """Switch to a specific tab by index."""
        if self.driver and 0 <= tab_index < len(self.tab_handles):
            self.driver.switch_to.window(self.tab_handles[tab_index])
            self.current_tab_handle = self.driver.current_window_handle
            sleep(1)

    def close_current_tab(self):
        """Close the current tab."""
        if self.driver and len(self.tab_handles) > 1:
            self.driver.close()
            self.tab_handles = self.driver.window_handles
            self.driver.switch_to.window(self.tab_handles[-1])
            self.current_tab_handle = self.driver.current_window_handle
            sleep(1)
        elif self.driver and len(self.tab_handles) == 1:
            self.close_browser()

    # Enhanced Stealth Features
    def enhanced_stealth_bypass(self):
        # Viewport randomization
        viewports = [(1366, 768), (1920, 1080), (1440, 900)]
        viewport = random.choice(viewports)
        self.driver.set_window_size(viewport[0], viewport[1])
        
        # Canvas fingerprint spoofing
        self.driver.execute_script("""
            const getContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type) {
                if (type === '2d') {
                    const context = getContext.call(this, type);
                    const getImageData = context.getImageData;
                    context.getImageData = function(x, y, width, height) {
                        const imageData = getImageData.call(this, x, y, width, height);
                        for (let i = 0; i < imageData.data.length; i += 4) {
                            imageData.data[i] = imageData.data[i] + Math.random() * 0.1;
                        }
                        return imageData;
                    };
                    return context;
                }
                return getContext.call(this, type);
            };
        """)
        
        # WebGL fingerprint spoofing
        self.driver.execute_script("""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter.call(this, parameter);
            };
        """)

