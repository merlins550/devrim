import os
import sys
import pickle
from cryptography.fernet import Fernet

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from cookie_manager import CookieManager  # noqa: E402


class DummyDriver:
    def __init__(self):
        self._cookies = []

    def get(self, url):
        # In tests we don't need to actually navigate anywhere
        pass

    def add_cookie(self, cookie):
        self._cookies.append(cookie)

    def get_cookies(self):
        return list(self._cookies)


def test_save_and_load_cookies_no_encryption(tmp_path, monkeypatch):
    cookie_file = tmp_path / "cookies.pkl"
    json_file = tmp_path / "cookies.json"

    monkeypatch.delenv("COOKIE_ENCRYPTION_KEY", raising=False)
    manager = CookieManager(
        cookie_file=str(cookie_file),
        json_file=str(json_file)
    )

    driver = DummyDriver()
    driver.add_cookie({"name": "session", "value": "abc"})

    manager.save_cookies(driver)

    assert cookie_file.exists()
    assert json_file.exists()

    new_driver = DummyDriver()
    manager.load_cookies(new_driver)

    assert new_driver.get_cookies() == driver.get_cookies()


def test_save_and_load_cookies_with_encryption(tmp_path, monkeypatch):
    cookie_file = tmp_path / "cookies.pkl"
    json_file = tmp_path / "cookies.json"

    key = Fernet.generate_key()
    monkeypatch.setenv("COOKIE_ENCRYPTION_KEY", key.decode())
    manager = CookieManager(
        cookie_file=str(cookie_file),
        json_file=str(json_file)
    )

    driver = DummyDriver()
    cookies = [{"name": "session", "value": "secret"}]
    for c in cookies:
        driver.add_cookie(c)

    manager.save_cookies(driver)

    encrypted_pickle = cookie_file.read_bytes()
    assert encrypted_pickle != pickle.dumps(cookies)

    encrypted_json = json_file.read_bytes()
    assert encrypted_json != pickle.dumps(cookies)

    new_driver = DummyDriver()
    manager.load_cookies(new_driver)

    assert new_driver.get_cookies() == cookies
