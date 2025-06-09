import os
import unittest
from unittest.mock import MagicMock
from cookie_manager import CookieManager

class TestCookieManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = 'test_cookies.pkl'
        self.manager = CookieManager(self.temp_file)
        self.driver = MagicMock()
        self.driver.get_cookies.return_value = [{'name': 'a', 'value': '1'}]

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load(self):
        self.manager.save_cookies(self.driver)
        self.assertTrue(os.path.exists(self.temp_file))
        self.driver.get.return_value = None
        self.manager.load_cookies(self.driver)
        self.driver.add_cookie.assert_called()

if __name__ == '__main__':
    unittest.main()
