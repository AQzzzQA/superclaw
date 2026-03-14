# Automation Scripts

Web automation, captcha solving, and data collection scripts.

## Scripts

### Web Automation
- **enhanced_login.py**: Enhanced login automation with session management
- **enhanced_website_login.py**: Website login with multi-factor authentication support
- **fixed_web_automation.py**: Fixed version of web automation with bug fixes
- **website_login.py**: Basic website login automation

### Captcha Solving
- **google_captcha_solver.py**: Google reCAPTCHA solver integration

### Data Collection
- **web_data_collector.py**: Automated web data collection and scraping
- **web_search_integration.py**: Integration with web search APIs
- **local_web_search.py**: Local web search implementation

## Usage

All scripts should be run from the workspace root:

```bash
python scripts/automation/enhanced_login.py
```

## Requirements

- Python 3.11+
- Selenium WebDriver
- BeautifulSoup4
- requests

## Notes

- Scripts may require `.env` configuration
- Captcha solving requires API keys
- Web automation may need headless browser setup
