from selenium.webdriver.common.by import By
from GUVI_Task15.pages.base_page import basepage

class LoginPage(basepage):

    username_text = (By.XPATH,"//input[@name='username']")
    passcode = (By.XPATH,"//input[@name='password']")
    login_btn = (By.XPATH,"//button[@type='submit']")

    def login(self,username,password):

        self.enter_text(self.username_text,username)
        self.enter_text(self.passcode,password)
        self.click_element(self.login_btn)

    def is_username_displayed(self):

        return self.is_element_displayed(self.username_text)

    def is_password_displayed(self):

         return self.is_element_displayed(self.passcode)

    def is_login_button_displayed(self):
        return self.is_element_displayed(self.login_btn)