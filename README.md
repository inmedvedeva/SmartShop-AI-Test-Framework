# SmartShop AI Test Framework

A comprehensive test automation framework for demonstrating Automation QA Engineer skills with AI integration.

## 🚀 Features

- **UI Testing**: Selenium WebDriver with Page Object Model
- **API Testing**: REST API testing with requests library
- **AI Integration**: OpenAI-powered test data generation with Faker fallback
- **Visual Testing**: Applitools integration for visual regression testing
- **Performance Testing**: Built-in performance monitoring
- **CI/CD Ready**: GitHub Actions workflow with Docker support
- **Reporting**: Allure reports with detailed test results
- **Containerization**: Docker support for consistent environments
- **Configuration**: Environment-based configuration with pydantic
- **Logging**: Structured logging with loguru

## 🏗️ Project Structure

```
SmartShop-AI-Test-Framework/
├── config/                 # Configuration files
│   └── settings.py        # Main settings with pydantic
├── data/                  # Test data and demo files
├── docs/                  # Documentation
├── pages/                 # Page Object Model classes
│   ├── base_page.py       # Base page class
│   ├── home_page.py       # Home page implementation
│   └── automation_exercise_home_page.py
├── reports/               # Test reports and screenshots
├── tests/                 # Test files
│   ├── api/              # API tests
│   ├── integration/      # Integration tests
│   ├── performance/      # Performance tests
│   └── ui/               # UI tests
├── utils/                 # Utility classes
│   ├── ai_data_generator.py  # AI-powered test data generation
│   └── visual_testing.py     # Visual testing utilities
├── venv/                  # Python virtual environment
├── .env                   # Environment variables (create from .env.example)
├── .github/workflows/     # CI/CD workflows
├── docker-compose.yml     # Docker services
├── Dockerfile.test        # Test container
├── requirements.txt       # Python dependencies
└── pytest.ini           # Pytest configuration
```

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized testing)
- Chrome/Firefox browser
- OpenAI API key (optional, for AI features)

### Quick Setup (Recommended)

**One-command setup:**
```bash
git clone <repository-url>
cd SmartShop-AI-Test-Framework
./quick_start.sh
```

### Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartShop-AI-Test-Framework
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env_example.txt .env
   # Edit .env with your settings
   ```

5. **Start Mock API Server** (for API testing)
   ```bash
   python start_mock_api.py
   # Or directly: python mock_api_server.py
   ```

6. **Install pre-commit hooks** (optional)
   ```bash
   pre-commit install
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env_example.txt`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

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

# Database (for integration tests)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartshop_test
DB_USER=test_user
DB_PASSWORD=test_password
```

### OpenAI Integration

The framework uses OpenAI for generating realistic test data. If OpenAI is unavailable (geographic restrictions, API limits, etc.), it automatically falls back to Faker.

**Supported OpenAI Models:**
- `gpt-3.5-turbo` (default)
- `gpt-4` (if configured)

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m ui          # UI tests only
pytest -m api         # API tests only
pytest -m smoke       # Smoke tests only
pytest -m performance # Performance tests only

# Run with verbose output
pytest -v

# Run with parallel execution
pytest -n auto
```

### Test Categories

- **UI Tests**: Selenium-based UI automation
- **API Tests**: REST API testing
- **Integration Tests**: End-to-end scenarios
- **Performance Tests**: Load and response time testing
- **Visual Tests**: Visual regression testing
- **Smoke Tests**: Critical functionality
- **Regression Tests**: Full test suite

### Running with Docker

```bash
# Start all services
docker-compose up -d

# Run tests in container
docker-compose run test-runner pytest -m smoke

# View reports
docker-compose run allure
```

## 📊 Reports

### Allure Reports

```bash
# Generate Allure report
pytest --alluredir=reports/allure-results

# View report
allure serve reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean
```

### Screenshots

Screenshots are automatically saved to `reports/screenshots/` on test failures.

## 🤖 AI Features

### Test Data Generation

The framework can generate realistic test data using AI:

```python
from utils.ai_data_generator import AIDataGenerator

ai_generator = AIDataGenerator()

# Generate user profiles
user = ai_generator.generate_user_profile("customer")

# Generate product catalogs
products = ai_generator.generate_product_catalog("electronics", 5)

# Generate test scenarios
scenarios = ai_generator.generate_test_scenarios("search")
```

### Fallback Mechanism

If OpenAI is unavailable, the framework automatically uses Faker:

- **Geographic restrictions** (403 errors)
- **Invalid API keys** (401 errors)
- **Rate limiting** (429 errors)
- **Network issues** (timeouts)

## 🐳 Docker Support

### Services

- **smartshop-app**: Demo web application (nginx)
- **smartshop-api**: Demo API server (FastAPI)
- **postgres**: Database for integration tests
- **redis**: Caching layer
- **selenium-hub**: Selenium Grid for parallel testing
- **chrome/firefox**: Browser nodes
- **test-runner**: Test execution container
- **allure**: Report server
- **grafana**: Monitoring dashboard

### Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# Run tests
docker-compose run test-runner pytest

# View reports
open http://localhost:5050  # Allure
open http://localhost:3000  # Grafana
```

## 🔧 Development

### Code Quality

The project uses pre-commit hooks for code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Adding New Tests

1. **UI Tests**: Create new page objects in `pages/` and tests in `tests/ui/`
2. **API Tests**: Add tests in `tests/api/`
3. **Integration Tests**: Add end-to-end scenarios in `tests/integration/`

### Custom Page Objects

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class CustomPage(BasePage):
    # Element locators
    CUSTOM_ELEMENT = (By.CSS_SELECTOR, ".custom-selector")

    def custom_action(self):
        """Custom page action"""
        self.click_element(self.CUSTOM_ELEMENT)
```

## 📈 CI/CD

### GitHub Actions

The framework includes GitHub Actions workflows:

- **Scheduled Tests**: Daily test execution
- **Manual Triggers**: On-demand test runs
- **Security Scanning**: Automated security checks
- **Report Generation**: Automatic report creation

### Workflow Features

- Parallel test execution
- Multiple browser testing
- Performance monitoring
- Security scanning
- Report publishing

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**
   ```bash
   # Update ChromeDriver
   pip install --upgrade webdriver-manager
   ```

2. **OpenAI API Errors**
   - Check API key in `.env`
   - Verify network connectivity
   - Framework will fallback to Faker automatically

3. **Docker Issues**
   ```bash
   # Clean up containers
   docker-compose down -v
   docker system prune
   ```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
pytest -v -s
```

## 📚 Examples

### Demo Scripts

- `automation_exercise_demo.py`: Basic UI testing demo
- `final_demo_with_error_handling.py`: Comprehensive demo with error handling
- `test_openai_config.py`: OpenAI configuration verification

### Test Examples

```python
# UI Test Example
def test_home_page_loads_successfully(self, home_page):
    home_page.open_home_page()
    assert "SmartShop" in home_page.get_page_title()

# API Test Example
def test_get_products(self, session, api_base_url):
    response = session.get(f"{api_base_url}/products")
    assert response.status_code == 200
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes.

## 🆘 Support

For questions or issues:
- Check the documentation in `docs/`
- Review example scripts
- Check GitHub Issues

---

**Happy Testing! 🧪✨**
