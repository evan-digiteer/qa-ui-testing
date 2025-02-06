import os

class TestConfig:
    ENVIRONMENTS = {
        "production": os.getenv('TEST_PROD_URL', 'https://www.prod.com'),
        "staging": os.getenv('TEST_STAGE_URL', 'https://www.staging.com')
    }
    
    # Browser settings
    SCREENSHOT_WIDTH = 1920
    SCREENSHOT_HEIGHT = 1080
    
    # Comparison settings
    COMPARISON_THRESHOLD = float(os.getenv('COMPARISON_THRESHOLD', '50.0'))  
