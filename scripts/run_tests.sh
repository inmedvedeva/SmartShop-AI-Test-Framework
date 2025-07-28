#!/bin/bash

# SmartShop AI Test Framework - Test Runner Script
# Author: Automation QA Engineer
# Version: 1.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function for outputting messages
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

# Function to show help
show_help() {
    echo "SmartShop AI Test Framework - Test Runner"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --test-type TYPE     Test type (ui, api, performance, visual, all)"
    echo "  -b, --browser BROWSER    Browser for UI tests (chrome, firefox, edge)"
    echo "  -p, --parallel           Run tests in parallel"
    echo "  -r, --rerun              Number of retries for failed tests"
    echo "  -m, --markers MARKERS    Pytest markers for test filtering"
    echo "  -o, --output FORMAT      Report format (html, allure, json)"
    echo "  -v, --verbose            Verbose output"
    echo "  -h, --help               Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 -t ui -b chrome                    # UI tests in Chrome"
    echo "  $0 -t api                             # API tests"
    echo "  $0 -t all -p -r 2                     # All tests in parallel with 2 retries"
    echo "  $0 -m smoke -o allure                 # Smoke tests with Allure report"
    echo ""
}

# Default parameters
TEST_TYPE="all"
BROWSER="chrome"
PARALLEL=false
RERUN=0
MARKERS=""
OUTPUT_FORMAT="html"
VERBOSE=false

# Command line argument parsing
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
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check virtual environment
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment is not activated"
        if [ -d "venv" ]; then
            print_message "Activating virtual environment..."
            source venv/bin/activate
        else
            print_error "Virtual environment not found. Create it with: python -m venv venv"
            exit 1
        fi
    fi
}

# Check dependencies
check_dependencies() {
    print_message "Checking dependencies..."

    if ! command -v python &> /dev/null; then
        print_error "Python is not installed"
        exit 1
    fi

    if ! python -c "import pytest" &> /dev/null; then
        print_error "pytest is not installed. Install dependencies: pip install -r requirements.txt"
        exit 1
    fi

    if ! python -c "import selenium" &> /dev/null; then
        print_error "selenium is not installed"
        exit 1
    fi

    print_success "Dependencies checked"
}

# Create directories for reports
create_report_dirs() {
    print_message "Creating directories for reports..."

    mkdir -p reports/allure-results
    mkdir -p reports/html
    mkdir -p reports/screenshots
    mkdir -p reports/json

    print_success "Directories created"
}

# Set up environment variables
setup_environment() {
    print_message "Setting up environment variables..."

    export BROWSER=$BROWSER
    export HEADLESS=true

    if [ "$VERBOSE" = true ]; then
        export PYTEST_ADDOPTS="-v -s"
    fi

    print_success "Environment variables set"
}

# Build pytest command
build_pytest_command() {
    local cmd="pytest"

    # Determine test path
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
            print_error "Unknown test type: $TEST_TYPE"
            exit 1
            ;;
    esac

    # Add markers if specified
    if [ ! -z "$MARKERS" ]; then
        cmd="$cmd -m $MARKERS"
    fi

    # Add parallel execution
    if [ "$PARALLEL" = true ]; then
        cmd="$cmd -n auto"
    fi

    # Add retries
    if [ "$RERUN" -gt 0 ]; then
        cmd="$cmd --reruns $RERUN --reruns-delay 1"
    fi

    # Add report formats
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

# Run tests
run_tests() {
    local cmd=$(build_pytest_command)

    print_message "Running tests..."
    print_message "Command: $cmd"
    echo ""

    # Start time
    local start_time=$(date +%s)

    # Run tests
    if eval $cmd; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        print_success "Tests completed successfully in ${duration} seconds"

        # Show report information
        show_report_info

    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        print_error "Tests completed with errors in ${duration} seconds"

        # Show report information even on errors
        show_report_info

        exit 1
    fi
}

# Show report information
show_report_info() {
    echo ""
    print_message "Reports generated:"

    if [ -f "reports/html/test_report.html" ]; then
        echo "  📊 HTML report: reports/html/test_report.html"
    fi

    if [ -d "reports/allure-results" ] && [ "$(ls -A reports/allure-results)" ]; then
        echo "  📈 Allure results: reports/allure-results/"
        echo "  💡 To view Allure report, run: allure serve reports/allure-results"
    fi

    if [ -f "reports/json/test_report.json" ]; then
        echo "  📋 JSON report: reports/json/test_report.json"
    fi

    if [ -d "reports/screenshots" ] && [ "$(ls -A reports/screenshots)" ]; then
        echo "  📸 Screenshots: reports/screenshots/"
    fi
}

# Clean up old reports
cleanup_old_reports() {
    print_message "Cleaning up old reports..."

    # Delete old HTML reports (older than 7 days)
    find reports/html -name "*.html" -mtime +7 -delete 2>/dev/null || true

    # Delete old screenshots (older than 3 days)
    find reports/screenshots -name "*.png" -mtime +3 -delete 2>/dev/null || true

    print_success "Cleanup complete"
}

# Main function
main() {
    echo "🧪 SmartShop AI Test Framework"
    echo "================================"
    echo ""

    print_message "Test type: $TEST_TYPE"
    print_message "Browser: $BROWSER"
    print_message "Parallel: $PARALLEL"
    print_message "Retries: $RERUN"
    print_message "Markers: $MARKERS"
    print_message "Report format: $OUTPUT_FORMAT"
    print_message "Verbose output: $VERBOSE"
    echo ""

    # Perform checks and setups
    check_venv
    check_dependencies
    create_report_dirs
    setup_environment
    cleanup_old_reports

    # Run tests
    run_tests

    print_success "Testing completed!"
}

# Start main function
main "$@"
