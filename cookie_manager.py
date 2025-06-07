class CookieManager:
    """Utility class for loading and saving browser cookies.

    The file paths can be overridden with the environment variables
    ``COOKIE_FILE_PATH`` for the pickle file and ``COOKIE_JSON_PATH`` for a
    JSON formatted cookie list. If ``COOKIE_ENCRYPTION_KEY`` is set the
    cookie data will be encrypted with ``cryptography.Fernet`` for basic
    session protection.
    """

    def __init__(self, cookie_file: str = "cookies.pkl", json_file: str | None = None,
                 cookie_dir: str | None = None):
        import os

        self.cookie_file = os.getenv("COOKIE_FILE_PATH", cookie_file)
        self.json_file = os.getenv("COOKIE_JSON_PATH", json_file)
        self.cookie_dir = os.getenv("COOKIE_DIR", cookie_dir)
        self.enc_key = os.getenv("COOKIE_ENCRYPTION_KEY")

    def load_cookies(self, driver) -> None:
        """Load cookies from a pickle or JSON file into the WebDriver.

        If ``COOKIE_DIR`` is set, a random file from that directory will be used
        to allow simple cookie rotation for anti-detection.
        """
        import os
        import random
        import pickle
        import json
        from cryptography.fernet import Fernet

        cookie_file = self.cookie_file
        json_file = self.json_file

        if self.cookie_dir and os.path.isdir(self.cookie_dir):
            files = [f for f in os.listdir(self.cookie_dir)
                     if f.endswith('.pkl') or f.endswith('.json')]
            if files:
                chosen = os.path.join(self.cookie_dir, random.choice(files))
                if chosen.endswith('.json'):
                    json_file = chosen
                else:
                    cookie_file = chosen

        if json_file and os.path.exists(json_file):
            try:
                driver.get("https://www.google.com")
                data = open(json_file, "rb").read()
                if self.enc_key:
                    fernet = Fernet(self.enc_key)
                    data = fernet.decrypt(data)
                    cookies = json.loads(data.decode("utf-8"))
                else:
                    cookies = json.loads(data.decode("utf-8"))
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception:
                        continue
                return
            except Exception as exc:
                print(f"⚠️ Cookie JSON load error: {exc}")

        if os.path.exists(cookie_file):
            try:
                driver.get("https://www.google.com")
                data = open(cookie_file, "rb").read()
                if self.enc_key:
                    fernet = Fernet(self.enc_key)
                    data = fernet.decrypt(data)
                cookies = pickle.loads(data)
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception:
                        continue
            except Exception as exc:
                print(f"⚠️ Cookie load error: {exc}")

    def save_cookies(self, driver) -> None:
        """Save current cookies from the WebDriver to file."""
        import pickle
        import json

        try:
            cookies = driver.get_cookies()
            data = pickle.dumps(cookies)
            if self.enc_key:
                from cryptography.fernet import Fernet
                fernet = Fernet(self.enc_key)
                data = fernet.encrypt(data)
            with open(self.cookie_file, "wb") as f:
                f.write(data)

            if self.json_file:
                json_data = json.dumps(cookies).encode("utf-8")
                if self.enc_key:
                    fernet = Fernet(self.enc_key)
                    json_data = fernet.encrypt(json_data)
                with open(self.json_file, "wb") as f:
                    f.write(json_data)
        except Exception as exc:
            print(f"⚠️ Cookie save error: {exc}")
