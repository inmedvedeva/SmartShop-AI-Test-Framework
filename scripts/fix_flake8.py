#!/usr/bin/env python3
"""
Script to automatically fix common flake8 issues
"""

import os
import re
from pathlib import Path


def fix_unused_imports(content):
    """Remove unused imports"""
    lines = content.split("\n")
    fixed_lines = []

    # Common unused imports to remove
    unused_imports = [
        "import os",
        "import sys",
        "from typing import Any",
        "from typing import Dict",
        "from typing import List",
        "from typing import Optional",
        "from typing import Tuple",
        "from typing import Union",
        "from selenium.webdriver.common.keys import Keys",
        "from selenium.webdriver.support import expected_conditions as EC",
        "from selenium.webdriver.support.ui import WebDriverWait",
        "from selenium.webdriver.common.by import By",
        "from selenium.common.exceptions import NoSuchElementException",
        "import pytest",
        "from unittest.mock import MagicMock",
        "from src.core.config.settings import settings",
    ]

    for line in lines:
        should_keep = True
        for unused in unused_imports:
            if line.strip() == unused:
                should_keep = False
                break
        if should_keep:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_bare_except(content):
    """Replace bare except with specific exception handling"""
    # Replace bare except with Exception
    content = re.sub(r"except:", "except Exception:", content)
    return content


def fix_long_lines(content):
    """Break long lines"""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        if len(line) > 79 and not line.strip().startswith("#"):
            # Try to break long lines at appropriate points
            if 'f"' in line and len(line) > 79:
                # Break f-strings
                parts = line.split('f"')
                if len(parts) > 1:
                    # Simple f-string breaking
                    if "logger.info" in line:
                        match = re.search(r'logger\.info\(f"([^"]+)"\)', line)
                        if match:
                            text = match.group(1)
                            if len(text) > 60:
                                # Break into multiple lines
                                words = text.split()
                                lines_parts = []
                                current_line = 'logger.info(f"'
                                for word in words:
                                    if len(current_line + word) > 70:
                                        current_line += '"'
                                        lines_parts.append(current_line)
                                        current_line = '    f"' + word + " "
                                    else:
                                        current_line += word + " "
                                current_line = current_line.rstrip() + '")'
                                lines_parts.append(current_line)
                                fixed_lines.extend(lines_parts)
                                continue
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_file(file_path):
    """Fix a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Apply fixes
        content = fix_unused_imports(content)
        content = fix_bare_except(content)
        content = fix_long_lines(content)

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Fixed: {file_path}")

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")


def main():
    """Main function"""
    project_root = Path(__file__).parent.parent

    # Files to fix
    files_to_fix = [
        "src/core/visual_testing.py",
        "src/main.py",
        "src/ui/pages/automation_exercise_home_page.py",
        "src/ui/pages/home_page.py",
        "src/ui/pages/base_page.py",
        "src/ui/pages/base_home_page.py",
        "src/ui/pages/internet_home_page.py",
        "src/ui/pages/nopcommerce_home_page.py",
        "src/ui/ui_helpers.py",
        "tests/conftest.py",
        "tests/api/test_api_endpoints.py",
        "tests/base_test_classes.py",
        "tests/ui/test_home_page.py",
        "tests/ui/test_nopcommerce_home_page.py",
        "tests/unit/test_ai_data_generator.py",
        "tests/visual/test_applitools_integration.py",
    ]

    for file_path in files_to_fix:
        full_path = project_root / file_path
        if full_path.exists():
            fix_file(full_path)
        else:
            print(f"File not found: {full_path}")


if __name__ == "__main__":
    main()
