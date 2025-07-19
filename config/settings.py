"""
Configuration settings for the test framework
"""

import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Application URLs
    base_url: str = Field(default="https://automationexercise.com", env="BASE_URL")
    api_base_url: str = Field(default="http://localhost:5000", env="API_BASE_URL")
    admin_url: str = Field(default="https://automationexercise.com", env="ADMIN_URL")

    # Browser Configuration
    browser: str = Field(default="chrome", env="BROWSER")
    headless: bool = Field(default=True, env="HEADLESS")
    browser_timeout: int = Field(default=30, env="BROWSER_TIMEOUT")
    implicit_wait: int = Field(default=10, env="IMPLICIT_WAIT")

    # API Configuration
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    api_retry_attempts: int = Field(default=3, env="API_RETRY_ATTEMPTS")

    # AI Tools Configuration
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=1000, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    openai_timeout: int = Field(default=30, env="OPENAI_TIMEOUT")
    applitools_api_key: str | None = Field(default=None, env="APPLITOOLS_API_KEY")
    applitools_app_name: str = Field(
        default="SmartShop_AI_Tests", env="APPLITOOLS_APP_NAME"
    )

    # Test Data
    test_user_email: str = Field(default="test@smartshop.com", env="TEST_USER_EMAIL")
    test_user_password: str = Field(
        default="TestPassword123!", env="TEST_USER_PASSWORD"
    )
    admin_email: str = Field(default="admin@smartshop.com", env="ADMIN_EMAIL")
    admin_password: str = Field(default="AdminPassword123!", env="ADMIN_PASSWORD")

    # Database Configuration
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="smartshop_test", env="DB_NAME")
    db_user: str = Field(default="test_user", env="DB_USER")
    db_password: str = Field(default="test_password", env="DB_PASSWORD")

    # Reporting
    allure_results_dir: str = Field(
        default="./reports/allure-results", env="ALLURE_RESULTS_DIR"
    )
    html_report_dir: str = Field(default="./reports/html", env="HTML_REPORT_DIR")
    screenshot_dir: str = Field(default="./reports/screenshots", env="SCREENSHOT_DIR")

    # Performance Testing
    locust_host: str = Field(default="https://demo.smartshop.com", env="LOCUST_HOST")
    locust_users: int = Field(default=100, env="LOCUST_USERS")
    locust_spawn_rate: int = Field(default=10, env="LOCUST_SPAWN_RATE")
    locust_run_time: int = Field(default=300, env="LOCUST_RUN_TIME")

    # Email Notifications
    smtp_server: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: str | None = Field(default=None, env="SMTP_USERNAME")
    smtp_password: str | None = Field(default=None, env="SMTP_PASSWORD")
    notification_email: str = Field(
        default="qa-team@smartshop.com", env="NOTIFICATION_EMAIL"
    )

    # Slack Notifications
    slack_webhook_url: str | None = Field(default=None, env="SLACK_WEBHOOK_URL")
    slack_channel: str = Field(default="#qa-notifications", env="SLACK_CHANNEL")

    # Test Environment
    environment: str = Field(default="staging", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def is_production() -> bool:
    """Check if environment is production"""
    return settings.environment.lower() == "production"


def is_debug() -> bool:
    """Check if debug mode is enabled"""
    return settings.debug
