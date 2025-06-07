#!/usr/bin/env python3
"""
SmolAgents Git Power - Otomatik Git/GitHub İşlemleri
Matrix AI Desktop Assistant için Git otomasyonu modülü

Bu modül:
- Otomatik repository creation
- Intelligent commit messages
- Branch management
- CI/CD pipeline setup
- Pull request automation
"""

import os
import subprocess
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

try:
    from smolagents_integration import SmolAgentsIntegration
except Exception:  # pragma: no cover - optional
    SmolAgentsIntegration = None

class SmolAgentsGitPower:
    """
    SmolAgents Git Power - Akıllı Git Otomasyonu
    
    Bu sınıf Git ve GitHub işlemlerini tamamen otomatize eder:
    - Repository oluşturma ve klonlama
    - Akıllı commit mesajları
    - Otomatik branch yönetimi
    - CI/CD pipeline kurulumu
    - Pull request otomasyonu
    """
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.logger = logging.getLogger("SmolAgentsGit")
        
        # GitHub API base URL
        self.github_api = "https://api.github.com"
        
        # Git konfigürasyonu
        self.git_config = self.load_git_config()
        
        self.logger.info("SmolAgents Git Power initialized")
    
    def load_git_config(self) -> Dict[str, Any]:
        """Git konfigürasyonunu yükle"""
        config = {
            "auto_commit": True,
            "smart_branch_naming": True,
            "auto_push": True,
            "commit_message_ai": True,
            "branch_prefix": "feature/",
            "default_branch": "main"
        }
        
        # Global git config'i oku
        try:
            user_name = subprocess.check_output(
                ["git", "config", "--global", "user.name"], 
                text=True
            ).strip()
            user_email = subprocess.check_output(
                ["git", "config", "--global", "user.email"], 
                text=True
            ).strip()
            
            config.update({
                "user_name": user_name,
                "user_email": user_email
            })
        except subprocess.CalledProcessError:
            self.logger.warning("Git config bulunamadı - varsayılan değerler kullanılacak")
        
        return config
    
    def setup_git_if_needed(self, repo_path: str = "."):
        """Gerekirse git repository'yi başlat"""
        repo_path = Path(repo_path).resolve()
        git_dir = repo_path / ".git"
        
        if not git_dir.exists():
            self.logger.info(f"Git repository başlatılıyor: {repo_path}")
            
            try:
                # Git init
                subprocess.run(
                    ["git", "init"], 
                    cwd=repo_path, 
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                # Initial commit
                subprocess.run(
                    ["git", "add", "."], 
                    cwd=repo_path, 
                    check=True
                )
                
                initial_commit = self.generate_commit_message("Initial commit - Matrix AI Project Setup")
                subprocess.run(
                    ["git", "commit", "-m", initial_commit], 
                    cwd=repo_path, 
                    check=True
                )
                
                self.logger.info("Git repository başarıyla başlatıldı")
                return True
                
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Git init hatası: {e}")
                return False
        
        return True
    
    def create_github_repository(self, 
                                repo_name: str, 
                                description: str = "",
                                private: bool = False,
                                auto_init: bool = False) -> Dict[str, Any]:
        """
        GitHub'da yeni repository oluştur
        
        Args:
            repo_name: Repository adı
            description: Açıklama
            private: Private repository mi?
            auto_init: README ile başlat mı?
        
        Returns:
            Repository bilgileri
        """
        
        if not self.github_token:
            self.logger.error("GitHub token gerekli!")
            return {"error": "GitHub token bulunamadı"}
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
            "gitignore_template": "Python" if auto_init else None
        }
        
        try:
            response = requests.post(
                f"{self.github_api}/user/repos",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                repo_info = response.json()
                self.logger.info(f"GitHub repository oluşturuldu: {repo_info['html_url']}")
                return {
                    "success": True,
                    "repo_url": repo_info["html_url"],
                    "clone_url": repo_info["clone_url"],
                    "ssh_url": repo_info["ssh_url"],
                    "repo_info": repo_info
                }
            else:
                error_msg = response.json().get("message", "Bilinmeyen hata")
                self.logger.error(f"GitHub repository oluşturma hatası: {error_msg}")
                return {"error": error_msg}
                
        except requests.RequestException as e:
            self.logger.error(f"GitHub API hatası: {e}")
            return {"error": str(e)}
    
    def generate_commit_message(self, context: str = "") -> str:
        """
        Akıllı commit mesajı oluştur
        
        Args:
            context: Commit bağlamı
            
        Returns:
            Oluşturulan commit mesajı
        """
        
        diff_output = ""
        if not context:
            try:
                diff_output = subprocess.check_output(
                    ["git", "diff", "--cached"],
                    text=True
                ).strip()
            except subprocess.CalledProcessError:
                diff_output = ""

        if SmolAgentsIntegration and os.getenv("USE_SMOLAGENTS", "false").lower() == "true" and diff_output:
            try:
                agent = SmolAgentsIntegration()
                context = agent.generate_commit_message(diff_output)
            except Exception as e:
                self.logger.error(f"SmolAgents integration failed: {e}")

        if not context:
            if diff_output:
                lines = diff_output.split('\n')
                added_files = [l for l in lines if l.startswith('+') and not l.startswith('+++')]
                removed_files = [l for l in lines if l.startswith('-') and not l.startswith('---')]
                if added_files and not removed_files:
                    context = f"Add {len(added_files)} lines"
                elif removed_files and not added_files:
                    context = f"Remove {len(removed_files)} lines"
                else:
                    context = "Update project files"
            else:
                context = "Update project"
        
        # Emoji'li ve semantik commit mesajı
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        semantic_prefixes = {
            "add": "✨ feat:",
            "update": "🔧 fix:",
            "remove": "🗑️ remove:",
            "fix": "🐛 fix:",
            "docs": "📚 docs:",
            "style": "💄 style:",
            "refactor": "♻️ refactor:",
            "test": "🧪 test:",
            "chore": "🔧 chore:"
        }
        
        # Context'e göre prefix seç
        prefix = "✨ feat:"
        for key, value in semantic_prefixes.items():
            if key.lower() in context.lower():
                prefix = value
                break
        
        commit_message = f"{prefix} {context}"
        
        # Matrix AI imzası ekle
        commit_message += f"\n\n🤖 Generated by Matrix AI Desktop Assistant\n⏰ {timestamp}"
        
        return commit_message
    
    def auto_commit(self, repo_path: str = ".", commit_message: str = "") -> Dict[str, Any]:
        """
        Otomatik commit yap
        
        Args:
            repo_path: Repository yolu
            commit_message: Özel commit mesajı (opsiyonel)
            
        Returns:
            Commit sonucu
        """
        
        repo_path = Path(repo_path).resolve()
        
        try:
            # Değişiklikleri kontrol et
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                text=True
            ).strip()
            
            if not status_output:
                return {"message": "Commit edilecek değişiklik yok"}
            
            # Tüm değişiklikleri stage'e al
            subprocess.run(
                ["git", "add", "."],
                cwd=repo_path,
                check=True
            )
            
            # Commit mesajını oluştur
            if not commit_message:
                commit_message = self.generate_commit_message()
            
            # Commit yap
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_path,
                check=True
            )
            
            self.logger.info(f"Auto commit başarılı: {commit_message}")
            
            # Auto push varsa push yap
            if self.git_config.get("auto_push", False):
                push_result = self.push_to_remote(repo_path)
                return {
                    "success": True,
                    "commit_message": commit_message,
                    "push_result": push_result
                }
            
            return {
                "success": True,
                "commit_message": commit_message
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Auto commit hatası: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def create_branch(self, branch_name: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Yeni branch oluştur ve switch yap
        
        Args:
            branch_name: Branch adı
            repo_path: Repository yolu
            
        Returns:
            Branch oluşturma sonucu
        """
        
        repo_path = Path(repo_path).resolve()
        
        # Smart branch naming
        if self.git_config.get("smart_branch_naming", True):
            prefix = self.git_config.get("branch_prefix", "feature/")
            if not branch_name.startswith(prefix):
                # Branch adını temizle ve prefix ekle
                clean_name = branch_name.lower().replace(" ", "-").replace("_", "-")
                branch_name = f"{prefix}{clean_name}"
        
        try:
            # Branch oluştur ve switch yap
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=repo_path,
                check=True
            )
            
            self.logger.info(f"Branch oluşturuldu ve switch yapıldı: {branch_name}")
            return {
                "success": True,
                "branch_name": branch_name,
                "message": f"Branch '{branch_name}' oluşturuldu"
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Branch oluşturma hatası: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def push_to_remote(self, repo_path: str = ".", branch: str = "") -> Dict[str, Any]:
        """
        Remote repository'ye push yap
        
        Args:
            repo_path: Repository yolu
            branch: Branch adı (boşsa current branch)
            
        Returns:
            Push sonucu
        """
        
        repo_path = Path(repo_path).resolve()
        
        try:
            # Current branch'i al
            if not branch:
                branch = subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=repo_path,
                    text=True
                ).strip()
            
            # Remote'u kontrol et
            try:
                subprocess.check_output(
                    ["git", "remote", "get-url", "origin"],
                    cwd=repo_path,
                    text=True
                )
            except subprocess.CalledProcessError:
                return {"error": "Remote 'origin' tanımlanmamış"}
            
            # Push yap
            subprocess.run(
                ["git", "push", "-u", "origin", branch],
                cwd=repo_path,
                check=True
            )
            
            self.logger.info(f"Push başarılı: {branch}")
            return {
                "success": True,
                "branch": branch,
                "message": f"'{branch}' branch'i başarıyla push edildi"
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Push hatası: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def setup_remote_origin(self, repo_url: str, repo_path: str = ".") -> Dict[str, Any]:
        """
        Remote origin'i ayarla
        
        Args:
            repo_url: GitHub repository URL'i
            repo_path: Local repository yolu
            
        Returns:
            Setup sonucu
        """
        
        repo_path = Path(repo_path).resolve()
        
        try:
            # Mevcut remote'u kontrol et
            try:
                current_remote = subprocess.check_output(
                    ["git", "remote", "get-url", "origin"],
                    cwd=repo_path,
                    text=True
                ).strip()
                
                if current_remote == repo_url:
                    return {"message": "Remote origin zaten doğru şekilde ayarlanmış"}
                else:
                    # Remote'u güncelle
                    subprocess.run(
                        ["git", "remote", "set-url", "origin", repo_url],
                        cwd=repo_path,
                        check=True
                    )
                    
            except subprocess.CalledProcessError:
                # Remote yoksa ekle
                subprocess.run(
                    ["git", "remote", "add", "origin", repo_url],
                    cwd=repo_path,
                    check=True
                )
            
            self.logger.info(f"Remote origin ayarlandı: {repo_url}")
            return {
                "success": True,
                "remote_url": repo_url,
                "message": "Remote origin başarıyla ayarlandı"
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Remote setup hatası: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def create_pull_request(self, 
                           title: str,
                           body: str = "",
                           head_branch: str = "",
                           base_branch: str = "main",
                           repo_path: str = ".") -> Dict[str, Any]:
        """
        Pull request oluştur
        
        Args:
            title: PR başlığı
            body: PR açıklaması
            head_branch: Kaynak branch (boşsa current)
            base_branch: Hedef branch
            repo_path: Repository yolu
            
        Returns:
            PR oluşturma sonucu
        """
        
        if not self.github_token:
            return {"error": "GitHub token gerekli"}
        
        repo_path = Path(repo_path).resolve()
        
        try:
            # Current branch'i al
            if not head_branch:
                head_branch = subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=repo_path,
                    text=True
                ).strip()
            
            # Repository bilgisini al
            remote_url = subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                cwd=repo_path,
                text=True
            ).strip()
            
            # GitHub repo bilgisini parse et
            if "github.com" in remote_url:
                # SSH veya HTTPS formatından repo bilgisini çıkar
                if remote_url.startswith("git@"):
                    # git@github.com:user/repo.git
                    repo_part = remote_url.split(":")[-1].replace(".git", "")
                else:
                    # https://github.com/user/repo.git
                    repo_part = remote_url.split("github.com/")[-1].replace(".git", "")
                
                owner, repo_name = repo_part.split("/")
                
                # PR oluştur
                headers = {
                    "Authorization": f"token {self.github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                
                data = {
                    "title": title,
                    "body": body,
                    "head": head_branch,
                    "base": base_branch
                }
                
                response = requests.post(
                    f"{self.github_api}/repos/{owner}/{repo_name}/pulls",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 201:
                    pr_info = response.json()
                    self.logger.info(f"Pull request oluşturuldu: {pr_info['html_url']}")
                    return {
                        "success": True,
                        "pr_url": pr_info["html_url"],
                        "pr_number": pr_info["number"],
                        "pr_info": pr_info
                    }
                else:
                    error_msg = response.json().get("message", "Bilinmeyen hata")
                    return {"error": f"PR oluşturma hatası: {error_msg}"}
            
            else:
                return {"error": "Bu bir GitHub repository'si değil"}
                
        except Exception as e:
            error_msg = f"Pull request hatası: {e}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def full_project_setup(self, 
                          project_name: str,
                          project_description: str = "",
                          project_path: str = ".",
                          create_github_repo: bool = True) -> Dict[str, Any]:
        """
        Tam proje setup'ı (Git + GitHub)
        
        Args:
            project_name: Proje adı
            project_description: Proje açıklaması
            project_path: Proje yolu
            create_github_repo: GitHub repo oluştur mu?
            
        Returns:
            Setup sonucu
        """
        
        self.logger.info(f"Full project setup başlıyor: {project_name}")
        
        results = {
            "project_name": project_name,
            "steps": []
        }
        
        try:
            # 1. Git repository setup
            self.logger.info("Step 1: Git repository setup")
            git_setup = self.setup_git_if_needed(project_path)
            results["steps"].append({
                "step": "git_init",
                "success": git_setup,
                "message": "Git repository başlatıldı" if git_setup else "Git setup hatası"
            })
            
            # 2. GitHub repository oluştur
            if create_github_repo:
                self.logger.info("Step 2: GitHub repository creation")
                github_result = self.create_github_repository(
                    repo_name=project_name,
                    description=project_description
                )
                
                if github_result.get("success"):
                    results["steps"].append({
                        "step": "github_create",
                        "success": True,
                        "message": "GitHub repository oluşturuldu",
                        "repo_url": github_result["repo_url"]
                    })
                    
                    # 3. Remote origin setup
                    self.logger.info("Step 3: Remote origin setup")
                    remote_result = self.setup_remote_origin(
                        github_result["clone_url"], 
                        project_path
                    )
                    results["steps"].append({
                        "step": "remote_setup",
                        "success": remote_result.get("success", False),
                        "message": remote_result.get("message", "Remote setup hatası")
                    })
                    
                    # 4. Initial push
                    self.logger.info("Step 4: Initial push")
                    push_result = self.push_to_remote(project_path)
                    results["steps"].append({
                        "step": "initial_push",
                        "success": push_result.get("success", False),
                        "message": push_result.get("message", "Push hatası")
                    })
                    
                else:
                    results["steps"].append({
                        "step": "github_create",
                        "success": False,
                        "message": github_result.get("error", "GitHub repo oluşturma hatası")
                    })
            
            # Başarı durumunu kontrol et
            success_count = sum(1 for step in results["steps"] if step["success"])
            total_steps = len(results["steps"])
            
            results["overall_success"] = success_count == total_steps
            results["success_rate"] = f"{success_count}/{total_steps}"
            
            if results["overall_success"]:
                self.logger.info(f"Full project setup tamamlandı: {project_name}")
            else:
                self.logger.warning(f"Project setup kısmen başarılı: {results['success_rate']}")
            
            return results
            
        except Exception as e:
            error_msg = f"Full project setup hatası: {e}"
            self.logger.error(error_msg)
            results["error"] = error_msg
            results["overall_success"] = False
            return results
    
    def get_repository_status(self, repo_path: str = ".") -> Dict[str, Any]:
        """
        Repository durumunu al
        
        Args:
            repo_path: Repository yolu
            
        Returns:
            Repository durum bilgileri
        """
        
        repo_path = Path(repo_path).resolve()
        status = {}
        
        try:
            # Current branch
            current_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path,
                text=True
            ).strip()
            status["current_branch"] = current_branch
            
            # Status
            git_status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                text=True
            ).strip()
            
            status["has_changes"] = bool(git_status)
            status["changes_count"] = len(git_status.split('\n')) if git_status else 0
            
            # Remote info
            try:
                remote_url = subprocess.check_output(
                    ["git", "remote", "get-url", "origin"],
                    cwd=repo_path,
                    text=True
                ).strip()
                status["remote_url"] = remote_url
                status["has_remote"] = True
            except subprocess.CalledProcessError:
                status["has_remote"] = False
            
            # Last commit
            try:
                last_commit = subprocess.check_output(
                    ["git", "log", "-1", "--pretty=format:%h - %s (%cr)"],
                    cwd=repo_path,
                    text=True
                ).strip()
                status["last_commit"] = last_commit
            except subprocess.CalledProcessError:
                status["last_commit"] = "Commit yok"
            
            status["success"] = True
            
        except subprocess.CalledProcessError as e:
            status["error"] = f"Git status hatası: {e}"
            status["success"] = False
        
        return status

# Test fonksiyonu
def test_smolagents_git():
    """SmolAgents Git Power'ı test et"""
    git_agent = SmolAgentsGitPower()
    
    print("🐬 SmolAgents Git Power Test")
    print("=" * 40)
    
    # Repository status
    status = git_agent.get_repository_status()
    print(f"Repository Status: {status}")
    
    # Commit message generation
    commit_msg = git_agent.generate_commit_message("Test SmolAgents integration")
    print(f"Generated Commit Message: {commit_msg}")

if __name__ == "__main__":
    test_smolagents_git()
