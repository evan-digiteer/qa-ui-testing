import os

class TestConfig:
    ENVIRONMENTS = {
        "production": os.getenv('TEST_PROD_URL', 'https://www.marygracecafe.com'),
        "staging": os.getenv('TEST_STAGE_URL', 'https://mary-grace-v24-staging-127c94b75d7c.herokuapp.com')
    }
    
    # Browser settings
    SCREENSHOT_WIDTH = 1920
    SCREENSHOT_HEIGHT = 1080
    
    # Comparison settings
    COMPARISON_THRESHOLD = float(os.getenv('COMPARISON_THRESHOLD', '70.0'))  # Default 0.5% difference allowed
