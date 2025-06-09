"""Simple DOM interaction utilities for Selenium WebDriver."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


def find_element(driver: WebDriver, selector: str, timeout: int = 10):
    """Return the first element matching the CSS selector within timeout."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def click(driver: WebDriver, selector: str, timeout: int = 10) -> None:
    """Wait for an element then click it."""
    elem = find_element(driver, selector, timeout)
    elem.click()


def type_text(driver: WebDriver, selector: str, text: str, timeout: int = 10) -> None:
    """Type text into the specified element."""
    elem = find_element(driver, selector, timeout)
    elem.clear()
    elem.send_keys(text)
