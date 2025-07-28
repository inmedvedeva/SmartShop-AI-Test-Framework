# SmartShop AI Test Framework

🚀 **Comprehensive test automation framework with AI integration for Automation QA Engineer position**

A modern, AI-powered test automation framework built with Python, featuring OpenAI integration, comprehensive test coverage, and CI/CD pipeline. This project demonstrates advanced testing capabilities including UI automation, API testing, visual testing, and AI-powered test data generation.

## 🎯 Project Overview

This framework showcases the skills and technologies required for an Automation QA Engineer position:

- **Python 3.12+** with modern testing libraries
- **AI Integration** using OpenAI GPT-3.5-turbo for test data generation
- **Multi-browser testing** with Selenium and Playwright
- **Mobile Testing** with Playwright for iOS and Android devices
- **API Testing** with comprehensive REST API coverage
- **Visual Testing** using Applitools and OpenCV
- **CI/CD Pipeline** with GitHub Actions
- **Containerization** with Docker
- **Comprehensive Reporting** with Allure

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Git
- Chrome/Firefox browser
- OpenAI API key (optional - falls back to Faker)

### One-Command Setup
```bash
git clone <repository-url>
cd SmartShop-AI-Test-Framework
./quick_start.sh
```

### Manual Setup
```bash
# Clone and setup
git clone <repository-url>
cd SmartShop-AI-Test-Framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/environments/env_example.txt .env
# Edit .env with your settings

# Setup Applitools (Optional)
python scripts/setup_applitools.py

# Start mock API server
python -m src.api.start_mock_api
```

## 🏗️ Project Structure

```
SmartShop-AI-Test-Framework/
├── src/                    # Main source code (framework logic)
│   ├── core/               # Core utilities, config, logging, constants, helpers
│   ├── api/                # API clients and mock server
│   ├── ui/                 # UI helpers and page objects
│   └── version.py          # Version info
├── tests/                  # Test suites (organized by type)
│   ├── api/                # API tests
│   ├── ui/                 # UI tests
│   ├── e2e/                # End-to-end tests
│   ├── integration/        # Integration tests
│   ├── performance/        # Performance tests
│   ├── regression/         # Regression tests
│   ├── smoke/              # Smoke tests
│   └── unit/               # Unit tests
├── config/                 # Environment and secret configs
│   ├── environments/       # Environment-specific configs (.env, etc.)
│   └── secrets/            # Secret files (not in VCS)
├── resources/              # Test data, locators, images
│   ├── test_data/          # JSON, CSV, or other test data
│   ├── locators/           # UI locators (YAML/JSON)
│   └── images/             # Reference images for visual testing
├── reports/                # Test and tool reports
│   ├── screenshots/        # Screenshots (failures, baselines, diffs)
│   └── allure-report/      # Allure HTML reports
├── scripts/                # Helper scripts
│   ├── setup/              # Setup/installation scripts
│   ├── dev/                # Developer utilities, demos
│   └── ci/                 # CI/CD helper scripts
├── documentation/          # Documentation organized by topics
├── .github/workflows/      # GitHub Actions workflows
├── docker-compose.yml      # Docker Compose config
├── README.md               # Main documentation (this file)
├── documentation/security/  # Security documentation
├── documentation/deployment/ # Deployment guides
└── ...                     # Other project files
```

**Key points:**
- All main code is under `src/` for clarity and import hygiene.
- Tests are organized by type for easy navigation and scalability.
- Configs, resources, and reports are separated for maintainability.
- Scripts are grouped by purpose (setup, dev, CI).
- Documentation is in `documentation/` and main info in `README.md`.

## 🧪 Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/ui/          # UI tests
pytest tests/api/         # API tests
pytest tests/unit/        # Unit tests
pytest tests/mobile/      # Mobile tests
pytest tests/visual/      # Visual tests
pytest tests/test_basic.py # Basic functionality tests
```

# Run with browser specification
pytest --browser=chrome
pytest --browser=firefox

# Run with verbose output
```

### Mobile Testing with Playwright

The framework includes comprehensive mobile testing capabilities using Playwright:

