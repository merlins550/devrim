#!/usr/bin/env python3
"""
Matrix AI Intent Detection System
Kullanıcı mesajlarının amacını tespit eden gelişmiş AI sistemi

Bu modül:
- Natural Language Understanding
- Context-aware intent classification
- Multi-language support (Türkçe/İngilizce)
- Learning from user interactions
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class Intent:
    """Intent veri sınıfı"""
    name: str
    confidence: float
    entities: Dict[str, Any]
    context: str

class MatrixAIIntentDetector:
    """
    Matrix AI Intent Detection System
    
    Kullanıcı mesajlarını analiz ederek amacını tespit eder:
    - Proje oluşturma istekleri
    - GitHub operasyonları
    - Kod yardımı talepleri
    - Sistem kontrol komutları
    - Genel sorgular
    """
    
    def __init__(self):
        self.logger = logging.getLogger("IntentDetector")
        
        # Intent patterns ve anahtar kelimeler
        self.intent_patterns = self.load_intent_patterns()
        
        # Entity extraction patterns
        self.entity_patterns = self.load_entity_patterns()
        
        # Context memory (son konuşmaları hatırla)
        self.context_memory: List[Dict[str, Any]] = []
        self.max_context_memory = 10
        
        self.logger.info("Matrix AI Intent Detector initialized")
    
    def load_intent_patterns(self) -> Dict[str, Any]:
        """Intent patterns'i yükle"""
        return {
            "project_creation": {
                "keywords": [
                    # Türkçe
                    "proje", "site", "uygulama", "web", "app", "program", 
                    "yazılım", "sistem", "platform", "portal", "dashboard",
                    "e-ticaret", "blog", "forum", "api", "backend", "frontend",
                    "mobil", "desktop", "oyun", "bot", "servis",
                    
                    # İngilizce
                    "project", "website", "application", "web", "app", "program",
                    "software", "system", "platform", "portal", "dashboard",
                    "ecommerce", "e-commerce", "blog", "forum", "api", "backend", "frontend",
                    "mobile", "desktop", "game", "bot", "service"
                ],
                "actions": [
                    # Türkçe
                    "yap", "oluştur", "geliştir", "kur", "başlat", "inşa et", 
                    "hazırla", "üret", "çıkar", "tasarla", "kodla",
                    
                    # İngilizce  
                    "create", "make", "build", "develop", "generate", "setup",
                    "start", "design", "code", "implement"
                ],
                "patterns": [
                    r"bir (.+) (yap|oluştur|geliştir|kur)",
                    r"(.+) (sitesi|uygulaması|programı) (yap|oluştur)",
                    r"create (.+) (app|website|application)",
                    r"build (.+) (system|platform|project)",
                    r"make (.+) (for|with|using)"
                ],
                "examples": [
                    "Bir e-ticaret sitesi yap",
                    "Blog uygulaması oluştur", 
                    "React ile dashboard geliştir",
                    "Create a todo app",
                    "Build a REST API"
                ]
            },
            
            "github_operation": {
                "keywords": [
                    # Git/GitHub komutları
                    "commit", "push", "pull", "branch", "merge", "fork", "clone",
                    "repository", "repo", "github", "git", "version", "control",
                    
                    # Türkçe git işlemleri
                    "kod", "değişiklik", "güncelle", "kaydet", "yükle", "indir",
                    "dal", "birleştir", "kopyala", "depo", "sürüm"
                ],
                "actions": [
                    # Git actions
                    "commit", "push", "pull", "fetch", "checkout", "branch",
                    "merge", "rebase", "clone", "fork", "sync",
                    
                    # Türkçe actions
                    "kaydet", "yükle", "çek", "birleştir", "geç", "oluştur"
                ],
                "patterns": [
                    r"git (.+)",
                    r"github (.+)",
                    r"(commit|push|pull) (.+)",
                    r"(.+) (repository|repo) (.+)",
                    r"(.+) (branch|dal) (.+)"
                ],
                "examples": [
                    "Git commit yap",
                    "GitHub'a push et",
                    "Yeni branch oluştur",
                    "Repository klonla"
                ]
            },
            
            "code_assistance": {
                "keywords": [
                    # Türkçe
                    "kod", "fonksiyon", "class", "sınıf", "metod", "değişken",
                    "hata", "bug", "debug", "test", "optimize", "refactor",
                    "algoritma", "logic", "mantık", "syntax", "sözdizimi",
                    "kütüphane", "framework", "library", "import", "modül",
                    
                    # İngilizce
                    "code", "function", "class", "method", "variable", "array",
                    "error", "bug", "debug", "test", "optimize", "refactor", 
                    "algorithm", "logic", "syntax", "library", "framework",
                    "import", "module", "package"
                ],
                "actions": [
                    # Türkçe
                    "yaz", "düzelt", "optimize", "test", "kontrol", "incele",
                    "açıkla", "analiz", "çözümle", "öner", "geliştir",
                    
                    # İngilizce
                    "write", "fix", "debug", "optimize", "test", "check",
                    "explain", "analyze", "improve", "suggest", "review"
                ],
                "patterns": [
                    r"(.+) (kodunu|fonksiyonunu) (.+)",
                    r"(hata|bug|error) (.+)",
                    r"(debug|test|optimize) (.+)",
                    r"(.+) (nasıl|how) (.+)",
                    r"(fix|düzelt) (.+)"
                ],
                "examples": [
                    "Bu kodda hata var",
                    "Fonksiyonu optimize et",
                    "Debug yap",
                    "Nasıl yapabilirim?"
                ]
            },
            
            "system_control": {
                "keywords": [
                    # Sistem komutları
                    "başlat", "durdur", "aç", "kapat", "bağlan", "çıkış",
                    "sistem", "servis", "uygulama", "program", "terminal",
                    "vscode", "chrome", "browser", "chatgpt", "selenium",
                    
                    # İngilizce
                    "start", "stop", "open", "close", "connect", "disconnect",
                    "system", "service", "application", "program", "terminal"
                ],
                "actions": [
                    "başlat", "start", "durdur", "stop", "aç", "open", 
                    "kapat", "close", "bağlan", "connect", "çıkış", "exit"
                ],
                "patterns": [
                    r"(başlat|start) (.+)",
                    r"(aç|open) (.+)",
                    r"(kapat|close|durdur|stop) (.+)",
                    r"(.+) (bağlan|connect|başlat|start)"
                ],
                "examples": [
                    "VS Code başlat",
                    "ChatGPT aç",
                    "GitHub bağlan",
                    "Sistemi durdur"
                ]
            },
            
            "file_operation": {
                "keywords": [
                    # Dosya işlemleri
                    "dosya", "klasör", "dizin", "path", "yol", "save", "kaydet",
                    "read", "oku", "write", "yaz", "delete", "sil", "copy", "kopyala",
                    "move", "taşı", "rename", "yeniden adlandır",
                    
                    # Dosya türleri
                    "txt", "json", "py", "js", "html", "css", "md", "pdf"
                ],
                "actions": [
                    "oluştur", "create", "oku", "read", "yaz", "write",
                    "kaydet", "save", "sil", "delete", "kopyala", "copy",
                    "taşı", "move"
                ],
                "patterns": [
                    r"(.+) dosya (.+)",
                    r"(oku|read|yaz|write) (.+)",
                    r"(kaydet|save|sil|delete) (.+)"
                ],
                "examples": [
                    "Dosya oku",
                    "JSON kaydet", 
                    "Klasör oluştur"
                ]
            },
            
            "information_query": {
                "keywords": [
                    # Soru kelimeleri
                    "nedir", "nasıl", "ne", "kim", "nerede", "neden", "hangi",
                    "what", "how", "who", "where", "why", "which", "when",
                    
                    # Bilgi talepleri
                    "açıkla", "anlat", "göster", "öğret", "yardım", "help",
                    "explain", "show", "tell", "teach", "guide", "tutorial"
                ],
                "actions": [
                    "açıkla", "explain", "anlat", "tell", "göster", "show",
                    "öğret", "teach", "yardım", "help", "rehber", "guide"
                ],
                "patterns": [
                    r"(.+) (nedir|nasıl|ne)",
                    r"(what|how|why) (.+)",
                    r"(açıkla|explain|anlat|tell) (.+)",
                    r"(.+) (hakkında|about) (.+)"
                ],
                "examples": [
                    "Python nedir?",
                    "Nasıl yapabilirim?",
                    "React'i açıkla",
                    "What is machine learning?"
                ]
            }
        }
    
    def load_entity_patterns(self) -> Dict[str, str]:
        """Entity extraction patterns"""
        return {
            # Programlama dilleri
            "programming_language": r"\b(python|javascript|java|c\+\+|c#|php|ruby|go|rust|swift|kotlin|typescript|react|vue|angular|django|flask|node|express)\b",
            
            # Teknolojiler
            "technology": r"\b(html|css|sql|mongodb|postgresql|mysql|redis|docker|kubernetes|aws|azure|gcp|linux|windows|macos)\b",
            
            # Proje türleri
            "project_type": r"\b(website|web app|mobile app|desktop app|api|backend|frontend|fullstack|e-commerce|blog|cms|dashboard|admin panel)\b",
            
            # Dosya uzantıları
            "file_extension": r"\.(py|js|html|css|json|txt|md|pdf|doc|xlsx|csv|xml|yaml|yml)\b",
            
            # Git branch isimleri
            "branch_name": r"\b(main|master|develop|feature\/[\w-]+|hotfix\/[\w-]+|release\/[\w-]+)\b",
            
            # URL'ler
            "url": r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
            
            # GitHub repository
            "github_repo": r"github\.com\/[\w-]+\/[\w-]+",
            
            # Sayılar
            "number": r"\b\d+\b",
            
            # Email
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }
    
    def detect_intent(self, message: str, context: Optional[Dict[str, Any]] = None) -> Intent:
        """
        Ana intent detection fonksiyonu
        
        Args:
            message: Kullanıcı mesajı
            context: Önceki konuşma bağlamı
            
        Returns:
            Tespit edilen intent
        """
        
        message_lower = message.lower().strip()
        
        # Context'i memory'ye ekle
        self.add_to_context_memory(message, context)
        
        # Tüm intent'leri skorla
        intent_scores = {}
        
        for intent_name, intent_data in self.intent_patterns.items():
            score = self.calculate_intent_score(message_lower, intent_data)
            intent_scores[intent_name] = score
        
        # En yüksek skoru bul
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]
        
        # Threshold kontrolü
        confidence_threshold = 0.3
        if best_score < confidence_threshold:
            best_intent = "general_query"
            best_score = 0.5
        
        # Entity'leri çıkar
        entities = self.extract_entities(message)
        
        # Context-aware adjustments
        adjusted_intent, adjusted_score = self.apply_context_awareness(
            best_intent, best_score, message, entities
        )
        
        self.logger.info(f"Intent detected: {adjusted_intent} (confidence: {adjusted_score:.2f})")
        
        return Intent(
            name=adjusted_intent,
            confidence=adjusted_score,
            entities=entities,
            context=self.get_context_summary()
        )
    
    def calculate_intent_score(self, message: str, intent_data: Dict[str, Any]) -> float:
        """Intent için skor hesapla"""
        score = 0.0
        
        # Keyword matching
        keywords = intent_data.get("keywords", [])
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in message)
        keyword_score = min(keyword_matches / len(keywords), 1.0) if keywords else 0
        
        # Action word matching
        actions = intent_data.get("actions", [])
        action_matches = sum(1 for action in actions if action.lower() in message)
        action_score = min(action_matches / len(actions), 1.0) if actions else 0
        
        # Pattern matching
        patterns = intent_data.get("patterns", [])
        pattern_score = 0
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                pattern_score = 1.0
                break
        
        # Weighted combination
        score = (keyword_score * 0.4) + (action_score * 0.3) + (pattern_score * 0.3)
        
        return score
    
    def extract_entities(self, message: str) -> Dict[str, Any]:
        """Mesajdan entity'leri çıkar"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, message, re.IGNORECASE)
            if matches:
                entities[entity_type] = matches
        
        # Özel entity extraction'lar
        entities.update(self.extract_special_entities(message))
        
        return entities
    
    def extract_special_entities(self, message: str) -> Dict[str, Any]:
        """Özel entity'leri çıkar"""
        special_entities = {}
        
        # Proje adı çıkarma
        project_name_patterns = [
            r"(?:adı|named|called)\s+['\"]([^'\"]+)['\"]",
            r"['\"]([^'\"]+)['\"]\s+(?:projesi|project|uygulaması|app)",
            r"bir\s+([^\.]+?)\s+(?:yap|oluştur|geliştir)"
        ]
        
        for pattern in project_name_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                special_entities["project_name"] = match.group(1).strip()
                break
        
        # Teknoloji stack çıkarma
        tech_stack = []
        tech_keywords = ["react", "vue", "angular", "django", "flask", "node", "express", "laravel"]
        for tech in tech_keywords:
            if tech in message.lower():
                tech_stack.append(tech)
        
        if tech_stack:
            special_entities["tech_stack"] = tech_stack
        
        # Urgency/Priority detection
        urgency_keywords = ["acil", "hızlı", "urgent", "asap", "quickly", "immediately"]
        if any(keyword in message.lower() for keyword in urgency_keywords):
            special_entities["urgency"] = "high"
        
        return special_entities
    
    def apply_context_awareness(self, 
                               intent: str, 
                               score: float, 
                               message: str, 
                               entities: Dict[str, Any]) -> Tuple[str, float]:
        """
        Context'e dayalı intent ayarlaması
        
        Önceki konuşmalara göre intent'i düzelt
        """
        
        # Son konuşmaları kontrol et
        recent_contexts = self.context_memory[-3:] if self.context_memory else []
        
        for context in recent_contexts:
            prev_intent = context.get("intent")
            
            # Eğer önceki intent proje oluşturma ise ve şimdi genel bir soru soruyorsa
            # muhtemelen proje ile ilgili detay soruyor
            if prev_intent == "project_creation" and intent == "general_query":
                if any(word in message.lower() for word in ["nasıl", "how", "ne", "what"]):
                    intent = "project_assistance"
                    score = min(score + 0.2, 1.0)
            
            # GitHub işlemi sonrası kod soruları
            elif prev_intent == "github_operation" and intent == "code_assistance":
                score = min(score + 0.1, 1.0)
            
            # Sistem kontrolü sonrası durumu sorguları
            elif prev_intent == "system_control" and "durum" in message.lower():
                intent = "system_status_query"
                score = min(score + 0.15, 1.0)
        
        # Entity-based adjustments
        if "github_repo" in entities or "branch_name" in entities:
            if intent in ["general_query", "information_query"]:
                intent = "github_operation"
                score = min(score + 0.2, 1.0)
        
        if "programming_language" in entities or "technology" in entities:
            if intent == "general_query":
                intent = "code_assistance"
                score = min(score + 0.15, 1.0)
        
        return intent, score
    
    def add_to_context_memory(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Context memory'ye yeni mesaj ekle"""
        context_entry = {
            "message": message,
            "timestamp": Path(__file__).stat().st_mtime,  # Basit timestamp
            "context": context or {}
        }
        
        self.context_memory.append(context_entry)
        
        # Memory limit'i kontrol et
        if len(self.context_memory) > self.max_context_memory:
            self.context_memory.pop(0)
    
    def get_context_summary(self) -> str:
        """Context'in özetini al"""
        if not self.context_memory:
            return "No previous context"
        
        recent_messages = [entry["message"] for entry in self.context_memory[-3:]]
        return " | ".join(recent_messages)
    
    def get_intent_confidence_explanation(self, intent: Intent) -> str:
        """Intent güven seviyesinin açıklaması"""
        confidence = intent.confidence
        
        if confidence >= 0.8:
            return "Çok yüksek güven - Kesin intent tespit edildi"
        elif confidence >= 0.6:
            return "Yüksek güven - Intent büyük olasılıkla doğru"
        elif confidence >= 0.4:
            return "Orta güven - Intent muhtemel ama alternatifler de olabilir"
        elif confidence >= 0.2:
            return "Düşük güven - Intent belirsiz, daha fazla bilgi gerekli"
        else:
            return "Çok düşük güven - Intent tespit edilemedi"
    
    def suggest_clarification_questions(self, intent: Intent) -> List[str]:
        """Belirsiz intent'ler için netleştirme soruları öner"""
        
        questions = []
        
        if intent.confidence < 0.5:
            if intent.name == "general_query":
                questions.extend([
                    "Hangi konuda yardım istiyorsunuz?",
                    "Bir proje mi geliştirmek istiyorsunuz?",
                    "Kod yazımı konusunda mı yardım gerekiyor?",
                    "GitHub işlemleri mi yapacaksınız?"
                ])
            
            elif intent.name == "project_creation":
                questions.extend([
                    "Hangi tür bir proje geliştirmek istiyorsunuz?",
                    "Hangi teknolojileri kullanmayı planlıyorsunuz?",
                    "Web sitesi mi, mobil uygulama mı, masaüstü programı mı?"
                ])
            
            elif intent.name == "code_assistance":
                questions.extend([
                    "Hangi programlama dili ile çalışıyorsunuz?",
                    "Specific bir hata mı var, yoksa genel yardım mı gerekiyor?",
                    "Kod optimize etme mi, debug mu, yoksa yeni kod yazma mı?"
                ])
        
        return questions[:3]  # En fazla 3 soru
    
    def get_suggested_actions(self, intent: Intent) -> List[str]:
        """Intent'e göre önerilen aksiyonlar"""
        
        actions = []
        
        if intent.name == "project_creation":
            actions.extend([
                "🏗️ Proje yapısı oluştur",
                "📂 GitHub repository aç", 
                "🤖 ChatGPT Codex ile kod yazdır",
                "⚙️ VS Code'da organize et"
            ])
        
        elif intent.name == "github_operation":
            actions.extend([
                "📁 Repository oluştur",
                "💾 Otomatik commit yap",
                "📤 Push işlemi gerçekleştir",
                "🌿 Yeni branch oluştur"
            ])
        
        elif intent.name == "code_assistance":
            actions.extend([
                "🤖 ChatGPT Codex'e sor",
                "🐛 Debug yardımı al",
                "⚡ Kod optimize et",
                "🧪 Test kodu yaz"
            ])
        
        elif intent.name == "system_control":
            actions.extend([
                "🚀 Matrix AI'yı başlat",
                "🤖 ChatGPT Codex aç",
                "📂 GitHub bağlan",
                "⚙️ VS Code Lite başlat"
            ])
        
        return actions

# Test fonksiyonu
def test_intent_detection():
    """Intent detection sistemini test et"""
    detector = MatrixAIIntentDetector()
    
    test_messages = [
        "Bir e-ticaret sitesi yap",
        "GitHub'a commit yap", 
        "Bu kodda hata var",
        "VS Code başlat",
        "React nedir?",
        "Python ile API geliştir",
        "Yeni branch oluştur main",
        "Chat GPT aç",
        "Nasıl yapabilirim?"
    ]
    
    print("🧠 Matrix AI Intent Detection Test")
    print("=" * 50)
    
    for message in test_messages:
        intent = detector.detect_intent(message)
        explanation = detector.get_intent_confidence_explanation(intent)
        
        print(f"\nMesaj: '{message}'")
        print(f"Intent: {intent.name}")
        print(f"Confidence: {intent.confidence:.2f}")
        print(f"Entities: {intent.entities}")
        print(f"Açıklama: {explanation}")
        
        if intent.confidence < 0.5:
            questions = detector.suggest_clarification_questions(intent)
            if questions:
                print(f"Netleştirme soruları: {questions}")

if __name__ == "__main__":
    test_intent_detection()
