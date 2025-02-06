import pytest
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from utils.visual_test import VisualTest
from config.settings import TestConfig

# Configure logging
LOGGER = logging.getLogger(__name__)

class TestEnvironmentComparison:
    @pytest.fixture
    def visual_test(self):
        return VisualTest()

    def test_compare_environments(self, driver, visual_test, caplog):
        # Set log level to INFO
        caplog.set_level(logging.INFO)
        
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
        
        comparison_result, diff_percentage = visual_test.compare_screenshots(
            prod_screenshot,
            stage_screenshot,
            diff_path
        )
        
        # Log results for both pass and fail cases
        result_message = (
            f"\nComparison Results:\n"
            f"Production: {prod_screenshot}\n"
            f"Staging: {stage_screenshot}\n"
            f"Difference: {diff_path}\n"
            f"Composite: {diff_path.replace('.png', '_composite.png')}\n"
            f"Difference Percentage: {diff_percentage:.2f}%\n"
            f"Threshold: {TestConfig.COMPARISON_THRESHOLD}%"
        )
        
        if not comparison_result:
            pytest.fail(f"Visual differences exceeded threshold.{result_message}")
        else:
            LOGGER.info(f"Visual comparison passed!{result_message}")