#### Quick Mobile Test Setup
```bash
# Install Playwright browsers
python scripts/run_mobile_tests.py --install-browsers

# Run mobile tests on specific device
python scripts/run_mobile_tests.py --device IPHONE_12 --browser chromium

# Run cross-browser mobile tests
python scripts/run_mobile_tests.py --device GALAXY_S23 --cross-browser

# Run cross-device compatibility tests
python scripts/run_mobile_tests.py --cross-device

# Run specific mobile test scenarios
python scripts/run_mobile_tests.py --scenarios responsive gestures performance
```

#### Supported Mobile Devices
- **iOS Phones**: iPhone 12, iPhone 13, iPhone 14, iPhone 15 series
- **iOS Tablets**: iPad Air, iPad Pro 11", iPad Pro 12.9"
- **Android Phones**: Galaxy S20-S24, Pixel 5-8
- **Android Tablets**: Galaxy Tab S7-S9, Pixel Tablet

#### Mobile Test Features
- **Responsive Design Testing** - Automatic breakpoint validation
- **Touch Gestures** - Tap, swipe, pinch, scroll testing
- **Orientation Testing** - Portrait and landscape validation
- **Mobile Performance** - Load time and network request monitoring
- **Accessibility Testing** - Mobile accessibility compliance
- **Cross-Browser Testing** - Chromium, Firefox, WebKit support
- **Cross-Device Testing** - Automated compatibility validation

#### Mobile Test Examples
```python
# Test responsive design
def test_mobile_responsive_design(self):
    self.navigate_to("https://automationexercise.com/")
    responsive_results = self.check_responsive_design()
    assert all(responsive_results.values()), "Responsive design issues found"

# Test mobile gestures
def test_mobile_gestures(self):
    gesture_results = self.test_mobile_gestures()
    assert gesture_results["tap"], "Tap gesture failed"
    assert gesture_results["swipe"], "Swipe gesture failed"

# Test orientation changes
def test_mobile_orientation(self):
    self.rotate_to_landscape()
    assert self.get_viewport_size()["width"] > self.get_viewport_size()["height"]
    self.rotate_to_portrait()
    assert self.get_viewport_size()["height"] > self.get_viewport_size()["width"]
```

## 🎨 Visual Testing with Applitools

### Setup
```bash
# Get API key from https://applitools.com/
python scripts/setup_applitools.py

# Run visual tests
pytest tests/visual/

# Demo without API key
python examples/applitools_demo_simple.py
```

### Features
- **AI-powered visual regression detection**
- **Automatic baseline management**
- **Cross-browser visual testing**
- **Responsive design validation**
- **Region-specific visual checks**
- **Smart change detection** (ignores minor changes)

### Visual Test Examples
```python
# Basic visual check
def test_home_page_visual(self):
    self.home_page.open_home_page()
    result = self.visual_tester.check_page_layout("home_page", self.driver)
    assert result['status'] in ['passed', 'baseline_created']

# Region-specific check
def test_header_visual(self):
    header_region = (x, y, width, height)
    result = self.visual_tester.check_page_layout("header", self.driver, region=header_region)
    assert result['status'] in ['passed', 'baseline_created']

# Responsive visual testing
def test_responsive_visual(self):
    self.driver.set_window_size(375, 667)  # Mobile
    result = self.visual_tester.check_page_layout("mobile_home", self.driver)
    assert result['status'] in ['passed', 'baseline_created']
```

### Report Management

Reports are automatically organized and cleaned up to prevent repository bloat:

#### Report Organization
- **Timestamped directories**: Each test run creates a timestamped directory (`YYYYMMDD_HHMMSS`)
- **Latest symlink**: Always points to the most recent report
- **JSON format**: Machine-readable results for automation
- **Markdown summary**: Human-readable summary

#### Cleanup Commands
```bash
# Show disk usage
python scripts/cleanup_reports.py --disk-usage

# Dry run (see what would be cleaned)
python scripts/cleanup_reports.py --dry-run

# Clean up reports older than 7 days (default)
python scripts/cleanup_reports.py

# Clean up reports older than 30 days
python scripts/cleanup_reports.py --days 30
```

