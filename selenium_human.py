import random
import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


def human_like_click(driver: WebDriver, element: WebElement) -> None:
    """Click an element in a human-like manner."""
    action = ActionChains(driver)
    action.move_to_element_with_offset(element, random.randint(-5, 5), random.randint(-5, 5))
    action.pause(random.uniform(0.2, 1.5))
    action.click()
    action.perform()


def human_typing(element: WebElement, text: str) -> None:
    """Type text into an element character by character with random delays."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.3))
