#!/usr/bin/env python3
"""
Script to run tests with proper Python path setup
"""
import os
import subprocess
import sys
from pathlib import Path


def run_tests(test_path=None, markers=None, verbose=True):
    """Run tests with proper configuration"""

    # Get project root
    project_root = Path(__file__).parent.absolute()

    # Set up environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if markers:
        cmd.extend(["-m", markers])

    if test_path:
        cmd.append(test_path)

    print(f"🚀 Running tests with PYTHONPATH: {project_root}")
    print(f"📋 Command: {' '.join(cmd)}")
    print("-" * 80)

    try:
        result = subprocess.run(cmd, env=env, cwd=project_root)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Run tests with proper setup")
    parser.add_argument("--test-path", help="Specific test path to run")
    parser.add_argument("--markers", help="Test markers (e.g., api, ui, smoke)")
    parser.add_argument(
        "--quiet", action="store_true", help="Run without verbose output"
    )

    args = parser.parse_args()

    success = run_tests(
        test_path=args.test_path, markers=args.markers, verbose=not args.quiet
    )

    if success:
        print("\n✅ All tests completed successfully!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
