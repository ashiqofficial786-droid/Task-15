"""
pages/login_page.py
--------------------
Page Object Model (POM) for the OrangeHRM demo Login page:
https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Only locators + page actions live here. No assertions and no test logic —
that stays in tests/test_login.py, keeping the framework's layers separate.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


class LoginPage(BasePage):
    # ---- Locators ---------------------------------------------------
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    # ---- Navigation ---------------------------------------------------
    def open(self):
        """Navigate to the login page."""
        self.driver.get(LOGIN_URL)
        # Confirm the page has actually loaded by waiting for the username field.
        self.wait_and_visible(self.USERNAME_INPUT)
        return self

    # ---- Actions ---------------------------------------------------
    def enter_username(self, username: str):
        field = self.wait_and_visible(self.USERNAME_INPUT)
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password: str):
        field = self.wait_and_visible(self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)
        return self

    def click_login(self):
        self.wait_and_click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """Convenience wrapper that performs a full login attempt."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    # ---- State checks ---------------------------------------------------
    def is_login_successful(self) -> bool:
        """
        A successful login lands on the Dashboard page, so we treat the
        presence of the Dashboard header as the source of truth. We do NOT
        use sleep() — this call itself is an Explicit Wait with Expected
        Conditions and simply returns False if the header never appears.
        """
        return self.is_element_visible(self.DASHBOARD_HEADER, timeout=10)

    def get_error_message(self) -> str:
        """Returns the text of the invalid-credentials error banner, if any."""
        if self.is_element_visible(self.ERROR_ALERT, timeout=5):
            return self.wait_and_visible(self.ERROR_ALERT).text
        return ""
