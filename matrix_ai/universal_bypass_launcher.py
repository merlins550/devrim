"""
🕵️ Universal Chrome Bypass Launcher
Jules'tan bağımsız, genel amaçlı Chrome bypass sistemi
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from pathlib import Path
from .universal_chrome_bypass import UniversalChromeBypass

class UniversalBypassLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🕵️ Universal Chrome Bypass Launcher")
        self.window.geometry("800x600")
        self.window.configure(bg='#1e1e1e')
        
        # Bypass instance
        self.bypass = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Ana frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Başlık
        title_label = tk.Label(main_frame, 
                              text="🕵️ Universal Chrome Bypass", 
                              font=("Arial", 16, "bold"),
                              bg='#1e1e1e', fg='#00ff00')
        title_label.pack(pady=10)
        
        # Profil seçimi
        profile_frame = ttk.LabelFrame(main_frame, text="Profil Ayarları")
        profile_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(profile_frame, text="Profil Adı:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.profile_entry = tk.Entry(profile_frame, width=30)
        self.profile_entry.insert(0, "default")
        self.profile_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.stealth_var = tk.BooleanVar(value=True)
        tk.Checkbutton(profile_frame, text="🕵️ Stealth Modu", 
                      variable=self.stealth_var).grid(row=0, column=2, padx=5, pady=5)
        
        # Site girişi
        site_frame = ttk.LabelFrame(main_frame, text="Site Bilgileri")
        site_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(site_frame, text="Hedef URL:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.url_entry = tk.Entry(site_frame, width=50)
        self.url_entry.insert(0, "https://accounts.google.com")
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        tk.Label(site_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = tk.Entry(site_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(site_frame, text="Password:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.password_entry = tk.Entry(site_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(button_frame, text="🚀 Bypass Başlat", 
                                  command=self.start_bypass, bg='#00ff00', fg='black',
                                  font=("Arial", 10, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.navigate_btn = tk.Button(button_frame, text="🌐 Siteye Git", 
                                     command=self.navigate_to_site, bg='#0080ff', fg='white',
                                     font=("Arial", 10, "bold"))
        self.navigate_btn.pack(side=tk.LEFT, padx=5)
        
        self.login_btn = tk.Button(button_frame, text="🔑 Otomatik Giriş", 
                                  command=self.auto_login, bg='#ff8000', fg='white',
                                  font=("Arial", 10, "bold"))
        self.login_btn.pack(side=tk.LEFT, padx=5)
        
        self.screenshot_btn = tk.Button(button_frame, text="📸 Screenshot", 
                                       command=self.take_screenshot, bg='#8000ff', fg='white',
                                       font=("Arial", 10, "bold"))
        self.screenshot_btn.pack(side=tk.LEFT, padx=5)
        
        self.close_btn = tk.Button(button_frame, text="❌ Kapat", 
                                  command=self.close_bypass, bg='#ff0000', fg='white',
                                  font=("Arial", 10, "bold"))
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Hızlı site butonları
        quick_frame = ttk.LabelFrame(main_frame, text="Hızlı Erişim")
        quick_frame.pack(fill=tk.X, pady=5)
        
        sites = [
            ("📧 Gmail", "https://mail.google.com"),
            ("📘 Facebook", "https://facebook.com"),
            ("🐦 Twitter", "https://twitter.com"),
            ("💼 LinkedIn", "https://linkedin.com"),
            ("📷 Instagram", "https://instagram.com"),
            ("🔍 Google", "https://google.com")
        ]
        
        for i, (name, url) in enumerate(sites):
            btn = tk.Button(quick_frame, text=name, 
                           command=lambda u=url: self.quick_navigate(u),
                           width=12, height=2)
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
        
        # Log alanı
        log_frame = ttk.LabelFrame(main_frame, text="İşlem Logları")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
                                                 bg='#000000', fg='#00ff00',
                                                 font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="🔴 Hazır - Bypass başlatılmadı")
        status_label = tk.Label(main_frame, textvariable=self.status_var,
                               bg='#1e1e1e', fg='#ffffff', anchor=tk.W)
        status_label.pack(fill=tk.X, pady=5)
        
        self.log("🕵️ Universal Chrome Bypass Launcher hazır!")
        self.log("💡 İpucu: Önce 'Bypass Başlat' butonuna tıklayın")
    
    def log(self, message):
        """Log mesajı ekle"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.window.update()
    
    def start_bypass(self):
        """Bypass sistemini başlat"""
        def _start():
            try:
                profile_name = self.profile_entry.get() or "default"
                stealth_mode = self.stealth_var.get()
                
                self.log(f"🚀 Bypass başlatılıyor... (Profil: {profile_name}, Stealth: {stealth_mode})")
                self.status_var.set("🟡 Bypass başlatılıyor...")
                
                self.bypass = UniversalChromeBypass(
                    profile_name=profile_name,
                    stealth_mode=stealth_mode
                )
                
                if self.bypass.initialize_driver():
                    self.log("✅ Chrome bypass başarıyla başlatıldı!")
                    self.status_var.set("🟢 Bypass aktif - Chrome hazır")
                    
                    # Butonları aktif et
                    self.navigate_btn.config(state=tk.NORMAL)
                    self.login_btn.config(state=tk.NORMAL)
                    self.screenshot_btn.config(state=tk.NORMAL)
                    self.start_btn.config(state=tk.DISABLED)
                else:
                    self.log("❌ Chrome bypass başlatılamadı!")
                    self.status_var.set("🔴 Hata - Bypass başarısız")
                    
            except Exception as e:
                self.log(f"❌ Hata: {str(e)}")
                self.status_var.set("🔴 Hata oluştu")
        
        threading.Thread(target=_start, daemon=True).start()
    
    def navigate_to_site(self):
        """Siteye git"""
        if not self.bypass:
            messagebox.showwarning("Uyarı", "Önce bypass sistemini başlatın!")
            return
        
        def _navigate():
            try:
                url = self.url_entry.get()
                if not url:
                    self.log("❌ URL boş olamaz!")
                    return
                
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                    self.url_entry.delete(0, tk.END)
                    self.url_entry.insert(0, url)
                
                self.log(f"🌐 {url} adresine gidiliyor...")
                self.status_var.set(f"🌐 Navigasyon: {url}")
                
                if self.bypass.navigate_to_site(url):
                    self.log(f"✅ {url} başarıyla yüklendi!")
                    self.status_var.set(f"✅ Sitede: {url}")
                else:
                    self.log(f"❌ {url} yüklenemedi!")
                    
            except Exception as e:
                self.log(f"❌ Navigasyon hatası: {str(e)}")
        
        threading.Thread(target=_navigate, daemon=True).start()
    
    def auto_login(self):
        """Otomatik giriş yap"""
        if not self.bypass:
            messagebox.showwarning("Uyarı", "Önce bypass sistemini başlatın!")
            return
        
        def _login():
            try:
                url = self.url_entry.get()
                username = self.username_entry.get()
                password = self.password_entry.get()
                
                if not all([url, username, password]):
                    self.log("❌ URL, username ve password gerekli!")
                    return
                
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                
                self.log(f"🔑 {domain} için otomatik giriş yapılıyor...")
                self.status_var.set(f"🔑 Giriş yapılıyor: {domain}")
                
                if self.bypass.login_to_account(domain, username, password):
                    self.log(f"✅ {domain} girişi başarılı!")
                    self.status_var.set(f"✅ Giriş yapıldı: {domain}")
                else:
                    self.log(f"❌ {domain} girişi başarısız!")
                    
            except Exception as e:
                self.log(f"❌ Giriş hatası: {str(e)}")
        
        threading.Thread(target=_login, daemon=True).start()
    
    def quick_navigate(self, url):
        """Hızlı navigasyon"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        if self.bypass:
            self.navigate_to_site()
    
    def take_screenshot(self):
        """Screenshot al"""
        if not self.bypass:
            messagebox.showwarning("Uyarı", "Önce bypass sistemini başlatın!")
            return
        
        try:
            filename = self.bypass.take_screenshot()
            self.log(f"📸 Screenshot alındı: {filename}")
            messagebox.showinfo("Başarılı", f"Screenshot kaydedildi:\n{filename}")
        except Exception as e:
            self.log(f"❌ Screenshot hatası: {str(e)}")
    
    def close_bypass(self):
        """Bypass sistemini kapat"""
        try:
            if self.bypass:
                self.bypass.close_browser()
                self.bypass = None
                
            self.log("🔴 Bypass sistemi kapatıldı")
            self.status_var.set("🔴 Bypass kapatıldı")
            
            # Butonları sıfırla
            self.start_btn.config(state=tk.NORMAL)
            self.navigate_btn.config(state=tk.DISABLED)
            self.login_btn.config(state=tk.DISABLED)
            self.screenshot_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            self.log(f"❌ Kapatma hatası: {str(e)}")
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self):
        """Uygulama kapanırken"""
        self.close_bypass()
        self.window.destroy()

if __name__ == "__main__":
    print("🕵️ Universal Chrome Bypass Launcher başlatılıyor...")
    launcher = UniversalBypassLauncher()
    launcher.run()
