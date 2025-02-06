from .base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.url = base_url
        
    def navigate_to(self):
        self.driver.get(self.url)
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
