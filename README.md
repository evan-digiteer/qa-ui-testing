# Visual UI Testing Framework

An automated UI testing framework for comparing visual differences between staging and production environments.

## Features

- Automated screenshot comparison between environments
- Configurable difference threshold
- Visual difference highlighting
- Date-organized screenshots
- Composite image generation showing differences
- Cross-browser support
- HTML test reports

## Project Structure

```
qa-ui-testing/
├── config/
│   └── settings.py         # Environment and threshold settings
├── pages/
│   ├── base_page.py       # Base page functionality
│   └── home_page.py       # Page-specific implementation
├── tests/
│   └── test_home_page.py  # Visual comparison tests
├── utils/
│   └── visual_test.py     # Screenshot and comparison utilities
├── screenshots/
│   └── YYYY-MM-DD/        # Date-organized screenshots
│       ├── current/       # Environment screenshots
│       └── diff/          # Difference images
├── conftest.py            # Test configuration
└── requirements.txt       # Python dependencies
```

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment URLs
Set your environment URLs either in `config/settings.py` or using environment variables:

```bash
export TEST_PROD_URL=https://www.your-website.com
export TEST_STAGE_URL=https://staging.your-website.com
```

### Difference Threshold
Configure how strict the visual comparison should be:

1. In settings.py:
```python
COMPARISON_THRESHOLD = 0.5  # 0.5% difference allowed
```

2. Or using environment variable:
```bash
export COMPARISON_THRESHOLD=1.0  # 1% difference allowed
```

Threshold guidelines:
- 0.1-0.5%: Very strict (pixel-perfect)
- 0.5-2.0%: Normal usage
- 2.0-5.0%: Lenient (dynamic content)
- >5.0%: Very lenient (major differences allowed)

## Running Tests

Run the visual comparison:
```bash
pytest tests/ -v
```

With custom threshold:
```bash
COMPARISON_THRESHOLD=2.0 pytest tests/ -v
```

With HTML report:
```bash
pytest tests/ -v --html=report.html
```

## Output

Tests generate three types of images in the `screenshots/YYYY-MM-DD/` directory:
1. Production screenshot
2. Staging screenshot
3. Difference visualization
4. Composite image showing all three side by side

## Interpreting Results

- Green test: No significant visual differences
- Red test: Differences exceed threshold
- Check the composite image (*_composite.png) to see:
  - Left: Production
  - Middle: Staging
  - Right: Differences (in red)

## Troubleshooting

- Different image dimensions: Check responsive design settings
- Black difference image: No differences detected
- Red areas: Visual differences highlighted
- High difference percentage: Adjust threshold or investigate changes