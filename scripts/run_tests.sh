#!/bin/bash

# SmartShop AI Test Framework - Test Runner Script
# Автор: Automation QA Engineer
# Версия: 1.0

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Функция для показа справки
show_help() {
    echo "SmartShop AI Test Framework - Test Runner"
    echo ""
    echo "Использование: $0 [ОПЦИИ]"
    echo ""
    echo "Опции:"
    echo "  -t, --test-type TYPE     Тип тестов (ui, api, performance, visual, all)"
    echo "  -b, --browser BROWSER    Браузер для UI тестов (chrome, firefox, edge)"
    echo "  -p, --parallel           Запуск тестов параллельно"
    echo "  -r, --rerun              Количество повторных запусков для неудачных тестов"
    echo "  -m, --markers MARKERS    Маркеры pytest для фильтрации тестов"
    echo "  -o, --output FORMAT      Формат отчета (html, allure, json)"
    echo "  -v, --verbose            Подробный вывод"
    echo "  -h, --help               Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 -t ui -b chrome                    # UI тесты в Chrome"
    echo "  $0 -t api                             # API тесты"
    echo "  $0 -t all -p -r 2                     # Все тесты параллельно с 2 повторами"
    echo "  $0 -m smoke -o allure                 # Дымовые тесты с Allure отчетом"
    echo ""
}

# Параметры по умолчанию
TEST_TYPE="all"
BROWSER="chrome"
PARALLEL=false
RERUN=0
MARKERS=""
OUTPUT_FORMAT="html"
VERBOSE=false

# Парсинг аргументов командной строки
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--test-type)
            TEST_TYPE="$2"
            shift 2
            ;;
        -b|--browser)
            BROWSER="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -r|--rerun)
            RERUN="$2"
            shift 2
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Неизвестная опция: $1"
            show_help
            exit 1
            ;;
    esac
done

# Проверка виртуального окружения
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Виртуальное окружение не активировано"
        if [ -d "venv" ]; then
            print_message "Активируем виртуальное окружение..."
            source venv/bin/activate
        else
            print_error "Виртуальное окружение не найдено. Создайте его командой: python -m venv venv"
            exit 1
        fi
    fi
}

# Проверка зависимостей
check_dependencies() {
    print_message "Проверяем зависимости..."

    if ! command -v python &> /dev/null; then
        print_error "Python не установлен"
        exit 1
    fi

    if ! python -c "import pytest" &> /dev/null; then
        print_error "pytest не установлен. Установите зависимости: pip install -r requirements.txt"
        exit 1
    fi

    if ! python -c "import selenium" &> /dev/null; then
        print_error "selenium не установлен"
        exit 1
    fi

    print_success "Зависимости проверены"
}

# Создание директорий для отчетов
create_report_dirs() {
    print_message "Создаем директории для отчетов..."

    mkdir -p reports/allure-results
    mkdir -p reports/html
    mkdir -p reports/screenshots
    mkdir -p reports/json

    print_success "Директории созданы"
}

# Настройка переменных окружения
setup_environment() {
    print_message "Настраиваем переменные окружения..."

    export BROWSER=$BROWSER
    export HEADLESS=true

    if [ "$VERBOSE" = true ]; then
        export PYTEST_ADDOPTS="-v -s"
    fi

    print_success "Переменные окружения настроены"
}

# Формирование команды pytest
build_pytest_command() {
    local cmd="pytest"

    # Определяем путь к тестам
    case $TEST_TYPE in
        "ui")
            cmd="$cmd tests/ui/"
            ;;
        "api")
            cmd="$cmd tests/api/"
            ;;
        "performance")
            cmd="$cmd tests/performance/"
            ;;
        "visual")
            cmd="$cmd tests/ui/ -m visual"
            ;;
        "all")
            cmd="$cmd tests/"
            ;;
        *)
            print_error "Неизвестный тип тестов: $TEST_TYPE"
            exit 1
            ;;
    esac

    # Добавляем маркеры если указаны
    if [ ! -z "$MARKERS" ]; then
        cmd="$cmd -m $MARKERS"
    fi

    # Добавляем параллельное выполнение
    if [ "$PARALLEL" = true ]; then
        cmd="$cmd -n auto"
    fi

    # Добавляем повторные запуски
    if [ "$RERUN" -gt 0 ]; then
        cmd="$cmd --reruns $RERUN --reruns-delay 1"
    fi

    # Добавляем форматы отчетов
    case $OUTPUT_FORMAT in
        "html")
            cmd="$cmd --html=reports/html/test_report.html --self-contained-html"
            ;;
        "allure")
            cmd="$cmd --alluredir=reports/allure-results"
            ;;
        "json")
            cmd="$cmd --json-report --json-report-file=reports/json/test_report.json"
            ;;
        "all")
            cmd="$cmd --html=reports/html/test_report.html --self-contained-html --alluredir=reports/allure-results --json-report --json-report-file=reports/json/test_report.json"
            ;;
    esac

    echo "$cmd"
}

# Запуск тестов
run_tests() {
    local cmd=$(build_pytest_command)

    print_message "Запускаем тесты..."
    print_message "Команда: $cmd"
    echo ""

    # Засекаем время
    local start_time=$(date +%s)

    # Запускаем тесты
    if eval $cmd; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        print_success "Тесты завершены успешно за ${duration} секунд"

        # Показываем информацию об отчетах
        show_report_info

    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        print_error "Тесты завершены с ошибками за ${duration} секунд"

        # Показываем информацию об отчетах даже при ошибках
        show_report_info

        exit 1
    fi
}

# Показ информации об отчетах
show_report_info() {
    echo ""
    print_message "Отчеты сгенерированы:"

    if [ -f "reports/html/test_report.html" ]; then
        echo "  📊 HTML отчет: reports/html/test_report.html"
    fi

    if [ -d "reports/allure-results" ] && [ "$(ls -A reports/allure-results)" ]; then
        echo "  📈 Allure результаты: reports/allure-results/"
        echo "  💡 Для просмотра Allure отчета выполните: allure serve reports/allure-results"
    fi

    if [ -f "reports/json/test_report.json" ]; then
        echo "  📋 JSON отчет: reports/json/test_report.json"
    fi

    if [ -d "reports/screenshots" ] && [ "$(ls -A reports/screenshots)" ]; then
        echo "  📸 Скриншоты: reports/screenshots/"
    fi
}

# Очистка старых отчетов
cleanup_old_reports() {
    print_message "Очищаем старые отчеты..."

    # Удаляем старые HTML отчеты (старше 7 дней)
    find reports/html -name "*.html" -mtime +7 -delete 2>/dev/null || true

    # Удаляем старые скриншоты (старше 3 дней)
    find reports/screenshots -name "*.png" -mtime +3 -delete 2>/dev/null || true

    print_success "Очистка завершена"
}

# Основная функция
main() {
    echo "🧪 SmartShop AI Test Framework"
    echo "================================"
    echo ""

    print_message "Тип тестов: $TEST_TYPE"
    print_message "Браузер: $BROWSER"
    print_message "Параллельно: $PARALLEL"
    print_message "Повторы: $RERUN"
    print_message "Маркеры: $MARKERS"
    print_message "Формат отчета: $OUTPUT_FORMAT"
    print_message "Подробный вывод: $VERBOSE"
    echo ""

    # Выполняем проверки и настройки
    check_venv
    check_dependencies
    create_report_dirs
    setup_environment
    cleanup_old_reports

    # Запускаем тесты
    run_tests

    print_success "Тестирование завершено!"
}

# Запуск основной функции
main "$@"
