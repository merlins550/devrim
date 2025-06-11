import os
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from cookie_manager import CookieManager
from cryptography.fernet import Fernet


class DummyDriver:
    def __init__(self):
        self.cookies_added = []

    def get_cookies(self):
        return [{"name": "session", "value": "test"}]

    def get(self, url: str):
        pass

    def add_cookie(self, cookie):
        self.cookies_added.append(cookie)


def test_save_and_load(tmp_path: Path):
    pkl = tmp_path / "cookies.pkl"
    jsn = tmp_path / "cookies.json"
    cm = CookieManager(cookie_file=str(pkl), json_file=str(jsn))
    driver = DummyDriver()
    cm.save_cookies(driver)
    assert pkl.exists() and jsn.exists()

    driver2 = DummyDriver()
    cm.load_cookies(driver2)
    assert driver2.cookies_added[0]["name"] == "session"


def test_encrypted_save_and_load(tmp_path: Path, monkeypatch):
    pkl = tmp_path / "enc.pkl"
    jsn = tmp_path / "enc.json"
    key = Fernet.generate_key().decode()
    monkeypatch.setenv("COOKIE_ENCRYPTION_KEY", key)

    cm = CookieManager(cookie_file=str(pkl), json_file=str(jsn))
    driver = DummyDriver()
    cm.save_cookies(driver)
    assert pkl.exists() and jsn.exists()

    driver2 = DummyDriver()
    cm.load_cookies(driver2)
    assert driver2.cookies_added[0]["value"] == "test"
    monkeypatch.delenv("COOKIE_ENCRYPTION_KEY")
