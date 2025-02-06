import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import TestConfig

# Configure report directory
def pytest_configure(config):
    # Create reports directory with date-based structure
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")
    report_dir = os.path.join("reports", current_date)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # Set the HTML report path
    report_path = os.path.join(report_dir, f"report_{current_time}.html")
    config.option.htmlpath = report_path
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

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
