import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from utils.visual_test import VisualTest
from config.settings import TestConfig

class TestEnvironmentComparison:
    @pytest.fixture
    def visual_test(self):
        return VisualTest()

    def test_compare_environments(self, driver, visual_test):
        # Setup pages for both environments
        prod_page = HomePage(driver, TestConfig.ENVIRONMENTS["production"])
        stage_page = HomePage(driver, TestConfig.ENVIRONMENTS["staging"])
        
        # Capture production screenshot with better waiting
        prod_page.navigate_to()
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        time.sleep(3)  # Wait for any animations to complete
        prod_screenshot = visual_test.capture_screenshot(driver, "production_home")
        
        # Capture staging screenshot with better waiting
        stage_page.navigate_to()
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        time.sleep(3)  # Wait for any animations to complete
        stage_screenshot = visual_test.capture_screenshot(driver, "staging_home")
        
        # Compare the environments
        diff_path = visual_test.get_diff_path("env_comparison")
        
        comparison_result = visual_test.compare_screenshots(
            prod_screenshot,
            stage_screenshot,
            diff_path
        )
        
        if not comparison_result:
            pytest.fail(
                "Visual differences detected between environments.\n"
                f"Production: {prod_screenshot}\n"
                f"Staging: {stage_screenshot}\n"
                f"Difference: {diff_path}"
            )
