# 📦 Установка и настройка SmartShop AI Test Framework

## 🎯 Цель проекта

Этот пет-проект демонстрирует все ключевые навыки для позиции **Automation QA Engineer (Python + AI)**:

### ✅ Демонстрируемые навыки
- **Python 3.12+** с pytest и ООП
- **Selenium/Playwright** для веб-автоматизации
- **REST API тестирование** с requests
- **AI-инструменты** (OpenAI, Applitools)
- **Page Object Model** архитектура
- **CI/CD интеграция** (GitHub Actions)
- **Docker контейнеризация**
- **Allure отчеты** и мониторинг

## 🚀 Быстрая установка

### 1. Системные требования
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git curl

# macOS
brew install python3 git

# Windows
# Скачайте Python 3.12+ с python.org
```

### 2. Клонирование проекта
```bash
git clone <your-repo-url>
cd SmartShop-AI-Test-Framework
```

### 3. Создание виртуального окружения
```bash
# Создаем виртуальное окружение
python3 -m venv venv

# Активируем его
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows
```

### 4. Установка зависимостей
```bash
# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
pip install -r requirements.txt

# Устанавливаем браузеры для Playwright
playwright install
playwright install-deps
```

### 5. Проверка установки
```bash
# Запускаем демонстрацию
python3 demo.py

# Проверяем pytest
pytest --version
```

## 🔧 Настройка переменных окружения

### 1. Создание .env файла
```bash
# Копируем пример настроек
cp config/settings.py .env.example

# Создаем .env файл
cat > .env << EOF
# Application URLs
BASE_URL=https://demo.smartshop.com
API_BASE_URL=https://api.smartshop.com

# Browser Configuration
BROWSER=chrome
HEADLESS=true

# AI Tools (опционально)
OPENAI_API_KEY=your_openai_api_key_here
APPLITOOLS_API_KEY=your_applitools_api_key_here

# Test Data
TEST_USER_EMAIL=test@smartshop.com
TEST_USER_PASSWORD=TestPassword123!

# Environment
ENVIRONMENT=staging
DEBUG=false
EOF
```

### 2. Настройка AI-инструментов (опционально)

#### OpenAI API
1. Зарегистрируйтесь на [OpenAI](https://openai.com)
2. Получите API ключ
3. Добавьте в .env файл:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

#### Applitools
1. Зарегистрируйтесь на [Applitools](https://applitools.com)
2. Получите API ключ
3. Добавьте в .env файл:
```bash
APPLITOOLS_API_KEY=your-applitools-key-here
```

## 🧪 Запуск тестов

### 1. Базовый запуск
```bash
# Все тесты
./scripts/run_tests.sh

# Только UI тесты
./scripts/run_tests.sh -t ui -b chrome

# API тесты
./scripts/run_tests.sh -t api

# Визуальные тесты
./scripts/run_tests.sh -t visual
```

### 2. Продвинутые опции
```bash
# Параллельное выполнение
./scripts/run_tests.sh -p

# Повторные запуски для неудачных тестов
./scripts/run_tests.sh -r 2

# Фильтрация по маркерам
./scripts/run_tests.sh -m smoke

# Allure отчеты
./scripts/run_tests.sh -o allure
```

### 3. Прямой запуск pytest
```bash
# UI тесты
pytest tests/ui/ -v

# API тесты
pytest tests/api/ -v

# Дымовые тесты
pytest -m smoke -v

# Все тесты с HTML отчетом
pytest --html=reports/html/report.html --self-contained-html
```

## 🐳 Docker установка

### 1. Установка Docker
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER

# macOS
brew install docker docker-compose

# Windows
# Скачайте Docker Desktop с docker.com
```

### 2. Запуск в Docker
```bash
# Собираем и запускаем тестовый контейнер
docker build -f Dockerfile.test -t smartshop-tests .
docker run -v $(pwd)/reports:/app/reports smartshop-tests

# Полное окружение с Docker Compose
docker-compose up -d
docker-compose --profile test run test-runner
```

## 📊 Просмотр отчетов

### 1. HTML отчеты
```bash
# Открываем в браузере
open reports/html/test_report.html  # macOS
xdg-open reports/html/test_report.html  # Linux
start reports/html/test_report.html  # Windows
```

### 2. Allure отчеты
```bash
# Устанавливаем Allure (если не установлен)
# macOS: brew install allure
# Linux: sudo apt install allure

# Генерируем отчет
pytest --alluredir=./reports/allure-results

# Просматриваем отчет
allure serve ./reports/allure-results
```