#### Report Locations
- **Latest report**: `reports/mobile/latest/`
- **All reports**: `reports/mobile/YYYYMMDD_HHMMSS/`
- **Screenshots**: `reports/screenshots/`
- **Logs**: `logs/`
pytest -v

# un tests + venv
source venv/bin/activate && pytest tests/ui/test_automation_exercise_home_page.py --maxfail=5 --disable-warnings -v
```

### Test Categories
- **UI Tests**: Selenium/Playwright-based UI automation
- **API Tests**: REST API testing with mock server
- **Unit Tests**: Core functionality testing
- **Integration Tests**: End-to-end scenarios
- **Performance Tests**: Load and response time testing
- **Visual Tests**: Visual regression testing

## 🤖 AI Features

### OpenAI Integration
The framework uses OpenAI for generating realistic test data:

```python
from src.core.utils.ai_data_generator import AIDataGenerator

ai_generator = AIDataGenerator()

# Generate user profiles
user = ai_generator.generate_user_profile("customer")

# Generate product catalogs
products = ai_generator.generate_product_catalog("electronics", 5)

# Generate test scenarios
scenarios = ai_generator.generate_test_scenarios("search")
```

### Applitools Visual Testing
The framework integrates with Applitools Eyes for AI-powered visual testing:

```python
from src.core.utils.visual_testing import VisualTester

visual_tester = VisualTester()

# Basic visual check
result = visual_tester.check_page_layout("home_page", driver)

# Region-specific check
result = visual_tester.check_page_layout("header", driver, region=(x, y, width, height))

# Responsive testing
driver.set_window_size(375, 667)  # Mobile
result = visual_tester.check_page_layout("mobile_home", driver)
```

### Smart Fallback System
If OpenAI is unavailable, automatically falls back to Faker:
- **Geographic restrictions** (403 errors)
- **Invalid API keys** (401 errors)
- **Rate limiting** (429 errors)
- **Network issues** (timeouts)

### Visual Testing Fallback
If Applitools is unavailable, falls back to basic image comparison:
- **No API key** - Uses OpenCV for pixel comparison
- **Network issues** - Local screenshot comparison
- **Package not installed** - Basic screenshot capture

### Configuration
```bash
# In .env file
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000
OPENAI_TIMEOUT=30

APPLITOOLS_API_KEY=your-applitools-api-key-here
APPLITOOLS_APP_NAME=SmartShop_AI_Tests
```

## 🌐 Demo Websites

The framework tests against real demo websites:
- **https://automationexercise.com/** - E-commerce automation
- **https://the-internet.herokuapp.com/** - UI automation examples
- **https://demo.nopcommerce.com/** - E-commerce platform

## 📊 Reporting

### Allure Reports
```bash
# Generate reports
pytest --alluredir=reports/allure-results

# View reports
allure serve reports/allure-results

# Generate HTML
allure generate reports/allure-results -o reports/allure-report --clean
```

### Screenshots
Automatically saved to `reports/screenshots/` on test failures.

## 🔄 CI/CD Pipeline

### GitHub Actions Features
- **Multi-browser testing** (Chrome, Firefox)
- **Parallel execution** with matrix strategy
- **Automatic reporting** with Allure
- **Security scanning** with Bandit and Safety
- **Code quality checks** with Black, isort, flake8, mypy
- **Slack notifications** for test results (optional - configure `SLACK_WEBHOOK_URL` secret)
- **GitHub Pages** integration for report hosting

### Workflow Triggers
- **Push to main/develop** - Full test suite
- **Pull requests** - Code quality + tests
- **Scheduled runs** - Daily at 2:00 UTC
- **Manual triggers** - On-demand testing

### Optional Secrets Configuration
To enable additional features, configure these secrets in your GitHub repository:

- **`SLACK_WEBHOOK_URL`** - Slack webhook URL for test result notifications
- **`OPENAI_API_KEY`** - OpenAI API key for AI-powered test data generation

Without these secrets, the framework will work normally with fallback mechanisms.

## 🐳 Docker Support

### Quick Docker Setup
```bash
# Start all services
docker-compose up -d

# Run tests in container
docker-compose run test-runner pytest

