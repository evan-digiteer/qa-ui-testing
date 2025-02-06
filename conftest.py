import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import TestConfig

@pytest.fixture(scope="session")
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--window-size={TestConfig.SCREENSHOT_WIDTH},{TestConfig.SCREENSHOT_HEIGHT}')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Set fixed viewport size
    driver.set_window_size(TestConfig.SCREENSHOT_WIDTH, TestConfig.SCREENSHOT_HEIGHT)
    
    yield driver
    driver.quit()