### 3. Allure в Docker
```bash
# Запускаем Allure сервер
docker-compose --profile reports up allure

# Открываем в браузере
open http://localhost:5050
```

## 🔄 CI/CD настройка

### 1. GitHub Actions
1. Создайте репозиторий на GitHub
2. Скопируйте файлы `.github/workflows/`
3. Настройте секреты в Settings > Secrets:
   - `SLACK_WEBHOOK_URL`
   - `OPENAI_API_KEY`
   - `APPLITOOLS_API_KEY`

### 2. Ручной запуск
1. Перейдите в GitHub > Actions
2. Выберите "SmartShop AI Test Runner"
3. Нажмите "Run workflow"
4. Выберите тип тестов

## 🛠️ Структура проекта

```
SmartShop-AI-Test-Framework/
├── 📁 config/                 # Конфигурация
│   └── settings.py           # Настройки приложения
├── 📁 pages/                 # Page Object Model
│   ├── base_page.py         # Базовый класс страницы
│   └── home_page.py         # Главная страница
├── 📁 tests/                 # Тестовые сценарии
│   ├── 📁 ui/               # UI тесты
│   ├── 📁 api/              # API тесты
│   ├── 📁 performance/      # Тесты производительности
│   └── 📁 integration/      # Интеграционные тесты
├── 📁 utils/                 # AI-инструменты и утилиты
│   ├── ai_data_generator.py # AI генератор данных
│   └── visual_testing.py    # Визуальное тестирование
├── 📁 scripts/               # Скрипты запуска
│   └── run_tests.sh         # Основной скрипт тестов
├── 📁 .github/               # CI/CD конфигурация
│   └── workflows/           # GitHub Actions
├── 📄 requirements.txt       # Python зависимости
├── 📄 docker-compose.yml     # Docker конфигурация
├── 📄 Dockerfile.test        # Dockerfile для тестов
├── 📄 pytest.ini           # Конфигурация pytest
├── 📄 README.md             # Основная документация
├── 📄 QUICK_START.md        # Быстрый старт
├── 📄 demo.py               # Демонстрационный скрипт
└── 📄 INSTALL.md            # Этот файл
```

## 🎓 Ключевые особенности

### 1. AI-интеграция
- **Генерация тестовых данных** с OpenAI
- **Визуальное тестирование** с Applitools
- **Кастомные алгоритмы** компьютерного зрения
- **Автоматическая генерация** сценариев

### 2. Современные практики
- **Page Object Model** архитектура
- **Фикстуры pytest** для переиспользования
- **Маркеры** для категоризации тестов
- **Параллельное выполнение**

### 3. DevOps готовность
- **Docker контейнеризация**
- **GitHub Actions** CI/CD
- **Allure отчеты**
- **Мониторинг и уведомления**

## 🚨 Устранение неполадок

### 1. Проблемы с зависимостями
```bash
# Очищаем кэш pip
pip cache purge

# Переустанавливаем зависимости
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### 2. Проблемы с браузерами
```bash
# Переустанавливаем браузеры
playwright install --force
playwright install-deps
```

### 3. Проблемы с Docker
```bash
# Очищаем Docker
docker system prune -a

# Пересобираем образ
docker build -f Dockerfile.test -t smartshop-tests . --no-cache
```

### 4. Проблемы с правами доступа
```bash
# Делаем скрипт исполняемым
chmod +x scripts/run_tests.sh

# Проверяем права
ls -la scripts/
```

## 📞 Поддержка

- 📖 **Документация**: README.md
- ⚡ **Быстрый старт**: QUICK_START.md
- 🐛 **Issues**: GitHub Issues
- 💬 **Обсуждения**: GitHub Discussions

## 🎯 Готовность к интервью

Этот проект демонстрирует:

✅ **Технические навыки**
- Python + pytest
- Selenium/Playwright
- API тестирование
- ООП и архитектурные паттерны

✅ **AI-инновации**
- Интеграция с AI-инструментами
- Автоматическая генерация данных
- Визуальное тестирование с AI

✅ **DevOps компетенции**
- CI/CD пайплайны
- Docker контейнеризация
- Мониторинг и отчетность

✅ **Производственная готовность**
- Масштабируемость
- Поддержка и документация
- Современные практики

---

**Создано для демонстрации навыков Automation QA Engineer с AI-интеграцией** 🚀
