import os
import sys
import pickle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cookie_manager import CookieManager
from cryptography.fernet import Fernet


class DummyDriver:
    def __init__(self):
        self.cookies_added = []
        self.cookies = [
            {"name": "a", "value": "1"},
            {"name": "b", "value": "2"},
        ]
        self.visited = []

    def get(self, url):
        self.visited.append(url)

    def add_cookie(self, cookie):
        self.cookies_added.append(cookie)

    def get_cookies(self):
        return list(self.cookies)


def test_save_and_load_cookies_plain(tmp_path):
    cookie_file = tmp_path / "cookies.pkl"
    json_file = tmp_path / "cookies.json"
    driver = DummyDriver()
    cm = CookieManager(cookie_file=str(cookie_file), json_file=str(json_file))
    cm.save_cookies(driver)

    assert cookie_file.exists()
    assert json_file.exists()

    new_driver = DummyDriver()
    cm.load_cookies(new_driver)
    assert new_driver.cookies_added == driver.get_cookies()


def test_save_and_load_cookies_encrypted(tmp_path):
    key = Fernet.generate_key()
    os.environ["COOKIE_ENCRYPTION_KEY"] = key.decode()
    cookie_file = tmp_path / "enc_cookies.pkl"
    json_file = tmp_path / "enc_cookies.json"
    driver = DummyDriver()
    cm = CookieManager(cookie_file=str(cookie_file), json_file=str(json_file))
    cm.save_cookies(driver)

    # Ensure data is encrypted in the pickle file
    with open(cookie_file, "rb") as f:
        raw = f.read()
    assert raw != pickle.dumps(driver.get_cookies())

    fernet = Fernet(key)
    decrypted = pickle.loads(fernet.decrypt(raw))
    assert decrypted == driver.get_cookies()

    new_driver = DummyDriver()
    cm.load_cookies(new_driver)
    assert new_driver.cookies_added == driver.get_cookies()

    del os.environ["COOKIE_ENCRYPTION_KEY"]
