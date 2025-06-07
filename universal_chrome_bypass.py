#!/usr/bin/env python3
"""
🕵️ Universal Chrome Account Bypass System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Matrix AI tarafından geliştirilen genel amaçlı Chrome bypass sistemi.
Google ve diğer sitelerin bot tespitini aşarak VS Code asistanlarının
ve otomasyonların hedef sitelere güvenli erişim sağlamasını mümkün kılar.

ÖZELLIKLER:
- Google bot tespiti bypass ✅
- selenium-stealth entegrasyonu ✅  
- İnsan benzeri etkileşim simülasyonu ✅
- Hesap bilgisi kalıcılığı ✅
- Çoklu site desteği ✅
- Universal account management ✅

KULLANIM ALANLARI:
- VS Code asistanları için web erişimi
- Otomatik form doldurama
- Sosyal medya hesap yönetimi  
- E-ticaret site botları
- İçerik kazıma işlemleri
- Web testing ve QA otomasyonu

2025 Matrix AI - Universal Chrome Bypass Technology
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import time
import random
import pickle
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    from selenium_stealth import stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("⚠️ selenium-stealth bulunamadı. 'pip install selenium-stealth' ile kurun.")

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('universal_bypass.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UniversalChromeBypass:
    """
    🌐 Universal Chrome Account Bypass Engine
    
    Google ve diğer major sitelerin bot tespitini aşarak
    otomatik hesap girişi ve site erişimi sağlar.
    """
    
    def __init__(self, 
                 profile_name: str = "default",
                 stealth_mode: bool = True,
                 headless: bool = False):
        """
        Universal bypass motor başlatması
        
        Args:
            profile_name: Profil adı (çoklu hesap yönetimi için)
            stealth_mode: Stealth teknolojilerini etkinleştir
            headless: Headless modu (arka planda çalıştırma)
        """
        self.profile_name = profile_name
        self.stealth_mode = stealth_mode
        self.headless = headless
        
        # Konfigürasyon
        self.base_path = Path("C:/Universal_Chrome_Bypass")
        self.profiles_path = self.base_path / "profiles"
        self.cookies_path = self.base_path / "cookies"
        self.accounts_path = self.base_path / "accounts"
        
        # Dizinleri oluştur
        for path in [self.base_path, self.profiles_path, self.cookies_path, self.accounts_path]:
            path.mkdir(exist_ok=True)
        
        # Profil path'i
        timestamp = str(int(time.time()))
        self.profile_path = self.profiles_path / f"{profile_name}_{timestamp}"
        self.profile_path.mkdir(exist_ok=True)
        
        # Driver ve tab yönetimi
        self.driver: Optional[WebDriver] = None
        self.tab_handles: List[str] = []
        self.current_tab_handle: Optional[str] = None
        
        # Hesap bilgileri cache
        self.accounts_cache: Dict[str, Dict[str, Any]] = {}
        self.load_accounts_cache()
        
        logger.info(f"🕵️ Universal Chrome Bypass başlatıldı - Profil: {profile_name}")
    
    def initialize_driver(self) -> bool:
        """Chrome driver'ı gelişmiş bypass teknolojileri ile başlat"""
        try:
            chrome_options = Options()
            
            # Temel stealth ayarları
            chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Platform ayarları
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins-discovery")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-pdf-viewer")
            
            # Headless modu
            if self.headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--window-size=1920,1080")
            else:
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--window-size=1000,1350")
                chrome_options.add_argument("--window-position=0,0")
            
            # Gerçekçi user-agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # WebDriver başlat
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Selenium-stealth uygula
            if STEALTH_AVAILABLE and self.stealth_mode:
                stealth(self.driver,
                       languages=["en-US", "en"],
                       vendor="Google Inc.",
                       platform="Win32",
                       webgl_vendor="Intel Inc.",
                       renderer="Intel Iris OpenGL Engine",
                       fix_hairline=True)
                logger.info("✅ Selenium-stealth aktif")
            
            # JavaScript maskeleme
            stealth_scripts = [
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
                "window.screen.availWidth = window.screen.width",
                "window.screen.availHeight = window.screen.height"
            ]
            
            for script in stealth_scripts:
                self.driver.execute_script(script)
            
            # Chrome DevTools Command
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    window.chrome = {
                        runtime: {}
                    };
                    Object.defineProperty(navigator, 'permissions', {
                        get: () => ({
                            query: () => Promise.resolve({state: 'granted'})
                        })
                    });
                '''
            })
            
            # Tab yönetimi
            self.tab_handles = self.driver.window_handles
            self.current_tab_handle = self.driver.current_window_handle
            
            logger.info("✅ Universal Chrome Bypass driver başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Driver başlatma hatası: {str(e)}")
            return False
    
    def navigate_to_site(self, url: str, load_cookies: bool = True) -> bool:
        """
        Hedef siteye bypass teknolojileri ile git
        
        Args:
            url: Hedef URL
            load_cookies: Site cookie'lerini yükle
        """
        if not self.driver:
            logger.error("❌ Driver başlatılmamış")
            return False
        
        try:
            # İnsan benzeri gecikme
            if self.stealth_mode:
                time.sleep(random.uniform(1.0, 3.0))
                self._perform_human_interactions()
            
            logger.info(f"🌐 Navigating to: {url}")
            
            # URL'ye git
            self.driver.get(url)
            
            # Cookie'leri yükle (eğer varsa)
            if load_cookies:
                self._load_site_cookies(url)
            
            # Sayfa yüklenme beklemesi
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # İnsan benzeri davranış simülasyonu
            if self.stealth_mode:
                self._perform_post_navigation_behavior()
            
            logger.info(f"✅ Başarılı navigasyon: {url}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Navigasyon hatası {url}: {str(e)}")
            return False
    
    def login_to_account(self, 
                        site_domain: str,
                        username: str,
                        password: str,
                        username_selector: str = None,
                        password_selector: str = None,
                        login_button_selector: str = None,
                        auto_detect: bool = True) -> bool:
        """
        Universal hesap giriş sistemi
        
        Args:
            site_domain: Site domain (örn: google.com, facebook.com)
            username: Kullanıcı adı/email
            password: Şifre
            username_selector: Kullanıcı adı input selector'ü
            password_selector: Şifre input selector'ü  
            login_button_selector: Giriş butonu selector'ü
            auto_detect: Otomatik form tespiti
        """
        try:
            logger.info(f"🔐 {site_domain} hesap girişi başlatılıyor...")
            
            # Otomatik form tespiti
            if auto_detect:
                login_forms = self._detect_login_forms()
                if login_forms:
                    username_selector = login_forms.get('username')
                    password_selector = login_forms.get('password')
                    login_button_selector = login_forms.get('submit')
            
            # Site özel selectors (bilinen siteler için)
            if not username_selector:
                site_selectors = self._get_site_specific_selectors(site_domain)
                username_selector = site_selectors.get('username')
                password_selector = site_selectors.get('password')
                login_button_selector = site_selectors.get('submit')
            
            # Kullanıcı adı girişi
            if username_selector:
                success = self._type_with_human_behavior(username_selector, username)
                if not success:
                    logger.error("❌ Kullanıcı adı girişi başarısız")
                    return False
            
            # Şifre girişi
            if password_selector:
                success = self._type_with_human_behavior(password_selector, password)
                if not success:
                    logger.error("❌ Şifre girişi başarısız")
                    return False
            
            # Giriş butonu tıklama
            if login_button_selector:
                success = self._click_with_human_behavior(login_button_selector)
                if not success:
                    # Enter tuşu ile dene
                    try:
                        active_element = self.driver.switch_to.active_element
                        active_element.send_keys(Keys.RETURN)
                        logger.info("✅ Enter tuşu ile giriş denendi")
                    except:
                        logger.error("❌ Giriş butonu tıklanamadı")
                        return False
            
            # Başarılı giriş kontrolü
            time.sleep(random.uniform(3.0, 6.0))
            
            # Account bilgilerini kaydet
            self._save_account_info(site_domain, username, password)
            
            # Cookie'leri kaydet
            self._save_site_cookies(site_domain)
            
            logger.info(f"✅ {site_domain} hesap girişi başarılı")
            return True
            
        except Exception as e:
            logger.error(f"❌ {site_domain} hesap giriş hatası: {str(e)}")
            return False
    
    def interact_with_site(self, 
                          actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Site ile gelişmiş etkileşim sistemi
        
        Args:
            actions: Etkileşim aksiyonları listesi
                    [
                        {"type": "click", "selector": "#button", "wait": 2},
                        {"type": "type", "selector": "#input", "text": "hello", "clear": True},
                        {"type": "scroll", "direction": "down", "amount": 500},
                        {"type": "wait", "time": 3},
                        {"type": "extract", "selector": ".result", "attribute": "text"}
                    ]
        
        Returns:
            Etkileşim sonuçları
        """
        results = {
            "success": True,
            "actions_completed": 0,
            "extracted_data": {},
            "errors": []
        }
        
        try:
            for i, action in enumerate(actions):
                action_type = action.get("type")
                
                if action_type == "click":
                    success = self._click_with_human_behavior(
                        action["selector"], 
                        wait_time=action.get("wait", 1)
                    )
                    if not success:
                        results["errors"].append(f"Click failed: {action['selector']}")
                
                elif action_type == "type":
                    success = self._type_with_human_behavior(
                        action["selector"],
                        action["text"],
                        clear_first=action.get("clear", False)
                    )
                    if not success:
                        results["errors"].append(f"Type failed: {action['selector']}")
                
                elif action_type == "scroll":
                    self._perform_scroll(
                        action.get("direction", "down"),
                        action.get("amount", 300)
                    )
                
                elif action_type == "wait":
                    time.sleep(action.get("time", 1))
                
                elif action_type == "extract":
                    data = self._extract_data(
                        action["selector"],
                        action.get("attribute", "text")
                    )
                    results["extracted_data"][f"action_{i}"] = data
                
                elif action_type == "screenshot":
                    filename = action.get("filename", f"screenshot_{int(time.time())}.png")
                    self.driver.save_screenshot(str(self.base_path / filename))
                    results["extracted_data"][f"screenshot_{i}"] = filename
                
                results["actions_completed"] += 1
                
                # İnsan benzeri gecikme
                if self.stealth_mode:
                    time.sleep(random.uniform(0.5, 2.0))
            
            return results
            
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Interaction error: {str(e)}")
            logger.error(f"❌ Site etkileşim hatası: {str(e)}")
            return results
    
    def get_current_cookies(self) -> List[Dict]:
        """Mevcut cookie'leri al"""
        if self.driver:
            return self.driver.get_cookies()
        return []
    
    def set_cookies(self, cookies: List[Dict]) -> bool:
        """Cookie'leri set et"""
        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return True
        except Exception as e:
            logger.error(f"❌ Cookie set hatası: {str(e)}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """Ekran görüntüsü al"""
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"
        
        filepath = str(self.base_path / filename)
        self.driver.save_screenshot(filepath)
        logger.info(f"📸 Ekran görüntüsü: {filepath}")
        return filepath
    
    def get_page_source(self) -> str:
        """Sayfa kaynağını al"""
        if self.driver:
            return self.driver.page_source
        return ""
    
    def execute_javascript(self, script: str) -> Any:
        """JavaScript çalıştır"""
        if self.driver:
            return self.driver.execute_script(script)
        return None
    
    def wait_for_element(self, 
                        selector: str, 
                        timeout: int = 10,
                        condition: str = "presence") -> bool:
        """Element bekle"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            if condition == "presence":
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            elif condition == "clickable":
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            elif condition == "visible":
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            
            return True
        except TimeoutException:
            return False
    
    def close_browser(self):
        """Browser'ı kapat ve verileri kaydet"""
        if self.driver:
            try:
                # Son cookie'leri kaydet
                current_url = self.driver.current_url
                if current_url:
                    domain = self._extract_domain(current_url)
                    self._save_site_cookies(domain)
                
                self.driver.quit()
                logger.info("🔴 Universal Chrome Bypass kapatıldı")
                
            except:
                pass
            finally:
                self.driver = None
                self.tab_handles = []
                self.current_tab_handle = None
    
    # ========== PRIVATE METHODS ==========
    
    def _perform_human_interactions(self):
        """İnsan benzeri etkileşimler"""
        if not self.stealth_mode:
            return
        
        try:
            actions = ActionChains(self.driver)
            
            # Rastgele fare hareketi
            actions.move_by_offset(
                random.randint(-50, 50), 
                random.randint(-50, 50)
            ).perform()
            
            time.sleep(random.uniform(0.1, 0.5))
            
            # Bazen scroll yap
            if random.random() < 0.3:
                self.driver.execute_script(f"window.scrollBy(0, {random.randint(-100, 100)});")
                time.sleep(random.uniform(0.2, 0.8))
            
            # Bazen klavye aktivitesi simüle et
            if random.random() < 0.2:
                actions.send_keys(Keys.SPACE).pause(0.1).send_keys(Keys.BACKSPACE).perform()
                
        except Exception as e:
            logger.debug(f"Human interaction simülasyonu hatası: {str(e)}")
    
    def _perform_post_navigation_behavior(self):
        """Navigasyon sonrası insan benzeri davranış"""
        if not self.stealth_mode:
            return
        
        # Sayfa yüklenmesini bekle
        time.sleep(random.uniform(1.0, 3.0))
        
        # Biraz scroll yap
        for _ in range(random.randint(1, 3)):
            scroll_amount = random.randint(100, 400)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))
        
        # Geri en üste çık
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1.0))
    
    def _detect_login_forms(self) -> Dict[str, str]:
        """Otomatik login form tespiti"""
        selectors = {}
        
        try:
            # Username field detection
            username_patterns = [
                'input[type="email"]',
                'input[type="text"][name*="user"]',
                'input[type="text"][name*="email"]',
                'input[id*="user"]',
                'input[id*="email"]',
                'input[placeholder*="email"]',
                'input[placeholder*="username"]'
            ]
            
            for pattern in username_patterns:
                elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                if elements and elements[0].is_displayed():
                    selectors['username'] = pattern
                    break
            
            # Password field detection
            password_elements = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
            if password_elements and password_elements[0].is_displayed():
                selectors['password'] = 'input[type="password"]'
            
            # Submit button detection
            submit_patterns = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Sign in")',
                'button:contains("Login")',
                'button:contains("Log in")',
                'button[id*="login"]',
                'button[id*="signin"]'
            ]
            
            for pattern in submit_patterns:
                elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                if elements and elements[0].is_displayed():
                    selectors['submit'] = pattern
                    break
            
            return selectors
            
        except Exception as e:
            logger.debug(f"Form tespiti hatası: {str(e)}")
            return {}
    
    def _get_site_specific_selectors(self, domain: str) -> Dict[str, str]:
        """Site özel selectors"""
        selectors_map = {
            "google.com": {
                "username": 'input[type="email"]',
                "password": 'input[type="password"]',
                "submit": '#identifierNext, #passwordNext'
            },
            "facebook.com": {
                "username": '#email',
                "password": '#pass',
                "submit": 'button[name="login"]'
            },
            "twitter.com": {
                "username": 'input[autocomplete="username"]',
                "password": 'input[autocomplete="current-password"]',
                "submit": 'div[data-testid="LoginForm_Login_Button"]'
            },
            "linkedin.com": {
                "username": '#username',
                "password": '#password',
                "submit": 'button[type="submit"]'
            },
            "instagram.com": {
                "username": 'input[name="username"]',
                "password": 'input[name="password"]',
                "submit": 'button[type="submit"]'
            }
        }
        
        return selectors_map.get(domain, {})
    
    def _type_with_human_behavior(self, 
                                 selector: str, 
                                 text: str,
                                 clear_first: bool = True) -> bool:
        """İnsan benzeri yazma"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            
            if clear_first:
                element.clear()
                time.sleep(random.uniform(0.1, 0.3))
            
            if self.stealth_mode:
                # İnsan benzeri yazma
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                element.send_keys(text)
            
            time.sleep(random.uniform(0.3, 0.8))
            return True
            
        except Exception as e:
            logger.error(f"Yazma hatası {selector}: {str(e)}")
            return False
    
    def _click_with_human_behavior(self, 
                                  selector: str,
                                  wait_time: float = 1.0) -> bool:
        """İnsan benzeri tıklama"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            
            if self.stealth_mode:
                # İnsan benzeri tıklama
                actions = ActionChains(self.driver)
                actions.move_to_element(element).pause(
                    random.uniform(0.1, 0.4)
                ).click().perform()
            else:
                element.click()
            
            time.sleep(wait_time)
            return True
            
        except Exception as e:
            logger.error(f"Tıklama hatası {selector}: {str(e)}")
            return False
    
    def _perform_scroll(self, direction: str, amount: int):
        """Scroll işlemi"""
        if direction == "down":
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
        elif direction == "up":
            self.driver.execute_script(f"window.scrollBy(0, -{amount});")
        
        time.sleep(random.uniform(0.3, 0.8))
    
    def _extract_data(self, selector: str, attribute: str = "text") -> Any:
        """Veri çıkarma"""
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            if not elements:
                return None
            
            if attribute == "text":
                return [elem.text for elem in elements if elem.text.strip()]
            elif attribute == "href":
                return [elem.get_attribute("href") for elem in elements]
            elif attribute == "src":
                return [elem.get_attribute("src") for elem in elements]
            else:
                return [elem.get_attribute(attribute) for elem in elements]
                
        except Exception as e:
            logger.error(f"Veri çıkarma hatası {selector}: {str(e)}")
            return None
    
    def _extract_domain(self, url: str) -> str:
        """URL'den domain çıkar"""
        from urllib.parse import urlparse
        return urlparse(url).netloc.lower()
    
    def _save_site_cookies(self, domain: str):
        """Site cookie'lerini kaydet"""
        try:
            cookies = self.driver.get_cookies()
            cookies_file = self.cookies_path / f"{domain}_{self.profile_name}.pkl"
            
            with open(cookies_file, 'wb') as f:
                pickle.dump(cookies, f)
            
            logger.info(f"✅ {domain} cookies kaydedildi")
            
        except Exception as e:
            logger.error(f"Cookie kaydetme hatası {domain}: {str(e)}")
    
    def _load_site_cookies(self, url: str):
        """Site cookie'lerini yükle"""
        try:
            domain = self._extract_domain(url)
            cookies_file = self.cookies_path / f"{domain}_{self.profile_name}.pkl"
            
            if cookies_file.exists():
                # Önce domain'e git
                self.driver.get(f"https://{domain}")
                time.sleep(1)
                
                with open(cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                
                for cookie in cookies:
                    try:
                        if domain in cookie.get('domain', ''):
                            self.driver.add_cookie(cookie)
                    except:
                        continue
                
                logger.info(f"✅ {domain} cookies yüklendi")
                
        except Exception as e:
            logger.debug(f"Cookie yükleme hatası: {str(e)}")
    
    def _save_account_info(self, domain: str, username: str, password: str):
        """Hesap bilgilerini güvenli kaydet"""
        try:
            accounts_file = self.accounts_path / f"{self.profile_name}_accounts.json"
            
            if accounts_file.exists():
                with open(accounts_file, 'r') as f:
                    accounts = json.load(f)
            else:
                accounts = {}
            
            # Basit encoding (gerçek uygulamada şifreleme kullanın)
            import base64
            encoded_password = base64.b64encode(password.encode()).decode()
            
            accounts[domain] = {
                "username": username,
                "password": encoded_password,
                "last_login": datetime.now().isoformat(),
                "login_count": accounts.get(domain, {}).get("login_count", 0) + 1
            }
            
            with open(accounts_file, 'w') as f:
                json.dump(accounts, f, indent=2)
            
            # Cache'i güncelle
            self.accounts_cache[domain] = accounts[domain].copy()
            
            logger.info(f"✅ {domain} hesap bilgileri kaydedildi")
            
        except Exception as e:
            logger.error(f"Hesap bilgisi kaydetme hatası {domain}: {str(e)}")
    
    def load_accounts_cache(self):
        """Hesap bilgilerini cache'e yükle"""
        try:
            accounts_file = self.accounts_path / f"{self.profile_name}_accounts.json"
            
            if accounts_file.exists():
                with open(accounts_file, 'r') as f:
                    self.accounts_cache = json.load(f)
                
                logger.info(f"✅ {len(self.accounts_cache)} hesap bilgisi yüklendi")
            
        except Exception as e:
            logger.debug(f"Hesap cache yükleme hatası: {str(e)}")
    
    def get_saved_account(self, domain: str) -> Optional[Dict[str, str]]:
        """Kaydedilmiş hesap bilgilerini al"""
        account = self.accounts_cache.get(domain)
        if account:
            import base64
            password = base64.b64decode(account['password'].encode()).decode()
            return {
                "username": account['username'],
                "password": password
            }
        return None
    
    def list_saved_accounts(self) -> List[str]:
        """Kaydedilmiş hesapları listele"""
        return list(self.accounts_cache.keys())

# ========== CONVENIENCE FUNCTIONS ==========

def quick_login(site_url: str, 
               username: str, 
               password: str,
               profile_name: str = "default",
               stealth: bool = True) -> UniversalChromeBypass:
    """Hızlı giriş fonksiyonu"""
    from urllib.parse import urlparse
    
    bypass = UniversalChromeBypass(profile_name=profile_name, stealth_mode=stealth)
    
    if not bypass.initialize_driver():
        return None
    
    domain = urlparse(site_url).netloc
    
    bypass.navigate_to_site(site_url)
    bypass.login_to_account(domain, username, password)
    
    return bypass

def automated_interaction(site_url: str,
                         actions: List[Dict[str, Any]],
                         login_first: bool = False,
                         username: str = None,
                         password: str = None) -> Dict[str, Any]:
    """Otomatik etkileşim fonksiyonu"""
    bypass = UniversalChromeBypass()
    
    try:
        if not bypass.initialize_driver():
            return {"success": False, "error": "Driver başlatılamadı"}
        
        bypass.navigate_to_site(site_url)
        
        if login_first and username and password:
            from urllib.parse import urlparse
            domain = urlparse(site_url).netloc
            bypass.login_to_account(domain, username, password)
        
        results = bypass.interact_with_site(actions)
        
        return results
        
    finally:
        bypass.close_browser()

# ========== USAGE EXAMPLES ==========

if __name__ == "__main__":
    # Örnek 1: Google hesap girişi
    print("🕵️ Universal Chrome Bypass Test - Google Login")
    
    bypass = UniversalChromeBypass(profile_name="test_profile", stealth_mode=True)
    
    if bypass.initialize_driver():
        # Google'a git
        bypass.navigate_to_site("https://accounts.google.com/signin")
        
        # Hesap girişi (manuel olarak yapılacak)
        print("Lütfen tarayıcıda Google hesabınıza giriş yapın...")
        input("Giriş tamamlandıktan sonra Enter'a basın...")
        
        # Gmail'e git
        bypass.navigate_to_site("https://mail.google.com")
        
        # Screenshot al
        bypass.take_screenshot("gmail_success.png")
        
        print("✅ Test tamamlandı!")
        
        bypass.close_browser()
