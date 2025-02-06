from PIL import Image, ImageChops, ImageDraw, ImageEnhance
import os
from datetime import datetime
import math
from config.settings import TestConfig

class VisualTest:
    def __init__(self):
        self.screenshot_dir = "screenshots"
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.timestamp = datetime.now().strftime("%H-%M-%S")
        
        # Create date-based directories
        self.today_dir = os.path.join(self.screenshot_dir, self.today)
        self.current_dir = os.path.join(self.today_dir, "current")
        self.diff_dir = os.path.join(self.today_dir, "diff")
        
        for dir_path in [self.current_dir, self.diff_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def capture_screenshot(self, driver, name):
        # Get original window size before changing it
        original_width = driver.get_window_size()['width']
        original_height = driver.get_window_size()['height']
        
        try:
            # Scroll to capture full page
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(TestConfig.SCREENSHOT_WIDTH, total_height)
            
            timestamped_name = f"{name}_{self.timestamp}"
            screenshot_path = os.path.join(self.current_dir, f"{timestamped_name}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Captured screenshot: {screenshot_path}")
            return screenshot_path
            
        finally:
            # Restore original window size
            driver.set_window_size(original_width, original_height)

    def get_diff_path(self, name):
        timestamped_name = f"{name}_{self.timestamp}"
        diff_path = os.path.join(self.diff_dir, f"{timestamped_name}.png")
        print(f"Difference path: {diff_path}")
        return diff_path

    @staticmethod
    def compare_screenshots(screenshot1_path, screenshot2_path, diff_path):
        print(f"\nComparing screenshots:")
        print(f"Image 1: {screenshot1_path}")
        print(f"Image 2: {screenshot2_path}")
        print(f"Diff will be saved to: {diff_path}")
        print(f"Using threshold: {TestConfig.COMPARISON_THRESHOLD}%")

        img1 = Image.open(screenshot1_path)
        img2 = Image.open(screenshot2_path)

        # Convert images to RGB mode
        img1 = img1.convert('RGB')
        img2 = img2.convert('RGB')

        # Get dimensions
        width1, height1 = img1.size
        width2, height2 = img2.size

        if width1 != width2:
            raise ValueError(f"Screenshots have different widths: {width1} vs {width2}")

        # Use the smaller height for comparison
        min_height = min(height1, height2)
        
        # Resize both images to match the smaller height while maintaining aspect ratio
        if height1 > min_height:
            img1 = img1.resize((width1, min_height), Image.Resampling.LANCZOS)
        if height2 > min_height:
            img2 = img2.resize((width2, min_height), Image.Resampling.LANCZOS)

        # Calculate difference
        diff = ImageChops.difference(img1, img2)
        
        # Enhance difference visibility
        diff = ImageEnhance.Brightness(diff).enhance(2.0)
        diff = ImageEnhance.Contrast(diff).enhance(2.0)
        
        # Initialize difference percentage
        diff_percentage = 0.0
        
        # Calculate difference percentage
        bbox = diff.getbbox()
        if bbox:
            # Create highlighted difference image and composite regardless of difference
            highlight = Image.new('RGB', img1.size, (0, 0, 0))
            draw = ImageDraw.Draw(highlight)
            
            # Compare pixels and highlight differences
            total_pixels = width1 * min_height
            different_pixels = 0
            
            for x in range(width1):
                for y in range(min_height):
                    r1, g1, b1 = img1.getpixel((x, y))
                    r2, g2, b2 = img2.getpixel((x, y))
                    pixel_diff = (abs(r1-r2) + abs(g1-g2) + abs(b1-b2)) / 765.0
                    if pixel_diff > (TestConfig.COMPARISON_THRESHOLD / 100.0):
                        draw.point((x, y), fill=(255, 0, 0))
                        different_pixels += 1

            # Calculate difference percentage
            diff_percentage = (different_pixels / total_pixels) * 100
            print(f"Difference percentage: {diff_percentage:.2f}%")
            print(f"Height difference: {abs(height1 - height2)} pixels")

            # Always save both diff and composite images
            highlight.save(diff_path)
            
            # Create and save composite image
            composite = Image.new('RGB', (width1 * 3, min_height))
            composite.paste(img1, (0, 0))
            composite.paste(img2, (width1, 0))
            composite.paste(highlight, (width1 * 2, 0))
            
            # Add labels to the composite image
            draw = ImageDraw.Draw(composite)
            font_size = 30
            draw.text((10, 10), "Production", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            draw.text((width1 + 10, 10), "Staging", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            draw.text((width1 * 2 + 10, 10), f"Diff ({diff_percentage:.1f}%)", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            
            composite_path = diff_path.replace('.png', '_composite.png')
            composite.save(composite_path)
            print(f"Composite image saved to: {composite_path}")

        # Return both the comparison result and difference percentage
        return (diff_percentage <= TestConfig.COMPARISON_THRESHOLD, diff_percentage)
