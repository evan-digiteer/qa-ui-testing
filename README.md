# Visual UI Testing Framework

An automated UI testing framework for comparing visual differences between staging and production environments.

## Features

- Automated screenshot comparison between environments
- Configurable difference threshold
- Visual difference highlighting with composite images
- Date-organized screenshots and reports
- Cross-browser support
- Detailed HTML test reports

## Project Structure

```
qa-ui-testing/
├── assets/
│   └── style.css          # Custom report styling
├── config/
│   └── settings.py        # Environment and threshold settings
├── pages/
│   ├── base_page.py       # Base page functionality
│   └── home_page.py       # Page-specific implementation
├── tests/
│   └── test_home_page.py  # Visual comparison tests
├── utils/
│   └── visual_test.py     # Screenshot and comparison utilities
├── screenshots/           # Test artifacts
│   └── YYYY-MM-DD/
│       ├── current/      # Environment screenshots
│       └── diff/         # Difference visualizations
├── reports/              # Test reports
│   └── YYYY-MM-DD/      # Date-organized reports
├── conftest.py          # Test configuration
└── requirements.txt     # Python dependencies
```

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment URLs
Set your environment URLs either in `config/settings.py`:

### Difference Threshold
Configure how strict the visual comparison should be:

```bash
# In settings.py
COMPARISON_THRESHOLD = 50.0  # 50% difference allowed

# Or via environment variable
export COMPARISON_THRESHOLD=50.0
```

## Running Tests

Basic test run:
```bash
pytest
```

The framework will automatically:
- Create dated folders for screenshots and reports
- Generate timestamped files
- Save both success and failure comparisons
- Create HTML reports with visual results

## Output Structure

### Screenshots
```
screenshots/
└── 2024-02-06/
    ├── current/
    │   ├── production_home_14-30-45.png
    │   └── staging_home_14-30-45.png
    └── diff/
        ├── env_comparison_14-30-45.png
        └── env_comparison_14-30-45_composite.png
```

### Reports
```
reports/
└── 2024-02-06/
    └── report_14-30-45.html
```

## Interpreting Results

### Composite Images
Each comparison generates a composite image showing:
- Left: Production screenshot
- Middle: Staging screenshot
- Right: Differences highlighted in red

### Difference Percentage
- Test passes if difference is below threshold
- Difference percentage and threshold are shown in:
  - Console output
  - HTML report
  - Composite image labels

## Troubleshooting

- **Different image dimensions**: Check responsive design settings
- **Black difference image**: No differences detected
- **Red areas**: Visual differences highlighted
- **High difference percentage**: Adjust threshold or investigate changes
- **Missing screenshots**: Check screenshot directory permissions