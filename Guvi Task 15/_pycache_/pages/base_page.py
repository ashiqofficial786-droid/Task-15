from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class basepage():
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def click_element(self,locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self,locator,text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self,locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def open_url(self,url):
        self.driver.get(url)

    def get_page_title(self):
        return self.driver.title

    def is_element_displayed(self,locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()