# View reports
docker-compose run allure
```

### Services
- **test-runner**: Test execution container
- **mock-api**: Flask API server
- **allure**: Report server
- **selenium-hub**: Browser grid

## 🔧 Development

### Code Quality
Pre-commit hooks ensure code quality:
```bash
# Install hooks
pre-commit install

# Manual run
pre-commit run --all-files
```

### Adding New Tests
1. **UI Tests**: Create page objects in `pages/` and tests in `tests/ui/`
2. **API Tests**: Add tests in `tests/api/`
3. **Unit Tests**: Add tests in `tests/unit/`

### Example Page Object
```python
from src.ui.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CustomPage(BasePage):
    CUSTOM_ELEMENT = (By.CSS_SELECTOR, ".custom-selector")
    
    def custom_action(self):
        self.click_element(self.CUSTOM_ELEMENT)
```

## 🛠️ Configuration

### Environment Variables
```bash
# Application URLs
BASE_URL=https://automationexercise.com
API_BASE_URL=http://localhost:5000

# Browser Settings
BROWSER=chrome
HEADLESS=true
BROWSER_TIMEOUT=10

# Test Settings
SCREENSHOT_DIR=reports/screenshots
LOG_LEVEL=INFO

# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **OpenAI API Issues**
   - Check API key in `.env`
   - Framework automatically falls back to Faker
   - Check network connectivity

3. **Browser Issues**
   ```bash
   # Update webdriver
   pip install --upgrade webdriver-manager
   
   # Install Playwright browsers
   playwright install
   ```

4. **CI/CD Issues**
   ```bash
   # Test locally first
   python test_ci_workflow.py
   ```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
pytest -v -s
```

## 📈 Test Coverage

### Current Coverage
- ✅ **UI Testing**: Selenium + Playwright with Page Object Model
- ✅ **Mobile Testing**: Playwright with iOS/Android device emulation
- ✅ **API Testing**: REST API with mock server
- ✅ **Unit Testing**: Core functionality with pytest
- ✅ **Integration Testing**: End-to-end scenarios
- ✅ **Performance Testing**: Load and response time
- ✅ **Visual Testing**: Applitools + OpenCV
- ✅ **AI Integration**: OpenAI with Faker fallback
- ✅ **CI/CD Pipeline**: GitHub Actions with comprehensive workflow
- ✅ **Reporting**: Allure with detailed analytics
- ✅ **Containerization**: Docker support
- ✅ **Security**: Automated security scanning
- ✅ **Code Quality**: Pre-commit hooks and linting

## 🎯 Framework Highlights

### Advanced Features
- **AI-Powered Test Data**: Realistic data generation with OpenAI
- **Smart Fallback**: Automatic fallback to Faker when AI unavailable
- **Multi-Browser Support**: Chrome, Firefox with parallel execution
- **Mobile Device Emulation**: iOS and Android device testing with Playwright
- **Touch Gesture Testing**: Tap, swipe, pinch, scroll gesture validation
- **Responsive Design Testing**: Automatic breakpoint validation
- **Visual Testing**: Applitools integration for visual regression
- **Mock API Server**: Flask-based mock server for API testing
- **Comprehensive Reporting**: Allure with detailed analytics
- **Security Scanning**: Automated security checks with Bandit
- **Code Quality**: Automated formatting and linting

### Best Practices
- **Page Object Model**: Clean separation of test logic and page elements
- **Configuration Management**: Environment-based configuration with Pydantic
- **Error Handling**: Robust error handling with graceful fallbacks
- **Logging**: Structured logging with loguru
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive documentation and examples

## 🚀 Getting Started with Development

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and add tests
4. **Run tests**: `pytest -v`
5. **Check code quality**: `pre-commit run --all-files`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Create Pull Request**

## 📚 Additional Resources

- **Documentation**: Check `documentation/` folder for detailed guides
- **Examples**: See `tests/` for comprehensive test examples
- **CI/CD**: Check `.github/workflows/` for pipeline details
- **Configuration**: Review `config/settings.py` for all options

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and ensure all tests pass before submitting.

## 📄 License

This project is for educational and demonstration purposes.

---

**Happy Testing! 🧪✨**

*Built with ❤️ for Automation QA Engineer position*
