#!/usr/bin/env python3
"""
Security Check Script for SmartShop AI Test Framework
Scans the project for potential security issues and sensitive data
"""
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set


class SecurityChecker:
    """Security checker for the project"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.security_issues = []
        self.warnings = []
        self.passed_checks = []

    def check_gitignore(self) -> bool:
        """Check if .gitignore exists and contains security patterns"""
        print("🔍 Checking .gitignore configuration...")

        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            self.security_issues.append("❌ .gitignore file is missing!")
            return False

        with open(gitignore_path) as f:
            content = f.read()

        required_patterns = [
            r"\.env",
            r"\.env\*",
            r"\*\.key",
            r"\*\.pem",
            r"secrets/",
            r"credentials\.json",
            r"\*\.db",
            r"\*\.sqlite",
            r"\*\.log",
            r"logs/",
            r"reports/screenshots/",
            r"reports/allure-results/",
        ]

        missing_patterns = []
        for pattern in required_patterns:
            if not re.search(pattern, content):
                missing_patterns.append(pattern)

        if missing_patterns:
            self.warnings.append(
                f"⚠️ Missing patterns in .gitignore: {missing_patterns}"
            )
            return False

        self.passed_checks.append("✅ .gitignore properly configured")
        return True

    def check_env_files(self) -> bool:
        """Check for environment files that shouldn't be committed"""
        print("🔍 Checking for sensitive environment files...")

        env_files = []
        for pattern in [".env*", "*.env"]:
            env_files.extend(self.project_root.glob(pattern))

        # Filter out example files
        sensitive_env_files = [
            f for f in env_files if not f.name.startswith("env_example")
        ]

        if sensitive_env_files:
            for file in sensitive_env_files:
                if file.stat().st_size > 0:
                    self.security_issues.append(
                        f"❌ Sensitive environment file found: {file}"
                    )
                else:
                    self.warnings.append(f"⚠️ Empty environment file found: {file}")
            return False

        self.passed_checks.append("✅ No sensitive environment files found")
        return True

    def check_hardcoded_secrets(self) -> bool:
        """Check for hardcoded secrets in code"""
        print("🔍 Checking for hardcoded secrets...")

        # Patterns for different types of secrets
        secret_patterns = {
            "openai_key": r"sk-[a-zA-Z0-9]{48}",
            "api_key": r'api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{10,}["\']',
            "password": r'password["\']?\s*[:=]\s*["\'][^"\']{6,}["\']',
            "token": r'token["\']?\s*[:=]\s*["\'][^"\']{10,}["\']',
            "secret": r'secret["\']?\s*[:=]\s*["\'][^"\']{6,}["\']',
            "credential": r'credential["\']?\s*[:=]\s*["\'][^"\']{6,}["\']',
        }

        found_secrets = []

        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or ".git" in str(py_file):
                continue

            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                for secret_type, pattern in secret_patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Skip test/demo files with fake keys
                        if self._is_test_file(py_file) and self._is_fake_key(match):
                            continue
                        # Skip constants file with test data
                        if "constants.py" in str(py_file):
                            continue
                        found_secrets.append(
                            {
                                "file": str(py_file.relative_to(self.project_root)),
                                "type": secret_type,
                                "match": (
                                    match[:20] + "..." if len(match) > 20 else match
                                ),
                            }
                        )
            except Exception as e:
                self.warnings.append(f"⚠️ Error reading {py_file}: {e}")

        if found_secrets:
            for secret in found_secrets:
                self.security_issues.append(
                    f"❌ Hardcoded {secret['type']} found in {secret['file']}: {secret['match']}"
                )
            return False

        self.passed_checks.append("✅ No hardcoded secrets found")
        return True

    def check_database_files(self) -> bool:
        """Check for database files that shouldn't be committed"""
        print("🔍 Checking for database files...")

        db_patterns = ["*.db", "*.sqlite", "*.sqlite3"]
        db_files = []

        for pattern in db_patterns:
            db_files.extend(self.project_root.glob(pattern))

        # Filter out venv and git directories
        db_files = [
            f for f in db_files if "venv" not in str(f) and ".git" not in str(f)
        ]

        if db_files:
            for db_file in db_files:
                self.security_issues.append(f"❌ Database file found: {db_file}")
            return False

        self.passed_checks.append("✅ No database files found")
        return True

    def check_log_files(self) -> bool:
        """Check for log files that might contain sensitive data"""
        print("🔍 Checking for log files...")

        log_patterns = ["*.log", "logs/"]
        log_files = []

        for pattern in log_patterns:
            if pattern.endswith("/"):
                log_dirs = list(self.project_root.glob(pattern))
                for log_dir in log_dirs:
                    if log_dir.is_dir():
                        log_files.extend(log_dir.rglob("*"))
            else:
                log_files.extend(self.project_root.glob(pattern))

        # Filter out venv and git directories
        log_files = [
            f for f in log_files if "venv" not in str(f) and ".git" not in str(f)
        ]

        if log_files:
            for log_file in log_files:
                if log_file.is_file() and log_file.stat().st_size > 0:
                    self.warnings.append(f"⚠️ Log file found: {log_file}")
            return False

        self.passed_checks.append("✅ No log files found")
        return True

    def check_file_permissions(self) -> bool:
        """Check file permissions for sensitive files"""
        print("🔍 Checking file permissions...")

        sensitive_files = []
        for pattern in [".env*", "*.key", "*.pem", "secrets.json"]:
            sensitive_files.extend(self.project_root.glob(pattern))

        permission_issues = []
        for file in sensitive_files:
            if file.exists():
                stat = file.stat()
                # Check if file is readable by others
                if stat.st_mode & 0o004:  # Others can read
                    permission_issues.append(f"⚠️ {file} is readable by others")

        if permission_issues:
            for issue in permission_issues:
                self.warnings.append(issue)
            return False

        self.passed_checks.append("✅ File permissions are secure")
        return True

    def check_pre_commit_hooks(self) -> bool:
        """Check if pre-commit hooks are installed"""
        print("🔍 Checking pre-commit hooks...")

        try:
            result = subprocess.run(
                ["pre-commit", "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                self.passed_checks.append("✅ Pre-commit hooks are installed")
                return True
            else:
                self.warnings.append("⚠️ Pre-commit hooks not found")
                return False
        except FileNotFoundError:
            self.warnings.append("⚠️ Pre-commit not installed")
            return False

    def check_dependencies_security(self) -> bool:
        """Check for known security vulnerabilities in dependencies"""
        print("🔍 Checking dependencies for security issues...")

        try:
            # Try to run safety check
            result = subprocess.run(
                ["safety", "check", "--json"], capture_output=True, text=True
            )

            if result.returncode == 0:
                self.passed_checks.append(
                    "✅ No known security vulnerabilities in dependencies"
                )
                return True
            else:
                # Parse safety output for vulnerabilities
                try:
                    vulns = json.loads(result.stdout)
                    if vulns:
                        for vuln in vulns:
                            self.security_issues.append(
                                f"❌ Security vulnerability: {vuln.get('package', 'Unknown')} - {vuln.get('description', 'No description')}"
                            )
                        return False
                except json.JSONDecodeError:
                    self.warnings.append("⚠️ Could not parse safety output")
                    return False
        except FileNotFoundError:
            self.warnings.append("⚠️ Safety tool not installed")
            return False

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test or demo file"""
        test_indicators = ["test", "demo", "example"]
        file_str = str(file_path).lower()
        return any(indicator in file_str for indicator in test_indicators)

    def _is_fake_key(self, key: str) -> bool:
        """Check if key is a fake/test key"""
        fake_patterns = [
            "sk-invalid-key",
            "sk-test-key",
            "test-password",
            "fake-key",
            "dummy-key",
        ]
        return any(pattern in key.lower() for pattern in fake_patterns)

    def _is_test_data(self, data: str) -> bool:
        """Check if data is test data"""
        test_patterns = [
            "test@smartshop.com",
            "TestPassword123!",
            "AdminPassword123!",
            "test_password",
            "test_user",
            "test@example.com",
            "wrongpassword",
        ]
        return any(pattern in data for pattern in test_patterns)

    def run_all_checks(self) -> dict:
        """Run all security checks"""
        print("🚀 Starting comprehensive security check...\n")

        checks = [
            ("Gitignore Configuration", self.check_gitignore),
            ("Environment Files", self.check_env_files),
            ("Hardcoded Secrets", self.check_hardcoded_secrets),
            ("Database Files", self.check_database_files),
            ("Log Files", self.check_log_files),
            ("File Permissions", self.check_file_permissions),
            ("Pre-commit Hooks", self.check_pre_commit_hooks),
            ("Dependencies Security", self.check_dependencies_security),
        ]

        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                self.warnings.append(f"⚠️ Error in {check_name}: {e}")
                results[check_name] = False

        return results

    def print_report(self):
        """Print security check report"""
        print("\n" + "=" * 80)
        print("🔒 SECURITY CHECK REPORT")
        print("=" * 80)

        if self.security_issues:
            print("\n🚨 CRITICAL SECURITY ISSUES:")
            for issue in self.security_issues:
                print(f"   {issue}")

        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"   {warning}")

        if self.passed_checks:
            print("\n✅ PASSED CHECKS:")
            for check in self.passed_checks:
                print(f"   {check}")

        print("\n" + "=" * 80)

        if self.security_issues:
            print("❌ SECURITY CHECK FAILED - FIX ISSUES ABOVE")
        elif self.warnings:
            print("⚠️ SECURITY CHECK PASSED WITH WARNINGS")
        else:
            print("✅ SECURITY CHECK PASSED - ALL CLEAR!")

        print("=" * 80)

    def save_report(self, filename: str = "security_check_report.json"):
        """Save security check report to JSON file"""
        report = {
            "security_issues": self.security_issues,
            "warnings": self.warnings,
            "passed_checks": self.passed_checks,
            "summary": {
                "critical_issues": len(self.security_issues),
                "warnings": len(self.warnings),
                "passed_checks": len(self.passed_checks),
            },
        }

        report_path = self.project_root / "reports" / filename
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n📄 Security report saved to: {report_path}")


def main():
    """Main function"""
    checker = SecurityChecker()

    try:
        # Run all checks
        results = checker.run_all_checks()

        # Print report
        checker.print_report()

        # Save report
        checker.save_report()

        # Exit with appropriate code
        if checker.security_issues:
            exit(1)
        else:
            exit(0)

    except Exception as e:
        print(f"❌ Error during security check: {e}")
        exit(1)


if __name__ == "__main__":
    main()
