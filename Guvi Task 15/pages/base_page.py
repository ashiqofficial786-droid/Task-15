"""
pages/base_page.py
-------------------
Every Page Object in this framework inherits from BasePage. It centralises
the Explicit Wait + Expected Conditions logic so individual page classes
never call time.sleep() and never talk to WebDriverWait directly — they
just call self.wait_and_find(...) etc.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 15  # seconds — generous enough for the live demo site


class BasePage:
    """Common functionality shared by every Page Object."""

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_and_find(self, locator):
        """Explicit wait until the element is present, then return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_and_click(self, locator):
        """Explicit wait until the element is clickable, then click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def wait_and_visible(self, locator):
        """Explicit wait until the element is visible, then return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def is_element_visible(self, locator, timeout: int = 5) -> bool:
        """
        Non-fatal visibility check — used for things like the login error
        banner, which only appears for the "invalid credentials" scenarios.
        Returns False instead of raising if the element never shows up.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False
